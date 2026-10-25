#!/usr/bin/env python3
"""OpenSCAD bodies + exact inherited thread/pin meshes; lengths are parameterized here."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np, trimesh, manifold3d as md
P=Path(__file__).resolve().parents[1]; C=P/'components'; M=P/'metadata'; CAD=P/'cad'
THREAD_LENGTH=27.; BODY_HEIGHT=3.6; END_CHAMFER=.6
V3=P.parent/'2026-10-19-microstepper-frame-v3'; V2=P.parent/'2026-10-18-microstepper-frame-v2'
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def mesh(s):
 m=s.to_mesh();return trimesh.Trimesh(m.vert_properties,m.tri_verts,process=False)
def save(n,m):
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,(n,m.is_watertight,m.is_winding_consistent,len(m.split()))
 m.export(C/(n+'.stl'));return m
def scad(n,part,src='minimal.scad'):
 r=subprocess.run(['openscad','-o',str(C/(n+'.stl')),'-D',f'part="{part}"','-D',f'body_h={BODY_HEIGHT}',str(CAD/src)],capture_output=True,text=True,check=True)
 assert 'ERROR' not in r.stderr,r.stderr
 return save(n,trimesh.load(C/(n+'.stl'),force='mesh'))
parts={}
for n,p in [('A-front','front'),('A-back','back'),('A-rotor-base','rotor-base'),('C-guide','guide-coupon')]:parts[n]=scad(n,p)
# Preserve helix/profile/phase; move exactly 27 mm of the original 48-mm thread.
base=solid(parts.pop('A-rotor-base')); (C/'A-rotor-base.stl').unlink()
old=trimesh.load(V2/'components/screw-long.stl',force='mesh')
thread=solid(old)^md.Manifold.cube([4,4,THREAD_LENGTH+.001]).translate([-2,-2,2.399])
thread=thread.translate([0,0,BODY_HEIGHT-2.4]) # historical thread starts2.4 -> new3.6
# A 0.6-mm end chamfer changes only the final partial turn, outside working engagement.
envelope=md.Manifold.cylinder(THREAD_LENGTH-END_CHAMFER,1.65,1.65,96)+md.Manifold.cylinder(END_CHAMFER,1.65,.7,96).translate([0,0,THREAD_LENGTH-END_CHAMFER])
thread=thread^envelope.translate([0,0,BODY_HEIGHT])
parts['A-screw']=save('A-screw',mesh(base+thread+md.Manifold.cylinder(.04,.69,.69,96).translate([0,0,BODY_HEIGHT-.02])))
parts['A-screw-supported']=scad('A-screw-supported','rotor-supported')
# Remove only the old sacrificial foot, preserve the exact female functional geometry.
for length,name in [(18,'pin'),(50,'pin-50')]:
 oldpin=trimesh.load(V3/'components'/f'{name}.stl',force='mesh')
 p=mesh(solid(oldpin)^md.Manifold.cube([4.4,4.4,length+.01]).translate([-2.2,-2.2,-.001]))
 parts[f'C-pin-{length}-upright']=save(f'C-pin-{length}-upright',p)
p=parts['C-pin-18-upright'].copy();p.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,0,1]));p.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));p.apply_translation([0,18,2.2])
parts['C-pin-18-horizontal']=save('C-pin-18-horizontal',p)
for n,p in [('B-stand','stand'),('B-pin','pin'),('B-boundary','boundary'),('B-liner','liner'),('B-spacer-3','spacer-3'),('B-spacer-15','spacer-15')]:parts[n]=scad(n,p,'neighbors.scad')
# Compact pair of plates. Primary uses existing motor, shim, washer, footless pin50.
layouts={
 'A-first':[('A-front',18,4,'A front'),('A-back',53,4,'A back'),('A-screw-supported',83,24,'A screw')],
 'BC-comparisons':[('B-stand',18,18,'B stand inverted'),('B-boundary',49,18,'B boundary inverted'),('B-liner',78,17,'B closer play'),
                  ('C-pin-18-upright',80,43,'C upright 1'),('C-pin-18-upright',94,43,'C upright 2'),
                  ('C-pin-18-horizontal',80,58,'C horizontal 1'),('C-pin-18-horizontal',94,58,'C horizontal 2'),('C-guide',106,42,'C guide')]
}
for i in range(9):layouts['BC-comparisons'].append(('B-pin',8+10*(i%6),46+18*(i//6),f'B pin {i+1}'))
for i in range(8):layouts['BC-comparisons'].append(('B-spacer-3',8+8*i,86,f'B low {i+1}'))
for i in range(4):layouts['BC-comparisons'].append(('B-spacer-15',8+9*i,98,f'B raised {i+1}'))
layout_data={}
for name,entries in layouts.items():
 meshes=[];rows=[]
 for source,x,y,label in entries:
  m=parts[source].copy();m.apply_translation([x,y,0]);meshes.append(m)
  rows.append(dict(source=source,name=label,center_xy=[x,y],bounds_mm=m.bounds.tolist()))
 plate=trimesh.util.concatenate(meshes);plate.export(C/(name+'.stl'));layout_data[name]=rows
(M/'layout.json').write_text(json.dumps(layout_data,indent=2)+'\n')
report={n:dict(bounds_mm=m.bounds.tolist(),volume_mm3=m.volume,watertight=m.is_watertight,bodies=len(m.split()),sha256=hashlib.sha256((C/(n+'.stl')).read_bytes()).hexdigest()) for n,m in parts.items()}
(M/'meshes.json').write_text(json.dumps(report,indent=2)+'\n')
(M/'source.json').write_text(json.dumps(dict(baseline_commit='1071f695b93951246a2865038e7fb9de9bdf2a05',sources={str(p.relative_to(P.parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for p in [V2/'components/screw-long.stl',V3/'components/pin.stl',V3/'components/pin-50.stl',V3/'cad/rig.scad']},thread_length_mm=THREAD_LENGTH,body_length_mm=BODY_HEIGHT,travel_mm=[0,15]),indent=2)+'\n')
print('Generated',len(parts),'components and two plates')
