"""Transport tests; a cycle interpreter executes the real PIO function's AST.

The interpreter models shift registers/FIFOs, delays, sampled pins and GPIO
direction. It is evidence about software timing, not a Pico hardware test.
"""
import ast
import importlib.util
import os
from pathlib import Path
import random
import unittest
from unittest.mock import patch

SOURCE = Path(os.environ.get("E302_FIRMWARE", Path(__file__).parents[1] / "main.py"))
SPEC = importlib.util.spec_from_file_location("transport_firmware_under_test", SOURCE)
fw = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fw)


class PIOModel:
    """Instruction-level interpreter for the PIO instructions used by firmware."""
    def __init__(self, words, reply=b"", delay_bits=8, reply_bit_cycles=8,
                 corrupt_stop=None):
        module = ast.parse(SOURCE.read_text())
        func = next(node for node in ast.walk(module)
                    if isinstance(node, ast.FunctionDef) and node.name == "_tmc_half_duplex")
        self.program, self.labels = [], {}
        for statement in func.body:
            call = statement.value
            delay = 0
            if isinstance(call, ast.Subscript):
                index = call.slice
                if hasattr(ast, "Index") and isinstance(index, ast.Index):
                    index = index.value
                delay = ast.literal_eval(index)
                call = call.value
            name = call.func.id
            args = [a.id if isinstance(a, ast.Name) else ast.literal_eval(a)
                    for a in call.args]
            if name == "label":
                self.labels[args[0]] = len(self.program)
            elif name not in ("wrap_target", "wrap"):
                self.program.append((name, args, delay))
        self.tx, self.rx = list(words), []
        self.pc = self.cycle = self.x = self.y = self.isr = 0
        self.osr = self.in_count = self.out_count = 0
        self.direction = 0
        self.output = 1
        self.output_events, self.direction_events = [], []
        self.reply_start = None
        self.reply_bits = []
        self.delay_bits, self.reply_bit_cycles = delay_bits, reply_bit_cycles
        self.contention = False
        for i, byte in enumerate(reply):
            self.reply_bits.extend([0] + [(byte >> bit) & 1 for bit in range(8)] +
                                   [0 if corrupt_stop == i else 1])

    def pin(self):
        external = 1
        if self.reply_start is not None and self.cycle >= self.reply_start:
            offset = (self.cycle - self.reply_start) / self.reply_bit_cycles
            if offset < len(self.reply_bits):
                external = self.reply_bits[int(offset)]
            if offset < len(self.reply_bits) + 4 and self.direction:
                self.contention = True
        return self.output if self.direction else external

    def push(self):
        if len(self.rx) >= 4:
            raise AssertionError("PIO FIFO would overflow/stall with no CPU servicing")
        self.rx.append(self.isr & 0xFFFFFFFF)
        self.isr = self.in_count = 0

    def run(self, limit=5000):
        while self.cycle < limit:
            name, args, delay = self.program[self.pc]
            next_pc = (self.pc + 1) % len(self.program)
            if name == "pull":
                if not self.tx:
                    break
                self.osr, self.out_count = self.tx.pop(0), 0
            elif name == "out":
                if self.out_count >= 32:
                    if not self.tx:
                        raise AssertionError("TX starvation")
                    self.osr, self.out_count = self.tx.pop(0), 0
                target, count = args
                value = self.osr & ((1 << count) - 1)
                self.osr >>= count
                self.out_count += count
                if target in ("x", "y"):
                    setattr(self, target, value)
                elif target == "pins":
                    self.output = value
                    self.output_events.append((self.cycle, value))
            elif name == "set":
                target, value = args
                if target == "pindirs":
                    if self.direction and not value:
                        self.reply_start = self.cycle + 8 * self.delay_bits
                    self.direction = value
                    self.direction_events.append((self.cycle, value))
                else:
                    setattr(self, target, value)
            elif name == "wait":
                if self.pin() != args[0]:
                    next_pc = self.pc
            elif name == "in_":
                self.isr = (self.isr >> 1) | (self.pin() << 31)
                self.in_count += 1
                if self.in_count == 24:
                    self.push()
            elif name == "jmp":
                if len(args) == 1:
                    branch, label = True, args[0]
                else:
                    condition, label = args
                    if condition in ("x_dec", "y_dec"):
                        register = condition[0]
                        value = getattr(self, register)
                        branch = value != 0
                        setattr(self, register, (value - 1) & 0xFFFFFFFF)
                    elif condition == "not_y":
                        branch = self.y == 0
                    elif condition == "pin":
                        branch = bool(self.pin())
                    else:
                        raise AssertionError(condition)
                if branch:
                    next_pc = self.labels[label]
            elif name == "push":
                self.push()
            elif name == "mov":
                setattr(self, args[0], getattr(self, args[1]))
            else:
                raise AssertionError(name)
            self.pin()  # Check drive contention on every instruction.
            self.pc = next_pc
            self.cycle += 1 + delay
        return self.rx


class Clock:
    def __init__(self):
        self.now = 0

    def ticks(self):
        self.now += 2
        return self.now

    def sleep(self, delay):
        self.now += delay


class FakeUART:
    def __init__(self, reply=b"", echo=True, change_echo=False, short=False,
                 trailing=b"", initial=b""):
        self.buffer = bytearray(initial)
        self.reply, self.echo, self.change_echo = reply, echo, change_echo
        self.short, self.trailing, self.writes = short, trailing, []
        self.closed = False

    def any(self):
        return len(self.buffer)

    def read(self, count=None):
        count = len(self.buffer) if count is None else count
        result = bytes(self.buffer[:count])
        del self.buffer[:count]
        return result

    def write(self, packet):
        self.writes.append(bytes(packet))
        echo = bytearray(packet) if self.echo else bytearray()
        if self.change_echo:
            echo[0] ^= 1
        self.buffer.extend(echo + self.reply + self.trailing)
        return len(packet) - (1 if self.short else 0)

    def deinit(self):
        self.closed = True


class FakePin:
    IN, PULL_UP = 0, 1

    def __init__(self, level=1):
        self.level, self.released = level, False

    def value(self):
        return self.level

    def init(self, *args):
        self.released = True


class FakeSM:
    def __init__(self, reply=None, corrupt_stop=None):
        self.tx, self.rx = [], []
        self.reply, self.corrupt_stop = reply, corrupt_stop
        self.enabled = False

    def put(self, word):
        self.tx.append(word)

    def active(self, active):
        self.enabled = bool(active)
        if active and self.reply is not None:
            self.rx = PIOModel(self.tx, self.reply, corrupt_stop=self.corrupt_stop).run()
            self.tx = []

    def rx_fifo(self):
        return len(self.rx)

    def get(self):
        return self.rx.pop(0)


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.patch_ticks = patch.object(fw, "_uart_ticks_us", self.clock.ticks)
        self.patch_sleep = patch.object(fw, "_uart_sleep_us", self.clock.sleep)
        self.patch_ticks.start()
        self.patch_sleep.start()
        self.addCleanup(self.patch_ticks.stop)
        self.addCleanup(self.patch_sleep.stop)
        self.request = bytes.fromhex("05 00 00 48")
        self.reply = bytes.fromhex("05 ff 00 00 00 01 c5 e4")

    def pio(self, reply=None, corrupt_stop=None, level=1):
        transport = fw.PIOUARTTransport.__new__(fw.PIOUARTTransport)
        transport._setup(115200, 20)
        transport.pin = FakePin(level)
        transport.sm = FakeSM(reply, corrupt_stop)
        transport._init_sm = lambda: None
        return transport

    def test_crc_known_vectors_and_single_bit_detection(self):
        self.assertEqual(fw.tmc_crc(bytes.fromhex("05 00 00")), 0x48)
        self.assertEqual(fw.tmc_crc(bytes.fromhex("05 00 06")), 0x6F)
        data = bytes.fromhex("05 00 80 00 00 01 c5")
        checksum = fw.tmc_crc(data)
        for bit in range(len(data) * 8):
            corrupted = bytearray(data)
            corrupted[bit // 8] ^= 1 << (bit % 8)
            self.assertNotEqual(fw.tmc_crc(corrupted), checksum)

    def test_hardware_echo_reply_stale_and_successive_write(self):
        uart = FakeUART(self.reply, initial=b"stale")
        transport = fw.HardwareUARTTransport(uart)
        self.assertEqual(transport.exchange(self.request, 8), self.reply)
        self.assertEqual(transport.stats["stale_bytes"], 5)
        uart.reply = b""
        self.assertEqual(transport.exchange(bytes(range(8))), b"")
        self.assertEqual(transport.stats["exchanges"], 2)
        self.assertEqual(transport.stats["errors"], 0)

    def test_hardware_missing_echo_and_truncated_reply(self):
        for uart in (FakeUART(echo=False), FakeUART(self.reply[:-1])):
            transport = fw.HardwareUARTTransport(uart)
            with self.assertRaisesRegex(OSError, "timeout"):
                transport.exchange(self.request, 8)
            self.assertEqual(transport.stats["timeouts"], 1)
            self.assertEqual(transport.stats["recoveries"], 1)

    def test_hardware_corrupt_echo_short_write_and_extra_data(self):
        for uart, message in ((FakeUART(self.reply, change_echo=True), "echo"),
                              (FakeUART(short=True), "short write"),
                              (FakeUART(self.reply, trailing=b"x"), "trailing")):
            transport = fw.HardwareUARTTransport(uart)
            with self.assertRaisesRegex(OSError, message):
                transport.exchange(self.request, 8)
            self.assertEqual(transport.stats["errors"], 1)

    def test_hardware_recovers_for_next_command_without_reinit(self):
        uart = FakeUART(echo=False)
        transport = fw.HardwareUARTTransport(uart)
        with self.assertRaises(OSError):
            transport.exchange(self.request, 8)
        uart.echo, uart.reply = True, self.reply
        self.assertEqual(transport.exchange(self.request, 8), self.reply)

    def test_frame_packing_exact_start_data_stop_and_fifo_capacity(self):
        for packet in (self.request, bytes(range(8))):
            words = fw._pio_tx_words(packet, 0)
            self.assertLessEqual(len(words), 4)
            model = PIOModel(words)
            self.assertEqual(model.run(), [1])
            expected = []
            for byte in packet:
                expected += [0] + [(byte >> bit) & 1 for bit in range(8)] + [1]
            self.assertEqual([v for _, v in model.output_events], expected)
            times = [t for t, _ in model.output_events]
            self.assertTrue(all(b - a == 8 for a, b in zip(times, times[1:])))
            self.assertEqual(model.direction_events[-1][0] - times[-1], 8)
            self.assertEqual(model.direction, 0)
            self.assertLessEqual(len(model.program), 32)

    def test_pio_receives_without_cpu_fifo_service_and_no_contention(self):
        rng = random.Random(302)
        for bit_cycles in (7.84, 8, 8.16):
            for _ in range(20):
                reply = bytes(rng.randrange(256) for _ in range(8))
                model = PIOModel(fw._pio_tx_words(self.request, 8), reply,
                                 reply_bit_cycles=bit_cycles)
                words = model.run()
                self.assertEqual(len(words), 4)
                self.assertEqual(words[-1], 1)
                actual = bytearray()
                for count, word in zip((3, 3, 2), words):
                    actual.extend((word >> (32 - count * 8)).to_bytes(count, "little"))
                self.assertEqual(actual, reply)
                self.assertFalse(model.contention)

    def test_pio_transport_parser_and_repeated_transactions(self):
        transport = self.pio(self.reply)
        for _ in range(3):
            self.assertEqual(transport.exchange(self.request, 8), self.reply)
            self.assertFalse(transport.sm.enabled)
        transport.sm.reply = b""
        self.assertEqual(transport.exchange(bytes(range(8))), b"")

    def test_pio_bad_stop_bit_at_each_byte(self):
        with patch.object(fw, "_transport_machine", type("Machine", (), {"Pin": FakePin})):
            for byte in range(8):
                transport = self.pio(self.reply, corrupt_stop=byte)
                with self.assertRaisesRegex(OSError, "framing"):
                    transport.exchange(self.request, 8)
                self.assertTrue(transport.pin.released)
                self.assertEqual(transport.stats["framing_errors"], 1)

    def test_pio_timeout_and_stuck_bus_release_pin(self):
        with patch.object(fw, "_transport_machine", type("Machine", (), {"Pin": FakePin})):
            for level in (0, 1):
                transport = self.pio(level=level)
                with self.assertRaisesRegex(OSError, "timeout|stuck"):
                    transport.exchange(self.request, 8)
                self.assertTrue(transport.pin.released)
                self.assertFalse(transport.sm.enabled)
                self.assertEqual(transport.stats["timeouts"], 1)

    def test_validation_does_not_touch_hardware(self):
        uart = FakeUART()
        transport = fw.HardwareUARTTransport(uart)
        with self.assertRaises(ValueError):
            transport.exchange(b"x", 8)
        transport.timeout_us = 1
        with self.assertRaisesRegex(ValueError, "timeout"):
            transport.exchange(self.request, 8)
        self.assertEqual(uart.writes, [])
        transport.close()
        with self.assertRaisesRegex(OSError, "closed"):
            transport.exchange(self.request)


if __name__ == "__main__":
    unittest.main()
