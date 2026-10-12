"""E-231. Ideal support replay + explicitly assumed resource scenarios. Stdlib.
No calibrated probabilities, market prices, CAD or physical validation.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
s = importlib.util.spec_from_file_location('e230', Path(__file__).resolve().parents[1]/'E-230/screen.py')
p = importlib.util.module_from_spec(s); s.loader.exec_module(p)
move, J = p.move, p.STEP
Q = p.Q


def replay(old, target, coupling='selective', stop=None):
    # State G=(bar,pickup)=(1,0), O=(1,1), M=(0,1).
    h=list(old); bar=[True]*len(h); pick=[False]*len(h)
    trace=[]
    def check(z):
        assert all(b or m for b,m in zip(bar,pick)), 'last support'
        assert all(not m or x==z for x,m in zip(h,pick)), 'plane contact'
        assert all(a!=b or x==a for a,b,x in zip(old,target,h)), 'unchanged'
    for k,z in enumerate(list(range(5))+list(reversed(range(5)))):
        h[:]=[z if m else x for x,m in zip(h,pick)]; check(z)
        selected=[a!=b and (a if k<5 else b)==z for a,b in zip(old,target)]
        before=pick[:]
        if coupling=='erase':
            pick[:]=[False]*len(h); check(z)
        for i,on in enumerate(selected):
            if not on: continue
            if k<5:
                pick[i]=True; check(z) # G -> O, prove before withdrawing bar
                bar[i]=False; check(z)
            else:
                bar[i]=True; check(z) # M -> O, prove before withdrawing pickup
                pick[i]=False; check(z)
        assert all(on or pick[i]==before[i] for i,on in enumerate(selected))
        trace.append(tuple(h))
        if stop==k:
            # Recovery requires seating every member at this discrete plane,
            # then releasing pickups; never erase an unsupported register.
            bar[:]=[True]*len(h); check(z)
            pick[:]=[False]*len(h); check(z)
            return tuple(h)
    assert h==list(target) and all(bar) and not any(pick)
    return trace


def phase(kind,q):
    n=80//q
    if kind=='direct': return 3*J # E-230 write then two support stages
    if kind=='scan':
        # At each stopped group: gate/prove, two output stages/proof,
        # retract gate/prove. No global reset or release of continuing members.
        return n*4*J+(n-1)*move(5.08)+move((n-1)*5.08)
    if kind=='matrix':
        # Optimistic grouped 3-state physical actuators, including overlap proof.
        # q driven columns x n group lines; no half-selected motion granted.
        return n*2*J+.003*n
    raise ValueError(kind)


def cycle(kind,q,a=8000):
    # Ten level writes, row out/in, empty underpass down/up, two height reads.
    return 8*move(10,a=a)+10*phase(kind,q)+2*J+2*move(2)+move(5.08)+.020


def timing(kind,q,b,a=8000,visits=None):
    n=math.ceil(80/b) if visits is None else visits
    c=cycle(kind,q,a)
    # Detected partial-row fault: actual read, ground at plane, release, empty
    # reset from 40, then online recompute/write/service; no prefetched retry.
    recovery=.010+phase(kind,q)+move(40)
    return 2+(n+1)*c+recovery


def bom(kind,q,b):
    # Same whole-machine base as E-230. Allocation, not quotes or a cost floor.
    d=dict(controller=15,power=20,frame=25,wiring=15,freight_spares=10,
        lift_motor_driver=30,common_brake=10,phase_drive=10,feed_drive=10,
        writer_drives=20,shafts_bearings=30,readers=10*b,bank_enable=3*b,
        bank_arrest=3*b,mounts_guides=4*b,retention_hardware=.02*80*b)
    if kind=='matrix':
        d.update(physical_three_state_actuators=.5*80*b,
                 bidirectional_line_drivers=.10*(q+80//q)*b,
                 isolation_components=.05*80*b)
    else: d['data_channels']=.5*(80 if kind=='direct' else q)*b
    return dict(total=sum(d.values()),items=d)


def best(kind,a=8000,multiplexed=False):
    cases=[]
    for b in range(1,81):
        for q in ((80,) if kind=='direct' else Q):
            if multiplexed and q == 80: continue
            t=timing(kind,q,b,a)
            if t<30:
                cases.append(dict(kind=kind,banks=b,q=q,time_s=t,cycle_s=cycle(kind,q,a),
                    allocation=bom(kind,q,b),physical_actuators=(80 if kind in ('direct','matrix') else q)*b,
                    retained_outputs=80*b,links=160*b,phase_s=phase(kind,q),
                    patch_five_rows_s=timing(kind,q,b,a,visits=5) if math.ceil(80/b)>=5 else None))
    return min(cases,key=lambda c:c['allocation']['total']) if cases else None


def checks():
    inherited=8*move(10)+32*J+move(5.08)+.020
    assert abs(2+15*inherited-28.674932768808223)<1e-10
    maps=0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        replay(old,target); maps+=1
    try: replay((0,1,2),(1,2,2),'erase')
    except AssertionError as e: assert str(e)=='last support'
    else: raise AssertionError('erase not exposed')
    retries=0
    for old,target in it.product(it.product(range(5),repeat=2),repeat=2):
        for k in range(10):
            actual=replay(old,target,stop=k)
            replay(actual,target); retries+=1
    # Closed-form timing agrees with explicit serial causal event list.
    for kind in ('direct','scan','matrix'):
        for q in ((80,) if kind=='direct' else Q):
            for b in (6,8,16,40):
                events=[2]+[cycle(kind,q)]*math.ceil(80/b)+[.010,phase(kind,q),move(40),cycle(kind,q)]
                assert abs(sum(events)-timing(kind,q,b))<1e-9
    # Real row realizing the stated group-event count, including sparse groups.
    for q in Q:
        old=[i%q%5 for i in range(80)]
        target=[(x+1)%5 for x in old]
        groups=sum(any(values[i]==z for i in range(g,g+q))
                   for values in (old,target) for z in range(5)
                   for g in range(0,80,q))
        assert groups==min(160,800//q)
    # Matrix sneak-path witness without isolation: selected row -> other column
    # -> other row -> selected column: three equal coils each see V/3.
    assert math.isclose(1/3+1/3+1/3,1)
    return dict(three_cell_maps=maps,partial_two_cell_retries=retries,
                erase_all_counterexample=True,measurements=0)


def main():
    results={k:best(k) for k in ('direct','scan','matrix')}
    b=results['scan']['banks']
    force=p.drive(b,3.27,head_mass=.5)
    # Worst all 0 ->10 detour: every cell rises 40 and descends 30.
    out=dict(checks=checks(),best=results,
        gravity_slow={k:best(k,a=2000) for k in results},
        multiplexed_only={k:best(k,multiplexed=True) for k in ('scan','matrix')},
        scanner_free_travel_best=min(
            [dict(banks=b,q=q,time_s=2+(math.ceil(80/b)+1)*(
                cycle('direct',80)-30*J+min(160,800//q)*4*J)+.010+(80//q)*4*J+move(40),
                allocation=bom('scan',q,b)['total'])
             for b in range(1,81) for q in Q
             if 2+(math.ceil(80/b)+1)*(cycle('direct',80)-30*J+min(160,800//q)*4*J)+.010+(80//q)*4*J+move(40)<30],
            key=lambda c:c['allocation']),
        writer_throw_s=J,scanner_force_N={str(r):results['scan']['q']*b*r for r in (.3,1,3)},
        drive_at_scanner_banks=force,work_detour_J=6400*3.27*.04,
        work_direct_0_to_10_J=6400*3.27*.01,
        gravity_drag_limit_N={str(a):.003*(9.81-a) for a in (8,2)},
        errors={str(e):dict(foot_side_clearance_mm=(5.08-4-1)/2-e,
            thin_half_mm_blade_margin_mm=(5.08-4-.5)/2-e,
            stopped_writer_margin_mm=(4-2)/2-e,
            underpass_margin_mm=2-2*e,opposing_seat_motion_mm=2*e) for e in (.15,.35,.70)},
        redundancy_optimistic=dict(extra_pickups_B6=480,extra_links_B6=480,
            extra_stage_time_s=10*2*J,base_cycle_s=cycle('direct',80)),
        read_union_bound_assuming_u=64000*1e-6)
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
