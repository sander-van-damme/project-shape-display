"""DND-72 checks for the ultra-low-cost S5-R variant screen (`s5r_ultra.py`).

CI-style assertions (same convention as `s5r_register_checks.py`): each check
prints PASS/FAIL and the process exits non-zero if any check fails. These pin
the DND-72 headline so it cannot drift:

- the S5-R promoted BOM still reproduces $404.60 delivered / 24.615 s;
- the fixed no-channel base is $218.70 parts -> $253.69 delivered, i.e. it
  ALONE exceeds the $250 delivered target;
- no (R, writers, bank-motors) point under $250 clears the 30 s gate;
- the exhaustive requirement-preserving floor is ~$345.90 (R6-W20-M2) and is
  under the mission's own $500 ceiling;
- the verdict is INFEASIBLE_UNDER_UNCHANGED_REQUIREMENTS and the relaxation
  ladder names the base as the binding term.

Evidence class: CALCULATION over the promoted model + sourced listings
(DND-27). No print, no purchase, no measurement.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_T12 = HERE.parent / "06-experiments" / "test12_winner_convergence"
if str(_T12) not in sys.path:
    sys.path.insert(0, str(_T12))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import s5r_register as s5r  # noqa: E402
import s5r_ultra as u  # noqa: E402

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    (PASSES if cond else FAILS).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def main() -> int:
    base = u.fixed_base()
    scan = u.budget_scan()
    floor = u.cheapest_requirement_preserving()
    dec = u.decide()
    ladder = dec["relaxation_ladder"]

    # --- Control: the promoted S5-R is untouched and still reproduces. --------
    s5r_bom = s5r.bom(s5r.ROWS_IN_BANK)
    check("C1 S5-R control: $404.60 delivered",
          s5r_bom["delivered_usd"] == 404.60,
          f"delivered_usd={s5r_bom['delivered_usd']}")
    s5r_tm = s5r.timing(s5r.ROWS_IN_BANK)
    check("C2 S5-R control: 24.615 s full map",
          s5r_tm["full_map_s5r_s"] == 24.615,
          f"full_map_s={s5r_tm['full_map_s5r_s']}")

    # --- The binding fact: the fixed base alone busts the target. ------------
    check("C3 fixed base parts = $218.70",
          base["parts_usd"] == 218.70, f"parts={base['parts_usd']}")
    check("C4 fixed base delivered = $253.69 (> $250 target)",
          base["delivered_usd"] == 253.69,
          f"delivered={base['delivered_usd']}")
    check("C5 fixed base ALONE exceeds the $250 target",
          base["base_alone_exceeds_target"] is True,
          f"overshoot=${base['overshoot_usd']}")
    check("C6 actuator headroom at the base is NEGATIVE (no room for any actuator)",
          base["actuator_headroom_parts_usd"] < 0.0,
          f"headroom=${base['actuator_headroom_parts_usd']} parts")

    # --- The search: no sub-$250 point exists; the 30 s point is the floor. --
    check("C7 no sub-$250 point exists in the whole lever space",
          scan["sub_250_points_exist"] is False,
          f"searched={scan['points_searched']}")
    check("C8 no sub-$250 point is also requirement-preserving",
          scan["sub_250_and_requirement_preserving_exist"] is False,
          f"count={scan['sub_250_viable_count']}")
    c30 = scan["cheapest_point_clearing_30s"]
    check("C9 an in-budget (<30 s) point exists and is the cost floor",
          c30 is not None and c30["all_requirements_preserved"] is True,
          f"id={c30['id']} delivered=${c30['delivered_usd']} t={c30['full_map_s']}s")
    check("C10 the cheapest <30 s point is over $250",
          c30 is not None and c30["delivered_usd"] > 250.0,
          f"delivered=${c30['delivered_usd']}")

    # --- Break-even. ---------------------------------------------------------
    check("C11 requirement-preserving floor found",
          floor.get("found") is True, f"id={floor.get('id')}")
    check("C12 floor = $345.90 (R6-W20-M2)",
          floor.get("delivered_usd") == 345.90 and floor.get("id") == "R6-W20-M2",
          f"id={floor.get('id')} delivered=${floor.get('delivered_usd')}")
    check("C13 floor clears < 30 s",
          floor.get("full_map_s", 99.0) < 30.0,
          f"full_map_s={floor.get('full_map_s')}")
    check("C14 floor clears the mission's own $500 ceiling",
          floor.get("delivered_usd", 1e9) < 500.0,
          f"margin_to_500=${floor.get('gap_to_500_usd')}")

    # --- Verdict + relaxation ladder. ---------------------------------------
    check("C15 verdict is INFEASIBLE_UNDER_UNCHANGED_REQUIREMENTS",
          dec["verdict"] == "INFEASIBLE_UNDER_UNCHANGED_REQUIREMENTS",
          dec["verdict"])
    check("C16 budget gap = $95.90 (~$96 too low)",
          dec["budget_gap_usd"] == 95.90, f"gap=${dec['budget_gap_usd']}")
    check("C17 base cut needed to reach $250 parts is small but nonzero",
          0.0 < ladder["base_cut_needed_to_reach_250_parts_usd"] < 5.0,
          f"cut=${ladder['base_cut_needed_to_reach_250_parts_usd']} "
          f"({ladder['base_cut_needed_pct_of_base']}% of base)")

    # --- Topology table sanity (the three named candidates must be shown). --
    topos = {t["id"]: t for t in u.topologies()}
    check("C18 promoted control topology present",
          "R4-W40-M2" in topos and topos["R4-W40-M2"]["cost"]["delivered_usd"] == 404.60)
    check("C19 cheapest named low-cost candidate fails 30 s or cost",
          all(not t["viable"] for t in u.topologies()),
          "no named topology is both <$250 and <30 s")

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
