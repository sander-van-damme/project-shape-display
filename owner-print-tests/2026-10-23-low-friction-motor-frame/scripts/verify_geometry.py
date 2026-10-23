"""Read-only audit of the supplied v3 meshes for the height/friction diagnosis.

Run from any directory: python path/to/verify_geometry.py
Requires numpy, trimesh and manifold3d. Writes only this pack's new report;
it does not regenerate or modify the baseline and is not a physical fit test.
"""
from pathlib import Path
import hashlib
import json
import math

import manifold3d as md
import numpy as np
import trimesh


PACK = Path(__file__).resolve().parents[1]
BASE = PACK.parent / "2026-10-19-microstepper-frame-v3"
COMPONENTS = BASE / "components"
TOL = 1e-4  # mm^3; distinguishes mesh numerical noise from finite overlap.


def load(name):
    return trimesh.load(COMPONENTS / (name + ".stl"), force="mesh")


def solid(mesh):
    return md.Manifold(md.Mesh(np.asarray(mesh.vertices, dtype=np.float32),
                              np.asarray(mesh.faces, dtype=np.uint32)))


def rotated(mesh, angle, axis=(0, 0, 1)):
    result = mesh.copy()
    result.apply_transform(trimesh.transformations.rotation_matrix(
        math.radians(angle), axis))
    return result


def translated(mesh, xyz):
    result = mesh.copy()
    result.apply_translation(xyz)
    return result


def cylinder(height, radius, z):
    return md.Manifold.cylinder(height, radius, radius, 192).translate([0, 0, z])


def box(size, origin):
    return md.Manifold.cube(size).translate(origin)


def overlap(a, b):
    return max(0.0, (a ^ b).volume())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


names = ["front", "back", "rotor", "rotor-long", "pin", "pin-50",
         "spacer-060", "spacer-072", "spacer-084"]
meshes = {name: load(name) for name in names}
assert all(mesh.is_watertight and mesh.is_winding_consistent and
           len(mesh.split()) == 1 for mesh in meshes.values())

# Undo the print pose, then rotate the actual back part. No reflection in
# assembly: determinant +1 is necessary for a physically realizable pose.
front = rotated(translated(meshes["front"], [0, 0, -6.5]), 90, (1, 0, 0))
back = rotated(rotated(translated(meshes["back"], [0, 0, -6.5]),
                       90, (1, 0, 0)), 180)
rotation_back = (trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1]) @
                 trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
assert abs(np.linalg.det(rotation_back[:3, :3]) - 1) < 1e-12
frame = solid(front) + solid(back)
assert overlap(solid(front), solid(back)) < TOL
rotors = {name: translated(meshes[name], [0, 0, 12.9])
          for name in ["rotor", "rotor-long"]}
washer = cylinder(.5, 3.5, 12.4) - cylinder(.5, 1.6, 12.4)

states = []
for rotor_name, pin_name in [("rotor", "pin"), ("rotor", "pin-50"),
                             ("rotor-long", "pin-50")]:
    for lift in [0.0, .3]:
        for travel in [0.0, 1.5, 3.0]:
            rotor = solid(translated(rotated(rotors[rotor_name], -120 * travel),
                                     [0, 0, lift]))
            pin = solid(translated(meshes[pin_name], [0, 0, 27.9 + travel + lift]))
            row = dict(rotor=rotor_name, pin=pin_name, travel_mm=travel,
                       rotor_lift_mm=lift, pin_frame_mm3=overlap(pin, frame),
                       rotor_frame_mm3=overlap(rotor, frame),
                       rotor_pin_mm3=overlap(rotor, pin))
            assert max(row[k] for k in row if k.endswith("mm3")) < TOL, row
            states.append(row)

# Directly measure print-foot and straight-bore extents from actual sections.
pin_sections = {}
for name in ["pin", "pin-50"]:
    pin_solid = solid(meshes[name])
    foot_bounds = list(pin_solid.slice(.12).bounds())
    top_polygons = pin_solid.slice(10).to_polygons()
    bounds = [[float(np.min(p[:, 0])), float(np.min(p[:, 1])),
               float(np.max(p[:, 0])), float(np.max(p[:, 1]))] for p in top_polygons]
    bounds.sort(key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    assert np.allclose(foot_bounds, [-6, -6, 6, 6], atol=1e-4)
    assert np.allclose(bounds[0], [-1.76, -1.76, 1.76, 1.76], atol=1e-4)
    assert np.allclose(bounds[-1], [-2.2, -2.2, 2.2, 2.2], atol=1e-4)
    pin_sections[name] = dict(foot_section_z_mm=.12, foot_bounds_xy_mm=foot_bounds,
                              tube_section_z_mm=10, tube_loop_bounds_xy_mm=bounds)

# This is a digital collision search, never an instruction to drive to a stop.
boundary_states = []
for pin_name in ["pin", "pin-50"]:
    for lift in [0.0, .3]:
        for travel in [-.71-lift, -.69-lift, 4.55-lift, 4.57-lift]:
            pin = solid(translated(meshes[pin_name], [0, 0, 27.9 + travel + lift]))
            volume = overlap(pin, frame)
            expected_collision = travel + lift < -.7 or travel + lift > 4.56
            assert (volume > TOL) == expected_collision, (pin_name, lift, travel, volume)
            boundary_states.append(dict(pin=pin_name, rotor_lift_mm=lift,
                                        thread_travel_mm=travel,
                                        absolute_pin_rise_mm=travel+lift,
                                        pin_frame_mm3=volume,
                                        expected_collision=expected_collision))

# Footless geometry is calculated only to expose why trimming the foot is not
# a qualified travel upgrade. It is not generated as a print or modification.
thread_overlap = []
for screw_length in [16, 48]:
    for travel in [0, 3, 7, 10, 13, 15, 39, 40, 45]:
        screw_bottom, screw_top = 24.9, 24.9+screw_length
        nut_bottom, nut_top = 27.9+travel, 33.9+travel
        axial_overlap = max(0., min(screw_top, nut_top)-max(screw_bottom, nut_bottom))
        thread_overlap.append(dict(screw_thread_length_mm=screw_length,
                                   travel_mm=travel,
                                   nominal_axial_thread_overlap_mm=axial_overlap))

# Owner subsequently reported about15 mm rise and a roughly40/50-mm pin.
# Check the actual supplied50-mm mesh; no invented40-mm mesh is substituted.
# The footless solid is an in-memory diagnostic only, not a new deliverable.
owner_height_checks = []
for rotor_name in ["rotor", "rotor-long"]:
    for lift in [0., .3]:
        for foot_present in [True, False]:
            pin_local = solid(meshes["pin-50"])
            if not foot_present:
                pin_local = pin_local ^ box([4.4, 4.4, 50.01], [-2.2, -2.2, -.001])
            pin = pin_local.translate([0, 0, 27.9+15+lift])
            rotor = solid(translated(rotated(rotors[rotor_name], -120*15), [0, 0, lift]))
            frame_volume = overlap(pin, frame)
            assert (frame_volume > TOL) == foot_present
            row = dict(rotor=rotor_name, pin="actual_pin_50_mesh",
                       reported_rise_mm=15, rotor_lift_mm=lift,
                       retained_foot=foot_present, pin_frame_mm3=frame_volume,
                       rotor_pin_mm3=overlap(rotor, pin),
                       rotor_frame_mm3=overlap(rotor, frame),
                       nominal_thread_axial_overlap_mm=0 if rotor_name=="rotor" else 6,
                       nominal_guide_overlap_mm=29.8-lift)
            assert row["rotor_pin_mm3"] < TOL and row["rotor_frame_mm3"] < TOL
            owner_height_checks.append(row)

footless_long_sweep = []
footless_long_pin = solid(meshes["pin-50"]) ^ box([4.4, 4.4, 50.01], [-2.2, -2.2, -.001])
for lift in [0., .3]:
    for travel in np.arange(0., 15.001, .5):
        pin = footless_long_pin.translate([0, 0, 27.9+float(travel)+lift])
        rotor = solid(translated(rotated(rotors["rotor-long"], -120*float(travel)), [0, 0, lift]))
        row = dict(travel_mm=float(travel), rotor_angle_deg=-120*float(travel),
                   rotor_lift_mm=lift, pin_frame_mm3=overlap(pin, frame),
                   rotor_pin_mm3=overlap(rotor, pin), rotor_frame_mm3=overlap(rotor, frame))
        assert max(row[k] for k in row if k.endswith("mm3")) < TOL, row
        footless_long_sweep.append(row)

# Complete motor-space envelopes from the existing measurement-based design;
# unmeasured appendages are explicit allowances, not precision motor contours.
envelopes = {
    "body_nominal_8": cylinder(9.2, 4, 2),
    "body_drawing_max_8_2": cylinder(9.2, 4.1, 2),
    "boss_measured_approx": cylinder(.25, 1.5, 11.2),
    "shaft_measured_approx": cylinder(3.35, .4, 11.2),
    "gear_outer_envelope_not_tooth_mesh": cylinder(1.25, 1.1, 13.2),
    "pcb_measured_approx": box([3.5, 7, 4], [-6, -3.5, 4]),
    "glue_design_allowance": box([3.5, 7.8, 2], [-6, -3.9, 2]),
    "wire_design_allowance": box([2.6, 8, 67], [-7, -4, 8]),
    "tabs_design_allowance": cylinder(1.2, 5.1, 10),
}
motor_checks = {}
for name, envelope in envelopes.items():
    values = dict(frame_mm3=overlap(envelope, frame), washer_mm3=overlap(envelope, washer),
                  rotor_mm3=overlap(envelope, solid(rotors["rotor"])))
    assert values["frame_mm3"] < TOL and values["washer_mm3"] < TOL, (name, values)
    if name != "gear_outer_envelope_not_tooth_mesh":
        assert values["rotor_mm3"] < TOL, (name, values)
    motor_checks[name] = values

spacer_checks = []
for thickness, name in [(.6, "spacer-060"), (.72, "spacer-072"), (.84, "spacer-084")]:
    shim = solid(translated(rotated(meshes[name], 90, (0, 1, 0)), [4.7-thickness, -1, 3]))
    spacer_checks.append(dict(spacer=name, thickness_mm=thickness,
                              frame_mm3=overlap(shim, frame),
                              nominal_centered_body8_mm3=overlap(shim, envelopes["body_nominal_8"]),
                              centered_body8_2_mm3=overlap(shim, envelopes["body_drawing_max_8_2"])))
assert spacer_checks[0]["nominal_centered_body8_mm3"] < TOL
assert all(r["nominal_centered_body8_mm3"] > TOL for r in spacer_checks[1:])

# Probe the actual frame: only the upper 3.7-mm band surrounds the rotor.
# Radius 3.69 is inside the nominal bore; 3.71 crosses its boundary.
journal_probes = []
for z, height, expected_band in [(13.0, 7.9, False), (21.3, 3.5, True)]:
    inner_volume = overlap(cylinder(height, 3.69, z), frame)
    outer_volume = overlap(cylinder(height, 3.71, z), frame)
    assert inner_volume < TOL
    assert (outer_volume > TOL) == expected_band
    journal_probes.append(dict(z_mm=z, height_mm=height,
                               probe_radius_3_69_mm3=inner_volume,
                               probe_radius_3_71_mm3=outer_volume))

thrust = dict(washer_frame_mm3=overlap(washer, frame),
             washer_rotor_mm3=overlap(washer, solid(rotors["rotor"])),
             lower_washer_contact_probe_mm3=overlap(washer.translate([0, 0, -.001]), frame),
             upper_washer_contact_probe_mm3=overlap(washer, solid(rotors["rotor"]).translate([0, 0, -.001])),
             upper_stop_at_lift_030_mm3=overlap(solid(rotors["rotor"]).translate([0, 0, .3]), frame),
             upper_stop_at_lift_031_mm3=overlap(solid(rotors["rotor"]).translate([0, 0, .31]), frame))
assert thrust["washer_frame_mm3"] < TOL and thrust["washer_rotor_mm3"] < TOL
assert thrust["lower_washer_contact_probe_mm3"] > TOL
assert thrust["upper_washer_contact_probe_mm3"] > TOL
assert thrust["upper_stop_at_lift_030_mm3"] < TOL
assert thrust["upper_stop_at_lift_031_mm3"] > TOL
thrust["approximate_washer_to_frame_contact_area_mm2"] = thrust["lower_washer_contact_probe_mm3"]/.001
thrust["approximate_rotor_to_washer_contact_area_mm2"] = thrust["upper_washer_contact_probe_mm3"]/.001
thrust["approximate_upper_stop_contact_area_mm2"] = thrust["upper_stop_at_lift_031_mm3"]/.01

coupling_section = solid(meshes["rotor"]).slice(1.0)
coupling_polygons = coupling_section.to_polygons()
assert len(coupling_section.decompose()) == 1 and len(coupling_polygons) == 2
coupling_radii = sorted([[float(np.linalg.norm(p, axis=1).min()),
                         float(np.linalg.norm(p, axis=1).max())]
                        for p in coupling_polygons], key=lambda r: r[1])
assert abs(coupling_radii[0][0]-1.05) < 1e-4
assert abs(coupling_radii[0][1]-1.25) < 1e-4
assert abs(coupling_radii[1][1]-3.5) < 1e-4

report = dict(
    status="DIGITAL_DIAGNOSTIC_AUDIT_PASS_NOT_A_PRINT_RELEASE",
    physical_validation="Owner reports tested v3 binding, roughly40/50-mm pin, about15-mm rise, long screw, print artifacts removed, and shaving of the coupling base only after the bad tests. Exact tested revision, extent of foot removal and post-test shaving dimensions remain unidentified. No new physical test performed.",
    source_baseline=str(BASE.relative_to(PACK.parent.parent)),
    source_sha256={str((COMPONENTS/(n+".stl")).relative_to(BASE)): sha(COMPONENTS/(n+".stl")) for n in names},
    cad_sha256=sha(BASE/"cad/rig.scad"),
    measurement_basis_sha256=sha(BASE/"metadata/motor-interface.json"),
    mesh_quality={n: dict(watertight=m.is_watertight, winding_consistent=m.is_winding_consistent,
                         connected_components=len(m.split()), bounds_mm=m.bounds.tolist())
                  for n, m in meshes.items()},
    assembly_transform="Front: Tz(-6.5), Rx(90); back: Tz(-6.5), Rx(90), Rz(180). No assembly mirror.",
    back_rotation_determinant=float(np.linalg.det(rotation_back[:3, :3])),
    frame_half_overlap_mm3=overlap(solid(front), solid(back)),
    motion_states=states,
    pin_section_measurements=pin_sections,
    boundary_probes=boundary_states,
    owner_reported_15mm_rise_checks=owner_height_checks,
    virtual_footless_long_screw_sweep_0_to_15mm=footless_long_sweep,
    travel_limits=dict(low_pin_bottom_z_mm=27.9, foot_thickness_mm=.24,
                      guide_underside_z_mm=32.7, keeper_upper_face_z_mm=27.2,
                      first_upward_foot_contact_absolute_rise_mm=4.56,
                      first_upward_contact_thread_travel_at_lift_030_mm=4.26,
                      first_downward_foot_contact_absolute_rise_mm=-.7,
                      intended_thread_travel_mm=[0, 3],
                      nominal_upper_margin_at_travel3_lift030_mm=1.26,
                      warning="Nominal CAD contact boundaries, not usable endstops or measured allowances."),
    foot_removal_counterfactual=dict(
        authorized_modification=False,
        short_screw_full_6mm_thread_overlap_until_travel_mm=7,
        short_screw_nominal_zero_overlap_at_travel_mm=13,
        long_screw_full_6mm_thread_overlap_until_travel_mm=39,
        long_screw_nominal_zero_overlap_at_travel_mm=45,
        thread_overlap_table=thread_overlap,
        tube_square_bore_mm=3.52,
        screw_nominal_outer_diameter_mm=3.2,
        nominal_straight_bore_side_gap_mm=.16,
        long_pin_remaining_guide_overlap_at_40mm_rise_mm=4.8,
        conclusion="Removing the foot alone does not qualify 40-mm travel: bearing overlap collapses, short screw disengages, and long screw/tube rubbing plus alignment remain untested."),
    motor_envelope_checks=motor_checks,
    spacer_centered_motor_interference=spacer_checks,
    journal_probes=journal_probes,
    contact_dimensions_from_cad=dict(
        rotor_diameter_mm=7, rotor_body_z_mm=[12.9, 24.9],
        rotor_radial_band_z_mm=[21.2, 24.9], radial_band_length_mm=3.7,
        radial_band_bore_mm=7.4, nominal_radial_gap_mm=.2,
        washer_pocket_diameter_mm=7.3, actual_washer_pocket_z_mm=[12.4, 12.65],
        washer_pocket_cutter_z_mm=[12.4, 12.7],
        rotor_bottom_above_actual_pocket_rim_mm=.25,
        washer_dimensions_id_od_thickness_mm=[3.2, 7, .5],
        thrust_deck_central_hole_mm=4, upper_keeper_hole_mm=4.2,
        upper_stop_bottom_z_mm=25.2, upper_stop_top_z_mm=27.2,
        square_guide_z_mm=[32.7, 72.7], square_guide_opening_mm=4.8,
        pin_square_width_mm=4.4, nominal_pin_side_gap_mm=.2,
        coupling_void_diameter_mm=2.5, coupling_lobe_radius_mm=.5,
        coupling_lobe_center_radius_mm=1.55, coupling_lobe_tip_radius_mm=1.05,
        coupling_leadin_mm=.25, coupling_void_length_mm=6,
        coupling_description="Three integral inward lobes of one continuous rotor wall. Spaces between engagement lobes; no exterior slots, separate brackets, or designed flexure hinges.",
        L_gear_straight_overlap_rest_mm=1.25, L_gear_straight_overlap_lift030_mm=1.0),
    thrust_probes=thrust,
    coupling_mesh_cross_section=dict(z_above_rotor_bottom_mm=1,
                                     material_components=1, boundary_loops=2,
                                     loop_min_max_radius_mm=coupling_radii,
                                     finding="One continuous wall around one bore; inward torque lobes are not disconnected brackets."),
    limitations=[
        "Nominal rigid meshes only; no print distortion, roughness, compliance, friction, torque or actual clearance measurement.",
        "Baseline motion states sampled at0/1.5/3 mm and rotor lift0/.3; virtual footless long-screw sweep sampled each0.5 mm through15 mm at both lifts. Neither is a continuous motion proof.",
        "Actual gear teeth, exact tabs, glue and wire routing are not measured contours; only gear-envelope/rib overlap is intentional.",
        "The washer carries downward rotor reaction; upward rotor reaction reaches the printed upper keeper after0.3 mm lift. Rotation direction alone does not determine axial reaction.",
        "No nominal axial gear/boss/shaft collision does not prove zero shaft load: a tight or misaligned coupling can transmit side load and frictional axial load.",
        "The current pin foot is retained. Actual owner parts may differ; identify them before using these coordinates.",
        "Owner removal of print artifacts is represented only by virtual removal of the protruding foot. Unmeasured hand shaving of the coupling base is not modeled and may change axial stack or engagement.",
    ],
)
output = PACK / "metadata/geometry-review.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(dict(status=report["status"], motion_states=len(states),
                      boundary_probes=len(boundary_states),
                      first_upward_contact_mm=4.56,
                      output=str(output.relative_to(PACK))), indent=2))
