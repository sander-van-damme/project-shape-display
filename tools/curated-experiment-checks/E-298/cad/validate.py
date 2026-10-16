#!/usr/bin/env python3
"""Actual new exported solids: fixed-state matrix and phase contact checks."""
import importlib.util,json,itertools,hashlib
from pathlib import Path
import trimesh as tm
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('gen',HERE/'generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
o=g.old
for name in ['frame-left','frame-center','frame-right','row-selector','input-shaft','screw','pin','hand-key','stop-spacer','reaction-jig']:
 o.MESHES[name]=tm.load(g.OUT/(name+'.stl'),force='mesh')
o.MESHES['rotor']=tm.load(g.OUT/'point48.stl',force='mesh')
fail=[];checks=0;states=[]
for mask in itertools.product([0,1],repeat=4):
 pp=o.assembly(mask[:2],mask[2:]);pp['reaction-jig']=o.shift(o.MESHES['reaction-jig'],[0,0,-2.2])
 solids={k:o.solid(m) for k,m in pp.items()}
 local=0
 for (na,a),(nb,b) in itertools.combinations(pp.items(),2):
  if (a.bounds[1]<b.bounds[0]).any() or (b.bounds[1]<a.bounds[0]).any():continue
  checks+=1;local+=1;v=abs((solids[na]^solids[nb]).volume())
  if v>1e-5:fail.append(dict(mask=mask,a=na,b=nb,volume=v))
 states.append(dict(mask=mask,bounding_box_candidate_boolean_count=local))
subset={}
original=o.solid(tm.load(g.OLD/'parts/rotor.stl',force='mesh'))
for name in g.VARIANTS:
 new=o.solid(tm.load(g.OUT/(name+'.stl'),force='mesh'))
 outside=abs((new-original).volume())
 subset[name]=dict(volume_outside_E297_mm3=outside,strict_mesh_subset=outside<1e-4,note='Different polygonal arc sampling: old 24 vs new 25 vertices per arc; not a literal mesh subset. Same nominal radial envelope, separately collision checked.')
 print(name,"outside",outside,flush=True)
phase=[]
for name in g.VARIANTS:
 a=o.solid(tm.load(g.OUT/(name+'.stl'),force='mesh'))
 for phi in [0,7.64,12,24,45,75,76,77,90,103,104,105,135,180]:
  # Relative mating face roots 3.36 mm at full commanded engagement.
  b=a.rotate([180,0,0]).rotate([0,0,phi]).translate([0,0,15.76])
  v=abs((a^b).volume());phase.append(dict(variant=name,phase_deg=phi,full_command_collision_volume_mm3=v,full_command_possible=v<1e-5))
  if phi==90:assert v<1e-5
  if phi==0:assert v>1e-5
# Unchanged E297 source meshes must remain byte-identical, including real threaded meshes.
unchanged={}
for name in ['frame-left','frame-center','frame-right','row-selector','single-comb','input-shaft','screw','pin','hand-key','stop-spacer','coupon-shaft']:
 for suff in ['.stl','-print.stl','.step']:
  p=g.OUT/(name+suff);source=g.OLD/'parts'/(name+suff)
  if source.exists():assert p.read_bytes()==source.read_bytes();unchanged[name+suff]=hashlib.sha256(p.read_bytes()).hexdigest()
record=dict(evidence='CAD and finite rigid mesh intersections only; no physical qualification',states=states,new_rotor_within_original_envelope=subset,intersection_checks=checks,unexpected_intersections=fail,phase_tests=phase,unchanged_E297_source_sha256=unchanged,reaction_jig=dict(assembled_plate_top_z=-.2,plug_top_z=2.19,input_socket_bottom_z=1.19,nominal_socket_engagement_mm=1.0,radial_clearance=.15,positive_end_clearance_mm=.21),pass_nominal=not fail)
(HERE/'validation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(checks=checks,failures=fail),indent=2));assert not fail
