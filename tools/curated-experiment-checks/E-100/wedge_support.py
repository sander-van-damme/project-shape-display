"""Necessary distributed-support transmission bounds: mm, N, MPa.
Exploratory elastic/friction ranges; no manufacturing priors or contact pass.
A translated ramp track beneath guided rail feet supplies moving ground support.
Uniform base cross-section and rigid feet/bed are favorable boundary grants.
"""
from math import pi, tan, radians, isclose
from itertools import product
import json

PITCH=5.08
STROKE=2.5
ENDPOINT=(1.5*pi/4+1)/2  # E-061: d=1, p=1.5 MPa, spring+drag=1 N


def ramp_factor(angle,mu):
    slope=tan(radians(angle))
    # Upper inclined dry contact: (slope+mu)/(1-mu*slope).
    # Flat lower sliding bed adds mu times the vertical load.
    assert 1-mu*slope>0
    return (slope+mu)/(1-mu*slope)+mu


def case(angle,mu,E,width,depth,segments=1,selected=True):
    n=80//segments;L=n*PITCH;slope=tan(radians(angle))
    p=.1+(ENDPOINT if selected else 0.)  # preload persists in half-select
    # Eight cells between feet; endpoint feet receive half-span load.
    # This is exact statics for isolated simply supported spans, not contact
    # load sharing of a continuous rail on imperfect unilateral supports.
    assert n%8==0
    positions=[i*8*PITCH for i in range(n//8+1)]
    reactions=[8*p*(.5 if i in (0,len(positions)-1) else 1.) for i in range(len(positions))]
    factor=ramp_factor(angle,mu)
    forces=[factor*r for r in reactions]
    force=sum(forces)
    # Integrate axial force from each downstream shoe to the drive at x=0.
    shortening=sum(f*x for f,x in zip(forces,positions))/(E*width*depth)
    dz=shortening*slope
    return dict(angle_deg=angle,mu=mu,E_MPa=E,base_width_mm=width,base_depth_mm=depth,
        segments_per_line=segments,stroke_mm=STROKE/slope,force_per_drive_N=force,
        vertical_load_per_drive_N=sum(reactions),axial_shortening_mm=shortening,
        lost_lift_mm=dz,section_area_for_point1_mm2=force*L*slope/(2*E*.1),
        work_ratio=force*(STROKE/slope)/(sum(reactions)*STROKE),
        input_drive_count=160*segments,support_contacts=160*segments*(n//8+1),
        favorable_transmission_bound=dz<=.1,accepted_machine=False)


def checks():
    # Work conservation of the lossless wedge and positive frictional work.
    for angle in (15,30,45):
        z=case(angle,0,1500,2,8)
        assert isclose(z['work_ratio'],1.)
        assert case(angle,.1,1500,2,8)['work_ratio']>1
    x=case(30,.1,1500,2,8)
    assert isclose(x['vertical_load_per_drive_N'],80*(.1+ENDPOINT))
    # Independent uniform-load integral F_total*L/(2EA), stiffness and
    # segmentation limiting cases. Both ends are separate drives/segments.
    assert isclose(x['axial_shortening_mm'],x['force_per_drive_N']*80*PITCH/(2*1500*16))
    assert isclose(case(30,.1,3000,2,8)['lost_lift_mm'],x['lost_lift_mm']/2)
    assert isclose(case(30,.1,1500,2,8,2)['lost_lift_mm'],x['lost_lift_mm']/4)
    assert case(30,.1,1500,2,8,selected=False)['lost_lift_mm']<x['lost_lift_mm']
    return dict(virtual_work=True,axial_integral=True,stiffness_scaling=True,
                segmentation_scaling=True,self_review_only=True)


def main():
    scenarios=[case(*v) for v in product((15,30,45),(0.,.1,.3,.5),(500,1500,3000),(2,4),(4,8,12),(1,2))]
    # No counts interpreted as manufacturing probability or diversity score.
    print(json.dumps(dict(checks=checks(),cases=len(scenarios),
        favorable_bound_count=sum(x['favorable_transmission_bound'] for x in scenarios),
        witnesses=[case(a,m,1500,2,8,s) for a,m,s in product((15,30,45),(.1,.3),(1,2))],
        reference_half_select=case(30,.1,1500,2,8,selected=False),
        scenarios=scenarios),indent=2))

if __name__=='__main__':main()
