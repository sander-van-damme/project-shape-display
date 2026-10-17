"""Hardware-free execution of the shipped firmware, not a separate motion model.
Run: python3 -m unittest discover -s .../pico/tests -v
"""
import sys
from pathlib import Path
import time
import unittest
from unittest.mock import patch
import types
import runpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
clock = [0]
time.ticks_ms = lambda: clock[0] // 1000
time.ticks_us = lambda: clock[0]
time.ticks_diff = lambda a, b: a - b

def advance(n):
    clock[0] += n

time.sleep_us = advance
time.sleep_ms = lambda n: advance(n * 1000)
from tmc2208 import Driver, crc, GCONF, CHOPCONF, CURRENT
from motion_policy import plan_move, speed, cycles, PIN_LIMIT, STEPS_PER_REV
from controller import Controller


class Uart:
    def __init__(self):
        self.reg = {6: 0x20000100, 0: 0, 0x6C: 0, 2: 254, 1: 1, 0x6F: 0}
        self.buffer = bytearray()
        self.drop = None
        self.corrupt = False
        self.no_reply = False
        self.writes = []

    def any(self):
        return len(self.buffer)

    def write(self, data):
        self.buffer.extend(data)
        if len(data) == 8:
            assert crc(data[:7]) == data[7]
            reg, value = data[2] & 127, int.from_bytes(data[3:7], 'big')
            self.writes.append((reg, value))
            if reg != self.drop:
                self.reg[reg] = (self.reg[reg] & ~value) if reg == 1 else value
                self.reg[2] = (self.reg[2] + 1) & 255
        else:
            assert crc(data[:3]) == data[3]
            reg = data[2]
            if self.no_reply:
                return
            # IHOLD_IRUN, TPOWERDOWN, TPWMTHRS, VACTUAL are write-only.
            assert reg not in (0x10, 0x11, 0x13, 0x22)
            reply = bytearray((5, 255, reg))
            reply.extend(self.reg[reg].to_bytes(4, 'big'))
            reply.append(crc(reply) ^ int(self.corrupt))
            self.buffer.extend(reply)

    def read(self, count=None):
        advance(100)
        count = len(self.buffer) if count is None else min(count, len(self.buffer))
        data = self.buffer[:count]
        del self.buffer[:count]
        return data


class Pin:
    def __init__(self, value=0):
        self.state = value
        self.rises = 0

    def value(self, value=None):
        if value is not None:
            self.rises += int(self.state == 0 and value == 1)
            self.state = value
        return self.state


class FirmwareTest(unittest.TestCase):
    def setUp(self):
        clock[0] = 0
        self.uart = Uart()
        self.driver = Driver(self.uart)
        self.step, self.direction, self.enable = Pin(), Pin(), Pin(1)
        self.pending = []
        self.messages = []
        self.app = Controller(self.step, self.direction, self.enable, self.driver,
                              self.receive, self.messages.append)

    def receive(self):
        advance(10)
        return self.pending.pop(0) if self.pending else ''

    def check_off(self):
        self.assertFalse(self.app.armed)
        self.assertEqual(self.enable.value(), 1)
        self.assertEqual(self.step.value(), 0)
        self.assertEqual(self.app.position, 0)

    def test_crc_datasheet_vectors(self):
        # Independent fixed protocol vectors, also used by published TMC tools.
        self.assertEqual(crc(bytes((5, 0, 0))), 0x48)
        self.assertEqual(crc(bytes((5, 0, 6))), 0x6F)

    def test_config_writeonly_ack_and_wrap(self):
        self.app.command('ARM MOTOR')
        self.assertTrue(self.app.armed)
        self.assertEqual(self.enable.value(), 1)
        self.assertEqual(self.uart.reg[0x10], CURRENT)
        self.assertEqual(self.uart.reg[0x6C], CHOPCONF)
        self.assertEqual(self.uart.reg[0], GCONF)
        self.assertEqual(self.driver.counter, 5)  # seven writes from 254
        self.assertNotIn(4, [r for r, v in self.uart.writes])  # no OTP_PROG

    def test_every_lost_configuration_write_fails_closed(self):
        for reg in (0, 0x6C, 0x10, 0x11, 0x13, 0x22, 1):
            with self.subTest(reg=reg):
                self.setUp()
                self.uart.drop = reg
                self.app.command('ARM MOTOR')
                self.check_off()
                self.assertEqual(self.step.rises, 0)

    def test_crc_and_wrong_chip_rejected(self):
        for error in ('crc', 'chip', 'sel'):
            self.setUp()
            if error == 'crc': self.uart.corrupt = True
            elif error == 'chip': self.uart.reg[6] = 0x21000100
            else: self.uart.reg[6] = 0x20000000
            self.app.command('ARM MOTOR')
            self.check_off()

    def test_cycle_and_both_limits(self):
        self.app.command('ARM PIN')
        self.app.command('S 120')
        self.app.command('C 10')
        self.assertEqual(self.app.position, 0)
        self.assertEqual(self.step.rises, 3200)
        self.app.command('M 0.5')
        self.assertEqual(self.app.position, PIN_LIMIT)
        previous = self.step.rises
        self.app.command('M 0.01')
        self.check_off()
        self.assertEqual(self.step.rises, previous)
        with self.assertRaises(ValueError): plan_move(True, -PIN_LIMIT, -.01)

    def test_stop_during_motion_and_no_backlog(self):
        self.app.command('ARM MOTOR')
        self.pending = ['M 1\n', '', '!M 1\n']
        self.app.command('M 1')
        self.check_off()
        self.assertLess(self.step.rises, STEPS_PER_REV)
        previous = self.step.rises
        self.app.poll()
        self.assertEqual(self.step.rises, previous)

    def test_stop_cancels_same_batch_commands(self):
        self.pending = ['ARM PIN\nM 1\n!']
        self.app.poll()
        self.check_off()
        self.assertEqual(self.step.rises, 0)

    def test_parser_overflow_nonfinite_and_limits(self):
        for text in ('S nan', 'S inf', 'S 1', 'S 121', 'M nan', 'M inf',
                     'M 0', 'M 1.1', 'C 0', 'C 21', 'C 1.5', 'M 0.25 junk'):
            self.app.command('ARM MOTOR')
            previous = self.step.rises
            self.app.command(text)
            self.check_off()
            self.assertEqual(self.step.rises, previous)
        self.pending = ['x' * 60 + '\nARM PIN\n']
        self.app.poll()
        self.check_off()

    def test_idle_run_limit_and_reset_recovery(self):
        self.app.command('ARM MOTOR')
        advance(30000000)
        self.app.poll()
        self.check_off()
        self.app.command('ARM PIN')
        self.app.command('S 2')
        self.app.command('C 20')
        self.check_off()
        self.assertTrue(any('120 s' in m for m in self.messages))
        # Model hard reset on supervisor RUN. Actual analogue timing is NOT
        # simulated; this checks that a fresh application never resumes motion.
        self.app = Controller(self.step, self.direction, self.enable, self.driver,
                              self.receive, self.messages.append)
        self.check_off()
        self.app.command("M 1")
        self.check_off()

    def test_live_fault_and_no_automatic_rearm(self):
        for fault in ('reset', 'config', 'ifcnt', 'temp', 'short', 'crc'):
            self.setUp()
            self.app.command('ARM MOTOR')
            if fault == 'reset': self.uart.reg[1] = 1
            elif fault == 'config': self.uart.reg[0] = 0
            elif fault == 'ifcnt': self.uart.reg[2] = 0
            elif fault == 'temp': self.uart.reg[0x6F] = 1
            elif fault == 'short': self.uart.reg[0x6F] = 4
            else: self.uart.corrupt = True
            advance(100000)
            self.app.poll()
            self.check_off()
            self.uart.corrupt = False
            self.app.command('M 1')
            self.check_off()
            self.assertEqual(self.step.rises, 0)

    def test_uart_failure_during_motion(self):
        self.app.command('ARM MOTOR')
        original = self.driver.health
        calls = [0]
        def fail_after_segment_start():
            calls[0] += 1
            if calls[0] == 2:
                raise OSError('injected cable failure')
            return original()
        self.driver.health = fail_after_segment_start
        self.app.command('M 1')
        self.check_off()
        self.assertGreater(self.step.rises, 0)
        self.assertLess(self.step.rises, STEPS_PER_REV)

    def test_uart_timeout(self):
        self.uart.no_reply = True
        self.app.command('ARM MOTOR')
        self.check_off()
        self.assertEqual(self.step.rises, 0)
        self.assertGreaterEqual(clock[0], 35000)

    def test_main_boot_and_keyboardinterrupt_cleanup(self):
        pins = {}
        def make_pin(number, *args, **kwargs):
            if number not in pins:
                pins[number] = Pin(kwargs.get('value', 0))
            return pins[number]
        make_pin.OUT = 1
        fake_machine = types.SimpleNamespace(Pin=make_pin, UART=lambda *a, **k: self.uart)
        fake_select = types.SimpleNamespace(poll=lambda: types.SimpleNamespace(
            register=lambda *a: None, poll=lambda *a: []), POLLIN=1)
        def interrupt(_):
            # Unexpected exit while outputs were energized must still disable.
            pins[6].value(0)
            pins[2].value(1)
            raise KeyboardInterrupt()
        with patch.dict(sys.modules, {'machine': fake_machine, 'select': fake_select}):
            with patch.object(time, 'sleep_ms', interrupt):
                with self.assertRaises(KeyboardInterrupt):
                    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'main.py'))
        self.assertEqual(pins[6].value(), 1)
        self.assertEqual(pins[2].value(), 0)

    def test_bounds_all_positions(self):
        for pos in range(-PIN_LIMIT, PIN_LIMIT + 1):
            for n in range(-STEPS_PER_REV, STEPS_PER_REV + 1):
                try:
                    result = plan_move(True, pos, n / STEPS_PER_REV)
                except ValueError:
                    self.assertTrue(n == 0 or abs(pos + n) > PIN_LIMIT)
                else:
                    self.assertEqual(n, result)
                    self.assertLessEqual(abs(pos + result), PIN_LIMIT)


if __name__ == '__main__':
    unittest.main()
