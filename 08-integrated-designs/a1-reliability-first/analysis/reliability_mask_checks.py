"""DND-104 reliability-first architecture program - regression checks.

Pins every headline number in `reliability_mask.py` so the prose cannot drift
from the arithmetic (the same convention as the S6-LC and S5 gates).

Run: python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask_checks.py
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
          bw["heads"] == 8 and bw["rate_cells_per_head_s"] > 0)

    # --- DND-111: the writer/reader rate is DERIVED, not the placeholder ----
    import a1_writer_rate as wr
    a = wr.achievable_rate()
    rr = wr.read_resolution_bound()
    fc = wr.full_cycle(heads=8)
    check("DND-111 derived per-head rate is ~164.5 cells/s",
          abs(a["per_head_rate_cells_s"] - 164.5) < 0.5)
    check("DND-111 placeholder 1,000 cells/s is NOT the model rate",
          m.HEAD_RATE_CELLS_S != m.PLACEHOLDER_HEAD_RATE_CELLS_S)
    check("DND-111 placeholder overstated the rate by >=4x",
          m.PLACEHOLDER_HEAD_RATE_CELLS_S / a["per_head_rate_cells_s"] >= 4.0)
    check("DND-111 stop-and-go is excluded (<100 cells/s at X1C accel)",
          a["bounds"]["stop_and_go"]["cells_s_x1c"] < 100.0)
    check("DND-111 dominant limit is traverse or actuation",
          a["primary_design_point"]["dominant_limit"] in ("traverse", "actuation"))
    check("DND-111 single-cell read spot fits the 3.60 mm top face (centre)",
          rr["spot_fits_centre"] is True)
    # DND-113 correction (DND-112 R1/R4): the read is state-dependent-standoff
    # bound, NOT registration bound. The up-state spot is 3.072 mm but the
    # down-state spot is ~24.5 mm at the 42 mm gap, so a down cell cannot be
    # read as single-cell by the as-drawn top-face reader.
    check("DND-113 read is state-dependent-standoff bound, not registration",
          rr["binding_read_limit"] == "state_dependent_standoff"
          and rr["resolves_single_cell"] is False)
    check("DND-113 down-state spot is ~24.5 mm = 4.82 pitches",
          abs(rr["spot_down_state_mm"] - 24.51) < 0.1
          and abs(rr["spot_down_state_pitches"] - 4.82) < 0.02)
    check("DND-113 up-neighbour swamps the down pocket by ~441x",
          abs(rr["standoff_ratio_neighbour_over_pocket"] - 441.0) < 5.0)
    check("DND-113 corrected corner reach is ~4.08 mm (not 2.17)",
          abs(rr["corner_reach_mm"] - 4.081) < 0.01)
    check("DND-113 registration number +/-0.264 mm is retained as provenance",
          abs(rr["registration_tolerance_mm"] - 0.264) < 0.01)
    # DND-114 supersedes the DND-113 "no artifact" state: the common-height
    # read target is now CAD-designed and validated (CH-A frame-fixed vane).
    cht = wr.common_height_read_target()
    check("DND-114 common-height read target is adopted + validated",
          cht["status"].startswith("VALIDATED")
          and cht["ch_a_fixed"] is True
          and cht["ch_a_delta_z_mm"] == 0.0)
    check("DND-114 CH-B hinge-arc DeltaZ is inside the +/-1 mm DoF",
          cht["ch_b_in_dof"] is True and cht["ch_b_delta_z_mm"] <= 1.0)
    fcon = wr.flag_read_contrast()
    check("DND-114 flag spot clears the neighbour body at the fixed standoff",
          fcon["spot_clears_neighbour"] is True
          and fcon["neighbour_clearance_margin_mm"] > 0.0)
    check("DND-114 flag spot fits the flag footprint in Y",
          fcon["spot_fits_flag_y"] is True)
    check("DND-114 read resolves with the common-height target (not as drawn)",
          rr["resolves_single_cell_with_common_height_target"] is True
          and rr["resolves_single_cell"] is False)
    zs = wr.z_stroke_trade_study()
    check("DND-113 reader Z stroke per cell is rate-fatal (>1000 s)",
          zs["per_cell_cycle_s"] > 1000.0)
    check("DND-113 reader Z refocus per line is priced (~29.8 s)",
          abs(zs["per_line_cycle_s"] - 29.8) < 0.5)
    check("DND-111 derived full cycle clears <30 s at 8 heads",
          fc["clears_30s"] is True and fc["full_cycle_s"] < 30.0)
    # DND-113 (DND-112 T1): the aggressive stop-and-go row must use the correct
    # trapezoid, giving 61.9 cells/s, not the V-shaped 89.6.
    check("DND-113 stop-and-go trapezoid gives 61.9 cells/s at 100 m/s^2",
          abs(a["bounds"]["stop_and_go"]["cells_s_aggressive"] - 61.9) < 0.5)
    # DND-113 (DND-112 T3): the full cycle now includes the per-line ramp.
    check("DND-113 8-head cycle includes per-line ramp (~1.0 s/pass)",
          abs(fc["ramp_overhead_per_pass_s"] - 1.0) < 0.02)
    check("DND-113 honest 8-head full cycle is 18.278 s (was 16.278 ideal)",
          abs(fc["full_cycle_s"] - 18.278) < 0.01)
    check("DND-111 pessimistic full-sweep toggle still clears <30 s at 8 heads",
          wr.full_cycle_pessimistic_sweep()["min_heads_to_clear_30s"] is not None and
          wr.full_cycle_pessimistic_sweep()["sweep"][8]["clears_30s"] is True)
    check("DND-111 outcome is (a) Bounded",
          wr.OUTCOME == "a" and "BOUNDED" in wr.OUTCOME_STATEMENT.upper())

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

    # --- CLI modes run cleanly (catches __main__ ordering / NameError) -----
    import subprocess
    here = Path(__file__).resolve().parent
    model = here / "reliability_mask.py"
    for args in ([], ["convergence"]):
        proc = subprocess.run([sys.executable, str(model), *args],
                              capture_output=True, text=True)
        check(f"CLI `reliability_mask.py {' '.join(args)}` exits 0",
              proc.returncode == 0)
    mt = subprocess.run([sys.executable, str(here / "make_table.py")],
                        capture_output=True, text=True)
    check("CLI `make_table.py` exits 0", mt.returncode == 0)

    # --- DND-108 pre-registered adversarial audit pointed at A1 -----------
    # The Falsifier's frozen register audits our selection with a default-deny
    # contract. A1 must come back PRE-REGISTERED CLEAN (all attacks answered).
    audit_script = here.parents[2] / "07-evidence-and-decisions" / "falsifier_dnd104_checks.py"
    audit_view = here / "audit_view_a1.py"
    if audit_script.exists():
        proc = subprocess.run(
            [sys.executable, str(audit_script), "--model", str(audit_view)],
            capture_output=True, text=True)
        check("DND-108 pre-registered audit of A1 is CLEAN", proc.returncode == 0)
        check("DND-108 audit reports no unresolved attacks",
              "unresolved: []" in proc.stdout)
    else:
        check("DND-108 audit script present", False)

    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{passed}/{total} checks pass")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
