#!/usr/bin/env python3
"""Independent E302 rigid CAD clearance screen; not physical fit verification.
Run with numpy, trimesh and manifold3d. Reads existing meshes only.
"""
from pathlib import Path
from paths import TEST_DIR, CAD, COMPONENTS, METADATA, IMAGES
import json, hashlib, io, subprocess
import numpy as np
import trimesh
import manifold3d as md
H=TEST_DIR
OLD=H.parent/'2026-10-17-microstepper-screw-pin'
def load(path): return trimesh.load(path,force='mesh')
def solid(mesh):return md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
def rotate(m,deg,axis=[0,0,1]):
 m=m.copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg),axis));return m
def shift(m,v):m=m.copy();m.apply_translation(v);return m
front=rotate(load(COMPONENTS / 'half-front.stl'),-90,[1,0,0])
back=rotate(load(COMPONENTS / 'half-back.stl'),-90,[1,0,0])
frame=solid(front)+solid(rotate(back,180))
cups={n:rotate(shift(load(COMPONENTS/f'coupling-{n}.stl'),[0,0,-28.8]),180,[1,0,0]) for n in ['C']}
screw=shift(load(COMPONENTS / 'screw.stl'),[0,0,26.2]);pin=shift(load(COMPONENTS / 'pin-50.stl'),[0,0,33.1])
results=[]
for a in np.linspace(0,360,25):
 # Clockwise rotation viewed from above raises the antirotating right-hand nut.
 s=solid(rotate(screw,-a));p=solid(shift(pin,[0,0,3*a/360-1.5]))
 for name,c in cups.items():
  rotor=solid(rotate(c,-a));results.append(dict(angle_deg=float(a),variant=name,cup_frame_mm3=(rotor^frame).volume(),cup_screw_mm3=(rotor^s).volume(),screw_frame_mm3=(s^frame).volume(),pin_frame_mm3=(p^frame).volume(),screw_pin_mm3=(s^p).volume()))
maxima={k:max(r[k] for r in results) for k in results[0] if k.endswith('_mm3')}
assert max(maxima.values())<1e-4,maxima
# Rigid nominal body intentionally intersects compliant contacts; quantify, do not treat as fit failure.
body=md.Manifold.cylinder(7.2,4,4,128).translate([0,0,2])
# This is the designed OPEN volume, deliberately not a fictional measured PCB.
pcb_open=md.Manifold.cube([5.5,7,8.5]).translate([-8,-3.5,2])
pcb_collision=(pcb_open^frame).volume()
assert pcb_collision < 1e-4, pcb_collision
# Opposite side retains rigid cradle support at the same height.
opposite=md.Manifold.cube([2.5,7,7.2]).translate([4.5,-3.5,2])
opposite_support=(opposite^frame).volume()
assert opposite_support > 1, opposite_support
assert abs(load(COMPONENTS / 'pin-50.stl').extents[2]-50)<.001
original_pin=solid(load(COMPONENTS / 'pin-18.stl'))
lower_pin=solid(load(COMPONENTS / 'pin-50.stl')) ^ md.Manifold.cube([30,30,18]).translate([-15,-15,0])
lower_difference=(lower_pin-original_pin).volume()+(original_pin-lower_pin).volume()
assert lower_difference < 1e-4, lower_difference
assert (COMPONENTS / 'screw.stl').read_bytes() == (OLD/'screw.stl').read_bytes()
assert (COMPONENTS / 'pin-18.stl').read_bytes() == (OLD/'pin.stl').read_bytes()

# New long screw: retain the original foot and thread phase up to the old
# tip taper, then validate the complete shaft inside the existing 50 mm pin.
long_mesh=load(COMPONENTS / 'screw-long.stl')
assert long_mesh.is_watertight and long_mesh.is_winding_consistent
assert len(long_mesh.split()) == 1
assert np.allclose(long_mesh.extents,[10,10,50.4],atol=.001)
lower_clip=md.Manifold.cube([20,20,17.799]).translate([-10,-10,0])
short_lower=solid(load(COMPONENTS / 'screw.stl')) ^ lower_clip
long_lower=solid(long_mesh) ^ lower_clip
long_lower_difference=(short_lower-long_lower).volume()+(long_lower-short_lower).volume()
assert long_lower_difference < .001, long_lower_difference
long_screw=shift(long_mesh,[0,0,26.2])
long_rows=[]
for a in np.linspace(0,360,25):
 s=solid(rotate(long_screw,-a))
 pin_bottom=31.6+3*a/360
 p=solid(shift(load(COMPONENTS / 'pin-50.stl'),[0,0,pin_bottom]))
 # The 3.52 mm square bore starts 6 mm above the pin's bottom. It must
 # contain the thread's complete 3.2 mm major diameter throughout travel.
 upper_region=md.Manifold.cube([20,20,44]).translate([-10,-10,pin_bottom+6])
 upper_pin=p ^ upper_region
 row=dict(screw_rotation_deg=float(-a),pin_bottom_z_mm=float(pin_bottom),
          screw_pin_mm3=(s^p).volume(),screw_upper_pin_mm3=(s^upper_pin).volume(),
          screw_frame_mm3=(s^frame).volume(),pin_frame_mm3=(p^frame).volume(),
          screw_tip_below_pin_top_mm=float(pin_bottom+50-76.6),
          full_thread_engagement_mm=6.0)
 for name,c in cups.items():
  row[f'screw_cup_{name}_mm3']=(s^solid(rotate(c,-a))).volume()
 long_rows.append(row)
long_maxima={k:max(r[k] for r in long_rows) for k in long_rows[0] if k.endswith('_mm3')}
assert max(long_maxima.values()) < 1e-4, long_maxima
long_review=dict(
 overall_height_mm=50.4,thread_length_mm=48,foot_dimensions_mm=[10,10,2.4],
 original_lower_screw_symmetric_difference_mm3=long_lower_difference,
 original_lower_comparison_z_mm=[0,17.799],
 shaft_nominal_major_diameter_mm=3.2,upper_pin_square_bore_width_mm=3.52,
 upper_pin_bore_minimum_radial_clearance_mm=.16,
 screw_tip_assembled_z_mm=76.6,minimum_tip_below_pin_top_mm=min(r['screw_tip_below_pin_top_mm'] for r in long_rows),
 full_thread_engagement_mm=6,pin_travel_mm=3,sampled_poses=len(long_rows),
 maximum_collision_volume_mm3=long_maxima,poses=long_rows,
 limitations=['CAD clearance does not prove thread fit after upright braced printing.',
              'Support removal can mark the thread; hand-fit before motor operation.',
              'Only the existing 3 mm travel is screened; the longer screw does not qualify additional travel.'])
(METADATA / 'long-screw-cad-review.json').write_text(json.dumps(long_review,indent=2)+'\n')
report=dict(scope='Independent nominal rigid CAD clearance screen, not physical fit or spring force validation',source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [CAD / 'rig.scad',COMPONENTS / 'half-front.stl',COMPONENTS / 'half-back.stl',COMPONENTS / 'pin-50.stl',COMPONENTS / 'pin-18.stl',COMPONENTS / 'screw.stl',*[COMPONENTS/f'coupling-{n}.stl' for n in ['C']]]},rotation_positions=25,variants=['C'],pin_height_mm=50,pin_lower_18mm_original_symmetric_difference_mm3=lower_difference,pin_travel_mm=3,pin_top_above_frame_mm=[37.6,40.6],maximum_collision_volume_mm3=maxima,pcb_open_design_volume_bounds_mm=[[-8,-3.5,2],[-2.5,3.5,10.5]],pcb_open_design_volume_frame_collision_mm3=pcb_collision,opposite_side_support_mm3=opposite_support,nominal_motor_body_contact_interference_mm3=(body^frame).volume(),nominal_clearances_mm=dict(socket_mouth_assembled_z=13.2,coupling_total_height=15.6,shortening=2.0,socket_shoulder_to_thrust_deck=.49,journal_diametral=.5,screw_foot_to_keeper=.3,source_photo_gear_tip_to_socket_roof=5.3),limitations=['Motor PCB/flange extent and second gear height are unmeasured; design open-volume clearance is not evidence that the real PCB fits.','Motor compliant contact interference is intentional; actual force and printed deflection unknown.','No motor tooth profile fabricated for this screen: tooth entry and torque transmission remain physical tests; see conditional dimension-review.json.','Screw/pin thread meshing not requalified; reused unchanged E301 screw and lower pin geometry.','Printability requires independent slicer layer support and contour inspection.'])
report['long_screw']={k:v for k,v in long_review.items() if k != 'poses'}
for name in ['screw-long.stl','long-screw.scad']:
 report['source_sha256'][name]=hashlib.sha256(((CAD if name.endswith('.scad') else COMPONENTS)/name).read_bytes()).hexdigest()
report['limitations'][3]='Screw/pin thread meshing screened in rigid CAD at 25 matched helical poses; physical fit and support-removal damage remain unknown.'

# Owner-requested shortening: preserve all interfaces above the removed mouth.
old_bytes=subprocess.check_output(['git','show','9a57fd6:'+str((H / 'coupling-C.stl').relative_to(H.parents[1]))],cwd=H.parents[1])
old=trimesh.load(io.BytesIO(old_bytes),file_type='stl')
new=load(COMPONENTS / 'coupling-C.stl')
assert abs(old.extents[2]-new.extents[2]-2)<.001
assert abs(new.extents[2]-15.6)<.001
clip=md.Manifold.cube([30,30,15.09]).translate([-15,-15,0])
a=solid(old)^clip;b=solid(new)^clip
retained_difference=(a-b).volume()+(b-a).volume()
assert retained_difference<1e-4
report['coupling_shortening']=dict(baseline_commit='9a57fd6',baseline_sha256=hashlib.sha256(old_bytes).hexdigest(),old_height_mm=float(old.extents[2]),new_height_mm=float(new.extents[2]),removed_height_mm=float(old.extents[2]-new.extents[2]),retained_region_print_z_mm=[0,15.09],retained_region_symmetric_difference_mm3=retained_difference,straight_lobe_assembled_z_mm=[13.7,19.5],photo_based_maximum_straight_overlap_mm=.5,physical_overlap_unknown=True)
(METADATA / 'cad-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
