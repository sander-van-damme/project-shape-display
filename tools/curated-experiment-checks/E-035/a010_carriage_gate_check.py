#!/usr/bin/env python3
"""Independent analytical gate; parses the shared SCAD parameter file."""
from pathlib import Path
import re
PARAMS = Path(__file__).with_name("a010_carriage_params.scad")
def p(name):
    m = re.search(rf"^\s*{name}\s*=\s*([0-9.]+)\s*;", PARAMS.read_text(), re.M)
    if not m: raise ValueError(f"missing shared parameter {name}")
    return float(m.group(1))
def check():
    pitch, n = p("state_pitch"), int(p("state_count"))
    states = tuple((i-(n-1)/2)*pitch for i in range(n))
    assert n == 5 and states == (-1.6, -0.8, 0.0, 0.8, 1.6)
    gate_radial = (p("gate_window") - p("follower_d"))/2
    stop_radial = (p("stop_bore") - p("follower_d"))/2
    shoulder_land = (p("shoulder_d") - p("stop_bore"))/2
    assert gate_radial > 0 and stop_radial > 0 and shoulder_land > 0
    assert p("guide_x") >= p("carriage_x") and p("guide_y") >= p("slider_y")
    assert p("slider_x") >= p("carriage_x")
    assert p("guide_z1") >= p("stop_z") + p("stop_t")
    assert p("gate_z") + p("gate_t") <= p("stop_z")
    travel = states[-1] - states[0]
    stroke = travel + 2*p("writer_approach")
    assert round(stroke, 8) == 3.60
    assert p("tab_engagement") > 0
    assert round((p("frame")-p("cartridge"))/2, 8) == 4.76
    return states, gate_radial, stop_radial, shoulder_land, travel, stroke
if __name__ == "__main__":
    s, g, stop, land, travel, stroke = check()
    print(f"states_y_mm={s}")
    print(f"state_travel_mm={travel:.2f} writer_stroke_mm={stroke:.2f}")
    print(f"gate_radial_clearance_mm={g:.2f} stop_radial_clearance_mm={stop:.2f}")
    print(f"shoulder_land_radial_mm={land:.2f}")
    print("PASS shared-datum aperture guide/carriage indexed-stop load-path writer clearances")
