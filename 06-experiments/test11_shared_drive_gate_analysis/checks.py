#!/usr/bin/env python3
"""Assertions for the S3/S4/S5 rejection gates.

These checks encode the *decision thresholds* proposed in README.md. They fail
loudly when an input drifts into a regime the candidate cannot survive. They are
not a mechanism qualification; passing means only that the arithmetic still
permits printing the smallest coupon.

Run: python checks.py
"""

from __future__ import annotations

import sys

from model import (
    S3Config, S4Config, s3_bom, s3_full_map_time,
    s3_printable_fanout_feasibility, s3_selector_force,
    s4_clutch_reality_check, s4_correlated_fault, s4_full_map_time,
    s5_gate_summary, s5_cost_ceiling, DEADLINE_S, PITCH_MM,
)


def check(name: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def main() -> int:
    ok = True
    c3, c4 = S3Config(), S4Config()

    t3 = s3_full_map_time(c3)
    ok &= check("S3 full-map <30 s", t3["total_s"] < DEADLINE_S,
                f"{t3['total_s']:.3f} s (margin {t3['margin_to_30_s']:.3f} s)")

    f3 = s3_selector_force(c3)
    ok &= check("S3 per-bank motor force <2 N", f3["motor_force_requirement_n"] < 2.0,
                f"{f3['motor_force_requirement_n']:.3f} N assumed mu=0.30/preload=0.1 N")

    b3 = s3_bom(c3)
    ok &= check("S3 bought per-channel selectors == 0", b3["bought_selector_count"] == 0,
                f"printable selectors={b3['printable_selector_count']}, allowance ${b3['purchased_allowance_usd']:.2f}")

    fan = s3_printable_fanout_feasibility(c3)
    ok &= check("S3 selector features at 0.4 mm nozzle", fan["features_per_cam_land_at_0p4mm"] >= 2.0,
                f"{fan['features_per_cam_land_at_0p4mm']:.3f} features on a {fan['cam_land_width_mm_per_row']:.2f} mm land")

    t4 = s4_full_map_time(c4)
    ok &= check("S4 full-map <30 s", t4["full_map_s"] < DEADLINE_S,
                f"{t4['full_map_s']:.3f} s")

    clut = s4_clutch_reality_check(c4)
    ok &= check("S4 bought clutch path is unaffordable (proves printed clutch required)",
                clut["printable_clutch_required"], f"64 x $6 = ${clut['bought_clutch_total_usd']:.0f}")

    corr = s4_correlated_fault(c4)
    ok &= check("S4 correlated bus backlash within decoder margin",
                corr["height_error_at_last_tile_mm"] <= corr["decoder_margin_mm"],
                f"{corr['height_error_at_last_tile_mm']:.4f} mm vs {corr['decoder_margin_mm']:.2f} mm")

    gates = s5_gate_summary()
    ok &= check("S5 still has unresolved gates (status is honest)",
                gates["passed"] == 0, f"{gates['passed']}/{gates['total']} passed")

    cost = s5_cost_ceiling()
    ok &= check("S5 $1.25 motor allowance does NOT fit $500 w/ 20% contingency",
                cost["passes"] is False, f"max ${cost['max_motor_each_usd']:.3f}/motor")

    ok &= check("Fan-out land / pitch", abs(fan["cam_land_width_mm_per_row"] - PITCH_MM / c3.rows_per_station) < 1e-9,
                "4 rows share one 5.08 mm band")

    print()
    print("ALL CHECKS PASS" if ok else "ONE OR MORE CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
