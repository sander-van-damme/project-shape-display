#!/usr/bin/env python3
"""Second check of shared parameters, with explicit interval assertions."""
from a010_carriage_gate_check import p
states = tuple((i-2)*p("state_pitch") for i in range(int(p("state_count"))))
assert states == (-1.6, -0.8, 0.0, 0.8, 1.6)
assert all(round(b-a, 8) == p("state_pitch") for a,b in zip(states, states[1:]))
assert p("gate_window")/2 > p("follower_d")/2
assert p("stop_bore")/2 > p("follower_d")/2
assert p("shoulder_d")/2 > p("stop_bore")/2
assert p("guide_x")-p("carriage_x") >= 0.5
assert p("guide_y")-p("slider_y") >= 0.3
assert p("guide_z1")-(p("stop_z")+p("stop_t")) >= 0
assert p("gate_z")+p("gate_t") <= p("stop_z")
assert round(states[-1]-states[0]+2*p("writer_approach"), 8) == 3.6
assert p("tab_engagement") > 0
print("PASS independent shared-parameter recheck")
print("indexed_stop_count=5 selected_stop_identity=one_of_S0_to_S4")
print("load_reaction=shoulder_to_selected_stop_land_to_stop_plate_to_frame")
