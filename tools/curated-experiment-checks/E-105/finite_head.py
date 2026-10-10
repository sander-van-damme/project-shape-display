#!/usr/bin/env python3
"""E-105 finite allocated solids + conditional orifice/control screen.
mm/N/s/MPa externally; SI inside the orifice. No qualified parts or priors.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('e104', Path(__file__).parents[1]/'E-104/valve_head_screen.py')
e104 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = e104
spec.loader.exec_module(e104)
P = 5.08


def box(name, x, y, z, dx, dy, dz):
    return dict(name=name, lo=(x-dx/2,y-dy/2,z-dz/2), hi=(x+dx/2,y+dy/2,z+dz/2))


def overlap(a,b):
    return all(min(a['hi'][k],b['hi'][k])-max(a['lo'][k],b['lo'][k]) > 1e-9 for k in range(3))


def lever_vertices(x, lane, angle, thickness=3.):
    # Rectangular prism rotating about x; root at y=-4,z=-9.5.
    return [(x+sx*.6, -4+u*math.cos(angle)-v*math.sin(angle),
             -9.5+u*math.sin(angle)+v*math.cos(angle))
            for sx,u,v in itertools.product((-1,1),(0,lane+5),(-thickness/2,thickness/2))]


def bounds(name,vertices):
    return dict(name=name,lo=tuple(min(p[k] for p in vertices) for k in range(3)),
                hi=tuple(max(p[k] for p in vertices) for k in range(3)))


def surface(y,angle,top=True):
    return -9.5+(y+4)*math.tan(angle)+(1 if top else -1)*1.5/math.cos(angle)


def angle_for_lift(lift):
    lo,hi=0.,.2
    for _ in range(50):
        mid=(lo+hi)/2
        if surface(0,mid)-surface(0,0)<lift: lo=mid
        else: hi=mid
    return hi


def geometry(lanes=3, samples=101):
    """Generated actuator boxes and rotating lever solids, nine-channel period.
    Clearance uses enclosing bounds: nonintersection is conservative; reported
    positive actuator overlaps are exact rectangular-solid witnesses.
    Own lever/rod contacts and omitted bearing/seal internals are not certified.
    """
    bodies=[box('actuator'+str(c),c*P,14*(c%lanes),-25,12,10,20) for c in range(9)]
    collisions=[(a['name'],b['name']) for i,a in enumerate(bodies) for b in bodies[i+1:] if overlap(a,b)]
    lever_hits=[]
    for i in range(samples):
        angle=angle_for_lift(.35*i/(samples-1))
        levers=[bounds('lever'+str(c),lever_vertices(c*P,14*(c%lanes),angle)) for c in range(9)]
        # Independent opening: all extrema covered by x separation and body z.
        for a in levers:
            for b in bodies:
                if overlap(a,b): lever_hits.append((a['name'],b['name'],i))
        for j,a in enumerate(levers):
            for b in levers[j+1:]:
                if overlap(a,b): lever_hits.append((a['name'],b['name'],i))
    angle=angle_for_lift(.35)
    # 1.2 diameter tip against .8 diameter stem. Full-face overlap bound.
    capture=(1.2-.8)/2
    # Closed stem bottom z=-2.5; acquired tip z=-2.5; bank withdraws 1 mm.
    # At any index y, tip top=-3.5 < all stems. +/- .1 each vertical bounds.
    index_gap=1.-2*.1
    return dict(lanes=lanes,body_collisions=collisions,lever_collisions=lever_hits,
                samples=samples,angle_deg=math.degrees(angle),capture_radius=capture,
                index_gap_bound=index_gap,
                actuator_strokes=[surface(14*j,angle,False)-surface(14*j,0,False) for j in range(lanes)])


def coaxial_overlap(a,b):
    """Exact positive-volume intersection of concentric annular cylinders."""
    return min(a['ro'],b['ro'])>max(a['ri'],b['ri'])+1e-10 and min(a['z1'],b['z1'])>max(a['z0'],b['z0'])+1e-10


def valve_states(samples=101, tail=2.5):
    # Flat poppet above seat; lower supply plenum, dry stem through gland.
    # Shell has one radial supply hole; omitted subtraction only overstates solid.
    fixed=[dict(name='seat',ri=.7,ro=1.4,z0=-.5,z1=0),
           dict(name='shell',ri=1.4,ro=2.2,z0=-1.8,z1=3),
           dict(name='gland',ri=.5,ro=1.4,z0=-1.8,z1=-1.3)]
    hits=[]
    for i in range(samples):
        lift=.35*i/(samples-1)
        moving=[dict(name='disk',ri=0,ro=1.1,z0=lift,z1=.4+lift),
                dict(name='stem',ri=0,ro=.4,z0=-tail+lift,z1=lift),
                dict(name='head_tip',ri=0,ro=.6,z0=-tail-.8+lift,z1=-tail+lift)]
        for a,b in itertools.product(moving,fixed):
            if coaxial_overlap(a,b):hits.append((a['name'],b['name'],lift))
    # Finite pressure seat, not just a port circle. Returns through same path.
    return dict(fixed_solids=fixed,collisions=hits,samples=samples,
                neighboring_shell_gap=P-4.4,stem_gland_radial_gap=.1,
                seat_contact_annulus=(.7,1.1),supply_port_diameter=.8,
                spring_space=dict(inner_radius=.5,outer_radius=1.3,z0=.75,z1=3.))


def port_area(port=1.4,stem=.8,lift=.35):
    # Flat annular seat curtain and through-annulus are SERIES restrictions.
    return math.pi*(port*port-stem*stem)/4, math.pi*port*max(0,lift), math.pi*.8**2/4


def flow_mm3s(areas, dp_mpa, cd=.6, rho=1000.):
    if dp_mpa <= 0 or min(areas)<=0: return 0.
    # Sum individual turbulent pressure losses, not min(area) shortcut.
    effective=1/math.sqrt(sum(1/a**2 for a in areas))
    return cd*effective*1e-6*math.sqrt(2*dp_mpa*1e6/rho)*1e9


def speed(bore,lift,dp,cd=.6,port=1.4,stem=.8):
    return flow_mm3s(port_area(port,stem,lift),dp,cd)/(math.pi*bore*bore/4)


def viscous_speed(bore,lift,dp,mu):
    # Competing discrepancy model: add fully developed radial parallel-plate
    # seat loss to inertial restrictions. mu is a SCENARIO in Pa s.
    if lift<=0 or dp<=0:return 0.
    areas=port_area(lift=lift)
    k=1000/2*sum(1/(.6*a*1e-6)**2 for a in areas)
    resistance=6*mu*math.log(1.1/.7)/(math.pi*(lift*1e-3)**3)
    q=2*dp*1e6/(resistance+math.sqrt(resistance**2+4*k*dp*1e6))
    return q*1e9/(math.pi*bore*bore/4)


def viscous_gap(mu):
    lo,hi=0.,.35
    for _ in range(60):
        mid=(lo+hi)/2
        if viscous_speed(2,mid,.1,mu)<75:lo=mid
        else:hi=mid
    return hi


def lift_for_speed(bore,v,dp,cd=.6):
    lo,hi=0.,.35
    if speed(bore,hi,dp,cd)<v: return None
    for _ in range(60):
        mid=(lo+hi)/2
        if speed(bore,mid,dp,cd)<v:lo=mid
        else:hi=mid
    return hi


def staged_envelope(bore=2.,lpm=8.,delay=.002,error=.2,reader=.05,fast=400.):
    """Uniform full-stroke split workload, simultaneous per-phase two-speed change.
    Delay bounds fast-to-slow response AND residual slow closure separately.
    A stopped transition is charged in addition to the conservative slow band.
    This is a specified controller, not a lower bound on all possible control.
    """
    sc=e104.Scenario(bore=bore,flow_lpm=lpm,speed=fast)
    slow=(error-reader)/delay
    band=fast*delay+reader
    assert 0<band<40 and 0<slow<=fast+1e-9
    a=sc.area(0)
    def phase(n):
        if not n:return 0.
        return max(n*a*(40-band)/sc.pump,(40-band)/fast)+delay+max(n*a*band/sc.pump,band/slow)
    retry=sc.acquire_withdraw+sc.row_read_settle+2*(sc.phase_overhead+phase(80))
    totals=[sc.global_setup+e104.route(range(80),0,sc)+80*(sc.acquire_withdraw+sc.row_read_settle+
            (int(n>0)+int(n<80))*sc.phase_overhead+phase(n)+phase(80-n))+retry for n in range(81)]
    return dict(bore=bore,lpm=lpm,delay_ms=delay*1000,slow=slow,band=band,
                worst=max(totals),up_count=totals.index(max(totals)))


def main():
    g=[geometry(k) for k in (1,2,3)]
    assert g[0]['body_collisions'] and g[1]['body_collisions']
    assert not g[2]['body_collisions'] and not g[2]['lever_collisions']
    # Refinement checks the same continuous separation witness.
    assert not geometry(3,201)['lever_collisions']
    assert all(abs(surface(0,angle_for_lift(h))-surface(0,0)-h)<1e-12 for h in (0,.1,.35))
    assert math.isclose(flow_mm3s((1,),.1)/flow_mm3s((1,1),.1),math.sqrt(2))
    assert math.isclose(flow_mm3s((1,2),.4)/flow_mm3s((1,2),.1),2.)
    assert speed(2,0,.1)==0 and speed(2,.35,0)==0
    assert math.isclose(speed(2,.35,.1)/speed(3,.35,.1),2.25)
    # Independently sum SI loss at predicted flow to recover applied pressure.
    areas=port_area(); q=flow_mm3s(areas,.1)*1e-9
    assert math.isclose(sum(1000/2*(q/(.6*a*1e-6))**2 for a in areas),100000.)
    # Opposing common seat bias and actuator zero error add, not RSS.
    nominal=lift_for_speed(2,75,.1)
    metering={str(e):dict(min_speed=speed(2,max(0,nominal-e),.1),max_speed=speed(2,nominal+e,.1)) for e in (.005,.01,.05)}
    lowering=[]
    for bore,net,cd,lift in itertools.product((2.,3.),(.02,.1,.3),(.4,.6,.8),(.15,.35)):
        a=math.pi*bore*bore/4
        dp=max(0,net/a-.01) # .01 MPa backpressure allocation
        lowering.append(dict(bore=bore,net_bias_minus_drag=net,cd=cd,lift=lift,dp=dp,speed=speed(bore,lift,dp,cd)))
    # Poppet pressure/preload necessary bound; not a seal/return design.
    seat=math.pi*1.4**2/4
    differential=.5
    preload=(seat-math.pi*.8**2/4)*differential
    opening=preload+seat*differential # supply at zero, chamber at high; no drag
    stiffness=[]
    for thickness in (1.4,3.):
        E=1500.;I=1.2*thickness**3/12;L=32.;a=4.
        compliance=a*a*(L-a)**2/(3*E*I*L)
        stiffness.append(dict(thickness=thickness,loss=opening*compliance))
    # Actual volume displaced into chamber by stem, not nominal exact memory.
    swept=math.pi*.8**2/4*.35
    assert math.isclose(viscous_speed(2,.1,.1,0),speed(2,.1,.1))
    assert viscous_speed(2,.01,.1,.01)<speed(2,.01,.1)
    valves=valve_states()
    short_tail=valve_states(tail=2.)
    assert short_tail['collisions'] and not valves['collisions']
    sc=e104.Scenario(bore=2,flow_lpm=8,speed=400)
    assert math.isclose(staged_envelope(delay=.000375)['worst'],
                        e104.uniform_envelope(sc)['worst']+162*.000375)
    valves['short_tail_witness']=short_tail['collisions'][-1]
    report=dict(valves=valves,checks='PASS: solids/sampling, surface contact, SI pressure reconstruction, scaling and limits',
                geometry=g,flow=dict(areas_mm2=areas,nominal_2mm_speed_at_100kpa=speed(2,.35,.1),
                slow_gap_for_75mm_s=nominal,metering_bounds=metering,lowering=lowering,
                viscous_gap_sensitivity={str(mu):viscous_gap(mu) for mu in (.001,.01,.1)}),
                control=[staged_envelope(b,q,d) for b,q,d in itertools.product((2.,3.),(8.,12.),(.001,.002,.003))],
                accuracy_sensitivity=[dict(error=e,**staged_envelope(delay=.002,error=e)) for e in (.2,.3,.5)],
                force=dict(preload_lower_bound=preload,opening_lower_bound=opening,lever_loss=stiffness),
                stem_displacement=dict(volume_mm3=swept,height_2mm=swept/(math.pi*2**2/4),height_3mm=swept/(math.pi*3**2/4)))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
