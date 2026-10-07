#!/usr/bin/env python3
"""Nominal and worst-case geometric checks for the E-033 A-010 insert.

This is an analytical envelope check.  It does not model friction, material
strength, compliance, print/process capability, or reader performance.
"""

from dataclasses import dataclass
from math import hypot


PITCH = 5.08
N = 5
FRAME = 40.0
ACTIVE = 25.40
CENTRE_SPAN = 20.32
FID = ((-15.0, -15.0), (15.0, 15.0))
READER_TARGET = (0.0, 0.0, 3.0, 3.0)

# A-010 cartridge and motion inputs, all millimetres.
CARTRIDGE = 30.48                 # 5 pitches plus 2.54 mm perimeter margin
SLIDER = (4.20, 4.60)              # transverse width, travel length
POCKET = (4.50, 4.90)              # guide pocket, same axes as SLIDER
RUNNING_CLEARANCE_TOTAL = POCKET[1] - SLIDER[1]
APERTURE = 3.00
FOLLOWER_DIAMETER = 1.20
STATE_STEP = 0.80
STATE_COUNT = 5
STATE_TRAVEL = STATE_STEP * (STATE_COUNT - 1)
WRITER_ENGAGEMENT = 0.60
WRITER_STROKE = STATE_TRAVEL + 0.40  # 0.20 mm end approach each end
WRITER_WIDTH = 1.00
WRITER_THICKNESS = 0.80
PARKED_CLEARANCE = 0.20
STOP_FACE = 0.60
STOP_STEP = STATE_STEP

# Declared stack measured from the frozen frame upper face (z=0).
LAYERS = [
    ("lower guide", 0.00, 0.40),
    ("gate slider", 0.40, 0.80),
    ("upper guide", 0.80, 1.20),
    ("five-stop plate", 1.20, 2.00),
]


@dataclass(frozen=True)
class Result:
    name: str
    value: float
    limit: float

    def check(self) -> None:
        assert self.value >= self.limit, f"{self.name}: {self.value} < {self.limit}"


def cell_centres():
    for row in range(N):
        for col in range(N):
            yield ((col - 2) * PITCH, (row - 2) * PITCH)


def main() -> None:
    assert abs((N - 1) * PITCH - CENTRE_SPAN) < 1e-9
    assert ACTIVE < FRAME
    assert abs(CARTRIDGE - (N * PITCH + 5.08)) < 1e-9

    # The two fiducial disks are outside the 25.40 mm active envelope and do
    # not overlap the 3 x 3 mm reader target.
    for x, y in FID:
        assert abs(x) > ACTIVE / 2 and abs(y) > ACTIVE / 2
        assert hypot(x, y) > 1.5

    Result("slider running clearance total", RUNNING_CLEARANCE_TOTAL, 0.20).check()
    Result("aperture/follower diametral margin", APERTURE - FOLLOWER_DIAMETER, 0.20).check()
    Result("five-state travel", STATE_TRAVEL, 3.20).check()
    Result("writer engagement", WRITER_ENGAGEMENT, 0.20).check()
    Result("writer stroke", WRITER_STROKE, STATE_TRAVEL).check()
    Result("writer parked clearance", PARKED_CLEARANCE, 0.20).check()
    Result("stop-face width", STOP_FACE, 0.40).check()
    assert all(b > a for _, a, b in LAYERS)
    assert LAYERS[-1][2] == 2.00

    # A 3.0 mm square reader target remains within the active envelope and
    # never consumes a fiducial or datum land by nominal geometry.
    rx, ry, rw, rh = READER_TARGET
    assert abs(rx) + rw / 2 <= ACTIVE / 2
    assert abs(ry) + rh / 2 <= ACTIVE / 2

    # Conservative rectangular tolerance exercise: +/-0.10 mm placement error
    # per guide/gate interface.  This is a bound, not process capability.
    placement_bound = 0.10 + 0.10 + 0.10
    residual_margin = (APERTURE - FOLLOWER_DIAMETER) / 2 - placement_bound
    assert residual_margin >= 0.20

    # Keep-out: cartridge perimeter stays 2.54 mm inside the 40 mm frame.
    edge_clearance = (FRAME - CARTRIDGE) / 2
    Result("cartridge edge clearance", edge_clearance, 2.00).check()

    print("PASS nominal A-010 E-033 geometry checks")
    print(f"cells={N*N} pitch_mm={PITCH:.2f} state_travel_mm={STATE_TRAVEL:.2f}")
    print(f"stack_height_mm={LAYERS[-1][2]:.2f} placement_bound_mm={placement_bound:.2f}")
    print(f"residual_margin_mm={residual_margin:.2f} edge_clearance_mm={edge_clearance:.2f}")


if __name__ == "__main__":
    main()
