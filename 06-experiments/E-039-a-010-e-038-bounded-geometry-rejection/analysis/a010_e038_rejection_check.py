#!/usr/bin/env python3
"""Reproduce the bounded-interface rejection recorded in E-039.

This is an evidence checker, not a fabrication or solid-topology validator.
It inspects the shared dimensions and the audited E-035 SCAD representation.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parents[2]
CAD = ROOT / "E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_bounded_carriage.scad"
PARAMS = ROOT / "E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_carriage_params.scad"


def value(source: str, name: str) -> float:
    match = re.search(rf"^\s*{name}\s*=\s*([0-9.]+)\s*;", source, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing parameter: {name}")
    return float(match.group(1))


def main() -> None:
    params = PARAMS.read_text()
    cad = CAD.read_text()
    aperture = value(params, "gate_window")
    guide = value(params, "guide_y")
    pitch = value(params, "state_pitch")
    count = int(value(params, "state_count"))
    travel = (count - 1) * pitch
    required = aperture + travel
    assert required > guide, "frozen geometry contradiction disappeared"

    assert "field = cartridge;" in cad
    assert "cube([slider_x,field,gate_t])" in cad
    assert len(re.findall(r"gate_slider\(state_y\[", cad)) == 1
    assert "frame_plate(0,0.20,\"gray\");" in cad
    assert "frame_plate(stop_z,stop_t,\"lightblue\");" in cad
    assert "support" not in cad.lower()

    print(f"minimum_slider_envelope_mm={required:.2f}")
    print(f"frozen_guide_span_mm={guide:.2f}")
    print("defects=oversized_slider single_aperture missing_stop_support")
    print("PASS rejection evidence")


if __name__ == "__main__":
    main()
