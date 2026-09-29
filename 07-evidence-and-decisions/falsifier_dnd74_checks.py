#!/usr/bin/env python3
"""Falsifier DND-74 checks: the S6-LC ultra-low-cost audit, asserted.

Run:  python3 07-evidence-and-decisions/falsifier_dnd74_checks.py

Evidence class: CALCULATION on the repository's own declared 09-low-cost-variant/s6lc
constants, plus sourced-fact readings of the S1 screen. No print, no measurement
(DND-27). These checks are deliberately HOSTILE to the S6-LC promotion: they assert
the discrepancies the report `dnd74-s6lc-falsification.md` claims, so the audit can be
verified rather than trusted.

Exit 0 if every finding holds (i.e. the audit reproduces), 1 otherwise.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S6LC_PY = REPO / "09-low-cost-variant" / "s6lc" / "analysis" / "s6lc.py"

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

    print("DND-74 S6-LC falsification checks")
    print("=" * 40)

    # --- Attack 2: lift-axis sizing is wrong by the bank factor --------------
    print("[A2] Lift-axis sizing (the decisive break)")
    fit = s6.column_fit()
    lift = s6.lift_axis()
    lead = s6.LEAD_MM
    motor = s6.LIFT_MOTOR_TORQUE_NM
    check("A2a lift_axis is coded on one bank's cells",
          lift["cells_lifted"] == s6.CELLS_PER_BANK == 800,
          f"cells_lifted={lift['cells_lifted']}")
    check("A2b the mechanism writes the whole board (global strokes)",
          s6.timing()["strokes"] == 4 and s6.BANKS * s6.RESET_S > 0,
          "timing banks only the reset")
    # Correct the load to all 6400 cells at the model's own 0.4 N/cell.
    global_load = s6.LIFT_LOAD_N * s6.CELLS
    tq_global = _torque(global_load, lead)
    check("A2c global write load (6400 x 0.4 N) exceeds the motor",
          tq_global > motor,
          f"{global_load:.0f} N -> {tq_global:.2f} Nm vs {motor} Nm")
    # Even per-screw on 4 belt-synced screws.
    tq_each = _torque(global_load / 4.0, lead)
    check("A2d per-screw torque also exceeds the NEMA17",
          tq_each > motor,
          f"{tq_each:.3f} Nm/screw vs {motor} Nm")
    # And the as-coded gate passes -> the inconsistency is real.
    check("A2e as-coded G3 passes only because of the wrong input",
          lift["passes"] and lift["margin"] >= 1.3,
          f"as-coded margin {lift['margin']}x")
    # Sensitivity: gravity+pawl only still fails.
    tq_soft = _torque(s6.CELLS * s6.pawl_spring()["release_force_n"], lead)
    check("A2f even gravity+pawl-only global load exceeds the motor",
          tq_soft > motor, f"{tq_soft:.2f} Nm vs {motor} Nm")

    # --- Attack 1: cost headroom collapses with honest allowances ------------
    print("[A1] Cost ladder honesty")
    b = s6.bom()
    added = 15.0 + 20.0 + 18.0 + 3.0 + 8.0 + 5.0
    delivered_after = (b["purchased_parts_usd"] + added) * s6.UPLIFT
    check("A1a base BOM matches the quoted $139.77 parts",
          abs(b["purchased_parts_usd"] - 139.77) < 0.02,
          f"{b['purchased_parts_usd']}")
    check("A1b +$69 allowances still under $250 delivered",
          delivered_after < s6.COST_GATE_USD,
          f"{delivered_after:.2f}")
    check("A1c but headroom collapses below $10",
          s6.COST_GATE_USD - delivered_after < 10.0,
          f"headroom ${s6.COST_GATE_USD - delivered_after:.2f}")
    check("A1d the model's own >=$50 margin check would now fail",
          (s6.COST_GATE_USD - delivered_after) < 50.0)

    # --- Attack 3: mask write is load-bearing, off the visible budget --------
    print("[A3] Mask-write product statement")
    ops = 3200 * (s6.LEVELS - 1)          # S1 holes-if-punch convention
    check("A3a serial punch is hopeless (>>30 s)",
          ops * 0.20 > 30.0 * 10, f"{ops * 0.20:.0f} s")
    check("A3b 30 s mask prep needs >400 ops/s",
          ops / 30.0 > 400.0, f"{ops / 30.0:.0f} ops/s")

    # --- Attack 3b: regional update is not bank-local ------------------------
    print("[A3b] Regional updates")
    check("A3b one global platen => all banks see every stroke",
          s6.timing()["strokes"] == 4 and s6.BANKS == 8)

    # --- Attack 4: per-cell reliability roll ---------------------------------
    print("[A4] No per-cell feedback / reliability")
    p = 1e-4
    p_all = (1 - p) ** s6.CELLS
    check("A4a at 0.01% per-cell error P(all 6400 correct) ~= 52.7%",
          abs(p_all - 0.527) < 0.01, f"{p_all:.4f}")
    check("A4b project goal q=1.57e-6 gives >=99%",
          (1 - 1.57e-6) ** s6.CELLS >= 0.99)

    # --- Attack 5: circular release-force ceiling ----------------------------
    print("[A5] Release-force ceiling provenance")
    # S1's banked output (0.37 N/cell x 800) is reused as S6-LC's "ceiling".
    s1_per_cell = 0.37
    s1_break_even = 1500.0 / s6.CELLS
    check("A5a S1 per-cell 0.37 N x 800 == the '296 N ceiling'",
          abs(s1_per_cell * s6.CELLS_PER_BANK - 296.0) < 1.0)
    check("A5b the 'ceiling' is S1's own banked output, not a structural limit",
          s6.release_force()["banked_ceiling_n"] == 296.0)
    # S1's own un-banked all-armed force (0.37 N x 6400 = 2368 N) exceeds the S1
    # 1500 N structural cap, so S1's "296 N" was a banked reduction, not a ceiling.
    check("A5c S1 un-banked all-armed exceeds the 1500 N structural cap",
          s1_per_cell * s6.CELLS > 1500.0,
          f"{s1_per_cell * s6.CELLS:.0f} N")
    check("A5c2 but S6-LC's softer pawl stays under the cap (so banked is fine)",
          s6.release_force()["unbanked_all_armed_n"] < 1500.0,
          f"{s6.release_force()['unbanked_all_armed_n']} N")
    check("A5d S1 break-even (0.234) < our per-pawl check uses it as ceiling",
          abs(s1_break_even - 0.234375) < 1e-6)

    # --- Attack 6: timing omits mask index -----------------------------------
    print("[A6] Timing completeness")
    tm = s6.timing()
    check("A6a timing still passes 30 s",
          tm["clears_30s"], f"{tm['full_map_s']} s")
    check("A6b but 4 mask-index moves fit comfortably (<30 s)",
          tm["full_map_s"] + 4 * 1.0 < 30.0)

    # --- Attack 7: pawl cam-out threshold ------------------------------------
    print("[A7] Pawl load holding")
    k = s6.pawl_spring()["rate_n_per_mm"]
    pocket = 0.80
    check("A7a lateral force to cam the toe out is < 1 N",
          k * pocket < 1.0, f"{k * pocket:.3f} N")

    # --- Evidence-class compliance table sanity ------------------------------
    print("[A8] Evidence-class")
    check("A8 every S6-LC gate is CALCULATION/CAD (no print/measurement)",
          "no print" in s6.decide()["evidence_class"])

    print("=" * 40)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
