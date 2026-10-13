#!/usr/bin/env python3
"""Shared rack + selectively docked screw tips. Conditional architecture screen.

No gear profile, force-qualified selector, rated RPM or actual-cap reader.
Rack is reset empty at each station; no sliding torque splines are assumed.
"""
import argparse
import itertools
import json
import math
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('direct', Path(__file__).resolve().parents[1]/'E-272/direct.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
h = d.h


def transaction(values, lead=3, diameter=4, rpm=850, switch=.08):
    """Positive threshold groups followed by negative, tips changed only at rest.

    Empty preposition max(B-A,0), active +A then -B, empty return max(A-B,0).
    Thus 0 <= rack <= max(A,B)*circumference/lead and distance=2*max(A,B)*ratio.
    All pinions rotate on empty rack moves, but every socket is disengaged.
    """
    a = max([0]+list(values)); b = max([0]+[-v for v in values])
    if a == b == 0:
        return dict(seconds=0., active_s=0., empty_s=0., switching_s=0.,
                    groups=0, travel_mm=0., read_retract_s=0.)
    circumference = math.pi*diameter
    ratio = circumference/lead
    speed = min(rpm, 200/circumference*60)
    accel = min(1000, 5000/circumference)
    groups = h.a.r.program(values)
    active = sum(h.a.r.spin(abs(step)/lead, speed, accel) for step,_ in groups)
    empty = h.a.r.move(max(b-a,0)*ratio)+h.a.r.move(max(a-b,0)*ratio)
    # Each threshold gets .08 insert/retire/proof; this is not measured latency.
    # Final .1 retract + .1 settle + .1 simultaneous actual-cap read.
    return dict(seconds=active+empty+switch*len(groups)+.30, active_s=active,
                empty_s=empty, switching_s=switch*len(groups), groups=len(groups),
                travel_mm=2*max(a,b)*ratio, read_retract_s=.30)


def schedule(delta, width, stroke, **kw):
    # Same adjacent interval cover and path cost as E-267; replace all dwell/retry.
    travel = h.schedule(delta,width)
    if not travel['stations']:
        return dict(seconds=0., stations=0, raised=0, lowered=0, unchanged=len(delta)**2)
    jobs = h.stations(delta,width)
    tx = [transaction([v for _,v in cells],**kw) for _,_,cells in jobs]
    retry = transaction([stroke],**kw)['seconds']
    terms = dict(common_s=5.,seek_s=travel['seek_s'],return_s=travel['return_s'],
                 active_s=sum(t['active_s'] for t in tx),
                 empty_s=sum(t['empty_s'] for t in tx),
                 switching_s=sum(t['switching_s'] for t in tx),
                 read_retract_s=sum(t['read_retract_s'] for t in tx),retry_s=retry)
    return dict(seconds=sum(terms.values()),**terms, stations=len(jobs),
                groups=sum(t['groups'] for t in tx),rack_travel_mm=sum(t['travel_mm'] for t in tx),
                raised=travel['raised_cells'],lowered=travel['lowered_cells'],
                unchanged=travel['unchanged_cells'],visited_rows=travel['visited_rows'],
                first_seek_s=travel['first_seek_s'])


def summarize(cases,width,stroke,**kw):
    rows={name:schedule(delta,width,stroke,**kw) for name,delta in cases.items() if any(map(any,delta))}
    worst=max(rows,key=lambda name:rows[name]['seconds'])
    return dict(max_s=rows[worst]['seconds'],worst=worst,ledger=rows[worst],
                nonempty=len(rows),within30=sum(v['seconds']<=30 for v in rows.values()))


def report(n,width,stroke,**kw):
    cases={name:delta for name,delta in h.a.workloads(n).items() if stroke==50 or 'deep:' not in name}
    targets,start=h.a.c.terrain(n,stroke-20,stroke-20)
    names=h.a.c.v.s.SUITES['relief']
    initial={name:h.a.r.delta(start,targets[name]) for name in names}
    prep=schedule(h.a.c.v.s.flat(n,stroke-20),width,stroke,**kw)['seconds']
    return dict(n=n,width=width,stroke=stroke,parameters=kw,
                local=summarize(h.local_cases(n,stroke),width,stroke,**kw),
                scene=summarize(cases,width,stroke,**kw),neutral_s=prep,
                minimum_rest_first_s=summarize({name:targets[name] for name in names},width,stroke,**kw)['max_s'],
                neutral_plus_first_s=prep+summarize(initial,width,stroke,**kw)['max_s'],
                dense_s=schedule(h.a.c.v.s.flat(n,stroke),width,stroke,**kw)['seconds'],
                mixed_dense_s=schedule([[stroke if (x+y)%2 else -stroke for x in range(n)] for y in range(n)],width,stroke,**kw)['seconds'])


def geometry(n,width=16,stroke=50,lead=3,e=.2,diameter=4,outer=5):
    pitch=406.4/n; span=(width-1)*pitch; excursion=stroke*math.pi*diameter/lead
    # Proposed shared rack face 6mm; moving pinion face 2mm +3mm docking.
    # Nominal gear profile unspecified: envelope clearance is only necessary.
    return dict(pinion_neighbor_gap_mm=pitch-outer-2*e,
                bearing_neighbor_gap_mm=pitch-4.4-2*e,
                axial_mesh_reserve_mm=6-2-3-2*e,
                rack_excursion_mm=excursion,rack_stock_mm=span+excursion+20,
                rack_swept_union_mm=span+2*excursion+20,
                whole_X_union_mm=406.4-pitch+2*excursion+20,
                selector_lanes=math.ceil((20+2*e+.05)/pitch),
                parked_gap_mm=1-2*e,insertion_mm=2-2*e)


def forces(width=16,torque=.35,mass=.5,diameter=4,inertia=1e-8):
    # Nmm, kg, mm, kg m²; bounded scenarios, NOT measured process/usage priors.
    radius=diameter/2000
    rack_accel=5.0
    reflected=width*inertia/radius**2
    tip=width*torque/(diameter/2)
    return dict(tip_force_N=tip,rack_inertial_N=mass*rack_accel,
                pinion_inertial_N=reflected*rack_accel,
                total_N=tip+(mass+reflected)*rack_accel,
                peak_mechanical_W=(tip+(mass+reflected)*rack_accel)*.2)


def phase_span(heights,lead=3,symmetry=6):
    """Smallest angular arc containing all socket phases modulo socket symmetry.

    Identical registered rigid heads are assumed; elastic phase accommodation
    is not granted. A common angle fits only if span <= twice angular allowance.
    """
    period=360/symmetry
    phases=sorted((360*z/lead)%period for z in heights)
    gaps=[b-a for a,b in zip(phases,phases[1:])]+[phases[0]+period-phases[-1]]
    return period-max(gaps)


def selection_envelope(n,width=16,e=.2):
    """Necessary cross-channel boxes; joints/supports not constructed internally.

    Narrow arms pass ABOVE every offset solenoid, unlike the failed E-271
    coax shafts through neighboring motors. Whole shaft/pinion carrier shifts
    axially; broad rack face remains meshed, with no sliding torque spline.
    """
    p=406.4/n;lanes=math.ceil((20+2*e+.05)/p);parts=[]
    for i in range(width):
        x=i*p;y=30+30*(i%lanes)
        parts += [d.r.box(i,'tip_carrier',x-2.2,x+2.2,-2.2,2.2,-40,2),
                  d.r.box(i,'arm',x-2.2,x+2.2,0,y+2.2,-38,-27),
                  d.r.box(i,'solenoid',x-10,x+10,y-12,y+12,-80,-44),
                  d.r.box(i,'plunger',x-1.5,x+1.5,y-1.5,y+1.5,-47,-30)]
    return dict(conflicts=len(d.r.conflicts(parts,e)),lanes=lanes,
                longest_arm_mm=30*lanes,depth_mm=90,head_Y_mm=30*lanes+30,
                min_cross_channel_gap_mm=min(d.r.gap(a,b)-2*e for a,b in itertools.combinations(parts,2) if a['channel']!=b['channel']))


def cost(n,width=16):
    # ALL allocations, not live quotes. Inherit comparison categories, remove
    # individual motors, belts, feedback, motor wiring; retain all selection.
    items=dict(docking_actuators=(width,4.46,8),shaft_tip_pinion_bushings=(width,5,14),
               carrier_guides_arm_return=(width,4,12),selector_electronics=(width,1,2),
               harness_connectors=(width,1,3),docking_switches=(width,2,4),
               common_rack_drive_encoder=(1,40,120),rack_guides_stops=(1,35,110),
               shared_precision_plates_jig=(1,100,250),distribution=(1,30,80),
               XY_guides_drives_limits=(1,120,240),chassis_service=(1,35,75),
               supply_protection_cooling=(1,80,150),controller=(1,35,70),
               resident_support=(n*n,.02,.08),cap_reader=(1,80,250),
               reader_mount=(1,80,180))
    pre=[sum(v[0]*v[j] for v in items.values()) for j in (1,2)]
    return dict(allocations=items,purchased_USD=[pre[0]*1.1+20,pre[1]*1.15+60],
                maker_hours=[8+n*n*8/3600+width/6+1,16+n*n*20/3600+width/2+3],
                print_material_USD=[60,160],selector_W=width*5.5,
                conductor_duties=6*width+6,termination_duties=12*width+12)


def checks():
    count=0
    # Independent exact replay, including empty travel with no selected socket.
    for row in itertools.product((-50,-20,0,10,30,50),repeat=4):
        a=max(0,*row);b=max(0,*(-v for v in row));position=max(b-a,0)
        actual=[0]*len(row); distance=position
        for step,mask in h.a.r.program(row):
            position+=step;distance+=abs(step)
            assert 0<=position<=max(a,b)
            actual=[v+step if m else v for v,m in zip(actual,mask)]
            assert all(min(0,want)<=v<=max(0,want) for want,v in zip(row,actual))
            assert all(v==0 for want,v in zip(row,actual) if want==0)
        distance+=position
        assert actual==list(row) and distance==2*max(a,b)
        for lead in (2,3):
            tx=transaction(row,lead=lead)
            assert math.isclose(tx['travel_mm'],distance*math.pi*4/lead)
            reverse=transaction([-v for v in row],lead=lead)
            assert math.isclose(tx['seconds'],reverse['seconds'])
        count+=1
    # Equal signed extrema eliminate empty reset; same-sign dense pays reset.
    assert transaction([50,-50])['empty_s']==0
    assert transaction([50])['empty_s']>1
    for n in (64,80):
        for stroke in (40,50):
            dense=schedule([[stroke]*n for _ in range(n)],16,stroke)
            tx=transaction([stroke]*16)
            assert dense['stations']==n*n//16
            expected=5+dense['seek_s']+dense['return_s']+(n*n//16+1)*tx['seconds']
            assert math.isclose(dense['seconds'],expected)
        assert schedule([[0]*n for _ in range(n)],16,50)['seconds']==0
    assert geometry(64)['pinion_neighbor_gap_mm']>0
    assert geometry(80)['pinion_neighbor_gap_mm']<0
    assert geometry(64,e=.6)['axial_mesh_reserve_mm']<0
    # Independent energy/force consistency for sixteen loaded torque sites.
    force=forces();theta=2*math.pi;travel=math.pi*4
    assert math.isclose(force['tip_force_N']*travel,16*.35*theta)
    # Mixed signed, threshold-rich rows: shared cannot inherit independent dwell.
    assert transaction([-50,-20,10,30,50])['groups']==5
    # Rigid sixfold sockets: commensurate command grid works ideally; arbitrary
    # off-grid correction destroys simultaneous engagement despite free torque.
    assert math.isclose(phase_span([0,10,20,30,40,50]),0.,abs_tol=1e-10)
    assert math.isclose(phase_span([0,.25]),30.,abs_tol=1e-10)
    assert phase_span([0,.25])>2*5
    assert selection_envelope(64)['conflicts']==0
    assert selection_envelope(80)['conflicts']==0  # gears still fail separately
    return dict(exhaustive_rows=count,checks='signed monotonic replay, unchanged isolation, finite rack travel, dense/no-op anchors, clearance failures, work equality')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    verified=checks()
    print(json.dumps(verified if args.check else dict(verification=verified,
        rows=[report(n,16,s) for n,s in itertools.product((64,80),(40,50))],
        sensitivities=[report(64,16,50,**kw) for kw in (dict(lead=2),dict(rpm=400),dict(switch=.2))],
        geometry=[dict(n=n,stroke=s,**geometry(n,stroke=s)) for n,s in itertools.product((64,80),(40,50))],
        selection={n:selection_envelope(n) for n in (64,80)},
        phase=dict(sixfold_grid_mm={lead:lead/6 for lead in (2,3)},off_grid_witness_span_deg=phase_span([0,.25])),
        force_scenarios=[dict(torque=t,mass=m,**forces(torque=t,mass=m)) for t,m in itertools.product((.1,.35,1.),(.25,.5,1.))],
        costs={n:cost(n) for n in (64,80)}),indent=2))
