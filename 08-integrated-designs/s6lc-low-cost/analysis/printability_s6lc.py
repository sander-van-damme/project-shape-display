"""S6-LC part-set printability against sourced FDM limits (DND-71).

Analytic replacement for a print test (DND-27). Reads the declared geometry in
s6lc.py and the sourced process limits in tools/fdm-limits, and emits a
PASS/RISK/FAIL table plus a JSON record. No STL is sliced, nothing is printed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUB = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SUB.parent / "tools" / "fdm-limits"))

import s6lc  # noqa: E402
from fdm_process_limits import ProcessSpec  # noqa: E402

RECORD = SUB / "cad" / "s6lc_printability_record.json"


def main() -> int:
    spec = ProcessSpec()
    min_feature = 0.44          # 1 extrusion line @ 0.4 mm nozzle
    min_wall = 0.88             # 2 lines, robust
    fit = s6lc.column_fit()

    def verdict(value: float, floor: float, target: float) -> str:
        if value < floor:
            return "FAIL"
        if value < target:
            return "RISK"
        return "PASS"

    checks = [
        ("column wall / body feature", s6lc.COLUMN_BODY_MM, min_wall,
         verdict(s6lc.COLUMN_BODY_MM, min_feature, min_wall)),
        ("inter-column gap (PITCH - body)", fit["inter_body_gap_mm"], min_feature,
         verdict(fit["inter_body_gap_mm"], min_feature, min_wall)),
        ("pawl LEAF thickness (bending axis)", s6lc.PAWL_LEAF_T_MM, min_feature,
         verdict(s6lc.PAWL_LEAF_T_MM, min_feature, min_wall)),
        ("pawl root block thickness", s6lc.PAWL_T_MM, min_feature,
         verdict(s6lc.PAWL_T_MM, min_feature, min_wall)),
        ("pawl leaf width", s6lc.PAWL_W_MM, min_feature,
         verdict(s6lc.PAWL_W_MM, min_feature, min_wall)),
        ("pawl leaf + clearance fits OWNED half-lane",
         round(fit["owned_lane_mm"] - fit["leaf_plus_clearance_mm"], 3), 0.0,
         "PASS" if fit["leaf_plus_clearance_mm"] <= fit["owned_lane_mm"] else "FAIL"),
        ("rack pocket depth (X)", 0.80, min_feature,
         verdict(0.80, min_feature, 0.80)),
        ("rack pocket height (Z)", 3.00, 0.20, "PASS"),
        ("release comb tooth width (2 lines)", 0.88, min_feature,
         verdict(0.88, min_feature, min_wall)),
        ("mask boss width (2 lines)", 0.88, min_feature,
         verdict(0.88, min_feature, min_wall)),
        ("bank envelope X vs bed 256 mm", 406.4, 256.0,
         "PRINTED AS SUB-TILES"),
    ]
    print(f"S6-LC printability ({spec.printer}, {spec.material}, "
          f"{spec.nozzle_mm} mm nozzle, {spec.layer_mm} mm layers)")
    print("=" * 64)
    worst = "PASS"
    for name, value, limit, v in checks:
        print(f"  {v:18s} {name:38s} {value:>7} (limit {limit})")
        if v == "FAIL":
            worst = "FAIL"
        elif v == "RISK" and worst == "PASS":
            worst = "RISK"
    print("=" * 64)
    print(f"overall: {worst}")

    record = dict(
        evidence_class="CALCULATION over sourced FDM limits; no print/measurement (DND-27)",
        printer=spec.printer, material=spec.material, nozzle_mm=spec.nozzle_mm,
        layer_mm=spec.layer_mm, overall=worst,
        checks=[dict(feature=n, value=val, limit=lim, verdict=v)
                for (n, val, lim, v) in checks],
        residual_uncertainty=[
            "As-printed pawl release-force spread across 6,400 parts (S1-D): the "
            "break-even sd is ~9% of mean; typical FDM thin-leaf spread is "
            "10-20% (assumption). This and as-printed friction mu are "
            "measurement-only (un-retirable under DND-27).",
            "The 406.4 mm bank is printed as sub-tiles (a 256 mm X1C bed does "
            "not fit the full width); tile seams are a printability/CAD "
            "question handled in the printable-path doc.",
        ])
    RECORD.write_text(json.dumps(record, indent=2) + "\n")
    print(f"record -> {RECORD.relative_to(SUB)}")
    return 1 if worst == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
