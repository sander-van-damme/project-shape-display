#!/usr/bin/env python3
"""Test11 -- runnable J2 isolation-rig protocol runner (no hardware required).

Executable half of `isolation_rig_protocol.md`. It reads the J2 measurement
table (`measurements/isolation.csv`), applies the protocol's pass/fail gates
row by row, and emits a per-survivor go / kill / inconclusive decision plus the
board-level reliability consequence of a counted-failure run.

No hardware is needed to *exercise* it. This is a gate engine, not a
measurement: running it proves the gate logic is consistent and that the
protocol applies mechanically once real rows exist. It proves nothing about
any architecture.

Evidence labels: CALCULATED (arithmetic), SYNTHETIC (engine exercise, never
evidence), MEASURED (a real instrument reading; the only label that can move a
survivor toward "go").

Usage:
    python isolation_rig_runner.py --validate
    python isolation_rig_runner.py --selftest
    python isolation_rig_runner.py --input measurements/isolation.csv
    python isolation_rig_runner.py --input run.csv --json

Exit codes: 0 = validated or all GO; 1 = at least one KILL; 2 = usage/file error.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import reliability as r

MAX_IS_LOWER = "max"
FULL_MAP_SECONDS = 26.251  # modelled full-map time; test09/test11


@dataclass(frozen=True)
class Gate:
    key: str
    field_name: str
    label: str
    units: str
    pass_at: float
    fail_at: float
    aggregation: str
    phase: str


# Peak-disturbance gates: the max across repeats is the statistic (protocol:
# "record the maximum, not the mean").
PEAK_GATES = [
    Gate("peak_vertical", "peak_vertical_mm",
         "Neighbour peak vertical displacement", "mm", 0.10, 0.25,
         MAX_IS_LOWER, "J2-1"),
    Gate("peak_lateral", "peak_lateral_mm",
         "Neighbour peak lateral displacement", "mm", 0.10, 0.25,
         MAX_IS_LOWER, "J2-1"),
    Gate("miniature_move", "miniature_move_mm",
         "Miniature base movement", "mm", 0.50, 0.50, MAX_IS_LOWER, "J2-1"),
    Gate("miniature_tip", "miniature_tip_mm",
         "Miniature tipping (edge lift)", "mm", 0.50, 0.50,
         MAX_IS_LOWER, "J2-1"),
    Gate("seam_step", "seam_step_mm",
         "Seam step at max adjacent heights", "mm", 0.25, 0.50,
         MAX_IS_LOWER, "J2-2"),
    Gate("cumulative_drift", "cumulative_drift_mm",
         "Cumulative drift over 100 cycles", "mm", 0.20, 0.50,
         MAX_IS_LOWER, "J2-3"),
]

RIG_GATES = [
    Gate("rig_noise", "rig_noise_mm",
         "Rig noise floor", "mm", 0.02, 0.02, MAX_IS_LOWER, "J2-0"),
]

TILE_TIME_GATES = {
    "5x5": Gate("regional_settle_5x5", "regional_clear_settle_s",
                "Regional clear+settle (5x5)", "s", 3.0, FULL_MAP_SECONDS,
                MAX_IS_LOWER, "J2-4"),
    "10x10": Gate("regional_settle_10x10", "regional_clear_settle_s",
                  "Regional clear+settle (10x10)", "s", 5.0, FULL_MAP_SECONDS,
                  MAX_IS_LOWER, "J2-4"),
    "20x20": Gate("regional_settle_20x20", "regional_clear_settle_s",
                  "Regional clear+settle (20x20)", "s", 8.0, FULL_MAP_SECONDS,
                  MAX_IS_LOWER, "J2-4"),
}

ALL_GATES = PEAK_GATES + RIG_GATES + list(TILE_TIME_GATES.values())

MIN_CYCLES_CORE = 10       # J2-1 repeats
MIN_CYCLES_EXCHANGE = 100  # J2-3 drift cycles


@dataclass
class GateResult:
    gate: Gate
    value: float
    outcome: str  # PASS | FAIL | INCONCLUSIVE | MISSING
    note: str = ""


@dataclass
class SurvivorVerdict:
    survivor: str
    fixture_id: str
    tile_size: str
    rows: int
    gates: list = field(default_factory=list)
    evidence: str = "MEASURED"

    @property
    def outcome(self) -> str:
        if not self.gates:
            return "INCONCLUSIVE"
        outcomes = {g.outcome for g in self.gates}
        if "FAIL" in outcomes:
            return "KILL"
        if "INCONCLUSIVE" in outcomes or "MISSING" in outcomes:
            return "INCONCLUSIVE"
        return "GO"

    @property
    def reason(self) -> str:
        if self.outcome == "KILL":
            bad = ", ".join(g.gate.key for g in self.gates
                            if g.outcome == "FAIL")
            return "failed gate(s): " + bad
        if self.outcome == "INCONCLUSIVE":
            weak = ", ".join(g.gate.key for g in self.gates
                             if g.outcome in ("INCONCLUSIVE", "MISSING"))
            return "insufficient evidence for: " + weak
        return "all gates pass on measured rows"


def _parse_float(raw):
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "" or text.lower() in ("na", "n/a", "nan", "none"):
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _score(gate: Gate, value: float) -> str:
    if value <= gate.pass_at:
        return "PASS"
    if value > gate.fail_at:
        return "FAIL"
    return "INCONCLUSIVE"


def read_rows(path: Path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("empty CSV (no header)")
        return list(reader)


def score_table(rows):
    groups = {}
    for row in rows:
        survivor = (row.get("survivor") or "").strip()
        if not survivor:
            continue
        key = (survivor, (row.get("fixture_id") or "").strip(),
               (row.get("tile_size") or "").strip())
        groups.setdefault(key, []).append(row)

    verdicts = []
    for (survivor, fixture, tile), grows in sorted(groups.items()):
        v = SurvivorVerdict(survivor=survivor, fixture_id=fixture,
                            tile_size=tile, rows=len(grows))

        noise_vals = [_parse_float(g.get("rig_noise_mm")) for g in grows]
        noise_vals = [n for n in noise_vals if n is not None]
        if noise_vals:
            worst = max(noise_vals)
            v.gates.append(GateResult(RIG_GATES[0], round(worst, 4),
                                      _score(RIG_GATES[0], worst),
                                      "worst rig_noise_mm in group"))
        else:
            v.gates.append(GateResult(RIG_GATES[0], float("nan"), "MISSING",
                                      "no J2-0 rig qualification recorded"))

        for gate in PEAK_GATES:
            vals = [_parse_float(g.get(gate.field_name)) for g in grows]
            vals = [x for x in vals if x is not None]
            if not vals:
                v.gates.append(GateResult(gate, float("nan"), "MISSING",
                                          "no reading"))
                continue
            worst = max(vals)
            outcome = _score(gate, worst)
            note = "n=%d max=%g" % (len(vals), worst)
            if gate.key == "cumulative_drift":
                cycles = [_parse_float(g.get("cycles")) for g in grows]
                cycles = [c for c in cycles if c is not None]
                if not cycles or max(cycles) < MIN_CYCLES_EXCHANGE:
                    outcome = "INCONCLUSIVE"
                    note += "; needs >= %d cycles" % MIN_CYCLES_EXCHANGE
            if gate.phase == "J2-1" and len(vals) < MIN_CYCLES_CORE:
                outcome = "INCONCLUSIVE"
                note += "; needs >= %d repeats" % MIN_CYCLES_CORE
            v.gates.append(GateResult(gate, round(worst, 4), outcome, note))

        tgate = TILE_TIME_GATES.get(tile)
        if tgate is not None:
            vals = [_parse_float(g.get("regional_clear_settle_s"))
                    for g in grows]
            vals = [x for x in vals if x is not None]
            if not vals:
                v.gates.append(GateResult(tgate, float("nan"), "MISSING",
                                          "no timing reading"))
            else:
                worst = max(vals)
                v.gates.append(GateResult(tgate, round(worst, 3),
                                          _score(tgate, worst),
                                          "n=%d max=%g" % (len(vals), worst)))
        verdicts.append(v)
    return verdicts


def reliability_consequence(operations: int, failures: int) -> dict:
    """Board-level consequence of a counted-failure coupon run (CALCULATED).

    With zero failures we report the one-sided 95% upper bound on q, the
    honest statement a zero-failure coupon supports.
    """
    if operations <= 0:
        raise ValueError("operations must be positive")
    if failures < 0 or failures > operations:
        raise ValueError("failures must be in [0, operations]")
    if failures == 0:
        q_hat = 0.0
        q_bound = 1.0 - 0.05 ** (1.0 / operations)
        bound_kind = "95% one-sided upper bound (zero failures)"
    else:
        q_hat = failures / operations
        q_bound = q_hat
        bound_kind = "point estimate"
    return {
        "operations": operations,
        "failures": failures,
        "q_point": q_hat,
        "q_bound": q_bound,
        "q_bound_kind": bound_kind,
        "perfect_map_prob": r.perfect_map_probability(q_bound),
        "passes_99pct_map": r.perfect_map_probability(q_bound) >= 0.99,
        "needed_q_for_99pct_map": r.cell_error_budget(0.99),
        "zero_failure_trials_for_99pct": r.zero_failure_trials(
            r.cell_error_budget(0.99), 0.95),
    }


def _synth_rows(prefix, n, **overrides):
    base = {
        "run_id": prefix, "date": "YYYY-MM-DD", "survivor": "S_TEST",
        "fixture_id": "FX-TEST", "tile_size": "10x10",
        "rig_noise_mm": "0.005", "peak_vertical_mm": "0.05",
        "peak_lateral_mm": "0.04", "miniature_move_mm": "0.10",
        "miniature_tip_mm": "0.05", "seam_step_mm": "0.10",
        "cumulative_drift_mm": "0.05", "cycles": "100",
        "regional_clear_settle_s": "3.5",
    }
    base.update(overrides)
    return [dict(base, run_id="%s-%d" % (prefix, i)) for i in range(n)]


def selftest() -> int:
    cases = {
        "PASS": _synth_rows("SYNTHETIC-PASS", 10),
        "FAIL": _synth_rows("SYNTHETIC-FAIL", 10,
                            peak_vertical_mm="0.30", peak_lateral_mm="0.30",
                            miniature_move_mm="0.80", miniature_tip_mm="0.80",
                            seam_step_mm="0.60", cumulative_drift_mm="0.60",
                            regional_clear_settle_s="30.0"),
        "INCONCLUSIVE": _synth_rows("SYNTHETIC-INC", 3, seam_step_mm="0.30",
                                    cumulative_drift_mm="0.30"),
    }
    expected = {"PASS": "GO", "FAIL": "KILL", "INCONCLUSIVE": "INCONCLUSIVE"}
    failures = 0
    for name, rows in cases.items():
        v = score_table(rows)[0]
        ok = v.outcome == expected[name]
        failures += 0 if ok else 1
        print("[SYNTHETIC] case=%-13s expected=%-13s got=%-13s %s"
              % (name, expected[name], v.outcome, "OK" if ok else "ENGINE BUG"))

    # A clean 10k-operation coupon must NOT be enough: the 95% upper bound on q
    # is still far above the 1.57e-6 budget, so the board cannot be called safe.
    rc = reliability_consequence(10000, 0)
    bound_ok = (rc["q_bound"] > rc["needed_q_for_99pct_map"]
                and not rc["passes_99pct_map"])
    failures += 0 if bound_ok else 1
    print("[CALCULATED] 0 failures / 10000 ops -> q_bound=%.3e, "
          "perfect-map=%.3f, passes_99pct=%s %s"
          % (rc["q_bound"], rc["perfect_map_prob"], rc["passes_99pct_map"],
             "OK" if bound_ok else "BOUND BUG"))
    print("SELFTEST %s" % ("PASS" if failures == 0 else "FAIL"))
    return 0 if failures == 0 else 1


def validate() -> int:
    """Validate the shipped table schema against the gate definitions."""
    here = Path(__file__).resolve().parent
    table = here / "measurements" / "isolation.csv"
    with table.open(newline="") as f:
        fields = set(next(csv.reader(f)))
    needed = {g.field_name for g in ALL_GATES} | {
        "survivor", "fixture_id", "tile_size", "cycles"}
    missing = sorted(needed - fields)
    print("gates: %d; table fields: %d" % (len(ALL_GATES), len(fields)))
    if missing:
        print("MISSING TABLE FIELDS: %s" % ", ".join(missing))
        return 1
    print("VALIDATE: table schema covers every gate field")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.validate:
        return validate()

    if args.input is None:
        args.input = (Path(__file__).resolve().parent
                      / "measurements" / "isolation.csv")
    if not args.input.exists():
        print("file not found: %s" % args.input, file=sys.stderr)
        return 2

    verdicts = score_table(read_rows(args.input))
    if args.json:
        print(json.dumps({
            "input": str(args.input),
            "evidence": "MEASURED (rows are operator-entered)",
            "verdicts": [{
                "survivor": v.survivor, "fixture_id": v.fixture_id,
                "tile_size": v.tile_size, "rows": v.rows,
                "outcome": v.outcome, "reason": v.reason,
                "gates": [{"key": g.gate.key, "value": g.value,
                           "outcome": g.outcome, "note": g.note}
                          for g in v.gates],
            } for v in verdicts],
        }, indent=2))
    else:
        if not verdicts:
            print("no scored rows (table is empty or header-only)")
        for v in verdicts:
            print("%s [%s/%s] rows=%d -> %s (%s)"
                  % (v.survivor, v.fixture_id, v.tile_size, v.rows,
                     v.outcome, v.reason))
            for g in v.gates:
                print("    %-22s %-13s %s" % (g.gate.key, g.outcome, g.note))

    return 1 if any(v.outcome == "KILL" for v in verdicts) else 0


if __name__ == "__main__":
    raise SystemExit(main())
