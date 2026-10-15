#!/usr/bin/env python3
"""Analytical/finite checks for E-295's underside hex driver; not a fit test."""
import json
import math


def hex_clearance(male_af, female_af, phase_deg, dx=0.0, dy=0.0):
    """Smallest signed margin to any female-hex side for all male vertices."""
    radius = male_af / math.sqrt(3)
    vertices = [
        (dx + radius * math.cos(math.radians(phase_deg + 60 * i)),
         dy + radius * math.sin(math.radians(phase_deg + 60 * i)))
        for i in range(6)
    ]
    return min(
        female_af / 2 - x * math.cos(math.radians(30 + 60 * j))
        - y * math.sin(math.radians(30 + 60 * j))
        for x, y in vertices for j in range(6)
    )


def main():
    pitch, collar_d, male_af, throat_af, mouth_af = 5.08, 4.4, 2.0, 2.2, 3.0
    tip_r = male_af / math.sqrt(3)
    phase_halfwindow = 30 - math.degrees(math.acos(throat_af / (2 * tip_r)))
    assert abs(hex_clearance(male_af, throat_af, 0) - 0.1) < 1e-12
    assert abs(hex_clearance(male_af, throat_af, phase_halfwindow)) < 1e-12
    assert hex_clearance(male_af, throat_af, phase_halfwindow + 0.001) < 0
    assert hex_clearance(male_af, throat_af, 0, dy=0.2) < 0
    assert hex_clearance(male_af, throat_af, 30) < 0
    mouth_capture = mouth_af / 2 - tip_r
    # Finite angular cross-check of the conservative all-phase/all-offset bound.
    for phase_i in range(361):
        for offset_i in range(73):
            phase = phase_i / 6
            angle = math.radians(offset_i * 5)
            assert hex_clearance(
                male_af, mouth_af, phase,
                mouth_capture * math.cos(angle), mouth_capture * math.sin(angle)
            ) > -1e-10
    results = {
        "evidence": "ideal planar geometry, no print/runout/compliance qualification",
        "tip_corner_diameter_mm": 2 * tip_r,
        "centered_throat_half_phase_window_deg": phase_halfwindow,
        "all_phase_mouth_capture_radius_mm": mouth_capture,
        "throat_wall_at_corner_mm": collar_d / 2 - throat_af / math.sqrt(3),
        "mouth_wall_at_corner_mm": collar_d / 2 - mouth_af / math.sqrt(3),
        "tip_to_neighbor_collar_gap_at_point2_offset_mm": pitch - collar_d / 2 - tip_r - 0.2,
        "ideal_phase_search_gap_at_60rpm_seconds": (60 - 2 * phase_halfwindow) / 360,
        "conservative_full_phase_period_at_60rpm_seconds": 1 / 6,
        "keeper_shelf_for_actual_3p6_hole_mm": (collar_d - 3.6) / 2,
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
