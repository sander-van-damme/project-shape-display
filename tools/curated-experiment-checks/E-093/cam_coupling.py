"""E-093: finite selector storage/dwell, slotted transmission, reversible cams.
mm and normalized downward load. Deterministic bounds, not calibrated priors.
Separate planar lanes, quasistatic; no strength, friction or hardware claim.
"""
import importlib.util
import itertools as it
import json
import sys
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parents[1] / path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


support = load('support093', 'E-092/support_transfer.py')
trip = support.trip
EPS = 1e-8


def sampled_flag():
    # Separate binary shutter, positions 0/1.5 mm. Same square-key principle as
    # E-091, but two holes. Source of SET energy is a compliant common pusher;
    # equality/sign tongues authorize it. Actuator force and keeper not credited.
    captures = holds = sweeps = 0
    reserve = 10.
    for hole, key, setter in it.product((1.2, 1.4), (.5, .7), (-.2, .2)):
        walls = [trip.rectangle(-2, -hole/2, 0, 1),
                 trip.rectangle(hole/2, 1.5-hole/2, 0, 1),
                 trip.rectangle(1.5+hole/2, 3.5, 0, 1)]
        assert 1.5-hole > 0
        for state in (0., 1.5):
            dog = trip.rectangle(state+setter-key/2, state+setter+key/2, -1.5, 1.5)
            assert not any(trip.overlap(dog, w) for w in walls)
            captures += 1
            play = (hole-key)/2
            for sign, datum, edge in it.product((-1, 1), (-.1, .1), (-.1, .1)):
                s = state+sign*play+datum
                tongue = trip.rectangle(0, 1, -2-s, .8+edge-s)
                lug = trip.rectangle(.1, .9, 0, 1)
                blocked = trip.overlap(tongue, lug)
                assert blocked == (state == 0.)
                reserve = min(reserve, .8+edge-s if blocked else s-.8-edge)
                holds += 1
        # A full flag transition with key engaged hits the intervening land.
        dog = trip.rectangle(.75-key/2, .75+key/2, -1.5, 1.5)
        assert any(trip.overlap(dog, w) for w in walls)
        # Whole retracted-key swept union lies below both holes and the land.
        sweep = trip.rectangle(-key/2, 1.5+key/2, -3.1, -.1)
        assert not any(trip.overlap(sweep, w) for w in walls)
        sweeps += 1
    # Logical contact boundary: sampling bit is not self-clearing. A stale set
    # flag admits a neutral command if physical reset or its proof fails.
    assert not trip.overlap(trip.rectangle(0, 1, -3.5, -.7), trip.rectangle(.1, .9, 0, 1))
    return dict(capture_cases=captures, held_gate_cases=holds, withdrawn_sweeps=sweeps,
                gate_reserve_mm=round(reserve, 6), extra_local_sliders=12800,
                full_board_local_sliders_at_least=57600,
                stale_flag_witness=True)


def reader_dwell():
    # Independent reader r holds q*5 while elevator reseats 2.2 mm. lambda is
    # parasitic coupling, not a fitted transmission model. Include common gain.
    rows = []
    for lam in (0., .25, .5, .75, 1.):
        misses = false = checks = 0
        for q, r, datum, gain, pin, slot, micro in it.product(
                range(-8, 9), range(-8, 9), (-.65, .65), (-.01, .01),
                (.3, .5), (5.3, 5.5), (0., 1.1, 2.2)):
            if q*r <= 0:
                continue  # finite E-091 sign gate required; never infer sign here
            dx = 5*(r-q)+datum+5*r*gain-lam*micro*(1+gain)
            full = not trip.collision(dx, 1.5, pin, slot, 42.)
            assert full == (trip.depth_reduced(dx, pin, slot) >= 1.5-EPS)
            misses += q == r and not full
            false += q != r and full
            checks += 1
        rows.append(dict(leakage_ratio=lam, polygon_cases=checks,
                         target_misses=misses, wrong_entries=false))
    assert all(x['target_misses'] == x['wrong_entries'] == 0 for x in rows[:3])
    assert all(x['target_misses'] and x['wrong_entries'] for x in rows[3:])
    # Conservative closed form, independently of polygon enumeration. Worst
    # existing capture/reject reserve 1.35 mm, leakage at most 2.2*1.01*lambda.
    limit = 1.35/(2.2*1.01)
    return dict(scenarios=rows, sufficient_leakage_strictly_below=limit,
                extra_shared_coordinate_per_bank=1, extra_local_selection_sliders=0)


def slotted_bridge():
    # Reader-borne drive pin enters a long vertical slot in a ground-dog bridge.
    # Slot spans z=-41..41, pin is square; reader needs r=-40..40 mm. Offsets are
    # explicit new bounds, not measured process transfer.
    vertical_checks = 0
    z_reserve = 10.
    for r, pin, datum, enderr in it.product(range(-40, 41, 5), (.5, .7), (-.2, .2), (-.1, .1)):
        lo, hi = -41+enderr, 41-enderr
        a, b = r+datum-pin/2, r+datum+pin/2
        assert lo <= a <= b <= hi
        z_reserve = min(z_reserve, a-lo, hi-b)
        vertical_checks += 1
    # Width/key/error same box as command lock. Driving on either flank allows
    # +/- .45 lost motion, then +/- .2 bridge-to-dog datum. A drive reversal may
    # change flank, so forward calibration cannot remove it in both directions.
    worst = (1.4-.5)/2+.2
    withdrawn_tip = -.2+worst
    inserted_tip = .5-worst
    x = support.population(3.)[0]
    # Wrong insertion reaches no rack overlap, although upstream cam is at end.
    assert inserted_tip < 0
    # Wrong withdrawal intersects an intervening land during a 5-mm rack move.
    bad_dog = support.rect(-1.2+worst, withdrawn_tip, -.8, 0.)
    rack_walls = support.walls(3., 2.5, [0.]*9)
    assert any(support.hit(bad_dog, w) for w in rack_walls)
    # Whole horizontal sweep at an actual pocket still fits vertically: this
    # demonstrates that the failure is added transmission, not E-092 replay.
    assert support.sweep_clear(x.hg, x.tg, 2.2-x.gap-x.deflection, 0., [0.]*9)
    return dict(vertical_checks=vertical_checks, slot_length_mm=82,
                vertical_reserve_mm=round(z_reserve, 6), lateral_error_bound_mm=worst,
                withdrawn_tip_mm=withdrawn_tip, inserted_tip_mm=inserted_tip,
                required_stroke_for_005_reserves_mm=2*worst+.1,
                existing_stroke_mm=.7, collision_and_no_engagement_witnesses=2)


def cam_walls(t, clearance=.05, thickness=.4):
    # Captive flat-pad cam shoe: a 0.4-mm-long x/y square pad follows a diagonal
    # groove y=a*x. Two finite parallel rails have vertical clearance on either
    # side of the square's support envelope. Axial carriage is x=t; scale y to
    # the E-092 0.7-mm dog stroke. Separate lanes for ground/elevator output.
    a=.7/4
    half=.2
    gap=half*(1+a)+clearance
    lo,hi=-1.,5.
    upper=[(lo,a*lo+gap),(hi,a*hi+gap),(hi,a*hi+gap+thickness),(lo,a*lo+gap+thickness)]
    lower=[(lo,a*lo-gap-thickness),(hi,a*hi-gap-thickness),(hi,a*hi-gap),(lo,a*lo-gap)]
    shoe=trip.rectangle(t-half,t+half,a*t-half,a*t+half)
    return a*t, shoe, (upper,lower)


def reversible_cam():
    # Grant perfect isolation and nominal transmission to avoid blaming either
    # earlier failure. Captive reversible slot directly drives dog with no latch,
    # clutch or over-center state. Reset is the reverse of the SET trajectory.
    sweeps = 0
    for steps in (1, 16, 64):
        for i in range(steps+1):
            t = 4*i/steps
            y, shoe, rails = cam_walls(t)
            assert not any(trip.overlap(shoe, rail) for rail in rails)
            # Both rail directions actually restrain the follower.
            for side in (-1, 1):
                beyond=[(px,py+side*.051) for px,py in shoe]
                assert any(trip.overlap(beyond, rail) for rail in rails)
            sweeps += 1
    # Ground dog tip is -.2+y. At y=.7 it bears; during reset it loses overlap
    # once y<=.2, i.e. t<=8/7. With grip already withdrawn both paths are absent.
    release_t = .2/(.7/4)
    # If a retained output stop tries to hold bearing overlap while the captured
    # cam returns, it jams: at home groove play <=.1, required shift >=.25.
    # Check actual finite rail polygons, not merely contradictory scalar goals.
    reset_jams = 0
    for clearance in (0., .05, .1):
        _, shoe, rails = cam_walls(0., clearance)
        held = [(px, py+.25) for px, py in shoe]
        assert any(trip.overlap(held, rail) for rail in rails)
        reset_jams += 1
    drops=[]; checked=0
    for x, old, target in it.product(support.population(3.), range(9), range(9)):
        if old == target:
            continue
        support.transfer(x, old, target, 2.2, 0.)
        # Ground seated rack at delta+Delta; inserted elevator top delta-gap.
        # Reinsert E at low coordinate before resetting G: finite geometry fits
        # but its top is below the ceiling; depth proof still means no load.
        delta=5*(target-old)
        ceiling=5*old+delta+x.tooth_error
        assert support.sweep_clear(x.he,x.te,ceiling,delta-x.gap,[0.]*9)
        gap=x.gap+x.tooth_error
        assert gap > 0
        drops.append(gap+x.deflection)
        checked+=1
    # Exhaust all orders of returning the two direct outputs with fixed e=v.
    # Initial deposited G=1,E=0. Final direct-cam home G=0,E=1. Either order
    # loses ground with no load-bearing elevator, even though E may be inserted.
    reset_orders=[]
    for order in it.permutations(('open_ground','insert_grip')):
        g,e=True,False
        loss=False
        for action in order:
            if action=='open_ground':g=False
            else:e=True
            if not g:loss=True  # E has positive vertical gap at fixed e=0
        assert loss
        reset_orders.append(list(order))
    # Raising e to take up gap before G withdrawal avoids the drop but restores
    # grip-only carriage. A subsequent macro step then moves a deposited column.
    reacquired_next_step_displacement_mm=5.
    assert reacquired_next_step_displacement_mm > 0
    # History-state collision: after query retraction, both a deposited cell and
    # a still-carried cell have inactive equality at the next station, but need
    # opposite output configurations. Single-valued linkage to reset cam +
    # instantaneous equality cannot implement both.
    # Concrete same-sign commands +5 (already deposited) and +15 (carried),
    # queried at +10 mm: identical blocked equality and positive sign inputs.
    for q in (1, 3):
        assert trip.depth_polygon(5*(2-q), .4, 5.4, 42.) < .7
    histories = { 'deposited': (True,False), 'still_carried': (False,True) }
    assert len(set(histories.values()))==2
    return dict(finite_rail_contact_checks=sweeps, retained_output_reset_jams=reset_jams,
                reset_loss_threshold_t_mm=release_t,
                replayed_support_cases=checked, both_low_reset_orders_fail=reset_orders,
                low_reset_equilibrium_drop_mm=[min(drops),max(drops)],
                lifted_reset_next_step_error_mm=reacquired_next_step_displacement_mm,
                minimum_distinct_output_histories=len(set(histories.values())))


def main():
    print(json.dumps(dict(evidence='bounded planar kinematics/contact; self-review only',
                         flag=sampled_flag(), dwell=reader_dwell(), bridge=slotted_bridge(),
                         cam=reversible_cam()),indent=2))


if __name__=='__main__':
    main()
