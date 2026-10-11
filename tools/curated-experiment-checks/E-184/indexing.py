"""Finite Geneva entry screen; mm, N, radians unless explicitly SI.

Deterministic assumed bounds, not X1C priors. Run without arguments.
Only pin/slot section and parked lock normals are constructed. No claim that
the omitted relief profile, bearings, rack teeth or docking are feasible.
"""
import itertools
import json
import math

TAU = 2 * math.pi


def geometry(n, center, theta):
    r = center * math.sin(math.pi / n)
    x, y = center - r * math.cos(theta), r * math.sin(theta)
    rho2 = x*x + y*y
    phi = math.atan2(y, x)
    derivative = (center*r*math.cos(theta) - r*r) / rho2
    return x, y, phi, derivative


def handover(n, center, radius, gap, error, timing_deg=1):
    """Worst coherent pin/slot/registration box; both ends by symmetry.

    Pin grows e, slot half-width shrinks e, tangential registration adds e.
    Mouth position adds e to required full-pin insertion. Release timing has
    +/- timing_deg error; do not count it twice inside either one-sided bound.
    """
    r = center * math.sin(math.pi/n)
    available = gap - 3*error
    insertion = radius + 2*error
    if available < 0 or insertion > r:
        return None
    early = math.asin(insertion/r)
    late = math.acos(1-available/r)
    half_index = math.pi/2-math.pi/n
    late = min(late, half_index)
    margin = late - early - 2*math.radians(timing_deg)
    return dict(earliest_deg=math.degrees(early), latest_deg=math.degrees(late),
                command_margin_deg=math.degrees(margin), feasible=margin >= 0)


def dwell_lock():
    # Driver center D=(6,0); output origin. Opposed radius-.5 pads attached
    # to output, tangent externally to radius-2 driver disk at +/-30 deg
    # about its LEFT-facing direction. Circular normals go through D.
    out = []
    for sign in (-1, 1):
        nx, ny = -math.cos(math.pi/6), sign*math.sin(math.pi/6)
        px, py = 6+2.5*nx, 2.5*ny
        output_moment = px*ny-py*nx
        driver_moment = (px-6)*ny-py*nx
        assert abs(driver_moment) < 1e-14
        assert math.isclose(abs(output_moment), 3)
        out.append(dict(pad_center_mm=[px, py], output_moment_arm_mm=output_moment,
                        driver_moment_arm_mm=driver_moment))
    return out


def checks():
    n, center, pin, gap = 4, 6., .5, .1
    beta, alpha = math.pi/n, math.pi/2-math.pi/n
    r, mouth = center*math.sin(beta), center*math.cos(beta)
    # Transform actual disk center into held slot coordinates. Slot side solids
    # have inner faces +/- (pin+gap), terminate at radial mouth, and extend
    # inward to center-r-pin-.2. Fully inserted disk clears both finite faces.
    radial = (math.cos(beta), -math.sin(beta))
    tangent = (math.sin(beta), math.cos(beta))
    max_identity_error = 0.
    for j in range(1001):
        delta = .4*j/1000
        x, y, _, _ = geometry(n, center, -alpha+delta)
        depth = mouth - x*radial[0]-y*radial[1]
        side = x*tangent[0]+y*tangent[1]
        max_identity_error = max(max_identity_error, abs(depth-r*math.sin(delta)),
                                 abs(side-r*(1-math.cos(delta))))
    assert max_identity_error < 1e-12
    # Independent polygon half-plane checks at every phase in the accepted
    # nominal handover window, with +/-1-degree timing excursion included.
    h = handover(n, center, pin, gap, 0)
    a, b = map(math.radians, [h['earliest_deg'], h['latest_deg']])
    min_margin = float('inf')
    for j in range(1001):
        delta = a+(b-a)*j/1000
        x, y, _, _ = geometry(n, center, -alpha+delta)
        p, t = x*radial[0]+y*radial[1], x*tangent[0]+y*tangent[1]
        margins = [mouth-p-pin, pin+gap-abs(t)-pin,
                   p-pin-(center-r-pin-.2)]
        min_margin = min(min_margin, *margins)
    assert min_margin > -1e-12
    # Active nominal centerline pose keeps the finite pin within radial sides;
    # end entry/exit is only partial engagement and is NOT credited as support.
    for j in range(1001):
        theta = -alpha+2*alpha*j/1000
        x, y, phi, derivative = geometry(n, center, theta)
        assert abs(-x*math.sin(phi)+y*math.cos(phi)) < 1e-12
        assert derivative >= -1e-12
    # Independent work quadrature and derivative finite differences.
    quadrature = []
    for count in (64, 256, 1024):
        dt = 2*alpha/count
        values = [geometry(n, center, -alpha+i*dt)[3] for i in range(count+1)]
        integral = dt*(sum(values)-.5*(values[0]+values[-1]))
        quadrature.append(abs(integral-TAU/n))
    eps = 1e-6
    derivative_error = max(abs((geometry(n, center, t+eps)[2]-
                               geometry(n, center, t-eps)[2])/(2*eps)-
                              geometry(n, center, t)[3])
                           for t in [-.7, -.3, 0, .3, .7])
    assert derivative_error < 1e-8
    return dict(transform_error_mm=max_identity_error, finite_face_margin_mm=min_margin,
                angle_work_errors_rad=quadrature, derivative_error=derivative_error)


def main():
    nominal = []
    for gap, error in itertools.product((.1, .2), (0, .025, .05, .1)):
        nominal.append(dict(gap_mm=gap, error_mm=error,
                            window=handover(4,6,.5,gap,error)))
    synthesis = []
    for e in (0, .025, .05, .1):
        candidates = list(itertools.product((4,6,8),(4,6,10),(.3,.5,.8),(.025,.05,.1,.2)))
        passes = [(n,c,a,g) for n,c,a,g in candidates
                  if (h := handover(n,c,a,g,e)) and h['feasible']]
        synthesis.append(dict(error_mm=e, tested=len(candidates),
                              necessary_condition_survivors=len(passes)))
    # Favorable zero-clearance lock and groove control, no brake/damping.
    # At corresponding dwell positions, input kinetic energy gains signed F*s.
    # Zero phi' at entry/exit transfers output velocity continuously to zero;
    # it does not reset input kinetic energy. Positive inertia is always free.
    energy = []
    for force, initial_mj in itertools.product((-10,-1,0,.02,1,10),(0,1.25,12.5)):
        initial = initial_mj/1000
        # Cut at the middle of an index, one millimetre short of the next dwell.
        # A cut at exactly stationary entry would not spontaneously start.
        after = initial + force*.001
        j = 1e-6
        omega = math.sqrt(2*after/j) if after > 0 else 0
        dwell = 3*math.pi/2
        energy.append(dict(force_N=force, initial_mJ=initial_mj,
                           energy_at_next_dwell_mJ=1000*after,
                           dwell_crossing_s=dwell/omega if omega else None,
                           outcome='reaches dwell' if after > 0 else 'turns or stays; no crossing credited'))
    # Signed raising/lowering torque-work; exact energy bookkeeping.
    assert math.isclose(20*10*.002, 10*.040)
    performance = []
    for n in (4,6,8):
        s, c, force = 2., 6., 10.
        r = c*math.sin(math.pi/n)
        rack_radius = s*n/TAU
        peak_ratio = r/(c-r)
        performance.append(dict(slots=n, pinion_radius_mm=rack_radius,
                                peak_pin_normal_N=force*rack_radius/(c-r),
                                peak_input_torque_Nmm=force*rack_radius*peak_ratio,
                                peak_speed_ratio=peak_ratio,
                                total_driver_turns_for_40mm=20))
    schedule=[]
    for rpm in (600,1200,2400):
        per_site=.1+20*60/rpm
        heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*per_site < 30)
        schedule.append(dict(rpm=rpm, heads=heads, seconds_at_80_heads=6+80*per_site,
                             max_head_dollars_with_free_cells=250/heads))
    backlash = []
    for gap in (.1, .2):
        for rho in (6/math.sqrt(2), 6-6/math.sqrt(2)):
            backlash.append(dict(gap_mm=gap, pin_radius_from_output_mm=rho,
                                 rack_span_mm=2*(8/TAU)*math.asin(gap/rho)))
    print(json.dumps(dict(checks=checks(), dwell_contacts=dwell_lock(), backlash=backlash,
                          handover=nominal, synthesis=synthesis, energy=energy,
                          performance=performance, schedule=schedule), indent=2))


if __name__ == '__main__':
    main()
