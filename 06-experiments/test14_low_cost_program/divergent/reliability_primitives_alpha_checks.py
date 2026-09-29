"""DND-106 checks for the reliability-first cell/mask primitives
(`reliability_primitives_alpha.py`).

CI-style assertions (same convention as `primitives_checks.py` and
`s6lc_checks.py`). Each check prints PASS/FAIL and exits non-zero if any fails.
These pin the DND-106 headline so it cannot drift:

- the correlation arithmetic (6,400 -> 80 decisions = 80x looser q) is exact;
- all three primitives R1/R2/R3 pass the FULL reliability-audit schema (no
  missing field, no unanswered functional job);
- the three primitives are materially different families;
- the zero-bought-parts claim for R1/R2 and the tiny R3 delta are reported;
- the machine clears < 30 s on the honest visible budget;
- R4 (shared return bar) is recorded as a REJECTED negative result;
- the decisive falsifier and coupon test exist for every primitive.

Evidence class: CALCULATION over sourced FDM limits (DND-27). No print, no
purchase, no measurement.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import reliability_primitives_alpha as r  # noqa: E402

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    (PASSES if cond else FAILS).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}"
          + (f" -- {detail}" if detail else ""))


def main() -> int:
    lesson = r.correlated_uniformity_lesson()
    s = r.screen()

    # --- the reliability arithmetic cannot drift -----------------------------
    check("C1 cells = 6,400", lesson["cells"] == 6400, f"{lesson['cells']}")
    check("C2 per-cell q break-even for 99% map = 1.57e-6",
          abs(lesson["q_per_cell_break_even_99"] - 1.57e-6) < 1e-8,
          f"{lesson['q_per_cell_break_even_99']}")
    check("C3 per-row q break-even is 80x looser",
          abs(lesson["row_vs_cell_looseness"] - 80.0) < 0.5,
          f"{lesson['row_vs_cell_looseness']}x")
    check("C4 per-bank q break-even is ~800x looser",
          abs(lesson["bank_vs_cell_looseness"] - 799.5) < 2.0,
          f"{lesson['bank_vs_cell_looseness']}x")

    # --- the audit schema is fully answered by all three primitives ----------
    for pid in ("R1", "R2", "R3"):
        a = s[pid]
        check(f"C5.{pid} reliability audit complete (no missing field)",
              a["missing_fields"] == [], f"missing={a['missing_fields']}")
        check(f"C6.{pid} all functional jobs answered",
              a["unanswered_jobs"] == [], f"missing={a['unanswered_jobs']}")
        check(f"C7.{pid} has a decisive falsifier",
              bool(a["decisive_falsifier"]), "")
        check(f"C8.{pid} has a 3x1 / 5x5 coupon test",
              bool(a["coupon_test"]), "")
        check(f"C9.{pid} states what must work 6,400 times",
              bool(a["what_must_work_6400_times"]), "")

    # --- materially different families ---------------------------------------
    fams = {s[pid]["family"] for pid in ("R1", "R2", "R3")}
    check("C10 three materially different families", len(fams) == 3,
          f"{sorted(fams)}")

    # --- the reliability reduction is real -----------------------------------
    fa = r.r1_failure_arithmetic()
    check("C11 R1 cuts 6,400 decisions to 80 (80x)",
          fa["repeated_moving_decisions"] == 80 and fa["decision_reduction"] == 80.0,
          f"{fa['repeated_moving_decisions']} decisions, "
          f"{fa['decision_reduction']}x")

    # --- the A8 gravity-drop failure class is removed ------------------------
    rp = r.r2_reset_positive()
    check("C12 R2 reset is a DRIVEN positive stop (not gravity release)",
          "pushes" in rp["r2_reset"], rp["r2_reset"][:60])

    # --- bought delta: zero for R1/R2, tiny for R3 ---------------------------
    bd = r.bom_delta()
    check("C13 bought delta <= $5 and no per-cell bought hardware",
          bd["bought_delta_usd"] <= 5.0 and bd["per_cell_bought_hardware"] == 0,
          f"${bd['bought_delta_usd']}")

    # --- timing gate (assumption-class, honest) ------------------------------
    tm = s["timing"]
    check("C14 full-map visible transition < 30 s",
          tm["clears_30s"] is True, f"{tm['full_map_visible_s']} s")
    check("C15 read pass reported separately (not hidden in the visible budget)",
          tm["read_pass_in_visible_budget"] is False,
          f"read pass {tm['read_pass_s']} s reported separately")

    # --- the rejected idea is recorded as evidence ---------------------------
    check("C16 R4 shared return bar recorded REJECTED as evidence",
          s["R4_rejected"]["verdict"] == "REJECTED"
          and s["R4_rejected"]["recorded_as_evidence"] is True, "")

    # --- pitch / printability geometry ---------------------------------------
    g1 = r.r1_geometry()
    g2 = r.r2_geometry()
    check("C17 R1 step/arm are 2-line/3-line printable",
          g1["printable"] is True and g1["tooth_load_margin"] >= 3.0,
          f"tooth margin {g1['tooth_load_margin']}x")
    check("C18 R2 gate is 2-line with a worst-case running clearance >= 0.10 mm",
          g2["gate_is_2line"] is True and g2["clearance_pass"] is True,
          f"clearance {g2['worst_case_running_clearance_mm']} mm")

    # --- decisions -----------------------------------------------------------
    dec = s["decision"]
    check("C19 all reliability-audit gates pass",
          all(dec["gates"].values()), f"{dec['gates']}")
    check("C20 exactly three primitives conform and none failed",
          dec["primitives_conforming"] == ["R1", "R2", "R3"]
          and dec["primitives_failed_conformance"] == [], "")

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
