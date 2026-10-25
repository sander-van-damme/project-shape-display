#!/usr/bin/env python3
"""Finite nominal interference / contact screens. No friction or physical fit qualification."""
from pathlib import Path
import importlib.util,itertools,json,math,functools,csv,hashlib
import numpy as np
import trimesh as tm
H=Path(__file__).resolve().parent;P=H.parent
s=importlib.util.spec_from_file_location('cad',P/'cad/generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for name in json.load(open(P/'metadata/meshes.json')):g.PART[name]=tm.load(g.ENG/(name+'.stl'))
g.follower=functools.lru_cache(maxsize=64)(g.follower)
def collisions(a):
 ms={k:g.mani(m) for k,m in a.items()};out=[];contacts=[];checks=0
 for i,j in itertools.combinations(a,2):
  if np.any(np.minimum(a[i].bounds[1],a[j].bounds[1])-np.maximum(a[i].bounds[0],a[j].bounds[0])<-.0001):continue
  v=(ms[i]^ms[j]).volume();checks+=1
  if v>.001:
   record={'a':i,'b':j,'volume_mm3':v}
   expected=i.startswith('rotor-') and j=='output-'+i.split('-')[-1] and v<.02
   (contacts if expected else out).append(record)
 return {'unexpected':out,'nominal_faceted_cone_contact':contacts,'checks':checks}
reports={}
for bits in itertools.product([0,1],repeat=4):
 name='mask-'+''.join(map(str,bits));reports[name]=collisions(g.assembly(bits[:2],bits[2:]));print(name,len(reports[name]['unexpected']),flush=True)
for value in [.25,.5,.75]:
 for kind,r,c in [('row',(value,value),(1,1)),('column',(1,1),(value,value))]:
  name=f'{kind}-stroke-{value}';reports[name]=collisions(g.assembly(r,c));print(name,len(reports[name]['unexpected']),flush=True)
for tr in [-2.8,-1.5,1.5,2.8]:
 name=f'drive-{tr}';reports[name]=collisions(g.assembly((1,1),(1,1),travel=tr));print(name,len(reports[name]['unexpected']),flush=True)
reports['one-follower-blocked']=collisions(g.assembly((1,1),(1,1),blocked=(0,)))
reports['one-output-stalled']=collisions(g.assembly((1,1),(1,1),travel=1.2,stalled=(0,)))
for tr in [-9.5,2.8]:
 reports[f'off-rack-end-{tr}']=collisions(g.assembly(travel=tr))
 reports[f'selected-rack-end-{tr}']=collisions(g.assembly((1,1),(1,1),travel=tr,phases=(tr/g.RP*180/math.pi,)*4))
# Full input tooth cycle: all gears, permanent rack, fixed supports. Output phases independently swept below.
base=g.assembly();gear_results=[]
for tr in np.linspace(0,math.pi*.3,25):
 a={k:v for k,v in base.items() if k in ['frame','keeper-upper-0','keeper-upper-1','keeper-lower-0','keeper-lower-1']}
 a['shared-rack']=g.move(g.PART['rack'],x=float(tr));a['hand-drive']=g.move(g.PART['drive'],x=-13.5,y=-3.6,rz=(-13.5-tr)/5.4*180/math.pi+5)
 for ix,iy in itertools.product(range(2),repeat=2):a[f'rotor-{iy*2+ix}']=g.move(g.PART['rotor'],ix*g.P,iy*g.P,rz=(ix*g.P-tr)/g.RP*180/math.pi+15)
 rr=collisions(a);gear_results.append({'rack_travel_mm':float(tr),**rr})
# Actual faceted cone only, 72 relative phases, offsets and tilt. Bisection finds first interference >1e-5mm³.
cm=g.mesh(g.cone(1.9,1.1,.8/math.tan(math.pi/6),41));cup=g.PART['output-screw']; cupm=g.mani(cup)
phase=[]
for eccentric,tilt in [(0,0),(.1,0),(.2,0),(.27,0),(0,2),(.27,3),(.27,6),(.4,3),(.7,6)]:
 for angle in range(0,360,5):
  m=g.move(cm,rz=angle)
  if tilt:m.apply_transform(tm.transformations.rotation_matrix(math.radians(tilt),[0,1,0],point=[0,0,41.6]))
  m.apply_translation([eccentric,0,0]);off=(g.mani(m)^cupm).volume();lo=-1.2;hi=1.0
  for _ in range(15):
   mid=(lo+hi)/2;vol=(g.mani(g.move(m,z=mid))^cupm).volume()
   if vol>1e-5:hi=mid
   else:lo=mid
  phase.append({'relative_angle_deg':angle,'radial_offset_mm':eccentric,'relative_tilt_deg':tilt,'first_contact_lift_mm':hi,'off_overlap_mm3':off})
with (P/'metadata/cone-phase-clearance.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=phase[0]);w.writeheader();w.writerows(phase)
# Negative control: forcing the gear into rack by0.4mm must be detected.
bad=base.copy();bad['rotor-0']=g.move(bad['rotor-0'],y=.4);control=collisions(bad)
report={'evidence':'finite nominal mesh intersection screens, not contact dynamics or physical fit','cad_source_sha256':hashlib.sha256((P/'cad/generate.py').read_bytes()).hexdigest(),'mesh_manifest_sha256':hashlib.sha256((P/'metadata/meshes.json').read_bytes()).hexdigest(),'threshold_mm3':.001,'expected_contact_rule':'matching male/female pair only, overlap < .02 mm3 due tessellation at nominal exact-surface contact','states':reports,'gear_cycle':gear_results,'cone_cases':len(phase),'cone_summary':[{ 'offset_mm':e,'tilt_deg':t,'min_contact_lift_mm':min(p['first_contact_lift_mm'] for p in phase if p['radial_offset_mm']==e and p['relative_tilt_deg']==t),'max_contact_lift_mm':max(p['first_contact_lift_mm'] for p in phase if p['radial_offset_mm']==e and p['relative_tilt_deg']==t),'max_off_overlap_mm3':max(p['off_overlap_mm3'] for p in phase if p['radial_offset_mm']==e and p['relative_tilt_deg']==t)} for e,t in [(0,0),(.1,0),(.2,0),(.27,0),(0,2),(.27,3),(.27,6),(.4,3),(.7,6)]],'negative_control_detected':bool(control['unexpected']),'negative_control':control,'rack_overtravel_at_4_5_mm':collisions(g.assembly(travel=4.5))}
(P/'metadata/geometry-review.json').write_text(json.dumps(report,indent=2)+'\n');print('COMPLETE',flush=True)
