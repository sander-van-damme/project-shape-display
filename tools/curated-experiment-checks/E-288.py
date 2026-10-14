#!/usr/bin/env python3
"""Shared underside probe: bounded geometry/force/schedule screen, not hardware.
All mm/N/s/MPa. Explicit scenarios; no calibrated process or sensor distributions.
Run: python3 tools/curated-experiment-checks/E-288.py
"""
from math import pi, sqrt, isclose, ceil
from itertools import product

# E-277 guides and intact 10-mm nut/136-mm body; E-286 support datum.
PITCH, WIDTH_MIN, OPEN_MAX, GUIDE_ERROR = 12.7, 10.2, 10.9, .1
GUIDE_SPAN, LOWER_GUIDE = 82., 54.
TIP_RADIUS, HEAD_ERROR, BORE_RADIUS = .5, .2, 1.75
OFFSET, PORT_RADIUS = 3.5, 1.


def center_bound(base):
    # Grant no yaw: even this relaxed 1D envelope does not certify all heights.
    return GUIDE_ERROR+(OPEN_MAX-WIDTH_MIN)/2 + (LOWER_GUIDE-base)*(OPEN_MAX-WIDTH_MIN+2*GUIDE_ERROR)/GUIDE_SPAN


def landing_interval(base):
    d=center_bound(base)
    # Full tip footprint on solid flat annulus, with independent head error.
    return BORE_RADIUS+d+TIP_RADIUS+HEAD_ERROR, WIDTH_MIN/2-d-TIP_RADIUS-HEAD_ERROR


def move_time(distance, v=50., a=500.):
    assert distance >= 0 and v>0 and a>0
    return 2*sqrt(distance/a) if distance <= v*v/a else distance/v+v/a


def trigger_z(rest, backlash, mass_g, trigger_force):
    # Quasi-static frictionless limiting case: if force exceeds deadweight,
    # unload gravity flank and move to opposite flank before trigger.
    return rest+(backlash if trigger_force>mass_g*.00981 else 0)


def run():
    for base in (2., 22., 32., 52.):
        lo,hi=landing_interval(base)
        print('base/center bound/allowable fixed offset',base,center_bound(base),lo,hi)
    lo,hi=landing_interval(2)
    assert lo>hi
    assert landing_interval(52)[0]<OFFSET<landing_interval(52)[1]
    # Independent explicit axis witnesses, not just interval arithmetic.
    # Positive body shift moves the port toward the bore; negative toward edge.
    d=center_bound(2)
    inward=OFFSET-d-HEAD_ERROR-TIP_RADIUS-BORE_RADIUS
    outward=WIDTH_MIN/2-(OFFSET+d+HEAD_ERROR+TIP_RADIUS)
    print('R3.5 minimum-base inner/outer margins',inward,outward)
    assert inward>0 and outward<0
    # Even changing the radius cannot meet both relaxed requirements here.
    mid=(lo+hi)/2
    assert mid-d-HEAD_ERROR-TIP_RADIUS < BORE_RADIUS
    assert mid+d+HEAD_ERROR+TIP_RADIUS > WIDTH_MIN/2
    print('incompatible offset interval width',hi-lo)
    # Nominal, centered construction is genuinely possible geometrically.
    assert BORE_RADIUS+TIP_RADIUS<OFFSET<10.3/2-TIP_RADIUS
    assert OFFSET-TIP_RADIUS>2.2 # driver/collar envelope
    assert OFFSET+PORT_RADIUS==4.5 # tangent port, not a closed keeper bore


def complete():
    # Audit port admission separately: a tangent port is not a closed bearing.
    nominal_edge=4.5-OFFSET-PORT_RADIUS
    print('keeper port nominal outer ligament',nominal_edge)
    assert nominal_edge==0
    # Port diameter -0.1mm; independent shaft placement and bow scenarios.
    for bow in (0.,.2):
        margin=.95-TIP_RADIUS-HEAD_ERROR-bow
        print('2mm port worst radius/placement/bow margin',bow,margin)
    # E-286 spine top/bottom plus keeper = three pierced layers per cell.
    # Actual lands, chamfers, local thrust flexibility and fastening unpaid.
    print('support central-hole ligament nominal',OFFSET-PORT_RADIUS-1.4)
    print('collar-to-port nominal radial separation',OFFSET-PORT_RADIUS-2.2)
    print('probe reach from below spine to highest underside',52-(-36))
    # Euler is an ideal rod-only diagnostic, not precision/load qualification.
    E,I,L=200000.,pi/64,88.
    for end_factor in (1.,2.):
        print('1mm assumed steel stylus Euler N',end_factor,pi*pi*E*I/(end_factor*L)**2)
    # No assumed stiffness distribution. Static tip compression before trigger.
    for k in (.1,1.,10.):
        print('contact compliance at .05N, stiffness N/mm, displacement',k,.05/k)
    for mass,force in product((1.,3.,5.,14.),(.02,.05)):
        print('mass g/trigger N/deadweight reserve N',mass,force,mass*.00981-force)
    assert trigger_z(30,0,3,.05)==trigger_z(29,1,3,.05)==30
    assert trigger_z(30,0,3,.02)!=trigger_z(29,1,3,.02)
    print('force-induced alias: rest30/lash0 and rest29/lash1 both trigger at30')
    # Broken/detached top creates a second observation ambiguity at any force:
    # identical nut location, distinct actual surface. Not a prevalence claim.
    states=[dict(nut=30,top=166),dict(nut=30,top=164)]
    assert states[0]['nut']==states[1]['nut'] and states[0]['top']!=states[1]['top']
    assert isclose(move_time(5),.2)
    # Shaft parked below Z-36 so head can traverse under the -34 spine.
    # Every active channel starts at same plane; unknown actual height => longest
    # reach. Four independently compliant/stopping probe channels is granted.
    for base in (2.,52.):
        stroke=base+36
        cycle=2*move_time(stroke)+.1+.2 # contact and post-release settle allocations
        print('base/full probe cycle s',base,cycle)
    cycle=2*move_time(88)+.3
    assert isclose(cycle,4.02)
    for side in (32,64,80):
        n=side**2
        # Pitches comparison only: unchanged coarse support does not fit fine.
        for channels in (1,4):
            print('N/channels/dense additional read s',n,channels,ceil(n/channels)*cycle)
        print('N/ports/10-30s finishing hours',n,3*n,[3*n*t/3600 for t in (10,30)])
    for groups in (1,4,8,16):
        print('changed four-cell groups/added read s',groups,groups*cycle)
    # Budget allocations, not supplier quotes; no board component selected.
    for channels in (1,4):
        low,high=channels*40+40,channels*120+120
        print('channels/shared added allocation USD/optimistic whole range',channels,low,high,798+low,798+high)
    print('No trustworthy actual-surface verification, speed, port manufacture or force pass.')


if __name__=='__main__':
    run()
    complete()
