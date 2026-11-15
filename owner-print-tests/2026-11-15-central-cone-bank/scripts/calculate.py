#!/usr/bin/env python3
"""Screening assumptions only: exact selected dimensions, no measured material data."""
from pathlib import Path
import math,json
from shapely.geometry import Point
from shapely.ops import unary_union
P=Path(__file__).resolve().parents[1]
def mean_r(a,b):return 2/3*(b**3-a**3)/(b**2-a**2)
rcone=mean_r(1.1,1.9);rupper=mean_r(1.75,2.2);rlower=mean_r(1.15,2.2);rinput=mean_r(1.6,2.1)
rows=[]
for y in [-35,-37,-39]:
 hull=unary_union([Point(0,0).buffer(2.8,quad_segs=512),Point(5.08,0).buffer(2.8,quad_segs=512),Point(2.54,y).buffer(5.8,quad_segs=512)]).convex_hull
 rows.append(dict(motor_y_mm=y,belt_centerline_length_mm=hull.length,nominal_oring_id32_centerline_length_mm=33*math.pi,stretch_fraction=hull.length/(33*math.pi)-1))
(P/'metadata/belt-length.json').write_text(json.dumps(rows,indent=2)+'\n')
r=dict(scope='Calculated screening scenarios; no physical forces/friction measured',cone_half_angle_degrees=30,cone_contact_area_mm2=math.pi*(1.1+1.9)*(1.9-1.1)/math.sin(math.radians(30)),cone_effective_radius_pressure_mm=rcone,cone_effective_radius_wear_mm=1.5,upper_thrust_effective_radius_mm=rupper,lower_thrust_effective_radius_mm=rlower,input_collar_effective_radius_mm=rinput,scenarios=[])
for mu in [.15,.25,.3,.4]:
 k=3*mu-.2*rupper-.1
 r['scenarios'].append(dict(assumed_mu_cone=mu,assumed_mu_thrust=.2,assumed_lateral_drag_Nmm_per_N=.1,net_thread_torque_Nmm_per_N=k,force_for_historical_0343_Nmm_N=.343/k if k>0 else None,input_collar_drag_Nmm_per_N=.2*rinput))
(P/'metadata/force-screening.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
