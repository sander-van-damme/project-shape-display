"""Blocking, bounded bench motion with frequent USB/driver checks; no queue."""
from time import ticks_us, ticks_ms, ticks_diff, sleep_us
from motion_policy import (plan_move, speed, cycles, STEPS_PER_REV,
                           IDLE_MS, MAX_RUN_MS)
REVERSE_DIR = False


class Controller:
    def __init__(self, step, direction, enable, driver, receive, report=print):
        self.step, self.direction, self.enable = step, direction, enable
        self.driver, self.receive, self.report = driver, receive, report
        self.rpm = 5
        self.line = ''
        self.discard = False
        self.off()
        self.last = ticks_ms()
        self.run_start = self.last
        self.last_health = self.last

    def off(self):
        self.enable.value(1)
        self.step.value(0)
        self.armed = False
        self.pin_mode = False
        self.position = 0

    def fault(self, message):
        self.off()
        self.line = ''
        self.discard = False
        self.report('STOP/OFF: ' + message + '; centre invalid; new ARM required')

    def guard(self):
        # No USB backlog: input during motion is discarded except immediate !.
        data = self.receive()
        if '!' in data:
            self.fault('!')
            return False
        if ticks_diff(ticks_ms(), self.run_start) >= MAX_RUN_MS:
            self.fault('120 s run limit')
            return False
        if ticks_diff(ticks_ms(), self.last_health) >= 100:
            self.driver.health()  # exception caught by command(), EN high first
            self.last_health = ticks_ms()
        return self.armed

    def wait(self, duration):
        start = ticks_us()
        while ticks_diff(ticks_us(), start) < duration:
            if not self.guard():
                return False
            sleep_us(100)
        return True

    def move(self, revs):
        if not self.armed:
            raise ValueError('ARM required')
        steps = plan_move(self.pin_mode, self.position, revs)
        self.driver.health()  # verify before every segment and before EN low
        self.last_health = ticks_ms()
        self.direction.value((steps > 0) ^ REVERSE_DIR)
        sleep_us(10)
        self.enable.value(0)
        if not self.wait(5000):
            return False
        count = abs(steps)
        for i in range(count):
            if not self.guard():
                return False
            edge = min(i, count - 1 - i, 16)
            velocity = min(self.rpm, 2 + (self.rpm - 2) * edge / 16)
            period = int(60000000 / (STEPS_PER_REV * velocity))
            self.step.value(1)
            sleep_us(5)
            self.step.value(0)
            self.position += 1 if steps > 0 else -1
            if not self.wait(period - 5):
                return False
        self.last = ticks_ms()
        self.report('DONE commanded rev=%.3f' % (self.position / STEPS_PER_REV))
        return True

    def command(self, text):
        self.last = ticks_ms()
        try:
            if text == 'OFF':
                self.fault('OFF')
            elif text == '?':
                self.report('ARM MOTOR | ARM PIN | S 2..120 | M -1..1 | C 1..20 | OFF | !')
            elif text in ('ARM MOTOR', 'ARM PIN'):
                if self.armed:
                    raise ValueError('OFF first; detach pin or manually recentre')
                self.off()
                self.driver.configure()
                self.pin_mode = text == 'ARM PIN'
                self.armed = True
                self.last_health = ticks_ms()
                self.last = ticks_ms()
                # EN remains HIGH: first explicit M/C enables bridge.
                self.report('ARMED ' + ('PIN; manual centre declared' if self.pin_mode
                                        else 'MOTOR; pin must be detached'))
            elif text.startswith('S '):
                self.rpm = speed(float(text[2:]))
                self.report('Speed set %.1f rpm' % self.rpm)
            elif text.startswith('M '):
                self.run_start = ticks_ms()
                self.move(float(text[2:]))
            elif text.startswith('C '):
                count = cycles(float(text[2:]))
                if not self.armed or not self.pin_mode or self.position != 0:
                    raise ValueError('C requires PIN at declared zero')
                self.run_start = ticks_ms()
                for index in range(count):
                    for rev in (.5, -1, .5):
                        if not self.move(rev) or not self.wait(300000):
                            return
                    self.report('CYCLE %d' % (index + 1))
            else:
                raise ValueError('unknown command; ? for help')
        except (ValueError, OSError) as error:
            # Conservative: rejected/malformed command ALSO disarms.
            self.fault(str(error))

    def poll(self):
        if self.armed:
            if ticks_diff(ticks_ms(), self.last) >= IDLE_MS:
                self.fault('30 s idle')
            elif ticks_diff(ticks_ms(), self.last_health) >= 100:
                try:
                    self.driver.health()
                    self.last_health = ticks_ms()
                except OSError as error:
                    self.fault(str(error))
        # Read a complete currently available batch before executing anything.
        # A stop anywhere in that batch cancels all older partial/full lines.
        data = self.receive()
        if '!' in data:
            self.fault('!')
            return
        for char in data:
            if char == '\r':
                continue
            if char == '\n':
                line, discarded = self.line, self.discard
                self.line, self.discard = '', False
                if discarded:
                    self.fault('overlong command')
                    return
                if line:
                    self.command(line)
                    # Discard rest of batch: no queued moves following M/C/ARM.
                    return
            elif not self.discard:
                if len(self.line) >= 39:
                    self.discard = True
                else:
                    self.line += char
