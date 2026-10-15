#!/usr/bin/env python3
"""Bounded admitted-yaw search of the longer-guide/shorter-toe variant.

Not a proof of all6DOF tolerance safety. Candidate translations are vertices of
the exact planar half-plane constraints of T-foot, mouth and rectangular key.
Every claimed counterexample is then tested against actual3D source meshes.
"""
import argparse,hashlib,json,math,subprocess,warnings
from pathlib import Path
import numpy as np,trimesh

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('work/des008-resident-escape'));args=parser.parse_args()
SRC=ROOT.parent/'cad/resident_cell_guide_escape.scad'
sha=hashlib.sha256(SRC.read_bytes()).hexdigest()
assert sha=='24eb609bdb034dccbd72d93b6ee8af8cca14b333965516dce820bfd237af07e9'
OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)

def mesh(part):
    out=OUT/(part+'.stl')
    subprocess.run(['openscad','-o',str(out),'-D',f'part="{part}"',str(SRC)],capture_output=True,check=True)
    return trimesh.load(out,force='mesh')
base={name:mesh(name) for name in ['dog','channel','dog_guide','pin']}
def volume(a,b):
    if np.any(a.bounds[1]<b.bounds[0]) or np.any(b.bounds[1]<a.bounds[0]):return 0
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        x=trimesh.boolean.intersection([a,b],engine='manifold')
        return 0 if x.is_empty else float(abs(x.volume))

def feasible_polygon(theta,cy):
    c=math.cos(theta);s=math.sin(theta);t=math.tan(theta);ineq=[]
    def le(a,v):ineq.append((np.array(a),v))
    for x in [2.75,3.25]:
      for y in [-.75,.75]:
        xr=3+(x-3)*c-y*s;yr=(x-3)*s+y*c
        le([1,0],3.5-xr);le([-1,0],xr-2.5)
        le([0,1],.85-yr);le([0,-1],yr+.85)
    for x in [2.2,2.5]:
        z=t*(x-3)
        le([-t,1],.5-.4/c-z);le([t,-1],.5-.4/c+z)
    for y in [-1.65,-.65]:
        z=3-1.175/c-t*(y-cy)
        le([1,t],2.05-.175/c-z);le([-1,-t],z-1.6-.175/c)
    points=[np.array(x,dtype=float) for x in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    for normal,limit in ineq:
        old=points;points=[]
        if not old:break
        for p,q in zip(old,old[1:]+old[:1]):
            vp=normal@p-limit;vq=normal@q-limit
            if vp<=1e-12:points.append(p)
            if (vp<0)!=(vq<0):points.append(p+(q-p)*vp/(vp-vq))
    return points

def pose(bit,a,deg,xy):
    cy=-3.05-1.6*(1-bit)+a
    m=base['dog'].copy();m.apply_translation([0,cy+2.2,0])
    t=math.radians(deg);R=np.array([[math.cos(t),-math.sin(t),0],[math.sin(t),math.cos(t),0],[0,0,1]])
    o=np.array([3,cy,-30.4]);m.vertices=(m.vertices-o)@R.T+o+[xy[0],xy[1],0]
    return m

valid={};checks=0;own_collisions=[]
for a in [0,.85]:
 for bit in [0,1]:
    cy=-3.05-1.6*(1-bit)+a
    ch=base['channel'].copy();ch.apply_translation([0,cy+2.2,0])
    points=[]
    for deg in np.linspace(-7,7,141):
      polygon=feasible_polygon(math.radians(deg),cy)
      candidates=polygon+[sum(polygon)/len(polygon)] if polygon else []
      for xy in candidates:
        m=pose(bit,a,float(deg),xy);checks+=1
        if volume(m,ch)>1e-6 or volume(m,base['dog_guide'])>1e-6:continue
        v=volume(m,base['pin'])
        if v>1e-6:
            own_collisions.append(dict(A=a,bit=bit,degrees=float(deg),translation=xy.tolist(),volume=v))
            continue
        # Vertices lying in the key's0.35mm strip before transformation.
        # All-part Y extrema are also useful conservative shortlist bounds.
        points.append((m,dict(A=a,bit=bit,degrees=float(deg),translation=xy.tolist()),float(m.bounds[0,1]),float(m.bounds[1,1])))
    valid[(a,bit)]=points

neighbor_collisions=[]
for a in [0,.85]:
    first=sorted(valid[(a,1)],key=lambda x:-x[3])[:30]
    second=sorted(valid[(a,0)],key=lambda x:x[2])[:30]
    for left in first:
      for right in second:
        m=right[0].copy();m.apply_translation([0,6.35,0]);v=volume(left[0],m)
        if v>1e-6:
            neighbor_collisions.append(dict(first=left[1],next=right[1],next_offset_Y=6.35,volume=v))
            left[0].export(OUT/'neighbor-first.stl');m.export(OUT/'neighbor-next.stl')
            break
      if neighbor_collisions:break
    if neighbor_collisions:break

result=dict(source_sha256=sha,candidate_count=checks,valid_counts={str(k):len(v) for k,v in valid.items()},
            own_collision_count=len(own_collisions),own_examples=own_collisions[:8],
            neighbor_examples=neighbor_collisions,
            scope='Bounded planar yaw search, not all3D or manufacturing tolerance proof')
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
