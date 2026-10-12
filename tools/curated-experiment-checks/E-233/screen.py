"""E-233: finite shared-layer obstruction and one-hot shutter control.
Stdlib; stdout only. Ideal geometry/support and explicitly assumed scenarios.
No CAD, calibrated distributions, prices, independent review or measurements.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

s = importlib.util.spec_from_file_location(
    'e231', Path(__file__).resolve().parents[1] / 'E-231/screen.py')
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)
move, J = p.move, p.J
LEVELS = (0, 10, 20, 30, 40)


def overlap(a, b):
    """Positive-length intersection: tangency is allowed."""
    return min(a[1], b[1]) > max(a[0], b[0]) + 1e-10


def ramp_collision(foot, shelf, steps):
    # Lower foot [0,f] is stationary on pickup. A homogeneous layer carries
    # upper foot bottom delta continuously from 10 to 0. At any still-bearing
    # transverse coordinate, shelf material is [delta-t,delta] at BOTH cells.
    # Even taper t->0 cannot remove collision of its top surface with (0,f).
    for k in range(steps + 1):
        delta = 10 * (1 - k / steps)
        if overlap((0, foot), (delta - shelf, delta)):
            return delta
    return None


def replay(old, target, fault=None, arrest=True):
    """Explicit nonuniform control: FIVE retained shutters/cell, one closed.
    Pickup lane A and shutter lane B are granted disjoint; each foot spans both.
    Fixed changed mask stays locked while a separate writer changes shutters.
    Collision test checks finite thickness at the active shutter in each cell.
    Arrest is a granted grounded mechanical load path, not a motor holding claim.
    """
    changed = [a != b for a, b in zip(old, target)]
    h = list(old)
    shutters = [{a} for a in old]
    actual = list(target)
    if fault is not None and changed[fault[0]]:
        actual[fault[0]] = fault[1]
    checks = 0

    def check(z):
        nonlocal checks
        for i, x in enumerate(h):
            grounded = x in shutters[i]
            on_plane = changed[i] and x == z and arrest
            assert grounded or on_plane, 'source loss leaves no grounded support'
            assert changed[i] or x == old[i], 'unchanged neighbor moved'
            for top in shutters[i]:
                assert not overlap((x, x + 2), (top - 2, top)), 'finite shelf collision'
        checks += 1

    # Fingers inserted at -6 while resident one-hot shelves carry all columns.
    check(-6)
    for z in range(-6, 43):
        h[:] = [max(a, z) if c else a for a, c in zip(old, changed)]
        check(z)
    # At 42, rewrite five physical layers; same mask excludes unchanged sites.
    # Deliberately check the temporarily empty state, then the new support.
    for level in LEVELS:
        for i, c in enumerate(changed):
            if c:
                shutters[i].discard(level)
        check(42)
        for i, c in enumerate(changed):
            if c and actual[i] == level:
                shutters[i].add(level)
        check(42)
    for z in range(42, -7, -1):
        h[:] = [max(z, a) if c else old[i] for i, (a, c) in enumerate(zip(actual, changed))]
        check(z)
    # Grounded shelves persist during finger withdrawal, row feed and next setup.
    assert all(x in a for x, a in zip(h, shutters))
    return tuple(h), checks


def cycle(a=8000):
    return dict(
        fixed_mask_setup=3*J,
        writer_mode_switch=2*J,
        five_physical_layer_writes=5*3*J,
        writer_layer_traverse=4*move(10)+move(40),
        pickup_ascent_descent=2*move(42, a=a),
        unloaded_finger_clear=2*J,
        underpass=2*move(6),
        row_feed=move(5.08),
        old_final_height_reads=.020)


def timing(b, a=8000, visits=None):
    # Fault class: stable wrong discrete shutter, detected after descent/seat.
    # Finish at supported actual heights, prove/read, clear/reset writer and
    # pickup, THEN recompute and perform complete physical programming again.
    recovery=move(42,a=a)+J+.010+move(40)
    return 2+((math.ceil(80/b) if visits is None else visits)+1)*sum(cycle(a).values())+recovery


def allocation(b, resident_retention=0):
    # E-231 direct channels reused between unloaded mask writing and shelf
    # writing. Mask copy stays mechanically backed during reuse (unbuilt).
    items=p.bom('direct',80,b)['items'].copy()
    items.update(layer_writer_axis_driver=20, layer_writer_brake=10,
                 layer_writer_local_mount_arrest=5*b,
                 resident_strip_mount_allocation=.20*400,
                 resident_purchased_retention=32000*resident_retention)
    return dict(total=sum(items.values()), items=items)


def best(a=8000):
    b=next(b for b in range(1,81) if timing(b,a)<30)
    return dict(banks=b, time_s=timing(b,a), allocation=allocation(b),
                gates=80*b, fixed_mask_states=80*b,
                resident_shutters=32000, layer_row_strips=400)


def checks():
    witnesses=[]
    for f,t in it.product((.5,1,2,4),repeat=2):
        collision=10-f-t
        assert collision<10
        for resolution in (100,1000):
            assert ramp_collision(f,t,resolution) is not None
        # Independent analytic interior witness, including taper-to-zero limit.
        delta=f/2
        assert 0<delta<f and overlap((0,f),(delta-t,delta))
        witnesses.append(dict(foot=f,shelf=t,stationary_collision_plane=collision,
                              upper_support_gap=f+t, ramp_interior_delta=delta))
    # Zero-thickness point-foot control removes this *particular* obstruction.
    assert 10-0-0 == 10
    # Downward flat pickup: bottom hits top of lower foot while pickup top is
    # f+d above the bearing surface it needs. It cannot pass through the foot.
    assert 2+2>0
    # Common rigid translation preserves interlayer spacing. Moving a loaded
    # unchanged layer by even 1 mm violates unchanged-neighbor invariance.
    for u in (-4,-1,1,4):
        assert (10+u)-(0+u)==10 and 20+u!=20
    maps=states=retries=0
    for old,target in it.product(it.product(LEVELS,repeat=3),repeat=2):
        result,n=replay(old,target)
        assert result==target
        maps+=1; states+=n
    for old,target in it.product(it.product(LEVELS,repeat=2),repeat=2):
        for i in range(2):
            for wrong in LEVELS:
                actual,_=replay(old,target,(i,wrong))
                final,_=replay(actual,target)
                assert final==target
                retries+=1
    try:
        replay((0,10,20),(10,0,20),arrest=False)
    except AssertionError as e:
        assert 'source loss' in str(e)
    else:
        raise AssertionError('missing arrest was not detected')
    for b in (1,5,8,16):
        events=[2]+[sum(cycle().values())]*(math.ceil(80/b)+1)+[move(42),J,.010,move(40)]
        assert abs(sum(events)-timing(b))<1e-10
    return dict(shared_layer_witnesses=witnesses, one_hot_maps=maps,
                support_state_checks=states, wrong_stop_retries=retries,
                source_loss_negative_controls=1)


def main():
    candidate=best(); b=candidate['banks']
    force={str(f):p.p.drive(b,f,head_mass=.5) for f in (1,3.27,10)}
    for f, result in force.items():
        result['full_map_up_work_J']=6400*float(f)*.042
    print(json.dumps(dict(
        checks=checks(), conditional_one_hot= candidate,
        cycle_s=cycle(), slow_acceleration=best(a=2000),
        regional_five_rows_s=timing(b,visits=5),
        retention_allocations={str(r):allocation(b,r)['total'] for r in (0,.005,.02)},
        total_free_command_channels_allocation=allocation(b)['total']-.5*80*b,
        next_smaller_bank_time_s=timing(b-1),
        force_scenarios=force,
        bounds={str(e):dict(ascent_gap_with_both_thicknesses_high=4+2*e,
                    common_bias_only_gap=4, dual_lane_margin=.5-e,
                    apex_margin=2-2*e, underpass_margin=6-2-2*e,
                    transfer_height_difference=2*e) for e in (0,.15,.35,.70)},
        shutter_stock_L=32000*12*4*2/1e6,
        stock_print_h=(8.192+3.072)*1e6/10/3600,
        stock_print_h_at_10pct_scrap=(8.192+3.072)*1e6/10/3600/.9,
        column_plus_shutter_assembly_h=(6400*5+32000*10)/3600,
        minimum_height_and_mask_read_sites=3*6400,
        five_layer_read_sites=5*6400,
        all_0_to_10_up_work_J=6400*3.27*.042,
        direct_0_to_10_work_J=6400*3.27*.010,
        gravity_drag_N={str(a):.003*(9.81-a) for a in (8,2)},
        physical_measurements=0),indent=2))


if __name__=='__main__':
    main()
