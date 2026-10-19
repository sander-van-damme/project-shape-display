#!/usr/bin/env python3
"""Conditional analytic tooth/lobe screen, NOT measured gear fitting evidence."""
from pathlib import Path
from paths import TEST_DIR, CAD, COMPONENTS, METADATA, IMAGES
import json
import math

H = TEST_DIR
module, teeth, pressure_angle = .2, 9, math.radians(20)
pitch_r = module * teeth / 2
base_r = pitch_r * math.cos(pressure_angle)
outer_r = 1.1
inv = lambda a: math.tan(a) - a
variants = []
for name, tip_r in [('C', 1.05)]:
    samples = []
    for i in range(10001):
        r = max(base_r, tip_r) + (outer_r - max(base_r, tip_r)) * i / 10000
        tooth_half_angle = math.pi / (2 * teeth) + inv(pressure_angle) - inv(math.acos(base_r / r))
        available_half_gap = math.pi / teeth - tooth_half_angle
        lobe_center = tip_r + .5
        lobe_half_angle = math.acos(max(-1, min(1, (lobe_center**2 + r*r - .5**2) / (2*lobe_center*r))))
        angle_clearance = available_half_gap - lobe_half_angle
        samples.append((r * angle_clearance, r, math.degrees(angle_clearance)))
    arc_clearance, radius, angle = min(samples)
    variants.append(dict(name=name, lobe_tip_radius_mm=tip_r,
                         nominal_radial_tip_engagement_mm=outer_r-tip_r,
                         minimum_angular_arc_clearance_mm=arc_clearance,
                         radius_at_minimum_mm=radius, angular_clearance_degrees=angle,
                         assumed_profile_has_overlap=arc_clearance < 0))

report = dict(
    scope='Conditional analytic CAD screen of ideal aligned teeth and continuous circular lobes; not physical fitting or manufactured tolerance verification',
    source='E-301 motor-dimensions-original.jpg, also supplied by owner in revision request; source annotations, not owner measurements',
    source_annotations=dict(gear_outer_diameter_mm=2.2, teeth=teeth, module_mm=module, motor_body_diameter_mm=8, motor_body_height_mm=8.2, total_shaft_gear_projection_mm=4),
    assumptions=dict(pressure_angle_deg=20, standard_unshifted_involute=True, nominal_pitch_diameter_mm=2*pitch_r, ideal_concentric_alignment=True, gear_space_alignment='Every third tooth gap receives one of three lobes'),
    socket=dict(main_bore_diameter_mm=2.5, round_lobe_radius_mm=.5, lobe_count=3, plain_bore_radial_tip_clearance_mm=.15, straight_lobe_z_mm=[13.7, 19.5], photo_gear_top_z_mm=14.2, gear_top_to_socket_roof_mm=5.3),
    variants=variants,
    limitations=[
        '20-degree pressure angle, profile shift, tooth shape and root geometry are not supplied or measured; a nine-tooth gear can be undercut or nonstandard.',
        'Arc clearance is a same-radius angular gap, not a guaranteed minimum Euclidean manufacturing clearance.',
        'Owner selected original C by hand fit; the 2 mm shorter C still needs physical overlap and powered-motion verification.',
        'Printed contours, shrinkage, eccentricity, debris, tooth length and second-motor protrusion are not represented.',
        'Photo four-mm dimension is total shaft-plus-gear projection, not gear tooth length.',
        'Axial overlap cannot be certified without measuring tooth lower/upper heights; require at least .6mm actual overlap with straight lobes and no contact with shaft shoulder or roof.',
        'No fit, torque, service life or motor stability pass is claimed.'
    ])
(METADATA / 'dimension-review.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
