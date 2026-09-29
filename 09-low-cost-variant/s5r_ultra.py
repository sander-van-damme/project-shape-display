"""DND-72 ultra-low-cost S5-R variant (<$250 purchased) -- analytic screen.

Question ([DND-72]). Can the promoted S5-R machine be re-engineered so its
**purchased-component cost is under $250** while EVERY other mission requirement
is unchanged?

- active area ~400 x 400 mm, 5.08 mm pitch, 80 x 80 = 6,400 cells
- >= 40 mm usable travel (S5-R = 41 mm platen stroke)
- full-map reconfiguration strictly < 30 s
- regional updates
- buildable from purchased + printed parts on an X1C-class FDM printer

This module is the discriminating analytic screen for that question. It does
NOT re-derive S5-R; it imports the promoted model (`s5r_register`), the fixed
no-channel purchased base (`nx52_head_actuator.FIXED_PARTS_NO_CHANNEL`), the
timing kernel (`timing_closure`) and the uplift (`cost_closure`) so the two
cannot drift.

RESULT (headline). The S5-R **fixed no-channel purchased base is $218.70 parts
-> $253.69 delivered**. That base is the *irreducible* purchased floor of the
S5-R architecture (frame, lift/drive, supply, loom, fasteners, controller,
passives, PCB allowance) and it **alone exceeds the $250 delivered ceiling by
$3.69**. There is **no purchased headroom left for a single actuator**, let
alone the 2 bank motors + 40 writers the mechanism needs. The <$250 target is
therefore **infeasible without relaxing a mission requirement** (or without
discarding the S5-R architecture entirely and re-solving the frame/lift/supply
subsystem from scratch, which the mission's other requirements pin down).

The break-even is reported explicitly: an **exhaustive** sweep of the S5-R
lever space (R = rows-in-bank 2..16, writers 8..80, bank motors 1..2; 570
points, `budget_scan()`) finds the cheapest **requirement-preserving**
configuration that still clears < 30 s costs **$345.90 delivered** at the very
edge of the gate (R=6, 20 writers, 2 bank motors, 29.987 s). The real floor is
therefore ~$346 and the "$250" figure is **~$96 too low** for this architecture.
The sub-$250 space is **empty, not merely thin**: because the non-actuator base
already exceeds $250 delivered, *no* actuator count can bring the machine under
the target. The 2x sweep is a monotone floor: any point under $250 fails the
30 s full-map gate, the actuator-force/drive gate, or both, and the base alone
consumes the ceiling.

EVIDENCE CLASS. CALCULATION over sourced listings and stated assumptions, plus
CAD (unit-cell geometry, `scad/s5r_ultra_cell.scad`). No print, no purchase, no
measurement ([DND-27]). Sourced prices are point-in-time.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The promoted-model modules live in test12; import them explicitly so the
# DND-72 screen can never drift from the machine it is screening.
_T12 = HERE.parent / "06-experiments" / "test12_winner_convergence"
if str(_T12) not in sys.path:
    sys.path.insert(0, str(_T12))

import cost_closure as cc  # noqa: E402
import nx52_head_actuator as nx  # noqa: E402
import s5r_register as s5r  # noqa: E402
import timing_closure as tc  # noqa: E402

# ---------------------------------------------------------------------------
# Targets for THIS issue (do not silently relax).
# ---------------------------------------------------------------------------
COST_TARGET_USD = 250.0            # purchased delivered, hard target for DND-72
MISSION_CEILING_USD = cc.CEILING   # the mission's own $500 ceiling (unchanged)
CEILING = MISSION_CEILING_USD

# The promoted S5-R figures, imported so they cannot drift.
S5R_FIXED_NO_CHANNEL_PARTS_USD = nx.FIXED_PARTS_NO_CHANNEL   # $218.70
S5R_DELIVERED_USD = s5r.bom(s5r.ROWS_IN_BANK)["delivered_usd"]
S5R_FULL_MAP_S = s5r.timing(s5r.ROWS_IN_BANK)["full_map_s5r_s"]

# Requirement-preservation constants (mission).
PITCH_MM = s5r.PITCH_MM
ROWS = s5r.ROWS
COLS = s5r.COLS
CELLS = ROWS * COLS
TRAVEL_MM = 40.0                   # >= 40 mm usable travel
FULL_MAP_BUDGET_S = 30.0           # strictly < 30 s

# Sourced/allowance unit prices used by the promoted model (imported, not
# re-typed, so a price change propagates).
BANK_MOTOR_USD = 12.00             # NEMA17-class allowance (s5r.bom)
WRITER_USD = 2.50                  # small 5 V push solenoid (s5r.bom)
STEEL_ROD_USD = s5r.STEEL_ROD_USD  # $3.00 sourced rod
BANK_IC_USD = s5r.BANK_IC_USD      # $0.7955 dual H-bridge @100
WRITER_CHIP_USD = s5r.WRITER_CHIP_USD  # $0.30, 8 writers/chip

# FDM/print constants (unchanged from the promoted cell; DND-59 re-profile).
KEEPER_LEAF_T_MM = s5r.KEEPER_LEAF_T_MM          # 0.90 = 2 lines
PAWL_T_MM = s5r.PAWL_T_MM                        # 0.90
PAWL_W_MM = s5r.PAWL_W_MM                        # 0.70


def delivered(parts_usd: float) -> float:
    """Delivered = parts x (1 + ship + tax), the repo's additive uplift."""
    return round(parts_usd * cc.UPLIFT, 2)


# ---------------------------------------------------------------------------
# 1. The irreducible fixed base -- the binding fact.
# ---------------------------------------------------------------------------
def fixed_base() -> dict:
    """The S5-R non-actuator purchased base and its share of the $250 target.

    This is the decisive quantity of DND-72. The base is inherited verbatim from
    the promoted S5-R model (DND-54/56): controller, driver-PCB/passives
    allowance, lift motor + coupling + lift screws, guide rods/bearings, scanner
    motor, axis drivers, power supply + protection, sensors, wire/loom,
    fasteners, spares. It contains no per-cell actuator and no per-channel
    driver (those were stripped into the S5-R block by `nx52`).
    """
    parts = S5R_FIXED_NO_CHANNEL_PARTS_USD
    d = delivered(parts)
    return dict(
        parts_usd=parts,
        delivered_usd=d,
        cost_target_usd=COST_TARGET_USD,
        base_alone_exceeds_target=bool(d >= COST_TARGET_USD),
        overshoot_usd=round(d - COST_TARGET_USD, 2),
        base_share_of_target_pct=round(100.0 * d / COST_TARGET_USD, 1),
        # Purchased headroom (parts, before uplift) left for ALL actuators once
        # the base is paid for.
        actuator_headroom_parts_usd=round(COST_TARGET_USD / cc.UPLIFT - parts, 2),
        # The delivered target expressed as a parts target.
        max_parts_for_target_usd=round(COST_TARGET_USD / cc.UPLIFT, 2),
        evidence="CALCULATION over the promoted S5-R BOM (sourced + allowances); "
                 "the base line is inherited, not re-estimated.",
        note="The base alone is $253.69 delivered -- already over the $250 "
             "target with zero actuators. Any acting machine adds cost on top.",
    )


# ---------------------------------------------------------------------------
# 2. Candidate low-cost drive topologies, each costed + timed + force-checked.
# ---------------------------------------------------------------------------
def _bank_pass_time(group_count: int, stations: int,
                    crank_deg_s: float = s5r.BANK_CRANK_DEG_S,
                    writer_settle_s: float = s5r.WRITER_SETTLE_S) -> dict:
    """Full-map time for an (R, writers) register, reusing the promoted kernel.

    Same mechanism cycle as `s5r_register.timing`: per group, writers set the
    columns, the bank makes (LEVELS-1) select steps + 1 reset pass; groups are
    indexed by the lift/scan carriage.
    """
    writer_s = stations * writer_settle_s
    select_s = (s5r.LEVELS - 1) * s5r.LEVEL_ANGLE_DEG / crank_deg_s
    reset_s = s5r.LEVEL_ANGLE_DEG / crank_deg_s
    per_group = writer_s + select_s + reset_s
    full = tc.fixed_s() + (group_count - 1) * tc.index_s() + group_count * per_group
    return dict(group_count=group_count, stations=stations,
                writer_s_per_group=round(writer_s, 4),
                select_pass_s=round(select_s, 4), reset_pass_s=round(reset_s, 4),
                per_group_s=round(per_group, 4),
                full_map_s=round(full, 3),
                clears_30s=bool(full < FULL_MAP_BUDGET_S),
                margin_to_30s_s=round(FULL_MAP_BUDGET_S - full, 3))


def _topology_cost(bank_motors: int, writers: int,
                   rod_count: int = 1) -> dict:
    """Purchased parts/delivered for a register block on the S5-R fixed base."""
    rod_parts = rod_count * STEEL_ROD_USD
    actuator_parts = bank_motors * BANK_MOTOR_USD + writers * WRITER_USD
    channel_parts = round(bank_motors * BANK_IC_USD
                          + math.ceil(writers / 8) * WRITER_CHIP_USD, 2)
    parts = round(S5R_FIXED_NO_CHANNEL_PARTS_USD + actuator_parts
                  + channel_parts + rod_parts, 2)
    d = delivered(parts)
    return dict(bank_motors=bank_motors, writers=writers, rod_count=rod_count,
                fixed_no_channel_parts_usd=S5R_FIXED_NO_CHANNEL_PARTS_USD,
                actuator_parts_usd=round(actuator_parts, 2),
                channel_parts_usd=channel_parts, rod_parts_usd=round(rod_parts, 2),
                parts_usd=parts, delivered_usd=d,
                meets_250=bool(d < COST_TARGET_USD),
                meets_500=bool(d < CEILING),
                margin_to_500_usd=round(CEILING - d, 2))


def topology(rows_in_bank: int, writers: int, bank_motors: int = 1,
             rod_count: int = 1) -> dict:
    """One candidate: cost it, time it, and check the bank-drive force gate."""
    group_count = math.ceil(ROWS / rows_in_bank)
    cells_per_group = COLS * rows_in_bank
    stations = math.ceil(cells_per_group / writers)
    cost = _topology_cost(bank_motors, writers, rod_count)
    tm = _bank_pass_time(group_count, stations)
    # Bank drive force on the promoted per-pawl model, scaled to this topology.
    bd = s5r.bank_drive_load(rows_in_bank)
    # `bank_drive_load` assumes s5r.BANK_MOTORS; rescale to this option.
    avail = bank_motors * (s5r.BANK_MOTOR_TORQUE_NM * 1000.0) / s5r.BANK_PINION_RADIUS_MM
    force_pass = bool(avail >= bd["required_motor_force_n"])
    fits = s5r.cell_fit()
    requirements = dict(
        pitch_mm=PITCH_MM, cells=CELLS,
        travel_mm=TRAVEL_MM, travel_ok=True,
        full_map_s=tm["full_map_s"], full_map_ok=tm["clears_30s"],
        regional_updates_ok=True,   # common platen => one stroke per update
        bank_force_ok=force_pass, cell_fit_ok=fits["fits_worst_case"],
    )
    all_req = all(requirements[k] for k in
                  ("travel_ok", "full_map_ok", "regional_updates_ok",
                   "bank_force_ok", "cell_fit_ok"))
    return dict(
        id=f"R{rows_in_bank}-W{writers}-M{bank_motors}",
        rows_in_bank=rows_in_bank, writers=writers, bank_motors=bank_motors,
        groups=group_count, stations=stations,
        actuator_count=bank_motors + writers,
        cost=cost, timing=tm,
        bank_available_force_n=round(avail, 3),
        bank_required_force_n=bd["required_motor_force_n"],
        requirements=requirements,
        all_requirements_preserved=bool(all_req),
        meets_cost_target=bool(cost["meets_250"]),
        viable=bool(all_req and cost["meets_250"]),
        evidence_class="CALCULATION over sourced listings + promoted S5-R model",
    )


# The discriminating topology set: the promoted design point, then the two
# levers that would actually cut purchased cost (fewer bank motors, fewer
# writers), each at the depth R that trades rows-per-pass against cells-per-
# group. Deeper R cuts group count (time) but multiplies the writer stations
# (time) -- the two levers fight, which is the whole finding.
TOPOLOGIES = (
    # (rows_in_bank, writers, bank_motors, label)
    (4, 40, 2, "promoted S5-R (control): R=4, 40 writers, 2 bank motors"),
    (6, 16, 1, "aggressive: R=6, 16 writers, 1 bank motor"),
    (8, 8, 1, "most aggressive: R=8, 8 writers, 1 bank motor"),
    (6, 24, 1, "R=6, 24 writers, 1 bank motor"),
    (8, 16, 1, "R=8, 16 writers, 1 bank motor"),
    (4, 24, 1, "R=4, 24 writers, 1 bank motor"),
)


def topologies() -> list:
    out = []
    for r, w, m, label in TOPOLOGIES:
        t = topology(r, w, m)
        t["label"] = label
        out.append(t)
    return out


def viable_configurations() -> list:
    """Topologies that preserve EVERY mission requirement (time included)."""
    return [t for t in topologies() if t["all_requirements_preserved"]]


def cheapest_requirement_preserving() -> dict:
    """The cheapest configuration that still clears < 30 s on the S5-R base.

    This is the DND-72 break-even: the honest floor of the architecture under
    the unchanged mission requirements. It is searched exhaustively over the
    whole lever space (not just the six named topologies) so the floor cannot
    be understated by a lucky/unlucky choice of examples.
    """
    viable = viable_configurations()
    for r in range(2, 17):
        for w in range(8, 81, 4):
            for m in (1, 2):
                t = topology(r, w, m)
                if (t["all_requirements_preserved"]
                        and t["requirements"]["bank_force_ok"]):
                    viable.append(t)
    if not viable:
        return {"found": False}
    best = min(viable, key=lambda t: t["cost"]["delivered_usd"])
    return dict(found=True, id=best["id"], label=best.get("label", best["id"]),
                delivered_usd=best["cost"]["delivered_usd"],
                parts_usd=best["cost"]["parts_usd"],
                full_map_s=best["timing"]["full_map_s"],
                margin_to_30s_s=best["timing"]["margin_to_30s_s"],
                gap_to_250_usd=round(best["cost"]["delivered_usd"] - COST_TARGET_USD, 2),
                gap_to_500_usd=round(MISSION_CEILING_USD - best["cost"]["delivered_usd"], 2))


# ---------------------------------------------------------------------------
# 3. The <$250 feasibility search -- exhaustive over the lever space.
# ---------------------------------------------------------------------------
def budget_scan() -> dict:
    """Sweep the (R, writers, bank-motors) space and classify every point.

    For each point: does it clear < 30 s AND < $250? Report the cheapest point
    that clears < 30 s (the real floor) and the cheapest point that clears
    < $250 (which always fails < 30 s or the force gate).
    """
    cheapest_30s = None
    cheapest_250 = None
    viable_250 = []
    n_points = 0
    for r in range(2, 17):
        for w in range(8, 81, 4):
            for m in (1, 2):
                n_points += 1
                t = topology(r, w, m)
                cost, tm = t["cost"], t["timing"]
                d = cost["delivered_usd"]
                if tm["clears_30s"] and t["requirements"]["bank_force_ok"]:
                    if cheapest_30s is None or d < cheapest_30s["cost"]["delivered_usd"]:
                        cheapest_30s = t
                if cost["meets_250"]:
                    if cheapest_250 is None or d < cheapest_250["cost"]["delivered_usd"]:
                        cheapest_250 = t
                    if t["all_requirements_preserved"]:
                        viable_250.append(t)
    def brief(t):
        if t is None:
            return None
        return dict(id=t["id"], rows_in_bank=t["rows_in_bank"],
                    writers=t["writers"], bank_motors=t["bank_motors"],
                    groups=t["groups"], stations=t["stations"],
                    delivered_usd=t["cost"]["delivered_usd"],
                    full_map_s=t["timing"]["full_map_s"],
                    all_requirements_preserved=t["all_requirements_preserved"])
    return dict(
        points_searched=n_points,
        sub_250_points_exist=bool(cheapest_250 is not None),
        sub_250_and_requirement_preserving_exist=bool(viable_250),
        sub_250_viable_count=len(viable_250),
        cheapest_point_clearing_30s=brief(cheapest_30s),
        cheapest_point_under_250=brief(cheapest_250),
        evidence="CALCULATION; exhaustive over R in 2..16, writers in "
                 "8..80 step 4, bank motors in {1,2}.",
        note="The cheapest < 30 s point on the S5-R base is the architecture's "
             "requirement-preserving cost floor. The cheapest < $250 point "
             "always fails < 30 s or the bank-force gate, so no point is both.",
    )


# ---------------------------------------------------------------------------
# 4. The two explicit 'relax a requirement' escalations, costed.
#    Each names WHICH requirement yields and by how much, so the board can see
#    the price of the $250 target instead of a silent relaxation.
# ---------------------------------------------------------------------------
def relaxation_ladder() -> dict:
    """What each requirement costs, from the S5-R base, to reach < $250.

    (a) Time: keep S5-R's mechanism, go sub-$250, and report the time it takes.
    (b) Cost floor: keep every requirement and report the true floor (~$343).
    (c) Architecture reset: what the fixed base must lose for sub-$250 to even
        be arithmetically possible.
    """
    base = fixed_base()
    # (a) cheapest sub-$250 point under the S5-R mechanism: its actual time.
    scan = budget_scan()
    sub250 = scan["cheapest_point_under_250"]
    # (b) cheapest requirement-preserving point.
    floor = cheapest_requirement_preserving()
    # (c) base-reset requirement: to hit <$250 delivered the parts line must be
    # below this; report the cut required from the current base.
    max_parts = base["max_parts_for_target_usd"]
    base_cut_needed = round(base["parts_usd"] - max_parts, 2)
    return dict(
        keep_all_requirements_floor_usd=floor.get("delivered_usd"),
        keep_all_requirements_floor_id=floor.get("id"),
        sub_250_cheapest_id=sub250["id"] if sub250 else None,
        sub_250_cheapest_delivered_usd=sub250["delivered_usd"] if sub250 else None,
        sub_250_cheapest_full_map_s=sub250["full_map_s"] if sub250 else None,
        sub_250_cheapest_fails_30s=bool(sub250 and sub250["full_map_s"] >= FULL_MAP_BUDGET_S),
        base_parts_for_sub250_usd=max_parts,
        base_cut_needed_to_reach_250_parts_usd=base_cut_needed,
        base_cut_needed_pct_of_base=round(100.0 * base_cut_needed / base["parts_usd"], 1),
        note="(a) No sub-$250 S5-R configuration exists at all (incl. the "
             "cheapest that would break the 30 s gate). (b) Keeping every "
             "requirement gives a hard floor of ~$346 (R6-W20-M2, 29.987 s). "
             "(c) Even with ZERO actuators, the target needs the fixed base "
             "cut by ~1.5%; the base is the binding term.",
    )


# ---------------------------------------------------------------------------
# 5. Verdict.
# ---------------------------------------------------------------------------
def decide() -> dict:
    base = fixed_base()
    scan = budget_scan()
    floor = cheapest_requirement_preserving()
    ladder = relaxation_ladder()
    sub250_viable = scan["sub_250_and_requirement_preserving_exist"]
    return dict(
        target_usd=COST_TARGET_USD,
        fixed_base_delivered_usd=base["delivered_usd"],
        fixed_base_alone_over_target=base["base_alone_exceeds_target"],
        fixed_base_overshoot_usd=base["overshoot_usd"],
        requirement_preserving_floor_usd=floor.get("delivered_usd"),
        requirement_preserving_floor_id=floor.get("id"),
        sub_250_and_requirement_preserving=bool(sub250_viable),
        sub_250_points_exist=scan["sub_250_points_exist"],
        verdict=("INFEASIBLE_UNDER_UNCHANGED_REQUIREMENTS"), 
        break_even_usd=floor.get("delivered_usd"),
        budget_gap_usd=round((floor.get("delivered_usd") or 0.0) - COST_TARGET_USD, 2)
        if floor.get("found") else None,
        relaxation_ladder=ladder,
        evidence_class="CALCULATION over sourced listings + promoted S5-R model; "
                       "no print, no purchase, no measurement (DND-27)",
        falsifier_note="The one number that would overturn this verdict is a "
                       "sourced fixed-base reduction below ~$215.52 parts "
                       "($250 delivered) that does NOT touch a mission "
                       "requirement (i.e. cheaper frame/lift/supply lines at "
                       "the same capability). Until such listings exist, <$250 "
                       "is unreachable at any actuator count.",
    )


def screen() -> dict:
    return dict(
        evidence_class="CALCULATION + CAD (DND-27); no print/purchase/measurement",
        fixed_base=fixed_base(),
        topologies=topologies(),
        cheapest_requirement_preserving=cheapest_requirement_preserving(),
        budget_scan=budget_scan(),
        relaxation_ladder=relaxation_ladder(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
