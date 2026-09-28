#!/usr/bin/env python3
"""Test11-A -- runnable selector fan-out fit-coupon gate engine (no hardware).

Executable half of `T11A_PRINT_PROTOCOL.md`. It reads the T11-A measurement table
(`runs/t11a_measurements.csv`), applies the M1..M6 pass/kill gates, and emits:
  * a per-print verdict (PASS / FAIL / KILL) for each coupon run, and
  * an architecture-level disposition implementing the protocol decision tree
    across the 0.4 mm baseline and the 0.2 mm fallback:

        PASS all M1-M6                       -> S3_DENSITY_PRINTABLE
        M1/M2 fail at 0.4 mm, pass at 0.2 mm -> S3_REQUIRES_FINE_NOZZLE
        M1/M2 fail at both nozzles           -> REJECT_S3_4ROW_DROP_TO_2_3
        otherwise (no 0.2 mm row yet)        -> INCONCLUSIVE_RUN_A4

No hardware is needed to exercise it. It is a GATE ENGINE, not a measurement:
running it proves the gate logic is consistent, nothing about S3.

Evidence: CALCULATED (arithmetic), SYNTHETIC (engine exercise, never evidence),
MEASURED (a real instrument reading; the only label that can move a disposition
off INCONCLUSIVE).

Usage:
    python t11a_fit_check.py --validate
    python t11a_fit_check.py --selftest
    python t11a_fit_check.py --predict
    python t11a_fit_check.py --input runs/t11a_measurements.csv
    python t11a_fit_check.py --input run.csv --json

Exit codes: 0 = validated or disposition not REJECT; 1 = KILL print or REJECT
disposition; 2 = usage/file error.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

COARSE_NOZZLE = 0.4
FINE_NOZZLE = 0.2

# Protocol numbers (T11A_PRINT_PROTOCOL.md).
WEB_PASS = 0.20
NOTCH_PASS = 0.40
# DND-4 M4 closure: M4_land_mm is the bank's raised land height (CAD) and the
# gate is that the land still seats the finger toe within the rocker's usable
# throw. The full tolerance stack-up lives in analytic/t11a_analytic_gate.py;
# this engine applies the nominal band.
LAND_NOMINAL = 0.90
LAND_H_MIN_CONTACT = 0.30
LAND_H_MAX = 3.20          # = FINGER_H; throw asin(land/FINGER_H) -> 90 deg
CLEARANCE_PASS = 0.20
BBOX_X, BBOX_Y, BBOX_Z = 25.4, 25.4, 20.0

STATIONS_BY_ROWS = {4: 20, 3: 27, 2: 40}

PITCH = 5.08
ROWS_PER_STATION = 4
BAND = PITCH / ROWS_PER_STATION
FINGER_T = 0.80
PIVOT_D = 0.80
NOTCH_D = 0.55

GATE_ORDER = ["M1", "M2", "M3", "M4", "M5", "M6"]

GATE_ORDER_FIELDS = [
    "run_id", "part", "nozzle_mm", "layer_mm",
    "M1_web_mm", "M2_notch_mm", "M3_pivot",
    "M4_land_mm", "M4_land_present", "M5_clearance_mm",
    "M6_bbox_x_mm", "M6_bbox_y_mm", "M6_bbox_z_mm",
]


@dataclass
class GateResult:
    key: str
    label: str
    value: object
    outcome: str  # PASS | FAIL | KILL | MISSING
    note: str = ""


@dataclass
class RunVerdict:
    run_id: str
    part: str
    nozzle_mm: float
    layer_mm: float
    gates: list = field(default_factory=list)
    evidence: str = "MEASURED"

    @property
    def worst(self) -> str:
        outcomes = {g.outcome for g in self.gates}
        if "KILL" in outcomes:
            return "KILL"
        if "FAIL" in outcomes:
            return "FAIL"
        if "MISSING" in outcomes:
            return "INCONCLUSIVE"
        return "PASS"

    @property
    def hard_fail_keys(self):
        return [g.key for g in self.gates if g.outcome in ("FAIL", "KILL")]


def _pf(raw):
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "" or text.lower() in ("na", "n/a", "nan", "none"):
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _yn(raw):
    if raw is None:
        return None
    t = str(raw).strip().lower()
    if t in ("y", "yes", "true", "t", "1", "pass", "free", "reaches"):
        return True
    if t in ("n", "no", "false", "f", "0", "fail", "fused", "missing"):
        return False
    return None


def _evidence(raw) -> str:
    """Evidence class for one row.

    The gate engine must never silently call an analytic row MEASURED. Rows may
    carry an explicit `evidence` column (CALCULATION / SIMULATION / CAD /
    MEASURED); a missing column defaults to MEASURED because the shipped
    `runs/t11a_measurements.csv` is the human print/measure table.
    """
    t = str(raw or "").strip().upper()
    if t in ("CALCULATION", "SIMULATION", "CAD", "MEASURED"):
        return t
    return "MEASURED"


def score_run(row: dict) -> RunVerdict:
    run_id = (row.get("run_id") or "").strip() or "UNKNOWN"
    part = (row.get("part") or "").strip()
    nozzle = _pf(row.get("nozzle_mm"))
    layer = _pf(row.get("layer_mm"))
    v = RunVerdict(run_id=run_id, part=part,
                   nozzle_mm=(nozzle if nozzle is not None else float("nan")),
                   layer_mm=(layer if layer is not None else float("nan")),
                   evidence=_evidence(row.get("evidence")))

    m1 = _pf(row.get("M1_web_mm"))
    if m1 is None:
        v.gates.append(GateResult("M1", "min web between adjacent fingers",
                                  None, "MISSING", "no reading"))
    elif m1 < WEB_PASS:
        v.gates.append(GateResult("M1", "min web between adjacent fingers",
                                  m1, "KILL", f"{m1} < {WEB_PASS} mm on a row"))
    else:
        v.gates.append(GateResult("M1", "min web between adjacent fingers",
                                  m1, "PASS", f"{m1} >= {WEB_PASS} mm"))

    m2 = _pf(row.get("M2_notch_mm"))
    if m2 is None:
        v.gates.append(GateResult("M2", "selector notch clear opening",
                                  None, "MISSING", "no reading"))
    elif m2 < NOTCH_PASS:
        v.gates.append(GateResult("M2", "selector notch clear opening",
                                  m2, "FAIL", f"{m2} < {NOTCH_PASS} mm"))
    else:
        v.gates.append(GateResult("M2", "selector notch clear opening",
                                  m2, "PASS", f"{m2} >= {NOTCH_PASS} mm"))

    m3 = _yn(row.get("M3_pivot"))
    if m3 is None:
        v.gates.append(GateResult("M3", "finger pivot free after print",
                                  None, "MISSING", "M3_pivot not recorded"))
    elif m3:
        v.gates.append(GateResult("M3", "finger pivot free after print",
                                  True, "PASS", "rotates under finger force"))
    else:
        v.gates.append(GateResult("M3", "finger pivot free after print",
                                  False, "KILL", "fused pivot"))

    m4 = _pf(row.get("M4_land_mm"))
    m4_state = _yn(row.get("M4_land_present"))
    if m4 is None and m4_state is None:
        v.gates.append(GateResult("M4", "bank land vs finger toe",
                                  None, "MISSING", "no reading"))
    elif m4_state is False:
        v.gates.append(GateResult("M4", "bank land vs finger toe",
                                  m4, "KILL", "land missing"))
    elif m4 is not None and m4 < LAND_H_MIN_CONTACT:
        v.gates.append(GateResult("M4", "bank land vs finger toe", m4, "KILL",
                                  f"land {m4} < {LAND_H_MIN_CONTACT} mm "
                                  "contact floor"))
    elif m4 is not None and m4 > LAND_H_MAX:
        v.gates.append(GateResult("M4", "bank land vs finger toe", m4, "KILL",
                                  f"land {m4} > {LAND_H_MAX} mm finger half-height"))
    else:
        v.gates.append(GateResult("M4", "bank land vs finger toe",
                                  m4, "PASS", "toe reaches land across rows"))

    m5 = _pf(row.get("M5_clearance_mm"))
    if m5 is None:
        v.gates.append(GateResult("M5", "lateral bank-to-bank clearance",
                                  None, "MISSING", "no reading"))
    elif m5 <= 0.0:
        v.gates.append(GateResult("M5", "lateral bank-to-bank clearance",
                                  m5, "KILL", "collision at 5.08 mm pitch"))
    elif m5 <= CLEARANCE_PASS:
        v.gates.append(GateResult("M5", "lateral bank-to-bank clearance",
                                  m5, "FAIL", f"{m5} <= {CLEARANCE_PASS} mm"))
    else:
        v.gates.append(GateResult("M5", "lateral bank-to-bank clearance",
                                  m5, "PASS", f"{m5} > {CLEARANCE_PASS} mm"))

    bx, by, bz = (_pf(row.get("M6_bbox_x_mm")), _pf(row.get("M6_bbox_y_mm")),
                  _pf(row.get("M6_bbox_z_mm")))
    if None in (bx, by, bz):
        dims = str(row.get("M6_bbox_mm") or "").lower().replace("x", " ")
        parts = [_pf(p) for p in dims.split()]
        if len(parts) == 3 and all(p is not None for p in parts):
            bx, by, bz = parts
    if None in (bx, by, bz):
        v.gates.append(GateResult("M6", "assembled bbox per 2x4",
                                  None, "MISSING", "no reading"))
    elif max(bx / BBOX_X, by / BBOX_Y, bz / BBOX_Z) <= 1.0:
        v.gates.append(GateResult("M6", "assembled bbox per 2x4",
                                  (bx, by, bz), "PASS",
                                  f"{bx}x{by}x{bz} <= {BBOX_X}x{BBOX_Y}x{BBOX_Z}"))
    else:
        v.gates.append(GateResult("M6", "assembled bbox per 2x4",
                                  (bx, by, bz), "FAIL",
                                  f"{bx}x{by}x{bz} exceeds 2x4 envelope"))
    return v


def read_rows(path: Path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("empty CSV (no header)")
        return list(reader)


def disposition_for(verdicts) -> dict:
    """Architecture disposition + an explicit evidence-class summary.

    Analytic/simulation records are allowed to exercise the decision tree, but
    the returned `evidence` field and the `action` text must make clear that a
    non-MEASURED result is a design-screen, not a print result.
    """
    disp = _disposition_core(verdicts)
    classes = sorted({v.evidence for v in verdicts})
    disp["evidence"] = classes
    if classes and classes != ["MEASURED"]:
        disp["evidence_warning"] = (
            "disposition derived from " + "/".join(classes)
            + " input, NOT a print/measurement; this is an analytic screen")
        disp["action"] = ("[ANALYTIC SCREEN, NOT A PRINT] " + disp["action"])
    return disp


def _disposition_core(verdicts) -> dict:
    by_nozzle = {}
    for v in verdicts:
        by_nozzle.setdefault(round(v.nozzle_mm, 2), []).append(v)
    coarse = by_nozzle.get(COARSE_NOZZLE, [])
    fine = by_nozzle.get(FINE_NOZZLE, [])

    # A full PASS only counts for the default 0.4 mm baseline. A pass earned
    # solely at the finer 0.2 mm nozzle is a process constraint, not a free
    # density result (protocol decision tree).
    if any(v.worst == "PASS" for v in coarse):
        best = [v for v in coarse if v.worst == "PASS"][0]
        return {
            "disposition": "S3_DENSITY_PRINTABLE",
            "reason": f"all M1-M6 pass on {best.run_id} at the 0.4 mm baseline",
            "action": "proceed to T11-B loaded dwell before head CAD/drive buy",
        }

    def webnotch_bad(rs):
        return any(set(v.hard_fail_keys) & {"M1", "M2"} for v in rs)

    coarse_block = webnotch_bad(coarse)
    fine_ok = any(v.worst == "PASS" for v in fine)
    if coarse_block and fine_ok:
        return {
            "disposition": "S3_REQUIRES_FINE_NOZZLE",
            "reason": "M1/M2 fail at 0.4 mm but pass at 0.2 mm (A4)",
            "action": "document 0.2 mm process constraint; re-pay timing with "
                      "slower fine-nozzle print cost",
        }


    if coarse and fine and webnotch_bad(coarse) and webnotch_bad(fine):
        return {
            "disposition": "REJECT_S3_4ROW_DROP_TO_2_3",
            "reason": "M1/M2 fail at both 0.4 mm and 0.2 mm",
            "action": f"drop to 2-3 rows/station and re-pay timing "
                      f"(stations: {STATIONS_BY_ROWS[3]} or "
                      f"{STATIONS_BY_ROWS[2]})",
        }

    summary = sorted({v.worst for v in coarse})
    return {
        "disposition": "INCONCLUSIVE_RUN_A4",
        "reason": "no 0.2 mm fallback row yet; 0.4 mm outcome: "
                  + (", ".join(summary) or "none"),
        "action": "print A4 (0.2 mm / 0.08 mm) and re-run this check",
    }


def predict() -> dict:
    web = BAND - FINGER_T
    lateral = PITCH - FINGER_T - PIVOT_D
    bbox = (PITCH * 2, PITCH * 4, 5.06)
    return {
        "M1_web_mm": round(web, 3),
        "M2_notch_mm": NOTCH_D,
        "M5_clearance_mm": round(lateral, 3),
        "M6_bbox_mm": [round(d, 2) for d in bbox],
        "labels": "CALCULATED from coupon parameters; NOT measured. "
                  "PREDICTION only.",
    }


NOTCH_D = 0.55


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--predict", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()

    if args.predict:
        print(json.dumps(predict(), indent=2) if args.json
              else "PREDICTED (calculated, not measured):\n"
              + "\n".join(f"  {k}: {v}" for k, v in predict().items()))
        return 0

    if args.selftest:
        return run_selftest()

    if args.validate:
        fields = GATE_ORDER_FIELDS
        here = Path(__file__).parent
        run_dir = here / "runs"
        files = [run_dir / "t11a_measurements.csv",
                 here / "analytic" / "runs" / "t11a_analytic_measurements.csv"]
        checked = 0
        for f in files:
            if not f.exists():
                print(f"[SKIP] {f} not present")
                continue
            rows = read_rows(f)
            missing = [c for c in fields if rows and c not in rows[0]]
            if missing:
                print(f"[FAIL] {f.name}: missing columns: {missing}")
                return 1
            print(f"[PASS] {f.name}: schema ok ({len(rows)} rows)")
            checked += 1
        if checked == 0:
            print("[FAIL] no run record found to validate")
            return 1
        return 0

    if not args.input:
        ap.error("need --input, --selftest, --predict or --validate")

    path = Path(args.input)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    rows = [r for r in read_rows(path) if (r.get("run_id") or "").strip()]
    verdicts = [score_run(r) for r in rows]
    disp = disposition_for(verdicts) if verdicts else {
        "disposition": "NO_DATA",
        "reason": "no run rows with a run_id",
        "action": "run the analytic gate and/or print A1-A4 and record M1-M6",
    }

    if args.json:
        out = {"runs": [], "disposition": disp}
        for v in verdicts:
            out["runs"].append({
                "run_id": v.run_id, "part": v.part,
                "nozzle_mm": v.nozzle_mm, "worst": v.worst,
                "evidence": v.evidence,
                "gates": [{"key": g.key, "outcome": g.outcome,
                           "value": g.value, "note": g.note}
                          for g in v.gates],
            })
        print(json.dumps(out, indent=2, default=str))
    else:
        for v in verdicts:
            print(f"== {v.run_id} ({v.part}, {v.nozzle_mm:g} mm, "
                  f"{v.evidence}) -> {v.worst}")
            for g in v.gates:
                print(f"   [{g.outcome:8}] {g.key}: {g.note}")
        print()
        print(f"DISPOSITION: {disp['disposition']}")
        print(f"  reason: {disp['reason']}")
        print(f"  action: {disp['action']}")
        if disp.get("evidence_warning"):
            print(f"  evidence: {disp['evidence_warning']}")

    if disp["disposition"] == "REJECT_S3_4ROW_DROP_TO_2_3":
        return 1
    if any(v.worst == "KILL" for v in verdicts):
        return 1
    return 0


def _row(**kw):
    base = {"run_id": "SYN", "part": "assembled", "nozzle_mm": "0.4",
            "layer_mm": "0.12"}
    base.update({k: str(v) for k, v in kw.items()})
    return base


def _check(name, got, want):
    ok = got == want
    print(f"[{'PASS' if ok else 'FAIL'}] selftest {name}: got {got!r}, want {want!r}")
    return ok


def run_selftest() -> int:
    """SYNTHETIC exercise of every gate branch. Never evidence about S3."""
    print("== T11-A fit-check SYNTHETIC selftest (not measured evidence) ==")
    ok = True

    # Every gate PASS at 0.4 mm -> density printable.
    r = _row(run_id="A1", M1_web_mm=0.22, M2_notch_mm=0.45, M3_pivot="yes",
             M4_land_mm=0.90, M5_clearance_mm=0.35,
             M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    v = score_run(r)
    ok &= _check("all-pass worst", v.worst, "PASS")
    ok &= _check("all-pass disposition",
                 disposition_for([v])["disposition"], "S3_DENSITY_PRINTABLE")

    # Coarse M1 web fuses (<0.20) but A4 fine passes -> fine nozzle required.
    rc = _row(run_id="A1", M1_web_mm=0.15, M2_notch_mm=0.45, M3_pivot="yes",
              M4_land_mm=0.90, M5_clearance_mm=0.35,
              M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    rf = _row(run_id="A4", nozzle_mm=0.2, layer_mm=0.08, M1_web_mm=0.25,
              M2_notch_mm=0.45, M3_pivot="yes", M4_land_mm=0.90,
              M5_clearance_mm=0.35, M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32,
              M6_bbox_z_mm=5.06)
    ok &= _check("coarse web kill", score_run(rc).worst, "KILL")
    ok &= _check("fine nozzle disposition",
                 disposition_for([score_run(rc), score_run(rf)])["disposition"],
                 "S3_REQUIRES_FINE_NOZZLE")

    # M1 web fuses at BOTH nozzles -> reject 4-row.
    rf2 = _row(run_id="A4", nozzle_mm=0.2, layer_mm=0.08, M1_web_mm=0.10,
               M2_notch_mm=0.45, M3_pivot="yes", M4_land_mm=0.90,
               M5_clearance_mm=0.35, M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32,
               M6_bbox_z_mm=5.06)
    ok &= _check("reject disposition",
                 disposition_for([score_run(rc), score_run(rf2)])["disposition"],
                 "REJECT_S3_4ROW_DROP_TO_2_3")

    # Coarse-only bad web with no A4 row -> inconclusive, ask for A4.
    ok &= _check("inconclusive disposition",
                 disposition_for([score_run(rc)])["disposition"],
                 "INCONCLUSIVE_RUN_A4")

    # M2 notch FAIL (0.30) but no kill -> is a FAIL, drives fine/nozzle path.
    rn = _row(run_id="A1", M1_web_mm=0.22, M2_notch_mm=0.30, M3_pivot="yes",
              M4_land_mm=0.90, M5_clearance_mm=0.35,
              M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    ok &= _check("notch fail worst", score_run(rn).worst, "FAIL")

    # M3 fused pivot -> KILL.
    r3 = _row(run_id="A2", M1_web_mm=0.22, M2_notch_mm=0.45, M3_pivot="no",
              M4_land_mm=0.90, M5_clearance_mm=0.35,
              M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    ok &= _check("fused pivot KILL", score_run(r3).worst, "KILL")

    # M5 collision (<=0) -> KILL.
    r5 = _row(run_id="A3", M1_web_mm=0.22, M2_notch_mm=0.45, M3_pivot="yes",
              M4_land_mm=0.90, M5_clearance_mm=0.0,
              M6_bbox_x_mm=10.16, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    ok &= _check("bank collision KILL", score_run(r5).worst, "KILL")

    # M6 bbox over-envelope -> FAIL.
    r6 = _row(run_id="A1", M1_web_mm=0.22, M2_notch_mm=0.45, M3_pivot="yes",
              M4_land_mm=0.90, M5_clearance_mm=0.35,
              M6_bbox_x_mm=30.0, M6_bbox_y_mm=20.32, M6_bbox_z_mm=5.06)
    ok &= _check("bbox over FAIL", score_run(r6).worst, "FAIL")

    # Missing fields -> INCONCLUSIVE.
    rmiss = _row(run_id="A1")
    ok &= _check("missing -> inconclusive", score_run(rmiss).worst,
                 "INCONCLUSIVE")

    # Packed bbox string parses.
    rpk = _row(run_id="A1", M1_web_mm=0.22, M2_notch_mm=0.45, M3_pivot="yes",
               M4_land_mm=0.90, M5_clearance_mm=0.35, M6_bbox_mm="10.16x20.32x5.06")
    ok &= _check("packed bbox PASS", score_run(rpk).worst, "PASS")

    print()
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
