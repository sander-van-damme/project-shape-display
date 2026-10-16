#!/usr/bin/env python3
"""Prescribed mixed-phase rigid 2x2 path, NOT self-alignment dynamics proof."""
from pathlib import Path
import importlib.util,itertools,json,hashlib
import numpy as np,trimesh as tm
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);o=g.old
for name in ['frame-left','frame-center','frame-right','row-selector','input-shaft','screw','pin','stop-spacer','reaction-jig']:
 o.MESHES[name]=tm.load(g.OUT/(name+'.stl'),force='mesh')
o.MESHES['rotor']=tm.load(g.OUT/'point48.stl',force='mesh')
envpath=H.parent/'mesh-contact-envelope.json';env=json.loads(envpath.read_text())['variants'][0]
assert env['name']=='point48'
assert env['source_sha256']==hashlib.sha256((g.OUT/'point48.stl').read_bytes()).hexdigest()
phases=np.array([30.,60.,120.,150.]);target=np.ones(4)*90
Dcurve=np.array(env['separation_envelope_mm']);axis=np.array(env['phase_deg'])
def required(phis):return max(float(np.interp(phi,axis,Dcurve)) for phi in phis)
# First move rows, then columns to an envelope-derived approach point.
# During phase change retain .03mm numerical safety above finite sampled envelope.
Dstart=max(3.36,required(phases)+.03);cstart=(5.76-Dstart)/2.4
poses=[('open',0.,0.,phases),('rows-half',.5,0.,phases),('rows-on',1.,0.,phases),('columns-approach',1.,cstart/2,phases)]
for t in np.linspace(0,1,13):
 ph=phases+(target-phases)*t
 D=max(3.36,required(ph)+.03)
 poses.append((f'prescribed-{t:.3f}',1.,(5.76-D)/2.4,ph))
poses.append(('full-closure',1.,1.,target))
counts=0;failures=[];records=[];cache={}
for label,r,c,ph in poses:
 pp=o.assembly((r,r),(c,c))
 # Shims must be removed while selectors move; reaction tool remains fixed.
 pp={n:m for n,m in pp.items() if 'shim' not in n}
 pp['reaction-jig']=o.shift(o.MESHES['reaction-jig'],[0,0,-2.2])
 for k,phi in enumerate(ph):
  i,j=divmod(k,2);x,y=[-2.54,2.54][j],[-2.54,2.54][i]
  pp[f'upper-{k}']=o.shift(o.rotate(o.rotate(o.MESHES['rotor'],[1,0,0],180),[0,0,1],phi),[x,y,27.56-2.4*c])
  pp[f'screw-{k}']=o.shift(o.rotate(o.MESHES['screw'],[0,0,1],phi),[x,y,22.64])
  pp[f'pin-{k}']=o.shift(o.MESHES['pin'],[x,y,38.21-3*(phi-90)/360])
 solids={n:o.solid(m) for n,m in pp.items()};local=0
 for (na,a),(nb,b) in itertools.combinations(pp.items(),2):
  if (a.bounds[1]<b.bounds[0]).any() or (b.bounds[1]<a.bounds[0]).any():continue
  counts+=1;local+=1
  # Exact vertex hashes allow reuse of truly identical pair configurations.
  key=tuple(hashlib.sha256(pp[n].vertices.tobytes()).hexdigest() for n in [na,nb])
  if key not in cache:cache[key]=abs((solids[na]^solids[nb]).volume())
  v=cache[key]
  if v>1e-5:failures.append(dict(pose=label,a=na,b=nb,intersection_mm3=v))
 records.append(dict(name=label,row_fraction=r,column_fraction=c,upper_phases_deg=ph.tolist(),fixed_input_phases_deg=[0]*4,pin_travel_from_90deg_reference_mm=(-3*(ph-90)/360).tolist(),required_sampled_root_separation_mm=required(ph),actual_root_separation_mm=8.16-2.4*(r+c),candidate_pair_checks=local))
report=dict(evidence='Finite prescribed kinematic path through actual printed-part source meshes; NOT automatic phase selection, force, friction or physical multi-pin proof.',poses=records,total_candidate_pair_checks=counts,unique_boolean_checks=len(cache),unexpected_intersections=failures,pass_nominal=not failures,source_envelope_sha256=hashlib.sha256(envpath.read_bytes()).hexdigest(),pin_height_change_start_to_end_mm=(-3*(target-phases)/360).tolist(),limitations=['Phases are externally prescribed independently, not solved by contact forces.','Small positive clearance above sampled contact envelope avoids claiming actual contact trajectories.','Only these 18 nominal poses; not all simultaneous initial phases, tolerances or continuous path.','One jammed pair can still block a shared selector.','Input DD backlash may permit small real input rotation despite reaction tool.'])
(H/'mixed-phase-path.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(poses=len(records),checks=counts,unique=len(cache),failures=failures),indent=2));assert not failures
