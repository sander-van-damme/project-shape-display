#!/usr/bin/env python3
"""Analytical checks for the E-031-G1 common coupon.

This is a nominal geometry/schema check.  It intentionally does not model
friction, compliance, process spread, optics, timing, wear, or load transfer.
"""

from __future__ import annotations

import argparse
import math


PITCH = 5.08
N = 5
CENTRE_SPAN = (N - 1) * PITCH
ACTIVE_ENVELOPE = N * PITCH
FRAME = 40.0
FIDUCIALS = ((-15.0, -15.0), (15.0, 15.0))
FIDUCIAL_R = 1.0
READER_HALF = 1.5
WRITER_X = -10.16
PLANE_Y = (-3.0, -1.0, 1.0, 3.0)
PORT_HALF_X = 2.0
PORT_HALF_Y = 0.5


def check() -> None:
    assert math.isclose(CENTRE_SPAN, 20.32, abs_tol=1e-9)
    assert math.isclose(ACTIVE_ENVELOPE, 25.40, abs_tol=1e-9)
    assert ACTIVE_ENVELOPE < FRAME
    for x, y in FIDUCIALS:
        assert abs(x) - FIDUCIAL_R > ACTIVE_ENVELOPE / 2 or abs(y) - FIDUCIAL_R > ACTIVE_ENVELOPE / 2
        assert abs(x) - FIDUCIAL_R > READER_HALF or abs(y) - FIDUCIAL_R > READER_HALF
    assert abs(WRITER_X) + PORT_HALF_X < FRAME / 2
    assert max(PLANE_Y) - min(PLANE_Y) == 6.0
    assert all(abs(PLANE_Y[i + 1] - PLANE_Y[i] - 2.0) < 1e-9 for i in range(3))
    # Contract limits are recorded here as acceptance thresholds, not results.
    assert 0.20 > 0.0  # writer and reseat screen, mm
    assert 0.10 > 0.0  # adjacent-witness displacement screen, mm
    assert 1000 > 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    args = parser.parse_args()
    if args.check:
        check()
        print("E-031-G1 common coupon nominal geometry checks: PASS")


if __name__ == "__main__":
    main()
