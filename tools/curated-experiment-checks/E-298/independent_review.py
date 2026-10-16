#!/usr/bin/env python3
"""Independent reviewer: immutable source copies and new input reaction jig."""
from pathlib import Path
import importlib.util, hashlib, itertools, json, math
import trimesh as tm
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=HERE.parent/'E-297'
spec=importlib.util.spec_from_file_location('old_cad',OLD/'cad/generate.py')
o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
parts=HERE/'cad/parts'
checks={}
for name in ['frame-left','frame-center','frame-right','row-selector','single-comb','input-shaft','screw','pin','hand-key','stop-spacer','coupon-shaft']:
 for suffix in ['.stl','-print.stl','.step']:
  a=OLD/'cad/parts'/(name+suffix);b=parts/(name+suffix)
  if a.exists():checks[name+suffix]=a.read_bytes()==b.read_bytes()
 o.MESHES[name]=tm.load(parts/(name+'.stl'),force='mesh')
o.MESHES['rotor']=tm.load(parts/'point48.stl',force='mesh')
jig=o.shift(tm.load(parts/'reaction-jig.stl',force='mesh'),[0,0,-2.2])
j=o.solid(jig);collisions=[];n=0
for state in itertools.product([0,1],repeat=4):
 for name,m in o.assembly(state[:2],state[2:]).items():
  if any(jig.bounds[1,k]<=m.bounds[0,k] or m.bounds[1,k]<=jig.bounds[0,k] for k in range(3)):continue
  v=(j^o.solid(m)).volume();n+=1
  if v>1e-6:collisions.append({'state':state,'part':name,'volume_mm3':v})
half_lash=math.degrees(math.asin(.95/1.1)-math.asin(.8/1.1))
report={'nominal_concentric_DD_half_lash_deg':half_lash,'nominal_concentric_DD_reversal_lash_deg':2*half_lash,'jig_to_lower_rotor_two_DD_total_reversal_lash_deg':4*half_lash,'source_copies_identical':checks,'all_source_copies_identical':all(checks.values()),'reaction_jig_states':16,'reaction_jig_boolean_pairs':n,'reaction_jig_collisions':collisions,'jig_sha256':hashlib.sha256((parts/'reaction-jig.stl').read_bytes()).hexdigest(),'scope':'Finite nominal assembly checks. Jig reacts existing inputs after nominal DD backlash during axial indexing; removable before transmission test. No tolerance, friction, physical strength or self-alignment proof.'}
(HERE/'independent-review.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['all_source_copies_identical'] and not collisions,report
print(json.dumps(report,indent=2))
