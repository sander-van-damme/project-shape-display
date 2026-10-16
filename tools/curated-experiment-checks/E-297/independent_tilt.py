#!/usr/bin/env python3
"""Independent allowable rotor-tilt search on exported E-297 meshes.
Run with numpy, trimesh and manifold3d; all files resolve relative to this script.
"""
from pathlib import Path
import sys,itertools,json,math,numpy as np
import trimesh as tm,manifold3d as md
ROOT=Path(__file__).resolve().parent
p=ROOT/'cad'/'parts'
def load(n):
 m=tm.load(p/(n+'.stl'));return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
rot=load('rotor');comb=load('row-selector').translate((2.54,0,9.4));shaft=load('input-shaft').translate((0,0,1.2))
frame=(load('frame-left')+load('frame-center')+load('frame-right')).translate((2.54,2.54,0))
guide=frame^md.Manifold.cube((5.08,5.08,1.22)).translate((-2.54,-2.54,11.79))
feasible=[];ng=0;tested=0
source_hashes={}
import hashlib
for n in ('rotor','row-selector','input-shaft','frame-left','frame-center','frame-right'):
 source_hashes[n]=hashlib.sha256((p/(n+'.stl')).read_bytes()).hexdigest()
shiftxy=[(dx,dy) for dx in (-.2,-.1,0,.1,.2) for dy in (-.2,-.1,0,.1,.2) if dx*dx+dy*dy<=.040001]
if '--replay' in sys.argv:
 previous=json.loads((ROOT/'independent-tilt.json').read_text())
 cases=previous['worst']+[item[key] for item in previous['by_state'] for key in ('worst','shaft_clear_worst') if item[key] is not None]
 cases=list({json.dumps(item,sort_keys=True):item for item in cases}.values())
 checks=[]
 for q in cases:
  state=q['selector_fraction'];base=7+2.4*state;pivotlocal=13-base
  r=rot.translate((0,0,-pivotlocal)).rotate((0,0,-q['phi'])).rotate((0,q['theta'],0)).rotate((0,0,q['phi'])).translate((q['dx'],q['dy'],13+q['dz']))
  vg=(r^guide).volume()
  vc=(r^comb.translate((0,q['combshift'],base-9.4))).volume()
  vs=(r^shaft).volume()
  checks.append(dict(pose=q,actual_guide_intersection_mm3=vg,actual_comb_intersection_mm3=vc,vertical_shaft_intersection_mm3=vs))
  assert vg<1e-5 and vc<1e-5,(q,vg,vc)
 previous['dense_search_source_mesh_sha256']=previous.pop('source_mesh_sha256',previous.get('dense_search_source_mesh_sha256',{}))
 previous['final_geometry_replay']=dict(source_mesh_sha256=source_hashes,cases=checks,
  conclusion='All recorded limiting poses remain admissible to the final guide and selector meshes. Only external grips and remote frame spines changed after the dense search; the constrained guide/capture regions are unchanged. This local replay is not a new exhaustive dense search.',
  physical_limitation='The OFF-state guide/comb-only superset includes flange envelopes beyond the cell midplane. Those recorded poses intersect the nominal vertical shaft. Combined input-shaft tilt, printing errors, friction and compliance remain physically unqualified; do not claim global neighbor isolation from this finite sampling.')
 (ROOT/'independent-tilt.json').write_text(json.dumps(previous,indent=2)+'\n')
 print(json.dumps(dict(final_replay_cases=len(checks),all_actual_guides_and_combs_clear=True),indent=2))
 raise SystemExit(0)
for state in (0,.5,1):
 base=7+2.4*state;pivotlocal=13-base
 thiscomb=comb.translate((0,0,base-9.4))
 for theta,phi in itertools.product(list(np.arange(0,4.01,.5))+list(range(5,21)),range(0,360,45)):
  rr=rot.translate((0,0,-pivotlocal)).rotate((0,0,-phi)).rotate((0,theta,0)).rotate((0,0,phi))
  t=math.radians(theta);f=math.radians(phi);axis=np.array([math.sin(t)*math.cos(f),math.sin(t)*math.sin(f),math.cos(t)])
  for (dx,dy),dz in itertools.product(shiftxy,(-.12,-.06,0,.06,.12)):
   tested+=1;r=rr.translate((dx,dy,13+dz))
   if (r^guide).volume()>1e-5:continue
   ng+=1
   shifts=[cs for cs in (-.2,0,.2) if (r^thiscomb.translate((0,cs,0))).volume()<1e-5]
   if not shifts:continue
   # A circular outer envelope conservatively includes every rotary phase.
   origin=np.array((dx,dy,13+dz))-pivotlocal*axis
   reaches=[]
   for z,rad in ((0,2.15),(.72,2.15),(.72,1.6),(2,1.6),(2.2,1.8),(8.6,1.8)):
    center=origin+z*axis
    reaches.extend((abs(center[j])+rad*math.sqrt(1-axis[j]**2)) for j in (0,1))
   shaftvolume=(r^shaft).volume()
   for cs in shifts:
    feasible.append(dict(selector_fraction=state,theta=float(theta),phi=phi,dx=dx,dy=dy,dz=dz,combshift=cs,round_reach=max(reaches),shaft_overlap_mm3=shaftvolume))
  if phi==315 and theta%5==0:print('state',state,'angle',theta,'tested',tested,'feasible',len(feasible),flush=True)
feasible.sort(key=lambda q:q['round_reach'],reverse=True)
result=dict(source_mesh_sha256=source_hashes,tested=tested,guide_clear=ng,feasible_count=len(feasible),maximum_tilt_deg=max(q['theta'] for q in feasible),worst=feasible[:20],shaft_clear_worst=next((q for q in feasible if q['shaft_overlap_mm3']<1e-5),None),by_state=[dict(selector_fraction=state,worst=next(q for q in feasible if q['selector_fraction']==state),shaft_clear_worst=next((q for q in feasible if q['selector_fraction']==state and q['shaft_overlap_mm3']<1e-5),None)) for state in (0,.5,1)],scope='Finite sampled geometry; full 3.6 mm circular tooth/body envelope includes every rotation phase. Actual frame guide and two-cell selector, including +/-0.2 mm transverse selector offset. Shaft is deliberately omitted from acceptance for a conservative superset; overlap with the nominal vertical shaft is separately recorded. Mirroring/quarter-turn maps to upper rotors. No print errors, friction, compliance or continuous-pose proof.')
(ROOT/'independent-tilt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(tested=tested,feasible=len(feasible),worst=result['worst'][0],by_state=result['by_state']),indent=2))
