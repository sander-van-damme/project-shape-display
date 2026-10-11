#!/usr/bin/env python3
"""E-157: SI-unit ideal topology, energy and bounded-scenario witnesses.
No seal/contact constitutive law or manufacturing probability is claimed.
Run with Python >=3.9; stdout is disposable JSON.
"""
import json
import math
from itertools import product

PI = math.pi
AP = PI * (0.002 / 2)**2
AT = PI * (0.001 / 2)**2
R = 0.010
N = 3
KQ = AT * R  # m^3/rad; homogenized ideal rotary displacement
H = 0.040


def close(a, b, tol=1e-11):
    assert abs(a-b) <= tol * max(1., abs(a), abs(b)), (a, b)


def components(closed):
    """Linear source--pocket--chamber graph; two point occlusions."""
    edges = [(0, 1), (1, 2)]
    reached = {2}
    while True:
        old = set(reached)
        for i, (a, b) in enumerate(edges):
            if not closed[i] and (a in reached or b in reached):
                reached.update((a, b))
        if old == reached:
            return sorted(reached)


def coverage(n, beta, edge_error=0., missing=()):
    """Exact closed angular intervals, plus independent midpoint enumeration.
    beta: full-occlusion arc, excluding unspecified entry/exit ramps.
    Adverse error removes edge_error from each end. Intervals on a circle.
    """
    period = 2*PI
    width = max(0., beta-2*edge_error)
    intervals = []
    for j in range(n):
        if j in missing:
            continue
        start = (-j*period/n+edge_error) % period
        end = start+width
        if end <= period:
            intervals.append((start, end))
        else:
            intervals.extend(((start, period), (0., end-period)))
    cuts = sorted(set([0., period]+[v for it in intervals for v in it]))
    counts = []
    uncovered = 0.
    for a, b in zip(cuts, cuts[1:]):
        mid = (a+b)/2
        count = sum(lo <= mid <= hi for lo, hi in intervals)
        counts.append(count)
        if count == 0:
            uncovered += b-a
    if not missing:
        analytic = n*max(0., period/n-width)
        close(uncovered, analytic)
    return dict(min_closed=min(counts), max_closed=max(counts),
                open_degrees=math.degrees(uncovered))


def sampled_race_coverage(samples, wall_error=0., gap_error=0., missing=()):
    """Generated radial section: 10-mm orbit, 2-mm rollers, 12.9-mm race.
    Full nominal bed 200 degrees. Linear 0.02 mm/degree exit/entry relief.
    Full closure is idealized at gap < twice the wall thickness.
    This checks actual defined gap through rotation, not real tube contact.
    """
    minimum = 3
    for i in range(samples):
        phase = 2*PI*(i+.5)/samples
        count = 0
        for j in range(3):
            if j in missing:
                continue
            a = (phase+j*2*PI/3+PI) % (2*PI)-PI
            relief = max(0., abs(math.degrees(a))-100.)*.00002
            race_radius = .0129+relief+gap_error
            gap = race_radius-(R+.002)
            if gap < 2*(.0005+wall_error)-1e-12:
                count += 1
        minimum = min(minimum,count)
    return minimum


def rotation(theta, omega, t, force, inertia):
    """Exact zero-loss/U0=0 limiting trajectory after drive disconnection."""
    torque = force/AP*KQ
    acc = -torque/inertia
    end = theta+omega*t+0.5*acc*t*t
    speed = omega+acc*t
    dh = KQ/AP*(end-theta)
    dkin = .5*inertia*(speed*speed-omega*omega)
    close(dkin+force*dh, 0., 1e-12)
    return dict(delta_height_mm=dh*1e3, omega_final=speed,
                energy_residual_J=dkin+force*dh)


def potential(theta, force, u0):
    return force/AP*KQ*theta+u0*(1-math.cos(N*theta))


def barrier(force, u0):
    """Exact backward barrier in a tilted sinusoidal tube-energy scenario.
    Torque convention: J*theta_ddot = -p*KQ - N*U0*sin(N*theta).
    No claim this U(theta) describes a particular tube.
    """
    torque = force/AP*KQ
    if u0 == 0 or torque >= N*u0:
        return dict(stable=False, barrier_mJ=0.)
    a = math.asin(torque/(N*u0))
    minimum = -a/N
    maximum_left = (-PI+a)/N
    b = potential(maximum_left, force, u0)-potential(minimum, force, u0)
    assert b >= -1e-14
    if force == 0:
        close(b, 2*u0)
    return dict(stable=True, barrier_mJ=b*1e3,
                equilibrium_height_mm=minimum*KQ/AP*1e3)


def packet(volume, bulk, initial, final, reopening=0.):
    """Linear compliance; moving constant-load output, isolated source.
    Linear pressure strain restriction is checked in callers.
    """
    c = volume/bulk
    dx = (c*(initial-final)-reopening)/AP
    d_elastic = .5*c*(final*final-initial*initial)
    load_work = final*AP*dx
    # With zero reopening the difference is equilibration heat.
    heat = .5*c*(initial-final)**2
    if reopening == 0:
        close(d_elastic+load_work+heat, 0., 1e-12)
    return dict(height_change_mm=dx*1e3, elastic_change_J=d_elastic,
                equilibration_heat_J=heat)


def section_force(force, stiff, wall_error, gap_error):
    """Specified flat closure section, not a circular tube contact solution.
    b = pi*d/2, axial contact length 2 mm; gap g, two wall thicknesses t.
    Remaining compression margin 2*t-g. Pressure projected force p*b*l.
    Stiffness input is N/mm for full flattening displacement (OD-gap).
    """
    d, t, gap, length = .001, .0005+wall_error, .0009+gap_error, .002
    width = PI*d/2
    margin = 2*t-gap
    displacement = d+2*t-gap
    normal = stiff*1e3*displacement+force/AP*width*length
    energy = .5*stiff*1e3*displacement**2
    return dict(closure_margin_mm=margin*1e3, normal_N=normal,
                elastic_energy_mJ=energy*1e3)


def main():
    out = {}
    # Advance/reversal/stop/source-off cannot change connectivity if fronts stay closed.
    schedules = {
        'resident_advance_reverse_stop_source_loss': [(True, True), (False, True), (True, True), (True, False)],
        'single_front_reset': [(False, True), (False, False), (True, False)],
        'overlap_reset': [(False, True), (True, True), (True, False)],
        'poppet_normal_hold': [(False, True)],
        'poppet_stuck_open': [(False, False)],
    }
    out['connectivity'] = {k:[components(s) for s in v] for k,v in schedules.items()}
    assert 0 in out['connectivity']['single_front_reset'][1]
    assert all(0 not in s for s in out['connectivity']['overlap_reset'])
    assert out['connectivity']['overlap_reset'][-1] == [1,2]  # pocket recombines
    out['rotary_coverage'] = [dict(rollers=n, arc_deg=b, error_deg=e,
        **coverage(n, math.radians(b), math.radians(e)))
        for n,b,e in product((2,3), (110,130,200), (0,5,10))]
    out['race_geometry'] = [dict(samples=s, wall_error_mm=w*1e3,
        gap_error_mm=g*1e3,min_closed=sampled_race_coverage(s,w,g))
        for s,w,g in product((720,1440,2880),(-.00005,0,.00005),(-.00005,0,.00005))]
    for case in out['race_geometry']:
        margin_mm = .1+2*case['wall_error_mm']-case['gap_error_mm']
        expected = 1 if margin_mm > 1e-9 else 0
        assert case['min_closed'] == expected
    assert sampled_race_coverage(2880) >= 1
    assert sampled_race_coverage(2880,-.00005,.00005) == 0
    assert sampled_race_coverage(2880,-.00005,0.) == 0  # equality is unqualified
    out['one_missing_roller'] = coverage(3,math.radians(200),missing=(0,))
    assert sampled_race_coverage(2880,missing=(0,)) == 0
    # Packet edges/gap errors are common-mode scenarios, not independent cell trials.
    out['loss_trajectories'] = [dict(force_N=f, initial_omega=w, t_s=.05,
        **rotation(0.,w,.05,f,1e-6)) for f,w in product((0,.02,1,10),(0,20,-20))]
    out['tube_barriers'] = [dict(force_N=f, U0_mJ=u*1e3, **barrier(f,u))
        for f,u in product((0,.02,1,10), (0,.0001,.001,.010))]
    # Straight front: volume and pressure work agree, exact reversal cancels.
    q = .010
    displacement = AT/AP*q
    for f in (0,.02,1,10):
        close(f*displacement, f/AP*AT*q)
    close(AT/AP*(q-q), 0.)
    out['front'] = dict(travel_for_40mm_mm=AP/AT*H*1e3,
        rollback_per_10mm_mm=displacement*1e3,
        horizontal_reaction_N=[dict(load_N=f, reaction=f*AT/AP) for f in (0,.02,1,10)])
    # Closing a second pinch does not pressure-match the enclosed reservoir pocket.
    v = AT*.010
    out['packet_merges'] = []
    for bulk, force, initial in product((10e6,100e6,1000e6), (.02,1,10),(0,.5e6)):
        final = force/AP
        assert max(abs(initial),abs(final))/bulk < .32  # worst flagged as large-strain limit
        out['packet_merges'].append(dict(K_MPa=bulk/1e6, load_N=force,
            initial_MPa=initial/1e6, **packet(v,bulk,initial,final)))
    for p in (0,1e5,1e6):
        close(packet(v,1e8,p,p)['height_change_mm'], 0.)
    close(packet(0.,1e8,0,1e6)['height_change_mm'],0.)
    out['repeated_reset_16_mm'] = 16*packet(v,100e6,0,10/AP)['height_change_mm']
    out['zero_load_suction_limit_N'] = 101325*AP
    out['reopening_only_mm'] = packet(v,1e8,0,0,reopening=.2e-9)['height_change_mm']
    out['normal_sections'] = [dict(load_N=f, stiffness_N_per_mm=k,
        **section_force(f,k,0.,0.)) for f,k in product((0,.02,1,10),(1,10,100))]
    out['closure_corners'] = [dict(wall_error_mm=w*1e3,gap_error_mm=g*1e3,
        **section_force(1,10,w,g)) for w,g in product((-.00005,0,.00005),(-.00005,0,.00005))]
    volume = 6400*AP*H
    out['board'] = dict(swept_litres=volume*1e3, minimum_L_min=volume*1e3*2,
        revolutions_per_full_stroke=AP*H/(2*PI*KQ),
        compression_cycles_per_full_stroke=N*AP*H/(2*PI*KQ),
        tube_m_at_60mm_each=6400*.060, rollers=6400*N,
        tube_only_budget_per_m=(500-250)/(6400*.060),
        cell_all_bought_budget=(500-250)/6400,
        rotor_angle_step_height_mm=2*PI/N*KQ/AP*1e3)
    # Optimistic fresh schedule; not E-108's pressure-flow schedule.
    # Two serial signed sweeps/group, 6 s overhead incl reset/proof/retry.
    timing=[]
    for rpm in (60,300,600):
        speed=KQ/AP*rpm*2*PI/60
        for extra in (0., .05):
            per_group=2*H/speed+extra
            heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*per_group<30)
            timing.append(dict(rpm=rpm,extra_s=extra,heads=heads,
                time_s=6+math.ceil(6400/heads)*per_group,
                max_head_dollars_if_cells_free=250/heads))
    out['optimistic_schedule']=timing
    # Static sealed hold: diagnostic, no product accuracy limit.
    out['hold'] = dict(leak_nL_s_for_point1mm_4h=AP*.0001/(4*3600)*1e12,
        sag_at_10N_mm=[dict(C_m3_Pa=c,sag_mm=c*(10/AP)/AP*1e3)
            for c in (0,1e-15,1e-14)])
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
