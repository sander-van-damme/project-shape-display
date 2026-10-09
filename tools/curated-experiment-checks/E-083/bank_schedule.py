"""Banked E-082 row writer, exact transient-mask differences and strip bounds.
Deterministic scenarios, not physical priors, hardware timing or cost quotes.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path


def source(name, relative):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parents[1]/relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

schedule = source('schedule', 'E-081/mask_schedule.py')
clutch = source('clutch', 'E-082/row_clutch.py')


def commands(old, target, policy):
    """Explicit selected sets matching E-081's acquire/deposit events."""
    changed = {(r,c) for r,row in enumerate(old) for c,h in enumerate(row) if h != target[r][c]}
    result = []
    if policy == 'displacement':
        for sign in (-1, 1):
            group = {x for x in changed if sign*(target[x[0]][x[1]]-old[x[0]][x[1]]) > 0}
            if group:
                result.append(group)
                for delta in sorted({target[r][c]-old[r][c] for r,c in group},key=abs):
                    result.append({(r,c) for r,c in group if target[r][c]-old[r][c] == delta})
    elif policy == 'reset':
        for heights in (old, target):
            group = {(r,c) for r,c in changed if heights[r][c] > 0}
            if group:
                result.append(group)
                for height in sorted({heights[r][c] for r,c in group}):
                    result.append({(r,c) for r,c in group if heights[r][c] == height})
    else:
        raise ValueError(policy)
    return result


def transactions(sequence, rows, banks, clear=True, broken=False):
    """Cam parked until all banks finish each phase. Independent 80-data-drive
    banks may address one distinct local row each. Final mask is zero.
    One transaction writes ALL row bits to their intended values, including 0.
    Ideal known old states/readback/output retention are prerequisites.
    """
    assert rows % banks == 0
    bank_rows = rows//banks
    state = [set() for _ in range(rows)]
    phases = []
    bit_changes = 0
    for mask in sequence + ([set()] if clear and sequence else []):
        goal = [set() for _ in range(rows)]
        for r,c in mask: goal[r].add(c)
        dirty = {r for r in range(rows) if state[r] != goal[r]}
        if broken: dirty &= {r for r,c in mask}  # deliberately omit stale-only rows
        counts = [sum(r//bank_rows == b for r in dirty) for b in range(banks)]
        bit_changes += sum(len(a ^ b) for a,b in zip(state,goal))
        for r in sorted(dirty): state[r] = goal[r].copy()
        assert state == goal, 'stale selection'
        phases.append(dict(row_writes=sum(counts),rounds=max(counts),bank_rows=counts))
    return dict(row_writes=sum(p['row_writes'] for p in phases),
                rounds=sum(p['rounds'] for p in phases),bit_changes=bit_changes,
                phases=phases)


def drive(banks, drag, stiffness, mass_g, requested_a=20., row_a=20., strength=10.):
    s = clutch.section(1.2,1.85,1.,.1)
    # Short independent bars reduce feet per drive. All feet may share adverse drag.
    f = clutch.force_window(s,stiffness,drag/banks,allowable=strength)
    f['foot_drag_N'] = drag
    f['feet_per_bar'] = 80//banks
    if not f['admissible']: return None
    # Reserve half the STATIC remaining force margin for limiter/overshoot error.
    # This is a necessary inertial screen; it does not solve flexible-bar dynamics.
    a = min(requested_a, .5*f['force_reserve_N']/(mass_g/1000))
    cycle = sum(clutch.rest(d,a) for d in (s['d'], f['x_drive_mm'], f['x_unload_mm']))
    cycle += 2*clutch.rest(1.,row_a)
    return dict(**f, mass_g=mass_g, acceleration_m_s2=a, cycle_s=cycle,
                dynamic_peak_N=f['peak_N']+mass_g/1000*a,
                residual_force_N=f['force_reserve_N']-mass_g/1000*a)


def inventory(banks, arrays=1, reserve=250., key_price=0.):
    data=80*banks*arrays
    rows=80*arrays
    repeated=6400*arrays
    remaining=500-reserve-repeated*key_price
    return dict(data_drives=data,row_channels=rows,total_channels=data+rows,
                dogs=repeated,keys=repeated,retention_sites=repeated,
                row_rails=rows,data_bars=data,active_bar_span_mm=406.4/banks,
                strict_data_channel_allowance_usd=remaining/data,
                strict_all_channel_allowance_usd=remaining/(data+rows),
                # Complete drives including motor, transmission, limiter and control;
                # not bare driver chips. Row hardware still omitted in first allowance.
                magnetic_reversible_lines=arrays*80*(banks+1),
                total_active_bar_length_m=32.512*arrays)


def checks():
    cases=0
    for old,new in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
        for policy in ('reset','displacement'):
            seq=commands([old],[new],policy)
            ref=schedule.replay([old],[new],policy=policy)
            assert len(seq)==ref['command_events']
            assert sum(map(len,seq))==ref['selected_site_commands']
            transactions(seq,1,1)
            cases+=1
    # Exhaust three successive 2x2 masks, with final clear: known old endpoints,
    # disjoint rows, all-zero masks and reuse of identical masks all exercised.
    masks=[{(r,c) for r in range(2) for c in range(2) if n & (1 << (r*2+c))} for n in range(16)]
    histories=0
    for seq in itertools.product(masks,repeat=3):
        serial=transactions(list(seq),2,1)
        parallel=transactions(list(seq),2,2)
        # Independently count each row's binary-vector changes including final 0.
        row_count=0
        for r in range(2):
            values=[tuple((r,c) in mask for c in range(2)) for mask in [set(),*seq,set()]]
            row_count+=sum(a!=b for a,b in zip(values,values[1:]))
        assert serial['row_writes']==parallel['row_writes']==row_count
        assert parallel['rounds']<=serial['rounds']
        histories+=1
    try: transactions([{(0,0)},{(1,0)}],2,1,broken=True)
    except AssertionError as exc: assert str(exc)=='stale selection'
    else: raise AssertionError('missed stale mask')
    s=clutch.section(1.2,1.85,1.,.1)
    ref=clutch.force_window(s,.5,.005)
    one=drive(1,.005,.5,20.)
    assert math.isclose(one['peak_N'],ref['peak_N'])
    assert math.isclose(one['acceleration_m_s2'],2.875)
    assert drive(1,.03,.5,20.) is None
    assert drive(1,.005,.5,20.,strength=5.) is None
    # Sparse workload exposes clearing old-only rows; identical masks need no rewrite.
    assert transactions([{(0,0)},{(1,0)}],80,1)['row_writes']==4
    assert transactions([{(0,0)},{(0,0)}],80,1)['row_writes']==2
    assert transactions([],80,1)['row_writes']==0
    return dict(two_cell_controller_cases=cases,three_mask_histories=histories,
                injected_stale_mask='caught',force_limit_and_strength_controls='pass')


def main():
    checked=checks()
    workloads=[]
    for H,kind,policy in itertools.product((5,21),('mixed','all_deltas','local','uniform'),('reset','displacement')):
        old,new=schedule.workloads(80,H,kind)
        seq=commands(old,new,policy)
        ref=schedule.replay(old,new,policy=policy)
        assert sum(len({r for r,c in mask}) for mask in seq)==ref['row_writes']
        workloads.append(dict(levels=H,kind=kind,policy=policy,command_events=len(seq),
            selected_row_count=ref['row_writes'],
            by_bank={b:transactions(seq,80,b) for b in (1,2,4,5,8,10,16,20,40,80)}))
    for w in workloads:
        physical = w['by_bank'][1]['row_writes']
        if w['kind'] == 'all_deltas' or (w['kind'] == 'mixed' and w['policy'] == 'reset'):
            assert physical == 80*(2*w['levels']+1)
        elif w['kind'] == 'mixed': assert physical == 240
        elif w['kind'] == 'uniform': assert physical == 160
        for banks, counts in w['by_bank'].items():
            if w['kind'] != 'local': assert counts['rounds'] == physical//banks
    cases=[]
    adverse=next(w for w in workloads if w['levels']==21 and w['kind']=='all_deltas' and w['policy']=='displacement')
    for b,f,k,m,a,strength in itertools.product((1,2,4,5,8,10,16,20,40,80),(.005,.01,.03),(.1,.5,1.),(5.,20.,50.),(20.,100.),(5.,10.,20.)):
        d=drive(b,f,k,m,requested_a=a,row_a=a,strength=strength)
        item=dict(banks=b,drag_N=f,k_N_mm=k,mass_g=m,requested_a=a,strength_MPa=strength)
        if d is None:
            cases.append(dict(**item,reject='static_force'))
            continue
        rounds=adverse['by_bank'][b]['rounds']
        base=6+rounds*d['cycle_s']
        cases.append(dict(**item,drive=d,rounds=rounds,time_s=base,
                          row_overhead_budget_ms=(30-base)*1000/rounds,
                          reject=None if base<30 else 'deadline'))
    representative=[]
    for b in (1,2,4,5,8,10,16,20,40,80):
        d=drive(b,.005,.5,20.)
        rounds=adverse['by_bank'][b]['rounds']
        representative.append(dict(banks=b,rounds=rounds,drive=d,
            time_s=6+rounds*d['cycle_s'],
            overhead_budget_ms=(24/rounds-d['cycle_s'])*1000,
            inventory=inventory(b),bought_key_inventory=inventory(b,key_price=.02)))
    summary={reason:sum(c.get('reject')==reason for c in cases) for reason in ('static_force','deadline',None)}
    print(json.dumps(dict(checks=checked,workloads=workloads,representative=representative,
        sweep=dict(total=len(cases),outcomes=summary,
            # Keep compact, reproducible counts; full population reconstructed above.
            min_banks_by_scenario=[dict(drag_N=f,mass_g=m,requested_a=a,strength_MPa=s,
                minimum_banks=min((c['banks'] for c in cases if c.get('reject') is None
                    and (c['drag_N'],c['mass_g'],c['requested_a'],c['strength_MPa'])==(f,m,a,s)),default=None))
                for f,m,a,s in itertools.product((.005,.01,.03),(5.,20.,50.),(20.,100.),(5.,10.,20.))]),
        sensitivity=dict(one_ms_overhead_at_8_banks_s=adverse['by_bank'][8]['rounds']*.001,
            retry_one_full_mask_at_8_banks_s=10*drive(8,.005,.5,20.)['cycle_s'])),indent=2))

if __name__=='__main__':main()
