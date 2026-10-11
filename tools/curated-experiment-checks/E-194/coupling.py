"""E-194. Finite routed conduits and ideal worm outage bounds; not hardware proof.
Routing uses mm, dynamics SI. NumPy only. All non-requirement inputs are bounds.
No calibrated probability model, mesh qualification, or complete-machine pass.
"""
import json
import math
from itertools import product
import numpy as np


def poly_distance(a, b):
    """Exact distance between two 2-D polylines, including segment crossings."""
    p, u = a[:-1, None, :], np.diff(a, axis=0)[:, None, :]
    q, v = b[None, :-1, :], np.diff(b, axis=0)[None, :, :]
    cross = lambda x, y: x[..., 0]*y[..., 1]-x[..., 1]*y[..., 0]
    den = cross(u, v)
    nz = abs(den) > 1e-14
    safe = np.where(nz, den, 1.)
    ta, tb = cross(q-p, v)/safe, cross(q-p, u)/safe
    if np.any(nz & (ta >= 0) & (ta <= 1) & (tb >= 0) & (tb <= 1)):
        return 0.

    def point_segment(x, y, d):
        t = np.clip(np.sum((x-y)*d, axis=-1)/np.sum(d*d, axis=-1), 0, 1)
        return np.min(np.sum((x-y-t[..., None]*d)**2, axis=-1))
    return math.sqrt(min(point_segment(p, q, v), point_segment(p+u, q, v),
                         point_segment(q, p, u), point_segment(q+v, p, u)))


def route(j, radius, step, n):
    """One left-half row, depth positive down. Includes full 40-mm end sweeps.
    Finite conduit is a constant-width capsule of this centerline; arc approximated
    by chords with explicit Hausdorff bound. Strip width lies normal to this plane.
    """
    x = (j+.5)*5.08
    depth = radius+(j+1)*step
    angle = np.linspace(0, math.pi/2, n+1)
    arc = np.column_stack((x-radius+radius*np.cos(angle),
                           depth-radius+radius*np.sin(angle)))
    return np.vstack(([x, -40.], arc, [-radius-40., depth]))


def routing(radius, step, n=32):
    curves = [route(j, radius, step, n) for j in range(40)]
    worst, pair = math.inf, None
    # Translation by (i*pitch,i*step) maps each pair's arcs to (0,j-i).
    # Remaining differences only extend the parallel straight legs upstream
    # and outward. Both representative straights already overlap longitudinally;
    # extensions cannot reduce their pitch/step separation or approach the arcs.
    # Thus 39 separation classes cover all 780 pairs (holdouts in checks()).
    for i, j in ((0,j) for j in range(1,40)):
        d = poly_distance(curves[i], curves[j])
        if d < worst:
            worst, pair = d, (i, j)
    sag = radius*(1-math.cos(math.pi/(4*n)))
    # Outside thickness .1 strip + .4 total running gap + two .4 walls = 1.3.
    gap = worst-1.3-2*sag
    # Fixed-route length excludes two 40-mm swept guide reserves.
    lengths = [(j+.5)*5.08+(j+1)*step+math.pi*radius/2 for j in range(40)]
    return dict(radius_mm=radius, depth_step_mm=step, chords=n, pair=pair,
                gap_lower_mm=gap, distance_polyline_mm=worst, sagitta_mm=sag,
                deepest_outer_mm=radius+40*step+.65,
                fixed_route_m=sum(lengths)*160/1000,
                core_m_with_40mm_total_tail=(sum(lengths)+40*40)*160/1000,
                guide_m_with_two_40mm_end_sweeps=(sum(lengths)+40*80)*160/1000,
                error_margins_mm={str(e): gap-3*e for e in (.05, .1, .2)},
                bend_outer_strain_at_t01=.1/(2*radius))


def strip_bounds():
    # Steel-like E is an assumption, not a specification for a selected foil.
    E, b = 200000., 2.
    rows = []
    for t, span in product((.025, .05, .1, .2), (5., 10., 40.)):
        EI = E*b*t**3/12
        rows.append(dict(thickness_mm=t, free_span_mm=span,
                         pinned_euler_N=math.pi**2*EI/span**2,
                         radius_at_half_percent_strain_mm=t/.01))
    # Under translation a uniform fully occupied frictionless bend stores constant
    # bending energy: no input latch/driver -> no generalized support force.
    EI, radius = E*b*.1**3/12, 10.
    bend_U = EI*math.pi/(4*radius)  # N mm; no feed coordinate in this energy.
    return dict(euler=rows, constant_bend_energy_Nmm=bend_U,
                ideal_free_tail_support_N=0.,
                quarter_bend_reversal_lost_motion_mm={str(c):math.pi*c/2
                                                     for c in (.1,.4,.8)},
                note='Euler first buckling is not confined-strip collapse; wall contact, friction and folds are unsolved.')


def torsion_bounds():
    # Assumed effective shaft stiffness, not solid-wire stiffness transferred to
    # a wound flexible shaft. Favorable instant clamp of proximal input.
    out=[]
    for K, W, mass in product((.0001,.001,.01),(.02,1.,10.),(.002,.1)):
        r=.002
        kz=K/r**2
        # Free output spring/mass at its loaded equilibrium: v creates oscillation.
        excursion=.1*math.sqrt(mass/kz)
        assert math.isclose(.5*kz*excursion**2,.5*mass*.1**2)
        out.append(dict(stiffness_Nm_rad=K,load_N=W,mass_kg=mass,
                        loaded_deflection_mm=1000*W/kz,
                        ideal_clamp_velocity_excursion_mm=1000*excursion))
    return out


def worm_geometry(module_mm, worm_radius_mm, teeth, shell=True):
    """Single-start worm, 2-mm output pinion; intentionally favorable inertia.
    Shell includes a .4-mm wall at root and .4-mm end webs, omits helical teeth,
    shafts and bearings. Solid comparison also omits teeth/shaft extensions.
    Wheel modeled as solid root disk; ideal lossless rack/pinion mesh.
    """
    rho, m, r = 1250., module_mm/1000, worm_radius_mm/1000
    root, length = r-1.25*m, 4*m
    if root <= .0004:
        return None
    wheel_R, pinion_R = teeth*m/2, .002
    wheel_root, width = wheel_R-1.25*m, 3*m
    disk_J = lambda rr, ll: rho*math.pi*ll*rr**4/2
    if shell:
        Jworm = disk_J(root, length)-disk_J(root-.0004, length-.0008)
    else:
        Jworm = disk_J(root, length)
    Jwheel = disk_J(wheel_root, width)+disk_J(pinion_R, .002)
    return dict(module_mm=module_mm, worm_radius_mm=worm_radius_mm, teeth=teeth,
                shell=shell, slope=m/(2*r), k=pinion_R/teeth,
                J=Jworm, output_rotary_mass=Jwheel/pinion_R**2,
                wheel_outer_diameter_mm=(teeth+2)*module_mm,
                worm_outer_diameter_mm=2*(worm_radius_mm+module_mm))


def loss(g, mu, W, mass, sign, speed=.1):
    """Constant single-flank ideal worm law, from unwrapped normal-force balance.
    mu/cos(alpha) replaces square-thread friction; mesh elasticity omitted.
    Source torque zero, motor/source inertia already disconnected (favorable).
    """
    s, k, J = g['slope'], g['k'], g['J']
    # Wheel inertia belongs downstream of the dissipative mesh. It therefore
    # participates in tooth force, unlike worm/source inertia. Do not merely
    # reflect both rotors into the upstream inertia across a lossy transmission.
    mass = mass+g['output_rotary_mass']
    f = mu/math.cos(math.radians(20))
    c = k/s*(f+sign*s)/(1-sign*f*s)
    A = J+sign*mass*k*c
    if A <= 0:
        return dict(state='invalid_inertance')
    alpha = -sign*W*c/A
    contact = W+mass*k*alpha
    if contact < -1e-12:
        return dict(state='lost_flank')
    drag = contact*(c-sign*k)
    assert drag >= -1e-12
    assert abs((-W*k-sign*drag)-(J+mass*k*k)*alpha) < 1e-12
    if sign*alpha >= 0:
        return dict(state='no_stop', acceleration_mm_s2=k*alpha*1000)
    stop_t = speed/(k*abs(alpha))
    theta = sign*speed/k*stop_t+.5*alpha*stop_t**2
    heat = drag*abs(theta)
    kinetic = .5*(J+mass*k*k)*(speed/k)**2
    assert abs(kinetic-W*k*theta-heat) < 1e-10
    a = k*abs(alpha)
    return dict(state='stop', coast_mm=abs(k*theta)*1000,
                stop_time_s=stop_t, acceleration_m_s2=a, contact_N=contact,
                heat_J=heat, optimistic_endpoint_contained_stroke_s=math.sqrt(.08/a))


def heads(service):
    return next((h for h in range(1,6401) if 6+math.ceil(6400/h)*service < 30), None)


def worm_screen():
    out = []
    for module, radius, teeth in product((.4, .8), (2., 5., 10., 20.), (20, 40)):
        g = worm_geometry(module, radius, teeth)
        low = [loss(g, .02, .02, .002, d) for d in (1,-1)]
        nominal = [loss(g, .05, .02, .002, d) for d in (1,-1)]
        r = dict(g, low_mu=low, nominal_mu=nominal)
        r['static_hold_at_mu05'] = g['slope'] <= .05/math.cos(math.radians(20))
        if all(x['state']=='stop' for x in low):
            # Independent bidirectional heads: choose slower direction, not two passes.
            # Bound admits infinite active acceleration, no speed/power limit.
            service = .1+max(x['optimistic_endpoint_contained_stroke_s'] for x in low)
            h = heads(service)
            r.update(service_lower_bound_s=service, necessary_heads=h,
                     head_budget_ceiling_USD=250/h if h else None)
        out.append(r)
    return out


def sensitivities():
    rows=[]
    for radius, mu, W in product((5.,10.,20.),(.02,.05,.3),(.02,1.,10.)):
        g=worm_geometry(.4,radius,20)
        losses=[loss(g,mu,W,max(.002,W/9.81),d) for d in (1,-1)]
        h=None
        if all(x['state']=='stop' for x in losses):
            h=heads(.1+max(x['optimistic_endpoint_contained_stroke_s'] for x in losses))
        rows.append(dict(radius_mm=radius,mu=mu,load_N=W,necessary_heads=h,
                         states=[x['state'] for x in losses],
                         down_coast_mm=losses[1].get('coast_mm')))
    # Coherent dimensional box around the 10-mm/.4-module light-load case.
    dims=[]
    for module,radius in product((.35,.45),(9.9,10.1)):
        g=worm_geometry(module,radius,20)
        dims.append(dict(module_mm=module,radius_mm=radius,
                         down=loss(g,.02,.02,.002,-1)))
    return dict(friction_load=rows,coherent_dimensions=dims)


def checks():
    # Distances: crossing, collinear overlap, parallel separation, common shift.
    a=np.array([[0.,0.],[2.,0.]])
    assert poly_distance(a,np.array([[1.,-1.],[1.,1.]])) == 0
    assert poly_distance(a,np.array([[1.,0.],[3.,0.]])) == 0
    assert math.isclose(poly_distance(a,a+[0,3]),3)
    assert math.isclose(poly_distance(a+[7,-4],a+[7,-1]),3)
    # At every height, output exposed core h plus input exposed core 40-h
    # is unchanged; no loop take-up or omitted 40-mm tail accumulation.
    path=route(0,10.,3.,128)
    nominal=None
    for h in np.linspace(0,40,81):
        core=path.copy()
        core[0,1]=-h
        core[-1,0]=-10.-40.+h
        length=float(np.linalg.norm(np.diff(core,axis=0),axis=1).sum())
        if nominal is None:
            nominal=length
        assert math.isclose(length,nominal,abs_tol=1e-10)
        # Independent exact arc length bounds the chord approximation.
        exact=2.54+3+math.pi*10/2+40
        assert 0 < exact-length < .0001
    route_checks=0
    for r,step in ((5.,1.7),(10.,3.),(20.,10.)):
        for gap in range(1,40):
            d=poly_distance(route(0,r,step,16),route(gap,r,step,16))
            for i in {1,19,39-gap}:
                if i+gap<40:
                    other=poly_distance(route(i,r,step,16),route(i+gap,r,step,16))
                    assert math.isclose(d,other,abs_tol=1e-10)
                    route_checks+=1
    # Square-thread limit with alpha=0 is algebraically the E-156 form at r=k/s.
    # Frictionless loss must accelerate down with ideal reflected mass.
    g=worm_geometry(.4,10,20)
    x=loss(g,0.,1.,.1,-1)
    assert x['state']=='no_stop'
    expected=-1/(.1+g['output_rotary_mass']+g['J']/g['k']**2)
    assert math.isclose(x['acceleration_mm_s2']/1000,expected)
    for mu, W, mass, sign in product((.01,.02,.05,.3),(.02,1.,10.),(.002,.05,1.),(-1,1)):
        loss(g,mu,W,mass,sign)
    # Static hold does not prevent a moving worm from coasting.
    assert loss(g,.02,.02,.002,-1)['coast_mm'] > 40
    assert heads(.1+.04/.1+.1/1.) == 165
    return dict(signed_worm_cases=72,route_translation_holdouts=route_checks,
                geometry_limits='pass',energy_identities='pass')


if __name__ == '__main__':
    routes=[routing(r,s) for r,s in product((5.,10.,20.),(1.7,3.,5.,10.))]
    # Refinement for a tight route and a wider route.
    refinement=[routing(r,s,n) for r,s in ((10.,1.7),(10.,3.)) for n in (64,128)]
    print(json.dumps(dict(checks=checks(),routing=routes,refinement=refinement,
                          strip=strip_bounds(),torsion=torsion_bounds(),
                          worm=worm_screen(),sensitivity=sensitivities()),indent=2))
