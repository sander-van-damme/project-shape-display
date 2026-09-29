#!/usr/bin/env python3
"""DND-76 regression checks pinning the primitives' headline numbers.

Run:  python 09-lowcost-alternative/primitives/primitives_checks.py

Exits non-zero if any headline drifts. All checks are CALCULATION/CAD-class
assertions over the model in `primitives.py` (DND-27: no print, no measurement).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import primitives as P  # noqa: E402

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f"  -- {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)


def main() -> int:
    # --- baseline -----------------------------------------------------------
    check("baseline S6-LC parts = $139.77",
          P.S6LC_PARTS_USD == 139.77, f"{P.S6LC_PARTS_USD}")
    check("baseline S6-LC motors = 3",
          P.S6LC_MOTORS == 3, f"{P.S6LC_MOTORS}")

    # --- P1 ----------------------------------------------------------------
    snap = P.bistable_snap()
    check("P1 link is a 2-line (>=0.88 mm) leaf",
          snap["printable_thickness"] and snap["leaf_thickness_mm"] >= P.MIN_WALL_MM,
          f"{snap['leaf_thickness_mm']} mm = {snap['extrusion_lines']} lines")
    spread = P.release_force_spread_comparison()
    check("P1 shows S6-LC friction pawl fails the sd<=9% gate",
          spread["s6lc_fails_spread_gate"],
          f"implied sd = {spread['implied_sd_fraction_of_mean']:.1%} of mean")
    check("P1 removes mu from the stored state",
          spread["latch_removes_mu_from_state"] is True)
    check("P1 release ratio (S6-LC) is >2x across the sourced mu band",
          spread["release_ratio_hi_over_lo"] > 2.0,
          f"{spread['release_ratio_hi_over_lo']}x")
    check("P1 snap force is sub-Newton (comb-settable)",
          snap["snap_force_n"] < 1.0, f"{snap['snap_force_n']} N")

    # --- P2 ----------------------------------------------------------------
    comb = P.comb_printability()
    check("P2 comb bar is >= 2 lines", comb["bar_thickness_mm"] >= P.MIN_WALL_MM,
          f"{comb['bar_thickness_mm']} mm")
    check("P2 slot web passes the robust 2-line wall",
          comb["slot_web_pass"], f"web {comb['slot_web_mm']} mm")
    check("P2 guide gap survives worst-case tolerance",
          comb["guide_gap_pass"],
          f"{comb['guide_gap_after_tolerance_mm']} mm after 2x0.10")
    scheme = P.mask_scheme_screen()
    check("P2 selected mask adds ZERO bought items",
          scheme["bought_mask_items_usd"] == 0.0)
    check("P2 selected mask adds ZERO motors",
          scheme["extra_motors_per_bank"] == 0)
    selected = [c for c in scheme["candidates"] if c["verdict"] == "SELECT"]
    check("P2 exactly one mask candidate is selected",
          len(selected) == 1 and
          "4-plane louvre" in selected[0]["name"])
    rejected = [c for c in scheme["candidates"] if "REJECT" in c["verdict"]]
    check("P2 paper punched card is rejected",
          any("paper" in c["name"] for c in rejected))
    check("P2 single relative-shift comb is rejected",
          any("relative shift" in c["name"] for c in rejected))
    fm = P.mask_failure_mode()
    check("P2 correlated failure spans a full 80-cell comb",
          fm["correlated_cells_per_comb"] == 80)
    check("P2 needs 32 comb home sensors for whole-comb detection",
          fm["home_sensors_needed"] == 32)

    # --- P3 ----------------------------------------------------------------
    lane = P.lane_budget()
    check("P3 pawl fits the 1.48 mm lane",
          lane["pawl_fits"], f"stack {lane['pawl_stack_worst_mm']} mm")
    check("P3 lane throw > 0.40 mm after bleeds",
          lane["throw_clear_after_bleed_mm"] >= 0.40,
          f"{lane['throw_clear_after_bleed_mm']} mm")
    check("P3 old side-by-side gate (5.60 mm) does NOT fit 5.08",
          3.60 + 0.80 + 0.20 + 0.80 + 0.20 > P.PITCH_MM)
    throat = P.pocket_throat()
    check("P3 pocket throat is support-free (<=45 deg)",
          throat["sharp_edge_free"], f"{P.POCKET_RELIEF_DEG} deg")
    grip = P.guide_budget()
    check("P3 V-guide centres the body with >5x margin",
          grip["margin_x"] > 5.0, f"{grip['margin_x']}x")
    load = P.pocket_load_path()
    check("P3 pocket floor load path is compression (>=5x)",
          load["margin"] >= 5.0 and load["loads_leaf"] is False,
          f"{load['margin']}x")

    # --- P4 ----------------------------------------------------------------
    rst = P.reset_mechanism()
    check("P4 reset adds ZERO motors",
          rst["extra_motors"] == 0)
    check("P4 reset adds ZERO bought clutches",
          rst["bought_clutches"] == 0)
    check("P4 uses 8 printed one-way clutches",
          rst["printed_clutches"] == 8)
    rf = P.reset_failure_mode()
    check("P4 failure mode is named and correlated",
          "800-cell" in rf["severity"])

    # --- system ------------------------------------------------------------
    t = P.full_map_timing()
    check("SYS full map < 30 s",
          t["clears_30s"], f"{t['full_map_s']} s (margin {t['margin_to_30s_s']} s)")
    check("SYS broadcast strokes are paid once (common platen)",
          t["broadcast_strokes_s"] == (P.LEVELS - 1) * P.PLATEN_STROKE_S)
    cc = P.component_counts()
    check("SYS zero bought per-cell selectors",
          cc["bought_per_cell_selectors"] == 0)
    check("SYS motor count unchanged at 3",
          cc["bought_motors"] == 3)
    check("SYS adds 6,400 printed bistable links at $0 bought",
          cc["printed_bistable_links"] == P.CELLS)
    b = P.bom_delta()
    check("SYS required bought delta is $0",
          b["primitives_required_bought_delta_usd"] == 0.0)
    check("SYS clears $250 even at worst-case optional bought items",
          b["clears_250_worst_case"],
          f"${b['primitives_machine_worst_case_parts_usd']}")

    # --- decision ----------------------------------------------------------
    d = P.decide()
    check("DECISION all gates pass",
          d["all_gates_pass"],
          ", ".join(k for k, v in d["gates"].items() if not v) or "none failing")
    check("DECISION verdict is PRIMITIVES_SURVIVE_SCREEN",
          d["verdict"] == "PRIMITIVES_SURVIVE_SCREEN")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} CHECK(S) FAILED: {', '.join(FAILURES)}")
        return 1
    print("All DND-76 primitive checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
