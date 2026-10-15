#!/usr/bin/env python3
"""Exact two-half mechanism. Python CadQuery + trimesh + manifold3d.
Run from repo root. Dimensions mm. E295 exact thread meshes are retained inputs.
"""
from pathlib import Path
import sys, json, math, hashlib
import numpy as np
import cadquery as cq
import trimesh as tm
import manifold3d as md
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=HERE/'parts'; OUT.mkdir(exist_ok=True)
P=5.08; S=2.40; G=3.36; H=2.40; RBASE=7.; CBASE=27.56
PARAMS=dict(pitch=P,stroke=S,tip_gap=G,tooth_height=H,tooth_width_deg=76,tooth_inner_radius=.6,tooth_outer_radius=1.8,tip_chamfer=.24,lower_base=RBASE,upper_base=CBASE,flange_thickness=.72,flange_diameter=4.3,comb_blade=.96,comb_gap=.96,axial_capture_play=.24,shaft_diameter=2.2,shaft_flats=1.6,socket_diameter=2.5,socket_flats=1.9,socket_depth=5.48)
def box(x,y,z,dx,dy,dz): return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cyl(r,h,z=0): return cq.Solid.makeCylinder(r,h,cq.Vector(0,0,z))
def cone(r1,r2,h,z=0): return cq.Solid.makeCone(r1,r2,h,cq.Vector(0,0,z))
def dd(d=2.2,af=1.6,h=5,z=0): return cyl(d/2,h,z).intersect(box(-d,-af/2,z,d*2,af,h))
def mesh(s):
 v,f=s.tessellate(.015,.08)
 return tm.Trimesh(np.array([a.toTuple() for a in v]),np.array(f),process=True)
def solid(m):
 a=md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
 assert a.status()==md.Error.NoError,a.status()
 return a
def fromsolid(s):
 m=s.to_mesh(); return tm.Trimesh(m.vert_properties[:,:3],m.tri_verts,process=True)
def merge(*mm):
 s=solid(mm[0])
 for m in mm[1:]: s=s+solid(m)
 return fromsolid(s)
def shift(m,xyz):
 n=m.copy();n.apply_translation(xyz);return n
def rotate(m,axis,deg):
 n=m.copy();n.apply_transform(tm.transformations.rotation_matrix(math.radians(deg),axis));return n
def sector_wire(width,z):
 aa=np.linspace(-width/2,width/2,24)*math.pi/180
 pts=[cq.Vector(1.8*math.cos(t),1.8*math.sin(t),z) for t in aa]
 pts += [cq.Vector(.6*math.cos(t),.6*math.sin(t),z) for t in aa[::-1]]
 return cq.Wire.makePolygon(pts+[pts[0]])
def rotor(relief=.15):
 b=cyl(2.15,.72).fuse(cyl(1.6,1.29,.71)).fuse(cone(1.6,1.8,.2,2)).fuse(cyl(1.8,4.01,2.19))
 # Angular tip setback is 10 degrees per flank over the last .24 mm.
 w0=sector_wire(76,6.2); w1=sector_wire(76,6.2+H-.24); w2=sector_wire(56,6.2+H)
 dog=cq.Solid.makeLoft([w0,w1,w2],True)
 b=b.fuse(dog).fuse(dog.rotate((0,0,0),(0,0,1),180))
 return b.cut(dd(2.2+2*relief,1.6+2*relief,5.49,-.01)).clean()
def selector(n=2,play=.24,radial=.15):
 # Two comb blades capture single .72-mm rotorbaseflange; crosslinks only outside rotating disks.
 cc=[-P/2,P/2] if n==2 else [0]
 xmin=min(cc)-2.3; xmax=max(cc)+2.3
 gap=.72+play
 zz=[-.96-play/2,.72+play/2]
 shapes=[]
 for k,z in enumerate(zz):
  b=box(xmin,-2.3,z,xmax-xmin,4.6,.96)
  d=(2.2 if k==0 else 3.2)+2*radial
  for x in cc:
   cut=cyl(d/2,1.1,z-.05).translate((x,0,0)).fuse(box(x-d/2,0,z-.05,d,3,1.1))
   b=b.cut(cut)
  shapes.append(b)
 lo=zz[0];hi=zz[1]+.96
 if n==2:
  for x,w in [(xmin-14,14),(xmax,14)]:
   shapes.append(box(x,-2.3,lo,w,3.3,hi-lo))
 else: shapes.append(box(xmax,-2.3,lo,6,3.3,hi-lo))
 b=shapes[0]
 for s in shapes[1:]: b=b.fuse(s)
 return b.clean()
def input_shaft():
 b=cyl(2.15,1.8).fuse(dd(h=8.93,z=1.79))
 # Socket below fixed thrust collar, removable hand key accesses it through base.
 return b.cut(dd(2.5,1.9,1.21,-.01)).clean()
def screw_base():
 # Tail on bed; 45deg cone is also lower axial thrust surface, no unsupported underside flange.
 return dd(h=7.09).fuse(cone(1.1,2.15,1.05,7.08)).fuse(cyl(2.15,1.2,8.13)).fuse(cyl(1.6,1.01,9.32)).clean()
def handkey():
 b=cyl(5,2).fuse(cone(3,1.1,1.9,2)).fuse(dd(h=7.1,z=3.89))
 return b.clean()
def couponshaft(): return cyl(4,1.2).fuse(dd(h=6,z=1.19)).clean()
def frame():
 # Three frame pieces, split THROUGH shaft axes X=+-2.54. Outer walls are print beds.
 b=box(-14,-13.5,0,1.2,27,52.4).fuse(box(12.8,-13.5,0,1.2,27,52.4))
 for y in [-13.5,12.3]: b=b.fuse(box(-P/2,y,0,P,1.2,52.4)).fuse(box(-14,y,22.5,28,1.2,7.5))
 collarblock=box(-7,-7,1.19,14,14,2.06)
 for x in [-P/2,P/2]:
  for y in [-P/2,P/2]: collarblock=collarblock.cut(cyl(2.3,2.2,1.15).translate((x,y,0)))
 b=b.fuse(collarblock)
 for z in [0,3.24,29.02,32.21,42.0,51.2]:
  thick=2.36 if z==3.24 else 1.2
  plate=box(-14,-12.3,z,28,24.6,thick)
  for x in [-P/2,P/2]:
   for y in [-P/2,P/2]:
    if z>=42: cut=box(x-2.3,y-2.3,z-.1,4.6,4.6,1.4)
    else:
     d={0:2.8,3.24:2.6,29.02:3.2,32.21:3.5}[z]
     cut=cyl(d/2,thick+.2,z-.1).translate((x,y,0))
    plate=plate.cut(cut)
  b=b.fuse(plate)
 # Row guide openings: full tab height2.88 + stroke2.4 + .24 allowance.
 for y in [-P/2,P/2]: b=b.cut(box(-14.1,y-2.5,5.8,28.2,3.7,5.52))
 # Column guide openings; same dimensions, axes turned 90 degrees.
 for x in [-P/2,P/2]: b=b.cut(box(x-2.5,-13.6,23.24,3.7,27.2,5.52))
 # Open windows avoid a bulky box, keep guide/screw support/upper pin rails.
 for z,h in [(12.,8.1),(33.5,2.8),(38.2,3.4),(43.6,7.2)]: b=b.cut(box(-14.1,-10.8,z,28.2,21.6,h))
 for y,z in [(9.8,15.0),(-13.5,38.8)]: b=b.fuse(box(-14,y,z,28,3.7,2.4))
 # Fixed radial guide decks keep both moving rotors aligned over full stroke.
 for z in [11.8,21.56]:
  g=box(-14,-12.3,z,28,24.6,1.2)
  for x in [-P/2,P/2]:
   for y in [-P/2,P/2]: g=g.cut(cyl(2.0,1.4,z-.1).translate((x,y,0)))
  b=b.fuse(g)
 return b.clean()
def stopblock():
 # External shim tongue supports a raised guide tab; 2.4 mm actual stroke stop.
 return box(-3,-1.7,0,6,3.4,2.4).fuse(box(-6,-2,0,3.01,4,2.4)).clean()
def orient_selector(m): return shift(rotate(m,[1,0,0],90),[0,0,2.3])
def orient_frame(m,side):
 n=rotate(m,[0,1,0],-90 if side=='left' else 90)
 n.apply_translation([0,0,-n.bounds[0,2]]); return n
SHAPES={};MESHES={}
def export_part(name,s,orientation=None):
 m=mesh(s) if not isinstance(s,tm.Trimesh) else s.copy()
 assert m.is_watertight,name
 if not isinstance(s,tm.Trimesh):
  SHAPES[name]=s; cq.exporters.export(s,str(OUT/(name+'.step')))
 MESHES[name]=m
 m.export(OUT/(name+'.stl'))
 p=orientation(m) if orientation else m.copy();p.apply_translation([0,0,-p.bounds[0,2]])
 p.export(OUT/(name+'-print.stl'))
 return p

def initial():
 export_part('rotor',rotor())
 export_part('row-selector',selector(),orient_selector)
 export_part('single-comb',selector(1),orient_selector)
 print('early rotor / selector available',flush=True)

def assembly(r=(0,0),c=(0,0),angles=(0,0,0,0),travels=(0,0,0,0)):
 """Named actual assembled STL meshes, selector fractions0..1 and angle degrees.
 Pin phase/travel initially neutral. Rotors upper canonical phase90deg.
 """
 parts={}
 for name in ['frame-left','frame-center','frame-right']: parts[name]=MESHES[name].copy()
 for i,y in enumerate([-P/2,P/2]): parts[f'row-{i}']=shift(MESHES['row-selector'],[0,y,RBASE+S*r[i]])
 for j,x in enumerate([-P/2,P/2]):
  m=rotate(MESHES['row-selector'],[1,0,0],180);m=rotate(m,[0,0,1],90)
  parts[f'column-{j}']=shift(m,[x,0,CBASE-S*c[j]])
 for i,y in enumerate([-P/2,P/2]):
  for j,x in enumerate([-P/2,P/2]):
   k=2*i+j;a=angles[k]
   parts[f'input-{k}']=shift(rotate(MESHES['input-shaft'],[0,0,1],a),[x,y,1.2])
   parts[f'lower-{k}']=shift(rotate(MESHES['rotor'],[0,0,1],a),[x,y,RBASE+S*r[i]])
   m=rotate(MESHES['rotor'],[1,0,0],180);m=rotate(m,[0,0,1],90+a)
   parts[f'upper-{k}']=shift(m,[x,y,CBASE-S*c[j]])
   # Upper bore must share screw-tail phase (90deg nominal).
   parts[f'screw-{k}']=shift(rotate(MESHES['screw'],[0,0,1],90+a),[x,y,22.64])
   parts[f'pin-{k}']=shift(MESHES['pin'],[x,y,38.21+travels[k]])
 # Shared external shims hold every raised selector at both ends.
 for i,y in enumerate([-P/2,P/2]):
  if abs(r[i]-1)<1e-9:
   parts[f'row-shim-{i}-left']=shift(MESHES['stop-spacer'],[-13,y-.65,5.8])
   parts[f'row-shim-{i}-right']=shift(rotate(MESHES['stop-spacer'],[0,0,1],180),[13,y-.65,5.8])
 for j,x in enumerate([-P/2,P/2]):
  if abs(c[j])<1e-9:
   parts[f'column-shim-{j}-front']=shift(rotate(MESHES['stop-spacer'],[0,0,1],90),[x-.65,-13,23.24])
   parts[f'column-shim-{j}-back']=shift(rotate(MESHES['stop-spacer'],[0,0,1],-90),[x-.65,13,23.24])
 return parts

def plate(name,items,dest):
 positioned=[];manifest=[];cursorx=5.;cursory=5.;rowheight=0.
 for label,m in items:
  mm=m.copy();sz=mm.extents
  if cursorx+sz[0]>145: cursorx=5;cursory+=rowheight+5;rowheight=0
  mm.apply_translation([cursorx-mm.bounds[0,0],cursory-mm.bounds[0,1],-mm.bounds[0,2]])
  positioned.append(mm);manifest.append(dict(name=label,bounds_mm=mm.bounds.tolist(),source=str(OUT.relative_to(ROOT)/(label.split('#')[0]+'-print.stl'))))
  cursorx+=sz[0]+4;rowheight=max(rowheight,sz[1])
 dest.mkdir(exist_ok=True,parents=True)
 tm.util.concatenate(positioned).export(dest/(name+'.stl'))
 (dest/'layout.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return positioned

def main():
 initial()
 if '--early' in sys.argv: return
 exports={}
 for label,clear,play in [('tight',.12,.18),('nominal',.15,.24),('loose',.20,.30)]:
  exports['rotor-'+label]=export_part('rotor-'+label,rotor(clear))
  exports['comb-'+label]=export_part('comb-'+label,selector(1,play,clear),orient_selector)
 exports['coupon-shaft']=export_part('coupon-shaft',couponshaft())
 fa=frame();left=fa.intersect(box(-20,-20,-1,20-P/2,40,60));right=fa.intersect(box(P/2,-20,-1,20,40,60));center=fa.intersect(box(-P/2,-20,-1,P,40,60))
 # Alignment pegs belong to outer shells, so center prints flat on split face.
 for y,z in [(11.65,16.2),(-11.65,40.0)]:
  left=left.fuse(cq.Solid.makeCylinder(.9,1.8,cq.Vector(-P/2,y,z),cq.Vector(1,0,0)))
  right=right.fuse(cq.Solid.makeCylinder(.9,1.8,cq.Vector(P/2,y,z),cq.Vector(-1,0,0)))
  center=center.cut(cq.Solid.makeCylinder(1.05,2.0,cq.Vector(-P/2-.01,y,z),cq.Vector(1,0,0)))
  center=center.cut(cq.Solid.makeCylinder(1.05,2.0,cq.Vector(P/2+.01,y,z),cq.Vector(-1,0,0)))
 for label,s in [('frame-left',left),('frame-center',center),('frame-right',right)]: exports[label]=export_part(label,s,lambda m,l=label:orient_frame(m,'left' if l.endswith('left') else 'right'))
 exports['input-shaft']=export_part('input-shaft',input_shaft())
 exports['hand-key']=export_part('hand-key',handkey())
 exports['stop-spacer']=export_part('stop-spacer',stopblock())
 thread=tm.load(HERE/'e295-thread.stl',force='mesh');pin=tm.load(HERE/'e295-pin.stl',force='mesh')
 sb=mesh(screw_base());screw=merge(sb,shift(thread,[0,0,10.32]))
 exports['screw']=export_part('screw',screw)
 # Closed top on bed; thread prints last, no internal support.
 exports['pin']=export_part('pin',pin,lambda m:rotate(m,[1,0,0],180))
 exports['row-selector']=tm.load(OUT/'row-selector-print.stl',force='mesh');exports['rotor']=tm.load(OUT/'rotor-print.stl',force='mesh')
 a=[]
 for label in ['tight','nominal','nominal','loose']:
  for q in range(2):a.append(('rotor-'+label, exports['rotor-'+label]))
  a.append(('comb-'+label,exports['comb-'+label]));a.append(('coupon-shaft',exports['coupon-shaft']));a.append(('coupon-shaft',exports['coupon-shaft']))
 plate('clutch-fit',a,ROOT/'owner-print-tests/2026-10-16-two-half-clutch-fit')
 b=[]
 for label,n in [('frame-left',1),('frame-right',1),('frame-center',1),('row-selector',4),('rotor',8),('input-shaft',4),('screw',4),('pin',4),('hand-key',1),('stop-spacer',8)]:
  b += [(label,exports[label]) for _ in range(n)]
 plate('clutch-matrix',b,ROOT/'owner-print-tests/2026-10-16-two-half-clutch-matrix')
 assembled=assembly()
 tm.util.concatenate(list(assembled.values())).export(HERE/'assembly-off.stl')
 tm.util.concatenate(list(assembly((1,0),(1,0)).values())).export(HERE/'assembly-r0-c0.stl')
 (HERE/'parameters.json').write_text(json.dumps(PARAMS,indent=2)+'\n')
 records={k:dict(extents_mm=v.extents.tolist(),volume_mm3=float(v.volume),watertight=bool(v.is_watertight),sha256=hashlib.sha256((OUT/(k+'.stl')).read_bytes()).hexdigest()) for k,v in MESHES.items()}
 (HERE/'mesh-validation.json').write_text(json.dumps(records,indent=2)+'\n')
 print('ALL EXPORTED',flush=True)
if __name__=='__main__': main()
