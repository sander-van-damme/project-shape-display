#!/usr/bin/env python3
"""E-149: prescribed magnetization and contact witnesses, SI throughout.
Run with Python + NumPy. JSON is disposable. No calibrated process priors.
"""
import json
import math
import itertools
import numpy as np

MU0 = 4 * math.pi * 1e-7
R = .001
M = 1.2 / MU0  # stipulated mu0*M, NOT an internal flux-density prediction
MOMENT = 4 * math.pi * R**3 * M / 3
C = 1e-7 * MOMENT**2
PITCH = .004
TRACK = np.arange(-1, 12) * PITCH


def pair(z, x, y=0., c=C):
    """Two nonoverlapping fixed-M spheres, moments parallel to x.
    z, x, y are receiver-source offsets. Returns energy and signed axial force.
    """
    rr = x*x + y*y + np.asarray(z)**2
    u = c * (rr**-1.5 - 3*x*x*rr**-2.5)
    f = c * (3*np.asarray(z)*rr**-2.5 - 15*x*x*np.asarray(z)*rr**-3.5)
    return u, f


def rail(z, gap=.0005, scale=1.):
    dz = np.asarray(z)[..., None] - TRACK
    u, f = pair(dz, 2*R+gap, c=C*scale**2)
    return u.sum(axis=-1), f.sum(axis=-1)


def root(fn, lo, hi):
    a = fn(lo)
    assert a * fn(hi) <= 0
    for _ in range(65):
        mid = (lo+hi)/2
        b = fn(mid)
        if a*b <= 0:
            hi = mid
        else:
            lo, a = mid, b
    return (lo+hi)/2


def stationary(load, gap=.0005, scale=1.):
    z = np.linspace(0, .04, 8001)
    force = rail(z, gap, scale)[1] - load
    out = []
    for i in np.flatnonzero(force[:-1]*force[1:] < 0):
        r = root(lambda q: float(rail(q, gap, scale)[1])-load, z[i], z[i+1])
        stable = rail(r+1e-8, gap, scale)[1] < rail(r-1e-8, gap, scale)[1]
        out.append((float(r), bool(stable)))
    return out


def magnetic():
    convergence = []
    for n in (4001, 16001, 64001):
        z = np.linspace(0, .04, n)
        u, f = rail(z)
        convergence.append(dict(n=n, peak_force_N=float(max(abs(f))),
                                range_energy_J=float(np.ptp(u))))
    scenarios = []
    for gap, scale in itertools.product((.0003, .0005, .001), (.9, 1., 1.1)):
        z = np.linspace(0, .04, 16001)
        u, f = rail(z, gap, scale)
        scenarios.append(dict(gap_mm=gap*1000, common_M_scale=scale,
                              peak_force_N=float(max(abs(f))),
                              stable_at_0p02N=sum(s for _, s in stationary(.02, gap, scale)),
                              stable_at_1N=sum(s for _, s in stationary(1., gap, scale))))
    eq = stationary(0.)
    well = min((q for q, s in eq if s), key=lambda q: abs(q-.02))
    crest = min(q for q, s in eq if not s and q > well)
    barrier = float(rail(crest)[0]-rail(well)[0])
    # Exact conservative reach witness: positive kinetic energy everywhere
    # between 2 and 38 mm => no turning point in that interval.
    zpath = np.linspace(.002, .038, 36001)
    u0 = float(rail(crest)[0])
    kinetic0 = .0001  # .02 kg, .1 m/s; zero applied load
    # A loose analytic |dU/dz| bound accounts for potential maxima between
    # samples. Every one of the 13 sources stays >=2.5 mm laterally away.
    path_allowance = 13*18*C/.0025**4*(zpath[1]-zpath[0])/2
    energy_margin = float(u0 + kinetic0 - max(rail(zpath)[0])-path_allowance)
    assert energy_margin > 0
    # Neighbor rider-height and direct writer exposure at adjacent y lane.
    dz = np.linspace(-.04, .04, 32001)
    neighbor = max(abs(pair(dz, 0., .00508)[1]))
    head_peak = max(abs(pair(dz, .003, c=C*1.5**3)[1]))
    head_neighbor = max(abs(pair(dz, .003, .00508, c=C*1.5**3)[1]))
    # Writing force capability along a full period. Independent head offset
    # may choose either sign; this is a necessary ceiling, not a trajectory.
    both_direction_load_ceiling = head_peak - convergence[-1]['peak_force_N']
    # Translation offsets really span 40 mm; all rail/head sphere gaps positive.
    assert min(abs(np.diff(TRACK))) >= 2*R
    # Independent derivative and quadrature checks.
    q = np.linspace(.00013, .03983, 211)
    h = 1e-8
    derivative_err = max(abs(-(rail(q+h)[0]-rail(q-h)[0])/(2*h)-rail(q)[1]))
    assert derivative_err < 1e-8
    work_errors = []
    for n in (1001, 4001, 16001):
        z = np.linspace(well, crest, n)
        work = np.trapz(rail(z)[1], z)
        work_errors.append(float(abs(work+barrier)))
    assert work_errors[-1] < 1e-10
    return dict(convergence=convergence, scenarios=scenarios,
                well_mm=well*1000, crest_mm=crest*1000,
                central_barrier_J=barrier,
                zero_load_well_escape_speed_m_s=math.sqrt(2*barrier/.02),
                crest_coast_2_to_38mm_margin_J=energy_margin,
                adjacent_rider_peak_N=float(neighbor),
                head_selected_peak_N=float(head_peak),
                head_adjacent_y_peak_N=float(head_neighbor),
                both_direction_load_ceiling_N=float(both_direction_load_ceiling),
                derivative_error_N=float(derivative_err),work_errors_J=work_errors)


def magnetic_board():
    """Central cell, 80x80 finite fixed tracks and arbitrary neighbor heights.
    Near tracks resolved in z; far sources bounded for every z. All M parallel.
    |Fz| <= 18*C/rho^4; |dFz/dz| <= 153*C/rho^5 are deliberately loose.
    """
    results=[]
    for gap, scale in itertools.product((.0003,.0005,.001),(.9,1.,1.1)):
        c=C*scale**2
        far=lip=neighbor_bound=0.
        z=np.linspace(0,.04,16001)
        f=np.zeros_like(z)
        for i,j in itertools.product(range(-40,40),repeat=2):
            x=i*.00508-(.002+gap); y=j*.00508
            rho=math.hypot(x,y)
            if abs(i)<=3 and abs(j)<=3:
                f+=pair(z[:,None]-TRACK,x,y,c=c)[1].sum(axis=1)
                lip+=13*153*c/rho**5
            else:
                far+=13*18*c/rho**4
            if i or j:
                neighbor_bound+=18*c/math.hypot(i*.00508,j*.00508)**4
        interp=lip*(z[1]-z[0])/2
        results.append(dict(gap_mm=1000*gap, common_M_scale=scale,
                            near_sample_peak_N=float(max(abs(f))),
                            far_bound_N=far, interpolation_bound_N=interp,
                            arbitrary_rider_bound_N=neighbor_bound,
                            total_force_bound_N=float(max(abs(f)))+far+interp+neighbor_bound))
    # Isolated favorable writer passes through the adjacent fixed track.
    head_track_clearance=abs(.003-(.00508-.0025))-(.0015+.001)
    assert head_track_clearance<0
    assert max(r['total_force_bound_N'] for r in results)<1.
    return dict(corners=results, head_neighbor_track_clearance_mm=1000*head_track_clearance)


def contact(theta, n0, modulation, phase, velocity, vmax, mu, direction=1):
    """Two resident compliant feet: prescribed normal/tangential ellipses.
    Normal stiffness converts displacement to force (N0 + modulation*cos).
    Coulomb sliding surrogate, no finite tangential compliance or stick dwell.
    """
    c = np.cos(np.asarray(theta)[:, None] + np.array([0., phase]))
    normal = np.maximum(n0 + modulation*c, 0.)
    speed = direction*vmax*c
    friction = mu*normal*np.sign(speed-velocity)
    heat = np.sum(friction*(speed-velocity), axis=1)
    assert min(heat) >= -1e-12
    return normal.sum(axis=1), friction.sum(axis=1), heat.mean(), (friction*speed).sum(axis=1).mean()


def wave():
    vmax = 2*math.pi*40000*1e-6
    results = []
    for n0, ratio, mu, phase in itertools.product((20., 60.), (.5, 1.5), (.02, .1, .3), (0., math.pi)):
        th = (np.arange(8192)+.5)*2*math.pi/8192
        n, f, heat, pin = contact(th,n0,n0*ratio,phase,0.,vmax,mu)
        assert abs(heat-pin) < 1e-10
        results.append(dict(n0_per_foot_N=n0, modulation_ratio=ratio, mu=mu,
                            phase_deg=phase*180/math.pi,
                            minimum_total_normal_N=float(min(n)),
                            contact_duty=float(np.mean(n>0)),
                            mean_stall_drive_N=float(f.mean()),
                            off_hold_N=2*n0*mu, stall_contact_heat_W=float(heat)))
    refinement = []
    for n in (1024, 4096, 16384):
        th = (np.arange(n)+.5)*2*math.pi/n
        normal, f, heat, pin = contact(th,60.,30.,math.pi,0.,vmax,.1)
        exact = 4*.1*30/math.pi
        refinement.append(dict(n=n, mean_stall_N=float(f.mean()), error_N=abs(float(f.mean())-exact)))
    # Reverse drive symmetry and conservation at a finite signed speed.
    th = (np.arange(16384)+.5)*2*math.pi/16384
    for v in (-.1, 0., .1):
        _, f, heat, pin = contact(th,60,90,math.pi,v,vmax,.1)
        _, rev, _, _ = contact(th,60,90,math.pi,-v,vmax,.1,-1)
        assert abs(float(f.mean()+rev.mean())) < 1e-10
        assert abs(pin - float(f.mean())*v - heat) < 1e-10
    # Correlated bank preload/drive changes and relative phase error.
    corners = []
    for preload, drive, phase_error in itertools.product((.8,1.2),(.8,1.2),(-.2,0.,.2)):
        n, f, _, _ = contact(th,60*preload,90*drive,math.pi+phase_error,0.,vmax,.1)
        corners.append(dict(preload_scale=preload,drive_scale=drive,phase_error_rad=phase_error,
                            min_N=float(min(n)), mean_drive_N=float(f.mean()),
                            off_capacity_N=12*preload))
    stops = []
    for load, mass, speed, mu in itertools.product((0.,10.),(1.1,),(-.1,.1),(.02,.1,.3)):
        capacity=120*mu
        # upward-positive, load downward. Constant Coulomb drag after instant
        # wave removal. Arrest in motion direction then static hold needed.
        decel_force=capacity+math.copysign(load,speed)
        stops.append(dict(load_N=load, velocity_m_s=speed, mu_kinetic=mu,
                          arrests_and_holds=capacity>load,
                          first_stop_distance_mm=(1000*mass*speed**2/(2*decel_force)
                            if decel_force>0 else None)))
    # Single-foot failure: one resident contact no longer supplies preload.
    n_single=np.maximum(60+90*np.cos(th),0.)
    speed_balance=[]
    # Force balance at constant runner velocity, a sliding-contact surrogate.
    # Weighted velocity quantile avoids an iterative nonsmooth root finder.
    for count in (4096,16384):
        theta=(np.arange(count)+.5)*2*math.pi/count
        cosine=np.cos(theta[:,None]+np.array([0.,math.pi]))
        weights=.1*np.maximum(60+90*cosine,0.)/count
        for load,direction in itertools.product((0.,1.,10.),(1,-1)):
            speeds=(direction*vmax*cosine).ravel()
            order=np.argsort(speeds)
            cumulative=np.cumsum(weights.ravel()[order])
            index=np.searchsorted(cumulative,(weights.sum()-load)/2)
            speed=float(speeds[order[index]])
            _,f,heat,pin=contact(theta,60,90,math.pi,speed,vmax,.1,direction)
            service=.04/abs(speed)+.05
            heads=next((h for h in range(1,6401)
                        if 6+math.ceil(6400/h)*service<30),None)
            speed_balance.append(dict(samples=count,load_N=load,direction=direction,
                                      velocity_m_s=speed, heat_W=heat,
                                      driver_contact_power_W=pin,
                                      force_residual_N=float(f.mean())-load,
                                      optimistic_heads=heads))
    return dict(vmax_m_s=vmax, scenarios=results, convergence=refinement,
                correlated_corners=corners, instant_off_stops=stops,
                constant_speed_balance=speed_balance,
                one_foot_contact_duty=float(np.mean(n_single>0)),
                ringdown_speed_envelope_mm={str(t):1000*vmax*t for t in (.001,.01,.1)})


def contact_geometry():
    # Generated 44-mm runner q-42..q+2 mm and 1-mm tall fixed contact shoes.
    # Normal contact represented by compliant-layer penetration, not rigid
    # interpenetration. No flexural resonator or wave-transmission solver.
    k=60e6; n0=60.; na=90.; b=1e-6
    q=np.linspace(0,.04,401)
    land=np.minimum((q+.002)-(.0005+b),(-.0005-b)-(q-.042))
    assert min(land)>0
    theta=np.linspace(0,2*math.pi,4097)
    d0=n0/k; a=na/k
    indentation=d0+a*np.cos(theta[:,None]+np.array([0.,math.pi]))
    normal=k*np.maximum(indentation,0.)
    assert min(normal.sum(axis=1))>119.999999
    return dict(runner_length_mm=44., minimum_end_land_mm=float(min(land))*1000,
                normal_stiffness_N_m=k, off_compression_um=d0*1e6,
                normal_amplitude_um=a*1e6, tangential_amplitude_um=b*1e6,
                contact_area_each_mm2=1., peak_contact_stress_MPa=float(normal.max()),
                assumed_runner_width_mm=2., unallocated_width_at_5p08_pitch_mm=3.08)


def accounting():
    schedules=[]
    for v in (.025,.05,.1,.2):
        service=.04/v+.05
        heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30)
        schedules.append(dict(v_m_s=v, heads=heads, time_s=6+math.ceil(6400/heads)*service,
                              max_head_dollars_if_cells_free=250/heads))
    screws=[]
    for mu in (.02,.05,.1):
        lead=math.pi*.003*mu
        screws.append(dict(mu=mu,zero_margin_lead_mm=1000*lead,
                           turns=.04/lead, rpm_at_160_heads=60*.04/lead/.55))
    return dict(schedules=schedules,screws=screws, track_magnets=6400*14,
                dollar_per_magnet_if_everything_else_250=250/(6400*14),
                wave_cell_contacts=12800, wave_nominal_sum_preload_N=6400*120,
                useful_raise_energy_J={str(f):6400*.04*f for f in (.02,1.,10.)})


if __name__=='__main__':
    print(json.dumps(dict(magnetic=magnetic(),magnetic_board=magnetic_board(),
                         wave=wave(),contact_geometry=contact_geometry(),
                         accounting=accounting()),indent=2))
