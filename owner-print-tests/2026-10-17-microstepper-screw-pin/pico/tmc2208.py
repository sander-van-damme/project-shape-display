"""TMC2208 single-wire UART, external R110; no OTP writes. MicroPython RP2."""
from time import ticks_ms, ticks_diff, sleep_ms

GCONF = 0x1C5  # analog Vref, external sense, SpreadCycle, PDN off, register MRES
CHOPCONF = (5 << 24) | (1 << 17) | (1 << 15) | (5 << 4) | 4
CURRENT = (5 << 8) | 5  # IRUN = IHOLD = 5; delay = 0


def crc(data):
    value = 0
    for byte in data:
        for _ in range(8):
            mix = (value >> 7) ^ (byte & 1)
            value = (value << 1) & 255
            if mix:
                value ^= 7
            byte >>= 1
    return value


class Driver:
    def __init__(self, uart):
        self.uart = uart
        self.counter = None

    def read(self, reg):
        # RX sees TX echo through the 1k resistor. Require exact echo AND reply.
        if self.uart.any():
            self.uart.read()
        request = bytearray((5, 0, reg))
        request.append(crc(request))
        self.uart.write(request)
        packet = bytearray()
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < 35 and len(packet) < 12:
            chunk = self.uart.read(12 - len(packet))
            if chunk:
                packet.extend(chunk)
        if len(packet) != 12 or packet[:4] != request:
            raise OSError('UART timeout/echo; check PDN bridge, RX/TX and power')
        reply = packet[4:]
        if reply[:3] != bytes((5, 255, reg)) or crc(reply[:7]) != reply[7]:
            raise OSError('UART reply address/register/CRC')
        return int.from_bytes(reply[3:7], 'big')

    def write_checked(self, reg, value):
        before = self.read(2) & 255
        message = bytearray((5, 0, reg | 128))
        message.extend(value.to_bytes(4, 'big'))
        message.append(crc(message))
        self.uart.write(message)
        # 8 bytes at 115200 baud plus settling; drain write echo on next read.
        sleep_ms(6)
        after = self.read(2) & 255
        if ((after - before) & 255) != 1:
            raise OSError('UART write not acknowledged, reg=%02x' % reg)
        self.counter = after

    def configure(self):
        if self.read(6) >> 24 != 0x20 or not (self.read(6) & 256):
            raise OSError('Expected TMC2208 IOIN version 0x20 and SEL_A=1')
        # EN remains HIGH throughout. Each write checked individually, including
        # write-only IHOLD_IRUN and VACTUAL; never pretend they can be read back.
        for reg, value in ((0, GCONF), (0x6C, CHOPCONF), (0x10, CURRENT),
                           (0x11, 0), (0x13, 0), (0x22, 0), (1, 7)):
            self.write_checked(reg, value)
        self.health()

    def health(self):
        if self.read(0) != GCONF or self.read(0x6C) != CHOPCONF:
            raise OSError('Driver configuration changed/reset')
        if self.read(2) & 255 != self.counter:
            raise OSError('Unexpected IFCNT/reset')
        if self.read(1) & 7:
            raise OSError('Driver reset/undervoltage/driver error')
        # Short/overtemperature/prewarning. Open-load at tiny current is not a
        # reliable diagnostic and is deliberately not treated as stall sensing.
        if self.read(0x6F) & 0x3F:
            raise OSError('Driver temperature/short fault')
