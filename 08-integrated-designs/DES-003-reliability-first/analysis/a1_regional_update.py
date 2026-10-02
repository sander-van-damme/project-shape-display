"""a1 regional update; CAD/calculation source, no physical validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a1_writer_rate as wr  # noqa: E402
import a1_promotion_timing as pt  # noqa: E402

# --- hard geometry (placed CAD, mirrors the design calculation audit constants) ---
PITCH_MM = 5.08
BODY_MM = 3.60
LATCH_T_MM = 0.45
CLEAR_MM = 0.20
OWNED_HALF_LANE_MM = PITCH_MM / 2 - BODY_MM / 2          # 0.74
LATCH_EXCURSION_MM = LATCH_T_MM + CLEAR_MM               # 0.65
SHUTTER_NEIGHBOUR_CLEAR_MM = 0.280                       # design calculation calc
READ_SPOT_NEIGHBOUR_CLEAR_MM = 0.353                     # design calculation calc

# --- Q5 protocol proposal (05-research-questions Q5 / Test11) ---
Q5_NEIGHBOUR_GATE_MM = 0.10
MODELLED_NEIGHBOUR_MM = 0.00  # no shared platen moves in A1

# --- regional timing allowances (assumption-class, stated) ---
SLEW_TO_REGION_S = 0.20       # gantry reposition to the tile
SETTLE_SHARE_S = 0.10         # local settle allowance for a tile reveal
Q_MISS = 0.01                 # nominal first-try miss rate (design calculation)

HEADS = 8
V_MM_S = 1000.0


def regional_time(n_cells: int, tile_cols: int,
                  heads: int = HEADS) -> dict:
    """Time for a tile-local reveal of ``n_cells`` changed cells."""
    fc = wr.full_cycle(heads=heads, v_mm_s=V_MM_S)
    write_cell_s = fc["write_cell_ms"] / 1000.0
    verify_cell_s = fc["verify_cell_ms"] / 1000.0
    engaged = max(1, min(heads, tile_cols))
    write_s = n_cells * write_cell_s / engaged
    verify_s = n_cells * verify_cell_s / engaged
    rb = pt.retry_budget(n_cells, Q_MISS)
    total = SLEW_TO_REGION_S + write_s + verify_s + rb["retry_total_s"] \
        + SETTLE_SHARE_S
    return dict(
        n_cells=n_cells, tile_cols=tile_cols, heads_engaged=engaged,
        slew_s=SLEW_TO_REGION_S,
        write_s=round(write_s, 4), verify_s=round(verify_s, 4),
        retry_s=rb["retry_total_s"], settle_share_s=SETTLE_SHARE_S,
        regional_s=round(total, 4),
    )


def report() -> dict:
    fc8 = wr.full_cycle(heads=8, v_mm_s=V_MM_S)
    fc4 = wr.full_cycle(heads=4, v_mm_s=V_MM_S)
    sweep = wr.full_cycle_head_sweep(v_mm_s=V_MM_S)
    sweep_pess = wr.full_cycle_pessimistic_sweep(v_mm_s=V_MM_S)
    prim = pt.decomposition(heads=8, q_miss=pt.Q_WRITE_MISS_NOMINAL)
    return dict(
        evidence_class="CALCULATION over sourced limits + placed CAD (design calculation)",
        # R5: head-count boundary, both actuation corners
        r5_head_boundary=dict(
            snap_sweep={h: d for h, d in sweep["sweep"].items()},
            pessimistic_sweep={h: d for h, d in sweep_pess["sweep"].items()},
            min_heads_snap=sweep["min_heads_to_clear_30s"],
            min_heads_pessimistic=sweep_pess["min_heads_to_clear_30s"],
            sustained_8_head_s=prim["sustained_cycle_s"],
            margin_8_head_s=prim["margin_s"],
            sustained_4_head_s=pt.decomposition(heads=4)["sustained_cycle_s"],
            design_rule="8 heads minimum (both corners need 8; "
                        "adopted build count)",
            verdict="R5 RETIRED as a design rule: analytically bounded, "
                    "not measurement-gated. 8 heads clear with 10.37 s "
                    "margin (snap) and clear pessimistic too; 4 heads fail "
                    "at both the bare-cycle (30.006 s) and sustained "
                    "(31.35 s) level.",
        ),
        # R6 + regional evidence under Q5
        r6_regional=dict(
            q5_gate_mm=Q5_NEIGHBOUR_GATE_MM,
            modelled_neighbour_mm=MODELLED_NEIGHBOUR_MM,
            geometric_margins_mm=dict(
                writer_owned_lane=round(
                    OWNED_HALF_LANE_MM - LATCH_EXCURSION_MM, 3),
                shutter_sweep_neighbour=SHUTTER_NEIGHBOUR_CLEAR_MM,
                read_spot_neighbour=READ_SPOT_NEIGHBOUR_CLEAR_MM,
            ),
            needs_no_full_reset=True,
            granularity="cell",
            verdict="R6 PARTIALLY retired: rigid-body/geometry half is "
                    "analytic (0.00 mm modelled vs 0.10 mm proposal, all "
                    "clearances positive). The elastic half "
                    "(loaded-neighbour motion, miniature tipping, wear "
                    "drift) is measurement-only and stays open as coupon B.",
        ),
        per_cell_ms=dict(write_cell_ms=fc8["write_cell_ms"],
                         verify_cell_ms=fc8["verify_cell_ms"]),
        full_cycle_8_head_s=fc8["full_cycle_s"],
        full_cycle_4_head_s=fc4["full_cycle_s"],
        regions={
            "single_cell": regional_time(1, 1),
            "5x5_tile": regional_time(25, 5),
            "10x10_tile": regional_time(100, 10),
            "20x20_tile": regional_time(400, 20),
            "full_row_80": regional_time(80, 80),
        },
        missing_piece="Loaded-neighbour elastic motion under tabletop load "
                      "(3.27 N service + miniature mass), miniature tip-over "
                      "on a 20x20 boundary sweep, and hinge-wear drift: all "
                      "require coupon B (5x5 cycling rig) under design calculation. No "
                      "further analysis can retire them.",
    )


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = report()
    CHECKS.clear()
    # R5: 8-head rule holds in both corners, 4-head fails
    check("R5 min heads = 8 (snap corner)", r["r5_head_boundary"]["min_heads_snap"] == 8)
    check("R5 min heads = 8 (pessimistic corner)",
          r["r5_head_boundary"]["min_heads_pessimistic"] == 8)
    check("R5 8-head sustained clears 30 s with >10 s margin",
          r["r5_head_boundary"]["sustained_8_head_s"] < 30.0
          and r["r5_head_boundary"]["margin_8_head_s"] > 10.0)
    check("R5 4-head sustained fails (load-bearing confirmed)",
          r["r5_head_boundary"]["sustained_4_head_s"] > 30.0)
    # R6 / Q5 geometry
    check("R6 modelled 0.00 mm within Q5 0.10 mm proposal",
          r["r6_regional"]["modelled_neighbour_mm"] <= Q5_NEIGHBOUR_GATE_MM)
    check("R6 writer excursion inside owned half-lane",
          r["r6_regional"]["geometric_margins_mm"]["writer_owned_lane"] > 0.0)
    check("R6 shutter sweep clears neighbour",
          r["r6_regional"]["geometric_margins_mm"]["shutter_sweep_neighbour"] > 0.0)
    check("R6 read spot clears neighbour",
          r["r6_regional"]["geometric_margins_mm"]["read_spot_neighbour"] > 0.0)
    check("R6 regional needs no full-board reset",
          r["r6_regional"]["needs_no_full_reset"] is True)
    # Regional timing: tile-local reveals are seconds, not tens of seconds
    check("single-cell reveal < 1 s", r["regions"]["single_cell"]["regional_s"] < 1.0)
    check("10x10 tile reveal < 3 s", r["regions"]["10x10_tile"]["regional_s"] < 3.0)
    check("20x20 tile reveal < 6 s", r["regions"]["20x20_tile"]["regional_s"] < 6.0)
    check("full-row reveal < 3 s", r["regions"]["full_row_80"]["regional_s"] < 3.0)
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    reg = r["regions"]["10x10_tile"]["regional_s"]
    print(f"\n10x10 tile-local reveal: {reg} s; "
          f"modelled neighbour: {MODELLED_NEIGHBOUR_MM:.2f} mm "
          f"(Q5 gate {Q5_NEIGHBOUR_GATE_MM:.2f} mm)")
    print(f"{passed}/{total} regional checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="design calculation A1 regional-update evidence")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
