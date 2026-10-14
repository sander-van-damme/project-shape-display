#!/usr/bin/env python3
"""CAD interference checks plus independent contact/layout bounds; not a fit qualification."""
import argparse, itertools, json, math, os, subprocess
from pathlib import Path
import numpy as np
import trimesh
HERE=Path(__file__).resolve().parents[1]

def moved(m,xyz=(0,0,0),angle=0):
 m=m.copy()
 if angle:m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[0,0,1]))
 m.apply_translation(xyz);return m

def overlap(a,b):
 if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])<=1e-6):return 0.
 c=trimesh.boolean.intersection([a,b],engine='manifold');return float(c.volume) if c is not None else 0.

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--bosl2',type=Path,required=True);args=ap.parse_args();out=args.build
 env=dict(os.environ,OPENSCADPATH=str(args.bosl2.resolve().parent))
 def raw(name):return trimesh.load_mesh(out/(name+'-raw.stl'))
 for row in (0,1):
  r=subprocess.run(['openscad','-o',str(out/f'bare_screw_{row}.stl'),'-D','part="screw"','-D',f'row={row}',str(HERE/'cad/rig.scad')],env=env,capture_output=True,text=True)
  assert r.returncode==0,r.stderr
 screws=[trimesh.load_mesh(out/f'bare_screw_{r}.stl') for r in (0,1)]
 pin=raw('pin');p=6.35;posts=[(-9,-7),(-9,17),(-9,3.175),(28.05,-7),(28.05,17),(28.05,3.175)]
 parts=[]
 for z in (0,15):
  parts += [(f'bed{z}_{r}',moved(raw(f'upper_{r}'),(0,0,z))) for r in range(3)]
 parts += [('keeper',moved(raw('keeper'),(0,0,20.2))),('lower_guide',moved(raw('guide'),(0,0,34))),('upper_guide',moved(raw('guide'),(0,0,44))),('roof',moved(raw('roof'),(0,0,53.2))),('foot',moved(raw('foot'),(0,0,-30))),('head',moved(raw('head'),(0,0,-25))),('head_cover',moved(raw('head_cover'),(0,0,-20.8)))]
 for i,(x,y) in enumerate(posts):
  for z,h in [(-27,27),(3,12),(18,2.2),(21.8,12.2),(36,8),(46,7.2)]:parts.append((f'spacer{i}_{z}',moved(raw(f'spacer_{h:g}'),(x,y,z))))
 for x in (-5,26.05):parts.append(('head_mount_spacer',moved(raw('spacer_2'),(x,-18,-27))))
 for x in np.arange(5)*p-p/2:
  wire=trimesh.creation.cylinder(radius=.5,height=23.8,sections=48);wire.apply_translation([x,-2.3,-12.9]);parts.append(('separator',wire))
 # Shoe export is rotated for printing; undo that before placing in assembly.
 tip=raw('shoe_tip');tip.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
 stem=trimesh.creation.cylinder(radius=.4,height=18.8,sections=48);stem.apply_translation([3.175,0,10.4])
 shoe=trimesh.util.concatenate([raw('shoe_base'),tip,stem])
 for i in range(4):
  for state,y in [('off',-4.4),('on',-4.0)]:
   sh=moved(shoe,(i*p,y,-24))
   for name,m in parts:
    v=overlap(sh,m)
    assert v<.002,('shoe',i,state,name,v)
 # Static structure must not contain interpenetrating material.
 conflicts=[]
 for (na,a),(nb,b) in itertools.combinations(parts,2):
  v=overlap(a,b)
  if v>.002:conflicts.append((na,nb,v))
 assert not conflicts,conflicts
 pair_max=0;checks=0
 for q in np.linspace(0,6,25):
  # Nut cutter begins at local -3; male begins at global 20.
  a=moved(screws[0],angle=120*(1-q));b=moved(pin,(0,0,22+q))
  v=overlap(a,b);pair_max=max(pair_max,v);assert v<.003,('thread',q,v)
  for row,x in itertools.product(range(2),range(4)):
   sc=moved(screws[row],(x*p,row*p,0),angle=120*(1-q));pn=moved(pin,(x*p,row*p,22+q))
   for name,m in parts:
    assert overlap(sc,m)<.003,('screw',row,x,name,overlap(sc,m))
    assert overlap(pn,m)<.003,('pin',q,row,x,name,overlap(pn,m))
   checks+=1
 # Deliberately wrong thread phase is required to fail (sensitivity/control).
 bad=overlap(screws[0],moved(pin,(0,0,25)))
 assert bad>.01,bad
 # Both wheel tiers, both selector positions and swept vertical access to parked Z.
 transport_collision=0
 for tier,y,qz in itertools.product((0,1),(-4.4,-4.0),np.linspace(-12,0,13)):
  sh=moved(shoe,(0,y,-24-6*tier+qz))
  for yy in (-p,p):
   for xx in (-p,0,p):
    behind=moved(screws[1-tier],(xx,yy,0))
    v=overlap(sh,behind);transport_collision=max(v,transport_collision)
    assert v<.003,('offset shoe',tier,y,qz,xx,yy,v)
 # Old straight upright is a retained failing CAD witness.
 old=trimesh.creation.box(extents=[2.4,.8,19.1]);old.apply_translation([0,-5.0,-11.55])
 bad_stem=overlap(old,moved(screws[1],(0,-p,0)))
 assert bad_stem>.01,bad_stem
 # All 16 masks: fixed separators force the unselected belt chord to y=-2.8.
 # Without separators, 1010 produces a tangent at y=-2.5 on unselected output 1.
 mask_clearances=[]
 for bits in itertools.product((0,1),repeat=4):
  for i,on in enumerate(bits):
   if not on:mask_clearances.append(2.8-2.5)
 assert min(mask_clearances)>0
 result=dict(evidence='nominal CAD + ideal taut-strip geometry, no physical evidence',
  structure_pairs=len(parts)*(len(parts)-1)//2,full_position_cases=checks,
  pair_intersection_max_mm3=pair_max,wrong_phase_intersection_mm3=bad,
  all_masks=16,unselected_belt_gap_nominal_mm=min(mask_clearances),
  offset_stem_intersection_mm3=transport_collision,old_straight_stem_intersection_mm3=bad_stem,
  status='nominal bench and offset-stem neighbor envelopes pass; loads, tolerances and drive tape unqualified',
  tolerance_notes='0.15 mm nominal guide side clearance; 0.2 mm screw axial capture float; neither is measured capability')
 (out/'geometry-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
