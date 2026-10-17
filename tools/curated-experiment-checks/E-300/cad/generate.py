#!/usr/bin/env python3
"""E-300 two-cell conical friction selector. Millimetres; exact E299 screw/pin retained.

The centrally hand-loaded rigid row may tilt about Y, without springs. It is a
two-contact force equalizer only; more than two independent heights are not solved.
"""
from pathlib import Path
import importlib.util,json,math,hashlib
import numpy as np
import trimesh as tm
import cadquery as cq
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; OUT=HERE/'parts'; OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('old',ROOT/'tools/curated-experiment-checks/E-297/cad/generate.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
box,cyl,cone,dd,mesh,merge,shift,rotate=old.box,old.cyl,old.cone,old.dd,old.mesh,old.merge,old.shift,old.rotate
P=5.08; S=3.; R=8.; C=29.36; BLADE=2.4; LO=-2.64; HI=5.36
PARAMS=dict(pitch=P,stroke=S,lower_base_off=R,upper_base_off=C,flange_thickness=.72,flange_diameter=4.3,fully_on_base_distance=15.36,cone_half_angle_deg=45,male_contact_z=[6.2,6.7],male_contact_r=[1.9,1.4],female_inner_z=[8.56,9.21],female_inner_r=[1.3,1.95],female_floor_z=8.56,tip_axial_clearance=.10,mouth_axial_extension=.05,cup_outer_diameter=4.7,cup_minimum_rim=.4,cup_pitch_gap=.38,selector_blade=BLADE,selector_capture_gap=1.20,selector_capture_play=.48,selector_height=HI-LO,selector_upper_fork=3.7,selector_upper_fork_tip=4.1,selector_lower_fork=2.8,selector_outer_width=4.6,neck_height=5.52,neck_transition_top=5.72,rotor_hub_diameter=3.6,guide_diameter=4.,row_tilt_degrees=3.,row_central_overtravel=.75,nominal_row_first_load_base=11.52,nominal_column_reaction_base=26.40,nominal_loaded_male_base=11.28,nominal_loaded_female_base=26.64,input_socket_depth=3.2,rotor_socket_depth=5.68,input_tip_z=13.0,selector_upper_blade=4.4,selector_blade_y=4.3,selector_spine_y=[-2.77,-2.31],selector_spine_top_rear_relief=.9,selector_top_print_ramp_y=[-2.60,-2.14],thread_source='E-299/cad/parts/screw.stl (exact retained mesh)',pin_source='E-299/cad/parts/pin.stl (exact retained mesh)',guide_note='Selector sweeps remove rear sectors of guide decks; front guide sectors retained. Test tooling only.')
SHAPES={}; MESHES={}; PRINT={}
def export(name,s,orient=None):
 m=mesh(s) if not isinstance(s,tm.Trimesh) else s.copy(); assert m.is_watertight,name
 if not isinstance(s,tm.Trimesh): cq.exporters.export(s,str(OUT/(name+'.step')));SHAPES[name]=s
 MESHES[name]=m;m.export(OUT/(name+'.stl'))
 p=orient(m) if orient else m.copy();p.apply_translation([0,0,-p.bounds[0,2]]);p.export(OUT/(name+'-print.stl'));PRINT[name]=p;return p

def rotor(female=False):
 b=cyl(2.15,.72).fuse(cyl(1.6,4.82,.71)).fuse(cone(1.6,1.8,.2,5.52)).fuse(cyl(1.8,.49,5.71))
 if female:
  # Flat printable base, 45-degree expanding outer shoulder, blind conical cup.
  b=b.fuse(cone(1.8,2.35,1.76,6.19)).fuse(cyl(2.35,1.27,7.94))
  b=b.cut(cone(1.3,1.95,.65,8.56).fuse(cyl(1.95,.05,9.21)))
 else:
  b=b.fuse(cone(1.9,1.4,.5,6.2))
 return b.cut(dd(2.5,1.9,5.69,-.01)).clean()

def selector(n=2,tooling=True):
 cc=[-P/2,P/2] if n==2 else [0];xmin=min(cc)-2.3;xmax=max(cc)+2.3;sh=[];lower_relief=None
 for k,z in enumerate([LO,.96]):
  thick=BLADE if k==0 else 4.4
  b=box(xmin,-2.15,z,xmax-xmin,4.3,thick);d=2.8 if k==0 else 3.7
  for x in cc:
   cut=cyl(d/2,thick+.2,z-.1).fuse(box(-d/2,0,z-.1,d,3,thick+.2))
   if k==1:
    # Flare the long upper U away from its flange-bearing face. This keeps the
    # capture lip at D3.7 while a tilted rigid row clears vertical rotor necks.
    rings=[]
    for zz,rr in [(z-.01,1.85),(z+thick+.01,2.05)]:
     rings.append(cq.Wire.makePolygon([cq.Vector(xx,yy,zz) for xx,yy in [(-rr,0),(rr,0),(rr,3),(-rr,3),(-rr,0)]]))
    cut=cut.fuse(cone(1.85,2.05,thick+.02,z-.01)).fuse(cq.Solid.makeLoft(rings,True))
   if n==1 and k==0:
    # The fixed screw thrust cone sweeps past the outside of this blade when OFF.
    # Retain a thick flange-side lip, relieve only its remote underside. A full
    # 2.4-mm straight fork would collide with the unchanged E299 screw support.
    rings=[]
    for zz,rr in [(z-.01,2.32),(z+BLADE+.01,1.39)]:
     rings.append(cq.Wire.makePolygon([cq.Vector(xx,yy,zz) for xx,yy in [(-rr,0),(rr,0),(rr,3),(-rr,3),(-rr,0)]]))
    cut=cut.fuse(cone(2.32,1.39,BLADE+.02,z-.01)).fuse(cq.Solid.makeLoft(rings,True))
    lower_relief=cut
   b=b.cut(cut.translate((x,0,0)))
  sh.append(b)
 sh.append(box(xmin,-2.77,LO,xmax-xmin,.46,HI-LO-.9))
 sh.append(box(xmin,-2.6,HI-.9,xmax-xmin,.29,.9))
 # Blades reach back into the thin full-height spine, outside the flange envelope.
 for za,hh in [(LO,BLADE),(.96,4.4-.9)]:sh.append(box(xmin,-2.77,za,xmax-xmin,.63,hh))
 sh.append(box(xmin,-2.6,HI-.9,xmax-xmin,.46,.9))
 if tooling:
  if n==2:
   sh += [box(-12,-4.5,LO,12+xmin+.01,3.4,HI-LO),box(xmax-.01,-4.5,LO,12-xmax+.01,3.4,HI-LO)]
   # Central force is applied through this broad paddle behind the frame. No row lock.
   # Near-45-degree wings support the central paddle during printing on the rear face.
   # At y=-13 only the 6-mm-wide hand pad touches the bed; width grows to 24 mm
   # by the backbone, avoiding the former floating rail behind a rectangular pad.
   wire=cq.Wire.makePolygon([cq.Vector(x,y,LO) for x,y in [(-3,-13),(3,-13),(12,-4.49),(-12,-4.49),(-3,-13)]])
   sh += [cq.Solid.extrudeLinear(wire,[],cq.Vector(0,0,HI-LO)),box(-3,-4.5,LO,6,1.74,HI-LO)]
  else:
   sh += [box(-1.65,-14,LO,3.3,9.51,HI-LO),box(-2.3,-14,LO,4.6,6.,HI-LO),box(-2.3,-5.04,LO,4.6,2.28,HI-LO)]
   shoulder=cq.Wire.makePolygon([cq.Vector(xx,yy,LO) for xx,yy in [(-1.65,-5.70),(1.65,-5.70),(2.3,-5.04),(-2.3,-5.04),(-1.65,-5.70)]])
   sh.append(cq.Solid.extrudeLinear(shoulder,[],cq.Vector(0,0,HI-LO)))
 b=sh[0]
 for s in sh[1:]:b=b.fuse(s)
 if lower_relief is not None:b=b.cut(lower_relief)
 # Subtract a roof wedge from the rear relief. During rear-face printing the
 # upper cap then grows gradually instead of beginning as a 9-mm orphan wall.
 # This only removes material from the checked raster envelope.
 ramp=cq.Wire.makePolygon([cq.Vector(xmin-.01,yy,zz) for yy,zz in [(-2.60,HI-.9),(-2.14,HI),(-2.14,HI+.1),(-2.60,HI+.1),(-2.60,HI-.9)]])
 b=b.cut(cq.Solid.extrudeLinear(ramp,[],cq.Vector(xmax-xmin+.02,0,0)))
 return b.clean()

def shaft():
 b=cyl(2.15,4.).fuse(dd(h=9.01,z=3.99));b=b.cut(dd(2.5,1.9,3.21,-.01));b=b.cut(cone(1.52,1.25,.4,-.01));return b.clean()

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
 # Entire moving selector envelope, including clearance for +/-3 degree row tilt.
 # The thicker fork crosses former full guide decks. Preserve their front sectors
 # rather than silently colliding with a deck or claiming full annular guidance.
 row=selector()
 for zbase in [R-.35,R+S+.75]:
  for tilt in [-3.,0.,3.]:
   moving=row.rotate((0,0,0),(0,1,0),tilt).translate((0,0,zbase))
   b=b.cut(moving)
 # Conservative continuous swept blade and backbone volumes (0.16 mm guide play).
 for z,d,thick in [(R+LO-.35-.85,2.8,2.4),(R+.96-.35-.85,3.7,4.4)]:
  env=box(-5.1,-2.65,z,10.2,5.3,thick+S+1.1+1.7)
  for x in [-P/2,P/2]:
   env=env.cut(cyl(max(.1,d/2-.22),thick+S+3.,z-.01).translate((x,0,0)).fuse(box(x-d/2+.22,0,z-.01,d-.44,3,thick+S+3.)))
  b=b.cut(env)
 b=b.cut(box(-12.3,-6.1,4.15,24.6,5.16,13.82))
 b=b.cut(box(-10.8,-7.3,4.15,21.6,2.9,13.82))
 # Column control tails, individually accessible on front wall.
 for x in [-P/2,P/2]:
  b=b.cut(box(x-1.85,5.9,20.84,3.7,1.4,11.32))
  # Column blades point toward -Y after inversion; their open mouths toward -Y.
  for z,d,thick in [(C-S-HI-.16,3.7,4.4),(C-S+.24-.16,2.8,2.4)]:
   env=box(x-2.46,-2.46,z,4.92,4.92,thick+S+.32)
   env=env.cut(cyl(d/2-.16,thick+S+.34,z-.01).translate((x,0,0)).fuse(box(x-d/2+.16,-3,z-.01,d-.32,3,thick+S+.34)))
   b=b.cut(env)
  b=b.cut(box(x-1.81,5.69,20.84,3.62,.32,11.32))
  b=b.cut(box(x-2.46,2.29,20.84,4.92,3.57,11.32))
 return b.clean()

def colholder():return box(-1.65,-1.4,0,3.3,3.8,3.).fuse(box(-2.3,2.39,0,4.6,3,3.)).clean()
def frameorient(m):return rotate(m,[1,0,0],90)

def assembly(r=0,c=(0,0),phase=(90,90),travels=(0,0),row_tilt=0,lower_offsets=(0,0),upper_offsets=(0,0)):
 a={name:MESHES[name].copy() for name in ['frame-back','frame-front']};a['row']=shift(rotate(MESHES['row-selector'],[0,1,0],row_tilt),[0,0,R+S*r])
 for j,x in enumerate([-P/2,P/2]):
  a[f'column-{j}']=shift(rotate(MESHES['column-selector'],[1,0,0],180),[x,0,C-S*c[j]])
  a[f'input-{j}']=shift(MESHES['input-shaft'],[x,0,0]);a[f'lower-{j}']=shift(MESHES['male-rotor'],[x,0,R+S*r+lower_offsets[j]])
  a[f'upper-{j}']=shift(rotate(rotate(MESHES['female-rotor'],[1,0,0],180),[0,0,1],phase[j]),[x,0,C-S*c[j]+upper_offsets[j]])
  a[f'screw-{j}']=shift(rotate(MESHES['screw'],[0,0,1],phase[j]),[x,0,24.33]);a[f'pin-{j}']=shift(MESHES['pin'],[x,0,39.41+travels[j]])
 for j,x in enumerate([-P/2,P/2]):
  a[f'column-holder-{j}']=shift(MESHES['column-holder'],[x,7.1,20.96 if c[j]==0 else 29.04])
 return a

def main():
 export('row-selector-core',selector(2,False));export('column-selector-core',selector(1,False));export('male-rotor',rotor());export('female-rotor',rotor(True));export('row-selector',selector(),lambda m:shift(rotate(m,[1,0,0],90),[0,0,4.5]));export('column-selector',selector(1),lambda m:rotate(m,[1,0,0],90))
 export('input-shaft',shaft());export('hand-key',old.handkey());export('column-holder',colholder())
 fa=frame();back=fa.intersect(box(-20,-20,-2,40,20,60));front=fa.intersect(box(-20,0,-2,40,20,60))
 export('frame-back',back,lambda m:rotate(m,[1,0,0],-90));export('frame-front',front,lambda m:rotate(m,[1,0,0],90))
 screw=tm.load(ROOT/'tools/curated-experiment-checks/E-299/cad/parts/screw.stl',force='mesh');pin=tm.load(ROOT/'tools/curated-experiment-checks/E-299/cad/parts/pin.stl',force='mesh')
 export('screw',screw);export('pin',pin,lambda m:rotate(m,[1,0,0],180))
 # Preserve the complete supported E299 screw print mesh, including all twenty tabs.
 export('screw-tree',tm.load(ROOT/'tools/curated-experiment-checks/E-299/cad/parts/screw-tree.stl',force='mesh'))
 dest=ROOT/'owner-print-tests/2026-10-17-cone-friction-selector';items=[]
 for name,n in [('frame-back',1),('frame-front',1),('row-selector',1),('column-selector',2),('male-rotor',2),('female-rotor',2),('input-shaft',2),('hand-key',1),('column-holder',2),('pin',2),('screw-tree',1)]:items +=[(name,PRINT[name]) for _ in range(n)]
 old.plate('cone-friction-selector',items,dest)
 # old.plate resolves source using E297 OUT; replace with correct source paths.
 layout=json.loads((dest/'layout.json').read_text())
 for obj in layout:obj['source']=str(OUT.relative_to(ROOT)/(obj['name']+'-print.stl'))
 (dest/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
 for name,r,c in [('off',0,(0,0)),('both-on',1,(1,1)),('left-on',1,(1,0)),('right-on',1,(0,1))]:
  a=assembly(r,c);tm.util.concatenate(list(a.values())).export(HERE/('assembly-'+name+'.stl'))
 # Nominal first loaded contact after taking up .24-mm axial play at each rotor
 # capture plus .04-mm column-holder seating play. Further hand force may flex
 # surfaces; this file models geometry only, without elastic strain or friction.
 a=assembly(r=1+.52/S,c=(1-.04/S,)*2,lower_offsets=(-.24,)*2,upper_offsets=(.24,)*2)
 tm.util.concatenate(list(a.values())).export(HERE/'assembly-both-loaded.stl')
 (HERE/'parameters.json').write_text(json.dumps(PARAMS,indent=2)+'\n')
 records={k:dict(extents_mm=v.extents.tolist(),volume_mm3=float(v.volume),watertight=bool(v.is_watertight),components=len(v.split()),sha256=hashlib.sha256((OUT/(k+'.stl')).read_bytes()).hexdigest()) for k,v in MESHES.items()};(HERE/'mesh-validation.json').write_text(json.dumps(records,indent=2)+'\n');print('ALL EXPORTED',flush=True)
if __name__=='__main__':main()
