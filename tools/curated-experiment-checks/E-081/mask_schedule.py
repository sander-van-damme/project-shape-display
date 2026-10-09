"""A-016 reset-and-rise controller and E-079 fixed-stroke writer budget.
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


def replay(old, target, skip_pawl_proof=False):
    """Ideal persistent physical output latches, one transient command mask.
    Verification here is an exact state observation. It is NOT a real reader.
    Failure injections below show the consequence when that assumption fails.
    """
    commands, levels = masks(old,target)
    changed = commands[0]
    shape = [(r,c) for r,row in enumerate(old) for c in range(len(row))]
    height = {x:old[x[0]][x[1]] for x in shape}
    pawl = {x:True for x in shape}
    grip = {x:False for x in shape}
    events = 0
    def check():
        nonlocal events
        events += 1
        assert all(pawl[x] or grip[x] for x in shape), 'unsupported cell'
        assert all(height[x] == old[x[0]][x[1]] and pawl[x] and not grip[x]
                   for x in shape if x not in changed), 'regional disturbance'
    check()
    for x in changed: grip[x] = True
    check()  # acquisition proof before removing ground support
    for x in changed: pawl[x] = False
    check()
    for x in changed: height[x] = 0
    check()
    for h, deposit in zip(levels, commands[1:]):
        for x in changed:
            if grip[x]: height[x] = h
        check()
        if not skip_pawl_proof:
            for x in deposit: pawl[x] = True
        check()  # pawl insertion and support proof before opening any collet
        for x in deposit: grip[x] = False
        check()
    assert all(height[x] == target[x[0]][x[1]] and pawl[x] and not grip[x] for x in shape)
    return events


def workloads(n, levels, kind):
    target = [[c % levels for c in range(n)] for _ in range(n)]
    old = [[(h+1) % levels for h in row] for row in target]
    if kind == 'uniform':
        target = [[levels-1]*n for _ in range(n)]; old = [[0]*n for _ in range(n)]
    if kind == 'local':
        old = [[0]*n for _ in range(n)]; target = [[0]*n for _ in range(n)]
        for r in range(5):
            for c in range(5):target[r][c] = 1+c % (levels-1)
    if kind == 'unchanged': old = [row[:] for row in target]
    return old,target


def account(old,target):
    commands, levels = masks(old,target)
    # Skip empty masks and untouched rows; no padding to a full scan.
    row_writes = sum(len({r for r,c in mask}) for mask in commands)
    changed = len(commands[0])
    return dict(changed=changed, destination_levels=len(levels),
                command_events=sum(bool(m) for m in commands),row_writes=row_writes,
                # Two physically independent arrays serially written; ideal parallel
                # dual writers or one reused mask pay only row_writes, but hardware differs.
                serial_dual_row_writes=2*row_writes,
                selected_site_commands=sum(map(len,commands)),state_events=replay(old,target))


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
        replay([old],[new]);cases+=1
    try:replay([[0]],[[1]],skip_pawl_proof=True)
    except AssertionError as exc:assert str(exc)=='unsupported cell'
    else:raise AssertionError('missed failed support handoff')
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
        assert row['row_writes']==80*(1+min(H,80))
        assert row['selected_site_commands']==12800
    assert account(*workloads(80,5,'unchanged'))['row_writes']==0
    return dict(exhaustive_two_cell_maps=cases,injected_handoff_failure='caught')


def main():
    checked=verification()
    opt=trip.optimum_section(.1,.1)
    drive=trip.driven_force(opt['d'],.1,.4,.8,.1,.1,r=opt['r'])
    stroke=drive['driver_travel_bound']
    # This is E-079's CHOSEN sufficient travel, not a necessary minimum over mechanisms.
    scenarios=[]
    for H in (2,5,9,21):
        for kind in ('mixed','uniform','local'):
            counts=account(*workloads(80,H,kind));n=counts['row_writes']
            scenarios.append(dict(levels=H,kind=kind,**counts,
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
            return_only_5level_s=480*leg,return_only_21level_s=1760*leg))
    print(json.dumps(dict(checks=checked,stroke_policy=drive,scenarios=scenarios,
        return_force_mass_cases=mass_cases,
        inventory=dict(one_array_command_memories=6400,two_array_command_memories=12800,
            one_array_shutter_apertures=12800,two_array_shutter_apertures=25600,
            row_local_writer_pins_per_array=80,persistent_output_states_per_cell=3,
            one_array_magnetic_reversible_lines=160,two_array_magnetic_reversible_lines=320),
        # Residual allowances, NOT quotes. Other contains all other purchased hardware.
        cost_allowances=[dict(other_usd=b,per_site_one_item=(500-b)/6400,
            per_site_two_items=(500-b)/12800) for b in (200,250,400)],
        readback_opportunities=dict(note='At least two critical support observations per changed cell',
            full_board=12800,union_bound_coeff=12800),
        sensitivity=dict(one_ms_per_row_5level_s=.480,one_ms_per_row_21level_s=1.760)),indent=2))

if __name__ == '__main__':main()
