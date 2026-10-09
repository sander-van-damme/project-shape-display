"""Rigid A-016 reset/displacement controllers and E-079 writer budget.
All physical input values are inherited hypothetical bounds, not measured priors.
Standard library; deterministic workload construction, no Monte Carlo.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('trip', Path(__file__).resolve().parents[1]/'E-079/short_trip.py')
trip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trip)


def masks(old, target):
    changed = {(r,c) for r,row in enumerate(old) for c,h in enumerate(row) if h != target[r][c]}
    levels = sorted({target[r][c] for r,c in changed})
    return [changed] + [{(r,c) for r,c in changed if target[r][c] == h} for h in levels], levels


def replay(old, target, skip_pawl_proof=False, policy="reset"):
    """Rigid common elevator; zero-deposit reset or direct signed displacements.

    Collet offset is fixed while gripped. Pawls are ideal ground supports;
    unloading microtravel, finite geometry and sensing remain unmodelled.
    """
    commands, _ = masks(old, target)
    changed = commands[0]
    shape = [(r,c) for r,row in enumerate(old) for c in range(len(row))]
    height = {x:old[x[0]][x[1]] for x in shape}
    pawl = {x:True for x in shape}
    offset = {}  # absent means not gripped; present means height=elevator+offset
    elevator = 0
    path = [0]
    events = 0
    written = []

    def check():
        nonlocal events
        events += 1
        assert all(pawl[x] or x in offset for x in shape), 'unsupported cell'
        assert all(height[x] >= 0 for x in shape), 'below ground datum'
        if policy == 'displacement':
            assert all(min(old[r][c],target[r][c]) <= height[(r,c)] <= max(old[r][c],target[r][c]) for r,c in shape)
        assert all(height[x] == elevator + d for x,d in offset.items())
        assert all(height[x] == old[x[0]][x[1]] and pawl[x] and x not in offset
                   for x in shape if x not in changed), 'regional disturbance'

    def acquire(sites):
        if not sites: return
        written.append(set(sites))
        for x in sites:
            assert pawl[x] and x not in offset
            offset[x] = height[x] - elevator
        check()  # grip proof before ground release
        for x in sites: pawl[x] = False
        check()

    def deposit(sites):
        if not sites: return
        written.append(set(sites))
        if not skip_pawl_proof:
            for x in sites: pawl[x] = True
        check()
        for x in sites: del offset[x]
        check()  # missed ground engagement must fail here

    def move(z):
        nonlocal elevator
        if z == elevator: return
        assert all(not pawl[x] for x in offset), 'moving against ground support'
        elevator = z
        path.append(z)
        for x,d in offset.items(): height[x] = z+d
        check()

    check()
    if policy == 'reset':
        descending = {x for x in changed if height[x] > 0}
        acquire(descending)
        old_levels = sorted({old[r][c] for r,c in descending})
        for h in old_levels:
            move(-h)
            deposit({x for x in descending if old[x[0]][x[1]] == h})
        assert all(height[x] == 0 and pawl[x] and x not in offset for x in changed)
        bottom = elevator
        ascending = {x for x in changed if target[x[0]][x[1]] > 0}
        acquire(ascending)
        for h in sorted({target[r][c] for r,c in ascending}):
            move(bottom+h)
            deposit({x for x in ascending if target[x[0]][x[1]] == h})
    elif policy == 'displacement':
        # Do opposite signs separately so no cell leaves its old/target interval.
        for sign in (-1,1):
            sites={x for x in changed if sign*(target[x[0]][x[1]]-old[x[0]][x[1]]) > 0}
            acquire(sites)
            deltas=sorted({target[r][c]-old[r][c] for r,c in sites},key=abs)
            for delta in deltas:
                move(delta)
                deposit({x for x in sites if target[x[0]][x[1]]-old[x[0]][x[1]] == delta})
            move(0)  # all of this sign deposited; opposite sign still grounded
    else: raise ValueError(policy)
    move(0)  # empty return is part of the cycle
    assert not offset
    assert all(height[x] == target[x[0]][x[1]] and pawl[x] for x in shape)
    return dict(state_events=events,command_events=len(written),
                row_writes=sum(len({r for r,c in mask}) for mask in written),
                selected_site_commands=sum(map(len,written)),
                elevator_path=path,travel=sum(abs(b-a) for a,b in zip(path,path[1:])))


def slip_reset(old, target, span_mm=40.):
    """Alternative: clamp slides down tails after columns meet a hard zero stop.
    Force is a scenario; this calculation supplies no clamp or stop qualification.
    """
    changed = masks(old,target)[0][0]
    max_old = max((old[r][c] for r,c in changed),default=0)
    slip = sum(max_old-old[r][c] for r,c in changed)
    return dict(relative_slip_m=slip*span_mm/1000,
                # Inputs are normalized heights in [0,1] in this function.
                changed=len(changed),max_stalled_cells=len(changed))


def workloads(n, levels, kind):
    target = [[c % levels for c in range(n)] for _ in range(n)]
    old = [[(h+1) % levels for h in row] for row in target]
    if kind == 'all_deltas':
        assert 2*(levels-1) <= n
        pairs=[(h,0) for h in range(1,levels)]+[(0,h) for h in range(1,levels)]
        old=[[pairs[c % len(pairs)][0] for c in range(n)] for _ in range(n)]
        target=[[pairs[c % len(pairs)][1] for c in range(n)] for _ in range(n)]
    if kind == 'uniform':
        target = [[levels-1]*n for _ in range(n)]; old = [[0]*n for _ in range(n)]
    if kind == 'local':
        old = [[0]*n for _ in range(n)]; target = [[0]*n for _ in range(n)]
        for r in range(5):
            for c in range(5):target[r][c] = 1+c % (levels-1)
    if kind == 'unchanged': old = [row[:] for row in target]
    return old,target


def account(old,target,policy='reset'):
    commands, levels = masks(old,target)
    # Historical synchronous-reset count retained only as an unattained/slip-route bound.
    baseline = sum(len({r for r,c in mask}) for mask in commands)
    result = replay(old,target,policy=policy)
    return dict(changed=len(commands[0]),destination_levels=len(levels),
                serial_dual_row_writes=2*result['row_writes'],
                synchronous_reset_row_writes=baseline,**result)


def rest_move(distance, acceleration, speed=float('inf')):
    if distance == 0:return 0.
    peak = min(speed,math.sqrt(distance*acceleration))
    return 2*peak/acceleration + (distance-peak*peak/acceleration)/peak


def asymmetric_move(distance, acceleration, braking):
    return math.sqrt(2*distance*(1/acceleration+1/braking))


def timing(stroke_mm,row_writes,accel,other=6.,retry_rows=0):
    # Two complete rest-to-rest legs; infinite speed cap is deliberately optimistic.
    cycle = 2*rest_move(stroke_mm/1000,accel)
    return dict(cycle_s=cycle,writer_only_s=row_writes*cycle,
                reserved_total_s=other+(row_writes+retry_rows)*cycle,
                strict_pass=other+(row_writes+retry_rows)*cycle < 30.)


def verification():
    # Exhaust every old/new two-cell map over three heights, including unchanged cells.
    cases=0
    for old,new in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
        replay([old],[new]);replay([old],[new],policy='displacement');cases+=1
    for policy in ('reset','displacement'):
        try: replay([[0]],[[1]],skip_pawl_proof=True,policy=policy)
        except AssertionError as exc: assert str(exc)=='unsupported cell'
        else: raise AssertionError('missed failed support handoff')
    # Independent hand computation for triangular motion; integrate both phases.
    d=.009;a=20.;half=math.sqrt(d/a)
    assert math.isclose(rest_move(d,a),2*half)
    assert math.isclose(.5*a*half**2 + a*half*half-.5*a*half**2,d)
    assert rest_move(0,20)==0
    assert math.isclose(asymmetric_move(d,a,a),rest_move(d,a))
    A,B=18.,178.
    peak=math.sqrt(2*d/(1/A+1/B))
    assert math.isclose(peak**2/(2*A)+peak**2/(2*B),d)
    assert math.isclose(peak/A+peak/B,asymmetric_move(d,A,B))
    assert math.isclose(rest_move(.1,20,.2),.51)
    for H in (2,5,9,21,80,81):
        row=account(*workloads(80,H,'mixed'))
        assert row['synchronous_reset_row_writes']==80*(1+min(H,80))
        if H <= 80: assert row['row_writes']==160*H
        old,target=workloads(80,H,'mixed')
        expected=2*sum(h>0 for row_ in old for h in row_)+2*sum(h>0 for row_ in target for h in row_)
        assert row['selected_site_commands']==expected
    assert account(*workloads(80,5,'unchanged'))['row_writes']==0
    # A rigid grip preserves differences; a simultaneous reset of unequal heights fails.
    initial = (10,40)
    at_bottom = tuple(h-40 for h in initial)
    assert at_bottom == (-30,0) and at_bottom[1]-at_bottom[0] == 30
    witness = replay([[1,2]],[[2,1]])
    assert witness['elevator_path'] == [0,-1,-2,-1,0]
    assert witness['row_writes'] == 6 and witness['selected_site_commands'] == 8
    # Independent path bound: down max(old), up max(target), then empty home.
    for old,new in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
        changed=[i for i in range(2) if old[i]!=new[i]]
        maximum=max([old[i] for i in changed]+[new[i] for i in changed]+[0])
        assert replay([old],[new])['travel']==2*maximum
    for H in (2,5,9,21):
        assert account(*workloads(80,H,'mixed'),policy='displacement')['row_writes']==320
        assert account(*workloads(80,H,'all_deltas'),policy='displacement')['row_writes']==160*H
    for old,new in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
        delta=[b-a for a,b in zip(old,new)]
        expected=2*(max(delta+[0])-min(delta+[0]))
        assert replay([old],[new],policy='displacement')['travel']==expected
    assert math.isclose(slip_reset([[0.,1.]],[[1.,0.]])['relative_slip_m'],.04)
    return dict(exhaustive_two_cell_maps=cases,injected_handoff_failure='caught',
                rigid_synchronous_reset_counterexample_mm=at_bottom)


def main():
    checked=verification()
    opt=trip.optimum_section(.1,.1)
    drive=trip.driven_force(opt['d'],.1,.4,.8,.1,.1,r=opt['r'])
    stroke=drive['driver_travel_bound']
    # This is E-079's CHOSEN sufficient travel, not a necessary minimum over mechanisms.
    scenarios=[]
    for H in (2,5,9,21):
        for kind in ('mixed','all_deltas','uniform','local'):
            counts=account(*workloads(80,H,kind));n=counts['row_writes']
            direct=account(*workloads(80,H,kind),policy='displacement')
            for result in (counts,direct):
                result['elevator_travel_mm']=result['travel']*40/(H-1)
                result['elevator_motion_s']=sum(rest_move(abs(b-a)*.04/(H-1),20.,.4)
                    for a,b in zip(result['elevator_path'],result['elevator_path'][1:]))
                result['writer_plus_elevator_100m_s2_s']=timing(stroke,result['row_writes'],100.)['writer_only_s']+result['elevator_motion_s']
            scenarios.append(dict(levels=H,kind=kind,**counts,direct_displacement=direct,
                all_inclusive_row_budget_ms=24000/n,
                acceleration_cases=[dict(acceleration_m_s2=a,**timing(stroke,n,a)) for a in (5.,20.,100.)],
                writer_acceleration_for_24s_m_s2=16*(stroke/1000)*(n/24)**2))
    # Optimistic constant force caps: 4.9N actuator magnitude, 4N opposing
    # Coulomb drag. Allow reversed motor force for braking. Treat gravity both
    # balanced and assisting downward return; friction is NOT a measured value.
    mass_cases=[]
    for grams,gravity in itertools.product((5.,20.,50.,100.),(0.,9.81)):
        mass=grams/1000
        accel=(4.9-4)/mass+gravity
        brake=(4.9+4)/mass-gravity
        leg=asymmetric_move(stroke/1000,accel,brake)
        mass_cases.append(dict(moving_mass_g=grams,gravity_assistance_m_s2=gravity,
            optimistic_return_acceleration=accel,optimistic_braking=brake,
            # Push assumed instantaneous to isolate return contribution.
            return_only_5level_s=800*leg,return_only_21level_s=3360*leg))
    print(json.dumps(dict(checks=checked,stroke_policy=drive,scenarios=scenarios,
        return_force_mass_cases=mass_cases,
        inventory=dict(one_array_command_memories=6400,two_array_command_memories=12800,
            one_array_shutter_apertures=12800,two_array_shutter_apertures=25600,
            row_local_writer_pins_per_array=80,persistent_output_states_per_cell=3,
            one_array_magnetic_reversible_lines=160,two_array_magnetic_reversible_lines=320),
        # Residual allowances, NOT quotes. Other contains all other purchased hardware.
        cost_allowances=[dict(other_usd=b,per_site_one_item=(500-b)/6400,
            per_site_two_items=(500-b)/12800) for b in (200,250,400)],
        readback_opportunities=dict(note='One ideal grip or pawl support observation per selected-site command; resets add handoffs',
            full_board_original_lower_bound=12800,
            corrected_5level=account(*workloads(80,5,'mixed'))['selected_site_commands'],
            corrected_21level=account(*workloads(80,21,'mixed'))['selected_site_commands']),
        slipping_comparator=[dict(levels=H,**slip_reset(
            [[h/(H-1) for h in row] for row in workloads(80,H,'mixed')[0]],
            [[h/(H-1) for h in row] for row in workloads(80,H,'mixed')[1]])) for H in (5,21)],
        sensitivity=dict(one_ms_per_row_5level_s=.800,one_ms_per_row_21level_s=3.360)),indent=2))

if __name__ == '__main__':main()
