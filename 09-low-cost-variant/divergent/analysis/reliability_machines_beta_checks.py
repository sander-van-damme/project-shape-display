"""DND-107 checks for the reliability-first machines (`reliability_machines_beta.py`).

CI-style assertions (same convention as `divergent_lowcost_checks.py`). Each
check prints PASS/FAIL and exits non-zero if any fails. These pin the DND-107
headline so it cannot drift:

- the imported S6-LC baseline reproduces ($263.05 delivered, 11.96 s);
- there are >= 2 materially different complete machines, and at least one is
  not a threshold-ratchet mask machine;
- B1 is reported as a FAILED candidate (timing-feasible and torque-feasible
  gang sets are disjoint) -- the honest negative result, not hidden;
- B2 clears cost + visible timing and has a positive blanket-force margin;
- B3 clears cost + visible timing and deletes the per-cell keeper (80 drum
  tracks instead of 6,400 keepers, an 80x reduction);
- every machine answers the DND-103 reliability audit fields;
- every machine reports an honest 7-stage timing decomposition.

Evidence class: CALCULATION over the promoted model + sourced-class allowances
(DND-27). No print, no purchase, no measurement.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import reliability_machines_beta as m  # noqa: E402

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    (PASSES if cond else FAILS).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def main() -> int:
    s = m.screen()
    gates = s["gates"]

    # --- Imported baseline cannot drift --------------------------------------
    check("C1 S6-LC delivered = $263.05", m.S6LC_DELIVERED == 263.05,
          f"{m.S6LC_DELIVERED}")
    check("C2 S6-LC full map = 11.96 s", m.S6LC_FULL_MAP_S == 11.96)
    check("C3 S6-LC base parts = $218.70 (imported)",
          m.S6LC_BASE_PARTS == 218.70)

    # --- Divergence requirement ----------------------------------------------
    check("C4 at least two complete machines", len(s["candidates"]) >= 2,
          f"{len(s['candidates'])}")
    check("C5 at least one NON-mask machine",
          any(not c["is_mask"] for c in s["candidates"]))
    check("C6 machines are materially different (one mask, one non-mask)",
          len({c["is_mask"] for c in s["candidates"]}) == 2)

    # --- B1 is honestly reported as FAILED -----------------------------------
    cg = m.B1["combined_gate"]
    check("C7 B1 as-drawn verdict = FAIL_AS_DRAWN",
          cg["result"] == "FAIL_AS_DRAWN")
    check("C8 B1 serial-row timing fails 30 s badly",
          cg["serial_s"] > 100.0, f"{cg['serial_s']} s")
    check("C9 every B1 timing-feasible point fails the torque gate",
          cg["timing_feasible_all_torque_infeasible"] is True)
    check("C10 B1 still lands under $250 (cost is not the blocker)",
          m.B1["bom"]["delivered_usd"] < 250.0,
          f"${m.B1['bom']['delivered_usd']}")

    # --- B2 gates ------------------------------------------------------------
    check("C11 B2 under $250", m.B2["bom"]["delivered_usd"] < 250.0,
          f"${m.B2['bom']['delivered_usd']}")
    check("C12 B2 visible transition clears 30 s",
          m.B2["timing"]["visible_clears_30s"] is True,
          f"{m.B2['timing']['visible_transition_s']} s")
    check("C13 B2 blanket force has positive margin",
          m.B2["blanket_force"]["pass_gate"] is True,
          f"margin={m.B2['blanket_force']['margin_n']} N")
    check("C14 B2 is a NON-mask machine", m.B2["mask_machine"] is False)

    # --- B3 gates ------------------------------------------------------------
    check("C15 B3 under $250", m.B3["bom"]["delivered_usd"] < 250.0,
          f"${m.B3['bom']['delivered_usd']}")
    check("C16 B3 visible transition clears 30 s",
          m.B3["timing"]["visible_clears_30s"] is True,
          f"{m.B3['timing']['visible_transition_s']} s")
    check("C17 B3 sustained cycle clears 30 s when double-buffered",
          m.B3["timing"]["sustained_clears_30s"] is True,
          f"{m.B3['timing']['sustained_cycle_s']} s")
    check("C18 B3 deletes the per-cell keeper (80x fewer decisions)",
          m.B3["repeated_count"]["reduction_factor"] == 80.0,
          f"{m.B3['repeated_count']['reduction_factor']}x")

    # --- Reliability audit fields present on every machine -------------------
    audit_fields = ("what_must_work_6400_times", "repeated_moving_parts",
                    "precision_contacts_per_cell", "compliant_printed_elements",
                    "wear_interfaces", "tolerance_sensitive_interactions",
                    "correlated_failure_modes", "single_cell_failure_modes",
                    "serviceability", "min_repeated_feature_mm",
                    "detection_path")
    for cid in ("B1", "B2", "B3"):
        a = getattr(m, cid)["reliability_audit"]
        check(f"C19.{cid} full DND-103 reliability audit present",
              all(k in a for k in audit_fields))

    # --- Honest 7-stage timing decomposition on every machine ----------------
    td_fields = ("digital_process_s", "mask_generation_s", "mask_transport_s",
                 "reset_s", "lift_s", "settle_s", "verify_s",
                 "visible_transition_s", "sustained_cycle_s")
    for cid in ("B1", "B2", "B3"):
        t = getattr(m, cid)["timing"]
        check(f"C20.{cid} 7-stage timing decomposition present",
              all(k in t for k in td_fields))

    # --- S6-LC reference is quantified for comparison ------------------------
    check("C21 S6-LC reference audit quantifies 6,400 repeated parts",
          m.S6LC_AUDIT["repeated_moving_parts"] == 6400)
    check("C22 S6-LC reference audit names its per-cell compliant elements",
          m.S6LC_AUDIT["compliant_printed_elements"] == 6400)

    # --- At least one candidate clears BOTH mission gates --------------------
    winners = [c for c in s["candidates"]
               if c["under_250"] and c["visible_clears_30s"]]
    check("C23 at least one candidate clears cost AND 30 s",
          len(winners) >= 1, f"winners={[w['id'] for w in winners]}")
    check("C24 at least one NON-mask candidate clears both gates",
          any((not w["is_mask"]) for w in winners),
          f"non-mask winners={[w['id'] for w in winners if not w['is_mask']]}")

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
