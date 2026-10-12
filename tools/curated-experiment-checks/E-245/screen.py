"""E-245: collective smooth-pin support. Assumed bounds, not hardware evidence.
Stdlib, stdout only. Coulomb/Winkler and ideal support models, no contact FEA.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e236', Path(__file__).resolve().parents[1] / 'E-236' / 'screen.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
move = prior.move
SEQ = (-2, -1, 3, -1, 1)
TABLE = prior.codes(SEQ, 6)


def replay(old, target, fault=None):
    """Active row plus two unchanged rows sharing column clamps.
    Binary support means an independently adequate friction capacity is GRANTED.
    Source loss requires frozen grips, closed keepers and local elevator arrest.
    """
    n = len(old)
    h = [list(old), [(2*c)%5 for c in range(n)], [(4+2*c)%5 for c in range(n)]]
    initial = [r[:] for r in h]
    row = [True]*3
    col = [True]*n
    grip = [False]*n
    codes = [TABLE[a, b][2] for a, b in zip(old, target)]
    observations = 0

    def check():
        nonlocal observations
        for r, c in it.product(range(3), range(n)):
            assert row[r] or col[c] or (r == 0 and grip[c]), 'unsupported'
            assert 0 <= h[r][c] <= 4
            if r != 0 or old[c] == target[c]:
                assert h[r][c] == initial[r][c], 'unchanged moved'
            observations += 1

    check()
    for j, d in enumerate(SEQ):
        assert all(row) and all(col) and not any(grip), 'unsafe overwrite'
        mask = [bool(code[j]) for code in codes]
        grip[:] = mask
        check()
        row[0] = False
        col[:] = [not on for on in mask]
        if fault == 'lost_grip':
            grip[:] = [False]*n
        if fault == 'open_idle_row':
            row[1] = False
        check()
        if fault == 'active_erase':
            grip[:] = [False]*n
            check()
        # Three interior observations add no physical dynamics; linear motion
        # is bounded by the endpoints and all selected pins are gripped.
        start = h[0][:]
        for fraction in (.25, .5, .75, 1.):
            h[0][:] = [x+fraction*d*on for x, on in zip(start, mask)]
            check()
        row[0] = True
        col[:] = [True]*n
        check()
        grip[:] = [False]*n
        check()
    assert h[0] == list(target)
    return observations


def pad(e, k, load=1., mu=.15, safety=1.5, clear=.2, area=25.6):
    """Two opposed faces; each face N=k*max(0,u-error) N, errors in [-e,e].
    k is effective per-face N/mm; u is each face's compression at zero error,
    not the total opposed-jaw gap change.
    Model grants independent local compliance within a continuous strip.
    """
    required = safety*load
    u = e+required/(2*mu*k)
    max_compression = u+e
    # 40 thick and 40 thin pins: coherent half-row/module offsets, not IID.
    errors = [-e]*40+[e]*40
    face = [k*max(0., u-x) for x in errors]
    assert math.isclose(min(2*mu*n for n in face), required)
    one_face_work = sum(.5*k*max(0., u-x)**2 for x in errors)/1000
    return dict(e_mm=e, k_N_mm=k, load_N=load, mu=mu,
                per_face_nominal_compression_mm=u,
                max_compression_mm=max_compression,
                per_jaw_release_stroke_mm=max_compression+clear,
                row_one_face_force_N=sum(face),
                all_thick_row_one_face_force_N=80*max(face),
                max_contact_pressure_MPa=max(face)/area,
                row_two_face_elastic_energy_J=2*one_face_work,
                min_capacity_N=min(2*mu*n for n in face),
                max_capacity_N=max(2*mu*n for n in face))


def timeline(stroke, banks, rows=None, grip_stroke=None):
    # Four separate stages: moving grip closes/proves, resident clamps open,
    # resident clamps close/prove, moving grip opens. Each stage favorably grants
    # simultaneous opposed-jaw and row/column motion; no actuator constructed.
    grip_stroke = stroke if grip_stroke is None else grip_stroke
    stages = [move(grip_stroke)+.003, move(stroke)+.003,
              move(stroke)+.003, move(grip_stroke)+.003]
    write = move(2)+.003  # retained 80-bit parallel writer, inherited allocation
    service = sum(move(10*abs(d)) for d in SEQ)+5*(sum(stages)+write)+move(5.08)
    visits = math.ceil(80/banks) if rows is None else rows
    t = 2+move(30)+.010+(visits+1)*service
    events = [2, move(30), .010]
    for _ in range(visits+1):
        for d in SEQ:
            events += [write]+stages[:2]+[move(10*abs(d))]+stages[2:]
        events += [move(5.08)]
    assert math.isclose(sum(events), t)
    return dict(banks=banks, seconds=t, service_s=service,
                allocation_before_pads_usd=195+20*banks+.52*80*banks)


def coupled(c):
    # load_N is TOTAL supported static weight, not additional mass plus weight.
    # Grant no other axial drag; 8 m/s2 ascent/braking needs W*(1+a/g).
    grip = pad(c['e_mm'], c['k_N_mm'], c['load_N']*(1+8/9.81), c['mu'])
    s, gs = c['per_jaw_release_stroke_mm'], grip['per_jaw_release_stroke_mm']
    b = next(b for b in range(1, 81) if timeline(s, b, grip_stroke=gs)['seconds'] < 30)
    return grip, timeline(s, b, grip_stroke=gs)


def main():
    maps = observations = 0
    for old, target in it.product(it.product(range(5), repeat=3), repeat=2):
        observations += replay(old, target)
        maps += 1
    for fault in ('lost_grip', 'open_idle_row', 'active_erase'):
        try:
            replay((0, 4, 2), (4, 0, 2), fault)
        except AssertionError:
            pass
        else:
            raise AssertionError('fault escaped '+fault)
    retries = 0
    for (_, target), entry in TABLE.items():
        for actual in entry[3]:
            replay((actual, 1, 3), (target, 1, 3))
            retries += 1
    full_row_observations = 0
    for old_height, target_height in it.product(range(5), repeat=2):
        old = [c%5 for c in range(80)]
        old[39] = old_height
        target = old[:]
        target[39] = target_height
        full_row_observations += replay(old, target)
    # Tangential load sharing is distinct from pad NORMAL stiffness. Two equal
    # linear shear springs support L at L/(2kt); removing one adds L/(2kt).
    # This is a no-slip compliant counterexample, not a physical displacement cap.
    neighbor_shift = [dict(load_N=f, tangential_stiffness_N_mm=kt,
                           transfer_displacement_mm=f/(2*kt))
                      for f, kt in it.product((.2,1.,10.),(1.,10.,100.))]

    cases = [pad(e, k, f, mu) for e, k, f, mu in it.product(
        (.05, .15, .35, .70), (2., 20., 200.), (.2, 1., 10.), (.1, .15, .3))]
    # No material inference: eta is a granted usable compressive strain, with
    # pad thickness limited by one concrete same-plane cell section.
    tmax = (5.08-3.2-.8)/2  # .8 mm combined backer allocation per pitch
    sweep = []
    for c in cases:
        grip, sched = coupled(c)
        for eta in (.1, .3, .5):
            pack = max(c['max_compression_mm'], grip['max_compression_mm']) <= eta*tmax
            sweep.append(dict(**c, **sched, eta=eta, pad_pack=pack))

    nominal = pad(.35, 20)
    # Independent elastic integral: midpoint sum exact for affine force.
    for e in (-.35, .35):
        comp = nominal['per_face_nominal_compression_mm']-e
        numerical = sum(20*(j+.5)*comp/1000*comp/1000 for j in range(1000))
        assert math.isclose(numerical, .5*20*comp**2)
    # A force-only controller can reach its total target while a thin pin has
    # no contact. 40 thick and 40 thin under u=0, k20, e=.35.
    capacities = [2*.15*20*max(0, -e) for e in [-.35]*40+[.35]*40]
    assert sum(capacities) > 80*.2 and sum(x == 0 for x in capacities) == 40
    # If residual normal remains, a pad can silently defeat gravity following.
    assert 2*.15*.1 > .003*9.81

    # Pressure membrane oracle: no stiffness-dependent force amplification.
    p = 1.5/(2*.15*25.6)  # N/mm2 = MPa; membrane tension/backing not modelled
    # Series spacers: common width bias accumulates from centered end datums.
    series = [dict(width_bias_mm=b, end_takeup_mm=80*b,
                   edge_pin_displacement_mm=39.5*b,
                   optimistic_lateral_allowance_mm=(5.08-3.2)/2)
              for b in (.05, .15, .35)]
    # Two faces at each row + column site, 8-mm high and 3.2-mm wide.
    pad_litres_per_mm = 12800*2*25.6/1e6
    representative = []
    for e, k in ((.05, 20), (.15, 20), (.35, 2), (.35, 20), (.35, 200), (.70, 20)):
        c = pad(e, k)
        grip, sched = coupled(c)
        representative.append(dict(**c, **sched,
            grip_stroke_mm=grip['per_jaw_release_stroke_mm']))
    # Compressed pads in two resident planes + moving pickup. At full duty all
    # column strips in B4 cycle plus active row strips and all selected pickups.
    # This is a conservative event envelope, not average miniature loading.
    moving_grip, nominal_schedule = coupled(nominal)
    work = nominal['row_two_face_elastic_energy_J']*(80+4)+4*moving_grip['row_two_face_elastic_energy_J']
    # A realizable full-board 40->0 workload has exactly three active masks.
    # Twenty serviced rows/head. This work omits retry and grants perfect load
    # retention; no arbitrary all-on-five-times workload is invented.
    assert TABLE[4, 0][2] == (1, 1, 0, 1, 0)
    actual_work = work*20*3
    resident_close_work = nominal['row_two_face_elastic_energy_J']*(80+4)
    grip_force = moving_grip['min_capacity_N']
    stem_volume = 6400*3.2**2*116/1e6
    print(json.dumps(dict(checks=dict(maps=maps, support_observations=observations,
        partial_retries=retries, injected_faults=3,
        full_80_cell_single_change_maps=25, full_row_observations=full_row_observations),
        unchanged_compliance_counterexamples=neighbor_shift,
        nominal=nominal, moving_grip=moving_grip, representative=representative,
        joint_sweep=dict(cases=len(sweep),
            same_plane_and_time_and_prepad_cost_survivors=sum(
                s['pad_pack'] and s['allocation_before_pads_usd']<500 for s in sweep),
            surviving_error_bounds=sorted(set(s['e_mm'] for s in sweep if
                s['pad_pack'] and s['allocation_before_pads_usd']<500))),
        same_plane_max_pad_thickness_mm=tmax,
        force_only_witness=dict(zero_contact_cells=40,
            summed_capacity_N=sum(capacities), row_test_load_N=16),
        pressure_oracle=dict(MPa=p, row_one_face_N=80*p*25.6,
            displacement_range_mm=.7, retained_pressure_zones_B4=80+320),
        series_spacers=series,
        pad_stock=dict(litres_per_mm_thickness=pad_litres_per_mm,
            two_mm_litres=2*pad_litres_per_mm,
            two_mm_raw_cost_at_20_60_100_usd_L=[2*pad_litres_per_mm*c for c in (20,60,100)]),
        full_duty_B4=dict(elastic_work_per_pulse_J=work,
            all_on_five_pulse_envelope_with_retry_J=work*105,
            all_40_to_0_elastic_work_without_retry_J=actual_work,
            resident_closure_mean_mechanical_W=resident_close_work/move(
                nominal['per_jaw_release_stroke_mm']),
            grip_capacity_N=grip_force,
            all_thick_column_one_face_force_N=80*nominal['all_thick_row_one_face_force_N']),
        direct_2mm_control=timeline(2,5),
        regional_five_rows=timeline(nominal['per_jaw_release_stroke_mm'],4,rows=5,
            grip_stroke=moving_grip['per_jaw_release_stroke_mm']),
        manufacture=dict(stem_litres=stem_volume,
            stem_mass_g=3.2**2*116*.00125,
            stem_print_hours_15_5_mm3_s_10pct_scrap=[stem_volume*1e6/r/3600/.9 for r in (15,5)],
            column_insert_hours_5_15_s=[6400*t/3600 for t in (5,15)],
            strip_placement_hours_10_30_s=[800*t/3600 for t in (10,30)])), indent=2))


if __name__ == '__main__':
    main()
