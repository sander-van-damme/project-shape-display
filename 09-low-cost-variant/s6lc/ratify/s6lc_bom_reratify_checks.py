#!/usr/bin/env python3
"""CI gate for the DND-98 S6-LC purchased-BOM re-ratification.

Run: python s6lc_bom_reratify_checks.py
Stdlib only (imports the re-ratifier). Exit 0 if every check holds, 1 otherwise.

These checks fail if (a) the DND-93 corrected headline stops reproducing,
(b) the additive x1.16 uplift changes, (c) the <$250 PURCHASED mission gate
stops holding or starts being confused with the delivered convention, (d) a
cost-driving line loses its break-even headroom, (e) the hostile scenario
silently starts clearing (or stops breaching) the purchased ceiling, (f) the
A5 capability allowance stack changes size, (g) the "no per-cell bought
hardware" fact drifts, (h) the reliability break-even moves, or (i) the
committed model / CSV / ADR drifts.
"""
from __future__ import annotations

from pathlib import Path

import s6lc_bom_reratify as r

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ADR = REPO / "07-evidence-and-decisions" / "dnd98-s6lc-bom-reratification.md"

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


def main() -> int:
    res = r.run()
    rd = res["rederivation"]
    ev = res["evidence"]
    dl = res["delta"]
    v = res["verdict"]
    be = res["break_even"]
    s = res["scenarios"]
    pc = res["per_cell"]
    rl = res["reliability"]

    print("DND-98 S6-LC BOM re-ratification checks")
    print("=" * 40)

    print("[1] Corrected claim reproduction (x1.16 additive basis, DND-41)")
    check("purchased parts reproduce $226.77", abs(rd["parts"] - 226.77) < 0.01,
          f"${rd['parts']}")
    check("delivered reproduces $263.05", abs(rd["delivered"] - 263.05) < 0.01,
          f"${rd['delivered']}")
    check("claim_reproduces flag", rd["claim_reproduces"])
    check("uplift is the additive 1.16 (not compounded)", rd["uplift_is_additive"])

    print("[2] Ceiling verdict (the DND-70 mission gate is the PURCHASED figure)")
    check("purchased parts clear $250", v["purchased_clears"], f"${v['purchased_parts']}")
    check("purchased margin is $23.23", abs(v["purchased_margin"] - 23.23) < 0.01,
          f"${v['purchased_margin']}")
    check("mission gate (purchased) HOLDS", v["mission_gate_holds"])
    check("delivered does NOT clear $250 (honest overrun)",
          not v["delivered_clears"], f"${v['delivered']}")
    check("delivered overrun is $13.05", abs(v["delivered_margin"] + 13.05) < 0.01,
          f"${v['delivered_margin']}")
    check("repo delivered convention does NOT hold",
          not v["repo_delivered_convention_holds"])
    check("parts to shed for the delivered convention is $11.25",
          abs(v["shed_needed_parts_to_clear_delivered"] - 11.25) < 0.01,
          v["shed_needed_parts_to_clear_delivered"])

    print("[3] Evidence-class audit + DND-73 -> DND-93 delta")
    check("traced + allowance reconciles to parts",
          abs(ev["traced_usd"] + ev["allowance_usd"] - rd["parts"]) < 0.01, ev)
    check("A5 capability allowances are $69.00",
          abs(ev["a5_capability_usd"] - 69.00) < 0.01, f"${ev['a5_capability_usd']}")
    check("traced share is a credible minority (<50%)",
          ev["traced_share"] < 0.5, ev["traced_share"])
    check("parts growth since DND-73 is $87.00",
          abs(dl["growth"] - 87.00) < 0.01, f"${dl['growth']}")
    check("six new A5 lines total $69.00",
          abs(dl["new_lines_usd"] - 69.00) < 0.01, f"${dl['new_lines_usd']}")
    check("NEMA17 -> NEMA23 re-price delta is $18.00",
          abs(dl["repriced_usd"] - 18.00) < 0.01, f"${dl['repriced_usd']}")

    print("[4] Break-even unit prices for the $250 PURCHASED ceiling")
    check("purchased headroom $23.23", abs(be["parts_headroom"] - 23.23) < 0.01,
          f"${be['parts_headroom']}")
    for item, vv in be["per_line"].items():
        check(f"{item[:38]:38s} cap > BOM", vv["be_unit"] > vv["bom_unit"], (item, vv))
    check("tightest line is the NEMA23 lift motor",
          be["tightest_item"] == "Lift motor (NEMA23-class stepper)",
          be["tightest_item"])
    check("tightest multiplier is 1.77x", abs(be["tightest_multiple"] - 1.77) < 0.01,
          be["tightest_multiple"])

    print("[5] Scenarios (on the PURCHASED mission gate; delivered reported)")
    check("scenario ordering opt<=work<=high<=hostile",
          s["optimistic_parts"] <= s["working_parts"] <= s["high_parts"]
          <= s["hostile_parts"], s)
    check("optimistic clears $250 purchased", s["optimistic_clears_parts"],
          f"${s['optimistic_parts']}")
    check("working clears $250 purchased", s["working_clears_parts"],
          f"${s['working_parts']}")
    check("high clears $250 purchased", s["high_clears_parts"],
          f"${s['high_parts']}")
    check("lean clears $250 purchased", s["lean_clears_parts"],
          f"${s['lean_parts']}")
    check("HOSTILE BREACHES $250 purchased (the honest finding)",
          not s["hostile_clears_parts"], f"${s['hostile_parts']}")
    check("hostile margin is -$50.58",
          abs(s["hostile_purchased_margin"] + 50.58) < 0.01,
          f"${s['hostile_purchased_margin']}")
    check("not all scenarios clear purchased", not s["all_clear_purchased"])
    check("working FAILS $250 delivered", not s["working_clears_delivered"],
          f"${s['working_usd']}")

    print("[6] Per-cell bought-hardware sensitivity")
    check("no per-cell bought hardware", pc["per_cell_bought_parts"] == 0, pc)
    check("three bought actuators only", pc["bought_actuators"] == 3, pc)
    check("purchased headroom is positive", pc["purchased_headroom_usd"] > 0, pc)
    check("cost per cell is 3.5433 cents",
          abs(pc["cents_per_cell_total"] - 3.5433) < 0.01, pc["cents_per_cell_total"])

    print("[7] Reliability / assembly scaling")
    check("99% map break-even q is ~1.57e-6",
          abs(rl["per_cell_error_break_even"] - 1.57e-6) < 1e-7, rl)
    check("q=1e-4 yields ~52.7% map (reliability is demanding)",
          abs(rl["rows"][1]["map_yield"] - 0.5273) < 0.01, rl["rows"][1])
    check("bank sub-tile replacement strategy is stated",
          "bank sub-tile" in rl["replace_strategy"].lower())

    print("[8] Reconciliation with the committed model / CSV / ADR")
    rec = r.reconcile_with_committed()
    check("model parts == ratified parts", abs(rec["model_parts"] - rd["parts"]) < 0.01, rec)
    check("model delivered == ratified delivered",
          abs(rec["model_delivered"] - rd["delivered"]) < 0.01, rec)
    check("model uplift == 1.16", abs(rec["model_uplift"] - r.UPLIFT) < 1e-9, rec)
    check("model bought actuators == 3", rec["model_actuators"] == 3, rec)
    check("model clears parts, not delivered",
          rec["model_clears_parts"] and not rec["model_clears_delivered"], rec)
    csvr = r.reconcile_with_csv()
    check("CSV parts == ratified parts", abs(csvr["csv_parts"] - rd["parts"]) < 0.01, csvr)
    check("CSV has 20 lines", csvr["csv_rows"] == 20, csvr)
    check("ADR exists", ADR.exists(), str(ADR))
    if ADR.exists():
        body = ADR.read_text()
        check("ADR states $226.77", "226.77" in body)
        check("ADR states the purchased gate HOLDS", "HOLD" in body or "holds" in body)
        check("ADR states delivered overrun $263.05", "263.05" in body)
    check("ratified CSV exists", (HERE / "s6lc_bom_ratified.csv").exists())

    print("=" * 40)
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"{CHECKS}/{CHECKS} checks passed")
    print("DND-98: corrected S6-LC purchased BOM re-ratified; <$250 PURCHASED holds "
          "($226.77), delivered convention fails ($263.05) -- both stated, not hidden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
