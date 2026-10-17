"""Execute shipped UART-only firmware with a fake clock/UART, no RP2040 hardware."""
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
from tmc2208 import Driver, crc, GCONF, CHOPCONF, CHOPCONF_OFF, CURRENT
from motion_policy import plan_move, uart_motion, PIN_LIMIT, STEPS_PER_REV, VELOCITY_HZ
from controller import Controller


class Uart:
    def __init__(self):
        self.reg = {6: 0x20000100, 0: 0, 0x6C: 0, 0x22: 0, 2: 254, 1: 1, 0x6F: 0}
        self.buffer = bytearray()
        self.drop = None
        self.corrupt = False
        self.no_reply = False
        self.tx_lost = False
        self.writes = []

    def any(self):
        return len(self.buffer)

    def write(self, data):
        if self.tx_lost:
            raise OSError('TX disconnected')
        self.buffer.extend(data)
        if len(data) == 8:
            assert crc(data[:7]) == data[7]
            reg, value = data[2] & 127, int.from_bytes(data[3:7], 'big')
            self.writes.append((reg, value, clock[0]))
            if reg != self.drop:
                self.reg[reg] = (self.reg[reg] & ~value) if reg == 1 else value
                self.reg[2] = (self.reg[2] + 1) & 255
        else:
            assert crc(data[:3]) == data[3]
            reg = data[2]
            if not self.no_reply:
                # These registers must NEVER be read back.
                assert reg not in (0x10, 0x11, 0x13, 0x22)
                reply = bytearray((5, 255, reg))
                reply.extend(self.reg[reg].to_bytes(4, 'big'))
                reply.append(crc(reply) ^ int(self.corrupt))
                self.buffer.extend(reply)
        return len(data)

    def read(self, count=None):
        advance(100)
        count = len(self.buffer) if count is None else min(count, len(self.buffer))
        data = self.buffer[:count]
        del self.buffer[:count]
        return data


class FirmwareTest(unittest.TestCase):
    def setUp(self):
        clock[0] = 0
        self.uart = Uart()
        self.driver = Driver(self.uart)
        self.pending = []
        self.messages = []
        self.app = Controller(self.driver, self.receive, self.messages.append)

    def receive(self):
        advance(10)
        return self.pending.pop(0) if self.pending else ''

    def moving_writes(self):
        return [v for r, v, _ in self.uart.writes if r == 0x22 and v != 0]

    def check_off(self):
        self.assertFalse(self.app.armed)
        self.assertEqual(self.app.position, 0)
        self.assertEqual(self.uart.reg[0x6C] & 15, 0)
        self.assertEqual(self.uart.reg[0x22], 0)

    def test_crc_datasheet_vectors(self):
        self.assertEqual(crc(bytes((5, 0, 0))), 0x48)
        self.assertEqual(crc(bytes((5, 0, 6))), 0x6F)

    def test_config_current_and_off_readback(self):
        self.app.command('ARM MOTOR')
        self.assertTrue(self.app.armed)
        self.assertEqual(self.uart.reg[0x10], CURRENT)
        self.assertEqual(self.uart.reg[0x6C], CHOPCONF_OFF)
        self.assertEqual(self.uart.reg[0], GCONF)
        self.assertEqual(self.driver.counter, self.uart.reg[2])
        self.assertEqual(self.driver.counter, (254 + len(self.uart.writes)) & 255)
        self.assertNotIn(4, [r for r, v, t in self.uart.writes])
        self.assertFalse(self.moving_writes())

    def test_every_lost_configuration_write_disarms(self):
        for reg in (0, 0x6C, 0x10, 0x11, 0x13, 0x22, 1):
            with self.subTest(reg=reg):
                self.setUp()
                self.uart.drop = reg
                self.app.command('ARM MOTOR')
                self.check_off()
                self.assertFalse(self.moving_writes())

    def test_crc_wrong_chip_and_timeout_rejected(self):
        for error in ('crc', 'chip', 'sel', 'timeout'):
            self.setUp()
            if error == 'crc': self.uart.corrupt = True
            elif error == 'chip': self.uart.reg[6] = 0x21000100
            elif error == 'sel': self.uart.reg[6] = 0x20000000
            else: self.uart.no_reply = True
            self.app.command('ARM MOTOR')
            self.check_off()
            self.assertFalse(self.moving_writes())

    def test_signed_velocity_values_and_duration(self):
        # Independent datasheet computation at 12 MHz, MRES=8, FULL_STEPS=20.
        self.assertEqual(STEPS_PER_REV, 160)
        self.assertEqual(uart_motion(160, 120), (447, 500439))
        self.assertEqual(uart_motion(-160, 120), (-447, 500439))
        self.assertEqual(uart_motion(160, 2), (7, 31956602))
        for rpm in (2, 5, 10, 20, 40, 60, 120):
            value, duration = uart_motion(40, rpm)
            self.assertAlmostEqual(value * VELOCITY_HZ * duration / 1e6, 40, places=3)
        for invalid in (0, 1 << 23, -(1 << 23) - 1, 1.5):
            with self.assertRaises(ValueError): self.driver.start(invalid)

    def test_forward_reverse_and_stop_order(self):
        self.app.command('ARM MOTOR')
        self.app.command('S 120')
        self.app.command('M 1')
        self.app.command('M -1')
        self.assertEqual(self.moving_writes(), [447, 0x1000000 - 447])
        self.assertEqual(self.app.position, 0)
        self.assertEqual(self.uart.reg[0x22], 0)
        self.assertEqual(self.uart.reg[0x6C], CHOPCONF_OFF)
        writes = self.uart.writes
        for i, (reg, value, at) in enumerate(writes):
            if reg == 0x22 and value:
                self.assertEqual(writes[i + 1][:2], (0x6C, CHOPCONF))
                stop_index = next(j for j in range(i + 2, len(writes))
                                  if writes[j][:2] == (0x6C, CHOPCONF_OFF))
                self.assertEqual(writes[stop_index + 1][:2], (0x22, 0))
                # Timed interval includes acknowledgment overhead, does not
                # append it to the requested run duration.
                elapsed = writes[stop_index][2] - writes[i + 1][2]
                self.assertGreaterEqual(elapsed, 500439)
                self.assertLess(elapsed, 501000)

    def test_cycle_and_both_limits(self):
        self.app.command('ARM PIN')
        self.app.command('S 120')
        self.app.command('C 10')
        self.assertEqual(self.app.position, 0)
        self.assertEqual(len(self.moving_writes()), 30)
        self.assertTrue(all(v == (447 if i % 3 != 1 else 0x1000000 - 447)
                            for i, v in enumerate(self.moving_writes())))
        self.app.command('M 0.5')
        self.assertEqual(self.app.position, PIN_LIMIT)
        previous = len(self.moving_writes())
        self.app.command('M 0.01')
        self.check_off()
        self.assertEqual(len(self.moving_writes()), previous)
        with self.assertRaises(ValueError): plan_move(True, -PIN_LIMIT, -.01)

    def test_stop_during_motion_and_no_backlog(self):
        for inputs in (['', '!', 'M 1\n'], ['', 'OF', 'F\n']):
            self.setUp()
            self.app.command('ARM MOTOR')
            self.pending = list(inputs)
            self.app.command('M 1')
            self.check_off()
            previous = len(self.moving_writes())
            self.app.poll()
            self.assertEqual(len(self.moving_writes()), previous)
            self.assertEqual(previous, 1)

    def test_stop_cancels_same_batch_commands(self):
        self.pending = ['ARM PIN\nM 1\n!']
        self.app.poll()
        self.check_off()
        self.assertFalse(self.moving_writes())

    def test_parser_overflow_nonfinite_and_limits(self):
        for text in ('S nan', 'S inf', 'S 1', 'S 121', 'M nan', 'M inf',
                     'M 0', 'M 1.1', 'C 0', 'C 21', 'C 1.5', 'M 0.25 junk'):
            self.app.command('ARM MOTOR')
            previous = len(self.moving_writes())
            self.app.command(text)
            self.check_off()
            self.assertEqual(len(self.moving_writes()), previous)
        self.pending = ['x' * 60 + '\nARM PIN\n']
        self.app.poll()
        self.check_off()

    def test_idle_run_limit_and_reset(self):
        self.app.command('ARM MOTOR')
        advance(30000000)
        self.app.poll()
        self.check_off()
        self.app.command('ARM PIN')
        self.app.command('S 2')
        self.app.command('C 20')
        self.check_off()
        self.assertTrue(any('120 s' in m for m in self.messages))
        self.app = Controller(self.driver, self.receive, self.messages.append)
        self.check_off()
        self.app.command('M 1')
        self.check_off()

    def test_live_faults_disarm_and_do_not_rearm(self):
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
            self.assertFalse(self.moving_writes())

    def test_health_accepts_deliberate_on_off_changes(self):
        self.app.command('ARM MOTOR')
        self.driver.start(447)
        self.driver.health()
        self.assertEqual(self.driver.chopconf, CHOPCONF)
        self.driver.stop()
        self.driver.health()
        self.assertEqual(self.driver.chopconf, CHOPCONF_OFF)

    def test_rx_lost_during_motion_still_sends_stop(self):
        self.app.command('ARM MOTOR')
        original = self.driver.health
        def lose_rx():
            self.uart.no_reply = True
            original()
        original_start = self.driver.start
        def start_then_lose(velocity):
            at = original_start(velocity)
            self.driver.health = lose_rx
            return at
        self.driver.start = start_then_lose
        self.app.command('M 1')
        self.check_off()  # TX still works, raw stop actually reached fake chip
        self.assertFalse(self.app.stop_confirmed)
        self.assertTrue(any('STOP UNCONFIRMED' in m for m in self.messages))
        self.assertTrue(any(r == 0x22 and v == 0 for r, v, t in self.uart.writes[-4:]))

    def test_total_uart_loss_reports_unconfirmed_stop(self):
        self.app.command('ARM MOTOR')
        self.driver.start(447)
        self.uart.tx_lost = True
        self.app.command('OFF')
        self.assertFalse(self.app.armed)
        self.assertFalse(self.app.stop_confirmed)
        # Deliberately NOT asserting a physical stop: software cannot deliver it.
        self.assertEqual(self.uart.reg[0x6C], CHOPCONF)
        self.assertEqual(self.uart.reg[0x22], 447)
        self.assertTrue(any('STOP UNCONFIRMED' in m for m in self.messages))

    def test_main_uses_only_uart_pins_and_stops_on_interrupt(self):
        pins = []
        def make_pin(number):
            pins.append(number)
            self.assertIn(number, (4, 5))
            return number
        fake_machine = types.SimpleNamespace(Pin=make_pin, UART=lambda *a, **k: self.uart)
        fake_select = types.SimpleNamespace(poll=lambda: types.SimpleNamespace(
            register=lambda *a: None, poll=lambda *a: []), POLLIN=1)
        sleeps = [0]
        def interrupt(milliseconds):
            sleeps[0] += 1
            if sleeps[0] == 4:  # after the three initial stop writes, in main loop
                self.uart.reg[0x6C] = CHOPCONF
                self.uart.reg[0x22] = 447
                raise KeyboardInterrupt()
            advance(milliseconds * 1000)
        with patch.dict(sys.modules, {'machine': fake_machine, 'select': fake_select}):
            with patch.object(time, 'sleep_ms', interrupt):
                with self.assertRaises(KeyboardInterrupt):
                    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'main.py'))
        self.assertEqual(pins, [4, 5])
        self.assertEqual(self.uart.reg[0x6C], CHOPCONF_OFF)
        self.assertEqual(self.uart.reg[0x22], 0)

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
