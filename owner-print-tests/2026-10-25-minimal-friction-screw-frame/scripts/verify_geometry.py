#!/usr/bin/env python3
"""Nominal meshes, force-path contact probes, thread fidelity and full travel sweep."""
from pathlib import Path
import json,math,hashlib
import numpy as np,trimesh,manifold3d as md
P=Path(__file__).resolve().parents[1];C=P/'components';V3=P.parent/'2026-10-19-microstepper-frame-v3'
def s(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def load(n):return s(trimesh.load(C/(n+'.stl'),force='mesh'))
def box(d,v):return md.Manifold.cube(d).translate(v)
def cyl(d,h,z):return md.Manifold.cylinder(h,d/2,d/2,192).translate([0,0,z])
def vol(a,b):return abs((a^b).volume())
f=load('A-front').translate([0,0,-6.5]).rotate([90,0,0]);b=load('A-back').translate([0,0,-6.5]).rotate([90,0,0]).rotate([0,0,180]);frame=f+b
assert vol(f,b)<1e-4,('halves',vol(f,b))
r=load('A-screw').translate([0,0,12.9]);p=load('C-pin-50-upright');washer=(cyl(7,.5,12.4)-cyl(3.2,.5,12.4))
rows=[]
for lift in [0,.3]:
 for travel in np.arange(0,15.001,.25):
  rr=r.rotate([0,0,-120*float(travel)]).translate([0,0,lift]);pp=p.translate([0,0,19.5+float(travel)+lift])
  row=dict(travel_mm=float(travel),lift_mm=lift,pin_frame_mm3=vol(pp,frame),screw_frame_mm3=vol(rr,frame),screw_pin_mm3=vol(rr,pp),thread_overlap_mm=max(0,min(43.5+lift,25.5+travel+lift)-max(16.5+lift,19.5+travel+lift)),guides_overlap_mm=[max(0,min(z+2,69.5+travel+lift)-max(z,19.5+travel+lift)) for z in [36,56]])
  assert max(row[k] for k in row if k.endswith('mm3'))<1e-4,row
  assert abs(row['thread_overlap_mm']-6)<1e-8 and row['guides_overlap_mm']==[2,2],row
  rows.append(row)
# A 40-mm pin is a top-cropped same-profile reference, not a new thread.
p40=p^box([4.4,4.4,40],[-2.2,-2.2,0]);short_checks=[]
for travel in [0,15]:
 for lift in [0,.3]:
  pp=p40.translate([0,0,19.5+travel+lift]);rr=r.rotate([0,0,-120*travel]).translate([0,0,lift]);vals=dict(travel_mm=travel,lift_mm=lift,pin_frame_mm3=vol(pp,frame),pin_screw_mm3=vol(pp,rr),upper_guide_overlap_mm=min(58,59.5+travel+lift)-max(56,19.5+travel+lift));assert max(vals['pin_frame_mm3'],vals['pin_screw_mm3'])<1e-4 and vals['upper_guide_overlap_mm']==2;short_checks.append(vals)
# Continuous envelope clearance against the stationary frame (phase-independent).
pin_envelope=box([4.4,4.4,65.3],[-2.2,-2.2,19.5]);assert vol(pin_envelope,frame)<1e-4
rotor_envelope=cyl(7,1.5,12.9)+cyl(4,3.9,12.9)+cyl(3.2,27.3,16.5);assert vol(rotor_envelope,frame)<1e-4
motor={
 'body8':cyl(8,9.2,2),'body8_2':cyl(8.2,9.2,2),'boss':cyl(3,.25,11.2),'shaft_L':cyl(.8,3.35,11.2),
 'gear_L_envelope':cyl(2.2,1.25,13.2),'tab_allowance':cyl(10.2,1.2,10),'pcb':box([3.5,7,4],[-6,-3.5,4]),
 'glue_allowance':box([3.5,7.8,2],[-6,-3.9,2]),'wire_allowance':box([2.6,8,67],[-7,-4,8])}
mc={}
for n,m in motor.items():
 mc[n]=dict(frame_mm3=vol(m,frame),rotor_mm3=vol(m,r),washer_mm3=vol(m,washer))
 assert mc[n]['frame_mm3']<1e-4 and mc[n]['washer_mm3']<1e-4,(n,mc[n])
 if n!='gear_L_envelope':assert mc[n]['rotor_mm3']<1e-4,(n,mc[n])
contacts=dict(washer_frame_mm3=vol(washer,frame),washer_rotor_mm3=vol(washer,r),washer_down_001_mm3=vol(washer.translate([0,0,-.001]),frame),rotor_down_001_mm3=vol(r.translate([0,0,-.001]),washer),upper_stop_at_030_mm3=vol(r.translate([0,0,.3]),frame),upper_stop_at_031_mm3=vol(r.translate([0,0,.31]),frame))
assert contacts['washer_frame_mm3']<1e-4 and contacts['washer_rotor_mm3']<1e-4 and contacts['upper_stop_at_030_mm3']<1e-4
assert all(contacts[k]>0 for k in ['washer_down_001_mm3','rotor_down_001_mm3','upper_stop_at_031_mm3'])
old=s(trimesh.load(V3/'components/rotor-long.stl',force='mesh')).translate([0,0,4.5]) # old local thread starts12 -> global16.5
clip=box([4,4,26.34],[-2,-2,16.55]);a=old^clip;c=r^clip
diff=abs((a-c).volume())+abs((c-a).volume());assert diff<1e-4,diff
# C-profile cross sections compared after shortening (radial shape EXACT, roof moved).
ca=load('A-screw').slice(1);cb=s(trimesh.load(V3/'components/rotor.stl',force='mesh')).slice(1)
mask=md.CrossSection.circle(1.5,96);c_diff=((ca^mask)-(cb^mask)).area()+((cb^mask)-(ca^mask)).area();assert abs(c_diff)<1e-5,c_diff
# Quantify where intentionally loose rotor land catches; it is not a rated shaft protector.
radial=[dict(dx_mm=dx,frame_overlap_mm3=vol(r.translate([dx,0,0]),frame)) for dx in [0,.1,.19,.2,.21,.3]]
# Misalignment envelope at the low pin thread: first interference is NOT a safe load rating.
misalignment=[]
for t in [0,15]:
 pp=p.translate([0,0,19.5+t]);rr=r.rotate([0,0,-120*t])
 for dx in [0,.05,.1,.15,.2]:misalignment.append(dict(travel_mm=t,parallel_pin_offset_mm=dx,screw_pin_overlap_mm3=vol(pp.translate([dx,0,0]),rr),pin_frame_overlap_mm3=vol(pp.translate([dx,0,0]),frame)))
# Neighbour geometry: actual square polygons, plus boundary cases, not circle surrogates.
from shapely.geometry import box as square
from shapely.affinity import rotate,translate
pin=square(-2.2,-2.2,2.2,2.2);near=[translate(pin,xoff=5.08*i,yoff=5.08*j) for i,j in [(1,0),(-1,0),(0,1),(0,-1)]]
ang=45-math.degrees(math.acos((2*5.08-4.4)/(4.4*math.sqrt(2))))
assert sum(rotate(pin,ang-.01,origin=(0,0)).intersection(n).area for n in near)<1e-8
assert sum(rotate(pin,ang+.01,origin=(0,0)).intersection(n).area for n in near)>0
neighbor=dict(pin_width_mm=4.4,pitch_mm=5.08,gap_mm=.68,fixed_centered_neighbors_first_contact_deg=ang,one_sided_lead_equivalent_mm=ang/360*3,reversal_lead_equivalent_mm=ang/180*3,collective_centered_rotation_first_contact_deg=math.degrees(math.acos(4.4/5.08)),body_overlap_at_15mm_height_difference_mm=15,zero_overlap_at_height_difference_mm=30,stem_side_play_mm=[.6,.3],boundary_clearance_per_side_mm=.22,limitations='Stem plate maintains pitch approximately but does not lock rotation or vertical motion. This is a bounded geometry/friction fixture, not an unsupported production array.')
# Fixture assembly: upright and staggered, liner present/absent, both boundary states.
stand=load('B-stand').rotate([180,0,0]).translate([0,0,22]);boundary=load('B-boundary').rotate([180,0,0]).translate([0,0,34]);fixture_checks=[]
for liner_on in [False,True]:
 fixed=stand+(load('B-liner').translate([0,0,22]) if liner_on else md.Manifold());datum=2.25+(1.2 if liner_on else 0)
 for stagger in [False,True]:
  pins=[]
  for i in [-1,0,1]:
   for j in [-1,0,1]:
    raised=15 if stagger and (i+j)%2 else 0
    pin=load('B-pin').translate([5.08*i,5.08*j,datum+raised]);pins.append(pin)
    assert vol(pin,fixed)<1e-4,(i,j,liner_on,stagger,'deck')
    assert vol(pin,boundary)<1e-4,(i,j,liner_on,stagger,'boundary')
  mx=max(vol(a,b) for k,a in enumerate(pins) for b in pins[k+1:]);assert mx<1e-4
  fixture_checks.append(dict(liner=liner_on,stagger=stagger,maximum_pin_pair_overlap_mm3=mx,center_hole_diameter_mm=4.8,low_body_bottom_mm=25+datum))
# New manufacturing meshes remain closed bodies and plate objects don't intersect.
layouts=json.loads((P/'metadata/layout.json').read_text());plate_checks={}
for name,ls in layouts.items():
 bodies=[load(q['source']).translate([*q['center_xy'],0]) for q in ls];mx=0
 for i,a in enumerate(bodies):
  for b in bodies[i+1:]:mx=max(mx,vol(a,b))
 assert mx<1e-4,(name,mx)
 plate_checks[name]=dict(objects=len(bodies),max_overlap_mm3=mx)
report=dict(status='NOMINAL_GEOMETRY_PASS_PHYSICAL_TEST_NOT_PERFORMED',sampled_motion_states=rows,pin40_endpoint_checks=short_checks,fixture_checks=fixture_checks,continuous_pin_frame_envelope_mm3=vol(pin_envelope,frame),continuous_rotor_frame_envelope_mm3=vol(rotor_envelope,frame),motor=mc,contacts=contacts,thread_symmetric_difference_mm3=diff,C_profile_symmetric_difference_mm2=c_diff,radial_land_probes=radial,misalignment_sensitivity=misalignment,neighbors=neighbor,plate_checks=plate_checks,shaft_warning='Zero nominal interference does not establish zero shaft bending or axial friction through the C fit. Guides react tip force; flange contacts react thrust/moment; motor may share residual radial load. No motor radial-load rating exists. Unloaded manual acceptance is required before any powered cycling.',limits=dict(travel_mm=[0,15],rotor_float_mm=.3,pin_length_range_mm=[40,50],minimum_thread_end_margin_mm=3,minimum_lower_guide_overlap_mm=2,motor_variant='L',K_min_gear_overlap_mm=.5,L_min_gear_overlap_mm=1))
(P/'metadata/geometry-review.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'motion states;',neighbor)
