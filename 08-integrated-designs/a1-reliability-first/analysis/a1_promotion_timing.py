"""SHA-7 A1 promotion timing: full-map decomposition with verify + retry.

Evidence class: CALCULATION over the DND-111/DND-113 derived rate
(`a1_writer_rate.py`) plus placed CAD. No print, no purchase, no measurement
(DND-27). Nothing here is physical validation.

Covers acceptance criterion 1: full-map timing decomposition (digital map
processing, write sweeps, reader verify + re-drive/retry, reset, settling)
with an explicit <30 s verdict at 80x80 scale, following the mask-subsystem
honest-timing rule (visible transition AND sustained cycle time reported
separately).

For A1 there is no physical mask, so visible == sustained (no hidden prep).
The retry loop is bounded explicitly: after the write pass + verify pass,
expected first-try misses are re-driven cell-by-cell and re-verified, with a
hard retry cap. Even the hostile retry corner stays inside <30 s.

Run: python 08-integrated-designs/a1-reliability-first/analysis/a1_promotion_timing.py
Gate: python .../a1_promotion_timing.py --gate  (exits 0 iff <30 s verdict holds)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a1_writer_rate as wr  # noqa: E402

TIME_GATE_S = 30.0
CELLS = 6400

# Retry model (assumption-class, stated explicitly).
# q_write_miss: per-cell first-try miss probability the retry loop must clean.
# The loop re-drives each missed cell individually (one extra head visit per
# miss, bounded by the fly-over per-cell time) and re-verifies it.
Q_WRITE_MISS_NOMINAL = 0.01   # 1 % first-try miss (hostile writer assumption)
Q_WRITE_MISS_WORST = 0.05     # 5 % stress corner
RETRY_CAP_CELLS = 500         # hard cap: 7.8 % of the field per map (timing guard;
REDIRIVE_CELL_S = 0.020       # one targeted re-drive visit (slew + snap + settle)


def retry_budget(cells: int, q_miss: float) -> dict:
    expected = cells * q_miss
    redriven = min(expected, RETRY_CAP_CELLS)
    # Re-verify each re-driven cell with the reader integration budget.
    reverify_s = redriven * (wr.READ_INTEGRATION_US / 1e6 + wr.SETTLE_MS / 1000.0)
    redrive_s = redriven * REDIRIVE_CELL_S
    capped = expected > RETRY_CAP_CELLS
    return dict(
        q_miss=q_miss,
        expected_misses=round(expected, 1),
        redriven_cells=int(round(redriven)),
        cap_cells=RETRY_CAP_CELLS,
        capped=capped,
        redrive_s=round(redrive_s, 4),
        reverify_s=round(reverify_s, 4),
        retry_total_s=round(redrive_s + reverify_s, 4),
    )


def decomposition(heads: int = 8, q_miss: float = Q_WRITE_MISS_NOMINAL,
                  v_mm_s: float = 1000.0) -> dict:
    fc = wr.full_cycle(heads=heads, v_mm_s=v_mm_s)
    st = fc["stages"]
    rb = retry_budget(CELLS, q_miss)
    stages = dict(
        digital_map_processing_s=st["digital_map"],
        physical_mask_generation_s=st["mask_generation"],
        mask_transport_indexing_s=st["transport"],
        display_reset_s=st["reset"],
        write_sweep_s=st["write"],
        reader_verify_pass_s=st["verify"],
        redrive_retry_s=rb["redrive_s"],
        retry_reverify_s=rb["reverify_s"],
        settling_locking_s=st["settle"],
    )
    # Honest-timing rule: visible transition AND sustained cycle separately.
    # A1 streams the map digitally (mask generation 0.00 s, nothing hidden),
    # so both are the same sum.
    visible_s = round(sum(v for k, v in stages.items()
                          if k != "physical_mask_generation_s"), 4)
    sustained_s = round(sum(stages.values()), 4)
    return dict(
        evidence_class="CALCULATION over sourced limits + placed CAD (DND-27)",
        scale="80x80 (6400 cells), worst-case all-change map",
        heads=heads,
        traverse_mm_s=v_mm_s,
        actuation_model=fc["actuation_model"],
        per_cell_ms=dict(write_cell_ms=fc["write_cell_ms"],
                         verify_cell_ms=fc["verify_cell_ms"]),
        ramp_overhead_per_pass_s=fc["ramp_overhead_per_pass_s"],
        stages=stages,
        retry=rb,
        visible_transition_s=visible_s,
        sustained_cycle_s=sustained_s,
        clears_30s_visible=bool(visible_s < TIME_GATE_S),
        clears_30s_sustained=bool(sustained_s < TIME_GATE_S),
        margin_s=round(TIME_GATE_S - sustained_s, 4),
        verdict=("PASS: full-map cycle clears <30 s with verify + bounded "
                 "retry included" if sustained_s < TIME_GATE_S
                 else "FAIL: cycle breaches the 30 s gate"),
    )


def report() -> dict:
    primary = decomposition(heads=8, q_miss=Q_WRITE_MISS_NOMINAL)
    worst = decomposition(heads=8, q_miss=Q_WRITE_MISS_WORST)
    pess = decomposition(heads=8, q_miss=Q_WRITE_MISS_NOMINAL)
    # pessimistic actuation corner via the full-sweep sweep table
    sweep_pess = wr.full_cycle_pessimistic_sweep()["sweep"][8]
    four = decomposition(heads=4, q_miss=Q_WRITE_MISS_NOMINAL)
    return dict(
        primary_8_heads_nominal_retry=primary,
        stress_8_heads_5pct_miss=worst,
        pessimistic_full_sweep_8_heads=dict(
            full_cycle_s=sweep_pess["full_cycle_s"],
            clears_30s=sweep_pess["clears_30s"],
            note="write+verify passes with the 13 ms full-sweep toggle, "
                 "before retry (retry adds "
                 f"{primary['retry']['retry_total_s']} s nominal)."),
        boundary_4_heads=four,
        gate_s=TIME_GATE_S,
    )


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = report()
    p = r["primary_8_heads_nominal_retry"]
    w = r["stress_8_heads_5pct_miss"]
    CHECKS.clear()
    check("primary 8-head sustained cycle < 30 s", p["sustained_cycle_s"] < 30.0)
    check("primary visible == sustained (no hidden mask prep)",
          abs(p["visible_transition_s"] - p["sustained_cycle_s"]) < 1e-9
          and p["stages"]["physical_mask_generation_s"] == 0.0)
    check("verify pass is priced (= write pass scale)",
          p["stages"]["reader_verify_pass_s"] > 0.0
          and abs(p["stages"]["reader_verify_pass_s"]
                  - p["stages"]["write_sweep_s"]) < 0.01)
    check("retry loop is bounded (cap + explicit seconds)",
          p["retry"]["capped"] is False
          and p["retry"]["retry_total_s"] >= 0.0)
    check("5 % miss stress corner still < 30 s", w["sustained_cycle_s"] < 30.0)
    check("pessimistic full-sweep 8-head + nominal retry still < 30 s",
          r["pessimistic_full_sweep_8_heads"]["full_cycle_s"]
          + p["retry"]["retry_total_s"] < 30.0)
    check("all seven DND-103 stages present",
          set(p["stages"]) == {"digital_map_processing_s",
                               "physical_mask_generation_s",
                               "mask_transport_indexing_s",
                               "display_reset_s", "write_sweep_s",
                               "reader_verify_pass_s", "redrive_retry_s",
                               "retry_reverify_s", "settling_locking_s"})
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\nprimary sustained: {p['sustained_cycle_s']} s "
          f"(margin {p['margin_s']} s); verdict: {p['verdict']}")
    print(f"{passed}/{total} timing checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
