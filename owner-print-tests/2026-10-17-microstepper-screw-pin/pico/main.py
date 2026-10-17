"""E-301: copy all four .py files to MicroPython Pico W root. No Wi-Fi."""
from machine import Pin, UART
import sys
import select
from time import sleep_ms
# Ctrl-C runs the same best-effort UART stop in finally.
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


app = Controller(Driver(uart), receive)
print('E-301 Pico W UART-only. OFF requested; Set/check Vref 0.80 V; ? for help.')
try:
    while True:
        app.poll()
        sleep_ms(1)
finally:
    app.off()
