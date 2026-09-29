"""CI gate for the DND-73 S6-LC BOM ratification.

Run: python s6lc_bom_ratify_checks.py
Stdlib only (imports the ratifier). Exit 0 if every check holds, 1 otherwise.

These checks fail if (a) the CTO headline stops reproducing, (b) the additive
x1.16 uplift changes, (c) a traced line is no longer cheaper than (or equal to)
the BOM figure, (d) any cost-driving line loses its >2x break-even headroom,
(e) the hostile scenario stops clearing the ceiling, (f) the honest
"hostile + shared card puncher breaks $250" finding is silently reversed, or
(g) the committed model / CSV / ADR drifts.
"""
from __future__ import annotations

import csv
from pathlib import Path

import s6lc_bom_ratify as r

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ADR = REPO / "07-evidence-and-decisions" / "dnd73-s6lc-bom-ratification.md"

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
    tr = res["trace"]
    be = res["break_even"]
    s = res["scenarios"]
    h = res["hostile"]

    print("DND-73 S6-LC BOM ratification checks")
    print("=" * 36)

    print("[1] Claim reproduction (x1.16 additive basis, DND-41)")
    check("purchased parts reproduce $139.77", abs(rd["parts"] - 139.77) < 0.01,
          f"${rd['parts']}")
    check("delivered reproduces $162.13", abs(rd["delivered"] - 162.13) < 0.01,
          f"${rd['delivered']}")
    check("margin to $250 is $87.87", abs(rd["margin"] - 87.87) < 0.01,
          f"${rd['margin']}")
    check("claim_reproduces flag", rd["claim_reproduces"])
    check("uplift is the additive 1.16 (not compounded)", rd["uplift_is_additive"])

    print("[2] Evidence-class audit (a finding, pinned)")
    check("traced + allowance = parts",
          abs(ev["traced_usd"] + ev["allowance_usd"] - rd["parts"]) < 0.01, ev)
    check("traced share > 30%", ev["traced_share"] > 0.30, ev)
    check("allowance share is disclosed (56% un-traced)", ev["allowance_usd"] > 0.0, ev)
    check("spares line is labelled `assumption`",
          any(l[0].startswith("Spares") and l[3] == "assumption"
              for l in r.CLAIMED_LINES))

    print("[3] Traced critical lines against the BOM unit")
    for item, t in tr.items():
        # The lift motor is the one line whose cheapest torque-matched listing
        # is $0.39 ABOVE the $12 BOM allowance (a small, honest finding). Every
        # other traced line is at or below its BOM unit. Allow <= $0.50 over for
        # the motor, exact-or-under for the rest.
        over = t["cheapest_unit"] - t["bom_unit"]
        allowed = 0.50 if "Lift motor" in item else 0.0
        check(f"traced {item[:38]} <= BOM unit (+ tolerance)",
              over <= allowed, f"over ${over:.2f}")
    check("every traced row carries an http URL and evidence class",
          all(row["url"].startswith("http")
              and row["evidence"] in ("SOURCED-LIVE", "UNVERIFIED-MARKETPLACE")
              for t in tr.values() for row in t["trace"]))

    print("[4] Break-even headroom per cost-driving line")
    check("parts headroom > $50", be["parts_headroom"] > 50.0, be)
    check("delivered headroom > $60", be["delivered_headroom"] > 60.0, be)
    for item, v in be["per_line"].items():
        check(f"{item[:38]} break-even > 2x BOM unit",
              v["be_unit"] > v["bom_unit"] and (v["multiple"] or 0) > 2.0, v)

    print("[5] Scenarios")
    check("all scenarios clear the $250 delivered ceiling", s["all_clear_ceiling"], s)
    check("optimistic < working < high < hostile",
          s["optimistic_usd"] <= s["working_usd"] <= s["high_usd"]
          <= s["hostile_usd"], s)
    check("working scenario == committed model delivered (162.13)",
          abs(s["working_usd"] - 162.13) < 0.01, s)
    check("hostile scenario still clears ($243.45)",
          s["hostile_clears"], s)

    print("[6] Honest finding: off-BOM shared tool")
    check("hostile + shared card puncher BREACHES $250 (finding)", 
          not h["with_puncher_clears"], h)
    check("breach margin is negative and pinned",
          h["with_puncher_margin"] < 0.0, h)
    check("printed parts are excluded by the requirement (not a hidden cost)",
          h["printed_parts_excluded_by_requirement"])

    print("[7] Reconciliation with the committed model + CSV")
    rec = r.reconcile_with_committed()
    check("s6lc.bom() parts == re-derivation", abs(rec["model_parts"] - rd["parts"]) < 0.01, rec)
    check("s6lc.bom() delivered == re-derivation",
          abs(rec["model_delivered"] - rd["delivered"]) < 0.01, rec)
    check("s6lc.model uplift == 1.16", abs(rec["model_uplift"] - r.UPLIFT) < 1e-9, rec)
    check("s6lc model has 3 bought actuators", rec["model_actuators"] == 3, rec)
    csvr = r.reconcile_with_csv()
    check("bom_s6lc.csv parts == re-derivation", abs(csvr["csv_parts"] - rd["parts"]) < 0.01, csvr)
    check("bom_s6lc.csv has 14 purchased lines", csvr["csv_rows"] == 14, csvr)

    print("[8] Emitted ratified CSV artifact is consistent")
    out = Path(r.emit_bom_csv())
    check("ratified CSV exists", out.exists(), str(out))
    rows = list(csv.DictReader(out.open(newline="")))
    body = [x for x in rows if not x["item"].startswith(("TOTAL", "scenario"))]
    total = [x for x in rows if x["item"].startswith("TOTAL")][0]
    check("CSV body parts sum == TOTAL",
          abs(round(sum(float(x["parts_usd"]) for x in body), 2)
              - float(total["parts_usd"])) < 0.05)
    check("CSV TOTAL delivered == $162.13",
          abs(float(total["delivered_usd"]) - 162.13) < 0.01, total)
    check("CSV labels the card-puncher breach in the scenario reference",
          any("266.65" in x.get("trace_note", "") for x in rows))

    print("[9] ADR document carries the decisive numbers")
    check("ADR exists", ADR.exists(), str(ADR))
    if ADR.exists():
        text = ADR.read_text()
        for token in ("DND-73", "139.77", "162.13", "1.16", "87.87",
                      "215.52", "allowance", "RATIFIED", "266.65", "S6-LC"):
            check(f"ADR contains {token!r}", token in text)

    print("=" * 36)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
