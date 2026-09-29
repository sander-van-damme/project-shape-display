"""SHA-15 divergent screen — M1 shared-pneumatic bladder lift gate.

Cheapest analytic test for the single advanced mechanism of SHA-15:
a single shared pneumatic bladder (fluid power bus) replaces the electric
lift, while 64 tile-level 3/2 valves gate printed ratchet enables per
10x10 tile. No per-cell cylinders/valves (that topology is row 3, killed).

Evidence class: CALCULATION over sourced-class prices (2026-09 web sweep,
ranges not quotations) + textbook pneumatics (V = A*h, t = V/Q). No print,
no purchase, no measurement (DND-27).

Key topology-independent insight asserted and checked below: banking does
NOT reduce total displaced air (8 banks x 4 strokes x bank volume == full
board x 4 strokes). It only bounds peak force. So the fill-time kill holds
for banked and unbanked variants alike.

Kill criteria (up front, binding):
  KC2 timing .. sustained full-map air-FILL alone must leave budget for
                reset/valve/settle/verify; KILL if nominal fill >= 20 s,
                or best-case fill + minimal reset >= 30 s.
  KC1 cost .... purchased total must beat A1 ($181), meaningful beat <= $171;
                KILL if nominal total >= $181.
  (KC3 silent / KC4 membrane recorded in the verdict note; timing kills first.)

Run:  python 06-experiments/test18_divergent_screen/pneumatic_gate.py
Gate: python 06-experiments/test18_divergent_screen/pneumatic_gate.py --gate
"""

from __future__ import annotations

import argparse

# ---- Board geometry (design criteria 02) ----
BOARD_M = 0.400          # active width (m); extent 406.4 mm only worsens volumes
AREA_M2 = BOARD_M ** 2   # 0.16 m^2
STROKE_FULL_M = 0.040    # 40 mm travel
STROKE_INC_M = 0.010     # 4 threshold increments (S1-style unary encoding)
N_BANKS = 8              # 8 x 10-row banks
N_TILE_VALVES = 64       # one 3/2 valve per 10x10 tile (selection layer)

VOL_FULL_L = AREA_M2 * STROKE_FULL_M * 1000.0        # 6.4 L per full 40 mm sweep
VOL_INC_FULLBOARD_L = AREA_M2 * STROKE_INC_M * 1000.0  # 1.6 L per 10 mm stroke
VOL_INC_BANK_L = VOL_INC_FULLBOARD_L / N_BANKS        # 0.2 L per bank-stroke
# 4 broadcast strokes per map:
VOL_MAP_L = 4.0 * VOL_INC_FULLBOARD_L                # 6.4 L (== VOL_FULL_L)
VOL_MAP_BANKED_L = N_BANKS * 4.0 * VOL_INC_BANK_L    # 6.4 L (identical: banking
# changes peak force only, not total displaced air)

# ---- Sourced-class pump (2026-09 web sweep, ranges not quotations) ----
# 12 V micro-diaphragm class (BODENFLO BD-04A15L et al.): 12-15 L/min free
# flow, >=100 kPa max, retail ~$21-25. Effective flow under 30-60 kPa load
# derated 60-90% (confidence: medium; unmodeled: heat, leak, line loss).
PUMP_FREE_LPM = (12.0, 13.5, 15.0)   # low, nominal, high
DERATE = (0.60, 0.75, 0.90)          # effective fraction under load
PUMP_COST = (21.0, 23.0, 25.0)       # USD retail (medium confidence)

# ---- Sourced-class tile valves (3/2 mini, direct-acting) ----
# Cheap import class ~$1.68-2.08 @qty (Alibaba 2-way/micro 3V1); EU retail
# EUR 27+. Used range $2-5 at 64 pcs (confidence: medium-low; quality risk
# at the $2 end is carried, not resolved).
VALVE_UNIT = (2.0, 3.0, 5.0)
# Fittings, tubing, regulator, filter, manifold share (confidence: low-medium).
PNEU_OVERHEAD = (20.0, 30.0, 40.0)

A1_PARTS = 181.0         # SHA-7 sourced-class BOM (medium)
MEANINGFUL_BEAT = 171.0  # need >= $10 clear to matter

# Force sanity (recorded, not binding): 30 kPa over full board.
FORCE_AT_30KPA_N = 30_000.0 * AREA_M2  # 4800 N >> S1-B worst 2.4 kN


def eff_flow_lps(flow_lpm: float, derate: float) -> float:
    return flow_lpm / 60.0 * derate


def fill_time_s(volume_l: float, flow_lpm: float, derate: float) -> float:
    return volume_l / eff_flow_lps(flow_lpm, derate)


def nominal_fill() -> float:
    return fill_time_s(VOL_MAP_L, PUMP_FREE_LPM[1], DERATE[1])


def best_fill() -> float:
    return fill_time_s(VOL_MAP_L, PUMP_FREE_LPM[2], 1.0)  # free flow, no derate


def worst_fill() -> float:
    return fill_time_s(VOL_MAP_L, PUMP_FREE_LPM[0], DERATE[0])


def nominal_cost() -> float:
    return PUMP_COST[1] + N_TILE_VALVES * VALVE_UNIT[1] + PNEU_OVERHEAD[1]


def low_cost() -> float:
    return PUMP_COST[0] + N_TILE_VALVES * VALVE_UNIT[0] + PNEU_OVERHEAD[0]


def high_cost() -> float:
    return PUMP_COST[2] + N_TILE_VALVES * VALVE_UNIT[2] + PNEU_OVERHEAD[2]


# Minimal mandatory reset: vent the same air volume (passive vent credited at
# 2x pump rate — generous to the mechanism) + 2 s valve/settle allowance.
def best_cycle_s() -> float:
    fill = best_fill()
    vent = VOL_MAP_L / (eff_flow_lps(PUMP_FREE_LPM[2], 1.0) * 2.0)
    return fill + vent + 2.0


CHECKS: list[tuple[str, str]] = [
    ("banking_invariant",
     "banked total air equals unbanked total air (banking bounds force only)"),
    ("nominal_fill_kills",
     "nominal air-fill alone >= 20 s (no budget left for reset/verify)"),
    ("best_cycle_kills",
     "best-case fill + vent + 2 s allowance >= 30 s (fails at every corner)"),
    ("nominal_cost_kills",
     "nominal purchased total >= A1 $181 (no beat; meaningful beat <= $171)"),
    ("force_passes",
     "30 kPa lift force >> worst-case ratchet load (force is NOT the killer)"),
]


def run_gate() -> tuple[int, int, list[str]]:
    lines: list[str] = []
    passed = 0

    ok = abs(VOL_MAP_BANKED_L - VOL_MAP_L) < 1e-9
    tag = "PASS" if ok else "FAIL"
    lines.append(f"[{tag} ] banking_invariant: "
                 f"banked {VOL_MAP_BANKED_L:.2f} L == full-board {VOL_MAP_L:.2f} L")
    passed += ok

    nf = nominal_fill()
    ok = nf >= 20.0
    tag = "PASS" if ok else "FAIL"
    lines.append(f"[{tag} ] nominal_fill_kills: "
                 f"{nf:.1f} s >= 20 s kill line")
    passed += ok

    bc = best_cycle_s()
    ok = bc >= 30.0
    tag = "PASS" if ok else "FAIL"
    lines.append(f"[{tag} ] best_cycle_kills: "
                 f"best {bc:.1f} s >= 30 s (fill {best_fill():.1f} s + vent + 2 s)")
    passed += ok

    nc = nominal_cost()
    ok = nc >= A1_PARTS
    tag = "PASS" if ok else "FAIL"
    lines.append(f"[{tag} ] nominal_cost_kills: "
                 f"${nc:.0f} nominal (low ${low_cost():.0f} / high ${high_cost():.0f}) "
                 f">= A1 ${A1_PARTS:.0f}")
    passed += ok

    ok = FORCE_AT_30KPA_N > 2400.0
    tag = "PASS" if ok else "FAIL"
    lines.append(f"[{tag} ] force_passes: "
                 f"{FORCE_AT_30KPA_N:.0f} N at 30 kPa >> 2400 N worst case")
    passed += ok

    print(f"M1 pneumatic gate: {passed}/{len(CHECKS)} kill-confirming checks hold")
    for line in lines:
        print(" ", line)
    print(f"  fill band: best {best_fill():.1f} s / nominal {nf:.1f} s / "
          f"worst {worst_fill():.1f} s (air-fill ONLY, before reset/valve/settle/verify)")
    return passed, len(CHECKS), lines


def main() -> None:
    parser = argparse.ArgumentParser(description="M1 shared-pneumatic gate")
    parser.add_argument("--gate", action="store_true",
                        help="run kill-confirming gate checks")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    args = parser.parse_args()

    if args.json:
        import json as _json
        print(_json.dumps({
            "vol_map_L": VOL_MAP_L,
            "fill_s": {"best": best_fill(), "nominal": nominal_fill(),
                       "worst": worst_fill()},
            "best_cycle_s": best_cycle_s(),
            "cost_usd": {"low": low_cost(), "nominal": nominal_cost(),
                         "high": high_cost()},
            "force_at_30kPa_N": FORCE_AT_30KPA_N,
        }, indent=1))
        return

    passed, total, _ = run_gate()
    if args.gate and passed != total:
        raise SystemExit(f"GATE INCOMPLETE: {passed}/{total} (M1 not killed)")


if __name__ == "__main__":
    main()
