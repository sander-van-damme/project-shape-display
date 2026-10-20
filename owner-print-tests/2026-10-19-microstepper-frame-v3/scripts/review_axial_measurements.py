"""Nominal axial re-evaluation from owner ruler measurements; no fit qualification."""
import json
from paths import METADATA
basis = json.loads((METADATA/'motor-interface.json').read_text())
measurements = json.loads((METADATA/'owner-motor-measurements.json').read_text())
top = basis['motor_base_z_mm'] + basis['body_height_mm']
rows = []
for name, m in measurements['variants'].items():
    bottom, tip = top+m['gear_bottom_mm'], top+m['gear_top_mm']
    for label, mouth, lead in [('legacy',12.2,.5),('blind_1mm_shift',13.2,.5),
                              ('corrected',basis['rotor_z_mm'],basis['lead_in_mm'])]:
        overlap = [max(0, min(tip, mouth+6+lift)-max(bottom, mouth+lead+lift))
                   for lift in [0, .3]]
        rows.append(dict(variant=name, geometry=label,
                         gear_z_mm=[bottom, tip], overlap_at_lift_0_and_030_mm=overlap,
                         shaft_roof_clearance_mm=mouth+6-tip-measurements['shaft_above_gear_mm'],
                         mouth_boss_clearance_mm=mouth-top-m['boss_height_mm']))
selected = next(r for r in rows if r['variant']=='L' and r['geometry']=='corrected')
assert min(selected['overlap_at_lift_0_and_030_mm']) >= .6
# Sensitivity only: deliberately assumed +/-0.2 mm endpoint error, not measured tolerance.
selected['overlap_with_assumed_top_minus_020_and_bottom_plus_020_mm'] = max(0,
    min(top+3.25-.2, basis['rotor_z_mm']+6+.3)-max(top+2+.2,basis['rotor_z_mm']+.25+.3))
report = dict(status=basis['status'], scope='Nominal axial intervals and labelled sensitivity, not physical fit',
              housing_top_z_mm=top, calculations=rows, selected_variant='L',
              production_geometry_changed=True)
(METADATA/'axial-measurement-review.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
