#!/usr/bin/env python3
"""Independent E302 rigid CAD clearance screen; not physical fit verification.
Run with numpy, trimesh and manifold3d. Reads existing meshes only.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import trimesh
import manifold3d as md
H=Path(__file__).resolve().parent
OLD=H.parent/'2026-10-17-microstepper-screw-pin'
def load(path): return trimesh.load(path,force='mesh')
def solid(mesh):return md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
def rotate(m,deg,axis=[0,0,1]):
 m=m.copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg),axis));return m
def shift(m,v):m=m.copy();m.apply_translation(v);return m
half=rotate(load(H/'half.stl'),-90,[1,0,0]);frame=solid(half)+solid(rotate(half,180))
cups={n:rotate(shift(load(H/f'coupling-{n}.stl'),[0,0,-28.8]),180,[1,0,0]) for n in ['A','N','C']}
screw=shift(load(OLD/'screw.stl'),[0,0,26.2]);pin=shift(load(OLD/'pin.stl'),[0,0,33.1])
results=[]
for a in np.linspace(0,360,25):
 s=solid(rotate(screw,a));p=solid(shift(pin,[0,0,3*a/360-1.5]))
 for name,c in cups.items():
  rotor=solid(rotate(c,a));results.append(dict(angle_deg=float(a),variant=name,cup_frame_mm3=(rotor^frame).volume(),cup_screw_mm3=(rotor^s).volume(),screw_frame_mm3=(s^frame).volume(),pin_frame_mm3=(p^frame).volume()))
maxima={k:max(r[k] for r in results) for k in results[0] if k.endswith('_mm3')}
assert max(maxima.values())<1e-4,maxima
# Rigid nominal body intentionally intersects compliant contacts; quantify, do not treat as fit failure.
body=md.Manifold.cylinder(7.2,4,4,128).translate([0,0,2])
report=dict(scope='Independent nominal rigid CAD clearance screen, not physical fit or spring force validation',source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [H/'rig.scad',H/'half.stl',*[H/f'coupling-{n}.stl' for n in ['A','N','C']]]},rotation_positions=25,variants=['A','N','C'],pin_travel_mm=3,maximum_collision_volume_mm3=maxima,nominal_motor_body_contact_interference_mm3=(body^frame).volume(),nominal_clearances_mm=dict(socket_shoulder_to_thrust_deck=.49,journal_diametral=.5,screw_foot_to_keeper=.3,source_photo_gear_tip_to_socket_roof=5.3),limitations=['Motor PCB/flange extent and second gear height are unmeasured.','Motor compliant contact interference is intentional; actual force and printed deflection unknown.','No motor tooth profile fabricated for this screen: tooth entry and torque transmission remain physical tests.','Screw/pin thread meshing not requalified; reused unchanged E301 components.','Printability requires independent slicer layer support and contour inspection.'])
(H/'cad-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
