#!/usr/bin/env python3
"""E-295: bounded, unmeasured screw-drive timing and cost scenarios.

Run: python3 tools/curated-experiment-checks/E-295/hybrid_timing_cost.py
     ... --json > tools/curated-experiment-checks/E-295/hybrid_results.json
Pure standard library, fixed seed, no claim of measured machine performance.
"""

import argparse
from dataclasses import asdict, dataclass
import json
import math
import random


@dataclass(frozen=True)
class Assumptions:
    grid: int = 80
    pitch_mm: float = 5.08
    lead_mm_rev: float = 3.0
    range_mm: float = 40.0
    neutral_mm: float = 20.0
    xy_mm_s: float = 150.0
    xy_mm_s2: float = 1500.0
    rpm: float = 600.0
    rotary_rpm_s: float = 3000.0
    approach_s: float = 0.15
    phase_search_s: float = 0.20
    seating_s: float = 0.10
    withdraw_s: float = 0.15
    command_settle_s: float = 0.15
    missed_dock_probability: float = 0.02
    failed_attempt_s: float = 0.60
    bank_direction_change_s: float = 0.15
    bank_release_s: float = 0.05
    home_rpm: float = 120.0
    home_overrun_s: float = 0.50
    seed: int = 295

    @property
    def dock_s(self):
        return (self.approach_s + self.phase_search_s + self.seating_s
                + self.withdraw_s + self.command_settle_s)


def rest_to_rest(distance, speed, acceleration):
    """Symmetric triangular/trapezoidal move; distance and speed use same units."""
    distance = abs(distance)
    if distance == 0:
        return 0.0
    transition = speed * speed / acceleration
    if distance <= transition:
        return 2 * math.sqrt(distance / acceleration)
    return distance / speed + speed / acceleration


def travel(a, b, assumptions):
    # Independent X/Y axes move concurrently and each stops at the next address.
    return max(rest_to_rest(abs(b[i] - a[i]) * assumptions.pitch_mm,
                            assumptions.xy_mm_s, assumptions.xy_mm_s2)
               for i in range(2))


def spin(delta_mm, assumptions, rpm=None):
    return rest_to_rest(abs(delta_mm) / assumptions.lead_mm_rev,
                        (assumptions.rpm if rpm is None else rpm) / 60,
                        assumptions.rotary_rpm_s / 60)


def expected_failed_rounds(count, probability):
    """E[max failures] for count independent geometric docking attempts.

    Dock failures are detected BEFORE spinning; retries occur at the same site.
    No model for undetected slip, damaged threads, or correlated frame errors.
    """
    if count == 0:
        return 0.0
    total, power = 0.0, probability
    for _ in range(100):
        term = -math.expm1(count * math.log1p(-power)) if power else 0.0
        total += term
        if term < 1e-14:
            break
        power *= probability
    return total


def scenarios(a):
    rng = random.Random(a.seed)
    positions = [(x, y) for y in range(a.grid) for x in range(a.grid)]
    dense = {(x, y): rng.uniform(0, a.range_mm) - rng.uniform(0, a.range_mm)
             for x, y in positions}
    known_to_neutral = {(x, y): a.neutral_mm - rng.uniform(0, a.range_mm)
                        for x, y in positions}
    local_positions = rng.sample(positions, 25)
    sparse = {p: rng.choice([-1, 1]) * rng.uniform(2, 10) for p in local_positions}
    clustered_25 = {(x, y): rng.choice([-1, 1]) * rng.uniform(2, 10)
                    for y in range(8, 13) for x in range(8, 13)}
    clustered_100 = {(x, y): rng.choice([-1, 1]) * rng.uniform(2, 10)
                     for y in range(5, 15) for x in range(5, 15)}
    # Circular hill in one quadrant: static partitions expose load imbalance.
    radius, center = a.grid / 8, a.grid / 4
    hill = {}
    for x, y in positions:
        r = math.hypot(x - center, y - center)
        if r < radius:
            hill[x, y] = 15 * (1 - r / radius)
    return {"dense_random_scene": dense,
            "known_scene_to_neutral": known_to_neutral,
            "neutral_to_one_hill": hill,
            "local_25_distributed": sparse,
            "local_25_clustered": clustered_25,
            "local_100_clustered": clustered_100}


def ordered(points):
    # Reproducible serpentine address order, not an optimized travelling salesman.
    return sorted(points, key=lambda p: (p[1], p[0] if p[1] % 2 == 0 else -p[0]))


def xy_time(changes, count, a):
    tiles = math.isqrt(count)
    assert tiles * tiles == count and a.grid % tiles == 0
    size = a.grid // tiles
    parts = [[] for _ in range(count)]
    for p in changes:
        parts[(p[1] // size) * tiles + p[0] // size].append(p)
    totals, components, counts = [], [], []
    for head, positions in enumerate(parts):
        # Each independently driven tile starts at its lower-left screw address.
        previous = ((head % tiles) * size, (head // tiles) * size)
        move_s = rotation_s = dock_s = retry_s = 0.0
        for p in ordered(positions):
            move_s += travel(previous, p, a)
            rotation_s += spin(changes[p], a)
            dock_s += a.dock_s
            retry_s += expected_failed_rounds(1, a.missed_dock_probability) * a.failed_attempt_s
            previous = p
        components.append({"travel_s": move_s, "rotation_s": rotation_s,
                           "dock_s": dock_s, "expected_retry_s": retry_s})
        totals.append(sum(components[-1].values()))
        counts.append(len(positions))
    critical = max(range(count), key=totals.__getitem__)
    return {"seconds": totals[critical], "head_count": count,
            "critical_head_changed_pins": counts[critical],
            "critical_head_components": components[critical],
            "head_changed_pin_counts": counts,
            "load_imbalance_vs_even_division":
                totals[critical] / (sum(totals) / count) if sum(totals) else 0,
            "scope": "Independent static square domains; no common-carriage packing claim"}


def bank_time(changes, count, a, stop_bus_for_release=False):
    """Conditional k-head common-bus bank, independent selectors and stops.

    Adjacent k-wide groups; shared direction requires up and down subpasses.
    Fresh seating for each direction if axial cups are the selectors. Optional
    stopped-bus releases avoid assuming harmless withdrawal during rotation.
    All seating and local no-slip stopping are assumed, not established.
    """
    assert a.grid % count == 0
    groups = {}
    for p, delta in changes.items():
        groups.setdefault((p[0] // count, p[1]), []).append(delta)
    previous = (0, 0)
    parts = {"travel_s": 0.0, "rotation_s": 0.0, "dock_s": 0.0,
             "expected_retry_s": 0.0, "direction_and_release_s": 0.0}
    for group in ordered(groups):
        deltas = groups[group]
        position = (group[0] * count, group[1])
        parts["travel_s"] += travel(previous, position, a)
        previous = position
        up, down = max(deltas + [0]), -min(deltas + [0])
        for sign in [1, -1]:
            active = [abs(d) for d in deltas if d * sign > 0]
            if not active:
                continue
            parts["expected_retry_s"] += expected_failed_rounds(
                len(active), a.missed_dock_probability) * a.failed_attempt_s
            if stop_bus_for_release:
                # Tips selected by axial engagement: stop common bus at each
                # distinct target, withdraw finished cups, restart remaining.
                # Shared dock excludes final withdrawal, which is charged at
                # each target event. Exact equal heights release together.
                parts["dock_s"] += a.dock_s - a.withdraw_s
                previous_height = 0.0
                for height in sorted(set(active)):
                    parts["rotation_s"] += spin(height - previous_height, a)
                    parts["direction_and_release_s"] += a.withdraw_s + a.bank_release_s
                    previous_height = height
            else:
                parts["dock_s"] += a.dock_s
                parts["rotation_s"] += spin(max(active), a)
                parts["direction_and_release_s"] += a.bank_release_s
        if up and down:
            parts["direction_and_release_s"] += a.bank_direction_change_s
    return {"seconds": sum(parts.values()), "heads": count,
            "address_groups": len(groups), "components": parts,
            "scope": ("Bus stops at every distinct release target; safe axial withdrawal still unproven"
                      if stop_bus_for_release else
                      "Optimistic continuous-release bound; anticipatory release and rotating withdrawal unproven")}


def unknown_to_neutral(count, a):
    """Worst unknown state: every group sweeps 40 mm to slipping bottom stops.

    Once all are physically bottomed, keep engaged and reverse to midheight.
    Lower stop, torque window and zero datum are essential preconditions.
    """
    assert a.grid * a.grid % count == 0
    batches = a.grid * a.grid // count
    if count == a.grid * a.grid:
        total_travel = 0.0
    else:
        previous, total_travel = (0, 0), 0.0
        for y in range(a.grid):
            starts = list(range(0, a.grid, count))
            if y % 2:
                starts.reverse()
            for x in starts:
                total_travel += travel(previous, (x, y), a)
                previous = (x, y)
    cycle = (a.dock_s + spin(a.range_mm, a, a.home_rpm)
             + a.home_overrun_s + a.bank_direction_change_s
             + spin(a.neutral_mm, a)
             + expected_failed_rounds(count, a.missed_dock_probability) * a.failed_attempt_s)
    return {"seconds": batches * cycle + total_travel, "groups": batches,
            "parallel_contacts": count,
            "scope": "Conditional slip-at-each-contact homing; includes full downward sweep then +20 mm"}


def cost_and_scaling(a):
    n = a.grid ** 2
    # Design allowances in USD, not quotes, purchased BOM or guaranteed budget.
    # Full-length volume is projected geometry, NOT short-coupon measurement.
    volume_cm3 = 0.60
    density_g_cm3 = 1.24
    material_kg = n * volume_cm3 * density_g_cm3 / 1000
    waste_yield = 0.85
    # Add 15–45% for tops/collars/print bracing, before rejected parts allowance.
    filament_kg_range = [material_kg * 1.15 / waste_yield,
                         material_kg * 1.45 / waste_yield]
    filament_cost = [filament_kg_range[0] * 20, filament_kg_range[1] * 35]
    common = [filament_cost[0] + 80 + 40, filament_cost[1] + 220 + 100]
    per_xy_head = [4 * 10 + 40 + 20 + 4 * 4,
                   4 * 20 + 100 + 60 + 4 * 8]
    return {
        "label": "2026-10 design allowances in USD; no supplier quotes, tax/shipping/labor excluded",
        "pins": n, "projected_pair_solid_cm3": volume_cm3,
        "projected_pair_mass_g": volume_cm3 * density_g_cm3,
        "filament_kg_with_added_features_and_85pct_yield": filament_kg_range,
        "filament_usd": filament_cost,
        "common_frame_guides_capture_electronics_plus_filament_usd": common,
        "independent_XY_head_axes": 4,
        "independent_XY_head_usd": per_xy_head,
        "independent_XY_system_usd": {
            str(h): [common[0] + h * per_xy_head[0], common[1] + h * per_xy_head[1]]
            for h in [1, 4, 16]},
        "common_bus_bank_usd": {
            str(h): [common[0] + 130 + h * (6 + 4),
                     common[1] + 300 + h * (18 + 12)] for h in [8, 16, 80]},
        "bank_allowance_components_usd": {
            "motion_and_rotary_bus": [130, 300],
            "each_selector": [6, 18], "each_cup_bearing_slip_module": [4, 12]},
        "assembly_hours_at_seconds_per_pair": {
            str(seconds): n * seconds / 3600 for seconds in [20, 45, 90]},
        "each_extra_0_10_usd_per_pin_adds_usd": n * 0.10,
        "each_extra_10_seconds_per_pin_adds_hours": n * 10 / 3600,
        "volume_only_extrusion_hours_at_5_to_12_mm3_s": [
            n * volume_cm3 * 1000 / 12 / 3600,
            n * volume_cm3 * 1000 / 5 / 3600],
        "torque_power_illustration_at_2_mNm_each": {
            str(h): {"summed_contact_torque_Nm": h * .002,
                     "mechanical_power_W_120_rpm": h * .002 * 120 * 2 * math.pi / 60,
                     "mechanical_power_W_600_rpm": h * .002 * 600 * 2 * math.pi / 60}
            for h in [1, 8, 16, 80, n]},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    a = Assumptions()
    cases = scenarios(a)
    results = {
        "evidence": "Reproducible analytical scenario calculations; all machine rates and costs unmeasured",
        "assumptions": asdict(a),
        "scenarios": {name: {"changed_pins": len(changes),
                              "mean_absolute_delta_mm": sum(map(abs, changes.values())) / len(changes),
                              "xy": {str(h): xy_time(changes, h, a) for h in [1, 4, 16]},
                              "common_bus_bank": {str(h): bank_time(changes, h, a) for h in [8, 16, 80]},
                              "common_bus_bank_stopped_release": {
                                  str(h): bank_time(changes, h, a, True) for h in [8, 16, 80]}}
                      for name, changes in cases.items()},
        "unknown_state_to_neutral": {str(h): unknown_to_neutral(h, a) for h in [1, 8, 16, 80, 6400]},
        "cost_and_scale": cost_and_scaling(a),
        "speed_sensitivity_dense_scene": {},
        "lead_sensitivity_dense_scene": {},
    }
    for label, rpm, accel, dock_scale, xy_accel in [
            ("fast_unproven", 1200, 6000, .6, 3000),
            ("planning_unproven", 600, 3000, 1, 1500),
            ("cautious_unproven", 300, 1500, 2, 750)]:
        values = asdict(a)
        values.update(rpm=rpm, rotary_rpm_s=accel, xy_mm_s2=xy_accel)
        for field in ["approach_s", "phase_search_s", "seating_s", "withdraw_s", "command_settle_s"]:
            values[field] *= dock_scale
        variant = Assumptions(**values)
        results["speed_sensitivity_dense_scene"][label] = {
            str(h): xy_time(cases["dense_random_scene"], h, variant)["seconds"] for h in [1, 4, 16]}
    for lead in [1.5, 2, 3]:
        values = asdict(a)
        values["lead_mm_rev"] = lead
        variant = Assumptions(**values)
        results["lead_sensitivity_dense_scene"][str(lead)] = {
            str(h): xy_time(cases["dense_random_scene"], h, variant)["seconds"] for h in [1, 4, 16]}
    # Analytic consistency checks for this model, not proof of physical mechanism.
    assert rest_to_rest(0, 10, 50) == 0
    assert abs(rest_to_rest(2, 10, 50) - .4) < 1e-12
    assert abs(expected_failed_rounds(1, .02) - .02 / .98) < 1e-12
    assert xy_time({(0, 0): 3}, 1, a)["seconds"] > spin(3, a) + a.dock_s
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        print("All times are calculations from unmeasured assumptions; seconds.")
        print("scenario,changed,XY1,XY4,XY16,continuous_bank8,continuous_bank16,continuous_bank80,stopped_bank8,stopped_bank16,stopped_bank80")
        for name, result in results["scenarios"].items():
            values = [result["xy"][str(h)]["seconds"] for h in [1, 4, 16]]
            values += [result["common_bus_bank"][str(h)]["seconds"] for h in [8, 16, 80]]
            values += [result["common_bus_bank_stopped_release"][str(h)]["seconds"] for h in [8, 16, 80]]
            print(name + "," + str(result["changed_pins"]) + "," + ",".join(f"{x:.1f}" for x in values))
        print("unknown-to-neutral:" + json.dumps(results["unknown_state_to_neutral"]))
        print("cost-and-scale:" + json.dumps(results["cost_and_scale"]))


if __name__ == "__main__":
    main()
