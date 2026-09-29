"""DND-75 checks for the divergent ultra-low-cost screen (`divergent_lowcost.py`).

CI-style assertions (same convention as `s5r_ultra_checks.py`). Each check
prints PASS/FAIL and exits non-zero if any fails. These pin the DND-75 headline
so it cannot drift:

- the DND-72 baseline reproduces ($218.70 base / $253.69 delivered / $404.60);
- the attacked base lines total $177.00 and leave only $41.70 retained;
- all three divergent candidates land under $250 delivered AND under 30 s;
- the substitute-line audit adds REAL lines and every deleted line has a
  substitute (no accounting trick);
- A1's single-motor camshaft gate is reported honestly as FAILING at 0.30 Nm;
- A3 needs 4 banks (not test11's 8) to clear both gates.

Evidence class: CALCULATION over the promoted model + sourced-class allowances
(DND-27). No print, no purchase, no measurement.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import divergent_lowcost as d  # noqa: E402

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    (PASSES if cond else FAILS).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def main() -> int:
    base = d.base_floor()
    s = d.screen()

    # --- Baseline cannot drift ------------------------------------------------
    check("C1 S6-LC fixed base = $218.70 parts", base["s6lc_base_parts_usd"] == 218.70,
          f"parts={base['s6lc_base_parts_usd']}")
    check("C2 S6-LC base delivered = $253.69 (> $250)",
          base["s6lc_base_delivered_usd"] == 253.69,
          f"delivered={base['s6lc_base_delivered_usd']}")
    check("C3 attacked lines total $177.00", base["attacked_lines_usd"] == 177.00,
          f"attacked={base['attacked_lines_usd']}")
    check("C4 retained base after attack = $41.70",
          base["retained_lines_usd"] == 41.70, f"retained={base['retained_lines_usd']}")

    # --- Attack legitimacy ----------------------------------------------------
    audit = s["attack_audit"]
    check("C5 every attacked line has a listed substitute",
          audit["every_line_has_substitute"] is True,
          f"missing={audit['missing_substitute']}")
    check("C6 all ten functional jobs answered by each candidate",
          all(len(getattr(d, a)["allocation"]) >= 10 for a in ("A1", "A2", "A3")),
          "A1/A2/A3 each allocate >=10 jobs")

    # --- Cost + timing gates --------------------------------------------------
    check("C7 A1 under $250 and under 30 s",
          d.A1["bom"]["delivered_usd"] < 250.0 and d.A1["timing"]["clears_30s"],
          f"${d.A1['bom']['delivered_usd']} / {d.A1['timing']['full_map_s']} s")
    check("C8 A2 under $250 and under 30 s",
          d.A2["bom"]["delivered_usd"] < 250.0 and d.A2["timing"]["clears_30s"],
          f"${d.A2['bom']['delivered_usd']} / {d.A2['timing']['full_map_s']} s")
    check("C9 A3 under $250 and under 30 s",
          d.A3["bom"]["delivered_usd"] < 250.0 and d.A3["timing"]["clears_30s"],
          f"${d.A3['bom']['delivered_usd']} / {d.A3['timing']['full_map_s']} s")

    # --- Honest substitute lines keep them under $250 -------------------------
    for a in ("A1", "A2", "A3"):
        ws = d.candidate_with_substitutes(getattr(d, a))
        check(f"C10.{a} still under $250 after substitute lines",
              ws["under_250"] is True,
              f"delivered=${ws['delivered_usd']} (+${ws['substitute_parts_usd']} subs)")

    # --- Hostile findings are recorded, not hidden ----------------------------
    check("C11 A1 single-motor camshaft gate FAILS at 0.30 Nm (honest)",
          d.A1["force_gate"]["pass_gate"] is False,
          f"peak={d.A1['force_gate']['phased_peak_torque_nm']} Nm")
    check("C12 A1 is robust: a 2nd/stronger motor keeps it under $250",
          d.A1["motor_break_even"]["verdict_two_motor"] == "UNDER_$250",
          f"two-motor delivered=${d.A1['motor_break_even']['two_motor_option_delivered_usd']}")

    # --- A3 bank correction ---------------------------------------------------
    sweep = {r["banks"]: r for r in d.A3["bank_sweep"]}
    check("C13 A3 8 banks FAILS 30 s (test11's prescription)",
          sweep[8]["clears_30s"] is False, f"8-bank time={sweep[8]['full_map_s']} s")
    check("C14 A3 4 banks clears BOTH gates (the correction)",
          sweep[4]["both_ok"] is True,
          f"4-bank time={sweep[4]['full_map_s']} s force={sweep[4]['per_bank_release_force_n']} N")

    # --- Headline -------------------------------------------------------------
    check("C15 all three candidates under $250", s["verdict"]["all_three_under_250"] is True)
    check("C16 best divergent cost beats S6-LC's $253.69 base floor",
          s["verdict"]["best_cost_delivered_usd"] < d.S6LC_BASE_DELIVERED,
          f"best=${s['verdict']['best_cost_delivered_usd']}")

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
