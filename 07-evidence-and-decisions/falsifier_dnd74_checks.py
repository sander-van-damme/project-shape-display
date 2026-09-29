#!/usr/bin/env python3
"""Falsifier DND-74 checks: the S6-LC ultra-low-cost audit (RE-BASELINED by DND-93).

Run:  python3 07-evidence-and-decisions/falsifier_dnd74_checks.py

Evidence class: CALCULATION on the repository's own declared 08-integrated-designs/s6lc-low-cost
constants, plus sourced-fact readings of the S1 screen. No print, no measurement
(DND-27).

HISTORY. As delivered (original gate) these checks asserted the PRE-FIX broken
state: `lift_axis()` sized on one bank while the write is global (decisive G3
break), a circular 296 N release ceiling, cost headroom collapsing under honest
allowances, and the mask-write/reliability bounds. [DND-93](/DND/issues/DND-93)
then fixed the lift axis and the bounded findings. This gate is re-baselined so
that it still *reproduces the attack arithmetic from the constants* (as the
historical record) AND asserts that the fix has landed and the corrected gate
result holds. The superseding, live adversarial gate is
`falsifier_dnd91_checks.py` (40 checks).

Exit 0 if every assertion holds, 1 otherwise.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S6LC_PY = (REPO / "08-integrated-designs" / "s6lc-low-cost" / "analysis"
           / "s6lc.py")

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILURES.append(name)


def _load_s6lc():
    spec = importlib.util.spec_from_file_location("s6lc_dnd74", S6LC_PY)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _torque(force_n: float, lead_mm: float, eff: float = 0.5) -> float:
    return force_n * (lead_mm / 1000.0) / (2 * math.pi * eff)


def main() -> int:
    s6 = _load_s6lc()

    print("DND-74 S6-LC falsification checks (re-baselined by DND-93)")
    print("=" * 40)

    # --- Attack 2: lift-axis sizing ------------------------------------------
    # The historical attack arithmetic is reproduced from the constants, and the
    # DND-93 fix is asserted in place.
    print("[A2] Lift-axis sizing (was the decisive break; FIXED by DND-93)")
    lift = s6.lift_axis()
    lead = s6.LEAD_MM
    # Historical: the old motor was a 0.30 N*m NEMA17 and the global load would
    # have broken it. Reproduce that arithmetic from the constants.
    old_motor = 0.30
    global_load = s6.LIFT_LOAD_N * s6.CELLS
    tq_global = _torque(global_load, lead)
    check("A2a historical: global load is 2560 N -> 1.63 Nm",
          abs(global_load - 2560.0) < 1e-6 and abs(tq_global - 1.6297) < 1e-3,
          f"{global_load:.0f} N -> {tq_global:.4f} Nm")
    check("A2b historical: the old 0.30 N*m NEMA17 would FAIL the global load",
          tq_global > old_motor, f"{tq_global:.2f} Nm > {old_motor} Nm")
    check("A2c historical: per-screw on 4 screws also breaks the NEMA17",
          _torque(global_load / 4.0, lead) > old_motor,
          f"{_torque(global_load / 4.0, lead):.3f} Nm/screw")
    check("A2d the mechanism writes the whole board (global strokes)",
          s6.timing()["strokes"] == 4 and s6.BANKS * s6.RESET_S > 0,
          "timing banks only the reset")
    check("A2e FIX: lift_axis is now sized on all 6400 cells",
          lift["cells_lifted"] == s6.CELLS, f"cells_lifted={lift['cells_lifted']}")
    check("A2f FIX: G3 passes with a NEMA23-class motor (1.35x)",
          lift["passes"] and abs(lift["margin"] - 1.35) < 0.01,
          f"{lift['torque_needed_nm']} Nm vs {lift['motor_torque_nm']} Nm, {lift['margin']}x")
    # Historical sensitivity: at the OLD (wrong) 0.160 N/col release force the
    # gravity+pawl-only global load broke the NEMA17. After DND-97/A2 the pawl is
    # 8x softer (0.020 N), so this bound no longer holds -- which is exactly the
    # coupling that let DND-93 keep the global broadcast.
    tq_soft_old = _torque(s6.CELLS * 0.160, lead)
    tq_soft_new = _torque(s6.CELLS * s6.pawl_spring()["release_force_n"], lead)
    check("A2g historical: at the OLD 0.160 N/col the global load broke the NEMA17",
          tq_soft_old > old_motor, f"{tq_soft_old:.2f} Nm vs {old_motor} Nm")
    check("A2h FIX: at the corrected 0.020 N/col the load fits the NEMA17 "
          "(coupling that keeps the global broadcast viable)",
          tq_soft_new < old_motor, f"{tq_soft_new:.3f} Nm vs {old_motor} Nm")

    # --- Attack 1: cost headroom with honest allowances ----------------------
    print("[A1] Cost ladder honesty (allowances ADDED by DND-93)")
    b = s6.bom()
    added = 15.0 + 20.0 + 18.0 + 3.0 + 8.0 + 5.0
    old_parts = 139.77
    old_delivered = old_parts * s6.UPLIFT
    check("A1a historical base was $139.77 parts",
          abs(old_parts - 139.77) < 1e-9)
    check("A1b historical: +$69 allowances would give $242.17 delivered",
          abs((old_parts + added) * s6.UPLIFT - 242.17) < 0.02,
          f"{(old_parts + added) * s6.UPLIFT:.2f}")
    check("A1c FIX: model now carries the six allowance lines",
          sum(1 for r in b["lines"] if r["evidence"] == "allowance") == 6)
    check("A1d FIX: parts now $226.77 (allowances + NEMA23 lift)",
          abs(b["purchased_parts_usd"] - 226.77) < 1e-9, f"${b['purchased_parts_usd']}")

    # --- Attack 3: mask write is load-bearing, off the visible budget --------
    print("[A3] Mask-write product statement (bounded, unchanged)")
    ops = 3200 * (s6.LEVELS - 1)          # S1 holes-if-punch convention
    check("A3a serial punch is hopeless (>>30 s)",
          ops * 0.20 > 30.0 * 10, f"{ops * 0.20:.0f} s")
    check("A3b 30 s mask prep needs >400 ops/s",
          ops / 30.0 > 400.0, f"{ops / 30.0:.0f} ops/s")

    # --- Attack 3b: regional update is not bank-local ------------------------
    print("[A3b] Regional updates (bounded, unchanged)")
    check("A3b one global platen => all banks see every stroke",
          s6.timing()["strokes"] == 4 and s6.BANKS == 8)

    # --- Attack 4: per-cell reliability roll ---------------------------------
    print("[A4] No per-cell feedback / reliability (bounded, unchanged)")
    p = 1e-4
    p_all = (1 - p) ** s6.CELLS
    check("A4a at 0.01% per-cell error P(all 6400 correct) ~= 52.7%",
          abs(p_all - 0.527) < 0.01, f"{p_all:.4f}")
    check("A4b project goal q=1.57e-6 gives >=99%",
          (1 - 1.57e-6) ** s6.CELLS >= 0.99)

    # --- Attack 5: release-force ceiling provenance -------------------------
    print("[A5] Release-force ceiling provenance (FIXED by DND-93)")
    # Historical: S1's banked output (0.37 N/cell x 800) was reused as a "ceiling".
    s1_per_cell = 0.37
    check("A5a historical: 0.37 N x 800 == the old '296 N ceiling'",
          abs(s1_per_cell * s6.CELLS_PER_BANK - 296.0) < 1.0)
    check("A5b FIX: the ceiling is no longer hard-coded 296 N",
          s6.release_force()["banked_ceiling_n"] != 296.0,
          f"{s6.release_force()['banked_ceiling_n']} N")
    check("A5c FIX: the ceiling is an independent comb-tooth bending limit",
          "CALCULATION" in s6.release_force()["banked_ceiling_evidence"])
    check("A5d historical: S1 un-banked all-armed exceeded its 1500 N cap",
          s1_per_cell * s6.CELLS > 1500.0, f"{s1_per_cell * s6.CELLS:.0f} N")

    # --- Attack 6: timing omits mask index (FIXED) ---------------------------
    print("[A6] Timing completeness (FIXED by DND-93)")
    tm = s6.timing()
    check("A6a FIX: mask-index term is now priced", tm["mask_index_s"] > 0.0)
    check("A6b FIX: carriage-traverse term is now priced",
          tm["carriage_traverse_s"] > 0.0)
    check("A6c full map still passes 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")

    # --- Attack 7: pawl cam-out threshold ------------------------------------
    print("[A7] Pawl load holding (bounded, unchanged)")
    k = s6.pawl_spring()["rate_n_per_mm"]
    pocket = 0.80
    check("A7a lateral force to cam the toe out is < 1 N",
          k * pocket < 1.0, f"{k * pocket:.3f} N")

    # --- Corrected verdict ----------------------------------------------------
    print("[V] Corrected gate result (DND-93 + DND-97)")
    dec = s6.decide()
    check("V1 G3 passes on the global board", dec["gates"]["G3_lift_axis_torque"])
    check("V2 G6 delivered convention is over the line (honest)",
          not dec["gates"]["G6_cost_under_250_delivered"],
          f"${b['delivered_usd']} vs $250")
    check("V3 G5 mission gate (purchased parts) PASSES", dec["mission_gate_pass"],
          f"${dec['parts_usd']}")
    check("V4 all mission gates pass (G1-G5, G7)", dec["all_mission_gates_pass"])
    check("V5 verdict reflects the mission gate + reliability measurement gate",
          dec["verdict"] == "PROMOTE_TO_09_WITH_MEASUREMENT_GATE", dec["verdict"])

    # --- Evidence-class -------------------------------------------------------
    print("[A8] Evidence-class")
    check("A8 every S6-LC gate is CALCULATION/CAD (no print/measurement)",
          "no print" in s6.decide()["evidence_class"])

    print("=" * 40)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("Audit arithmetic reproduces and the DND-93 fix is asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
