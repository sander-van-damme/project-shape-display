"""SHA-22 A1 update-time characterization: full-board vs 30 s + local-update model.

Evidence class: CALCULATION over the DND-111/DND-113 derived rate
(`a1_writer_rate.py`) plus placed CAD. No print, no purchase, no measurement
(DND-27). Nothing here is physical validation.

Covers SHA-22 acceptance:
  (1) full-board update-time model vs the 30 s requirement (worst-case
      all-change plus changed-fraction scaling);
  (2) small-region local-update time model and behaviour (does a small change
      disturb the rest of the surface?);
  (3) sensitivity to write-path assumptions (gantry speed, actuation model,
      head count, first-try miss rate);
  (4) data for the coupon measurement/test plan (recorded in the SHA-22
      decision note, not here).

Model notes
-----------
* The authoritative worst-case full-board number is NOT re-derived here: it is
  `a1_promotion_timing.decomposition()` (SHA-7, 19.63 s sustained at 8 heads).
  This module calls it directly and only adds the changed-fraction scaling.
* Changed-fraction scaling is a conservative UPPER bound: the write pass is
  scaled by the changed fraction f while the full per-line ramp and the FULL
  verify pass (the reader always scans all 6,400 cells) are charged in full.
  At f = 1.0 the model reproduces the SHA-7 sustained number exactly (gated).
* Local-update timing reuses `a1_regional_update.regional_time()` (SHA-9):
  addressed cells only, engaged heads = min(heads, tile columns), no reset
  term. Multi-region totals charge one slew per region and a single settle
  share, with per-region write/verify/retry summed.

Run: python 08-integrated-designs/a1-reliability-first/analysis/a1_update_times.py
Gate: python .../a1_update_times.py --gate  (exits 0 iff all checks pass)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a1_writer_rate as wr  # noqa: E402
import a1_promotion_timing as pt  # noqa: E402
import a1_regional_update as rg  # noqa: E402

TIME_GATE_S = 30.0
CELLS = 6400
HEADS = 8
V_MM_S = 1000.0

# Representative D&D reveal workloads (changed cells, touched columns).
# tile_cols caps engaged heads at min(8, tile_cols) per the SHA-9 model.
WORKLOADS: dict[str, tuple[int, int]] = {
    "single_cell": (1, 1),
    "5x5_tile": (25, 5),
    "10x10_tile": (100, 10),
    "room_12x12": (144, 12),
    "corridor_40x4": (160, 40),
    "20x20_tile": (400, 20),
    "full_row_80": (80, 80),
}

FRACTIONS: tuple[float, ...] = (1.0, 0.5, 0.25, 0.10)

SPEEDS: tuple[float, ...] = (500.0, 1000.0, 1500.0)
ACTUATION_MODELS: tuple[str, ...] = ("snap", "full-sweep")
HEAD_SWEEP: tuple[int, ...] = (4, 8, 12, 16)
MISS_SWEEP: tuple[float, ...] = (0.01, 0.05)


def _with_actuation(model: str):
    """Context-light helper: set the writer actuation model, return old value."""
    old = wr.WRITE_ACTUATION_MODEL
    wr.WRITE_ACTUATION_MODEL = model
    return old


def full_board_fraction(f: float, heads: int = HEADS, v_mm_s: float = V_MM_S,
                        actuation: str = "snap",
                        q_miss: float = pt.Q_WRITE_MISS_NOMINAL) -> dict:
    """Conservative full-board time when a fraction f of cells change.

    write pass scales with f; verify pass is always full-field; the full
    per-line ramp is charged (upper bound); retry scales with f*6400.
    """
    old = _with_actuation(actuation)
    try:
        fc = wr.full_cycle(heads=heads, v_mm_s=v_mm_s)
    finally:
        wr.WRITE_ACTUATION_MODEL = old
    st = fc["stages"]
    changed = int(round(CELLS * f))
    rb = pt.retry_budget(changed, q_miss)
    write_s = round(f * st["write"], 4)
    total = round(st["digital_map"] + st["mask_generation"] + st["transport"]
                  + st["reset"] + write_s + st["verify"]
                  + rb["retry_total_s"] + st["settle"], 4)
    return dict(
        changed_fraction=f, changed_cells=changed, heads=heads,
        traverse_mm_s=v_mm_s, actuation_model=actuation, q_miss=q_miss,
        fixed_s=round(st["digital_map"] + st["transport"] + st["reset"]
                      + st["settle"], 4),
        write_s=write_s, verify_full_s=st["verify"],
        retry_s=rb["retry_total_s"], total_s=total,
        clears_30s=bool(total < TIME_GATE_S),
        margin_s=round(TIME_GATE_S - total, 4),
    )


def multi_region(regions: list[tuple[int, int]],
                 heads: int = HEADS) -> dict:
    """Total for k separated regions: one slew each, summed write/verify/retry."""
    parts = [rg.regional_time(n, c, heads=heads) for n, c in regions]
    total = round(sum(p["write_s"] + p["verify_s"] + p["retry_s"]
                      for p in parts)
                  + len(parts) * rg.SLEW_TO_REGION_S + rg.SETTLE_SHARE_S, 4)
    return dict(n_regions=len(parts),
                changed_cells=sum(p["n_cells"] for p in parts),
                parts=parts, total_s=total,
                clears_30s=bool(total < TIME_GATE_S))


def sensitivity() -> dict:
    """Sustained full-board (f = 1) across the write-path assumption box."""
    grid: dict[str, dict] = {}
    for v in SPEEDS:
        for model in ACTUATION_MODELS:
            old = _with_actuation(model)
            try:
                fc = wr.full_cycle(heads=HEADS, v_mm_s=v)
            finally:
                wr.WRITE_ACTUATION_MODEL = old
            rb = pt.retry_budget(CELLS, pt.Q_WRITE_MISS_NOMINAL)
            sust = round(fc["full_cycle_s"] + rb["retry_total_s"], 4)
            grid[f"v={v:.0f}_mm_s+{model}"] = dict(
                full_cycle_s=fc["full_cycle_s"],
                retry_s=rb["retry_total_s"], sustained_s=sust,
                clears_30s=bool(sust < TIME_GATE_S),
                margin_s=round(TIME_GATE_S - sust, 4))
    head_sweep: dict[int, dict] = {}
    for h in HEAD_SWEEP:
        head_sweep[h] = full_board_fraction(1.0, heads=h)
    miss_sweep: dict[str, dict] = {}
    for q in MISS_SWEEP:
        miss_sweep[f"q={q:.2f}"] = full_board_fraction(1.0, q_miss=q)
    worst = max(d["sustained_s"] for d in grid.values())
    best = min(d["sustained_s"] for d in grid.values())
    return dict(grid=grid, head_sweep=head_sweep, miss_sweep=miss_sweep,
                worst_sustained_s=worst, best_sustained_s=best,
                box_clears_30s=bool(worst < TIME_GATE_S))


def report() -> dict:
    prim = pt.decomposition(heads=HEADS, q_miss=pt.Q_WRITE_MISS_NOMINAL)
    fractions = {f"f={f:.2f}": full_board_fraction(f) for f in FRACTIONS}
    locals_ = {name: rg.regional_time(n, c)
               for name, (n, c) in WORKLOADS.items()}
    multi = {
        "three_separated_10x10": multi_region([(100, 10)] * 3),
        "room_plus_corridor": multi_region([(144, 12), (160, 40)]),
    }
    sens = sensitivity()
    return dict(
        evidence_class="CALCULATION over sourced limits + placed CAD (DND-27)",
        scale="80x80 (6400 cells)",
        primary_full_board=prim,
        full_board_fractions=fractions,
        local_updates=locals_,
        multi_region=multi,
        disturbance=dict(
            modelled_rigid_body_neighbour_mm=rg.MODELLED_NEIGHBOUR_MM,
            q5_proposal_gate_mm=rg.Q5_NEIGHBOUR_GATE_MM,
            geometric_margins_mm=dict(
                writer_owned_lane=round(rg.OWNED_HALF_LANE_MM
                                        - rg.LATCH_EXCURSION_MM, 3),
                shutter_sweep_neighbour=rg.SHUTTER_NEIGHBOUR_CLEAR_MM,
                read_spot_neighbour=rg.READ_SPOT_NEIGHBOUR_CLEAR_MM),
            needs_no_full_reset=True,
            granularity="cell",
            behaviour=("A small change does not disturb the rest of the "
                       "surface in the rigid-body model: only differing "
                       "cells are toggled, there is no shared platen move, "
                       "no full-board reset, and every write-path clearance "
                       "is positive. The elastic half (loaded-neighbour "
                       "motion, miniature tipping, wear drift) is "
                       "measurement-only, coupon B.")),
        sensitivity=sens,
        gate_s=TIME_GATE_S,
    )


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = report()
    CHECKS.clear()
    p = r["primary_full_board"]
    # (1) full-board vs 30 s
    check("primary 8-head sustained < 30 s with >10 s margin",
          p["sustained_cycle_s"] < 30.0 and p["margin_s"] > 10.0)
    check("f=1.0 fraction model reproduces SHA-7 sustained exactly",
          abs(r["full_board_fractions"]["f=1.00"]["total_s"]
              - p["sustained_cycle_s"]) < 1e-9)
    check("fraction scaling is monotonic (less change = less time)",
          r["full_board_fractions"]["f=0.10"]["total_s"]
          < r["full_board_fractions"]["f=0.25"]["total_s"]
          < r["full_board_fractions"]["f=0.50"]["total_s"]
          < r["full_board_fractions"]["f=1.00"]["total_s"])
    check("every changed fraction clears 30 s",
          all(d["clears_30s"]
              for d in r["full_board_fractions"].values()))
    # (2) local updates: fast and non-disturbing
    check("single-cell reveal < 1 s",
          r["local_updates"]["single_cell"]["regional_s"] < 1.0)
    check("10x10 tile reveal < 3 s",
          r["local_updates"]["10x10_tile"]["regional_s"] < 3.0)
    check("room 12x12 + corridor 40x4 each < 3 s",
          r["local_updates"]["room_12x12"]["regional_s"] < 3.0
          and r["local_updates"]["corridor_40x4"]["regional_s"] < 3.0)
    check("three separated 10x10 regions < 3 s total",
          r["multi_region"]["three_separated_10x10"]["total_s"] < 3.0)
    check("local update needs no full-board reset",
          r["disturbance"]["needs_no_full_reset"] is True
          and r["disturbance"]["modelled_rigid_body_neighbour_mm"]
          <= r["disturbance"]["q5_proposal_gate_mm"])
    check("all write-path clearances positive",
          all(v > 0.0
              for v in r["disturbance"]["geometric_margins_mm"].values()))
    # (3) sensitivity: whole assumption box clears at 8 heads
    check("sensitivity box (3 speeds x 2 actuations) all clear 30 s",
          r["sensitivity"]["box_clears_30s"] is True)
    check("5 % miss stress still clears (SHA-7 corner, re-checked)",
          r["sensitivity"]["miss_sweep"]["q=0.05"]["clears_30s"] is True)
    check("16-head build is strictly faster than 8-head",
          r["sensitivity"]["head_sweep"][16]["total_s"]
          < r["sensitivity"]["head_sweep"][8]["total_s"])
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\nfull-board worst case: {p['sustained_cycle_s']} s "
          f"(margin {p['margin_s']} s); verdict: {p['verdict']}")
    print(f"sensitivity box: {r['sensitivity']['best_sustained_s']} s "
          f"(best) .. {r['sensitivity']['worst_sustained_s']} s (worst)")
    print(f"10x10 local: {r['local_updates']['10x10_tile']['regional_s']} s; "
          f"3x10x10 separated: "
          f"{r['multi_region']['three_separated_10x10']['total_s']} s")
    print(f"{passed}/{total} update-time checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SHA-22 A1 update-time evidence")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
