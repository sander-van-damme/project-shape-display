#!/usr/bin/env python3
"""Reproduce DES-010 nominal parts; exact inherited thread profile retained."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np,trimesh,manifold3d as md
P=Path(__file__).resolve().parents[1];C=P/'components';M=P/'metadata'
def solid(m):return md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
def mesh(s):
 m=s.to_mesh();return trimesh.Trimesh(m.vert_properties,m.tri_verts,process=False)
def save(n,m):
 assert m.is_watertight and m.is_winding_consistent,(n,'badmesh')
 m.export(C/(n+'.stl'));return m
parts={}
for n in ['bank','lower0','lower1','lower2','upper','guide','cupbase','male','rotor','motorpulley','yoke','spacer','endblock','foot','springseat','strap','index','cap','torque-arm','yoke-long','motorplate']:
 subprocess.run(['openscad','-o',str(C/(n+'.stl')),'-D',f'part="{n}"',str(P/'cad/bank.scad')],check=True,capture_output=True)
 parts[n]=save(n,trimesh.load(C/(n+'.stl'),force='mesh'))
old=P.parent/'2026-10-25-minimal-friction-screw-frame/components/A-screw.stl'
a=solid(trimesh.load(old,force='mesh'));thread=(a^md.Manifold.cube([4,4,27.001]).translate([-2,-2,3.599])).translate([0,0,4.6])
parts['screw']=save('screw',mesh(solid(parts.pop('cupbase'))+thread))
(C/'cupbase.stl').unlink()
oldpin=P.parent/'2026-10-25-minimal-friction-screw-frame/components/C-pin-50-upright.stl'
female=solid(trimesh.load(oldpin,force='mesh'))^md.Manifold.cube([4.4,4.4,40]).translate([-2.2,-2.2,0])
# Only add outer 0.05mm per face; inherited female helix/cavity remain exactly unchanged.
shell=md.Manifold.cube([4.5,4.5,40]).translate([-2.25,-2.25,0])-md.Manifold.cube([4.4,4.4,40.02]).translate([-2.2,-2.2,-.01])
parts['pin']=save('pin',mesh(female+shell))
# Two sacrificial screw braces, same print orientation/neck scheme as A, repositioned thread start.
subprocess.run(['openscad','-o',str(C/'screw-supported.stl'),'-D','part="screw-supported"',str(P/'cad/bank.scad')],check=True,capture_output=True)
parts['screw-supported']=save('screw-supported',trimesh.load(C/'screw-supported.stl',force='mesh'))
# Flatten wide rail bank by keeping assembly z datums and shifting bed underside.
parts['bank'].apply_translation([0,0,-3]);save('bank',parts['bank'])
# Hand-test three nominal sliding-key pairs; root/bore relief variants only rotor bore via SCAD later.
layouts={ 'mechanical':[], 'actuator':[] }
def add(n,x,y,count=1):
 for i in range(count):layouts['mechanical'].append(dict(source=n,name=f'{n}-{len(layouts["mechanical"])+1}',center_xy=[x,y]))
add('bank',40,85);add('motorplate',115,258.5)
add('endblock',0,0);add('endblock',0,13)
for i,n in enumerate(['lower0','lower1','lower2']):add(n,150,12+i*20)
for i,n in enumerate(['upper','guide','guide']):add(n,105+i*36,76)
for i in range(4):add('screw-supported',102+i*22,102);add('pin',12+i*16,143);add('foot',8+i*16,115)
for i in range(2):add('male',110+i*16,150);add('rotor',146+i*12,150);add('yoke' if i==0 else 'yoke-long',183+i*12,130)
add('torque-arm',150,185);add('cap',80,180);add('motorpulley',90,149);add('index',184,170)
for i in range(4):add('strap',10+i*14,195)
for i in range(4):add('spacer',100+i*12,163)
for i in range(2):add('springseat',105+i*10,180)
# Small tolerant interfaces; no full alternate prototypes.
for n,part,var in [('rotor-tight','rotor','key_open=2.2'),('rotor-loose','rotor','key_open=2.4'),('guide-46','guide-coupon','guide_open=4.6'),('guide-47','guide-coupon','guide_open=4.7'),('guide-48','guide-coupon','guide_open=4.8')]:
 subprocess.run(['openscad','-o',str(C/(n+'.stl')),'-D',f'part="{part}"','-D',var,str(P/'cad/bank.scad')],check=True,capture_output=True)
 parts[n]=save(n,trimesh.load(C/(n+'.stl'),force='mesh'))
for i,n in enumerate(['rotor-tight','rotor-loose','guide-46','guide-47','guide-48']):layouts['actuator'].append(dict(source=n,name=n,center_xy=[20+i*22,118]))
for n in ['base','slider','bobbin','follower','bridge']:
 src=P/'cad/actuator.scad'
 if not src.exists():continue
 subprocess.run(['openscad','-o',str(C/('actuator-'+n+'.stl')),'-D',f'part="{n}"',str(src)],check=True,capture_output=True)
 parts['actuator-'+n]=save('actuator-'+n,trimesh.load(C/('actuator-'+n+'.stl'),force='mesh'))
if (P/'cad/actuator.scad').exists():
 for n,x,y in [('base',32,49),('slider',68,29),('bobbin',78,59),('bobbin',94,59),('follower',94,29),('bridge',94,85)]:layouts['actuator'].append(dict(source='actuator-'+n,name=f'actuator-{n}-{x}',center_xy=[x,y]))
for i in range(3):
 layouts['actuator'].append(dict(source='rotor',name=f'nominal-rotor-{i+1}',center_xy=[130+i*15,60]))
 layouts['actuator'].append(dict(source='male',name=f'nominal-male-{i+1}',center_xy=[130+i*15,76]))
layouts['actuator'].append(dict(source='pin',name='fit-pin-4.50',center_xy=[130,20]))
allreport={}

for name,rows in layouts.items():
 if not rows:continue
 meshes=[]
 for r in rows:
  m=parts[r['source']].copy();m.apply_translation([*r['center_xy'],0]);r['bounds_mm']=m.bounds.tolist();meshes.append(m)
 trimesh.util.concatenate(meshes).export(C/(name+'.stl'))
(M/'layout.json').write_text(json.dumps(layouts,indent=2)+'\n')
for n,m in parts.items():allreport[n]=dict(bounds_mm=m.bounds.tolist(),volume_mm3=float(m.volume),watertight=m.is_watertight,bodies=len(m.split()),sha256=hashlib.sha256((C/(n+'.stl')).read_bytes()).hexdigest())
(M/'meshes.json').write_text(json.dumps(allreport,indent=2)+'\n')
print('parts',len(parts))
