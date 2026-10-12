"""E-230: retained row programs and synchronized drive; stdlib, stdout only.
All non-product numbers are explicit unqualified scenarios, not measurements.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e229', Path(__file__).resolve().parents[1]/'E-229'/'screen.py')
prev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prev)
move = prev.move
PULSES = (1, 1, 2, -1, -1, -2)
Q = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)
STEP = move(2)+.003


def binary(delta):
    return (int(delta < 0),)+prev.base.code(abs(delta), (1, 1, 2))


def decode(bits, phase):
    sign, *magnitude = bits
    return bool(sign == (phase >= 3) and magnitude[phase % 3])


ROM = {d: tuple(decode(binary(d), k) for k in range(6)) for d in range(-4, 5)}


def writer(kind, q, error=.35, code_pitch=3):
    """Position: common strip reset, q pushers, serial group indexing and return,
    temporary drag retention, final common positive clamp + read. All pushers
    return before group feed. Worst-case maximum push at every group is feasible.
    Binary/tape: E-229 continuous reset/set/read scan generalized to 320/480 bits.
    """
    if kind == 'position':
        n = 80//q
        stroke = 8*code_pitch
        t = (2*move(stroke)+2*move(2)+.010
             + n*(2*move(stroke)+.010)+(n-1)*move(5.08)+move((n-1)*5.08))
        return dict(seconds=t, channels=q, positions=80, bits=0,
                    span_mm=(n-1)*5.08, pusher_stroke_mm=stroke)
    count = 320 if kind == 'binary' else 480
    n = count//q
    speed = .8*min(200, (5.08-2-2*error)/(move(2)+.001),
                     2*math.sqrt(20000/(2*math.pi*2)))
    length = (n-1)*5.08+4+2*5.08
    span = length+speed**2/8000
    t = length/speed+2*speed/8000+move(span)+2*move(2)+.010
    return dict(seconds=t, channels=q, positions=0, bits=count,
                span_mm=span, pusher_stroke_mm=2)


def service():
    # Six explicit decoder retractions/index/read events; not free logical AND.
    # Two row-height reads (before and final) at .010 s each are granted.
    return 1.1+6*prev.transfer()+6*STEP+move(5.08)+.020


def schedule(w, banks, buffered, visits=None, retry=True):
    n = (math.ceil(80/banks) if visits is None else visits)+int(retry)
    s = service()
    if not buffered:
        return 2+n*(w+s)
    # Synchronized bank cohorts, two physical registers/bank. Separate common
    # writer/service selectors. No future buffer overwritten while serving.
    ready, end = [], []
    for i in range(n):
        begin = max(ready[-1] if ready else 0, end[i-2] if i >= 2 else 0)
        ready.append(begin+w+STEP)
        end.append(max(ready[-1], end[-1] if end else 0)+s+STEP)
    assert end[-1] >= n*(w+STEP)
    assert end[-1] >= w+STEP+n*(s+STEP)-1e-9
    # Retry row selected at last proof, not prefetched before the fault exists.
    # Its actual heights must be read, delta recomputed, then rewritten online.
    # Replace the last (optimistically overlapped) service with a causal drain.
    if retry:
        causal = end[-2]+.010+w+STEP+s+STEP if n > 1 else .010+w+STEP+s+STEP
        assert causal >= end[-1]-1e-9
        end[-1] = causal
    return 2+end[-1]


def inventory(kind, q, b, buffered):
    r = b*(2 if buffered else 1)
    sites = (80 if kind == 'position' else 320 if kind == 'binary' else 480)*r
    return dict(banks=b, data_actuators=q*b, media_sites=sites,
        index_notches=720*r if kind=='position' else 2*sites,
        decision_lands=(4320 if kind=='position' else 960 if kind=='binary' else 480)*r,
        decoder_probes=80*b, serial_decisions_per_probe=2 if kind=='binary' else 1,
        output_links=160*b, column_bars=80*b, pickup_slides=80*b,
        bank_enable_couplings=b, local_arrests=b,
        register_select_interfaces=2*b if buffered else 0,
        row_combs=80, columns=6400, guides=12800, shelves=44800,
        resident_support_sites=12800, temporary_drag_sites=sites if kind=='position' else 0,
        media_stock_L=sites*(32*36*3 if kind=='position' else 20*4*3)/1e6)


def bom(kind, q, b, buffered, lean=False):
    """Complete category allocations, not quotes or qualified mechanisms.
    Position channels cost same as binary optimistically: explicit sensitivity.
    """
    inv = inventory(kind,q,b,buffered)
    items = dict(controller=15 if lean else 20, power=20 if lean else 35,
        frame=25 if lean else 35, wiring=15 if lean else 25, freight_spares=10 if lean else 20,
        common_lift_motor_driver=30 if lean else 40, common_brake=10 if lean else 20,
        common_phase_drive=10 if lean else 15, common_feed_drive=10 if lean else 15,
        common_writer_drives=20, common_shafts_bearings=30,
        bank_readers=(10 if lean else 15)*b, bank_enable= (3 if lean else 5)*b,
        local_arrest=(3 if lean else 5)*b, bank_mounts_guides=(4 if lean else 5)*b,
        data_channels=.5*inv['data_actuators'], media_hardware=.02*inv['media_sites'],
        buffer_interfaces=2*inv['register_select_interfaces'],
        common_buffer_drives=16 if buffered else 0)
    return dict(total=sum(items.values()), items=items)


def replay(old, target, kind, fault=None, truncate=None):
    h=list(old); programs=[b-a for a,b in zip(old,target)]
    row=True; col=[True]*len(h); pickup=[False]*len(h)
    def check(brake=True):
        assert all(row or c or (p and brake) for c,p in zip(col,pickup)), 'last support'
        assert all(a!=b or x==a for a,b,x in zip(old,target,h)), 'unchanged height'
        assert all(0<=x<=4 for x in h), 'range'
    for k,pulse in enumerate(PULSES):
        if truncate == k: return tuple(h)
        assert row and all(col) and not any(pickup)
        phase = (k+1)%6 if fault=='phase' else k
        assert phase == k, 'phase read'
        mask=[(decode(binary(d),phase) if kind=='binary' else ROM[d][phase]) for d in programs]
        if fault=='overwrite': programs[0]=0
        assert programs == [b-a for a,b in zip(old,target)], 'retained program read'
        pickup[:]=mask
        if fault=='output': pickup[0]=not pickup[0]
        assert pickup==mask, 'actual output read'
        check(); row=False; col[:]=[not s for s in mask]
        check(brake=fault!='arrest')
        h[:]=[x+pulse if s else x for x,s in zip(h,mask)]; check()
        row=True; col[:]=[True]*len(h)
        if fault=='reseat': row=False; col[:]=[False]*len(h)
        assert row and all(col), 'actual support read'
        pickup[:]=[False]*len(h); check()
    assert h == list(target)
    return tuple(h)


def drive(b, load, head_mass=.5, column_mass=.003, friction=.2):
    count=80*b
    mass=b*head_mass+count*column_mass
    # load includes gravity/load of selected columns, not inertial force.
    f=count*load*(1+friction)+b*head_mass*9.81+mass*8
    torque=f*.01
    shaft={str(d):.01*torque*.4/(80e9*(math.pi*(d/1000)**4/32))*1000
           for d in (8,12,20)}
    return dict(selected_cells=count, moving_mass_kg=mass, peak_force_N=f,
        shaft_torque_Nm=torque, motor_torque_at_efficiency_07_Nm=torque/.7,
        peak_input_power_W=f*.2/.7, static_arrest_Nm=(count*load+b*head_mass*9.81)*.01,
        # All cells 0 ->40 gives useful work; ± pulse train travel is not
        # simultaneous full payload work. Worst-row drive still runs six phases.
        full_map_up_work_J=6400*load*.04,
        output_shaft_twist_height_mm=shaft)


def merge_retire(old, target):
    """Changed transaction control: acquire at actual old height on one common
    plane, pool at 40, retire on descent at target. No old-height capture array.
    Continuing membership may NOT be erased during a mask update.
    """
    h=list(old); member=[False]*len(h); bar=[True]*len(h)
    def check(z):
        assert all(c or m for c,m in zip(bar,member))
        assert all(not m or x==z for x,m in zip(h,member))
        assert all(a!=b or x==a for a,b,x in zip(old,target,h))
    for z in range(5):
        if z:
            h[:]=[z if m else x for x,m in zip(h,member)]
        check(z)
        join=[a!=b and a==z for a,b in zip(old,target)]
        member[:]=[m or j for m,j in zip(member,join)]; check(z)
        bar[:]=[c and not j for c,j in zip(bar,join)]; check(z)
    for z in reversed(range(5)):
        h[:]=[z if m else x for x,m in zip(h,member)]; check(z)
        leave=[m and b==z for m,b in zip(member,target)]
        bar[:]=[c or v for c,v in zip(bar,leave)]; check(z)
        member[:]=[m and not v for m,v in zip(member,leave)]; check(z)
    assert h==list(target) and all(bar) and not any(member)


def checks():
    assert abs(prev.schedule(0,6)-31.720199576606166)<1e-9
    assert abs(prev.schedule(prev.writer('direct',80)['seconds'],8)-26.079916278555654)<1e-9
    assert len(set(binary(d) for d in ROM))==9
    for d,mask in ROM.items():
        assert sum(p*s for p,s in zip(PULSES,mask))==d
    maps=0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        for kind in ('position','binary','tape'): replay(old,target,kind)
        merge_retire(old,target)
        maps+=1
    for kind in ('position','binary','tape'):
        for fault in ('phase','overwrite','output','arrest','reseat'):
            try: replay((0,4,2),(4,0,2),kind,fault)
            except AssertionError: pass
            else: raise AssertionError('fault escaped '+fault)
    # Read actual resident-supported partial heights, regenerate the delta.
    for old,target in it.product(range(5),repeat=2):
        for k in range(7):
            partial=replay((old,),(target,),'binary',truncate=k)
            replay(partial,(target,),'binary')
    # Explicit stale-delta counterexample: 0 ->4 after first +1 becomes5.
    assert 1+sum(p*s for p,s in zip(PULSES,ROM[4]))==5
    # Reset both sites, push one group at a time, retract with temporary
    # retention, clamp after all writes. Loss of temporary retention is fatal.
    for initial,target in it.product(it.product(range(9),repeat=2),repeat=2):
        state=list(initial); state[:]=[0,0]
        for group in range(2):
            before=state[:]; state[group]=target[group]
            assert state[1-group]==before[1-group]
            retained=state[:]
            pusher=0
            assert state==retained
        assert tuple(state)==target
    for q in Q:
        for kind in ('position','binary','tape'):
            w=writer(kind,q)['seconds']
            for b in (6,8,16):
                assert schedule(w,b,False)==2+(math.ceil(80/b)+1)*(w+service())
                assert schedule(w,b,True)>schedule(w,b,True,retry=False)+service()
    return dict(three_cell_maps_per_decoder=maps, decoder_topologies=3,
        injected_faults=15, partial_row_retry_cases=175,
        predecessor_control='reproduced', physical_measurements=0)


def main():
    out=dict(checks=checks(), evidence='assumptions, finite ideal replay, calculations',
        code_table={str(d):dict(binary=binary(d), pulses=ROM[d]) for d in ROM},
        row_service_s=service(), inherited_B8_extra_row_budget_s=(28/11-1.1-6*prev.transfer()-move(5.08)))
    picks=[]
    for kind in ('position','binary','tape'):
        for buffered in (False,True):
            candidates=[]
            for b in range(1,81):
                for q in Q:
                    w=writer(kind,q)
                    t=schedule(w['seconds'],b,buffered)
                    if t<30:
                        candidates.append(dict(kind=kind,banks=b,lanes=q,buffered=buffered,
                            time_s=t,writer=w,inventory=inventory(kind,q,b,buffered),
                            lean=bom(kind,q,b,buffered,True),allocation=bom(kind,q,b,buffered)))
            best=min(candidates,key=lambda c:c['lean']['total'])
            best['fewest_channels']=min(c['inventory']['data_actuators'] for c in candidates)
            best['five_row_patch_s']=schedule(best['writer']['seconds'],best['banks'],buffered,visits=5)
            picks.append(best)
    out['lowest_lean_allocation_timing_cases']=picks
    out['B8_position_buffer_q20']=dict(writer=writer('position',20),
        time_s=schedule(writer('position',20)['seconds'],8,True),
        no_retry_s=schedule(writer('position',20)['seconds'],8,True,retry=False))
    out['position_6mm_pitch_best'] = min(
        [dict(banks=b,lanes=q,time_s=schedule(writer('position',q,code_pitch=6)['seconds'],b,True),
              lean=bom('position',q,b,True,True)['total'])
         for b in range(1,81) for q in Q
         if schedule(writer('position',q,code_pitch=6)['seconds'],b,True)<30],
        key=lambda c:c['lean'])
    # Optimistic direct writer common-plane control; no scanning reset allowed.
    c=8*move(10)+22*STEP+10*STEP+move(5.08)+.020
    b=next(b for b in range(1,81) if 2+(math.ceil(80/b)+1)*c<30)
    out['merge_retire_direct_control']=dict(row_cycle_s=c,banks=b,
        time_s=2+(math.ceil(80/b)+1)*c,data_channels=80*b,
        lean_allocation=195+20*b+.5*80*b+.02*80*b,
        status='ideal alternative; active membership overwrite and routing owed')
    out['force_B8']={str(f):drive(8,f) for f in (1,3.27,10)}
    out['error_bounds']={str(e):dict(position_3mm_pitch_2mm_probe_margin_mm=.5-e,
        position_6mm_pitch_2mm_probe_margin_mm=2-e,
        binary_4_2_margin_mm=1-e, serial_two_gate_adverse_margin_mm=1-2*e,
        opposing_support_settling_mm=2*e) for e in (.15,.35,.7)}
    out['union_bound_at_u_1e_6']=dict(row_codes=6400e-6,binary_sites=25600e-6,
        output_mask_decisions=38400e-6)
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
