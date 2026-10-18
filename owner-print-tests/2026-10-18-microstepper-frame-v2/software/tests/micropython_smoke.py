"""Portable simulated runtime smoke, also runs in MicroPython 1.26.1 unix.

Run with the interpreter from software/: micropython tests/micropython_smoke.py
This checks interpreter compatibility, not RP2040 peripherals or motor motion.
"""
import sys

sys.path.insert(0, sys.path[0] + "/..")
import main


def run():
    # Reproduce long-uptime clock accumulation on RP2040 float32 without waiting
    # nine hours: 1 ms additions to a 32768-second float otherwise round to zero.
    old_ticks_us, old_ticks_diff = main.ticks_us, main.ticks_diff
    fake_ticks = [0]
    main.ticks_us = lambda: fake_ticks[0]
    main.ticks_diff = lambda a, b: a - b
    try:
        accumulated = main.MonotonicClock()
        for _ in range(1024):
            fake_ticks[0] += 32000000
            accumulated()
        before = accumulated()
        for _ in range(20):
            fake_ticks[0] += 1000
            accumulated()
        assert accumulated() - before > 0.015, "Clock lost small elapsed ticks"
    finally:
        main.ticks_us, main.ticks_diff = old_ticks_us, old_ticks_diff

    # Float32 rounding must retain both signed 24-bit extrema.
    for value in (-8388608, -1, 1, 8388607):
        rpm = main.vactual_to_rpm(value, main.DEFAULT_MOTOR_CONFIG)
        assert main.rpm_to_vactual(rpm, main.DEFAULT_MOTOR_CONFIG) == value

    clock = [0.0]
    firmware = main.make_simulated_firmware(clock=lambda: clock[0], motor_count=2)
    sequence = [0]

    def request(command, **fields):
        sequence[0] += 1
        fields["id"] = sequence[0]
        fields["cmd"] = command
        reply = firmware.handle(fields)
        assert reply["ok"], reply
        return reply["result"]

    def advance(seconds, heartbeat=True):
        endpoint = clock[0] + seconds
        while clock[0] < endpoint:
            clock[0] = min(endpoint, clock[0] + 0.01)
            if heartbeat:
                request("heartbeat")
            firmware.tick(clock[0])

    def status(motor="m1"):
        return request("status", motor=motor)["motors"][0]

    hello = request("hello")
    assert hello["protocol"] == 1
    assert len(hello["motors"]) == 2
    request("configure", motor="m1", config={})
    request("configure", motor="m2", config={})
    request("move", motor="m1", mode="continuous", rpm=600,
            accel=3000, decel=3000)
    request("move", motor="m2", mode="continuous", rpm=-30,
            accel=120, decel=120)
    advance(0.6)
    assert status()["motion"]["rpm_calculated"] > 590
    assert status("m2")["motion"]["rpm_calculated"] < -29
    request("speed", motor="m1", rpm=-600)
    advance(0.6)
    assert status()["motion"]["rpm_calculated"] < -590
    request("stop", motor="m1")
    advance(0.5)
    assert status()["state"] == "idle"
    assert status("m2")["state"] == "running"
    firmware.feed(b'{"id":999,"cmd":"bad incomplete input !')
    assert status("m2")["state"] == "idle"
    request("move", motor="m1", mode="cycles", rpm=60,
            accel=120, decel=120, revolutions=0.5, cycles=3, dwell_s=0.02)
    advance(15)
    assert status()["motion"]["completed"]
    assert abs(status()["motion"]["position_rev_calculated"]) < 0.03
    request("mechanics", motor="m1", settings={"mode": "pin", "min_mm": 0,
            "max_mm": 12, "lead_mm_per_rev": 3, "position_mm": 6})
    request("move", motor="m1", mode="continuous", rpm=60,
            accel=120, decel=120)
    advance(8)
    assert status()["state"] == "idle", status()
    assert status()["mechanics"]["position_mm_calculated"] <= 12
    request("move", motor="m2", mode="continuous", rpm=60,
            accel=120, decel=120)
    advance(2.2, heartbeat=False)
    assert status("m2")["state"] == "fault"
    request("heartbeat")
    request("clear_fault", motor="m2")
    assert status("m2")["state"] == "idle"
    print("PASS: simulated firmware runtime on", sys.implementation.name,
          sys.implementation.version)


if __name__ == "__main__":
    run()
