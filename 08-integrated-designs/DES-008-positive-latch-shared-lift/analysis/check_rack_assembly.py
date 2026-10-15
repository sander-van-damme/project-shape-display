#!/usr/bin/env python3
"""Independent nominal assembly path for the comb/seat/clamp subassembly.
No allowance for actual print size, hand access, fastener threading or elasticity.
Reuses hash-qualified component exports from E-prototype-check.py.
"""
import argparse,hashlib,itertools,json
from pathlib import Path
import numpy as np
import trimesh
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--prototype',type=Path);ap.add_argument('--meshes',type=Path,default=Path('work/des008-handoff-review/components'));ap.add_argument('--nominal-results',type=Path,default=Path('work/des008-handoff-review/poses.json'));ap.add_argument('--output',type=Path,default=Path('work/des008-handoff-review/assembly.json'));a=ap.parse_args()
scad=a.source or (a.prototype/'rack_handoff.scad' if a.prototype else Path(__file__).resolve().parents[1]/'cad'/'rack_handoff.scad')
sha=hashlib.sha256(scad.read_bytes()).hexdigest()
nominal=json.loads(a.nominal_results.read_text());assert nominal['source_sha256']==sha
m={p.stem:trimesh.load_mesh(p) for p in a.meshes.glob('*.stl')};counts={};hits=[]
def check(stage,step,moving,offset,fixed):
 counts[stage]=counts.get(stage,0)+1
 for x,y in itertools.product(moving,fixed):
  xm=m[x].copy();xm.apply_translation(offset);ym=m[y]
  if np.any(np.minimum(xm.bounds[1],ym.bounds[1])-np.maximum(xm.bounds[0],ym.bounds[0])<=1e-5):continue
  v=float(abs(trimesh.boolean.intersection([xm,ym],engine='manifold').volume))
  if not np.isfinite(v):raise RuntimeError('Non-finite Boolean volume')
  if v>1e-4:hits.append({'stage':stage,'step':step,'moving':x,'fixed':y,'offset':list(offset),'volume_mm3':v})
for row in (0,1):
 for k,z in enumerate(np.linspace(30,0,121)):
  check('clamp_over_comb_'+str(row),k,[f'root_clamp-{row}'],(0,0,z),[f'ground_comb-{row}'])
installed=['ground_seat-0']
for row in (1,0):
 unit=[f'ground_comb-{row}',f'root_clamp-{row}',f'bolt-{4+2*row}',f'bolt-{5+2*row}']
 for k,z in enumerate(np.linspace(-10.4,.2,107)):
  check('comb_raise_'+str(row),k,unit,(0,-2.15,z),installed)
 for k,y in enumerate(np.linspace(-2.15,0,44)):
  check('comb_shift_'+str(row),k,unit,(0,y,.2),installed)
 for k,z in enumerate(np.linspace(.2,0,5)):
  check('comb_seat_'+str(row),k,unit,(0,0,z),installed)
 installed.extend(unit)
for k,z in enumerate(np.linspace(8,0,81)):
 check('bundle_into_lower_guide',k,installed,(0,0,z),['lower_guide-0'])
# Keeper installation: pin already unloaded; leaf initially held at matching
# release position. This checks keeper against stationary frame, not the
# force/deformation path needed to pull the leaf by hand.
keeper=m['ground_keeper-0']
frame=['ground_seat-0','upper_guide-0']
for k,y in enumerate(np.linspace(1.05,0,22)):
 check('keeper_slide_above_wall',k,['ground_keeper-0'],(0,y,1.4),frame)
for k,z in enumerate(np.linspace(1.4,0,29)):
 check('keeper_drop_into_anchor',k,['ground_keeper-0'],(0,0,z),frame)
result={'source_sha256':sha,'states_by_stage':counts,'total_states':sum(counts.values()),'collisions':hits,'limits':'Nominal rigid sample paths only. Keeper leaf manipulation, hand/tool access, actual fits, screw threading and clamping preload require physical verification. Witness comb installed first; preinsert root bolts; root nuts installed after lower-guide seating.'}
if hashlib.sha256(scad.read_bytes()).hexdigest()!=sha:raise RuntimeError('CAD changed during verification')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(hits))
