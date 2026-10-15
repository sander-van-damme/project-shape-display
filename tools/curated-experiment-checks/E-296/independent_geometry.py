#!/usr/bin/env python3
"""Independent closed-form envelope/kinematic checks for E-296.

Uses only the standard library; does not import the CAD generator. Dimensions
are the reviewed design inputs, not measurements or manufacturing capability.
Run from repository root; JSON is printed or written with --output PATH.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


PITCH = 5.08
STROKE = 1.4
CATCH_LIFT = 0.2
OFF_GAP = 0.6
SLEEVE_OD = 3.0
SLEEVE_BOTTOM = -0.6
SLEEVE_TOP = 4.1
INPUT_TOP = 3.3
OUTPUT_TIP = 4.7
ROW_Z = (0.0, 0.3)
COLUMN_Z = (4.1, 4.5)
RING_OD = 4.7
ROW_ID = 3.2
COLUMN_ID = 2.4
MALE_AF = 1.8
FEMALE_AF = 1.95


def rounded(value):
    if isinstance(value, float):
        return round(value, 9)
    if isinstance(value, dict):
        return {key: rounded(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [rounded(item) for item in value]
    return value


def q(row, column):
    """Spring-biased sleeve constrained by ceiling and positive row catch."""
    return min(column, row + CATCH_LIFT)


def min_affine_maximum(a0, a1, b0, b1):
    """Exact maximum of min(two affine functions) over t in [0,1]."""
    candidates = [0.0, 1.0]
    denominator = (a1 - a0) - (b1 - b0)
    if abs(denominator) > 1e-14:
        cross = (b0 - a0) / denominator
        if 0 < cross < 1:
            candidates.append(cross)
    return max((min(a0 + (a1 - a0) * t, b0 + (b1 - b0) * t), t)
               for t in candidates)


def phase_clearance(male_af, female_af):
    """Coaxial regular-hex inclusion, independent of external CAD meshes.

    A male hex of circumradius male_af/sqrt(3) can rotate freely through all
    angles if its circumcircle fits the female hex's incircle.
    """
    radius = male_af / math.sqrt(3)
    flat_clearance = female_af - male_af
    capture = 2 * radius - female_af
    all_angles_fit = capture <= 0
    phase = None if flat_clearance < 0 else (
        30.0 if all_angles_fit else
        30.0 - math.degrees(math.acos(female_af / (2 * radius))))
    return dict(male_af=male_af, female_af=female_af,
                total_flat_clearance=flat_clearance,
                torque_capture_diameter_margin=capture,
                all_angles_fit_without_positive_hex_capture=all_angles_fit,
                half_free_angle_deg=phase)


def states_and_transitions():
    states = []
    for row, column in itertools.product((0.0, STROKE), repeat=2):
        displacement = q(row, column)
        overlap = max(0.0, displacement - OFF_GAP)
        states.append(dict(row=row, column=column, q=displacement,
                           geometric_overlap=overlap,
                           expected_selected=bool(row and column)))
        assert (overlap > 0) == bool(row and column)

    # All one-coordinate movements are bounded by the held-off input.
    held_off_max = dict(column_closed=0.0, row_retracted=CATCH_LIFT)
    assert max(held_off_max.values()) < OFF_GAP
    crossed_q, crossed_t = min_affine_maximum(
        0.0, STROKE, STROKE + CATCH_LIFT, CATCH_LIFT)
    assert crossed_q > OFF_GAP  # Deliberate negative control.

    command_states = list(itertools.product((0, 1), repeat=4))
    masks = []
    for rows0, rows1, cols0, cols1 in command_states:
        rows, columns = (rows0, rows1), (cols0, cols1)
        selected = [[bool(rows[i] and columns[j]) for j in range(2)] for i in range(2)]
        sleeve_q = [[q(STROKE * rows[i], STROKE * columns[j]) for j in range(2)] for i in range(2)]
        assert selected == [[value > OFF_GAP for value in row] for row in sleeve_q]
        masks.append(dict(rows=rows, columns=columns, selected=selected, q=sleeve_q))
    unique_masks = {tuple(value for row in item["selected"] for value in row) for item in masks}
    assert len(unique_masks) == 10
    assert (True, False, False, True) not in unique_masks
    assert (False, True, True, False) not in unique_masks

    hazardous_crossfades = []
    for start, end in itertools.product(command_states, repeat=2):
        ghost_cells = []
        for i, j in itertools.product(range(2), repeat=2):
            start_selected = bool(start[i] and start[2 + j])
            end_selected = bool(end[i] and end[2 + j])
            maximum, time = min_affine_maximum(
                STROKE * start[2 + j], STROKE * end[2 + j],
                STROKE * start[i] + CATCH_LIFT,
                STROKE * end[i] + CATCH_LIFT)
            if not start_selected and not end_selected and maximum > OFF_GAP:
                ghost_cells.append(dict(cell=[i, j], maximum_q=maximum, t=time))
        if ghost_cells:
            hazardous_crossfades.append(dict(start=start, end=end, ghosts=ghost_cells))
    assert hazardous_crossfades

    return dict(four_single_cell_states=states,
                held_off_maximum_q=held_off_max,
                exact_continuous_crossfade_negative_control=dict(
                    start=[STROKE, 0.0], end=[0.0, STROKE],
                    maximum_q=crossed_q, at_fraction=crossed_t,
                    unwanted_overlap=crossed_q - OFF_GAP),
                all_2x2_command_masks=masks,
                unique_static_masks=len(unique_masks),
                simultaneous_diagonal=dict(possible=False,
                    requested=[[True, False], [False, True]],
                    both_rows_and_columns=[[True, True], [True, True]],
                    ghost_cells=[[0, 1], [1, 0]]),
                arbitrary_linear_2x2_crossfades=dict(
                    checked=256,
                    transitions_with_interior_only_ghost=len(hazardous_crossfades),
                    first_counterexample=hazardous_crossfades[0]),
                required_sequence="Retract all rows, set columns, then raise selected rows; or stop input during crossed handoffs.")


def spring_check():
    wire, mean_d, active, total = 0.2, 3.7, 5, 7
    free_length, shear_modulus = 3.716, 79000.0
    rate = shear_modulus * wire ** 4 / (8 * active * mean_d ** 3)
    solid = total * wire
    normal_space = 3.7 - ROW_Z[1]
    blocked_space = normal_space - STROKE
    # Centered 30-degree hex phase stops inside the enlarged 45-degree mouth.
    phase_wait_q = OFF_GAP + 0.375 - (2*MALE_AF/math.sqrt(3)-FEMALE_AF)/2
    phase_wait_space = normal_space + phase_wait_q - STROKE
    cases = {name: dict(length=space, force=rate * (free_length - space),
                        solid_reserve=space - solid)
             for name, space in (("normal", normal_space),
                                 ("row_on_ceiling_closed", blocked_space),
                                 ("centered_30deg_hex_phase_wait", phase_wait_space),
                                 ("row_off_ceiling_open", normal_space + CATCH_LIFT))}
    inner, outer = mean_d - wire, mean_d + wire
    assert min(case["solid_reserve"] for case in cases.values()) > 0
    assert inner > SLEEVE_OD and outer < 4.2
    return dict(assumptions=dict(material="hypothetical steel", shear_modulus_N_mm2=shear_modulus,
                 wire=wire, mean_diameter=mean_d, inner_diameter=inner,
                 outer_diameter=outer, active_coils=active, total_coils=total,
                 free_length=free_length),
                rate_N_mm=rate, solid_height=solid, states=cases,
                centered_30deg_phase_wait_q=phase_wait_q,
                radial_clearance_to_sleeve=(inner-SLEEVE_OD)/2,
                radial_flange_support=(4.2-outer)/2,
                coil_centerline_seat_width=(RING_OD-ROW_ID)/2,
                caveat="Ideal coil equations; end seating, buckling, friction, fatigue and supplier capability unqualified.")


def envelope_check():
    row_sweep = (ROW_Z[0], ROW_Z[1] + STROKE)
    col_sweep = (COLUMN_Z[0], COLUMN_Z[1] + STROKE)
    crossing_gap = col_sweep[0] - row_sweep[1]
    assert crossing_gap > 0
    external_corners = []
    for center_error, diameter_error in ((0.02, 0.02), (0.05, 0.05), (0.1, 0.1)):
        gap = PITCH - 2 * center_error - (RING_OD + diameter_error)
        external_corners.append(dict(independent_center_bound=center_error,
            independent_diameter_bound=diameter_error, worst_neighbor_gap=gap))
    pin, guide, angle, center = 4.4, 4.6, math.radians(1), 0.05
    rotated_width = pin * (math.cos(angle) + math.sin(angle))
    guide_side_reserve = guide / 2 - (rotated_width / 2 + center)
    neighbor_gap = PITCH - 2 * center - rotated_width
    assert guide_side_reserve > 0 and neighbor_gap > 0
    return dict(pitch=PITCH, ring_outer_diameter=RING_OD,
                nominal_ring_neighbor_gap=PITCH-RING_OD,
                row_full_sweep=row_sweep, column_full_sweep=col_sweep,
                crossing_minimum_z_gap=crossing_gap,
                bridge=dict(width=0.8, thickness=0.3, ring_to_ring_length=PITCH-RING_OD,
                            inside_ring_xy_envelope=True),
                two_by_two_ring_xy_envelope=PITCH+RING_OD,
                external_tolerance_corners=external_corners,
                pin=dict(width=pin, guide=guide, guide_web=PITCH-guide,
                    center_error=center, twist_deg=1.0, rotated_width=rotated_width,
                    guide_per_side_reserve=guide_side_reserve,
                    neighbor_pin_gap=neighbor_gap,
                    center_error_point1_negative_control_reserve=guide/2-rotated_width/2-0.1),
                radial_interfaces=dict(row_ring_to_sleeve=(ROW_ID-SLEEVE_OD)/2,
                    column_ring_to_male_hex=(COLUMN_ID-2*MALE_AF/math.sqrt(3))/2,
                    integral_lower_flange_to_row_ring_capture=(3.4-ROW_ID)/2,
                    spring_installation_over_lower_flange=(3.5-3.4)/2,
                    sleeve_minimum_wall=(3.0-2*FEMALE_AF/math.sqrt(3))/2),
                axial_supports=dict(journal_diameter=2.0, journal_bore=2.02,
                    plate_length=4.0, diametrical_clearance=0.02,
                    nominal_journal_only_tilt_deg=math.degrees(math.atan(.02/4)),
                    input_plate_z=[-6.0,-2.0], input_collars_z=[[-6.5,-6.1],[-1.9,-1.5]],
                    output_plate_z=[7.5,11.5], output_collars_z=[[7.0,7.4],[11.6,12.0]],
                    per_face_axial_clearance=0.1,
                    axial_load_path="Output screw -> captive output collar -> stationary plate; sleeve not required for pin axial support.",
                    caveat="Nominal journal clearance does not fix shaft-axis registration or sleeve float; split-plate clamping and supports require measurement."))


def hex_check():
    nominal = phase_clearance(MALE_AF, FEMALE_AF)
    corners = []
    for bound in (0.02, 0.05, 0.1):
        results = [phase_clearance(MALE_AF + male_sign * bound, FEMALE_AF + female_sign * bound)
                   for male_sign, female_sign in itertools.product((-1, 1), repeat=2)]
        corners.append(dict(independent_AF_error_bound=bound,
                            minimum_flat_clearance=min(v["total_flat_clearance"] for v in results),
                            minimum_torque_capture_margin=min(v["torque_capture_diameter_margin"] for v in results),
                            all_corners_assemble_and_capture=all(v["total_flat_clearance"] > 0 and
                                not v["all_angles_fit_without_positive_hex_capture"] for v in results),
                            corners=results))
    assert corners[0]["all_corners_assemble_and_capture"]
    assert not corners[-1]["all_corners_assemble_and_capture"]
    minimum_overlap = INPUT_TOP - (SLEEVE_BOTTOM + STROKE)
    flat_play = FEMALE_AF - MALE_AF
    tilt = math.atan(flat_play / minimum_overlap)
    output_extension = OUTPUT_TIP - INPUT_TOP
    extrapolated_offset = flat_play/2 + output_extension * flat_play/minimum_overlap
    # Conservative initial mouth capture: loose input/sleeve fit plus maximum
    # output hex. Circumcircle/inscribed-circle inequality is sufficient at
    # every angular phase. This does not solve frictional seating dynamics.
    af_bound, mouth_af, chamfer, hub_axis_offset = 0.02, 2.7, 0.375, 0.03
    loose_play = (FEMALE_AF + af_bound) - (MALE_AF - af_bound)
    loose_tip_offset = loose_play/2 + output_extension * loose_play/minimum_overlap
    max_output_radius = (MALE_AF + af_bound)/math.sqrt(3)
    capture_radius = (mouth_af-af_bound)/2-max_output_radius
    capture_reserve = capture_radius-loose_tip_offset-hub_axis_offset
    minimum_flat_half_gap = ((FEMALE_AF-af_bound)-(MALE_AF+af_bound))/2
    assert capture_reserve > 0
    assert minimum_flat_half_gap > hub_axis_offset
    return dict(nominal=nominal, AF_tolerance_corners=corners,
                minimum_permanent_input_overlap=minimum_overlap,
                maximum_selected_output_overlap=STROKE-OFF_GAP,
                free_tilt_bound=dict(tilt_deg=math.degrees(tilt),
                    assumed_differential_flat_play=flat_play,
                    output_tip_extension_beyond_input=output_extension,
                    extrapolated_tip_center_offset=extrapolated_offset,
                    full_hex_aligned_per_side_gap=flat_play/2,
                    conclusion="Unconstrained clearance permits more tilt than full-hex entry gap; lead-in and real guides must center it. No anti-jam proof."),
                enlarged_mouth_capture=dict(mouth_AF=mouth_af, chamfer_axial_height=chamfer,
                    independent_AF_feature_error=af_bound,
                    measured_hub_axis_offset_prerequisite=hub_axis_offset,
                    loose_input_sleeve_total_flat_play=loose_play,
                    loose_sleeve_tip_offset_bound=loose_tip_offset,
                    all_phase_capture_radial_budget=capture_radius,
                    residual_initial_capture_margin=capture_reserve,
                    smallest_final_flat_half_gap=minimum_flat_half_gap,
                    final_axis_fit_reserve=minimum_flat_half_gap-hub_axis_offset,
                    nominal_straight_output_overlap=STROKE-OFF_GAP-chamfer,
                    straight_output_overlap_after_point1_axial_error=STROKE-OFF_GAP-chamfer-0.1,
                    interpretation="A continuous centered assembly path is geometrically available within this measured alignment prerequisite. Friction, impact, flank loading and physical self-centering remain unqualified."),
                nominal_hex_reversal_free_angle_deg=2*nominal["half_free_angle_deg"],
                equivalent_pin_height_backlash_at_3mm_lead=3*2*nominal["half_free_angle_deg"]/360)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = rounded(dict(evidence="Independent analytical geometry/kinematics; no physical qualification",
                          units="mm unless stated", states=states_and_transitions(),
                          envelope=envelope_check(), spring=spring_check(), hex=hex_check()))
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
