#!/usr/bin/env python3
"""Finite implicit solids, mm. Barrel minus swept-sphere groove; sphere/neck
follower, annular thrust, slotted dock collar and separate neighbor. Sampled
surface containment plus analytic neck/load bounds; NOT CAD/FEA qualification.
"""
import itertools
import json
import math

TAU=2*math.pi


def golden(f,a,b):
    r=(math.sqrt(5)-1)/2
    c=b-r*(b-a);d=a+r*(b-a);fc=f(c);fd=f(d)
    for _ in range(45):
        if fc<fd:b,d,fd=d,c,fc;c=b-r*(b-a);fc=f(c)
        else:a,c,fc=c,d,fd;d=a+r*(b-a);fd=f(d)
    x=(a+b)/2
    return x,f(x)


def probe(samples=128,lead=4.,amp=.3,radius=1.5,cutter=.4,ball=.3,neck=.4):
    clearance=cutter-ball;outer=radius+.25;inner_sleeve=2.
    peak=math.acos(-lead/(TAU*4*amp))/4;valley=TAU/4-peak
    def h(t):return 4+lead/TAU*(t-valley)+amp*(math.sin(4*t)-math.sin(4*valley))
    def curve(t,q):return (radius*math.cos(t-q),radius*math.sin(t-q),h(t))
    def distance(p,q):
        # Adjacent turns differ >=3.9 mm versus .4-mm radius; only the local
        # segment can be nearest for the sampled follower/cutter witnesses.
        f=lambda t:sum((a-b)**2 for a,b in zip(p,curve(t,q)))
        return math.sqrt(golden(f,max(q-.7,valley-TAU/4),min(q+.7,valley+45*TAU/4))[1])
    def lower(q):
        delta=2*math.asin(clearance/(2*radius))
        f=lambda t:h(t)-math.sqrt(max(0.,clearance**2-2*radius**2*(1-math.cos(t-q))))
        return golden(f,q-delta,q+delta)[1]
    worst_ball=-1e9;worst_neck=-1e9;max_offset=0.;min_rho=1e9
    contact_error=0.;min_z=1e9;max_z=-1e9
    for i in range(samples+1):
        q=valley+i*TAU/4/samples
        z=lower(q);max_offset=max(max_offset,h(q)-z)
        center=(radius,0.,z)
        contact_error=max(contact_error,abs(distance(center,q)-clearance))
        hp=lead/TAU+4*amp*math.cos(4*q);hpp=-16*amp*math.sin(4*q)
        rho=(radius**2+hp**2)**1.5/(radius*math.sqrt(radius**2+hp**2+hpp**2))
        min_rho=min(min_rho,rho)
        for latitude in range(1,8):
            beta=math.pi*latitude/8
            for longitude in range(16):
                alpha=TAU*longitude/16
                p=(radius+ball*math.sin(beta)*math.cos(alpha),
                   ball*math.sin(beta)*math.sin(alpha),z+ball*math.cos(beta))
                worst_ball=max(worst_ball,distance(p,q)-cutter)
        # Neck extends radially from sphere centre into sleeve wall; portions
        # outside the rotor are free. Sample actual cylindrical side surface.
        for ix in range(9):
            x=radius+(inner_sleeve-radius)*ix/8
            for it in range(32):
                angle=TAU*it/32
                p=(x,neck/2*math.cos(angle),z+neck/2*math.sin(angle))
                if math.hypot(p[0],p[1])<=outer:
                    worst_neck=max(worst_neck,distance(p,q)-cutter)
        min_z=min(min_z,z);max_z=max(max_z,z+44*lead/4)
    assert min_z-ball>0 and max_z+ball<52  # finite barrel end walls
    # Thrust flange R=2.1, rotating barrel R=outer; grounded annulus starts
    # at R=1.8. Dock neck R=.6, shoulder R=.8, jaws at |x|>=.65.
    assert outer<1.8 and 2.1<5.08/2
    assert .6<.65<.8
    dock_states=[]
    for jaw_inner in (.65,.9):
        for head_z in (0.,-.1,-.2,-1.):
            # Rotor lower collar occupies z=[-4,-3.6], radius .8.
            # Jaws occupy z=[-3.5,-3.3]+head_z on both sides of the neck.
            axial_overlap=max(0.,min(-3.6,-3.3+head_z)-max(-4.,-3.5+head_z))
            radial_overlap=max(0.,.8-jaw_inner)
            dock_states.append(dict(jaw_inner_mm=jaw_inner,head_z_mm=head_z,
                collar_collision=axial_overlap>1e-12 and radial_overlap>0,
                collar_touch=abs(-3.5+head_z+3.6)<1e-12 and radial_overlap>0))
    assert dock_states[1]['collar_touch'] and dock_states[2]['collar_collision']
    # Opening the jaws permits withdrawal; closed jaws reach the collar at .1 mm.
    assert all(not s['collar_collision'] and not s['collar_touch'] for s in dock_states[4:])
    neighbor_gap=5.08-5.0  # fixed guide outer width; tops are 4.8 mm
    assert neighbor_gap>0 and 5.08-4.8>0
    # Exact cantilever bound at sleeve inner face, load at sphere centre.
    stresses={str(f):32*f*(inner_sleeve-radius)/(math.pi*neck**3)
              for f in (.02,1.,10.)}
    return dict(samples=samples,lead_mm=lead,amp_mm=amp,
        minimum_centerline_curvature_radius_mm=min_rho,
        cutter_radius_mm=cutter,ball_surface_max_intrusion_mm=worst_ball,
        neck_surface_max_intrusion_mm=worst_neck,
        center_contact_error_mm=contact_error,max_loaded_path_offset_mm=max_offset,
        follower_center_z_bounds_44_steps_mm=[min_z,max_z],
        required_44step_travel_mm=44*lead/4,
        neighbor_guide_gap_mm=neighbor_gap,neighbor_top_gap_mm=5.08-4.8,
        thrust_area_mm2=math.pi*(2.1**2-1.8**2),
        closed_dock_radial_overlap_mm=.8-.65,
        closed_dock_neck_clearance_mm=.65-.6,dock_transition_samples=dock_states,
        neck_bending_stress_MPa=stresses,
        neck_force_capacity_N_at_20_60MPa=[s*math.pi*neck**3/(32*(inner_sleeve-radius)) for s in (20,60)])


if __name__=='__main__':
    result=[probe(n) for n in (32,64,128)]
    result += [probe(64,l,a) for l,a in itertools.product((3.9,4.1),(.25,.35))]
    print(json.dumps(result,indent=2))
