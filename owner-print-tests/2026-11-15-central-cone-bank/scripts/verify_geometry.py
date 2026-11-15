#!/usr/bin/env python3
"""Independent nominal mesh interference review; does not qualify physical fits."""
from pathlib import Path
import json
import numpy as np,trimesh,manifold3d as md
P=Path(__file__).resolve().parents[1]
def load(n):return trimesh.load(P/'components'/(n+'.stl'),force='mesh')
def pose(n,t=(0,0,0),angle=None):
 m=load(n)
 if angle is not None:m.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]))
 m.apply_translation(t);return m

def solid(m):return md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
def common(a,b):return float((solid(a)^solid(b)).volume())
R=[]
def check(label,a,b,allow=0.001):
 v=common(a,b);R.append(dict(check=label,intersection_mm3=v,limit_mm3=allow,pass_nominal=v<=allow));return v
bank=pose('bank',(0,0,3))
for i in range(2):
 x=i*5.08;rot=pose('rotor',(x,0,12));check(f'rotor{i}-bank',rot,bank)
 for drop in [0,2,2.4,2.7]:
  male=pose('male',(x,0,11-drop));yoke=load('yoke-long' if i else 'yoke');yoke.apply_translation([0,0,-2.45]);yoke.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]));yoke.apply_transform(trimesh.transformations.rotation_matrix(0,[0,0,1]));yoke.apply_translation([x,0,29-drop])
  check(f'male{i}-bank-drop{drop}',male,bank);check(f'male{i}-rotor-drop{drop}',male,rot);check(f'yoke{i}-bank-drop{drop}',yoke,bank);check(f'yoke{i}-rotor-drop{drop}',yoke,rot);check(f'yoke{i}-male-drop{drop}',yoke,male)
  for j in range(2):
   for k in range(2):check(f'male{i}-resident{j}{k}-drop{drop}',male,pose('screw',(j*5.08,k*5.08,29)));check(f'yoke{i}-resident{j}{k}-drop{drop}',yoke,pose('screw',(j*5.08,k*5.08,29)))
 for j in range(2):
  for k in range(2):
   s=pose('screw',(j*5.08,k*5.08,29));check(f'rotor{i}-resident{j}{k}',rot,s)
for j in range(2):
 for k in range(2):
  s=pose('screw',(j*5.08,k*5.08,29))
  for n,z in [('lower0',31.35),('lower1',31.35),('lower2',31.35),('upper',35.05)]:check(f'screw{j}{k}-{n}',s,pose(n,(0,0,z)))
  for travel in [0,4,8]:
   pin=pose('pin',(j*5.08,k*5.08,40.2+travel));check(f'pin{j}{k}-screw-travel{travel}',pin,pose('screw',(j*5.08,k*5.08,29),-120*travel))
   for z in [50,66]:check(f'pin{j}{k}-guide{z}-travel{travel}',pin,pose('guide',(0,0,z)))
for cx in [-42,47]:
 for cy in [-5,10.08]:
  foot=pose('foot',(cx-6,cy-6,0))
  for row in [0,5.08]:check(f'foot{cx},{cy}-bank-row{row}',foot,pose('bank',(0,row,3)))
for row in [0,1.27,2.54,3.81,5.08]:
 for i in range(2):
  for j in range(2):
   for k in range(2):check(f'parked-male{i}-resident{j}{k}-bank-y{row}',pose('male',(i*5.08,row,8.3)),pose('screw',(j*5.08,k*5.08,29)))
for cx in [-42,47]:
 for z in [29.35,33.95]:
  strap=pose('strap',(cx,0,z))
  for row in [0,5.08]:check(f'strap{cx},{z}-bankrow{row}',strap,pose('bank',(0,row,3)))
  for n in ['lower0','lower1','lower2']:check(f'strap{cx},{z}-{n}',strap,pose(n,(0,0,31.35)))
layout_report=[]
for job,rows in json.loads((P/'metadata/layout.json').read_text()).items():
 models=[]
 for r in rows:
  m=pose(r['source'],(*r['center_xy'],0));models.append((r['name'],m))
  layout_report.append(dict(job=job,part=r['name'],on_bed=bool(m.bounds[0,2]>=-.001),inside_bed=bool(np.all(m.bounds[0,:2]>=0) and np.all(m.bounds[1,:2]<=256))))
 for i,(a,am) in enumerate(models):
  for b,bm in models[i+1:]:
   if np.all(np.minimum(am.bounds[1],bm.bounds[1])-np.maximum(am.bounds[0],bm.bounds[0])>0):check(f'layout-{job}:{a}-vs-{b}',am,bm)
for row in [0,5.08]:
 for ey in [-70,35]:check(f'endblock-y{ey}-bankrow{row}',pose('endblock',(-36,ey,0)),pose('bank',(0,row,3)))
 if (P/'components/index.stl').exists():check(f'index-bankrow{row}',pose('index',(41.5,19,14)),pose('bank',(0,row,3)))
if (P/'components/cap.stl').exists():
 cap=pose('cap',(0,0,18.2));check('cap-bank',cap,bank)
 for i in range(2):
  x=i*5.08;rot=pose('rotor',(x,0,12));check(f'cap-rotor{i}',cap,rot)
  for h in [24,22,20,18,16,14,13,12]:check(f'rotor{i}-insertion-z{h}-bank',pose('rotor',(x,0,h)),bank)
  for z in [26,24,22,20,18.2]:check(f'cap-insertion-z{z}-rotor{i}',pose('cap',(0,0,z)),rot)
  for drop in [0,2,2.4,2.7]:
   check(f'cap-male{i}-drop{drop}',cap,pose('male',(x,0,11-drop)))
   y=load('yoke-long' if i else 'yoke');y.apply_translation([0,0,-2.45]);y.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]));y.apply_transform(trimesh.transformations.rotation_matrix(0,[0,0,1]));y.apply_translation([x,0,29-drop]);check(f'cap-yoke{i}-drop{drop}',cap,y)
def fromsolid(s):
 a=s.to_mesh();return trimesh.Trimesh(a.vert_properties,a.tri_verts,process=False)
# Conservative rectangular envelope of Ø1 round belt; nominal effective radii.
for motor_y in [-35,-39]:
 body=fromsolid(md.Manifold.cube([42.3,42.3,40]).translate([-18.61,motor_y-21.15,-33]));check(f'motorbody-y{motor_y}-bank',body,bank)
 boss=fromsolid(md.Manifold.cylinder(2,11,11,64).translate([2.54,motor_y,7]));check(f'motorboss-y{motor_y}-bank',boss,bank)
 shaft=fromsolid(md.Manifold.cylinder(20,2.5,2.5,64).translate([2.54,motor_y,7]));check(f'motorshaft-y{motor_y}-bank',shaft,bank)
 circles=[md.CrossSection.circle(2.8,128),md.CrossSection.circle(2.8,128).translate([5.08,0]),md.CrossSection.circle(5.8,128).translate([2.54,motor_y])]
 hull=md.CrossSection.batch_hull(circles);belt=fromsolid((hull.offset(.5)-hull.offset(-.5)).extrude(1).translate([0,0,15.5]));check(f'belt-envelope-y{motor_y}-bank',belt,bank)
 if (P/'components/cap.stl').exists():check(f'belt-envelope-y{motor_y}-cap',belt,pose('cap',(0,0,18.2)))
 for i,(jx,jy) in enumerate([(0,18),(5.08,25)]):
  for head_z in [-10,-5,0,3,6]:
   insertion_head=fromsolid(md.Manifold.cylinder(3,2.75,2.75,64).translate([jx,jy,head_z]));check(f'jackhead{i}-insertion-z{head_z}-bank-motory{motor_y}',insertion_head,bank);check(f'jackhead{i}-insertion-z{head_z}-motorbody-y{motor_y}',insertion_head,body)
  head=fromsolid(md.Manifold.cylinder(3,2.75,2.75,64).translate([jx,jy,6]));check(f'jackhead{i}-motorbody-y{motor_y}',head,body);check(f'jackhead{i}-bank-y{motor_y}',head,bank)
  jack=fromsolid(md.Manifold.cylinder(21,1.5,1.5,64).translate([jx,jy,9]));check(f'belt-envelope-y{motor_y}-jackshaft{i}',belt,jack)
  for drop in [0,2.4,2.7]:
   hardware=fromsolid(md.Manifold.cylinder(4,3.5,3.5,64).translate([jx,jy,17-drop]));check(f'belt-envelope-y{motor_y}-jackhardware{i}-drop{drop}',belt,hardware)


def yoke_mesh(i,drop,row=0):
 m=load('yoke-long' if i else 'yoke');m.apply_translation([0,0,-2.45]);m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]));m.apply_translation([i*5.08,row,29-drop]);return m
for i,(jx,jy) in enumerate([(0,18),(5.08,25)]):
 for drop in [0,2.4,2.7]:
  hardware=md.Manifold.cylinder(25,1.5,1.5,64).translate([jx,jy,9-drop])
  hardware+=md.Manifold.cylinder(3,2.75,2.75,64).translate([jx,jy,6-drop])
  hardware+=md.Manifold.cylinder(2.9,3.5,3.5,64).translate([jx,jy,17-drop])
  hardware+=md.Manifold.cylinder(4.4,2.5,2.5,64).translate([jx,jy,19.9-drop])
  hardware+=md.Manifold.cylinder(.5,3.5,3.5,64).translate([jx,jy,27.3-drop])
  hardware+=md.Manifold.cylinder(2.4,3.175,3.175,6).translate([jx,jy,27.8-drop])
  hardware+=md.Manifold.cylinder(2.4,3.175,3.175,6).translate([jx,jy,30.2-drop])
  hm=fromsolid(hardware)
  check(f'jackhardware{i}-fullstack-drop{drop}-bank',hm,bank)
  for otherdrop in [0,2.4,2.7]:
   check(f'jackhardware{i}-drop{drop}-otheryoke-drop{otherdrop}',hm,yoke_mesh(1-i,otherdrop))
   check(f'crossyokes-{i}-drop{drop}-otherdrop{otherdrop}',yoke_mesh(i,drop),yoke_mesh(1-i,otherdrop))
  for row in [0,5.08]:
   h=hm.copy();h.apply_translation([0,row,0])
   for n,z in [('lower0',31.35),('lower1',31.35),('lower2',31.35),('upper',35.05)]:check(f'jackhardware{i}-drop{drop}-bankrow{row}-{n}',h,pose(n,(0,0,z)))
   for j in range(2):
    for k in range(2):check(f'jackhardware{i}-drop{drop}-bankrow{row}-screw{j}{k}',h,pose('screw',(j*5.08,k*5.08,29)))
   for ey in [-70,35]:check(f'jackhardware{i}-drop{drop}-bankrow{row}-endblock{ey}',h,pose('endblock',(-36,ey,0)))
   for cx in [-42,47]:
    for cy in [-5,10.08]:check(f'jackhardware{i}-drop{drop}-bankrow{row}-foot{cx},{cy}',h,pose('foot',(cx-6,cy-6,0)))

# Shared exact thread pair: finer full-travel sweep, all four cells have identical profile.
for travel in np.arange(0,8.001,.25):
 pin=pose('pin',(0,0,40.2+float(travel)))
 check(f'fulltravel-thread-{travel:.2f}',pin,pose('screw',(0,0,29),-120*float(travel)))
# Exact inherited working thread comparison, excluding only its terminal chamfer.
a=solid(load('screw'));old=trimesh.load(P.parent/'2026-10-25-minimal-friction-screw-frame/components/A-screw.stl',force='mesh');old.apply_translation([0,0,4.6]);b=solid(old)
mask=md.Manifold.cube([4,4,25.9]).translate([-2,-2,8.25]);delta=abs(((a^mask)-(b^mask)).volume())+abs(((b^mask)-(a^mask)).volume())
assert delta<1e-4,delta

# Stop engagement is expected overlap after 0.01 mm attempted overtravel.
# This proves finite nominal keeper geometry, not physical stiffness/load rating.
contact_checks=[]
for j in range(2):
 for k in range(2):
  down=pose('screw',(j*5.08,k*5.08,28.94));up=pose('screw',(j*5.08,k*5.08,29.06))
  vd=sum(common(down,pose(n,(0,0,31.35))) for n in ['lower0','lower1','lower2'])
  vu=common(up,pose('upper',(0,0,35.05)))
  contact_checks.append(dict(cell=[j,k],downward_lower_stop_intersection_mm3=vd,upward_keeper_intersection_mm3=vu,pass_nominal=vd>.01 and vu>.01))
assert all(r['pass_nominal'] for r in contact_checks),contact_checks
oldfemale=solid(trimesh.load(P.parent/'2026-10-25-minimal-friction-screw-frame/components/C-pin-50-upright.stl',force='mesh'))
fmask=md.Manifold.cube([4.4,4.4,40]).translate([-2.2,-2.2,0]);newfemale=solid(load('pin'))^fmask;oldfemale=oldfemale^fmask
female_delta=abs((newfemale-oldfemale).volume())+abs((oldfemale-newfemale).volume());assert female_delta<1e-4,female_delta

# Removable motorplate prints flat and is fixed with four M3x8 screws.
mp=pose('motorplate',(0,0,9));check('motorplate-bank',mp,bank)
for my in [-35,-39]:
 motor=md.Manifold.cube([42.3,42.3,40]).translate([2.54-21.15,my-21.15,-33])
 boss=md.Manifold.cylinder(2,11,11,96).translate([2.54,my,7])
 shaft=md.Manifold.cylinder(20,2.5,2.5,96).translate([2.54,my,7])
 for label,ss in [('body',motor),('boss',boss),('shaft',shaft)]:
  mm=ss.to_mesh();check(f'motorplate-{label}-motorY{my}',mp,trimesh.Trimesh(mm.vert_properties,mm.tri_verts,process=False))
for my in [-35,-39]:
 pulley=pose('motorpulley',(2.54,my,10))
 boss=fromsolid(md.Manifold.cylinder(2,11,11,96).translate([2.54,my,7]))
 check(f'motorpulley-boss-with-2mm-shim-y{my}',pulley,boss)
report=dict(contact_checks=contact_checks,female_profile_symmetric_difference_mm3=female_delta,hardware_envelopes=dict(jack_centers_xy=[[0,18],[5.08,25]],lower_adjust_nut_bottom_on_z=17,lower_adjust_nut_and_washer_height=2.9,spring_working_length_mm=4.4,spring_od_mm=5,upper_washer_z_on=[27.3,27.8],upper_two_nuts_z_on=[27.8,32.6],jack_shaft_z_on=[9,34],motor_y_positions=[-35,-39],motor_face_z=7,motor_spacer_height_mm=2,belt_diameter_mm=1,belt_center_z=16),thread_working_symmetric_difference_mm3=delta,layout_checks=layout_report,scope='Nominal unstrained mesh poses; physical fits, deformation, belt traction, tolerances, unmodeled fasteners and loads unqualified.',checks=R,failed=[r for r in R if not r['pass_nominal']])
(P/'metadata/geometry-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(checks=len(R),failures=report['failed']),indent=2))
if report['failed'] or any(not x['on_bed'] or not x['inside_bed'] for x in layout_report):
 raise SystemExit('Geometry review contains failures; inspect metadata/geometry-review.json')
