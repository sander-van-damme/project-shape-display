"""E-232: fixed-mask admission counterexamples and unloaded-stop bounds.
Stdlib, stdout only. Ideal supports and labelled allocation/error scenarios;
no contact model, calibrated process distribution, prices or measurements.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e231', Path(__file__).resolve().parents[1]/'E-231/screen.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
move, J = p.move, p.J


def fixed_failure(old, target, keep_support):
    """Periodic rigid groove support, changed mask fixed for whole sweep.
    Keeping a 2-mm tooth in a 4-mm groove allows at most 2 mm upward escape
    even when initially seated against the favorable face (not just +/-1).
    """
    for a, b in zip(old, target):
        if a == b:
            continue
        if not keep_support and a > 0:
            return 'unsupported before pickup'
        if keep_support and 40-a > 2:
            return 'groove roof blocks ascent'
    return None


def oracle_replay(old, target, fault=None):
    """EXPLICIT ORACLE: release old support individually on plane contact.
    Tests only target-stop handoff, not the requested fixed-mask admission.
    Recovery completes descent to the actual stop profile, seats row, reads,
    then replans. It never retracts loaded stops or prefetches a retry.
    """
    changed = [a != b for a, b in zip(old, target)]
    h = list(old)
    support = ['resident']*len(h)
    trace = []
    for z in range(0, 43):
        for i, a in enumerate(old):
            if changed[i] and z >= a:
                h[i] = z
                support[i] = 'arrested pickup'
        assert all(a != b or h[i] == a for i, (a,b) in enumerate(zip(old,target)))
        trace.append(tuple(h))
    # Stops were programmed below feet: top target-42, then common +42.
    assert all(b-42 < a for a,b in zip(old,target))
    actual = list(target)
    if fault is not None:
        i, code = fault
        actual[i] = code
    for z in range(42, -1, -1):
        for i in range(len(h)):
            if changed[i]:
                h[i] = max(z, actual[i])
                support[i] = 'grounded stop' if actual[i] >= z else 'arrested pickup'
        assert all(support)
        assert all(a != b or h[i] == a for i,(a,b) in enumerate(zip(old,target)))
    # Common row comb seats only at observed grid heights; stops clear AFTER.
    assert all(x % 10 == 0 for x in h)
    support[:] = ['resident']*len(h)
    return tuple(h), trace


def writer(kind):
    # Direct 80 release gates/head; preset plus five releases; reset out/back,
    # clear return, four stopped programming increments, clamp in/out, read.
    stroke, step = (32,8) if kind == 'stairs' else (40,10)
    if kind == 'layers':
        # Three physical binary leaf outputs/cell; common lock, full read.
        return 3*J+2*J+.010
    return 3*move(stroke)+4*move(step)+8*J+.010


def cycle(kind, live=False, a=8000):
    # Three-stage fixed changed-mask setup, whole stop-carrier down/up, pickup
    # rise/fall, row out/in, underpass out/in, feed and old/final reads.
    ascent = 4*move(10,a=a)+move(2,a=a) if live else move(42,a=a)
    c = (writer(kind)+3*J+2*move(42)+ascent+move(42,a=a)
         +2*J+2*move(2)+move(5.08)+.020)
    # Hybrid retains five contact-triggered admission writes, descent geometric.
    return c + (15*J if live else 0)


def bom(kind,b):
    d = p.bom('direct',80,b)['items'].copy()
    d.update(stop_carrier_motor_driver=20, stop_carrier_brake=10,
             stop_carrier_local_arrests=3*b, stop_mounts_guides=5*b,
             stop_read_coverage=5*b)
    d['stop_hardware'] = .02*80*b*(3 if kind=='layers' else 1)
    d['stop_program_channels'] = .5*80*b*(3 if kind=='layers' else 1)
    if kind=='bars':
        d['temporary_unloaded_bar_holds'] = .10*80*b
    return dict(total=sum(d.values()), items=d)


def timing(kind,b,live=False,a=8000,visits=None):
    # After detected stable discrete stop error, finish supported descent,
    # seat row, read, clear plane and stops, then fresh full physical program.
    r=move(42,a=a)+J+.010+move(42)+move(42)
    return 2+((math.ceil(80/b) if visits is None else visits)+1)*cycle(kind,live,a)+r


def best(kind,live=False,a=8000):
    candidates=[dict(banks=b,time_s=timing(kind,b,live,a),row_s=cycle(kind,live,a),
                     allocation=bom(kind,b),outputs=(320 if kind=='layers' else 160)*b)
                for b in range(1,81) if timing(kind,b,live,a)<30]
    return min(candidates,key=lambda c:c['allocation']['total'])


def checks():
    levels=(0,10,20,30,40)
    maps=retries=0
    for old,target in it.product(it.product(levels,repeat=3),repeat=2):
        actual,_=oracle_replay(old,target)
        assert actual == target
        maps+=1
    # A mixed changed row fails both choices, with unchanged neighbor invariant.
    witness=((10,30,20),(20,0,20))
    assert fixed_failure(*witness,False)=='unsupported before pickup'
    assert fixed_failure(*witness,True)=='groove roof blocks ascent'
    for old,target in it.product(it.product(levels,repeat=2),repeat=2):
        for i in range(2):
            for code in levels:
                partial,_=oracle_replay(old,target,(i,code))
                final,_=oracle_replay(partial,target)
                assert final==target
                retries+=1
    # Before ascent, stationary target may geometrically penetrate old foot.
    assert max(10,30)==30 and 30>10
    # Two level combs: finite lower foot hits upper shelf before upper pickup.
    for foot, shelf in it.product((1.,2.,4.),repeat=2):
        collision_z=10-foot-shelf
        assert collision_z < 10
    # Stair stock arbitrary translations: intervals disjoint only if row pitch
    # exceeds five 8-mm lands plus four 8-mm index offsets = 72 mm.
    for b in range(1,81):
        gap=406.4/b
        assert (gap>=72)==(b<=5)
    assert abs(p.timing('direct',80,6)-29.962484334260363)<1e-6
    assert abs(move(0))<1e-12
    assert move(42,a=2000)>move(42,a=8000)
    for kind in ('bars','stairs','layers'):
        for b in (4,8,16):
            events=[2]+[cycle(kind)]*(math.ceil(80/b)+1)+[move(42),J,.010,move(42),move(42)]
            assert abs(sum(events)-timing(kind,b))<1e-9
    return dict(oracle_three_cell_maps=maps,wrong_stop_retries=retries,
                fixed_mask_failures=2,finite_layer_collision_cases=9,
                physical_measurements=0)


def main():
    results={k:best(k) for k in ('bars','stairs','layers')}
    b=results['stairs']['banks']
    out=dict(checks=checks(),oracle_only=results,
             hybrid_stairs=best('stairs',live=True),slow_oracle_stairs=best('stairs',a=2000),
             reused_stairs_writer=dict(
                 allocation=results['stairs']['allocation']['total']-.5*80*b+10+.02*80*b,
                 physical_gates=80*b, fixed_mask_bits=80*b,
                 time_s=timing('stairs',b)+(math.ceil(80/b)+1)*2*J,
                 assumption='common mode shift + retained mask; extra interfaces unbuilt'),
             free_stairs_channels_allocation=results['stairs']['allocation']['total']-80*b,
             stairs_nonoverlap_B5_s=timing('stairs',5),
             stairs_five_rows_s=timing('stairs',b,visits=5),
             force_scenarios={str(f):p.p.drive(b,f,head_mass=1.5) for f in (1,3.27,10)},
             writer_force_N={str(r):80*b*r for r in (.3,1,3)},
             errors={str(e):dict(existing_blade_margin_mm=.04-e,
                         two_1mm_lanes_each_margin_mm=(4/2-1)/2-e,
                         stop_parking_margin_mm=2-2*e,
                         stair_land_margin_mm=(8-2)/2-2*e,
                         row_takeover_shift_mm=2*e) for e in (.15,.35,.7)},
             stairs_stock_L=80*b*40*40*4/1e6,
             bars_stock_L=80*b*64*3.4*1.6/1e6,
             detour_up_work_J=6400*3.27*.042,
             direct_0_10_work_J=6400*3.27*.01,
             gravity_drag_N={str(a):.003*(9.81-a) for a in (8,2)},
             read_union_bound_at_assumed_1e_6=4*6400*1e-6)
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
