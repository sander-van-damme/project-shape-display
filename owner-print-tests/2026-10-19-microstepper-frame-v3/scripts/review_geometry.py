"""Rigid mesh checks; measured motor geometry and physical reliability unknown."""
import json,hashlib
import numpy as np
import trimesh
import manifold3d as md
from paths import *
def load(n):return trimesh.load(COMPONENTS/(n+'.stl'),force='mesh')
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def rot(m,a,axis=[0,0,1]):
 m=m.copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(a),axis));return m
def move(m,v):m=m.copy();m.apply_translation(v);return m
front=rot(move(load('front'),[0,0,-6.5]),90,[1,0,0])
back=rot(move(load('back'),[0,0,-6.5]),90,[1,0,0]);back.apply_scale([1,-1,1])
f,b=solid(front),solid(back);frame=f+b
rotor=move(load('rotor'),[0,0,12.2])
rows=[]
for a in np.linspace(0,360,25):
 r=solid(rot(rotor,-a));p=solid(move(load('pin'),[0,0,27.2+3*a/360]))
 rows.append(dict(angle_deg=float(a),rotor_frame_mm3=(r^frame).volume(),pin_frame_mm3=(p^frame).volume(),rotor_pin_mm3=(r^p).volume()))
maxima={k:max(r[k]for r in rows)for k in rows[0]if k.endswith('mm3')}
assert max(maxima.values())<.0001,maxima
assert (f^b).volume()<.0001
pcb=md.Manifold.cube([5.5,7,8.5]).translate([-8,-3.5,2]);assert (pcb^frame).volume()<.0001
body=md.Manifold.cylinder(7.2,4,4,128).translate([0,0,2]);assert (body^frame).volume()<.0001
shim_checks=[]
for t,n in[(.60,'spacer-060'),(.72,'spacer-072'),(.84,'spacer-084')]:
 shim=solid(move(rot(load(n),90,[0,1,0]),[4.7-t,-1,3]))
 clash=(shim^frame).volume();assert clash<.0001,(n,clash)
 shim_checks.append(dict(thickness_mm=t,frame_collision_mm3=clash,nominal_motor_interference_mm3=(shim^body).volume(),nominal_tangent_available_width_mm=8.8-t))
# Original thread symmetry difference, including original tip chamfer.
old=trimesh.load(TEST_DIR.parent/'2026-10-18-microstepper-frame-v2/components/screw.stl',force='mesh')
clip=md.Manifold.cube([10,10,16.001]).translate([-5,-5,24.20001])
a=solid(move(old,[0,0,21.8]))^clip;b=solid(rotor)^clip
diff=(a-b).volume()+(b-a).volume();assert diff<.0001,diff
# Upward stop at .30, rotating body still clear at both axial extremes.
assert (solid(move(rotor,[0,0,.3]))^frame).volume()<.0001
# Washer is positively located in OD7.3 pocket. No motor-shaft loading modeled.
washer=(md.Manifold.cylinder(.5,3.5,3.5,128)-md.Manifold.cylinder(.5,1.6,1.6,128)).translate([0,0,11.7])
assert (washer^frame).volume()<.0001 and (washer^solid(rotor)).volume()<.0001
report=dict(scope='CAD only',spacers=shim_checks,sampled_poses=rows,max_collision_mm3=maxima,frame_half_intersection_mm3=(f^solid(back)).volume(),thread_symmetric_difference_mm3=diff,pcb_envelope_collision_mm3=(pcb^frame).volume(),nominal_motor_collision_mm3=(body^frame).volume(),radial_rotor_clearance_mm=.2,axial_float_mm=.3,pin_top_above_frame_mm=[5.2,8.2],socket_mouth_z_mm=12.2,straight_ribs_z_mm=[12.7,18.2],worst_case_straight_ribs_at_max_lift_mm=[13,18.5],photo_only_gear_tip_z_mm=14.2,photo_only_max_overlap_at_max_lift_mm=1.2,washer_dimensions_mm=[3.2,7,.5],unknowns=['Actual tooth lower/upper heights, boss and PCB envelope','Motor fit and spacer preload','Friction, slip and printed dimensions','Physical motion not performed'])
(METADATA/'cad-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='sampled_poses'},indent=2))
# Illustrative actual mesh views, no invented hardware dimensions.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(11,5))
for i,meshes,title in [(1,[(front,'#7296ad'),(rotor,'#db9f43'),(move(load('pin'),[0,0,28.7]),'#63a68f')],'Open assembly — one half omitted'),(2,[(move(load(p['source']),[*p['center_xy'],0]),'#7296ad' if p['source'] in ['front','back'] else '#db9f43')for p in json.loads((METADATA/'layout.json').read_text())],'Print plate — outer faces on bed')]:
 ax=fig.add_subplot(1,2,i,projection='3d')
 for mesh,c in meshes:ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor=c,linewidth=0))
 if i==1:ax.set(xlim=(-18,18),ylim=(-12,12),zlim=(0,50));ax.set_box_aspect((36,24,50));ax.view_init(24,-65)
 else:ax.set(xlim=(0,72),ylim=(0,60),zlim=(0,30));ax.set_box_aspect((72,60,30));ax.view_init(50,-65)
 ax.set_title(title);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
fig.tight_layout();fig.savefig(IMAGES/'cad.png',dpi=150)
