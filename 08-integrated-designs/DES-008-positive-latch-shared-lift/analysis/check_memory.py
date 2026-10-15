#!/usr/bin/env python3
"""Revision 3: regenerate meshes, test nominal clearance and conditional capture bounds."""
from pathlib import Path
import subprocess,json,math,hashlib,argparse,shutil
import trimesh
SOURCE=Path(__file__).resolve().parents[1]/'cad/memory_coupon.scad'
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('work/des008-memory'))
ROOT=p.parse_args().output;ROOT.mkdir(parents=True,exist_ok=True)
shutil.copyfile(SOURCE,ROOT/'memory_coupon.scad')
CHECKS=ROOT/'checks';CHECKS.mkdir(exist_ok=True)
results={'revision':3,'source_sha256':hashlib.sha256((ROOT/'memory_coupon.scad').read_bytes()).hexdigest()}
for name in ['base','cassette','flag','flag_support','supported_flag','codebar','shim','keeper','key','plate']:
 p=ROOT/(name+'.stl')
 run=subprocess.run(['openscad','-o',str(p),'-D',f'part="{name}"',str(ROOT/'memory_coupon.scad')],capture_output=True,text=True)
 if run.returncode:raise RuntimeError(run.stderr)
 mesh=trimesh.load(p)
 results[name]={'watertight':bool(mesh.is_watertight),'volume_mm3':float(mesh.volume),'bounds_mm':mesh.bounds.tolist(),'components':len(mesh.split())}
 assert mesh.is_watertight and mesh.bounds[0,2]>-1e-5
assert results['plate']['components']==19
results['solid_PLA_g_at_1p24']=results['plate']['volume_mm3']*.00124
checks=[]
def record(name,body):checks.append((name,body))
fixed='union(){base();for(y=[4,28])translate([0,y,11])keeper();}'
for b in [0,1]:
 for lift in [0,.4,.8,1.2,1.6,2,2.1,2.4,2.7]:
  record(f'flag_old{b}_lift{lift}',f'''intersection(){{
   translate([12+2*{b},12,1.4+{lift}])flag();
   union(){{{fixed}translate([0,12,3.9+{lift}])cassette();translate([12+2*{b},0,9.9])codebar();}}
  }}''')
  record(f'cassette_lift{lift}_code{b}',f'''intersection(){{
   translate([0,12,3.9+{lift}])cassette();
   union(){{{fixed}translate([12+2*{b},0,9.9])codebar();}}
  }}''')
for b in [0,.25,.5,.75,1]:
 record(f'flag_write{b}',f'''intersection(){{
  translate([12+2*{b},12,4.1])flag();
  union(){{{fixed}translate([0,12,6.6])cassette();translate([12+2*{b},0,9.9])codebar();}}
 }}''')
for old in [0,1]:
 for code in [0,.5,1]:
  record(f'neighbor{old}_code{code}',f'''intersection(){{
   translate([12+2*{old},18.35,1.4])flag();translate([12+2*{code},0,9.9])codebar();
  }}''')
for a in [0,1]:
 for b in [0,1]:
  record(f'adjacent_bars{a}{b}',f'''intersection(){{
   translate([12+2*{a},0,9.9])codebar();translate([18.35+2*{b},0,9.9])codebar();
  }}''')
  record(f'adjacent_flags{a}{b}',f'''intersection(){{
   translate([12+2*{a},12,4.1])flag();translate([18.35+2*{b},12,4.1])flag();
  }}''')
for x in [12,18.35]:
 for b in [0,.5,1]:
  record(f'bar{x}_state{b}_fixed',f'''intersection(){{translate([{x}+2*{b},0,9.9])codebar();{fixed}}}''')
for lift in [0,1.35,2.7]:
 record(f'cassette_neighbor_lift{lift}',f'''intersection(){{translate([0,12,3.9+{lift}])cassette();translate([0,18.35,3.9])cassette();}}''')
for y in [4,28]:
 record(f'keeper{y}_base','intersection(){translate([0,'+str(y)+',11])keeper();base();}')
 for x in [5,27]:
  record(f'key{x}_{y}',f'''intersection(){{translate([{x},{y}-3,11.5])key();union(){{base();translate([0,{y},11])keeper();}}}}''')
# Insertion occurs off the base: lower through the loading port, then slide left.
for z in [-2.5,-1.5,0,1.5,3]:
 record(f'load_port_z{z}',f'intersection(){{cassette();translate([25.35,0,{z}])flag();}}')
for x in [25.35,24,22.5,20.35,18.35,16,14,12]:
 record(f'load_slide_x{x}',f'intersection(){{cassette();translate([{x},0,-2.5])flag();}}')
source='include <../memory_coupon.scad>\n'+'\n'.join(f'translate([{100*i},0,0]){{{body}}}' for i,(_,body) in enumerate(checks))
(CHECKS/'collision_check.scad').write_text(source)
run=subprocess.run(['openscad','-o',str(CHECKS/'collision_check.stl'),'-D','part="none"',str(CHECKS/'collision_check.scad')],capture_output=True,text=True)
empty='Current top level object is empty' in run.stderr
contact_volume=0.0 if empty else float(abs(trimesh.load(CHECKS/'collision_check.stl').volume))
results['nominal_collision_checks']={'count':len(checks),'all_no_positive_overlap':contact_volume<1e-7,'intersection_volume_mm3':contact_volume,'case_names':[n for n,_ in checks],'note':'Zero-thickness seating contact may remain; no positive volume allowed. Samples, not a continuum or tolerance proof.'}
if contact_volume>=1e-7:raise RuntimeError('Unexpected positive-volume collision: '+run.stderr)
(CHECKS/'wrong_old_check.scad').write_text('''include <../memory_coupon.scad>
intersection(){translate([12,12,4.1])flag();translate([14,0,9.9])codebar();}
''')
run=subprocess.run(['openscad','-o',str(CHECKS/'wrong_old_check.stl'),'-D','part="none"',str(CHECKS/'wrong_old_check.scad')],capture_output=True,text=True)
mesh=trimesh.load(CHECKS/'wrong_old_check.stl')
results['wrong_old_blocked']={'intersection_mm3':float(mesh.volume),'blocked':bool(mesh.volume>0)}
assert mesh.volume>0
# Restricted planar screen, not an acceptance envelope. Dimensions need measurement.
# The captured shoulder limits planar flag tilt. The minimum in-plane width bounds
# the stated planar tilt only. Coupled yaw/translation/tilt is not bounded here.
post_angle=math.atan(.6/9.8)
shoulder_width_min=3.3
shoulder_thickness_min=1.1
vertical_clearance_max=.3
# W sin(theta)+T cos(theta)=T+clearance; smaller positive root.
shoulder_angle=math.asin((shoulder_thickness_min+vertical_clearance_max)/math.hypot(shoulder_width_min,shoulder_thickness_min))-math.atan2(shoulder_thickness_min,shoulder_width_min)
theta=post_angle+shoulder_angle
transverse_diagonal=math.hypot(1.2,2.6)
remaining=7.9*math.cos(theta)-transverse_diagonal*math.sin(theta)-6.5-.5
results['restricted_planar_screen']={
 'nominal_mm':1.6,'maximum_diametral_post_hole_gap_mm':.6,'minimum_effective_guide_length_mm':9.8,
 'maximum_cassette_tilt_deg':math.degrees(post_angle),'minimum_shoulder_inplane_width_mm':shoulder_width_min,
 'minimum_shoulder_thickness_mm':shoulder_thickness_min,'maximum_shoulder_slot_vertical_clearance_mm':vertical_clearance_max,
 'maximum_independent_flag_tilt_deg':math.degrees(shoulder_angle),'maximum_combined_tilt_deg':math.degrees(theta),
 'minimum_flag_height_mm':7.9,'maximum_lug_width_mm':1.2,'maximum_foot_and_lug_depth_mm':2.6,
 'maximum_lug_or_foot_transverse_diagonal_mm':transverse_diagonal,
 'maximum_floor_to_channel_gap_without_lift_mm':6.5,'maximum_measured_local_codebar_vertical_lift_mm':.5,
 'calculated_planar_full_face_overlap_mm':remaining,
 'nominal_key_and_keeper_vertical_lift_mm':.4,
 'statement':'Restricted planar screen only: zero shoulder yaw and all extreme shoulder points remain beneath the floor/roof retaining rails. Adds cassette tilt and independent flag tilt, with hypothetical measured dimensional limits. NOT a general tolerance or configuration-space guarantee: coupled yaw/translation/tilt and elastic deflection remain unqualified. Codebar play must be measured locally at BOTH rows.'}
assert remaining>.3
results['release_and_idle_nominal_mm']={'row_lift':2.7,'foot_engagement':2.1,'raised_foot_floor_clearance':.6,'idle_lug_channel_clearance':.5,'raised_lug_roof_clearance':.4,'cassette_to_bar_raised_clearance':.3,'cassette_to_neighbor_clearance':.95}
results['loading_port']={'x_center_mm':25.35,'roof_window_bounds_x_mm':[23.2,27.5],'second_flag_max_operating_right_edge_mm':22.05,'nominal_separation_mm':1.15,'note':'Load flags off the base. Slide first flag to left column; then load second. Only codebar/pocket-controlled positions are operational.'}
results['print_process_review']={'base':'pockets upward','cassette':'long side down; 2.9 mm guide-hole roof bridges','flag':'wide shoulder side down; two sacrificial end towers anchor 3.6 / 3.8 mm bridges. Clip one-layer necks only at the foot bottom and lug top. No support contacts functional side walls; bridged side surfaces require inspection and measurement.','keeper':'inverted, sockets upward','codebar':'inverted closed roof down; no channel bridge','transverse_key_holes':'2 mm bridge span','slicer_revision_3':'Separate PrusaSlicer 2.7.4 comparison: 11.02 g, 2h 1m 24s, 1 mm brim, supports off, no warnings. Flag first spanning layer at Z=0.96 mm is anchored to its shoulder and end towers; slicer labels these thin paths Overhang perimeter, not Bridge infill. Physical bridging remains untested.'}
(ROOT/'validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
