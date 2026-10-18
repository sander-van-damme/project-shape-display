"""Driver tests against register/serial hardware models, never physical passes."""
import importlib.util
import math
from pathlib import Path
import struct
import unittest


SOFTWARE = Path(__file__).resolve().parents[1]


def load_firmware():
    path = SOFTWARE / "main.py"
    spec = importlib.util.spec_from_file_location("driver_test_firmware", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fw = load_firmware()


class Float32(float):
    """Round every operation as RP2040's MicroPython single precision does."""
    def __new__(cls, value):
        return float.__new__(cls, struct.unpack("f", struct.pack("f", value))[0])

    def __mul__(self, other):
        return Float32(float(self) * float(other))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Float32(float(self) / float(other))

    def __sub__(self, other):
        return Float32(float(self) - float(other))

    def __add__(self, other):
        return Float32(float(self) + float(other))


class RegisterTransport:
    def __init__(self):
        self.registers = {0x06: 0x20000100, 0x01: 1, 0x02: 0}
        self.stats = {"exchanges": 0, "tx_bytes": 0, "rx_bytes": 0, "errors": 0}
        self.packets = []
        self.writes = []
        self.reads = []
        self.drop_write = False
        self.corrupt_crc = False
        self.wrong_header = False
        self.short_reply = False
        self.timeout = False
        self.fail_write_regs = set()

    def exchange(self, packet, reply_length=0):
        self.stats["exchanges"] += 1
        self.stats["tx_bytes"] += len(packet)
        self.packets.append(bytes(packet))
        if fw.tmc_crc(packet[:-1]) != packet[-1]:
            raise AssertionError("Driver emitted invalid CRC")
        if packet[0:2] != bytes((5, 0)):
            raise AssertionError("TMC2208 only has address 0")
        reg = packet[2] & 0x7F
        if packet[2] & 0x80:
            if reply_length != 0 or len(packet) != 8:
                raise AssertionError("invalid write framing")
            value = int.from_bytes(packet[3:7], "big")
            self.writes.append((reg, value))
            if reg in self.fail_write_regs:
                raise OSError("simulated TX failure")
            if self.drop_write:
                self.drop_write = False
                return b""
            self.registers[0x02] = (self.registers[0x02] + 1) & 255
            if reg == 0x01:
                self.registers[reg] &= ~value
            else:
                self.registers[reg] = value
            return b""
        if reply_length != 8 or len(packet) != 4:
            raise AssertionError("invalid read framing")
        self.reads.append(reg)
        if self.timeout:
            self.stats["errors"] += 1
            raise OSError("simulated reply timeout")
        response = bytearray((5, 255, reg))
        response.extend(self.registers.get(reg, 0).to_bytes(4, "big"))
        if self.wrong_header:
            response[1] = 0
        response.append(fw.tmc_crc(response))
        if self.corrupt_crc:
            response[-1] ^= 1
        self.stats["rx_bytes"] += len(response)
        return bytes(response[:-1] if self.short_reply else response)


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.transport = RegisterTransport()
        self.driver = fw.Driver(self.transport, {})

    def configure(self):
        self.driver.configure()

    def test_conservative_registers_match_working_e301(self):
        self.configure()
        self.assertEqual(self.transport.registers[0x00], 0x1C5)
        self.assertEqual(self.transport.registers[0x6C], 0x05028050)
        self.assertEqual(self.transport.registers[0x10], 0x505)
        self.assertEqual(self.transport.registers[0x11], 0)
        self.assertEqual(self.transport.registers[0x70], 0xC10D0024)
        self.assertFalse(self.driver.enabled)
        self.assertEqual(self.transport.registers[0x01], 0)
        # No attempts to read write-only settings or to program irreversible OTP.
        self.assertTrue(set(self.transport.reads).isdisjoint({0x03, 0x10, 0x11, 0x13, 0x22}))
        self.assertNotIn(0x04, [r for r, _ in self.transport.writes])
        self.assertTrue(self.driver.ready()["ifcnt_matches"])

    def test_enable_velocity_signed_encoding_and_fast_writes(self):
        self.configure()
        self.driver.set_velocity(-12345)
        self.assertEqual(self.transport.registers[0x22], (1 << 24) - 12345)
        self.driver.enable()
        reads = len(self.transport.reads)
        self.driver.set_velocity(23456)
        self.driver.set_velocity(23456)
        self.assertEqual(len(self.transport.reads), reads)
        self.assertEqual(self.transport.registers[0x6C] & 15, 4)
        self.assertEqual(self.driver.check_health()["velocity_register_commanded"], 23456)
        for value in (fw.VACTUAL_MIN, fw.VACTUAL_MAX, 0):
            self.driver.set_velocity(value)
            self.assertEqual(self.transport.registers[0x22], value & 0xFFFFFF)
        for value in (fw.VACTUAL_MIN - 1, fw.VACTUAL_MAX + 1, 1.0, True):
            with self.assertRaises(ValueError):
                self.driver.set_velocity(value)

    def test_ifcnt_wrap_and_missing_fast_write_detected(self):
        self.transport.registers[0x02] = 252
        self.configure()
        for v in range(1, 260):
            self.driver.set_velocity(v)
        self.driver.check_health()
        self.transport.drop_write = True
        self.driver.set_velocity(1000)
        with self.assertRaisesRegex(OSError, "IFCNT"):
            self.driver.check_health()

    def test_each_config_write_confirmed(self):
        self.configure()
        self.transport.drop_write = True
        with self.assertRaisesRegex(OSError, "IFCNT"):
            self.driver.write_checked(0x10, 0x606)

    def test_disable_attempts_both_writes_before_broken_rx(self):
        self.configure()
        self.driver.enable()
        self.driver.set_velocity(1000)
        self.transport.timeout = True
        before = len(self.transport.packets)
        with self.assertRaisesRegex(OSError, "timeout"):
            self.driver.disable()
        packet_regs = [p[2] for p in self.transport.packets[before:]]
        self.assertEqual(packet_regs[:2], [0xEC, 0xA2])
        self.assertEqual(self.transport.registers[0x6C] & 15, 0)
        self.assertEqual(self.transport.registers[0x22], 0)

    def test_disable_attempts_zero_even_if_first_tx_fails(self):
        self.configure()
        self.transport.fail_write_regs.add(0x6C)
        before = len(self.transport.writes)
        with self.assertRaisesRegex(OSError, "TX failure"):
            self.driver.disable()
        self.assertEqual([r for r, _ in self.transport.writes[before:]], [0x6C, 0x22])

    def test_invalid_configuration_preserves_state_and_does_no_io(self):
        self.configure()
        previous = self.driver.config.copy()
        before = len(self.transport.packets)
        with self.assertRaises(ValueError):
            self.driver.configure({"irun": 32})
        self.assertEqual(self.driver.config, previous)
        self.assertEqual(len(self.transport.packets), before)
        self.driver.check_health()

    def test_driver_identification_rejected_with_outputs_disabled(self):
        self.transport.registers[0x06] = 0x21000100
        with self.assertRaisesRegex(OSError, "VERSION"):
            self.configure()
        self.assertEqual(self.transport.writes[0][0], 0x6C)
        self.assertFalse(self.driver.configured)

    def test_crc_header_length_and_timeout_errors(self):
        for attr, message in (("corrupt_crc", "CRC"), ("wrong_header", "reply"),
                              ("short_reply", "reply"), ("timeout", "timeout")):
            setattr(self.transport, attr, True)
            with self.assertRaisesRegex(OSError, message):
                self.driver.read(0x06)
            setattr(self.transport, attr, False)
        self.assertEqual(self.driver.stats["crc_errors"], 1)
        self.assertEqual(self.driver.stats["reply_errors"], 2)

    def test_fault_bits_and_reset_latch_are_not_motor_measurements(self):
        self.configure()
        self.transport.registers[0x6F] = 1 | (1 << 8) | (5 << 16)
        data = self.driver.diagnostics()
        self.assertIn("overtemperature_warning", data["faults"])
        self.assertTrue(data["flags"]["driver_t120"])
        self.assertEqual(data["current_scale_actual"], 5)
        self.assertNotIn("motor_temperature", data)
        self.assertNotIn("position_measured", data)
        with self.assertRaisesRegex(OSError, "temperature"):
            self.driver.check_health()
        self.transport.registers[0x6F] = (1 << 6) | (1 << 7)
        self.driver.check_health()  # Open-load flags are informational, not stall.
        self.transport.registers[0x01] = 1
        with self.assertRaisesRegex(OSError, "reset"):
            self.driver.check_health()

    def test_configuration_reset_and_pwm_tuning_diagnostics(self):
        self.configure()
        self.transport.registers[0x71] = 75 | (0x1FE << 16)
        self.transport.registers[0x72] = 23 | (45 << 16)
        data = self.driver.check_health()
        self.assertEqual(data["pwm_scale_auto"], -2)
        self.assertEqual(data["pwm_ofs_auto"], 23)
        self.assertEqual(data["pwm_grad_auto"], 45)
        self.transport.registers[0x00] ^= 1
        with self.assertRaisesRegex(OSError, "configuration"):
            self.driver.check_health()

    def test_compact_health_still_checks_all_safety_registers(self):
        self.configure()
        before = len(self.transport.reads)
        data = self.driver.check_health(compact=True)
        self.assertEqual(len(self.transport.reads) - before, 7)
        self.assertTrue(data["compact"])
        self.assertNotIn("pwm_scale_sum", data)
        self.assertEqual(set(data["registers"]),
                         {"IOIN", "GSTAT", "DRV_STATUS", "GCONF", "CHOPCONF", "PWMCONF", "IFCNT"})
        self.transport.registers[0x6F] = 4
        with self.assertRaisesRegex(OSError, "short_to_gnd_a"):
            self.driver.check_health(compact=True)


class ConfigAndPhysicsTests(unittest.TestCase):
    def test_every_profile_valid(self):
        for config in fw.DRIVER_PROFILES.values():
            self.assertEqual(fw.validate_motor_config(config), config)
        self.assertEqual(set(fw.CONFIG_SCHEMA), set(fw.DEFAULT_MOTOR_CONFIG))

    def test_register_ranges_types_and_cross_constraints(self):
        bad = ({"microsteps": 3}, {"irun": 32}, {"ihold": -1}, {"clock_hz": 19e6},
               {"full_steps_per_rev": 0}, {"full_steps_per_rev": 20.0}, {"irun": True},
               {"tpwmthrs": 1 << 20}, {"senddelay": 16}, {"intpol": 1},
               {"calibration_factor": float("nan")}, {"rsense_ohm": 0},
               {"toff": 1, "tbl": 1}, {"hend": 15, "hstrt": 7},
               {"pwm_autoscale": False}, {"chopper": "stealthchop", "tpowerdown": 1},
               {"internal_Rsense": True}, {"stallguard": 1}, {"vref_v": -1})
        for config in bad:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    fw.validate_motor_config(config)
        valid = fw.validate_motor_config({"hend": 11, "hstrt": 7, "toff": 1, "tbl": 2})
        self.assertEqual(valid["hend"], 11)  # Actual hysteresis 8+8=16.
        for key, schema in fw.CONFIG_SCHEMA.items():
            if schema["type"] in ("integer", "number"):
                for value in (float("inf"), float("nan")):
                    with self.assertRaises(ValueError):
                        fw.validate_motor_config({key: value})

    def test_microsteps_register_encoding_and_velocity_meaning(self):
        for index, microsteps in enumerate((256, 128, 64, 32, 16, 8, 4, 2, 1)):
            config = fw.validate_motor_config({"microsteps": microsteps})
            self.assertEqual((fw.driver_registers(config)[0x6C] >> 24) & 15, index)
            self.assertAlmostEqual(fw.vactual_to_rpm(1000, config),
                                   1000 * 12000000 / 16777216 * 60 / 20 / microsteps)

    def test_rpm_above_old_limit_and_roundtrip_register_extremes(self):
        config = fw.validate_motor_config({})
        for velocity in (fw.VACTUAL_MIN, -1, 0, 1, fw.VACTUAL_MAX):
            rpm = fw.vactual_to_rpm(velocity, config)
            self.assertEqual(fw.rpm_to_vactual(rpm, config), velocity)
        self.assertGreater(fw.rpm_to_vactual(6000, config), 0)
        self.assertEqual(fw.rpm_to_vactual(1e-12, config), 0)
        with self.assertRaises(ValueError):
            fw.rpm_to_vactual(fw.vactual_to_rpm(fw.VACTUAL_MAX, config) * 2, config)
        with self.assertRaises(ValueError):
            fw.rpm_to_vactual(float("nan"), config)

    def test_calibration_factor_direction_and_nearest_quantum(self):
        config = fw.validate_motor_config({})
        calibrated = fw.validate_motor_config({"calibration_factor": 1.1})
        self.assertAlmostEqual(fw.vactual_to_rpm(1000, calibrated),
                               1.1 * fw.vactual_to_rpm(1000, config))
        for rpm in (-10, 10, 100, 5000):
            rounded = fw.vactual_to_rpm(fw.rpm_to_vactual(rpm, calibrated), calibrated)
            quantum = fw.vactual_to_rpm(1, calibrated)
            self.assertLessEqual(abs(rounded - rpm), quantum * .501)

    def test_rp2040_float32_extreme_register_roundtrip(self):
        for microsteps in (1, 2, 4, 8, 16, 32, 64, 128, 256):
            config = fw.validate_motor_config({"microsteps": microsteps})
            config["clock_hz"] = Float32(config["clock_hz"])
            for value in (fw.VACTUAL_MIN, -8388607, -1, 1, 8388606, fw.VACTUAL_MAX):
                with self.subTest(microsteps=microsteps, value=value):
                    rpm = fw.vactual_to_rpm(value, config)
                    self.assertIsInstance(rpm, Float32)
                    self.assertEqual(fw.rpm_to_vactual(rpm, config), value)

    def test_current_formula_vref_saturation_and_digital_reference(self):
        config = fw.validate_motor_config({})
        current = fw.current_estimate(config)
        self.assertAlmostEqual(current["run_peak_a"], .07714285714285714)
        self.assertAlmostEqual(current["run_rms_a"], .05454823740547652)
        self.assertEqual(current["source"], "theoretical_from_config")
        full_ref = fw.current_estimate(fw.validate_motor_config({"vref_v": 2.5}))
        high_ref = fw.current_estimate(fw.validate_motor_config({"vref_v": 3.3}))
        digital = fw.current_estimate(fw.validate_motor_config({"i_scale_analog": False, "vref_v": 0}))
        self.assertEqual(full_ref["run_rms_a"], high_ref["run_rms_a"])
        self.assertEqual(full_ref["run_rms_a"], digital["run_rms_a"])


if __name__ == "__main__":
    unittest.main()
