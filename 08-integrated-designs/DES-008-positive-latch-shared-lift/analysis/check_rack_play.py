#!/usr/bin/env python3
"""Independent finite guide-play screen; nominal printed dimensions only.

Uses independently exported parts from E-prototype-check.py. Tests extreme
admitted pin centerlines between the bottom and top pin guides, and independent
carriage translations. Does not infer print tolerance, elastic deformation,
force-dependent key pitch, or closed-loop control from these rigid poses.
"""
from pathlib import Path
import argparse,itertools,json,hashlib,re
import numpy as np
import trimesh

ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--prototype',type=Path);ap.add_argument('--meshes',type=Path,default=Path('work/des008-handoff-review/components'));ap.add_argument('--nominal-results',type=Path,default=Path('work/des008-handoff-review/poses.json'));ap.add_argument('--output',type=Path,default=Path('work/des008-handoff-review/guide-play.json'));a=ap.parse_args()
scad=a.source or (a.prototype/'rack_handoff.scad' if a.prototype else Path(__file__).resolve().parents[1]/'cad'/'rack_handoff.scad')
src=scad.read_bytes();sha=hashlib.sha256(src).hexdigest()
nominal=json.loads(a.nominal_results.read_text())
assert nominal['source_sha256']==sha,'Mesh provenance does not match current source'
mesh={p.stem:trimesh.load_mesh(p) for p in a.meshes.glob('*.stl')}
# Geometry values are deliberately independently stated and verified against
# the component bounds below. No CAD-author tolerance helper is imported.
z_low=-14.;z_high=62.;pivot=(z_low+z_high)/2
assert abs(mesh['bottom_guide-0'].bounds[0,2]-z_low)<1e-5
assert abs(mesh['upper_guide-0'].bounds[1,2]-z_high)<1e-5
pin_x=.20;pin_y=.10;head_x=.20;head_y=.20
release=float(re.search(r'^release=([.0-9]+);',src.decode(),re.M).group(1))
# Every pin is checked against its own/preceding selector and the continuous
# carrier floor/lid. The witness row must clear those same moving objects.
hits=[];cases=0
for pin_index in range(8):
 pin=mesh[f'pin-{pin_index}'].copy()
 heights=json.loads(re.search(r'^'+('active_h' if pin_index<4 else 'witness_h')+r'=(\[[^;]+\]);',src.decode(),re.M).group(1))
 pin.apply_translation((0,0,-heights[pin_index%4]))
 center_x=(pin_index%4)*6.35;center_y=(pin_index//4)*6.35
 for xl,xh,yl,yh in itertools.product((-pin_x,pin_x),(-pin_x,pin_x),(-pin_y,pin_y),(-pin_y,pin_y)):
  sx=(xh-xl)/(z_high-z_low);sy=(yh-yl)/(z_high-z_low)
  direction=np.asarray([sx,sy,1.]);direction/=np.linalg.norm(direction)
  rot=trimesh.geometry.align_vectors([0,0,1],direction)
  ref=np.asarray([center_x,center_y,pivot]);rot[:3,3]=ref-rot[:3,:3]@ref+np.asarray([(xl+xh)/2,(yl+yh)/2,0])
  for hx,hy in itertools.product((-head_x,head_x),(-head_y,head_y)):
   for state,pinz,keyz,on in [('park',0,0,False),('capture',0,0,True),('unselected_up',0,5.6,False),('unselected_down',10,-5.55,False)]:
    pm=pin.copy();pm.apply_translation((0,0,pinz));pm.apply_transform(rot)
    case={'pin':pin_index,'guide_endpoints_mm':[xl,xh,yl,yh],'head_offset_mm':[hx,hy],'state':state}
    parts=[(f'drive_key-{k}',(hx,hy-(release if on else 0),keyz)) for k in (pin_index%4-1,pin_index%4) if k>=0]
    parts += [(n,(hx,hy,keyz)) for n in ('carriage_base-0','carriage_lid-0')]
    for name,shift in parts:
     km=mesh[name].copy();km.apply_translation(shift)
     d=np.minimum(pm.bounds[1],km.bounds[1])-np.maximum(pm.bounds[0],km.bounds[0])
     if np.any(d<=1e-6):volume=0.
     else:volume=float(abs(trimesh.boolean.intersection([pm,km],engine='manifold').volume))
     if not np.isfinite(volume):raise RuntimeError('Non-finite Boolean volume')
     if volume>1e-4:hits.append(dict(case,part=name,volume_mm3=volume))
    cases+=1
result={'source_sha256':sha,'cases':cases,'tested_pins':list(range(8)),'moving_parts':'Own and preceding drive keys, carrier base and lid', 'guide_span_mm':[z_low,z_high], 'guide_translations_mm':{'pin_x':pin_x,'pin_y':pin_y,'head_x':head_x,'head_y':head_y}, 'collisions':hits,'limits':'Rigid parts at nominal dimensions. No twist about pin axis, carriage angular play, key pitch, extrusion variation, friction or elasticity. Capture tested clear of load flanks; moving selected-pin force contact is in separate pose audit. Guide centerline extremes approximate finite rigid rotation and are conservative enough only for first-order clearance screening.'}
if hashlib.sha256(scad.read_bytes()).hexdigest()!=sha:raise RuntimeError('CAD changed during verification')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(hits))
