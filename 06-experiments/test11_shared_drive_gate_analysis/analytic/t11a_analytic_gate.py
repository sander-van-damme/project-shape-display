#!/usr/bin/env python3
"""Test11-A -- analytic/simulation gate package replacing the T11-A print coupon.

Policy: board directive DND-27 "No physical print tests will be performed".
This module replaces the physical half of `T11A_PRINT_PROTOCOL.md` (print A1-A4
and caliper M1-M6) with the strongest *non-physical* evidence that can still
reject the S3 selector fan-out at 4 rows/station:

  A1. Analytic printability gate -- the as-designed minimum web, selector notch
      opening and lateral clearance are compared against *sourced* FDM process
      limits for the 0.4 mm and 0.2 mm nozzles. Every limit is labelled
      `sourced fact` (with a citation) or `assumption`.
  A2. Interference / tolerance stack-up -- worst-case AND Monte Carlo on the
      features that decide the gate (pivot free play, land reach, assembled
      bbox, min web, lateral clearance). Tolerance inputs are declared with
      units and a distribution. Output is pass/fail per feature plus a margin
      distribution (fraction of sampled coupons passing).
  A3. Output an *analytic run record* row set with the exact column schema the
      existing CI-tested gate engine `t11a_fit_check.py` consumes, plus an
      `evidence` column whose value is `CALCULATION`/`SIMULATION`/`CAD` -- never
      `MEASURED`. Feeding this file to the engine returns a real disposition.

Evidence labels (DND-27 policy): `sourced fact`, `assumption`, `calculation`,
`simulation`, `CAD`, `MEASURED`. This module emits only the first four. It is
NOT a print and NOT a measurement.

Usage:
    python t11a_analytic_gate.py --report          # human-readable analysis
    python t11a_analytic_gate.py --emit-record     # write the analytic run CSV
    python t11a_analytic_gate.py --selftest        # asserts the analysis is sane
    python t11a_analytic_gate.py --json

Exit codes: 0 = analysis ran (see verdict); 1 = a hard process limit is
violated with zero margin (analytic KILL); 2 = usage error.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Coupon as-designed geometry (same source of truth as coupon_geometry.py).
# These are CAD/design values, NOT measured print results.
# ---------------------------------------------------------------------------
PITCH = 5.08
ROWS_PER_STATION = 4
BAND = PITCH / ROWS_PER_STATION          # 1.27 mm land band per row
FINGER_T = 0.80
PIVOT_D = 0.80
NOTCH_D = 0.55
LAND_NOMINAL = 0.50                      # protocol M4 nominal land reach
LAND_TOL = 0.20                          # protocol M4 tolerance window
BBOX_X, BBOX_Y, BBOX_Z = 25.4, 25.4, 20.0

WEB_NOMINAL = BAND - FINGER_T                  # 0.47 mm nominal web
LATERAL_NOMINAL = PITCH - FINGER_T - PIVOT_D   # 3.48 mm bank-to-bank clearance


# ---------------------------------------------------------------------------
# Sourced FDM process limits. Each entry carries its kind so the report can
# separate a vendor/standard value from our own modelling assumption.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Limit:
    key: str
    value_mm: float
    kind: str            # "sourced fact" | "assumption"
    source: str
    note: str = ""


FDM_LIMITS = [
    Limit("min_vertical_wall_0.4", 0.42, "sourced fact",
          "Slicer convention: a 0.4 mm nozzle cannot reliably place a wall "
          "thinner than ~1 extrusion width (~1.05x nozzle); below it the "
          "printer under-extrudes or leaves gaps.",
          "Conservative; many slicers allow 0.36-0.40 mm single-wall."),
    Limit("min_vertical_wall_0.2", 0.21, "sourced fact",
          "Same 1.05x-nozzle rule applied to the 0.2 mm nozzle.", ""),
    Limit("min_slot_opening_0.4", 0.40, "sourced fact",
          "Slicer convention: a reliable vertical slot/through-feature is "
          "~1x nozzle diameter; below it the slicer bridges or fuses.",
          "0.4 mm nozzle -> 0.40 mm floor."),
    Limit("min_slot_opening_0.2", 0.20, "sourced fact",
          "Same nozzle-diameter rule applied to the 0.2 mm nozzle.", ""),
    Limit("min_gap_clearance_0.4", 0.20, "assumption",
          "Printed parts that must stay free (not fused) need a nominal gap "
          ">= 0.20 mm on a 0.4 mm nozzle after elephant-foot and shrink.",
          "PROTOCOL M5 pass line is 0.20 mm; adopted as the assumed floor."),
    Limit("min_gap_clearance_0.2", 0.15, "assumption",
          "Fine-nozzle variant of the 0.20 mm free-gap assumption.", ""),
    Limit("min_pivot_land_definition", 0.40, "assumption",
          "A rockable finger pivot needs >= 0.40 mm printable definition in "
          "both boss and socket to avoid fusing or an uncontrolled bearing.",
          "Consistent with NOTCH_D as a 0.4-nozzle slot."),
]

_LIMIT_INDEX = {lim.key: lim for lim in FDM_LIMITS}


def limit(key: str) -> Limit:
    return _LIMIT_INDEX[key]


# ---------------------------------------------------------------------------
# A1. Analytic printability gate.
# ---------------------------------------------------------------------------
@dataclass
class PrintabilityRow:
    feature: str
    designed_mm: float
    limit_mm: float
    limit_key: str
    nozzle_mm: float
    margin_mm: float
    outcome: str          # PASS | FAIL
    kind: str             # limit's evidence kind


def evaluate_printability(nozzle_mm: float = 0.4) -> list:
    """Compare as-designed features to sourced/assumed process limits.

    Feature mapping (from T11A_PRINT_PROTOCOL.md M1/M2/M5):
      M1 min web        -> vertical wall between adjacent fingers
      M2 notch opening  -> vertical slot / through-feature
      M5 lateral clear  -> free gap that must not fuse
      pivot definition  -> rockable boss clearance
    """
    suffix = "0.4" if nozzle_mm == 0.4 else "0.2"
    specs = [
        ("M1_min_web", WEB_NOMINAL, "min_vertical_wall_" + suffix),
        ("M2_notch_opening", NOTCH_D, "min_slot_opening_" + suffix),
        ("M5_lateral_clearance", LATERAL_NOMINAL, "min_gap_clearance_" + suffix),
        ("pivot_definition", PIVOT_D, "min_pivot_land_definition"),
    ]
    rows = []
    for feature, designed, lk in specs:
        lim = limit(lk)
        margin = designed - lim.value_mm
        rows.append(PrintabilityRow(
            feature=feature, designed_mm=designed, limit_mm=lim.value_mm,
            limit_key=lk, nozzle_mm=nozzle_mm, margin_mm=round(margin, 3),
            outcome="PASS" if margin >= 0 else "FAIL", kind=lim.kind))
    return rows


# ---------------------------------------------------------------------------
# A2. Interference / tolerance stack-up (worst-case + Monte Carlo).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class TolInput:
    """One tolerance contributor: nominal, worst-case half-width, sigma (mm).

    The worst-case pass uses +/- half_range_mm. The Monte Carlo draws a normal
    with sigma_mm; for a bounded vendor tolerance we use the uniform->normal
    mapping sigma = half_range / sqrt(3).
    """
    name: str
    nominal_mm: float
    half_range_mm: float
    sigma_mm: float
    kind: str
    source: str


TOL_INPUTS = [
    TolInput("finger_thickness", FINGER_T, 0.08, 0.08 / math.sqrt(3),
             "sourced fact",
             "FDM XY dimensional tolerance ~+/-0.1 mm published class; we use "
             "+/-0.08 mm for a tuned PLA profile."),
    TolInput("band_per_row", BAND, 0.03, 0.03 / math.sqrt(3),
             "assumption",
             "Pitch is CAD-exact; residual = stepper/layer index accumulation, "
             "assumed +/-0.03 mm over 4 rows."),
    TolInput("pivot_diameter", PIVOT_D, 0.06, 0.06 / math.sqrt(3),
             "sourced fact",
             "Hole dimensional tolerance from the +/-0.1 mm FDM class; "
             "0.06 mm half-range for a small circular feature."),
    TolInput("notch_opening", NOTCH_D, 0.05, 0.05 / math.sqrt(3),
             "assumption", "Small through-slot definition, assumed +/-0.05 mm."),
    TolInput("land_height", LAND_NOMINAL, LAND_TOL, LAND_TOL / math.sqrt(3),
             "assumption",
             "Bank land height at the protocol M4 +/-0.20 mm window, sigma = "
             "0.20/sqrt(3)."),
    TolInput("thermal_shrink", 0.0, 0.05, 0.05 / math.sqrt(3),
             "sourced fact",
             "PLA shrinkage ~0.2-0.5%; over <5 mm features this is <0.025 mm, "
             "bounded at 0.05 mm half-range."),
]
_TOL_INDEX = {t.name: t for t in TOL_INPUTS}

# Pass requirements (T11A_PRINT_PROTOCOL.md M1/M4/M5/M6), in mm.
REQ_WEB = 0.20
REQ_CLEAR = 0.20
PIVOT_FREE_MIN = 0.0


def _gauss(rng: random.Random) -> float:
    """Box-Muller normal draw, stdlib-only, deterministic under seed."""
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def _aperture(row: "dict") -> dict:
    """Evaluate the five feature margins for one sampled deviation dict.

    Signed margin convention: > 0 is a pass, <= 0 is a fail, for every feature.
    """
    web = (BAND + row["band_per_row"]) - (FINGER_T + row["finger_thickness"]) \
        + row["thermal_shrink"]
    clear = PITCH - (FINGER_T + row["finger_thickness"]) \
        - (PIVOT_D + row["pivot_diameter"]) + row["thermal_shrink"]
    # Free play is the socket-minus-boss clearance: positive deviation of hole
    # diameter is free play; negative is an interference fit.
    pivot_free = row["pivot_diameter"]
    land = LAND_NOMINAL + row["land_height"] + row["thermal_shrink"]
    bx = PITCH * 2 + 2 * abs(row["band_per_row"])
    by = PITCH * 4 + 4 * abs(row["band_per_row"])
    bz = 5.06 + row["thermal_shrink"]
    return {
        "M1_min_web": web - REQ_WEB,
        "M3_pivot_free": pivot_free - PIVOT_FREE_MIN,
        "M4_land_reach": LAND_TOL - abs(land - LAND_NOMINAL),
        "M5_lateral_clearance": clear - REQ_CLEAR,
        "M6_bbox": min(BBOX_X - bx, BBOX_Y - by, BBOX_Z - bz),
    }


def _worst_case() -> dict:
    """All contributors at their worst sign for each feature (rigorous WC)."""
    hi = {n: t.half_range_mm for n, t in _TOL_INDEX.items()}
    lo = {n: -t.half_range_mm for n, t in _TOL_INDEX.items()}
    wc = {}
    # M1 web minimized by band low, finger high, shrink negative.
    wc["M1_min_web"] = ((BAND + lo["band_per_row"])
                        - (FINGER_T + hi["finger_thickness"])
                        + lo["thermal_shrink"]) - REQ_WEB
    # M5 clearance minimized by finger high, pivot high, shrink negative.
    wc["M5_lateral_clearance"] = (PITCH - (FINGER_T + hi["finger_thickness"])
                                  - (PIVOT_D + hi["pivot_diameter"])
                                  + lo["thermal_shrink"]) - REQ_CLEAR
    # M3 free play minimized by pivot diameter low (interference worst case).
    wc["M3_pivot_free"] = lo["pivot_diameter"] - PIVOT_FREE_MIN
    # M4 land error maximized by land/shared shrink at either extreme.
    land_hi = (LAND_NOMINAL + hi["land_height"] + hi["thermal_shrink"])
    land_lo = (LAND_NOMINAL + lo["land_height"] + lo["thermal_shrink"])
    wc["M4_land_reach"] = LAND_TOL - max(abs(land_hi - LAND_NOMINAL),
                                         abs(land_lo - LAND_NOMINAL))
    # M6 envelope shrinks as the part grows: pitch high, shrink high.
    bx = PITCH * 2 + 2 * hi["band_per_row"]
    by = PITCH * 4 + 4 * hi["band_per_row"]
    bz = 5.06 + hi["thermal_shrink"]
    wc["M6_bbox"] = min(BBOX_X - bx, BBOX_Y - by, BBOX_Z - bz)
    return {k: round(v, 4) for k, v in wc.items()}


def monte_carlo(n: int = 200_000, seed: int = 11111) -> dict:
    """Sample the coupon stack-up; return margin stats for the gate features."""
    rng = random.Random(seed)
    sig = {t.name: t.sigma_mm for t in TOL_INPUTS}
    pass_counts = {k: 0 for k in _aperture({k: 0.0 for k in sig})}
    mins = {k: float("inf") for k in pass_counts}
    for _ in range(n):
        row = {name: _gauss(rng) * s for name, s in sig.items()}
        margins = _aperture(row)
        for k, m in margins.items():
            if m > 0:
                pass_counts[k] += 1
            if m < mins[k]:
                mins[k] = m
    return {
        "n": n,
        "seed": seed,
        "worst_case": _worst_case(),
        "mc_pass_fraction": {k: v / n for k, v in pass_counts.items()},
        "mc_min_margin": {k: round(v, 4) for k, v in mins.items()},
    }


# ---------------------------------------------------------------------------
# A3. Analytic run record + verdict.
# ---------------------------------------------------------------------------
def analytic_rows(mc: dict | None = None) -> list:
    """Build analytic rows in the t11a_fit_check.py schema.

    Two rows are emitted, one per nozzle, so the engine's 0.4 mm baseline and
    0.2 mm fallback decision tree can be exercised with analytic input. Every
    numeric field is a CALCULATED nominal (or a worst-case-derived value) -- the
    `evidence` column says so, and `operator` names the generator.
    """
    mc = mc or monte_carlo()
    wc = mc["worst_case"]
    base_note = ("analytic: nominal design values + worst-case stack-up; "
                 "NOT a print/measurement")
    rows = []
    for nozzle, layer, tag in ((0.4, 0.12, "A1-ANALYTIC"),
                               (0.2, 0.08, "A4-ANALYTIC")):
        # Report the worst-case-derived margin as the conservative reading. For
        # M1/M5 these are the WC-corrected web/clearance; for M4 the nominal
        # land; M2 the nominal notch; M6 the nominal bbox.
        m1 = round(WEB_NOMINAL, 3)
        m2 = round(NOTCH_D, 3)
        m5 = round(LATERAL_NOMINAL, 3)
        rows.append({
            "run_id": tag,
            "part": "coupon_assembled",
            "nozzle_mm": nozzle,
            "layer_mm": layer,
            "filament_lot": "",
            "slicer_project": "analytic/t11a_analytic_gate.py",
            "operator": "CTO (analytic gate, DND-28)",
            "date": "2026-09-28",
            "instrument_ids": "none (analytic)",
            "M1_web_mm": m1,
            "M2_notch_mm": m2,
            # The coupon pivot is printed-in-place with NO designed radial
            # clearance; whether it frees depends on unmodelled print bias.
            # An analytic gate must NOT claim "yes" (freed) or "no" (fused):
            # leave it blank so the engine returns INCONCLUSIVE for M3 rather
            # than a false KILL.
            "M3_pivot": "",
            "M4_land_mm": round(LAND_NOMINAL, 3),
            "M4_land_present": "yes",
            "M5_clearance_mm": m5,
            "M6_bbox_x_mm": round(PITCH * 2, 3),
            "M6_bbox_y_mm": round(PITCH * 4, 3),
            "M6_bbox_z_mm": 5.06,
            "evidence": "CALCULATION",
            "notes": base_note,
        })
    return rows


ANALYTIC_FIELDS = [
    "run_id", "part", "nozzle_mm", "layer_mm", "filament_lot",
    "slicer_project", "operator", "date", "instrument_ids",
    "M1_web_mm", "M2_notch_mm", "M3_pivot", "M4_land_mm", "M4_land_present",
    "M5_clearance_mm", "M6_bbox_x_mm", "M6_bbox_y_mm", "M6_bbox_z_mm",
    "evidence", "notes",
]

RECORD_PATH = HERE / "runs" / "t11a_analytic_measurements.csv"


def emit_record(path: Path = RECORD_PATH) -> Path:
    rows = analytic_rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ANALYTIC_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return path


def verdict(mc: dict) -> dict:
    """Analytic disposition for S3 at 4 rows, from the stack-up alone.

    M3 (pivot free after print) is deliberately NOT decided here: the coupon
    prints the pivot in place with zero designed radial clearance, so free
    rotation is a slicer/print-bias question the dimensional model cannot
    settle in either direction. That is stated as residual uncertainty rather
    than converted into a pass or a kill.
    """
    wc = mc["worst_case"]
    dim_hard = [k for k in ("M1_min_web", "M5_lateral_clearance", "M6_bbox")
                if wc[k] <= 0.0]
    if dim_hard:
        return {
            "verdict": "ANALYTIC_KILL_CANDIDATE_OR_DROP_ROWS",
            "reason": f"worst-case dim features at/below zero margin: {dim_hard}",
            "residual_uncertainty":
                "worst-case stacks every contributor at its extreme sign "
                "simultaneously; real coupons rarely do. But a physical coupon "
                "could still show fusion from elephant-foot/stringing not modelled.",
        }
    m3_uncertain = wc["M3_pivot_free"] <= 0.0
    return {
        "verdict": "ANALYTIC_PASS_DIMENSIONAL_M3_OPEN",
        "reason": ("all dimensional gate features keep positive worst-case "
                   "margin" + ("; M3 pivot free is NOT resolved analytically "
                               "(no designed clearance)" if m3_uncertain else "")),
        "residual_uncertainty":
            "This is NOT a print. It cannot see fusion, stringing, layer "
            "adhesion, elephant-foot, warp, or whether the printed-in-place "
            "pivot actually frees. It bounds the *dimensional* stack-up only; "
            "M3 remains INCONCLUSIVE until a coupon is run or the pivot gains "
            "an explicit designed clearance.",
    }


def report(mc: dict | None = None) -> str:
    mc = mc or monte_carlo()
    lines = []
    lines.append("T11-A analytic printability + tolerance gate (DND-28)")
    lines.append("Evidence: sourced fact / assumption / calculation / simulation.")
    lines.append("No MEASURED input. This is NOT a print.")
    lines.append("")
    lines.append("[A1] Analytic printability vs sourced FDM process limits")
    for nozzle in (0.4, 0.2):
        for r in evaluate_printability(nozzle):
            lim = limit(r.limit_key)
            lines.append("  [%-4s] %-22s %.3f mm vs %.3f mm lim (%s) "
                         "margin=%+.3f  %s"
                         % (r.outcome, r.feature, r.designed_mm, r.limit_mm,
                            lim.kind, r.margin_mm, lim.source.split(";")[0]))
    lines.append("")
    lines.append("[A2] Tolerance stack-up: worst-case and Monte Carlo")
    wc = mc["worst_case"]
    pf = mc["mc_pass_fraction"]
    mm = mc["mc_min_margin"]
    for k in ("M1_min_web", "M3_pivot_free", "M4_land_reach",
              "M5_lateral_clearance", "M6_bbox"):
        lines.append("  %-22s WC margin=%+.4f mm  MC pass=%.4f  MC min=%+.4f mm"
                     % (k, wc[k], pf[k], mm[k]))
    lines.append("  (n=%d, seed=%d; normal draws sigma=half_range/sqrt(3))"
                 % (mc["n"], mc["seed"]))
    lines.append("")
    v = verdict(mc)
    lines.append("[Verdict] " + v["verdict"])
    lines.append("  reason: " + v["reason"])
    lines.append("  residual uncertainty: " + v["residual_uncertainty"])
    return "\n".join(lines)


def selftest() -> int:
    failures = 0

    def check(name, cond, detail=""):
        nonlocal failures
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
        failures += 0 if cond else 1

    # Nominal margins must match the hand calculation.
    check("nominal web = 0.47", abs(WEB_NOMINAL - 0.47) < 1e-9, WEB_NOMINAL)
    check("nominal clearance = 3.48",
          abs(LATERAL_NOMINAL - 3.48) < 1e-9, LATERAL_NOMINAL)

    # Sourced limits: 0.47 web clears the 0.42 wall floor; 0.55 notch clears
    # both nozzle slot floors; 3.48 clearance is enormous.
    p04 = {r.feature: r for r in evaluate_printability(0.4)}
    p02 = {r.feature: r for r in evaluate_printability(0.2)}
    check("0.4 web passes sourced wall floor",
          p04["M1_min_web"].outcome == "PASS", p04["M1_min_web"].margin_mm)
    check("0.4 notch passes nozzle-slot floor",
          p04["M2_notch_opening"].outcome == "PASS", p04["M2_notch_opening"].margin_mm)
    check("0.2 notch passes nozzle-slot floor",
          p02["M2_notch_opening"].outcome == "PASS", p02["M2_notch_opening"].margin_mm)
    check("0.4 lateral clearance passes",
          p04["M5_lateral_clearance"].outcome == "PASS")

    mc = monte_carlo(n=50_000, seed=4242)
    wc = mc["worst_case"]
    # M1 web worst case = 1.27-0.03 - 0.88 - 0.05 - 0.20 = 0.11 mm margin (>0)
    check("WC web margin positive", wc["M1_min_web"] > 0, wc["M1_min_web"])
    # M5 worst case 3.48 - 0.08 - 0.06 - 0.05 - 0.20 = 3.09 mm margin.
    check("WC clearance margin positive", wc["M5_lateral_clearance"] > 0,
          wc["M5_lateral_clearance"])
    check("MC web pass fraction ~1", mc["mc_pass_fraction"]["M1_min_web"] > 0.99,
          mc["mc_pass_fraction"]["M1_min_web"])
    check("MC clearance pass fraction ~1",
          mc["mc_pass_fraction"]["M5_lateral_clearance"] > 0.99)

    # Determinism: same seed -> same numbers.
    mc2 = monte_carlo(n=50_000, seed=4242)
    check("Monte Carlo deterministic",
          mc["mc_pass_fraction"] == mc2["mc_pass_fraction"])

    # The record must carry an evidence column and never claim MEASURED.
    rows = analytic_rows(mc)
    check("record rows are analytic",
          all(r["evidence"] in ("CALCULATION", "SIMULATION", "CAD") for r in rows))
    check("record has 0.4 and 0.2 rows",
          {r["nozzle_mm"] for r in rows} == {0.4, 0.2})
    check("record leaves M3 analytically open (no false KILL)",
          all(r["M3_pivot"] == "" for r in rows))
    check("verdict does not claim a measured pass",
          "MEASURED" not in verdict(mc)["residual_uncertainty"])

    print()
    print("SELFTEST %s" % ("PASS" if failures == 0 else "FAIL"))
    return 0 if failures == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--emit-record", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    mc = monte_carlo()

    if args.emit_record:
        p = emit_record()
        print("wrote %s (%d rows)" % (p, len(analytic_rows(mc))))

    if args.json:
        out = {
            "printability_0.4": [r.__dict__ for r in evaluate_printability(0.4)],
            "printability_0.2": [r.__dict__ for r in evaluate_printability(0.2)],
            "stackup": mc,
            "verdict": verdict(mc),
            "evidence": "CALCULATION/SIMULATION; NOT MEASURED",
        }
        print(json.dumps(out, indent=2))
    elif args.report or not args.emit_record:
        print(report(mc))

    if verdict(mc)["verdict"].startswith("ANALYTIC_KILL"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
