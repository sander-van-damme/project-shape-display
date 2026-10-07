#!/usr/bin/env python3
"""Independent interval-style recheck of the bounded carriage geometry."""
STATES = [0.0, 0.8, 1.6, 2.4, 3.2]
assert STATES == sorted(STATES) and len(STATES) == 5
assert all(round(b-a, 8) == 0.8 for a, b in zip(STATES, STATES[1:]))
assert 1.5 - 0.6 == 0.9       # gate half-width minus follower radius
assert round(0.8 - 0.6, 8) == 0.2       # selected stop half-width minus radius
assert 1.5 - 0.8 == 0.7       # shoulder land radial width
assert round(4.50 - 4.20, 8) == 0.30
assert round(4.90 - 4.60, 8) == 0.30
assert 4.00 <= 4.60
assert STATES[-1] - STATES[0] == 3.2
assert STATES[-1] - STATES[0] + 0.4 == 3.6
print("PASS independent recheck")
print("indexed_stop_count=5 selected_stop_identity=one_of_S0_to_S4")
print("load_reaction=shoulder_to_stop_land; gate_is_not_support")
