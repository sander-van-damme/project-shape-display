"""Manual finite-pulse helper for MicroPython Pico, NOT hardware-tested.
No auto-run, repeated cycles, current or temperature measurement.
External 10k pulldowns and current-limited supply remain required.
"""
from machine import Pin
import time
sleep_pin=Pin(4,Pin.OUT,value=0)
a=Pin(2,Pin.OUT,value=0)
b=Pin(3,Pin.OUT,value=0)
def off():
    a.value(0);b.value(0);sleep_pin.value(0)
def pulse(sign,ms):
    if sign not in ['+','-'] or ms not in [200,1000,2000]:raise ValueError('Invalid pulse')
    off();time.sleep_ms(5)
    try:
        sleep_pin.value(1);time.sleep_ms(5)
        a.value(sign=='+');b.value(sign=='-')
        time.sleep_ms(ms)
    finally:
        off()
print('No physical validation. Verify current limit and temperature first.')
print('+ or - = 200ms. +1/-1 = 1s. +2/-2 = 2s ONLY at <=0.3A.')
print('Longer readings require settled scale and thermal checks in test.md. q exits.')
try:
    while True:
        s=input('Pulse (power is OFF): ').strip()
        if s=='q':break
        if s not in ['+','-','+1','-1','+2','-2']:
            print('Unknown command; OFF');continue
        duration=200 if len(s)==1 else int(s[1])*1000
        pulse(s[0],duration)
        print('OFF. Cooling 20s; recheck temperature before next command.')
        time.sleep_ms(20000)
finally:
    off()
