"""DND-104 reliability-first architecture program - regression checks.

Pins every headline number in `reliability_mask.py` so the prose cannot drift
from the arithmetic (the same convention as the S6-LC and S5 gates).

Run: python 10-reliability-mask/analysis/reliability_mask_checks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reliability_mask as m  # noqa: E402

CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def main() -> int:
    s = m.screen()
    conv = m.convergence()

    # --- mission unchanged -------------------------------------------------
    check("pitch is 5.08 mm", m.PITCH_MM == 5.08)
    check("6,400 cells", m.CELLS == 6400)
    check("active area 406.4 mm", round(m.ACTIVE_MM, 1) == 406.4)
    check("travel >= 40 mm", m.TRAVEL_MM >= 40.0)

    # --- divergence breadth ------------------------------------------------
    check("at least 7 materially different architectures", s["architecture_count"] >= 7)
    check("each architecture has a decisive falsifier",
          all(r["decisive_falsifier"] for r in s["ranked_feasible_full"] + s["rejected_full"]))
    check("each architecture has a prototype coupon",
          all(r["prototype_coupon"] for r in s["ranked_feasible_full"] + s["rejected_full"]))
    check("each architecture has a reliability audit",
          all("silent_elements" in r["reliability"]
              for r in s["ranked_feasible_full"] + s["rejected_full"]))

    # --- the reliability gate is discriminating ---------------------------
    a1 = next(r for r in s["ranked_feasible_full"] if r["name"].startswith("A1"))
    check("A1 is the only all-gate-feasible architecture", len(s["ranked_feasible_full"]) == 1)
    check("A1 has zero structurally silent elements",
          a1["reliability"]["silent_elements"] == 0)
    check("A1 has readback", a1["reliability"]["has_readback"] is True)
    check("A1 has no compliant printed part deciding correctness",
          a1["reliability"]["compliant_printed_parts"] == 0)
    check("A1 has no precision contact per cell",
          a1["reliability"]["precision_contacts_per_cell"] == 0.0)
    check("A1 clears tabletop load", a1["clears_tabletop_load"] is True)
    check("A1 clears 30 s", a1["clears_30s"] is True)
    check("A1 clears <$250 parts", a1["clears_parts"] is True)

    # --- every global-lift machine fails the tabletop-load gate (honest) --
    globals_ = [r for r in s["rejected_full"] if "global lift" in r["tabletop_load"]["mode"]]
    check("all global-lift machines fail tabletop-load (A7 modelled)",
          len(globals_) >= 6 and all(not r["clears_tabletop_load"] for r in globals_))

    # --- the silent-error gap between A1 and the runner-up ----------------
    check("runner-up silent elements >= 6,000 (10^3 worse than A1)",
          conv["runner_up"] is not None and
          next(r for r in s["ranked_feasible_full"] + s["rejected_full"]
               if r["name"] == conv["runner_up"])["reliability"]["silent_elements"] >= 6000)

    # --- timing decomposition sums correctly ------------------------------
    for r in s["ranked_feasible_full"] + s["rejected_full"]:
        total = round(sum(v["seconds"] for v in r["timing"]["stages"].values()), 4)
        check(f"{r['name'][:6]} timing stages sum to full_cycle_s",
              abs(total - r["timing"]["full_cycle_s"]) < 1e-6)

    # --- A1 timing is derived from the bandwidth model, not magic ---------
    bw = conv["bandwidth"]
    a1_t = a1["timing"]
    check("A1 lift stage equals computed write-all time",
          abs(a1_t["stages"]["lift"]["seconds"] - bw["worst_case_write_all_s"]) < 0.01)
    check("A1 verify stage equals computed verify-pass time",
          abs(a1_t["stages"]["verify"]["seconds"] - bw["verify_pass_s"]) < 0.01)
    check("A1 head count and rate are stated",
          bw["heads"] == 8 and bw["rate_cells_per_head_s"] == 1000.0)

    # --- reliability math --------------------------------------------------
    check("break-even q for 99% map is ~1.57e-6",
          abs(m.PER_CELL_ERROR_BREAK_EVEN - 1.57e-6) < 0.05e-6)
    check("map yield at q=1e-4 for 6,400 silent cells is ~0.527",
          abs(m.map_yield(1e-4, 6400) - 0.527) < 0.005)
    check("map yield at q=1e-5 for 6,400 silent cells is ~0.938",
          abs(m.map_yield(1e-5, 6400) - 0.938) < 0.005)

    # --- prototype ladder --------------------------------------------------
    check("prototype ladder has A/B/C/D + full machine",
          len(conv["prototype_ladder"]) == 5)
    check("ladder stages start with A,B,C,D",
          [x["stage"][0] for x in conv["prototype_ladder"][:4]] == ["A", "B", "C", "D"])

    # --- cost bands --------------------------------------------------------
    check("A1 parts under $250", a1["parts_usd"] < 250.0)
    check("A1 delivered reported", a1["delivered_usd"] > 0)

    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{passed}/{total} checks pass")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
