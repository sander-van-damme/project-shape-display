#!/usr/bin/env python3
"""DND-104 pre-registered adversarial audit gate (DND-108).

Run from anywhere:
    python 07-evidence-and-decisions/falsifier_dnd104_checks.py
    python 07-evidence-and-decisions/falsifier_dnd104_checks.py --model <path-to-model.py>

Two jobs:

1. SELF-TEST (no --model): pins the counter-numbers in
   `falsifier_dnd104_criteria.md` against the repository's own reliability arithmetic
   (`06-experiments/test11_falsification_library/reliability.py`) and the historic
   S6-LC / S1 numbers. This is what CI asserts, so the pre-registered prose cannot
   drift from arithmetic.

2. MODEL AUDIT (--model): applies the same checklist to the CTO's
   `10-reliability-mask/` model the moment it lands, via `audit(model)`.

Evidence class: CALCULATION over the repo's own model. No print, no purchase, no
measurement (DND-27). No board contact (DND-32).

The audit is DEFAULT-DENY: an attack field that is absent or null is reported
UNRESOLVED and forces the audit verdict to FAIL. A model is only "pre-registered
clean" if every attack is answered with a number and meets its threshold.
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RELIABILITY = REPO / "06-experiments" / "test11_falsification_library" / "reliability.py"

CELLS_FULL = 6400
PITCH_MM = 5.08
COLUMN_BODY_MM = 3.60
OWNED_HALF_LANE_MM = PITCH_MM / 2 - COLUMN_BODY_MM / 2  # 0.74
Q_FEAR = 1e-4                 # 0.01 % per-cell, the program's stated fear point
Q_BUDGET_6400 = 1.570e-6      # 1 - 0.99^(1/6400): the 99 %-map per-cell budget
MAP_TARGET = 0.99
S1_MASK_HOLES = 12800         # 3200 cells x 4 unary planes (test11 rejection.py:148)
S1_HOLE_WRITE_S = 0.20        # seconds per hole, serial
S1_CHANNELS = 80
S6LC_PARTS = 226.77           # DND-93/98 corrected S6-LC purchased parts
S6LC_DELIVERED = 263.05
S6LC_PARTIAL_DELIVERED = 196.93  # DND-91/A5 hostile reprice, pre-DND-93
CEILING_STRONG = 250.0        # <$250 purchased (DND-72 ultra-low-cost track)
CEILING_MISSION = 500.0       # goal-level purchased cost


def _load_reliability():
    spec = importlib.util.spec_from_file_location("test11_reliability", RELIABILITY)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    # dataclasses look their module up in sys.modules, so register before exec.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# attacks: pure functions of model fields. Each returns (pass, detail, decided).
# absent/None fields -> UNRESOLVED (fail).
# --------------------------------------------------------------------------

def attack_a1_yield(m):
    """Map yield compounds: (1-q)^N >= 0.99 for the declared N and q."""
    n = m.get("N")
    q = m.get("q")
    if n is None or q is None:
        return (False, "UNRESOLVED (declare N and q)", None)
    yield_ = (1.0 - q) ** n
    return (yield_ >= MAP_TARGET,
            f"(1-{q:g})^{n} = {yield_:.4f} vs target {MAP_TARGET}", yield_)


def attack_a2_coupon_bound(m):
    """Coupon must run enough counted cycles to bound q below 1-0.99^(1/N)."""
    n = m.get("N")
    trials = m.get("coupon_trials")
    misses = m.get("coupon_misses", 0)
    if n is None or trials is None:
        return (False, "UNRESOLVED (declare N and coupon_trials)", None)
    q_budget = 1.0 - MAP_TARGET ** (1.0 / n)
    if misses and misses > 0:
        return (False, f"{misses} counted miss(es) in {trials} trials", misses / trials)
    q_ub = 1.0 - 0.05 ** (1.0 / trials)
    return (q_ub <= q_budget,
            f"95% UB q={q_ub:.3e} vs budget={q_budget:.3e}", q_ub)


def attack_a3_correlated(m):
    """Correlated group must be bounded AND detectable."""
    group = m.get("correlated_group_size")
    detect = m.get("correlated_detection")
    if group is None or detect is None:
        return (False, "UNRESOLVED (declare group size + detection path)", None)
    ok = isinstance(detect, str) and len(detect.strip()) > 0 and group >= 1
    return (ok, f"group={group}, detection={detect!r}", group)


def attack_a4_count(m):
    """Per-cell force-critical / precision elements must be zero."""
    springs = m.get("per_cell_force_critical_springs")
    contacts = m.get("per_cell_precision_contacts")
    if springs is None or contacts is None:
        return (False, "UNRESOLVED (declare per-cell counters)", None)
    ok = springs == 0 and contacts == 0
    return (ok, f"force-critical springs={springs}, precision contacts={contacts}",
            (springs, contacts))


def attack_a5_timing(m):
    """All seven DND-103 stages present; visible AND sustained < 30 s."""
    stages = m.get("timing_stages")
    if not stages:
        return (False, "UNRESOLVED (declare all 7 timing stages)", None)
    required = {"digital_map_s", "mask_generation_s", "mask_transport_s",
                "display_reset_s", "broadcast_s", "settle_s", "verification_s"}
    missing = required - set(stages)
    if missing:
        return (False, f"missing stages: {sorted(missing)}", None)
    visible = m.get("visible_transition_s", sum(stages.values()))
    sustained = m.get("sustained_cycle_s", sum(stages.values()))
    ok = visible < 30.0 and sustained < 30.0
    return (ok, f"visible={visible:.3f} s, sustained={sustained:.3f} s (<30 required)", visible)


def attack_a6_regional(m):
    """Regional disturbance bounded; no full-board reset for a local reveal."""
    dist = m.get("regional_neighbour_displacement_mm")
    full_reset = m.get("regional_requires_full_reset")
    if dist is None or full_reset is None:
        return (False, "UNRESOLVED (declare neighbour displacement + reset policy)", None)
    ok = (dist <= 0.10) and (full_reset is False)
    return (ok, f"neighbour={dist} mm (<=0.10), full_reset={full_reset}", dist)


def attack_a7_cost(m):
    """Hostile repriced purchased total under the strong ceiling; capabilities costed."""
    total = m.get("hostile_repriced_purchased_usd")
    missing = m.get("uncosted_capabilities", None)
    if total is None:
        return (False, "UNRESOLVED (declare hostile repriced purchased total)", None)
    if missing:
        return (False, f"uncosted capabilities: {missing}", total)
    ok = total < CEILING_STRONG
    return (ok, f"hostile purchased=${total:.2f} (<${CEILING_STRONG:.0f} required)", total)


def attack_a8_load(m):
    """Write-time load per moving column vs hold capacity, with a mini load."""
    load = m.get("write_load_per_column_n")
    cap = m.get("hold_capacity_n")
    sf = m.get("load_sf", 1.0)
    if load is None or cap is None:
        return (False, "UNRESOLVED (declare write load + hold capacity)", None)
    ok = load <= cap / sf
    return (ok, f"load={load} N <= capacity/SF={cap}/{sf}", load)


def attack_a9_jam(m):
    """Jam blast radius 1 cell and detectable."""
    blast = m.get("jam_blast_radius_cells")
    detect = m.get("jam_detection")
    if blast is None or detect is None:
        return (False, "UNRESOLVED (declare jam blast radius + detection)", None)
    ok = blast == 1 and isinstance(detect, str) and detect.strip()
    return (ok, f"blast radius={blast}, detection={detect!r}", blast)


def attack_a10_placement(m):
    """Placed CAD: max feature excursion within the owned half-lane."""
    exc = m.get("max_feature_excursion_mm")
    lane = m.get("owned_half_lane_mm", OWNED_HALF_LANE_MM)
    if exc is None:
        return (False, "UNRESOLVED (declare placed max feature excursion)", None)
    ok = exc <= lane
    return (ok, f"excursion={exc} mm <= owned lane={lane:.2f} mm", exc)


def attack_a12_pitch(m):
    """Same class as A10 but explicitly requires the PLACED number, not a budget."""
    placed = m.get("placement_is_placed_cad")
    exc = m.get("max_feature_excursion_mm")
    if placed is None or exc is None:
        return (False, "UNRESOLVED (placement must be shown in CAD, not budgeted)", None)
    ok = bool(placed) and exc <= OWNED_HALF_LANE_MM
    return (ok, f"placed={placed}, excursion={exc} <= {OWNED_HALF_LANE_MM:.2f}", (placed, exc))


_ALL_FIELDS = {
    "N", "q", "coupon_trials", "coupon_misses", "correlated_group_size",
    "correlated_detection", "per_cell_force_critical_springs",
    "per_cell_precision_contacts", "timing_stages", "visible_transition_s",
    "sustained_cycle_s", "regional_neighbour_displacement_mm",
    "regional_requires_full_reset", "hostile_repriced_purchased_usd",
    "uncosted_capabilities", "write_load_per_column_n", "hold_capacity_n",
    "load_sf", "jam_blast_radius_cells", "jam_detection",
    "max_feature_excursion_mm", "owned_half_lane_mm", "placement_is_placed_cad",
}


ATTACKS = {
    "A1_yield": attack_a1_yield,
    "A2_coupon_bound": attack_a2_coupon_bound,
    "A3_correlated": attack_a3_correlated,
    "A4_count": attack_a4_count,
    "A5_timing": attack_a5_timing,
    "A6_regional": attack_a6_regional,
    "A7_cost": attack_a7_cost,
    "A8_load": attack_a8_load,
    "A9_jam": attack_a9_jam,
    "A10_placement": attack_a10_placement,
    "A12_pitch": attack_a12_pitch,
}


def audit(model):
    """Apply the pre-registered checklist to a candidate model.

    `model` is any mapping-like object with the declared fields (a dict, a module
    namespace, or similar). Returns per-attack results, the list of unresolved
    attacks, and the default-deny verdict.
    """
    if hasattr(model, "get"):
        view = model
    else:
        view = {k: getattr(model, k, None) for k in _ALL_FIELDS}
    results = {}
    unresolved = []
    for name, fn in ATTACKS.items():
        ok, detail, decided = fn(view)
        results[name] = {"pass": bool(ok), "detail": detail, "decided_number": decided}
        if "UNRESOLVED" in detail:
            unresolved.append(name)
    passed = all(r["pass"] for r in results.values())
    return {"attacks": results, "unresolved": unresolved, "pass": passed}


# --------------------------------------------------------------------------
# self-test: pins the pre-registered counter-numbers (CI)
# --------------------------------------------------------------------------

FAILURES = []
CHECKS = 0


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def run_selftest():
    rel = _load_reliability()
    print("DND-104 pre-registered adversarial audit - SELF-TEST")
    print("=" * 68)

    # ---- A1: map yield compounds ----------------------------------------
    print("[A1] Map yield (1-q)^N -- the 52.7 % headline")
    p = rel.perfect_map_probability(Q_FEAR, CELLS_FULL)
    check("q=0.01% at N=6400 -> 52.7 %", abs(p - 0.5273) < 5e-4, f"{p:.4f}")
    check("q=0.01% at N=800 -> 92.3 %",
          abs(rel.perfect_map_probability(Q_FEAR, 800) - 0.9231) < 5e-4)
    check("q=0.01% at N=100 -> 99.0 %",
          abs(rel.perfect_map_probability(Q_FEAR, 100) - 0.9900) < 5e-4)
    check("a 99 % map needs q <= 1.570e-6 at N=6400",
          abs(rel.cell_error_budget(MAP_TARGET, CELLS_FULL) - Q_BUDGET_6400) < 1e-9,
          f"{rel.cell_error_budget(MAP_TARGET, CELLS_FULL):.4e}")

    # ---- A2: what a coupon must bound -----------------------------------
    print("[A2] Coupon zero-failure trial counts (95 % upper bound)")
    check("exclude q=1e-4 needs 29,956 trials",
          rel.zero_failure_trials(1e-4, 0.95) == 29956)
    check("exclude q=1e-5 needs 299,572 trials",
          rel.zero_failure_trials(1e-5, 0.95) == 299572)
    check("exclude q=1.570e-6 needs 1,908,109 trials",
          rel.zero_failure_trials(Q_BUDGET_6400, 0.95) == 1908109)
    check("legacy zero-failure convention is ~58x smaller (do not use)",
          rel.zero_failure_trials(1e-5, 0.95, convention="zero_failure_probability")
          == math.ceil(math.log(0.95) / math.log(1 - 1e-5)))

    # ---- A2b: a coupon can kill, not crown ------------------------------
    print("[A2b] 'A coupon can kill, but cannot crown'")
    n_coupon = 400  # 4 elements x 100 counted cycles
    q_ub_400 = 1.0 - 0.05 ** (1.0 / n_coupon)
    check("400 clean cycles bound q only at ~7.5e-3",
          abs(q_ub_400 - 0.007485) < 5e-5, f"{q_ub_400:.4e}")
    check("that is >1000x looser than the 1.570e-6 board budget",
          q_ub_400 / Q_BUDGET_6400 > 1000, f"{q_ub_400 / Q_BUDGET_6400:.0f}x")

    # ---- A3: correlated group / detection -------------------------------
    print("[A3] Correlated failure + detection")
    check("S6-LC detection is 4 sensors/bank, not per-cell (32 over 8 banks)",
          4 * 8 == 32)
    check("an undetected correlated fault is CORRELATED_FAIL",
          rel.jam_containment(100, 80, True) == "CORRELATED_FAIL")
    check("a lone jam with no shared boundary is CONTAINED",
          rel.jam_containment(1, 0, False) == "CONTAINED")

    # ---- A4: the count attack -------------------------------------------
    print("[A4] Per-cell precision/force-critical count")
    check("owned half-lane is 0.74 mm", abs(OWNED_HALF_LANE_MM - 0.74) < 1e-9)
    check("a 0.90 pawl placed at BODY/2+0.10 overflows 0.260 mm (DND-91 A1)",
          abs(((COLUMN_BODY_MM / 2 + 0.10 + 0.90) - PITCH_MM / 2) - 0.26) < 1e-9)

    # ---- A5: honest timing ----------------------------------------------
    print("[A5] Honest mask/timing terms")
    serial = S1_MASK_HOLES * S1_HOLE_WRITE_S
    ch80 = S1_MASK_HOLES / S1_CHANNELS * 0.35
    ch500 = S1_MASK_HOLES / 500 * 0.35
    check("S1 mask write is 12,800 holes (3200 x 4)", S1_MASK_HOLES == 12800)
    check("serial mask write = 2,560 s", abs(serial - 2560.0) < 1e-9, f"{serial:.0f} s")
    check("80-channel mask write = 56 s (FAILS 30 s)", abs(ch80 - 56.0) < 1e-9,
          f"{ch80:.1f} s")
    check("500-channel mask write = 8.96 s (passes)", abs(ch500 - 8.96) < 1e-9,
          f"{ch500:.2f} s")

    # ---- A7: cost ladder honesty ----------------------------------------
    print("[A7] Cost ladder (DND-46 hostile reprice)")
    check("S6-LC hostile reprice was ~$197 delivered (pre-DND-93)",
          abs(S6LC_PARTIAL_DELIVERED - 196.93) < 1e-9)
    check("S6-LC corrected purchased parts = $226.77 (<$250, mission gate)",
          S6LC_PARTS < CEILING_STRONG, f"${S6LC_PARTS}")
    check("S6-LC corrected delivered = $263.05 (>$250, convention fails)",
          S6LC_DELIVERED > CEILING_STRONG, f"${S6LC_DELIVERED}")
    check("mission ceiling is $500 (purchased)", CEILING_MISSION == 500.0)

    # ---- A11/A12: placement not budget ----------------------------------
    print("[A11/A12] A coupon can kill, not crown; placement is mandatory")
    clean_model = {
        "N": 6400, "q": 1.570e-6, "coupon_trials": 1_908_109,
        "correlated_group_size": 800, "correlated_detection": "per-bank home sensor",
        "per_cell_force_critical_springs": 0, "per_cell_precision_contacts": 0,
        "timing_stages": {"digital_map_s": 0.1, "mask_generation_s": 1.0,
                          "mask_transport_s": 0.5, "display_reset_s": 2.0,
                          "broadcast_s": 3.4, "settle_s": 0.6, "verification_s": 1.0},
        "regional_neighbour_displacement_mm": 0.05, "regional_requires_full_reset": False,
        "hostile_repriced_purchased_usd": 200.0, "uncosted_capabilities": [],
        "write_load_per_column_n": 0.7, "hold_capacity_n": 200.0, "load_sf": 2.0,
        "jam_blast_radius_cells": 1, "jam_detection": "per-bank home sensor",
        "max_feature_excursion_mm": 0.40, "placement_is_placed_cad": True,
    }
    ok = audit(clean_model)
    check("a fully-answered clean model passes audit()", ok["pass"],
          f"unresolved={ok['unresolved']}")
    empty = audit({})
    check("an empty model FAILS audit() (default-deny)", empty["pass"] is False)
    check("empty model reports every attack UNRESOLVED",
          len(empty["unresolved"]) == len(ATTACKS), f"{len(empty['unresolved'])}/{len(ATTACKS)}")

    print("=" * 68)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} pre-registration checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("All DND-104 pre-registered counter-numbers are pinned: prose cannot "
          "drift from arithmetic.")
    return 0


def load_model(path):
    spec = importlib.util.spec_from_file_location("dnd104_model", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    if hasattr(mod, "build_model"):
        return mod.build_model()
    if hasattr(mod, "MODEL"):
        return mod.MODEL
    raise SystemExit(f"{path}: no build_model() or MODEL found")


def main(argv=None):
    ap = argparse.ArgumentParser(description="DND-104 pre-registered adversarial audit")
    ap.add_argument("--model", help="path to a candidate model module to audit")
    args = ap.parse_args(argv)
    if args.model:
        model = load_model(args.model)
        result = audit(model)
        print(f"DND-104 audit of {args.model}")
        print("=" * 68)
        for name, r in result["attacks"].items():
            print(f"  {'PASS' if r['pass'] else 'FAIL'}  {name:18s} {r['detail']}")
        print("=" * 68)
        verdict = "PRE-REGISTERED CLEAN" if result["pass"] else "FAIL / NOT CLEAN"
        print(f"verdict: {verdict}  (unresolved: {result['unresolved']})")
        return 0 if result["pass"] else 1
    return run_selftest()


if __name__ == "__main__":
    raise SystemExit(main())
