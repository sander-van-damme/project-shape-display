"""E-301: copy all four .py files to MicroPython Pico W root. No Wi-Fi."""
from machine import Pin, UART
# First operations: reset-safe defaults, reinforced by EXTERNAL resistors.
enable = Pin(6, Pin.OUT, value=1)  # physical 9, EN_N active LOW
step = Pin(2, Pin.OUT, value=0)    # physical 4, external 10k pulldown
level = Pin(3, Pin.OUT, value=0)   # physical 5, DIR
import sys
import select
from time import sleep_ms
# Ctrl-C keeps its normal meaning; finally below disables the bridge.
from tmc2208 import Driver
from controller import Controller
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=1, timeout_char=1)
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)


def receive():
    result = ''
    # Bounded read: a continuous host flood cannot starve the safety loop.
    for _ in range(128):
        if not poller.poll(0):
            break
        char = sys.stdin.read(1)
        if not char:
            break
        result += char
    return result


app = Controller(step, level, enable, Driver(uart), receive)
print('E-301 Pico W OFF. Set/check Vref 0.80 V; ? for help.')
try:
    while True:
        app.poll()
        sleep_ms(1)
finally:
    app.off()
