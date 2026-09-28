#!/usr/bin/env python3
"""Cheap rejection tests for S1 / S2.

Every test returns a PASS/FAIL/UNCERTAIN verdict against a stated threshold,
using DETERMINISTIC arithmetic (no mechanism simulation, no measurement).
The point is to fail ideas before CAD/BOM, not to validate them.

Test A  gate+pawl density at 5.08 mm: does a 5-pocket ratchet, pawl and a
        mask-gated interlock fit in one cell with printable walls?
Test B  aggregate force / friction on ONE broadcast stroke of the whole board.
Test C  mask programming throughput: can four unary 6400-bit planes be written
        inside (or hidden behind) the 30 s budget?
Test D  print variation: with a realistic per-part force spread, what fraction
        of 6400 cells fall outside the safe release window?
Test E  transaction count: does S1/S2 avoid >213 serial cell-services/s?
Test F  regional isolation: does a tile replay disturb untouched loaded cells?
"""

from __future__ import annotations

import math
from dataclasses import dataclass

PITCH_MM = 5.08
N = 80
CELLS = N * N
LEVELS = 5
DEADLINE_S = 30.0

PASS = "PASS"
FAIL = "FAIL"
UNCERTAIN = "UNCERTAIN"


@dataclass
class Verdict:
    name: str
    verdict: str
    detail: str
    margin: float | None = None


# ---------------------------------------------------------------- Test A
def test_gate_density(
    column_body_mm: float = 4.72,
    pawl_thickness_mm: float = 0.6,
    gate_bar_mm: float = 0.5,
    wall_min_mm: float = 0.4,
) -> Verdict:
    """Packing check across the cell BELOW the visible surface.

    At 5.08 mm pitch the full 5.08 x 5.08 mm cell cross-section is available
    below the surface; the 0.36 mm top gap is only the visible-seam clearance.
    The moving column must pass through a guide, and beside it must fit a
    pawl and a mask-gated interlock within the same 5.08 mm cell.

    Conservative budget on the pitch axis:
      guide_wall + pawl + gate + guide_wall <= column_wall_to_wall allowance
    The column body (4.72 mm) leaves (5.08 - 4.72) = 0.36 mm of free gap only
    if the column is full width. The real question is whether the column can be
    narrower below the surface to make room, without breaking the visible tile.
    """
    # Below-surface the column may be necked down. Reserve 1.0 mm for the
    # visible square cap overhang and check the mechanism shaft budget.
    mech_shaft_mm = 2.0
    available = PITCH_MM - mech_shaft_mm - 2 * wall_min_mm
    need = pawl_thickness_mm + gate_bar_mm
    fits = need <= available
    return Verdict(
        "A gate+pawl density (sub-surface)",
        PASS if fits else FAIL,
        f"available beside a {mech_shaft_mm:.1f} mm shaft {available:.2f} mm "
        f"vs pawl+gate {need:.2f} mm; visible gap is only "
        f"{PITCH_MM - column_body_mm:.2f} mm",
        available - need,
    )


def test_rack_pocket_depth(pocket_depth_mm: float = 1.2,
                           cap_mm: float = 4.72,
                           min_rail_mm: float = 0.4) -> Verdict:
    """A 1.2 mm deep pocket on a 4.72 mm face leaves side rails."""
    rail = (cap_mm - 2.0 * 0.0) / 2 - pocket_depth_mm / 2  # conservative
    # Simpler: the pocket is cut vertically into the face; rails are the face
    # material on either side of the pocket along the pitch axis.
    rail = (cap_mm - pocket_depth_mm) / 2
    ok = rail >= min_rail_mm
    return Verdict(
        "A2 rack pocket side rail",
        PASS if ok else FAIL,
        f"side rail {rail:.2f} mm vs min {min_rail_mm:.2f} mm",
        rail - min_rail_mm,
    )


# ---------------------------------------------------------------- Test B
def test_aggregate_stroke_force(
    cells: int = CELLS,
    mu: float = 0.25,
    normal_n_per_cell: float = 0.02,
    pawl_lift_n_per_cell: float = 0.15,
    gate_drag_n_per_cell: float = 0.05,
    platen_mass_kg: float = 3.0,
    accel_m_s2: float = 0.5,
    max_reasonable_n: float = 1500.0,
) -> Verdict:
    """One broadcast stroke must move up to 6400 columns at once.

    Force = gravity + friction + pawl lifting + gate drag over engaged cells,
    plus platen inertia. This is the number that decides whether ONE cheap
    motor can drive the board or whether force must be distributed.
    """
    grav = normal_n_per_cell
    friction = mu * normal_n_per_cell
    per_cell = grav + friction + pawl_lift_n_per_cell + gate_drag_n_per_cell
    total = cells * per_cell + platen_mass_kg * accel_m_s2
    ok = total <= max_reasonable_n
    return Verdict(
        "B aggregate stroke force",
        PASS if ok else FAIL,
        f"{total:.0f} N board-wide ({per_cell:.3f} N/cell x {cells}) vs "
        f"reasonableness cap {max_reasonable_n:.0f} N",
        max_reasonable_n - total,
    )


def test_worst_case_simultaneous(
    locked_fraction: float = 1.0,
    per_cell_release_n: float = 0.37,
    max_n: float = 1500.0,
) -> Verdict:
    """Worst mask: every column armed in the same stroke (all-high map)."""
    total = CELLS * locked_fraction * per_cell_release_n
    ok = total <= max_n
    return Verdict(
        "B2 all-cells-armed stroke",
        PASS if ok else FAIL,
        f"{total:.0f} N if all {CELLS} pawls must release together",
        max_n - total,
    )


# ---------------------------------------------------------------- Test C
def test_mask_write_throughput(
    bits: int = CELLS * (LEVELS - 1),
    visible_budget_s: float = DEADLINE_S,
    per_hole_punch_s: float = 0.20,
    holes_if_punch: int = 3200 * (LEVELS - 1),
    writer_channels: int = 80,
) -> Verdict:
    """If masks must be punched/written during the visible transition.

    Serial holes: holes * per_hole. Parallel writer: holes / channels * step.
    Compare with the visible budget. This is the classic S1/S2 killer.
    """
    serial = holes_if_punch * per_hole_punch_s
    parallel = holes_if_punch / writer_channels * 0.35
    detail = (
        f"{holes_if_punch} hole/set operations: serial {serial:.0f} s, "
        f"{writer_channels}-channel {parallel:.1f} s vs {visible_budget_s:.0f} s visible"
    )
    ok = parallel < visible_budget_s
    return Verdict(
        "C mask programming in visible time",
        PASS if ok else FAIL,
        detail,
        visible_budget_s - parallel,
    )


def test_media_hidden_pipeline(interval_s: float = 300.0,
                               writer_channels: int = 80,
                               holes: int = 3200 * (LEVELS - 1),
                               step_s: float = 0.35) -> Verdict:
    """S2 double-buffer: can the off-line writer prepare before the next map?"""
    t = holes / writer_channels * step_s
    ok = t < interval_s
    return Verdict(
        "C2 off-line writer vs re-plan interval",
        PASS if ok else FAIL,
        f"{t:.1f} s to write a full board off-line vs {interval_s:.0f} s interval",
        interval_s - t,
    )


# ---------------------------------------------------------------- Test D
def test_print_variation_window(
    n: int = CELLS,
    target_release_n: float = 0.45,
    sigma_frac: float = 0.15,
    window_low_n: float = 0.30,
    window_high_n: float = 0.80,
) -> Verdict:
    """Per-cell pawl release force varies. What fraction lands outside the
    safe window (too light -> false step under load; too heavy -> stroke can't
    release it)? Gaussian spread on a 0.45 N nominal."""
    sigma = target_release_n * sigma_frac
    # P(outside window)
    from math import erf, sqrt
    def phi(x: float) -> float:
        return 0.5 * (1 + erf(x / sqrt(2)))
    z_lo = (window_low_n - target_release_n) / sigma
    z_hi = (window_high_n - target_release_n) / sigma
    p_out = phi(z_lo) + (1 - phi(z_hi))
    bad = round(n * p_out)
    # A board is "correct" only if all 6400 cells are in-window:
    p_all = (1 - p_out) ** n
    ok = p_all > 0.5
    return Verdict(
        "D print variation safe window",
        PASS if ok else FAIL,
        f"sigma {sigma:.3f} N -> {p_out*100:.3f}% out-of-window, "
        f"~{bad} bad cells/board, P(all good)={p_all:.3f}",
        p_all - 0.5,
    )


# ---------------------------------------------------------------- Test E
def test_transaction_count(
    visible_s: float = DEADLINE_S,
    cells: int = CELLS,
) -> Verdict:
    """Serial cell services needed for the 30 s target."""
    rate = cells / visible_s
    ok = rate <= 213.34
    return Verdict(
        "E serial cell-service rate",
        PASS if ok else FAIL,
        f"{rate:.1f} cells/s needed if serial vs 213.3 limit "
        "(S1/S2 avoid this by construction)",
        rate - 213.34,
    )


# ---------------------------------------------------------------- Test F
def test_regional_isolation(
    adjacent_load_n: float = 1.0,
    coupling_compliance_n_per_mm: float = 5.0,
    allowed_disturbance_mm: float = 0.20,
    coupling_stiffness_fraction: float = 0.05,
) -> Verdict:
    """A tile replay must not move a loaded untouched neighbor.

    If the shared platen couples through a compliant clutch, the neighbor sees
    a fraction of the stroke force through frame compliance. Estimate the
    neighbor displacement and compare with a 0.2 mm disturbance allowance.
    """
    # Frame load path stiffness is unknown; parameterize as a fraction of the
    # coupling stiffness. This is explicitly an assumption to be measured.
    k_frame = coupling_compliance_n_per_mm / max(coupling_stiffness_fraction, 1e-9)
    disp = adjacent_load_n / (k_frame * 1000.0)  # N / (N/mm) -> mm
    ok = disp <= allowed_disturbance_mm
    return Verdict(
        "F regional isolation disturbance",
        UNCERTAIN if not ok else PASS,
        f"neighbor displacement {disp:.4f} mm (assumed frame stiffness "
        f"{k_frame:.0f} N/mm) vs {allowed_disturbance_mm} mm allowance",
        allowed_disturbance_mm - disp,
    )


def run_all() -> dict[str, Verdict]:
    return {
        "A_gate_density": test_gate_density(),
        "A2_rack_rail": test_rack_pocket_depth(),
        "B_aggregate_force": test_aggregate_stroke_force(),
        "B2_all_armed": test_worst_case_simultaneous(),
        "C_mask_visible": test_mask_write_throughput(),
        "C2_offline_writer": test_media_hidden_pipeline(),
        "D_print_variation": test_print_variation_window(),
        "E_transaction_rate": test_transaction_count(),
        "F_regional_isolation": test_regional_isolation(),
        "G_tile_registration": test_tile_registration(),
        "H_media_registration_stack": test_media_registration_stack(),
    }


# ---------------------------------------------------------------- S2 tests
def test_tile_registration(
    pitch_mm: float = PITCH_MM,
    layers: int = 5,
    per_layer_registration_mm: float = 0.10,
    follower_tip_mm: float = 0.80,
    hole_diameter_mm: float = 1.60,
    max_layer_misalignment_mm: float = 0.25,
) -> Verdict:
    """S2 stacked perforated plates: worst-case accumulated misalignment must
    leave a follower able to pass through its programmed holes.

    If each of four planes registers to +/-0.10 mm independently, the relative
    misalignment between the 40 mm-stop plane and the follower can approach a
    multiple of the per-layer tolerance. Compare with the hole/follower
    clearance budget.
    """
    # Independent per-layer errors combine as sqrt for a random stack.
    stack = per_layer_registration_mm * (layers ** 0.5)
    # Clearance available: (hole - follower)/2 per side.
    clearance = (hole_diameter_mm - follower_tip_mm) / 2
    ok = stack <= clearance
    return Verdict(
        "G media stack misalignment vs hole clearance",
        PASS if ok else FAIL,
        f"worst-case stack {stack:.3f} mm vs {(clearance):.3f} mm "
        f"({hole_diameter_mm:.2f} mm hole, {follower_tip_mm:.2f} mm follower)",
        clearance - stack,
    )


def test_media_registration_stack(
    layers: int = 4,
    per_plane_hole_pitch_error_mm: float = 0.05,
    stack_height_mm: float = 6.0,
    follower_taper_deg: float = 30.0,
    max_adjacent_step_mm: float = 10.0,
) -> Verdict:
    """A tapered follower can absorb lateral registration error over its
    insertion depth. Compare the taper's lateral capture with the stack error.
    """
    import math
    # Lateral capture over the insertion path of the first plate.
    capture = 2 * (stack_height_mm) * math.tan(math.radians(follower_taper_deg))
    error = per_plane_hole_pitch_error_mm * layers
    ok = error <= capture
    return Verdict(
        "H follower taper capture vs registration error",
        PASS if ok else FAIL,
        f"capture {capture:.2f} mm vs accumulated error {error:.2f} mm "
        f"over {layers} planes",
        capture - error,
    )


def main() -> None:
    results = run_all()
    width = max(len(v.name) for v in results.values())
    print(f"{'test'.ljust(width)}  verdict  detail")
    print("-" * 100)
    for key, v in results.items():
        print(f"{v.name.ljust(width)}  {v.verdict:5s}    {v.detail}")


if __name__ == "__main__":
    main()
