"""E-302 standalone Raspberry Pi Pico W / RP2040 MicroPython 1.26.1 firmware.
Copy ONLY this file to the Pico as main.py. USB JSON protocol: see PROTOCOL.md.
No motor position/speed/temperature feedback. Host simulation is explicitly marked.
"""
import time

def ticks_us():
    return time.ticks_us() if hasattr(time, 'ticks_us') else int(time.monotonic() * 1000000)

def ticks_diff(a, b):
    return time.ticks_diff(a, b) if hasattr(time, 'ticks_diff') else a - b

def sleep_ms(value):
    if hasattr(time, 'sleep_ms'):
        time.sleep_ms(value)
    else:
        time.sleep(value / 1000.0)

# UART transports: this fragment is assembled into the standalone Pico main.py.
import time as _transport_time
try:
    import machine as _transport_machine
    import rp2 as _transport_rp2
except ImportError:
    _transport_machine = None
    _transport_rp2 = None


def _uart_ticks_us():
    if hasattr(_transport_time, "ticks_us"):
        return _transport_time.ticks_us()
    return int(_transport_time.monotonic() * 1000000)


def _uart_elapsed(now, before):
    if hasattr(_transport_time, "ticks_diff"):
        return _transport_time.ticks_diff(now, before)
    return now - before


def _uart_sleep_us(delay):
    if hasattr(_transport_time, "sleep_us"):
        _transport_time.sleep_us(delay)
    else:
        _transport_time.sleep(delay / 1000000.0)


def tmc_crc(data):
    """TMC2208 CRC8-ATM, input bits LSB first (datasheet 4.2)."""
    value = 0
    for byte in data:
        for _ in range(8):
            mix = (value >> 7) ^ (byte & 1)
            value = (value << 1) & 255
            if mix:
                value ^= 7
            byte >>= 1
    return value


def _pio_tx_words(packet, reply_length):
    """Preload the *complete* frame: control + at most three 32-bit words."""
    if len(packet) not in (4, 8) or reply_length not in (0, 8):
        raise ValueError("TMC UART needs a 4/8-byte request and 0/8-byte reply")
    bits = 0
    for index, byte in enumerate(packet):
        bits |= ((byte << 1) | (1 << 9)) << (index * 10)
    count = len(packet) * 10
    words = [(count - 1) | (128 if reply_length else 0)]
    for offset in range(0, count, 32):
        words.append((bits >> offset) & 0xFFFFFFFF)
    return words


if _transport_rp2 is not None:
    @_transport_rp2.asm_pio(
        set_init=_transport_rp2.PIO.IN_HIGH,
        out_init=_transport_rp2.PIO.IN_HIGH,
        out_shiftdir=_transport_rp2.PIO.SHIFT_RIGHT,
        in_shiftdir=_transport_rp2.PIO.SHIFT_RIGHT,
        autopull=True, pull_thresh=32, autopush=True, push_thresh=24,
    )
    def _tmc_half_duplex():
        # freq = 8 * baud. GPIO is input while idle and throughout receiving.
        wrap_target()
        pull(block)
        out(x, 7)
        out(y, 1)
        out(null, 24)
        set(pindirs, 1)
        label("tx_bit")
        out(pins, 1) [6]
        jmp(x_dec, "tx_bit")
        # Last OUT was the final stop bit; exactly eight cycles have elapsed.
        set(pindirs, 0)
        jmp(not_y, "done")
        set(y, 7)
        label("rx_byte")
        wait(0, pin, 0)
        set(x, 7) [10]
        label("rx_bit")
        in_(pins, 1)
        jmp(x_dec, "rx_bit") [6]
        # Centre of stop bit: low is a framing error, never accepted as data.
        jmp(pin, "valid_stop")
        set(x, 2)
        jmp("finish")
        label("valid_stop")
        jmp(y_dec, "rx_byte")
        # Auto-push packs 3 + 3 bytes; explicitly push the remaining 2 bytes.
        push(block)
        label("done")
        set(x, 1)
        label("finish")
        mov(isr, x)
        push(block)
        # Status 1 = done, 2 = bad stop. Data words always have low byte zero.
        wrap()


class _UARTTransportBase:
    def _setup(self, baud, timeout_ms):
        if isinstance(baud, bool) or not isinstance(baud, int) or baud < 9000:
            raise ValueError("UART baud must be an integer >= 9000")
        if not isinstance(timeout_ms, (int, float)) or timeout_ms <= 0:
            raise ValueError("UART timeout must be positive")
        self.baud = baud
        self.timeout_us = int(timeout_ms * 1000)
        # 12 idle bit times after success; >63 + 12 after an incomplete frame.
        self.guard_us = (12000000 + baud - 1) // baud
        self.recovery_us = (80000000 + baud - 1) // baud
        self.closed = False
        self.stats = {"exchanges": 0, "tx_bytes": 0, "rx_bytes": 0,
                      "timeouts": 0, "echo_errors": 0, "framing_errors": 0,
                      "errors": 0, "recoveries": 0, "stale_bytes": 0}

    def _validate(self, packet, reply_length):
        if self.closed:
            raise OSError("UART transport closed")
        if len(packet) not in (4, 8) or reply_length not in (0, 8):
            raise ValueError("TMC UART needs a 4/8-byte request and 0/8-byte reply")
        # SENDDELAY can be up to 15 (120 bit times), plus request and reply.
        if self.timeout_us < ((len(packet) + reply_length) * 10 + 120) * 1000000 / self.baud:
            raise ValueError("UART timeout shorter than worst-case TMC transaction")
        self.stats["exchanges"] += 1


class HardwareUARTTransport(_UARTTransportBase):
    """Two GPIOs, TX through 1k to PDN_UART; RX directly to that same node."""
    def __init__(self, uart, baud=115200, timeout_ms=20):
        self._setup(baud, timeout_ms)
        self.uart = uart

    def _drain(self):
        available = self.uart.any()
        if available:
            data = self.uart.read(available)
            if data:
                self.stats["stale_bytes"] += len(data)

    def exchange(self, packet, reply_length=0):
        self._validate(packet, reply_length)
        self._drain()
        received = bytearray()
        expected = len(packet) + reply_length
        started = _uart_ticks_us()
        try:
            if self.uart.write(packet) != len(packet):
                raise OSError("UART short write")
            self.stats["tx_bytes"] += len(packet)
            while len(received) < expected:
                available = self.uart.any()
                if available:
                    chunk = self.uart.read(min(available, expected - len(received)))
                    if chunk:
                        received.extend(chunk)
                if _uart_elapsed(_uart_ticks_us(), started) >= self.timeout_us:
                    self.stats["timeouts"] += 1
                    raise OSError("UART timeout: received %d/%d echo+reply bytes" %
                                  (len(received), expected))
                if len(received) < expected:
                    _uart_sleep_us(10)
            self.stats["rx_bytes"] += len(received)
            if received[:len(packet)] != packet:
                self.stats["echo_errors"] += 1
                raise OSError("UART TX echo mismatch; check RX/TX/PDN and wiring")
            # RX last-byte availability can precede end of stop; 12 bits also
            # cover the driver's four-bit output-release delay (datasheet 4.3).
            _uart_sleep_us(self.guard_us)
            if self.uart.any():
                self._drain()
                raise OSError("UART unexpected trailing bytes")
            return bytes(received[len(packet):])
        except OSError:
            self.stats["errors"] += 1
            self.stats["recoveries"] += 1
            _uart_sleep_us(self.recovery_us)
            self._drain()
            raise

    def close(self):
        self.uart.deinit()
        self.closed = True


class PIOUARTTransport(_UARTTransportBase):
    """Single physical GPIO, one PIO state machine, no Python turnaround race."""
    def __init__(self, pin, sm_id=0, baud=115200, timeout_ms=20):
        self._setup(baud, timeout_ms)
        if _transport_machine is None or _transport_rp2 is None:
            raise RuntimeError("PIO transport needs RP2040 MicroPython")
        if not isinstance(sm_id, int) or not 0 <= sm_id <= 7:
            raise ValueError("RP2040 PIO state machine must be 0..7")
        self.sm_id = sm_id
        self.pin = _transport_machine.Pin(pin, _transport_machine.Pin.IN,
                                          _transport_machine.Pin.PULL_UP)
        self.sm = _transport_rp2.StateMachine(sm_id)
        self._init_sm()

    def _init_sm(self):
        self.sm.init(_tmc_half_duplex, freq=self.baud * 8,
                     set_base=self.pin, out_base=self.pin, in_base=self.pin,
                     jmp_pin=self.pin)
        self.sm.active(0)

    def _idle_bus(self):
        start = _uart_ticks_us()
        high_since = start
        while _uart_elapsed(_uart_ticks_us(), high_since) < self.guard_us:
            if not self.pin.value():
                high_since = _uart_ticks_us()
            if _uart_elapsed(_uart_ticks_us(), start) >= self.timeout_us:
                self.stats["timeouts"] += 1
                raise OSError("PIO UART bus stuck low or not idle")

    def _recover(self):
        self.sm.active(0)
        # Force input even when timeout interrupted a request's start/data bit.
        self.pin.init(_transport_machine.Pin.IN, _transport_machine.Pin.PULL_UP)
        _uart_sleep_us(self.recovery_us)
        self._init_sm()
        self.stats["recoveries"] += 1

    def exchange(self, packet, reply_length=0):
        self._validate(packet, reply_length)
        try:
            self._idle_bus()
            # All TX words fit the four-word FIFO before starting. A Python GC
            # pause cannot insert invalid >63-bit gaps inside a request.
            for word in _pio_tx_words(packet, reply_length):
                self.sm.put(word)
            self.stats["tx_bytes"] += len(packet)
            self.sm.active(1)
            received = bytearray()
            started = _uart_ticks_us()
            done = False
            while not done:
                while self.sm.rx_fifo():
                    word = self.sm.get()
                    if word & 255:
                        if word == 2:
                            self.stats["framing_errors"] += 1
                            raise OSError("PIO UART framing error: stop bit is low")
                        if word != 1:
                            raise OSError("PIO UART unexpected status word")
                        done = True
                        break
                    count = min(3, reply_length - len(received))
                    if count <= 0:
                        raise OSError("PIO UART unexpected data")
                    data = word >> (32 - count * 8)
                    for _ in range(count):
                        received.append(data & 255)
                        data >>= 8
                if not done and _uart_elapsed(_uart_ticks_us(), started) >= self.timeout_us:
                    self.stats["timeouts"] += 1
                    raise OSError("PIO UART reply timeout (%d/%d bytes)" %
                                  (len(received), reply_length))
                if not done:
                    _uart_sleep_us(10)
            self.sm.active(0)
            if len(received) != reply_length:
                raise OSError("PIO UART incomplete reply")
            self.stats["rx_bytes"] += len(received)
            _uart_sleep_us(self.guard_us)
            return bytes(received)
        except OSError:
            self.stats["errors"] += 1
            self._recover()
            raise

    def close(self):
        self.sm.active(0)
        self.pin.init(_transport_machine.Pin.IN, _transport_machine.Pin.PULL_UP)
        self.closed = True


# TMC2208 register layer. Static section of main.py, no files imported on Pico.
import math

VACTUAL_MIN = -(1 << 23)
VACTUAL_MAX = (1 << 23) - 1

DEFAULT_MOTOR_CONFIG = {
    "full_steps_per_rev": 20, "microsteps": 8, "clock_hz": 12000000,
    "calibration_factor": 1.0, "chopper": "spreadcycle", "shaft": False,
    "irun": 5, "ihold": 5, "iholddelay": 0, "tpowerdown": 0,
    "i_scale_analog": True, "vsense": 1, "vref_v": 0.8, "rsense_ohm": 0.11,
    "toff": 4, "hstrt": 5, "hend": 0, "tbl": 1, "intpol": False,
    "multistep_filt": True, "tpwmthrs": 0, "senddelay": 0,
    "pwm_ofs": 36, "pwm_grad": 0, "pwm_freq": 1,
    "pwm_autoscale": True, "pwm_autograd": True,
    "pwm_reg": 1, "pwm_lim": 12, "freewheel": 0,
    "hold_on_stop": False,
}

# Metadata serves both the generic desktop editor and strict firmware validator.
CONFIG_SCHEMA = {
    "full_steps_per_rev": {"type": "integer", "min": 1, "description": "Assumed full motor steps per revolution; verify physically"},
    "microsteps": {"type": "integer", "choices": [1, 2, 4, 8, 16, 32, 64, 128, 256]},
    "clock_hz": {"type": "number", "min": 4000000, "max": 18000000, "description": "Assumed TMC clock (datasheet 4..18 MHz external), not RP2040 clock"},
    "calibration_factor": {"type": "number", "exclusive_min": 0, "description": "Measured/calculated travel ratio; does not detect slip"},
    "chopper": {"type": "string", "choices": ["spreadcycle", "stealthchop"]},
    "shaft": {"type": "boolean"},
    "irun": {"type": "integer", "min": 0, "max": 31},
    "ihold": {"type": "integer", "min": 0, "max": 31},
    "iholddelay": {"type": "integer", "min": 0, "max": 15},
    "tpowerdown": {"type": "integer", "min": 0, "max": 255},
    "i_scale_analog": {"type": "boolean"},
    "vsense": {"type": "integer", "choices": [0, 1]},
    "vref_v": {"type": "number", "min": 0, "max": 5, "description": "Manually measured voltage; never read/written by UART"},
    "rsense_ohm": {"type": "number", "exclusive_min": 0, "description": "Assumed external shunt resistance"},
    "toff": {"type": "integer", "min": 1, "max": 15},
    "hstrt": {"type": "integer", "min": 0, "max": 7},
    "hend": {"type": "integer", "min": 0, "max": 15},
    "tbl": {"type": "integer", "min": 0, "max": 3},
    "intpol": {"type": "boolean"},
    "multistep_filt": {"type": "boolean"},
    "tpwmthrs": {"type": "integer", "min": 0, "max": 1048575},
    "senddelay": {"type": "integer", "min": 0, "max": 15},
    "pwm_ofs": {"type": "integer", "min": 0, "max": 255},
    "pwm_grad": {"type": "integer", "min": 0, "max": 255},
    "pwm_freq": {"type": "integer", "min": 0, "max": 3},
    "pwm_autoscale": {"type": "boolean"},
    "pwm_autograd": {"type": "boolean"},
    "pwm_reg": {"type": "integer", "min": 1, "max": 15},
    "pwm_lim": {"type": "integer", "min": 0, "max": 15},
    "freewheel": {"type": "integer", "min": 0, "max": 3},
    "hold_on_stop": {"type": "boolean"},
}
for _config_key in CONFIG_SCHEMA:
    CONFIG_SCHEMA[_config_key]["default"] = DEFAULT_MOTOR_CONFIG[_config_key]
del _config_key


def validate_motor_config(config):
    """Validate a partial config without changing caller data or hardware."""
    if not isinstance(config, dict):
        raise ValueError("config must be an object")
    result = DEFAULT_MOTOR_CONFIG.copy()
    for key, value in config.items():
        if key not in CONFIG_SCHEMA:
            raise ValueError("Unknown motor setting: " + str(key))
        rule = CONFIG_SCHEMA[key]
        kind = rule["type"]
        if kind == "boolean":
            if not isinstance(value, bool):
                raise ValueError(key + " must be boolean")
        elif kind == "string":
            if not isinstance(value, str):
                raise ValueError(key + " must be string")
        else:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(key + " must be numeric")
            try:
                finite = math.isfinite(value)
            except (OverflowError, TypeError):
                finite = False
            if not finite:
                raise ValueError(key + " must be finite")
            if kind == "integer" and (not isinstance(value, int)):
                raise ValueError(key + " must be integer")
            if "min" in rule and value < rule["min"]:
                raise ValueError(key + " below register/parameter minimum")
            if "max" in rule and value > rule["max"]:
                raise ValueError(key + " above register/parameter maximum")
            if "exclusive_min" in rule and value <= rule["exclusive_min"]:
                raise ValueError(key + " must be positive")
        if "choices" in rule and value not in rule["choices"]:
            raise ValueError(key + " unsupported value")
        result[key] = value
    # Encoded HEND means -3..12; encoded HSTRT means +1..8.
    if result["hend"] - 3 + result["hstrt"] + 1 > 16:
        raise ValueError("Effective HEND+HSTRT must be <=16 (datasheet 5.4.1)")
    if result["toff"] == 1 and result["tbl"] < 2:
        raise ValueError("TOFF=1 requires TBL>=2 (datasheet 5.4.1)")
    if result["pwm_autograd"] and not result["pwm_autoscale"]:
        raise ValueError("PWM autograd requires autoscale")
    if (result["chopper"] == "stealthchop" and result["pwm_autoscale"]
            and result["tpowerdown"] < 2):
        raise ValueError("StealthChop autotuning requires TPOWERDOWN>=2")
    return result


DRIVER_PROFILES = {
    "e301_conservative": DEFAULT_MOTOR_CONFIG.copy(),
    "stealthchop_low_current": validate_motor_config({
        "chopper": "stealthchop", "tpowerdown": 20,
        "intpol": True, "iholddelay": 4,
    }),
    "spreadcycle_16_microsteps": validate_motor_config({"microsteps": 16}),
}


def rpm_to_vactual(rpm, config):
    if isinstance(rpm, bool) or not isinstance(rpm, (int, float)) or not math.isfinite(rpm):
        raise ValueError("RPM must be finite")
    # Share the identical quantum with the inverse. Repeated multiply/divide
    # through large intermediate values loses low bits on RP2040 float32.
    raw = rpm / _velocity_quantum(config)
    if not math.isfinite(raw):
        raise ValueError("RPM outside signed 24-bit VACTUAL range")
    # Do not add 0.5 before int(): RP2040 float32 would round the exact
    # VACTUAL_MAX + 0.5 up to 8388608 and reject a representable register value.
    value = int(raw)
    fraction = raw - value
    if fraction >= 0.5:
        value += 1
    elif fraction <= -0.5:
        value -= 1
    if not VACTUAL_MIN <= value <= VACTUAL_MAX:
        raise ValueError("RPM outside signed 24-bit VACTUAL range")
    return value


def vactual_to_rpm(value, config):
    if isinstance(value, bool) or not isinstance(value, int) or not VACTUAL_MIN <= value <= VACTUAL_MAX:
        raise ValueError("VACTUAL must be signed 24-bit integer")
    return value * _velocity_quantum(config)


def _velocity_quantum(config):
    return (config["clock_hz"] / (1 << 24) * 60.0
            / config["full_steps_per_rev"] / config["microsteps"]
            * config["calibration_factor"])


def current_estimate(config):
    """Datasheet 9/9.1 ideal sinusoidal phase current, NEVER a measurement."""
    analog_scale = min(config["vref_v"] / 2.5, 1.0) if config["i_scale_analog"] else 1.0
    full_scale_v = 0.180 if config["vsense"] else 0.325
    phase_peak_scale = full_scale_v * analog_scale / (config["rsense_ohm"] + 0.030)
    run_peak = phase_peak_scale * (config["irun"] + 1) / 32.0
    hold_peak = phase_peak_scale * (config["ihold"] + 1) / 32.0
    return {
        "source": "theoretical_from_config", "run_peak_a": run_peak,
        "run_rms_a": run_peak / math.sqrt(2), "hold_peak_a": hold_peak,
        "hold_rms_a": hold_peak / math.sqrt(2), "analog_scale": analog_scale,
        "vref_v_manual": config["vref_v"], "rsense_ohm_assumed": config["rsense_ohm"],
        "regulated": config["chopper"] == "spreadcycle" or config["pwm_autoscale"],
        "standstill_freewheel": config["chopper"] == "stealthchop" and config["ihold"] == 0 and config["freewheel"] != 0,
    }


def motor_config_warnings(config):
    result = []
    if config["irun"] < 16:
        result.append("IRUN<16 reduces effective current/microstep precision; conservative default retained")
    if config["i_scale_analog"] and config["vref_v"] < 1:
        result.append("Low manually recorded Vref increases relative analog noise")
    if config["chopper"] == "stealthchop":
        result.append("StealthChop low-current regulation/autotuning must be verified physically")
    if not config["pwm_autoscale"]:
        result.append("PWM autoscale disabled: IRUN/IHOLD do not regulate actual StealthChop current")
    if config["ihold"] > config["irun"]:
        result.append("Configured hold current exceeds run current")
    return result


def driver_registers(config):
    # External sense only, no test mode, no disabling short-circuit protection.
    gconf = (int(config["i_scale_analog"]) | (int(config["chopper"] == "spreadcycle") << 2)
             | (int(config["shaft"]) << 3) | (1 << 6) | (1 << 7)
             | (int(config["multistep_filt"]) << 8))
    mres = 0
    resolution = 256
    while resolution > config["microsteps"]:
        mres += 1
        resolution //= 2
    chopconf = (config["toff"] | (config["hstrt"] << 4) | (config["hend"] << 7)
                | (config["tbl"] << 15) | (config["vsense"] << 17)
                | (mres << 24) | (int(config["intpol"]) << 28))
    pwmconf = (config["pwm_ofs"] | (config["pwm_grad"] << 8) | (config["pwm_freq"] << 16)
               | (int(config["pwm_autoscale"]) << 18) | (int(config["pwm_autograd"]) << 19)
               | (config["freewheel"] << 20) | (config["pwm_reg"] << 24) | (config["pwm_lim"] << 28))
    return {
        0x00: gconf, 0x03: config["senddelay"] << 8,
        0x10: config["ihold"] | (config["irun"] << 8) | (config["iholddelay"] << 16),
        0x11: config["tpowerdown"], 0x13: config["tpwmthrs"],
        0x6C: chopconf, 0x70: pwmconf,
    }


class Driver:
    """TMC2208 address 0; IFCNT verifies even write-only registers.

    tmc_crc comes from the preceding transport section of this same main.py.
    Fast VACTUAL writes track an expected IFCNT, checked by periodic diagnostics.
    """
    def __init__(self, transport, config=None):
        self.transport = transport
        self.config = validate_motor_config(config or {})
        self.registers = driver_registers(self.config)
        self.counter = None
        self.enabled = False
        self.configured = False
        self.velocity = 0
        self.last_diagnostics = {}
        self.stats = {"reads": 0, "writes": 0, "checked_writes": 0,
                      "crc_errors": 0, "reply_errors": 0, "ifcnt_errors": 0}

    def read(self, reg):
        request = bytearray((5, 0, reg))
        request.append(tmc_crc(request))
        response = self.transport.exchange(request, reply_length=8)
        self.stats["reads"] += 1
        if len(response) != 8 or response[:3] != bytes((5, 255, reg)):
            self.stats["reply_errors"] += 1
            raise OSError("UART invalid reply length/address/register")
        if tmc_crc(response[:7]) != response[7]:
            self.stats["crc_errors"] += 1
            raise OSError("UART reply CRC error")
        return int.from_bytes(response[3:7], "big")

    def _write(self, reg, value):
        packet = bytearray((5, 0, reg | 0x80))
        packet.extend(value.to_bytes(4, "big"))
        packet.append(tmc_crc(packet))
        self.transport.exchange(packet, reply_length=0)
        self.stats["writes"] += 1
        if self.counter is not None:
            self.counter = (self.counter + 1) & 255

    def _check_counter(self, actual=None):
        if actual is None:
            actual = self.read(0x02) & 255
        if self.counter is not None and actual != self.counter:
            self.stats["ifcnt_errors"] += 1
            raise OSError("UART IFCNT mismatch: expected %d, received %d; lost write or reset" % (self.counter, actual))
        self.counter = actual

    def write_checked(self, reg, value, readback=False):
        self._check_counter()
        self._write(reg, value)
        self._check_counter()
        if readback and self.read(reg) != value:
            raise OSError("Driver register readback mismatch: 0x%02x" % reg)
        self.stats["checked_writes"] += 1

    def disable(self):
        # Both commands attempted BEFORE any read/ack: broken RX cannot prevent
        # transmitting an output-disable. EN GPIO is controlled by the caller.
        off = self.registers[0x6C] & ~15
        error = None
        self.enabled = False
        self.velocity = 0
        self.counter = None
        for reg, value in ((0x6C, off), (0x22, 0)):
            try:
                self._write(reg, value)
            except OSError as exc:
                error = exc
        if error is not None:
            raise error
        if self.read(0x6C) != off:
            raise OSError("Driver output disable readback failed")
        # Reconfirm the write-only VACTUAL zero with an individual IFCNT ack.
        self.write_checked(0x22, 0)

    def configure(self, config=None):
        candidate = self.config if config is None else validate_motor_config(config)
        # Validation happens before modifying either software or hardware.
        self.disable()
        self.configured = False
        ioin = self.read(0x06)
        if ioin >> 24 != 0x20 or not (ioin & 0x100):
            raise OSError("Expected TMC2208-compatible IOIN VERSION=0x20, SEL_A=1")
        self.config = candidate.copy()
        self.registers = driver_registers(self.config)
        for reg in (0x00, 0x03, 0x6C, 0x10, 0x11, 0x13, 0x70):
            value = self.registers[reg] & ~15 if reg == 0x6C else self.registers[reg]
            self.write_checked(reg, value, reg in (0x00, 0x6C, 0x70))
        self.write_checked(0x22, 0)
        self.write_checked(0x01, 7)  # Clear startup GSTAT latches, then inspect.
        self.configured = True
        try:
            return self.check_health()
        except OSError:
            self.configured = False
            raise

    def ready(self):
        if not self.configured:
            raise OSError("Driver must be configured before motion")
        return self.check_health(compact=True)

    def set_velocity(self, vactual):
        if isinstance(vactual, bool) or not isinstance(vactual, int) or not VACTUAL_MIN <= vactual <= VACTUAL_MAX:
            raise ValueError("VACTUAL must be a signed 24-bit integer")
        if not self.configured:
            raise OSError("Driver not configured")
        if vactual != self.velocity:
            self._write(0x22, vactual & 0xFFFFFF)
            self.velocity = vactual

    def enable(self):
        if not self.configured:
            raise OSError("Driver not configured")
        self.write_checked(0x6C, self.registers[0x6C], True)
        self.enabled = True

    def diagnostics(self, compact=False):
        # VACTUAL/IHOLD_IRUN/TPOWERDOWN/TPWMTHRS are write-only, not read back.
        raw = {}
        selected = [("IOIN", 0x06), ("GSTAT", 0x01), ("DRV_STATUS", 0x6F),
                    ("GCONF", 0x00), ("CHOPCONF", 0x6C), ("PWMCONF", 0x70),
                    ("IFCNT", 0x02)]
        if not compact:
            selected += [("TSTEP", 0x12), ("MSCNT", 0x6A),
                         ("PWM_SCALE", 0x71), ("PWM_AUTO", 0x72)]
        for name, reg in selected:
            raw[name] = self.read(reg)
        gs, ds = raw["GSTAT"], raw["DRV_STATUS"]
        fault_flags = []
        for bit, name in ((0, "reset"), (1, "driver_error"), (2, "charge_pump_undervoltage")):
            if gs & (1 << bit):
                fault_flags.append(name)
        driver_flags = {}
        for bit, name in ((0, "overtemperature_warning"), (1, "overtemperature_shutdown"),
                          (2, "short_to_gnd_a"), (3, "short_to_gnd_b"),
                          (4, "short_low_side_a"), (5, "short_low_side_b"),
                          (6, "open_load_a"), (7, "open_load_b"),
                          (8, "driver_t120"), (9, "driver_t143"),
                          (10, "driver_t150"), (11, "driver_t157"),
                          (30, "stealthchop_active"), (31, "standstill")):
            driver_flags[name] = bool(ds & (1 << bit))
            if driver_flags[name] and (bit < 6 or 8 <= bit <= 11):
                fault_flags.append(name)
        expected_chop = self.registers[0x6C] if self.enabled else self.registers[0x6C] & ~15
        matches = (raw["GCONF"] == self.registers[0x00] and raw["CHOPCONF"] == expected_chop
                   and raw["PWMCONF"] == self.registers[0x70])
        counter_ok = self.counter is None or (raw["IFCNT"] & 255) == self.counter
        data = {
            "source": "driver_registers", "compact": compact,
            "version": raw["IOIN"] >> 24,
            "tmc220x": bool(raw["IOIN"] & 0x100), "configured": self.configured,
            "enabled_commanded": self.enabled, "enn_pin_high": bool(raw["IOIN"] & 1),
            "registers": raw, "flags": driver_flags, "faults": fault_flags,
            "configuration_matches": matches, "ifcnt_expected": self.counter,
            "ifcnt_matches": counter_ok, "current_scale_actual": (ds >> 16) & 31,
            "current_theoretical": current_estimate(self.config),
            "warnings": motor_config_warnings(self.config), "uart": self.transport.stats.copy(),
            "register_io": self.stats.copy(),
            "velocity_register_commanded": self.velocity,
            "rpm_calculated": vactual_to_rpm(self.velocity, self.config),
        }
        if not compact:
            pwm_auto = (raw["PWM_SCALE"] >> 16) & 0x1FF
            if pwm_auto & 0x100:
                pwm_auto -= 512
            data.update({"pwm_scale_sum": raw["PWM_SCALE"] & 255,
                         "pwm_scale_auto": pwm_auto,
                         "pwm_ofs_auto": raw["PWM_AUTO"] & 255,
                         "pwm_grad_auto": (raw["PWM_AUTO"] >> 16) & 255})
        self.last_diagnostics = data
        return data

    def check_health(self, compact=False):
        data = self.diagnostics(compact=compact)
        if data["version"] != 0x20 or not data["tmc220x"]:
            raise OSError("Driver identification changed")
        if data["faults"]:
            raise OSError("Driver fault: " + ", ".join(data["faults"]))
        if not data["configuration_matches"]:
            raise OSError("Driver configuration changed/reset")
        if not data["ifcnt_matches"]:
            self.stats["ifcnt_errors"] += 1
            raise OSError("UART IFCNT mismatch; lost write or driver reset")
        return data


# Motion planning: all distances below are calculated, never sensor readings.
import math


def _motion_number(value, name, positive=False, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a finite number")
    if not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    if positive and value <= 0:
        raise ValueError(name + " must be positive")
    if nonnegative and value < 0:
        raise ValueError(name + " must be nonnegative")
    return value


class MotionPlanner:
    """Sampled trapezoids with integration of the last *written* VACTUAL.

    update() only proposes a velocity. Call applied() after a successful UART
    write, using its completion time and vactual_to_rpm(written_value, config).
    This intentionally does not integrate a fictitious smooth acceleration.
    Position is cumulative; distance and elapsed time describe the latest run.
    """

    def __init__(self, config, update_period_s=0.020, uart_latency_s=0.002):
        self.config = config
        self.update_period_s = _motion_number(
            update_period_s, "update_period_s", positive=True)
        self.uart_latency_s = _motion_number(
            uart_latency_s, "uart_latency_s", nonnegative=True)
        self.quantum_rpm = abs(vactual_to_rpm(1, config))
        self.active = False
        self.position_rev_calculated = 0.0
        self.distance_rev_calculated = 0.0
        self.rpm_calculated = 0.0
        self.rpm_requested = 0.0
        self.accel = 100.0
        self.decel = 100.0
        self.mode = None
        self.completed = False
        self.completion_reason = None
        self.cycle = 0
        self._last_integrated = None
        self._last_update = None
        self._started = 0.0
        self._finished = None
        self._command_rpm = 0.0
        self._stop_requested = False
        self._finishing = None
        self._dwell_until = None
        self._target_position = None
        self._origin = 0.0
        self._leg = 0
        self._sign = 1
        self._revolutions = None
        self._duration = None
        self._cycles = None
        self._dwell = 0.0
        self.max_update_gap_s = 0.0
        self.late_updates = 0

    def _validate_rpm(self, rpm, allow_zero=False):
        _motion_number(rpm, "rpm")
        value = rpm_to_vactual(rpm, self.config)
        if rpm == 0:
            if allow_zero:
                return rpm
            raise ValueError("rpm must be nonzero")
        if value == 0:
            raise ValueError("rpm rounds to zero VACTUAL; minimum nonzero RPM is "
                             + str(self.quantum_rpm))
        return rpm

    def _integrate(self, now):
        _motion_number(now, "now")
        if self._last_integrated is not None:
            if now < self._last_integrated:
                raise ValueError("motion clock must be monotonic")
            delta = self.rpm_calculated * ((now - self._last_integrated) / 60.0)
            self.position_rev_calculated += delta
            self.distance_rev_calculated += abs(delta)
        self._last_integrated = now

    def start(self, mode, rpm, accel, decel, revolutions=None,
              duration_s=None, cycles=None, dwell_s=0, now=0):
        # Validate everything before touching a previous run or its reference.
        if self.active or self.rpm_calculated != 0:
            raise ValueError("motor is already moving")
        if mode not in ("continuous", "revolutions", "duration", "cycles"):
            raise ValueError("unknown motion mode")
        self._validate_rpm(rpm)
        _motion_number(accel, "accel", positive=True)
        _motion_number(decel, "decel", positive=True)
        _motion_number(dwell_s, "dwell_s", nonnegative=True)
        _motion_number(now, "now")
        if self._last_integrated is not None and now < self._last_integrated:
            raise ValueError("motion clock must be monotonic")
        if mode in ("revolutions", "cycles"):
            _motion_number(revolutions, "revolutions", positive=True)
            endpoint = self.position_rev_calculated + (revolutions if rpm > 0 else -revolutions)
            if not math.isfinite(endpoint):
                raise ValueError("endpoint exceeds floating point representation")
        if mode == "duration":
            _motion_number(duration_s, "duration_s", positive=True)
            if not math.isfinite(now + duration_s):
                raise ValueError("duration exceeds floating point representation")
        if mode == "cycles":
            _motion_number(cycles, "cycles", positive=True)
            if int(cycles) != cycles:
                raise ValueError("cycles must be an integer")
        self._integrate(now)
        self.active = True
        self.mode = mode
        self.rpm_requested = rpm
        self.accel, self.decel = accel, decel
        self.completed = False
        self.completion_reason = None
        self.distance_rev_calculated = 0.0
        self._command_rpm = 0.0
        self._started = now
        self._last_update = now
        self._finished = None
        self._stop_requested = False
        self._finishing = None
        self._dwell_until = None
        self._origin = self.position_rev_calculated
        self._sign = 1 if rpm > 0 else -1
        self._revolutions = revolutions
        self._duration = duration_s
        self._cycles = int(cycles) if mode == "cycles" else None
        self._dwell = dwell_s
        self._leg = 0
        self.cycle = 0
        self._target_position = endpoint if mode in ("revolutions", "cycles") else None
        self.max_update_gap_s = 0.0
        self.late_updates = 0

    def applied(self, rpm, now):
        _motion_number(rpm, "applied rpm")
        self._integrate(now)
        self.rpm_calculated = rpm

    def set_speed(self, rpm, accel=None, decel=None, now=0):
        if not self.active or self.mode != "continuous" or self._stop_requested:
            raise ValueError("speed changes require an active continuous run")
        self._validate_rpm(rpm, allow_zero=True)
        if accel is not None:
            _motion_number(accel, "accel", positive=True)
        if decel is not None:
            _motion_number(decel, "decel", positive=True)
        self._integrate(now)
        self.rpm_requested = rpm
        if accel is not None:
            self.accel = accel
        if decel is not None:
            self.decel = decel
        self._last_update = now
        if rpm == 0:
            self._stop_requested = True

    def stop(self, now=0):
        self._integrate(now)
        if self.active and not self._stop_requested:
            self._stop_requested = True
            self._finishing = None
            self._dwell_until = None
            self._last_update = now

    def emergency_stop(self, now):
        # Caller must separately disable EN and attempt VACTUAL=0. This method
        # records that output change; it cannot confirm a broken UART stop.
        self._integrate(now)
        self.rpm_calculated = 0.0
        self._command_rpm = 0.0
        self.active = False
        self.completed = False
        self.completion_reason = "emergency_stop"
        self._finished = now

    def stopping_distance_rev(self, rpm=None, decel=None, reaction_s=None):
        """Conservative calculated reserve, not a guarantee of actual position."""
        speed = abs(self.rpm_calculated if rpm is None else rpm)
        rate = self.decel if decel is None else decel
        _motion_number(rate, "decel", positive=True)
        delay = (self.update_period_s + self.uart_latency_s
                 if reaction_s is None else reaction_s)
        _motion_number(delay, "reaction_s", nonnegative=True)
        if speed == 0:
            return 0.0
        # A half quantum bounds nearest-integer conversion during braking.
        upper = speed + self.quantum_rpm * 0.5
        return (upper / rate) * (upper / 120.0) + upper * (delay / 60.0)

    def endpoint_resolution_rev(self):
        return self.quantum_rpm * (self.update_period_s + self.uart_latency_s) / 60.0

    def _distance_cap(self, remaining, maximum):
        # Solve v²/(120*d) + v*h/60 = remaining, including quantization.
        h = self.update_period_s + self.uart_latency_s
        if self.stopping_distance_rev(maximum) <= remaining:
            return maximum
        dh = self.decel * h
        square = dh * dh + (120.0 * remaining) * self.decel
        if math.isfinite(square) and square > 0:
            cap = ((120.0 * remaining) * self.decel) / (math.sqrt(square) + dh)
            cap -= self.quantum_rpm * 0.5
        else:
            # Rare numeric extremes: bounded search avoids overflow in sqrt.
            low, high = 0.0, maximum
            for unused in range(40):
                middle = (low + high) * 0.5
                if self.stopping_distance_rev(middle) <= remaining:
                    low = middle
                else:
                    high = middle
            cap = low
        # Below one quantum there is no slower nonzero VACTUAL. A final
        # one-quantum sample is allowed, then finish within that resolution.
        return min(maximum, max(self.quantum_rpm, cap))

    def _ramp(self, target, dt):
        current = self._command_rpm
        # Reach a written zero before allowing opposite-direction acceleration.
        reversing = (current * target < 0 or self.rpm_calculated * target < 0)
        if reversing:
            target = 0.0
        rate = self.decel if abs(target) < abs(current) or reversing else self.accel
        delta = rate * dt
        if current < target:
            current = min(target, current + delta)
        elif current > target:
            current = max(target, current - delta)
        self._command_rpm = current
        return current

    def _finish(self, now, reason):
        self.active = False
        self.completed = reason == "completed"
        self.completion_reason = reason
        self._finished = now
        self._command_rpm = 0.0
        self._finishing = None
        return 0.0

    def _finish_leg(self, now):
        if self.mode != "cycles":
            return self._finish(now, "completed")
        self._leg += 1
        self.cycle = self._leg // 2
        if self.cycle >= self._cycles:
            return self._finish(now, "completed")
        # Absolute alternating endpoints prevent a residual error accumulating
        # by redefining every leg from the last slightly-short endpoint.
        self._target_position = (self._origin if self._leg % 2 else
                                 self._origin + self._sign * self._revolutions)
        self._finishing = None
        self._command_rpm = 0.0
        self._dwell_until = now + self._dwell
        return 0.0

    def update(self, now, bounds=None):
        if bounds is not None:
            if len(bounds) != 2:
                raise ValueError("bounds must contain minimum and maximum revolutions")
            _motion_number(bounds[0], "minimum revolutions")
            _motion_number(bounds[1], "maximum revolutions")
            if bounds[0] >= bounds[1]:
                raise ValueError("minimum revolutions must be below maximum")
        self._integrate(now)
        if not self.active:
            return 0.0
        dt = now - self._last_update
        self._last_update = now
        self.max_update_gap_s = max(self.max_update_gap_s, dt)
        if dt > self.update_period_s + self.uart_latency_s:
            self.late_updates += 1
        if self._finishing:
            if self.rpm_calculated == 0:
                if self._finishing == "completed":
                    return self._finish_leg(now)
                return self._finish(now, self._finishing)
            return 0.0
        if self._stop_requested:
            result = self._ramp(0.0, dt)
            if result == 0:
                self._finishing = "stopped"
                if self.rpm_calculated == 0:
                    return self._finish(now, "stopped")
            return result
        if self._dwell_until is not None:
            if now < self._dwell_until:
                return 0.0
            # Do not count stationary dwell time as acceleration time.
            dt = max(0.0, now - max(self._dwell_until, now - dt))
            self._dwell_until = None
        target = self.rpm_requested
        if self.mode in ("revolutions", "cycles"):
            direction = self._sign if self._leg % 2 == 0 else -self._sign
            remaining = direction * (self._target_position - self.position_rev_calculated)
            if remaining <= self.endpoint_resolution_rev():
                self._command_rpm = 0.0
                self._finishing = "completed"
                if self.rpm_calculated == 0:
                    return self._finish_leg(now)
                return 0.0
            target = direction * self._distance_cap(remaining, abs(self.rpm_requested))
        elif self.mode == "duration":
            remaining_s = self._duration - (now - self._started)
            if remaining_s <= 0:
                self._command_rpm = 0.0
                self._finishing = "completed"
                if self.rpm_calculated == 0:
                    return self._finish_leg(now)
                return 0.0
            cap = self.decel * max(0.0, remaining_s - self.update_period_s - self.uart_latency_s)
            target = self._sign * min(abs(target), cap)
        if bounds is not None:
            # Check the direction still being executed before an opposite
            # requested direction. Reversal first has to brake to zero.
            moving = self._command_rpm or self.rpm_calculated or target
            if moving:
                direction = 1 if moving > 0 else -1
                remaining = ((bounds[1] - self.position_rev_calculated) if direction > 0
                             else (self.position_rev_calculated - bounds[0]))
                if remaining <= self.endpoint_resolution_rev():
                    self._command_rpm = 0.0
                    self._finishing = "boundary"
                    if self.rpm_calculated == 0:
                        return self._finish(now, "boundary")
                    return 0.0
                if target * direction > 0:
                    target = direction * self._distance_cap(remaining, abs(target))
        return self._ramp(target, dt)

    def status(self, now):
        self._integrate(now)
        end = now if self.active else self._finished
        elapsed = max(0.0, (self._started if end is None else end) - self._started)
        residual = (None if self._target_position is None else
                    self._target_position - self.position_rev_calculated)
        phase = "idle"
        if self.active:
            phase = ("stopping" if self._stop_requested or self._finishing else
                     "dwell" if self._dwell_until is not None else "moving")
        return {
            "mode": self.mode,
            "phase": phase,
            "rpm_requested": self.rpm_requested,
            "rpm_calculated": self.rpm_calculated,
            "position_rev_calculated": self.position_rev_calculated,
            "distance_rev_calculated": self.distance_rev_calculated,
            "elapsed_s": elapsed,
            "completed": self.completed,
            "completion_reason": self.completion_reason,
            "cycle": self.cycle,
            "cycles_requested": self._cycles,
            "target_position_rev_calculated": self._target_position,
            "residual_rev": residual,
            "endpoint_resolution_rev": self.endpoint_resolution_rev(),
            "stopping_distance_rev_calculated": self.stopping_distance_rev(),
            "max_update_gap_s": self.max_update_gap_s,
            "late_updates": self.late_updates,
            "accel_rpm_s": self.accel,
            "decel_rpm_s": self.decel,
        }


# --- Motor supervision, JSON protocol and RP2040 startup ---
try:
    import ujson as json
except ImportError:
    import json

FIRMWARE_VERSION = 'E302-1.0'
UPDATE_PERIOD_S = 0.020
PLANNER_UART_BUDGET_S = 0.040  # reserve for a checked start/periodic health batch
HEALTH_PERIOD_S = 0.5
HEARTBEAT_TIMEOUT_S = 2.0
MAX_LINE_BYTES = 8192
# Only these channel entries need editing to add independent drivers. The 2208
# has fixed slave address 0: each entry MUST have its own PDN_UART wire.
MOTOR_CHANNELS = [
    {'id': 'm1', 'transport': 'pio', 'pin': 4, 'sm_id': 0, 'enable_pin': 6},
    # {'id': 'm2', 'transport': 'pio', 'pin': 8, 'sm_id': 1, 'enable_pin': 9},
    # {'id': 'm3', 'transport': 'pio', 'pin': 12, 'sm_id': 2, 'enable_pin': 13},
    # Two-pin diagnostic fallback (replace m1, do not enable both):
    # {'id': 'm1', 'transport': 'hardware', 'uart_id': 1,
    #  'tx': 4, 'rx': 5, 'enable_pin': 6},
]


def finite_number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + ' must be a number')
    if value != value or value in (float('inf'), -float('inf')):
        raise ValueError(name + ' must be finite')
    if positive and value <= 0:
        raise ValueError(name + ' must be positive')
    return value


class MonotonicClock:
    """Accumulate ticks_diff frequently; never compare wrapping tick absolutes."""
    def __init__(self):
        self.previous = ticks_us()
        self.total_us = 0

    def __call__(self):
        now = ticks_us()
        self.total_us += ticks_diff(now, self.previous)
        self.previous = now
        return self.total_us / 1000000.0


class MotorController:
    def __init__(self, name, driver, clock, enable_pin=None):
        self.name = name
        self.driver = driver
        self.clock = clock
        self.enable_pin = enable_pin
        self.planner = MotionPlanner(driver.config, uart_latency_s=PLANNER_UART_BUDGET_S)
        self.fault = None
        self.last_diagnostics = {}
        self.mechanics = {'mode': 'free', 'reference_valid': False}
        self.reference_base = 0.0
        self.pending = None
        self.warm_until = 0.0
        self.last_update = clock()
        self.last_health = self.last_update
        self.last_tick = self.last_update
        self.last_velocity = 0
        self._enable(False)

    def _enable(self, enabled):
        if self.enable_pin is not None:
            self.enable_pin.value(0 if enabled else 1)

    def busy(self):
        return self.pending is not None or self.planner.active

    def energized(self):
        return self.busy() or bool(self.driver.enabled)

    def _require_idle(self):
        if self.busy():
            raise ValueError('Stop motion before changing configuration')

    def _pin_position(self, now):
        if not self.mechanics.get('reference_valid', False):
            return None
        motion = self.planner.status(now)
        return self.reference_base + motion['position_rev_calculated'] * self.mechanics['lead_mm_per_rev']

    def status(self, now=None):
        now = self.clock() if now is None else now
        state = 'fault' if self.fault else ('warming' if self.pending else
                ('running' if self.planner.active else
                 ('holding' if self.driver.enabled else 'idle')))
        mechanics = dict(self.mechanics)
        mechanics['position_mm_calculated'] = self._pin_position(now)
        return {'motor': self.name, 'state': state, 'config': dict(self.driver.config),
                'motion': self.planner.status(now), 'mechanics': mechanics,
                'diagnostics': self.last_diagnostics, 'fault': self.fault,
                'uart': dict(self.driver.transport.stats)}

    def emergency_stop(self, reason=None):
        # EN first: UART loss cannot prevent this local output inhibit, provided
        # the optional wire is fitted. Not a physical safety certification.
        self._enable(False)
        self.pending = None
        if self.driver.last_diagnostics:
            self.last_diagnostics = dict(self.driver.last_diagnostics)
        now = self.clock()
        self.planner.emergency_stop(now)
        self.last_velocity = 0
        self.mechanics['reference_valid'] = False
        try:
            self.driver.disable()
        except Exception as exc:
            reason = (reason + '; ' if reason else '') + 'UART stop unconfirmed: ' + str(exc)
        if reason:
            self.fault = reason

    def configure(self, changes):
        self._require_idle()
        if not isinstance(changes, dict):
            raise ValueError('config must be an object')
        candidate = dict(self.driver.config)
        candidate.update(changes)
        candidate = validate_motor_config(candidate)
        # All validation precedes output changes. A typo never destroys setup.
        old = self.driver.config
        position = self._pin_position(self.clock())
        self._enable(False)
        self.driver.configure(candidate)
        if any(candidate[k] != old[k] for k in
               ('full_steps_per_rev', 'microsteps', 'clock_hz', 'calibration_factor', 'shaft')):
            self.mechanics['reference_valid'] = False
        self.driver.config = candidate
        self.planner = MotionPlanner(candidate, uart_latency_s=PLANNER_UART_BUDGET_S)
        if position is not None:
            self.reference_base = position
        self.last_velocity = 0
        return self.status()

    def set_mechanics(self, settings):
        self._require_idle()
        if not isinstance(settings, dict):
            raise ValueError('settings must be an object')
        allowed = ('mode', 'min_mm', 'max_mm', 'lead_mm_per_rev', 'position_mm')
        if any(k not in allowed for k in settings):
            raise ValueError('Unknown mechanical setting')
        if settings.get('mode') == 'free':
            self.mechanics = {'mode': 'free', 'reference_valid': False}
        elif settings.get('mode') == 'pin':
            required = ('min_mm', 'max_mm', 'lead_mm_per_rev', 'position_mm')
            if not all(k in settings for k in required):
                raise ValueError('Pin mode requires explicit min/max, lead and manual position')
            for key in required:
                finite_number(settings[key], key, key == 'lead_mm_per_rev')
            if not settings['min_mm'] < settings['max_mm']:
                raise ValueError('min_mm must be smaller than max_mm')
            if not settings['min_mm'] <= settings['position_mm'] <= settings['max_mm']:
                raise ValueError('Manual position outside mechanical bounds')
            self.mechanics = dict(settings)
            self.mechanics['reference_valid'] = True
            self.reference_base = settings['position_mm']
            self.planner = MotionPlanner(self.driver.config, uart_latency_s=PLANNER_UART_BUDGET_S)
        else:
            raise ValueError('mode must be free or pin')
        return self.status()

    def reference(self, position):
        self._require_idle()
        finite_number(position, 'position_mm')
        if self.mechanics['mode'] != 'pin':
            raise ValueError('Configure explicit pin mechanics first')
        if not self.mechanics['min_mm'] <= position <= self.mechanics['max_mm']:
            raise ValueError('Manual position outside mechanical bounds')
        self.planner = MotionPlanner(self.driver.config, uart_latency_s=PLANNER_UART_BUDGET_S)
        self.reference_base = position
        self.mechanics['position_mm'] = position
        self.mechanics['reference_valid'] = True
        return self.status()

    def start(self, request):
        self._require_idle()
        if self.fault:
            raise ValueError('Clear fault before starting: ' + self.fault)
        args = {k: request[k] for k in ('mode', 'rpm', 'accel', 'decel',
                'revolutions', 'duration_s', 'cycles', 'dwell_s') if k in request}
        for key in ('mode', 'rpm', 'accel', 'decel'):
            if key not in args:
                raise ValueError('Missing ' + key)
        now = self.clock()
        candidate = MotionPlanner(self.driver.config, uart_latency_s=PLANNER_UART_BUDGET_S)
        candidate.start(now=now, **args)  # validate completely before touching HW
        position = self._pin_position(now)
        if self.mechanics['mode'] == 'pin':
            if position is None:
                raise ValueError('Pin reference unknown; manually set reference')
            if args['mode'] in ('revolutions', 'cycles'):
                sign = 1 if args['rpm'] > 0 else -1
                end = position + sign * args['revolutions'] * self.mechanics['lead_mm_per_rev']
                if not self.mechanics['min_mm'] <= end <= self.mechanics['max_mm']:
                    raise ValueError('Requested movement exceeds configured pin bounds')
        self._enable(False)
        if not self.driver.configured:
            self.driver.configure()
        self.last_diagnostics = self.driver.check_health(compact=True)
        if position is not None:
            self.reference_base = position
        self.planner = MotionPlanner(self.driver.config, uart_latency_s=PLANNER_UART_BUDGET_S)
        self.last_velocity = 0
        self.last_update = self.clock()
        self.last_tick = self.last_update
        self.last_health = self.last_update
        if self.driver.config['chopper'] == 'stealthchop':
            # STEP must be tied low. Allow hardware PWM_AUTOSCALE initialization
            # at IRUN while stationary. Main loop stays responsive to STOP.
            self.driver.set_velocity(0)
            self.driver.enable()
            self._enable(True)
            self.pending = args
            self.warm_until = self.clock() + 0.150
        else:
            # Rebase time after the relatively slow configuration transaction.
            self.planner.start(now=self.clock(), **args)
        return self.status()

    def change_speed(self, request):
        if self.pending:
            raise ValueError('Wait for driver initialization before changing speed')
        if not self.planner.active:
            raise ValueError('No continuous movement active')
        now = self.clock()
        if self.mechanics['mode'] == 'pin' and request.get('decel') is not None:
            decel = finite_number(request['decel'], 'decel', positive=True)
            position = self._pin_position(now)
            velocity = self.planner.status(now)['rpm_calculated']
            remaining = ((self.mechanics['max_mm'] - position) if velocity >= 0
                         else (position - self.mechanics['min_mm']))
            reserve = self.planner.stopping_distance_rev(decel=decel) * self.mechanics['lead_mm_per_rev']
            if velocity and reserve > remaining:
                raise ValueError('Proposed deceleration cannot stop within configured pin bounds')
        self.planner.set_speed(request.get('rpm'), accel=request.get('accel'),
                               decel=request.get('decel'), now=self.clock())
        return self.status()

    def stop(self, emergency=False):
        if emergency:
            self.emergency_stop()
        elif self.pending:
            self.pending = None
            self._enable(False)
            self.driver.disable()
            self.planner.emergency_stop(self.clock())
        else:
            self.planner.stop(now=self.clock())
        return self.status()

    def diagnose(self):
        self.last_diagnostics = self.driver.check_health() if self.driver.configured else self.driver.diagnostics()
        return self.status()

    def clear_fault(self):
        self._require_idle()
        self._enable(False)
        self.driver.configure()
        self.last_diagnostics = self.driver.check_health()
        self.fault = None
        return self.status()

    def tick(self, now, health_allowed=True):
        if self.fault:
            return
        try:
            if self.pending:
                if now < self.warm_until:
                    return
                args = self.pending
                self.pending = None
                self.planner.start(now=now, **args)
            if self.planner.active and now - self.last_update >= UPDATE_PERIOD_S - 0.000001:
                bounds = None
                if self.mechanics['mode'] == 'pin':
                    position = self._pin_position(now)
                    if position is None:
                        raise OSError('Pin reference lost')
                    if not self.mechanics['min_mm'] - 0.00001 <= position <= self.mechanics['max_mm'] + 0.00001:
                        raise OSError('Calculated pin boundary exceeded; reference invalid')
                    lead = self.mechanics['lead_mm_per_rev']
                    bounds = ((self.mechanics['min_mm'] - self.reference_base) / lead,
                              (self.mechanics['max_mm'] - self.reference_base) / lead)
                desired = self.planner.update(now, bounds=bounds)
                value = rpm_to_vactual(desired, self.driver.config)
                if value != self.last_velocity:
                    self.driver.set_velocity(value)
                    if value and not self.driver.enabled:
                        self.driver.enable()
                        self._enable(True)
                    applied_at = self.clock()
                    self.planner.applied(vactual_to_rpm(value, self.driver.config), applied_at)
                    self.last_velocity = value
                self.last_update = now
                if not self.planner.active:
                    if self.driver.config.get('hold_on_stop', False):
                        self.driver.set_velocity(0)
                        if not self.driver.enabled:
                            self.driver.enable()
                        self._enable(True)
                    else:
                        self._enable(False)
                        self.driver.disable()
                    self.planner.applied(0.0, self.clock())
                    self.last_velocity = 0
            if health_allowed and self.driver.enabled and now - self.last_health >= HEALTH_PERIOD_S:
                self.last_diagnostics = self.driver.check_health(compact=True)
                self.last_health = self.clock()
            self.last_tick = now
        except Exception as exc:
            self.emergency_stop(str(exc))


class Firmware:
    def __init__(self, motors, clock, heartbeat_timeout_s=HEARTBEAT_TIMEOUT_S):
        self.motors = motors
        self.clock = clock
        self.heartbeat_timeout_s = heartbeat_timeout_s
        self.last_heartbeat = clock()
        self.line = bytearray()
        self.overflow = False

    def emergency_stop(self, reason=None):
        for motor in self.motors.values():
            motor.emergency_stop(reason)

    def tick(self, now=None):
        explicit_now = now is not None
        now = self.clock() if now is None else now
        if now - self.last_heartbeat > self.heartbeat_timeout_s:
            for motor in self.motors.values():
                if motor.energized():
                    motor.emergency_stop('Desktop heartbeat timeout; motion will not resume')
        health_serviced = False
        for motor in self.motors.values():
            tick_now = now if explicit_now else self.clock()
            due = motor.driver.enabled and tick_now - motor.last_health >= HEALTH_PERIOD_S
            motor.tick(tick_now, health_allowed=not health_serviced)
            if due:
                health_serviced = True

    def handle(self, request):
        request_id = request.get('id') if isinstance(request, dict) else None
        motor = None
        try:
            if not isinstance(request, dict):
                raise ValueError('Request must be a JSON object')
            if 'id' in request and (isinstance(request['id'], bool) or not isinstance(request['id'], int)):
                raise ValueError('id must be an integer when supplied')
            cmd = request.get('cmd')
            if cmd == 'hello':
                result = {'protocol': 1, 'firmware': FIRMWARE_VERSION,
                          'motors': list(self.motors), 'profiles': DRIVER_PROFILES,
                          'config_schema': CONFIG_SCHEMA,
                          'heartbeat_timeout_s': self.heartbeat_timeout_s}
            elif cmd == 'heartbeat':
                self.last_heartbeat = self.clock()
                result = {'alive': True}
            elif cmd == 'status':
                names = [request['motor']] if 'motor' in request else list(self.motors)
                if any(name not in self.motors for name in names):
                    raise ValueError('Unknown motor')
                result = {'motors': [self.motors[name].status() for name in names]}
            elif cmd == 'stop' and 'motor' not in request:
                result = {'motors': [m.stop(bool(request.get('emergency', False))) for m in self.motors.values()]}
            else:
                name = request.get('motor')
                if name not in self.motors:
                    raise ValueError('Select a known motor')
                motor = self.motors[name]
                if cmd in ('configure', 'diagnose', 'clear_fault') and any(m.busy() for m in self.motors.values()):
                    raise ValueError('Stop all motion before full driver configuration/diagnostics')
                if cmd == 'move' and not motor.driver.configured and any(m.busy() for m in self.motors.values()):
                    raise ValueError('Configure all selected drivers while idle before simultaneous tests')
                if cmd == 'configure':
                    result = motor.configure(request.get('config'))
                elif cmd == 'move':
                    result = motor.start(request)
                elif cmd == 'speed':
                    result = motor.change_speed(request)
                elif cmd == 'stop':
                    result = motor.stop(bool(request.get('emergency', False)))
                elif cmd == 'mechanics':
                    result = motor.set_mechanics(request.get('settings'))
                elif cmd == 'reference':
                    result = motor.reference(request.get('position_mm'))
                elif cmd == 'diagnose':
                    result = motor.diagnose()
                elif cmd == 'clear_fault':
                    result = motor.clear_fault()
                else:
                    raise ValueError('Unknown command')
            return {'id': request_id, 'ok': True, 'result': result}
        except (ValueError, TypeError, KeyError) as exc:
            return {'id': request_id, 'ok': False, 'error': str(exc)}
        except Exception as exc:
            if motor is not None:
                motor.emergency_stop(str(exc))
            return {'id': request_id, 'ok': False, 'error': str(exc)}

    def feed(self, data):
        """Incremental bounded JSON framing; ! bypasses any malformed/long line."""
        replies = []
        for byte in data:
            if not isinstance(byte, int):
                byte = ord(byte)
            if byte == 33:
                self.emergency_stop()
                self.line = bytearray()
                self.overflow = False
            elif byte == 10:
                if self.overflow:
                    replies.append({'id': None, 'ok': False, 'error': 'Line exceeds 8192 bytes'})
                elif self.line:
                    try:
                        replies.append(self.handle(json.loads(bytes(self.line).decode('utf-8'))))
                    except Exception as exc:
                        replies.append({'id': None, 'ok': False, 'error': 'Invalid JSON: ' + str(exc)})
                self.line = bytearray()
                self.overflow = False
            elif byte != 13 and not self.overflow:
                if len(self.line) >= MAX_LINE_BYTES:
                    self.overflow = True
                    self.line = bytearray()
                else:
                    self.line.append(byte)
        return replies


def validate_channels(channels):
    names, pins, state_machines, uarts = set(), set(), set(), set()
    if not channels:
        raise ValueError('Configure at least one motor channel')
    for item in channels:
        if item['id'] in names:
            raise ValueError('Duplicate motor ID')
        names.add(item['id'])
        used = [item['enable_pin']] if item.get('enable_pin') is not None else []
        if item['transport'] == 'pio':
            used.append(item['pin'])
            sm = item.get('sm_id', 0)
            if sm not in range(8) or sm in state_machines:
                raise ValueError('Each PIO channel needs a unique SM in 0..7')
            state_machines.add(sm)
        elif item['transport'] == 'hardware':
            used += [item['tx'], item['rx']]
            uart = item['uart_id']
            if uart not in (0, 1) or uart in uarts:
                raise ValueError('Hardware UART must be independently allocated')
            valid = {0: ((0, 1), (12, 13), (16, 17)), 1: ((4, 5), (8, 9), (20, 21))}
            if (item['tx'], item['rx']) not in valid[uart]:
                raise ValueError('Unsupported Pico W hardware UART TX/RX pair')
            uarts.add(uart)
        else:
            raise ValueError('transport must be pio or hardware')
        if len(set(used)) != len(used) or any(pin in pins for pin in used):
            raise ValueError('Each motor needs separate UART/EN pins')
        if any(not isinstance(pin, int) or pin < 0 or pin > 28 or pin in (23, 24, 25) for pin in used):
            raise ValueError('Choose an exposed Pico W GPIO')
        pins.update(used)


def run():
    import sys
    import select
    import machine
    if sys.platform != 'rp2':
        raise RuntimeError('Firmware target is Raspberry Pi Pico W / RP2040 MicroPython')
    validate_channels(MOTOR_CHANNELS)
    clock = MonotonicClock()
    motors = {}
    # Inhibit every configured bridge before creating any serial transport.
    enables = {}
    for channel in MOTOR_CHANNELS:
        pin = channel.get('enable_pin')
        enables[channel['id']] = machine.Pin(pin, machine.Pin.OUT, value=1) if pin is not None else None
    for channel in MOTOR_CHANNELS:
        if channel['transport'] == 'pio':
            transport = PIOUARTTransport(channel['pin'], sm_id=channel.get('sm_id', 0))
        else:
            uart = machine.UART(channel['uart_id'], baudrate=115200,
                                tx=machine.Pin(channel['tx']), rx=machine.Pin(channel['rx']),
                                timeout=0, timeout_char=0)
            transport = HardwareUARTTransport(uart)
        motor = MotorController(channel['id'], Driver(transport, DEFAULT_MOTOR_CONFIG), clock,
                                enables[channel['id']])
        motors[channel['id']] = motor
        try:
            motor.driver.disable()
        except OSError as exc:
            # VM may be switched on after USB. Startup remains idle/inhibited;
            # the first move still requires a full successful driver check.
            motor.last_diagnostics = {'boot_stop_error': str(exc), 'enabled_commanded': False}
    app = Firmware(motors, clock)
    poller = select.poll()
    poller.register(sys.stdin, select.POLLIN)
    try:
        while True:
            app.tick()
            # Bounded input work keeps floods from starving motion/heartbeat.
            for _ in range(128):
                if not poller.poll(0):
                    break
                char = sys.stdin.read(1)
                if not char:
                    break
                for reply in app.feed(char.encode('utf-8')):
                    print(json.dumps(reply))
                app.tick()
            sleep_ms(1)
    finally:
        app.emergency_stop('Application exited')


# --- Optional host simulation: no physical sensor values are synthesized ---
class SimulatedTransport:
    """Register-level mock shared by GUI demo and integration tests."""
    def __init__(self):
        self.registers = {0: 0, 1: 1, 2: 0, 6: 0x20000100,
                          0x6C: 0x10000053, 0x6F: 0x80000000,
                          0x70: 0xC10D0024, 0x71: 0, 0x72: 0,
                          0x12: 0, 0x41: 0, 0x6A: 0, 0x6B: 0}
        self.stats = {'transactions': 0, 'tx_bytes': 0, 'rx_bytes': 0,
                      'errors': 0, 'timeouts': 0, 'simulated': True}
        self.fail = False
        self.bad_crc = False
        self.drop_writes = False
        self.writes = []

    def exchange(self, packet, reply_length=0):
        self.stats['transactions'] += 1
        self.stats['tx_bytes'] += len(packet)
        if self.fail:
            self.stats['errors'] += 1
            self.stats['timeouts'] += 1
            raise OSError('Simulated UART timeout')
        if len(packet) not in (4, 8) or packet[0:2] != bytes((5, 0)) or tmc_crc(packet[:-1]) != packet[-1]:
            self.stats['errors'] += 1
            raise OSError('Malformed simulated UART request')
        reg = packet[2] & 0x7F
        if packet[2] & 0x80:
            if not self.drop_writes:
                value = int.from_bytes(packet[3:7], 'big')
                # Only a recent diagnostic trace; counters cover the entire run.
                # Never retain an unbounded allocation per write in host simulation.
                if len(self.writes) == 128:
                    del self.writes[0]
                self.writes.append((reg, value))
                if reg == 1:
                    self.registers[1] &= ~value
                else:
                    self.registers[reg] = value
                self.registers[2] = (self.registers[2] + 1) & 255
            return b''
        value = self.registers.get(reg, 0)
        answer = bytearray((5, 255, reg))
        answer.extend(value.to_bytes(4, 'big'))
        answer.append(tmc_crc(answer) ^ (1 if self.bad_crc else 0))
        self.stats['rx_bytes'] += len(answer)
        return bytes(answer)

    def close(self):
        pass


class SimulatedEnablePin:
    def __init__(self):
        self.level = 1

    def value(self, level=None):
        if level is not None:
            self.level = level
        return self.level


def make_simulated_firmware(clock=None, motor_count=1):
    if clock is None:
        import time
        clock = time.monotonic if hasattr(time, 'monotonic') else MonotonicClock()
    if isinstance(motor_count, bool) or not isinstance(motor_count, int) or motor_count < 1:
        raise ValueError('motor_count must be a positive integer')
    motors = {}
    for index in range(motor_count):
        name = 'm' + str(index + 1)
        driver = Driver(SimulatedTransport(), DEFAULT_MOTOR_CONFIG)
        motors[name] = MotorController(name, driver, clock, SimulatedEnablePin())
    return Firmware(motors, clock)


if __name__ == '__main__':
    import sys
    if sys.platform == 'rp2':
        run()
