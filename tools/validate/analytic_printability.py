#!/usr/bin/env python3
"""Analytic FDM printability checker for the Shape Display test coupons.

This is the **analytic replacement for the physical print test** (board directive
DND-27). It reads the coupon's declared geometry directly from the OpenSCAD
source and compares every printed feature against *sourced* FDM process limits
from `tools/fdm-limits/fdm_process_limits.py`. It produces a PASS / RISK / FAIL
table and a machine-readable JSON record.

WHAT IT IS
----------
    evidence class: CALCULATION over CAD-declared parameters.
    No STL is sliced, nothing is printed, nothing is measured.

WHAT IT IS NOT
--------------
    It is not a printer. It cannot catch a real slicer bug, a tuning problem,
    or material/lot variation. Those residuals are listed explicitly in the
    output so no reader mistakes this table for physical validation.

USAGE
-----
    python tools/validate/analytic_printability.py \
        06-experiments/test11_shared_drive_gate_analysis/selector_fanout_coupon.scad
    python tools/validate/analytic_printability.py --json out.json <coupon.scad>

Called with no argument it defaults to the T11-A selector fan-out coupon.

EXIT CODES
----------
    0   the checker ran and produced a verdict (PASS, RISK **or FAIL**).
        A printability FAIL is a *design* finding, not a tool error, so it does
        not fail the process by default. This matches the unified harness,
        which reports a FAIL as a design finding and still exits 0.
    1   the checker ran and the verdict is FAIL, **only** when
        `--fail-on-design-fail` is passed (opt in to gate on the design risk).
    2   the checker could not run (missing/invalid coupon source).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "fdm-limits"))
from fdm_process_limits import (  # noqa: E402
    ProcessSpec,
    lateral_clearance,
    rules,
)

DEFAULT_COUPON = (
    HERE.parents[1]
    / "06-experiments"
    / "test11_shared_drive_gate_analysis"
    / "selector_fanout_coupon.scad"
)


def parse_scad_constants(path: Path) -> dict[str, float]:
    """Read `NAME = <number>;` assignments from an OpenSCAD file.

    Only simple numeric constants are read (that is all the coupons use), so
    the checker tracks the CAD source of truth instead of duplicating values.
    """
    text = path.read_text()
    consts: dict[str, float] = {}
    for m in re.finditer(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*([0-9.]+)\s*;", text, re.M):
        consts[m.group(1)] = float(m.group(2))
    # derived band if the file computes it
    m = re.search(r"^\s*BAND\s*=\s*PITCH\s*/\s*ROWS_PER_STATION\s*;", text, re.M)
    if m and "PITCH" in consts and "ROWS_PER_STATION" in consts:
        consts["BAND"] = consts["PITCH"] / consts["ROWS_PER_STATION"]
    return consts


@dataclass
class Check:
    feature: str
    value_mm: float
    limit_mm: float
    verdict: str          # PASS | RISK | FAIL
    rule: str
    evidence: str
    source: str
    note: str = ""


def _verdict(value: float, limit: float, margin: float = 0.0) -> str:
    """PASS above limit+margin, RISK within `margin`, FAIL below limit."""
    if value >= limit + margin:
        return "PASS"
    if value >= limit:
        return "RISK"
    return "FAIL"


def _restricted(value: float, abs_floor: float, robust_target: float) -> str:
    """Verdict against two thresholds for features with a hard floor plus a
    robustness target.

    - value >= robust_target            -> PASS
    - abs_floor <= value < robust      -> RISK (prints, but fragile/thin)
    - value < abs_floor                -> FAIL (below one extrusion line)
    """
    if value >= robust_target:
        return "PASS"
    if value >= abs_floor:
        return "RISK"
    return "FAIL"


def check_register_cell(coupon_path: Path, spec: ProcessSpec = ProcessSpec()) -> dict:
    """Analytic printability for the DND-54 S5-R register unit cell.

    Same sourced rules and same evidence class as `check_coupon`, applied to the
    pawl / keeper / rack / wall features of the shared-drive register cell. It
    reads the SCAD constants so it tracks the CAD source of truth rather than
    duplicating values.
    """
    c = parse_scad_constants(coupon_path)
    rl = {r.key: r for r in rules(spec)}
    checks: list[Check] = []

    def add(feature, value, limit, verdict, rule_key, note=""):
        r = rl[rule_key]
        if verdict == "auto":
            verdict = _verdict(value, limit)
        checks.append(Check(feature, round(value, 3), round(limit, 3), verdict,
                            r.label, r.evidence, r.source, note))

    def add_wall(feature, value, note=""):
        r = rl["min_wall"]
        v = _restricted(value, spec.min_feature_mm, spec.min_wall_mm)
        checks.append(Check(feature, round(value, 3), round(spec.min_wall_mm, 3),
                            v, r.label, r.evidence, r.source,
                            note + " (hard floor = 1 line "
                            f"{spec.min_feature_mm:.2f} mm)"))

    # 1. pawl leaf thickness in the pitch direction.
    add_wall("pawl leaf thickness (PAWL_T)", c["PAWL_T"],
             "spring leaf across the pitch band; 1 line is the hard floor")

    # 2. keeper leaf thickness (DND-59: re-profiled to 2 lines).
    add_wall("keeper leaf thickness (KEEPER_T)", c["KEEPER_T"],
             "bistable over-centre leaf; DND-59 re-profile to 2 lines")

    # 2b. keeper hard shoulder (DND-59): must be a printable feature >= 1 line.
    if "KEEPER_SHOULDER_X" in c:
        add("keeper hard shoulder (KEEPER_SHOULDER_X)", c["KEEPER_SHOULDER_X"],
            spec.min_feature_mm, "auto", "min_feature",
            "the compression hold shoulder must print as a solid feature")

    # 3. housing wall.
    add_wall("housing wall (WALL)", c["WALL"], "structural cell wall")

    # 4. free lateral gap between the pawl/keeper stack and the neighbour cell.
    # DND-59: the keeper is re-profiled into the ROW (Y) direction, so the X-band
    # holds only the pawl and the Y-band holds pawl + keeper. Both axes checked.
    free_band = c["PITCH"] - 2.0 * c["ROTOR_RADIUS"]
    stack_x = c["PAWL_T"]
    stack_y = c["PAWL_W"] + c["KEEPER_T"]
    for axis, stack in (("X (pitch)", stack_x), ("Y (row)", stack_y)):
        v = lateral_clearance(free_band - stack, required_mm=0.20, spec=spec)
        checks.append(Check(
            feature=f"free lateral gap to neighbour cell, {axis} "
                    f"(PITCH - 2R - stack), worst case",
            value_mm=v.pessimistic_mm, limit_mm=0.20,
            verdict="PASS" if v.ok else "FAIL",
            rule="lateral running clearance", evidence=v.evidence,
            source=v.source,
            note=f"nominal {v.nominal_mm} mm minus 2x0.1 mm print error; this is "
                 "the no-neighbour-cross-talk geometric gate"))

    # 5. rotor bore clearance (printed journal fit).
    if "ROTOR_BORE_CLEAR" in c:
        v = lateral_clearance(c["ROTOR_BORE_CLEAR"], required_mm=0.20,
                              spec=spec)
        checks.append(Check(
            feature="rotor bore free play (ROTOR_BORE_CLEAR), worst case",
            value_mm=v.pessimistic_mm, limit_mm=0.20,
            verdict="PASS" if v.ok else "FAIL",
            rule="lateral running clearance", evidence=v.evidence,
            source=v.source,
            note=f"nominal {v.nominal_mm} mm minus 2x0.1 mm print error; the "
                 "printed rotor must spin free in its bore"))

    # 6. rack tooth height (a small printed tooth).
    add("rack tooth height (RACK_TOOTH_HEIGHT)", c["RACK_TOOTH_HEIGHT"],
        spec.min_feature_mm, "auto", "min_feature",
        "tooth narrower than one line cannot print")

    fails = [x for x in checks if x.verdict == "FAIL"]
    risks = [x for x in checks if x.verdict == "RISK"]
    overall = "FAIL" if fails else ("RISK" if risks else "PASS")

    return {
        "coupon": coupon_path.name,
        "evidence_class": "calculation",
        "process": {
            "printer": spec.printer, "material": spec.material,
            "nozzle_mm": spec.nozzle_mm, "layer_mm": spec.layer_mm,
            "perimeters": spec.perimeters,
        },
        "constants_read": {k: round(v, 3) for k, v in sorted(c.items())},
        "checks": [asdict(x) for x in checks],
        "verdict": overall,
        "residual_uncertainty": [
            "Not a slicer: real toolpath decisions (seam placement, thin-wall "
            "detection, bridging params) are not modelled.",
            "Not a printer: machine calibration, filament lot, moisture and "
            "temperature effects are not modelled.",
            "FDM dimensional accuracy is a generic assumption (+/-0.1 mm/face); "
            "the actual X1C value is not measured here.",
            "These checks retire geometry-vs-process risk only; they do not "
            "validate function, fit, or mechanism behaviour.",
        ],
    }


def check_bank_assembly(coupon_path: Path, spec: ProcessSpec = ProcessSpec()) -> dict:
    """Analytic printability for the DND-55 S5-R R=4 multi-row bank assembly.

    Same sourced rules and evidence class as `check_coupon`, applied to the
    ADDED parts of the bank: the drive bar / rack teeth, the reset-comber tine,
    the writer-carriage wall and nose, and the cross-row (Y) spacing. It reads
    the SCAD constants so it tracks the CAD source of truth rather than
    duplicating values.
    """
    c = parse_scad_constants(coupon_path)
    rl = {r.key: r for r in rules(spec)}
    checks: list[Check] = []

    def add(feature, value, limit, verdict, rule_key, note=""):
        r = rl[rule_key]
        if verdict == "auto":
            verdict = _verdict(value, limit)
        checks.append(Check(feature, round(value, 3), round(limit, 3), verdict,
                            r.label, r.evidence, r.source, note))

    def add_wall(feature, value, note=""):
        r = rl["min_wall"]
        v = _restricted(value, spec.min_feature_mm, spec.min_wall_mm)
        checks.append(Check(feature, round(value, 3), round(spec.min_wall_mm, 3),
                            v, r.label, r.evidence, r.source,
                            note + " (hard floor = 1 line "
                            f"{spec.min_feature_mm:.2f} mm)"))

    # 1. drive bar cross-section in the two printed in-plane directions.
    add_wall("drive bar width (BAR_W)", c["BAR_W"], "bar section across Y")
    add_wall("drive bar height (BAR_H)", c["BAR_H"], "bar section across Z")

    # 2. rack tooth height (a small printed tooth).
    add("rack tooth height (RACK_TOOTH_HEIGHT)", c["RACK_TOOTH_HEIGHT"],
        spec.min_feature_mm, "auto", "min_feature",
        "a tooth narrower than one line cannot print")

    # 3. rack tooth pitch must leave a printable gap between teeth.
    tooth_gap = c["RACK_TOOTH_PITCH"] - c["RACK_TOOTH_HEIGHT"]
    if tooth_gap > 0:
        add("rack tooth gap (RACK_TOOTH_PITCH - tooth)", tooth_gap,
            spec.min_feature_mm, "auto", "min_feature",
            "inter-tooth void narrower than one line fuses the rack")
    else:
        checks.append(Check("rack tooth gap (RACK_TOOTH_PITCH - tooth)",
                            round(tooth_gap, 3), round(spec.min_feature_mm, 3),
                            "FAIL", rl["min_feature"].label,
                            rl["min_feature"].evidence, rl["min_feature"].source,
                            "teeth overlap: no rack void"))

    # 4. reset-comber tine thickness.
    add_wall("reset comber tine thickness (COMBER_TINE_T)", c["COMBER_TINE_T"],
             "comber rake tine")

    # 5. writer-carriage wall thickness (body and nose).
    add_wall("writer carriage wall (CARRIAGE_WALL)", c["CARRIAGE_WALL"],
             "carriage body printed wall")

    # 6. cross-row (Y) spacing: adjacent R rows must clear after print error.
    row_free = c["ROW_PITCH"] - c["BAR_W"]
    v = lateral_clearance(row_free, required_mm=0.20, spec=spec)
    checks.append(Check(
        feature="cross-row free gap (ROW_PITCH - BAR_W), worst case",
        value_mm=v.pessimistic_mm, limit_mm=0.20,
        verdict="PASS" if v.ok else "FAIL",
        rule="lateral running clearance", evidence=v.evidence, source=v.source,
        note=f"nominal {v.nominal_mm} mm minus 2x0.1 mm print error; the "
             "R-row bank must keep every row clear of its neighbour"))

    fails = [x for x in checks if x.verdict == "FAIL"]
    risks = [x for x in checks if x.verdict == "RISK"]
    overall = "FAIL" if fails else ("RISK" if risks else "PASS")

    return {
        "coupon": coupon_path.name,
        "evidence_class": "calculation",
        "process": {
            "printer": spec.printer, "material": spec.material,
            "nozzle_mm": spec.nozzle_mm, "layer_mm": spec.layer_mm,
            "perimeters": spec.perimeters,
        },
        "constants_read": {k: round(v, 3) for k, v in sorted(c.items())},
        "checks": [asdict(x) for x in checks],
        "verdict": overall,
        "residual_uncertainty": [
            "Not a slicer: real toolpath decisions (seam placement, thin-wall "
            "detection, bridging params) are not modelled.",
            "Not a printer: machine calibration, filament lot, moisture and "
            "temperature effects are not modelled.",
            "FDM dimensional accuracy is a generic assumption (+/-0.1 mm/face); "
            "the actual X1C value is not measured here.",
            "These checks retire geometry-vs-process risk only; they do not "
            "validate function, fit, or mechanism behaviour.",
        ],
    }


def _dispatch_checker(path: Path, spec: ProcessSpec = ProcessSpec()) -> dict:
    """Route a SCAD source to its feature-specific printability checker."""
    name = path.name
    if "s5r_bank" in name:
        return check_bank_assembly(path, spec)
    if "s5r_register" in name:
        return check_register_cell(path, spec)
    return check_coupon(path, spec)


def check_coupon(coupon_path: Path, spec: ProcessSpec = ProcessSpec()) -> dict:
    c = parse_scad_constants(coupon_path)
    rl = {r.key: r for r in rules(spec)}
    checks: list[Check] = []

    def add(feature, value, limit, verdict, rule_key, note=""):
        r = rl[rule_key]
        if verdict == "auto":
            verdict = _verdict(value, limit)
        checks.append(Check(feature, round(value, 3), round(limit, 3), verdict,
                            r.label, r.evidence, r.source, note))

    def add_wall(feature, value, note=""):
        """Walls have a hard floor (one extrusion line) and a robustness target
        (2 lines). Below the floor is FAIL; between is RISK."""
        r = rl["min_wall"]
        v = _restricted(value, spec.min_feature_mm, spec.min_wall_mm)
        checks.append(Check(feature, round(value, 3), round(spec.min_wall_mm, 3),
                            v, r.label, r.evidence, r.source,
                            note + " (hard floor = 1 line "
                            f"{spec.min_feature_mm:.2f} mm)"))

    # 1. finger thickness (a wall printed across the row axis)
    add_wall("finger thickness (FINGER_T)", c["FINGER_T"],
             "structural rocker body; wants 3 perimeters")

    # 2. printed web between adjacent fingers in the 1.27 mm band
    web = c["BAND"] - c["FINGER_T"]
    add_wall("web between adjacent fingers (BAND - FINGER_T)", web,
             "must print as a solid web, no infill")

    # 3. selector notch diameter (internal void that must clear)
    add("selector notch (NOTCH_D)", c["NOTCH_D"], spec.min_feature_mm,
        "auto", "min_feature",
        "an internal slot narrower than one line closes up")

    # 4. printed pivot boss diameter (a printed-in-place journal, NOT an
    #    inserted pin). The `min_pin_dia` rule is for a bought inserted pin and
    #    does not apply: a printed boss is bounded by the minimum printable
    #    circular feature, with a robustness target at the page's min_wall. The
    #    functional fit (boss vs socket free play) is a tolerance stack-up owned
    #    by the analytic gate, not this screen.
    add_wall("pivot boss diameter (PIVOT_D, printed-in-place journal)",
             c["PIVOT_D"], "printed boss, not an inserted pin; needs a free socket bore")

    # 5. designed journal clearance (PIVOT_SOCKET_D - PIVOT_D) if declared, as a
    #    worst-case lateral running clearance; this decides whether the printed
    #    pivot can actually rotate.
    if "PIVOT_CLR" in c:
        free = 2.0 * c["PIVOT_CLR"]
        v = lateral_clearance(free, required_mm=0.20, spec=spec)
        checks.append(Check(
            feature="designed journal free play (2 x PIVOT_CLR)",
            value_mm=v.pessimistic_mm, limit_mm=0.20,
            verdict="PASS" if v.ok else "FAIL",
            rule="lateral running clearance", evidence=v.evidence,
            source=v.source,
            note="printed boss-in-socket must stay free, not fused"))
    elif "MIN_WEB" in c:
        # Legacy declared min-web constant: reported for traceability only, and
        # never overrides the computed web at check #2.
        add_wall("declared min web (MIN_WEB, traceability only)",
                 c["MIN_WEB"], "legacy design-intent constant")

    # 6. lateral pivot-to-neighbour clearance (worst case)
    if {"PITCH", "FINGER_T", "PIVOT_D"} <= c.keys():
        lat_nom = c["PITCH"] - c["FINGER_T"] - c["PIVOT_D"]
        v = lateral_clearance(lat_nom, required_mm=0.20, spec=spec)
        checks.append(Check(
            feature="lateral clearance to neighbour column "
                    "(PITCH - FINGER_T - PIVOT_D), worst case",
            value_mm=v.pessimistic_mm, limit_mm=0.20,
            verdict="PASS" if v.ok else "FAIL",
            rule="lateral running clearance", evidence=v.evidence,
            source=v.source,
            note=f"nominal {v.nominal_mm} mm minus 2x0.1 mm print error"))

    fails = [x for x in checks if x.verdict == "FAIL"]
    risks = [x for x in checks if x.verdict == "RISK"]
    overall = "FAIL" if fails else ("RISK" if risks else "PASS")

    return {
        "coupon": coupon_path.name,
        "evidence_class": "calculation",
        "process": {
            "printer": spec.printer, "material": spec.material,
            "nozzle_mm": spec.nozzle_mm, "layer_mm": spec.layer_mm,
            "perimeters": spec.perimeters,
        },
        "constants_read": {k: round(v, 3) for k, v in sorted(c.items())},
        "checks": [asdict(x) for x in checks],
        "verdict": overall,
        "residual_uncertainty": [
            "Not a slicer: real toolpath decisions (seam placement, thin-wall "
            "detection, bridging params) are not modelled.",
            "Not a printer: machine calibration, filament lot, moisture and "
            "temperature effects are not modelled.",
            "FDM dimensional accuracy is a generic assumption (+/-0.1 mm/face); "
            "the actual X1C value is not measured here.",
            "These checks retire geometry-vs-process risk only; they do not "
            "validate function, fit, or mechanism behaviour.",
        ],
    }


def print_table(res: dict) -> None:
    print(f"Analytic printability — {res['coupon']}")
    p = res["process"]
    print(f"  process: {p['printer']}, {p['material']}, "
          f"{p['nozzle_mm']} mm nozzle, {p['layer_mm']} mm layers\n")
    print(f"  {'FEATURE':<52} {'VALUE':>8} {'LIMIT':>8}  VERDICT")
    for x in res["checks"]:
        print(f"  {x['feature']:<52} {x['value_mm']:>8.3f} "
              f"{x['limit_mm']:>8.3f}  {x['verdict']}")
    print()
    print(f"  VERDICT: {res['verdict']}")
    print(f"  evidence class: {res['evidence_class']} "
          f"(not a print, not a measurement)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("coupon", nargs="?", default=str(DEFAULT_COUPON),
                    help="OpenSCAD coupon source to analyse")
    ap.add_argument("--json", metavar="PATH", help="write JSON record here")
    ap.add_argument("--fail-on-design-fail", action="store_true",
                    help="exit 1 when the verdict is FAIL (design gate); "
                    "off by default because a FAIL is a design finding, not "
                    "a tool error")
    args = ap.parse_args()

    path = Path(args.coupon)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2

    res = (_dispatch_checker(path))
    print_table(res)
    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=2) + "\n")
        print(f"\nwrote {args.json}", file=sys.stderr)
    if args.fail_on_design_fail and res["verdict"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
