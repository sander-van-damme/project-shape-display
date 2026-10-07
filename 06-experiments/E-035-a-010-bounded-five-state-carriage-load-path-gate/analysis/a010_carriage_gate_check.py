#!/usr/bin/env python3
"""Geometry/tolerance gate for bounded A-010; not hardware validation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class G:
    state_pitch: float = 0.80
    follower_d: float = 1.20
    gate_window: float = 3.00
    stop_bore: float = 1.60
    shoulder_d: float = 3.00
    guide_pocket: float = 4.50
    slider: float = 4.20
    carriage_slot: float = 4.60
    carriage: float = 4.00
    frame: float = 40.00
    cartridge: float = 30.48

def check(g=G()):
    states = tuple(i * g.state_pitch for i in range(5))
    assert tuple(round(x, 8) for x in states) == (0.00, 0.80, 1.60, 2.40, 3.20)
    assert len(states) == 5
    gate_radial = (g.gate_window - g.follower_d) / 2
    stop_radial = (g.stop_bore - g.follower_d) / 2
    shoulder_land = (g.shoulder_d - g.stop_bore) / 2
    assert tuple(round(x, 8) for x in (gate_radial, stop_radial, shoulder_land)) == (0.90, 0.20, 0.70)
    assert round(g.guide_pocket - g.slider, 8) == 0.30
    assert g.carriage <= g.carriage_slot
    assert round(states[-1] - states[0], 8) == 3.20
    assert round(states[-1] - states[0] + 2 * 0.20, 8) == 3.60
    assert round((g.frame - g.cartridge) / 2, 8) == 4.76
    return states, gate_radial, stop_radial, shoulder_land

if __name__ == "__main__":
    states, gate, stop, land = check()
    print(f"states_mm={states}")
    print("state_travel_mm=3.20 writer_stroke_mm=3.60")
    print(f"gate_radial_clearance_mm={gate:.2f} stop_radial_clearance_mm={stop:.2f}")
    print(f"shoulder_land_radial_mm={land:.2f} guide_running_clearance_mm=0.30")
    print("cartridge_edge_margin_mm=4.76")
    print("load_path=shoulder->selected_stop_land->stop_plate->frame")
    print("PASS bounded A-010 carriage geometry")
