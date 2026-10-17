#!/usr/bin/env python3
"""E-299 two-cell supported selector. Millimetres; exact E295 thread retained."""
from pathlib import Path
import importlib.util,json,math,hashlib
import numpy as np
import trimesh as tm
import cadquery as cq
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; OUT=HERE/'parts'; OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('old',ROOT/'tools/curated-experiment-checks/E-297/cad/generate.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
box,cyl,cone,dd,mesh,merge,shift,rotate=old.box,old.cyl,old.cone,old.dd,old.mesh,old.merge,old.shift,old.rotate
P=5.08; S=3.; R=8.; C=29.36; BLADE=1.6; LO=-1.72; HI=2.44
PARAMS=dict(pitch=P,stroke=S,lower_base_off=R,upper_base_off=C,rotor_root=6.2,tooth_height=2.4,tip_chamfer=.24,tooth_width=76,fully_on_root_gap=2.96,fully_on_total_overlap=1.84,fully_on_straight_overlap=1.36,tip_to_floor=.56,single_selected_tip_clearance=1.16,selector_blade=BLADE,selector_capture_play=.24,neck_height=2.6,rotor_diameter=3.6,guide_diameter=4.,input_socket_depth=3.2,thread_source='E-297/cad/e295-thread.stl (E295 exact mesh)',pin_source='E-297/cad/e295-pin.stl')
SHAPES={}; MESHES={}; PRINT={}
def export(name,s,orient=None):
 m=mesh(s) if not isinstance(s,tm.Trimesh) else s.copy(); assert m.is_watertight,name
 if not isinstance(s,tm.Trimesh): cq.exporters.export(s,str(OUT/(name+'.step')));SHAPES[name]=s
 MESHES[name]=m;m.export(OUT/(name+'.stl'))
 p=orient(m) if orient else m.copy();p.apply_translation([0,0,-p.bounds[0,2]]);p.export(OUT/(name+'-print.stl'));PRINT[name]=p;return p

def rotor():
 b=cyl(2.15,.72).fuse(cyl(1.6,1.90,.71)).fuse(cone(1.6,1.8,.2,2.6)).fuse(cyl(1.8,3.41,2.79))
 dog=cq.Solid.makeLoft([old.sector_wire(76,6.2),old.sector_wire(76,8.36),old.sector_wire(56,8.6)],True)
 return b.fuse(dog).fuse(dog.rotate((0,0,0),(0,0,1),180)).cut(dd(2.5,1.9,5.49,-.01)).clean()

def selector(n=2):
 cc=[-P/2,P/2] if n==2 else [0];xmin=min(cc)-2.3;xmax=max(cc)+2.3;sh=[]
 for k,z in enumerate([LO,.84]):
  b=box(xmin,-2.3,z,xmax-xmin,4.6,BLADE);d=(2.8 if n==1 else 2.5) if k==0 else 3.5
  for x in cc: b=b.cut(cyl(d/2,1.8,z-.1).translate((x,0,0)).fuse(box(x-d/2,0,z-.1,d,3,1.8)))
  sh.append(b)
 sh.append(box(xmin,-4.5,LO,xmax-xmin,2.21,HI-LO))
 if n==2:
  sh += [box(-15,-4.5,LO,15+xmin,3.4,HI-LO),box(xmax,-4.5,LO,15-xmax,3.4,HI-LO)]
 else:
  sh += [box(-1.65,-14,LO,3.3,9.51,HI-LO),box(-2.3,-14,LO,4.6,6.,HI-LO),box(-2.3,-5.7,LO,4.6,1.21,HI-LO)]
 b=sh[0]
 for s in sh[1:]:b=b.fuse(s)
 return b.clean()

def shaft():
 b=cyl(2.15,4.).fuse(dd(h=9.21,z=3.99));b=b.cut(dd(2.5,1.9,3.21,-.01));b=b.cut(cone(1.52,1.25,.4,-.01));return b.clean()

def screwbase(): return dd(h=6.60).fuse(cone(1.1,2.15,1.05,6.59)).fuse(cyl(2.15,1.2,7.64)).fuse(cyl(1.6,1.01,8.83)).clean()

def frame():
 b=box(-12.2,-7.2,-1.4,1.2,14.4,55.).fuse(box(11,-7.2,-1.4,1.2,14.4,55.))
 for y in [-7.2,6.0]: b=b.fuse(box(-12.2,y,-1.4,24.4,1.2,55.))
 # Wide viewing windows in side walls; solid rails support plates and selector windows.
 for x in [-12.3,10.9]:
  for z,h in [(15.2,7.2),(35.6,6.4),(44.6,6.8)]: b=b.cut(box(x,-5.9,z,1.4,11.8,h))
 for y in [-7.3,5.9]:
  for z,h in [(6.0,8.8),(15.2,7.2),(35.6,6.4),(44.6,6.8)]: b=b.cut(box(-9.8,y,z,19.6,1.4,h))
 decks=[(-1.4,1.2,'key'),(4.2,1.2,'shaft'),(13.6,.8,'rotor'),(22.9,.7,'rotor'),(31.3,.7,'cone'),(33.4,1.2,'neck'),(43.2,1.2,'pin'),(52.4,1.2,'pin')]
 for z,h,kind in decks:
  bplate=box(-12.2,-6,z,24.4,12,h)
  for x in [-P/2,P/2]:
   if kind=='pin':cut=box(x-2.3,-2.3,z-.1,4.6,4.6,h+.2)
   elif kind=='cone':cut=cone(1.63,2.33,.7,z).fuse(cyl(1.63,.1,z-.1)).fuse(cyl(2.33,.1,z+h)) .translate((x,0,0))
   else:cut=cyl({'key':1.5,'shaft':1.3,'rotor':2.,'neck':1.75}[kind],h+.2,z-.1).translate((x,0,0))
   bplate=bplate.cut(cut)
  b=b.fuse(bplate)
 # End windows retain the full selector stroke without thin rods.
 b=b.cut(box(-12.3,-4.65,6.20,24.6,3.7,7.32))
 # row openings above also cut any deck only where tails pass, outside rotor columns.
 # Column control tails, individually accessible on front wall.
 for x in [-P/2,P/2]: b=b.cut(box(x-1.85,5.9,23.84,3.7,1.4,7.32))
 # Added external row stop seats; windows cut all across would remove central shaft deck? no z>6.2.
 return b.clean()

def rowholder():
 # One large connected U: bridge behind frame, outer arms, tongues inside endwindows.
 b=box(-14.2,-8.6,0,28.4,1.2,3.)
 for x in [-14.2,12.3]:b=b.fuse(box(x,-7.41,0,1.9,6.1,3.))
 for x in [-14.2,11.05]:b=b.fuse(box(x,-4.61,0,3.15,3.3,3.))
 return b.clean()
def colholder():return box(-1.65,-1.4,0,3.3,3.8,3.).fuse(box(-2.3,2.39,0,4.6,3,3.)).clean()
def frameorient(m):return rotate(m,[1,0,0],90)

def assembly(r=0,c=(0,0),phase=(90,90),travels=(0,0)):
 a={name:MESHES[name].copy() for name in ['frame-back','frame-front']};a['row']=shift(MESHES['row-selector'],[0,0,R+S*r])
 for j,x in enumerate([-P/2,P/2]):
  a[f'column-{j}']=shift(rotate(MESHES['column-selector'],[1,0,0],180),[x,0,C-S*c[j]])
  a[f'input-{j}']=shift(MESHES['input-shaft'],[x,0,0]);a[f'lower-{j}']=shift(MESHES['rotor'],[x,0,R+S*r])
  a[f'upper-{j}']=shift(rotate(rotate(MESHES['rotor'],[1,0,0],180),[0,0,1],phase[j]),[x,0,C-S*c[j]])
  a[f'screw-{j}']=shift(rotate(MESHES['screw'],[0,0,1],phase[j]),[x,0,24.33]);a[f'pin-{j}']=shift(MESHES['pin'],[x,0,39.41+travels[j]])
 a['row-holder']=shift(MESHES['row-holder'],[0,0,6.2 if r==1 else 10.52])
 for j,x in enumerate([-P/2,P/2]):
  a[f'column-holder-{j}']=shift(MESHES['column-holder'],[x,7.1,23.84 if c[j]==0 else 28.16])
 return a

def tree(screw):
 pieces=[mesh(box(-1.1,-2,0,2.2,4,1.))]; contacts=[];screws=[]
 for x in [-5.,5.]:
  screws.append(shift(screw,[x,0,1.0]));pieces.append(mesh(box(x-4,-4.8,0,8,9.6,1.)))
  for y in [-3.8,3.8]:pieces.append(mesh(box(x-.8,y-.8,.9,1.6,1.6,26.81)))
  # Crossbrace to thick collar, not the functional thread.
  for sign in [-1,1]:
   ya=sign*1.98;yb=sign*3.8;pieces.append(mesh(box(x-.3,min(ya,yb),9.11,.6,abs(yb-ya),.4)));contacts.append(dict(screw_x=x,z=8.11,part='collar',sign=sign))
   # Find actual helical crest at outward side in small z windows.
   for target in [12.01,16.51,21.01,24.21]:
    best=None
    for z in np.arange(target-1.25,min(target+1.25,25.66),.06):
     section=screw.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
     if section is None:continue
     vv=section.vertices;vv=vv[np.abs(vv[:,0])<.28]
     if not len(vv):continue
     rr=max(sign*vv[:,1]);
     if best is None or rr>best[0]:best=(rr,float(z))
    rad,z=best; ya=sign*(rad-.14);yb=sign*3.8
    pieces.append(mesh(box(x-.25,min(ya,yb),z+1-.18,.5,abs(yb-ya),.36)));contacts.append(dict(screw_x=x,z=z,radial_contact=rad,penetration=.14,part='threadcrest',sign=sign))
 pieces+=screws
 (HERE/'tree-contacts.json').write_text(json.dumps(contacts,indent=2)+'\n')
 return merge(*pieces)

def main():
 export('rotor',rotor());export('row-selector',selector(),lambda m:shift(rotate(m,[1,0,0],90),[0,0,4.5]));export('column-selector',selector(1),lambda m:rotate(m,[0,1,0],90))
 export('input-shaft',shaft());export('hand-key',old.handkey());export('row-holder',rowholder());export('column-holder',colholder())
 fa=frame();back=fa.intersect(box(-20,-20,-2,40,20,60));front=fa.intersect(box(-20,0,-2,40,20,60))
 export('frame-back',back,lambda m:rotate(m,[1,0,0],-90));export('frame-front',front,lambda m:rotate(m,[1,0,0],90))
 thread=tm.load(ROOT/'tools/curated-experiment-checks/E-297/cad/e295-thread.stl',force='mesh');pin=tm.load(ROOT/'tools/curated-experiment-checks/E-297/cad/e295-pin.stl',force='mesh')
 screw=merge(mesh(screwbase()),shift(thread,[0,0,9.83]));export('screw',screw);export('pin',pin,lambda m:rotate(m,[1,0,0],180));export('screw-tree',tree(screw))
 dest=ROOT/'owner-print-tests/2026-10-17-two-cell-supported-selector';items=[]
 for name,n in [('frame-back',1),('frame-front',1),('row-selector',1),('column-selector',2),('rotor',4),('input-shaft',2),('hand-key',1),('row-holder',1),('column-holder',2),('pin',2),('screw-tree',1)]:items +=[(name,PRINT[name]) for _ in range(n)]
 old.plate('two-cell-supported-selector',items,dest)
 # old.plate resolves source using E297 OUT; replace with correct source paths.
 layout=json.loads((dest/'layout.json').read_text())
 for obj in layout:obj['source']=str(OUT.relative_to(ROOT)/(obj['name']+'-print.stl'))
 (dest/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
 for name,r,c in [('off',0,(0,0)),('both-on',1,(1,1)),('left-on',1,(1,0)),('right-on',1,(0,1))]:
  a=assembly(r,c);tm.util.concatenate(list(a.values())).export(HERE/('assembly-'+name+'.stl'))
 (HERE/'parameters.json').write_text(json.dumps(PARAMS,indent=2)+'\n')
 records={k:dict(extents_mm=v.extents.tolist(),volume_mm3=float(v.volume),watertight=bool(v.is_watertight),components=len(v.split()),sha256=hashlib.sha256((OUT/(k+'.stl')).read_bytes()).hexdigest()) for k,v in MESHES.items()};(HERE/'mesh-validation.json').write_text(json.dumps(records,indent=2)+'\n');print('ALL EXPORTED',flush=True)
if __name__=='__main__':main()
