#!/usr/bin/env python3
"""Independent mesh checks, no geometry mutation or implicit contact exclusions."""
from pathlib import Path
import importlib.util,json,itertools,hashlib,math
import numpy as np
import trimesh as tm
import manifold3d as md
HERE=Path(__file__).resolve().parent;CAD=HERE.parent/'cad'
s=importlib.util.spec_from_file_location('cad',CAD/'generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for name in ['frame-back','frame-front','row-selector','column-selector','input-shaft','rotor','screw','pin','row-holder','column-holder','hand-key','screw-tree']:
 g.MESHES[name]=tm.load(CAD/'parts'/(name+'.stl'),force='mesh')
 assert g.MESHES[name].is_watertight and len(g.MESHES[name].split())==1,name
def solid(m):
 o=md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
 assert o.status()==md.Error.NoError,o.status()
 return o
cache={};checks=0;fails=[];states=[]
def check(parts,label):
 global checks
 ss={}
 for n,m in parts.items():
  key=hashlib.sha256(m.vertices.tobytes()+m.faces.tobytes()).hexdigest()
  if key not in cache:cache[key]=solid(m)
  ss[n]=cache[key]
 for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
  if np.any(a.bounds[1]<b.bounds[0]+1e-7) or np.any(b.bounds[1]<a.bounds[0]+1e-7):continue
  checks+=1;v=abs((ss[na]^ss[nb]).volume())
  if v>1e-5:fails.append(dict(state=label,a=na,b=nb,intersection_volume_mm3=v))
for r,c0,c1 in itertools.product([0,1],repeat=3):
 label=f'mask_{r}{c0}{c1}';check(g.assembly(r,(c0,c1)),label);states.append(label)
# Stroke poses use holders removed: the real protocol must remove locks before moving.
for path in ['all','row','columns']:
 for t in np.linspace(0,1,31):
  r,c=(t,(t,t)) if path=='all' else ((t,(0,1)) if path=='row' else (1,(t,1-t)))
  parts={n:m for n,m in g.assembly(float(r),tuple(map(float,c))).items() if 'holder' not in n}
  label=f'stroke_{path}_{t:.4f}';check(parts,label);states.append(label)
# Selected input/output rotation and unselected neighbour input rotation. Screw lead sign
# follows the existing E295/E297 actual right-hand mesh: +rotation lowers pin.
for r,c0,c1 in itertools.product([0,1],repeat=3):
 for alpha in [-90,-45,45,90]:
  c=(c0,c1);sel=[bool(r and cc) for cc in c]
  phases=tuple(90+alpha if s else 90 for s in sel)
  travel=tuple(-3*alpha/360 if s else 0 for s in sel)
  parts=g.assembly(r,c,phases,travel)
  for j,x in enumerate([-g.P/2,g.P/2]):
   for name in [f'input-{j}',f'lower-{j}']:
    m=parts[name];m.apply_translation([-x,0,0]);m=g.rotate(m,[0,0,1],alpha);m.apply_translation([x,0,0]);parts[name]=m
  label=f'drive_{r}{c0}{c1}_{alpha}';check(parts,label);states.append(label)
# Two preassembled halves approach parallel to Y with everything OFF. This checks the
# stated inlay/mating route at 0.5-mm intervals, not a force or assembly dexterity model.
base=g.assembly(0,(0,0))
front_names=[n for n in base if n=='frame-front' or n.startswith(('column','upper','screw','pin'))]
for dy in np.linspace(0,15,31):
 parts={n:(g.shift(m,[0,float(dy),0]) if n in front_names else m.copy()) for n,m in base.items()}
 label=f'frame_mating_y_{dy:.2f}';check(parts,label);states.append(label)
# Conservative continuous selector sweeps: Minkowski sum by a vertical segment
# thickened by 0.00001 mm in XY/Z, intersected with the actual fixed frame meshes.
frame=solid(g.MESHES['frame-back'])+solid(g.MESHES['frame-front'])
sweeps=[]
for name,base,dz in [('row',g.assembly(0,(0,0))['row'],3),('column-0',g.assembly(0,(0,0))['column-0'],-3),('column-1',g.assembly(0,(0,0))['column-1'],-3)]:
 eps=.00001
 segment=md.Manifold.cube([2*eps,2*eps,abs(dz)+2*eps]).translate([-eps,-eps,min(0,dz)-eps])
 sweep=solid(base).minkowski_sum(segment)
 volume=abs((sweep^frame).volume());checks+=1
 sweeps.append(dict(part=name,travel_mm=dz,conservative_padding_mm=eps,frame_intersection_volume_mm3=volume))
 if volume>1e-5:fails.append(dict(state='continuous_selector_sweep',a=name,b='frame',intersection_volume_mm3=volume))
# Explicit feasible finite phase-search path: the input rotates, output initially
# stays fixed, and column insertion is limited by actual dog contact. Contact
# pressure, friction and passive dynamics are not solved.
phase_path=[]
for alpha in [0,15,30,45,60,75,76,80,90]:
 lo,hi=0.,1.
 def pose(cc):
  aa=g.assembly(1,(cc,0),phase=(0,90),travels=(.75,0));aa.pop('column-holder-0',None)
  for n in ['input-0','lower-0']:
   m=aa[n];m.apply_translation([g.P/2,0,0]);m=g.rotate(m,[0,0,1],alpha);m.apply_translation([-g.P/2,0,0]);aa[n]=m
  return aa
 a=pose(1)
 if abs((solid(a['lower-0'])^solid(a['upper-0'])).volume())<1e-8:cc=1.
 else:
  for _ in range(20):
   mid=(lo+hi)/2;a=pose(mid)
   if abs((solid(a['lower-0'])^solid(a['upper-0'])).volume())<1e-8:lo=mid
   else:hi=mid
  cc=max(0,lo-.0001)
 label=f'phase_search_input_{alpha}_column_{cc:.5f}';check(pose(cc),label);states.append(label)
 phase_path.append(dict(input_rotation_deg=alpha,column_fraction=cc,fully_inserted=cc==1))
assert phase_path[0]['column_fraction']<1 and phase_path[-1]['fully_inserted']
# Physical axial support begins at first mesh overlap; binary contact thresholds
# are estimates for the triangulated nominal surfaces, not physical measurements.
axial=[]
a=g.assembly(0,(0,0));ss=solid(a['screw-0']);rr=solid(a['upper-0'])
for direction,bound in [('down',-.35),('up',.35)]:
 lo,hi=0.,abs(bound)
 for _ in range(25):
  mid=(lo+hi)/2;dz=-mid if direction=='down' else mid
  if abs((ss.translate([0,0,dz])^frame).volume())>1e-7:hi=mid
  else:lo=mid
 dz=-lo if direction=='down' else lo
 axial.append(dict(direction=direction,first_frame_contact_dz_mm=dz,rotor_intersection_at_frame_contact_mm3=abs((ss.translate([0,0,dz])^rr).volume())))
record=dict(evidence='Actual exported mesh intersections at finite poses. No physical qualification.',checks=checks,states=states,unexpected_intersections=fails,exclusions=[],continuous_selector_sweeps=sweeps,active_phase_search_path=phase_path,screw_axial_support=axial,mesh_sha256={name:hashlib.sha256((CAD/'parts'/(name+'.stl')).read_bytes()).hexdigest() for name in g.MESHES})
(HERE/'geometry-review.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(checks=checks,poses=len(states),failures=fails),indent=2))

assert not fails, f"{len(fails)} unexpected mesh intersections"
