"""E-141: SI bounded head-braking screens, not a device or reliability model.

Python 3 + NumPy. Exact piecewise Coulomb ramp; exact linear hydraulic segments;
analytic governor/closure/schedule bounds. JSON stdout is disposable.
"""
from itertools import product
import json
import math
from pathlib import Path
import runpy
import numpy as np


def closure(normal=80., gap=.0001, restitution=.5, plate_mass=.02):
    """Upper flight-time bound: spring force >= normal, no residual release force.

    Ignore all tangential braking during flights/impacts; e<1, no extra excitation.
    Impact speed <= sqrt(2*Fmax*g/m) needs spring stiffness correction below.
    """
    k = 2000.  # N/m; explicit spring scenario
    tc = math.sqrt(2*plate_mass*gap/normal)
    u = math.sqrt((2*normal*gap+k*gap*gap)/plate_mass)
    return tc + 2*plate_mass*u/normal*restitution/(1-restitution)


def spring_bound(force, mass, speed, drag, delay):
    """No braking before delay, full minimum drag thereafter; downward envelope.

    Valid for signed initial speeds |v|<=speed and positive constant service force.
    Deliberately ignores favorable transient braking. Not a failure prediction.
    """
    if drag <= force:
        return math.inf
    v = speed + force*delay/mass
    return speed*delay + force*delay*delay/(2*mass) + mass*v*v/(2*(drag-force))


def allowed_delay(force, mass, speed, drag, clearance):
    """Inverse of the sufficient all-off-then-full-force displacement bound."""
    a=force*drag/(2*mass*(drag-force))
    b=drag*speed/(drag-force)
    c=mass*speed*speed/(2*(drag-force))-clearance
    if c >= 0:
        return 0.
    return (-b+math.sqrt(b*b-4*a*c))/(2*a)


def ramp_arrest(force, mass, velocity, drag, delay, rise):
    """Exact signed rigid-coordinate trajectory under a stipulated force ramp.

    Downward x,v positive; Coulomb static=kinetic. Resolve every velocity zero,
    including raising -> rest -> falling during a still-insufficient brake ramp.
    Returns unrestricted travel extrema; compare to stroke separately.
    """
    x = t = heat = 0.
    lo = hi = 0.
    v = velocity
    e0 = mass*v*v/2
    for b0, slope, duration in [(0., 0., delay), (0., drag/rise, rise),
                                (drag, 0., 100.)]:
        tau = 0.
        while duration-tau > 1e-12:
            b = b0+slope*tau
            if abs(v) < 1e-10:
                v = 0.
                if b >= force-1e-12:
                    # All subsequent forces are nondecreasing: stays at rest.
                    assert abs(e0+force*x-heat) < 1e-8
                    return dict(min_mm=lo*1000, max_mm=hi*1000,
                                final_mm=x*1000, seconds=t, heat_J=heat)
                sign = 1.
            else:
                sign = math.copysign(1.,v)
            a = (force-sign*b)/mass
            j = -sign*slope/mass
            span = duration-tau
            roots = []
            if abs(j) > 1e-15:
                disc = a*a-2*j*v
                if disc >= 0:
                    roots = [(-a+math.sqrt(disc))/j,(-a-math.sqrt(disc))/j]
            elif abs(a) > 1e-15:
                roots = [-v/a]
            roots = [r for r in roots if 1e-10 < r <= span+1e-12]
            h = min(roots) if roots else span
            dx = v*h+a*h*h/2+j*h**3/6
            # Independent integral of B(t)*|v(t)| over this signed segment.
            heat += sign*(b*v*h+(b*a+slope*v)*h*h/2
                          +(b*j/2+slope*a)*h**3/3+slope*j*h**4/8)
            x += dx
            v += a*h+j*h*h/2
            if roots:
                v = 0.
            t += h
            tau += h
            lo, hi = min(lo,x), max(hi,x)
            assert abs(e0+force*x-mass*v*v/2-heat) < 1e-7
    raise ValueError('No arrest under the stipulated ramp')


def fluid_step(z, force, mass, area, compliance, conductance, seconds):
    """Exact constant-conductance v,p dynamics and integrated displacement."""
    # Scale pressure to velocity units to avoid ill-conditioned SI eigenvectors.
    scale = math.sqrt(compliance/mass)
    omega = area/math.sqrt(mass*compliance)
    a = np.array([[0.,-omega],[omega,-conductance/compliance]])
    eq = np.array([conductance*force/area**2, force/area*scale])
    old = z*np.array([1.,scale])
    vals, vecs = np.linalg.eig(a)
    prop = vecs @ np.diag(np.exp(vals*seconds)) @ np.linalg.inv(vecs)
    new = eq+prop@(old-eq)
    assert np.max(np.abs(new.imag)) < 1e-9*(1+np.max(np.abs(new.real)))
    new = new.real
    dx = eq[0]*seconds + np.linalg.solve(a,new-old)[0]
    return new/np.array([1.,scale]), float(dx)


def hydraulic(force=1., mass=.3, velocity=.1, beta=1e8, steps=100):
    """Equal-area cross-port head damper, spring-shut valve after 5+5 ms.

    Effective compliance includes both chambers/lines/walls/gas. Zero leakage is
    only a mathematical best-case comparison; not credited as a built valve.
    """
    area, volume, damping = 20e-6, 1e-6, 20.
    c = volume/beta
    g0 = area*area/damping
    z = np.array([velocity,damping*velocity/area])
    e0 = mass*z[0]**2/2+c*z[1]**2/2
    z, x = fluid_step(z,force,mass,area,c,g0,.005)
    lo, hi = min(0.,x),max(0.,x)
    for i in range(steps):
        g = g0*(1-(i+.5)/steps)
        z, dx = fluid_step(z,force,mass,area,c,g,.005/steps)
        x += dx
        lo, hi = min(lo,x),max(hi,x)
    vc, pc = z
    amp = math.sqrt((pc-force/area)**2+mass/c*vc*vc)
    center = x+c/area*(force/area-pc)
    # Exact subsequent extrema of the *lossless closed* fluid spring.
    closed_lo,closed_hi = center-c/area*amp,center+c/area*amp
    heat = e0+force*x-mass*vc*vc/2-c*pc*pc/2
    assert heat >= -1e-9
    # One exact oscillator period: state, position and energy recover.
    period = 2*math.pi*math.sqrt(mass*c)/area
    back, dx = fluid_step(z,force,mass,area,c,0.,period)
    assert np.max(np.abs(back-z)/(1+np.abs(z))) < 1e-8 and abs(dx)<1e-10
    leakage=[]
    for q_mm3_s in (.01,.1,1.):
        # Conductance specified by a labelled flow at 0.5 MPa, NOT constant flow.
        g = q_mm3_s*1e-9/5e5
        end, dx = fluid_step(z,force,mass,area,c,g,30.)
        leakage.append(dict(flow_at_half_MPa_mm3_s=q_mm3_s,
                            drift_mm_s=g*force/area**2*1000,
                            position_at_30s_mm=(x+dx)*1000))
    return dict(sampled_closing_min_mm=lo*1000,sampled_closing_max_mm=hi*1000,
                min_mm=closed_lo*1000,max_mm=closed_hi*1000,closed_amplitude_mm=c/area*amp*1000,
                max_abs_closed_pressure_MPa=(force/area+amp)/1e6,
                period_s=period,closure_heat_J=heat,leakage=leakage)


def checks():
    # Exact constant drag stopping work, both travel signs and gravity-free limit.
    for f,m,v in product((0.,.02,10.),(.03,3.),(-.3,.1)):
        r=ramp_arrest(f,m,v,20.,0.,1e-9)
        exact=m*v*v/(2*(20.-math.copysign(f,v)))
        assert abs(abs(r['final_mm'])/1000-exact)<1e-8
    # Independent RK4/quadrature holdout for a lossy hydraulic segment.
    m,a,c,g,f=.3,20e-6,1e-14,2e-11,1.
    z=np.array([.1,1e5,0.,0.])  # v,p,x,heat
    def rhs(q):
        v,p,_,_=q
        return np.array([(f-a*p)/m,(a*v-g*p)/c,v,g*p*p])
    exact,dx=fluid_step(z[:2],f,m,a,c,g,.002)
    errors=[]
    for n in (100,200,400):
        y=z.copy();dt=.002/n
        for _ in range(n):
            k1=rhs(y);k2=rhs(y+dt*k1/2);k3=rhs(y+dt*k2/2);k4=rhs(y+dt*k3)
            y += dt*(k1+2*k2+2*k3+k4)/6
        err=max(abs(y[0]-exact[0]),abs(y[1]-exact[1])/1e6,abs(y[2]-dx))
        errors.append(float(err))
        residual=.5*m*z[0]**2+.5*c*z[1]**2+f*y[2]-.5*m*y[0]**2-.5*c*y[1]**2-y[3]
        assert abs(residual)<1e-8
    assert errors[-1]<errors[0]
    return dict(hydraulic_rk4_errors=errors)


def controls():
    """Reuse the committed Weston model, matching r, total inertia and speed.

    Different capture geometry remains unresolved; this compares energy sinks only.
    E-132's counterbalanced-pad necessary-condition witness is reconstructed directly.
    """
    legacy=runpy.run_path(str(Path(__file__).resolve().parents[1]/'E-140'/'brake.py'))
    p=legacy['Brake']()
    mass=(p.ji+p.jo)/p.radius**2
    rows=[]
    for f in (.02,1.):
        rows.append(dict(force=f,mass=mass,
                         weston=legacy['simulate'](p,force=f,height=.012),
                         spring=ramp_arrest(f,mass,.1,12.8,.001+closure(),.001),
                         fluid=hydraulic(f,mass,.1)))
    return dict(matched_rows=rows,
                E132_pad_acceleration_m_s2=(10.-4.4-2*.02*80)/.5)


def main():
    spring=[]
    for name,delay,rise,gap,e in [('fast',.001,.001,.0001,.5),
                                 ('slow',.020,.020,.0004,.8)]:
        flight=closure(gap=gap,restitution=e)
        total=delay+flight+rise
        corners=[]
        # Conservative minimum effective radius 8 mm on an 8..12-mm annulus.
        drag=2*.02*80*.008/.002
        for force,mass,speed in product((.02,1.,10.),(.03,.3,3.),(.1,.3)):
            for sign in (-1,1):
                r=ramp_arrest(force,mass,sign*speed,drag,delay+flight,rise)
                corners.append(dict(force=force,mass=mass,velocity=sign*speed,
                                    bound_mm=spring_bound(force,mass,speed,drag,total)*1000,**r))
        spring.append(dict(name=name,flight_bound_ms=flight*1000,
                           full_force_by_ms=total*1000,min_drag_N=drag,cases=corners))
    fluids=[]
    for force,mass,velocity,beta in product((.02,10.),(.03,3.),(-.1,.1),(1e6,1e8,1e9)):
        fluids.append(dict(force=force,mass=mass,velocity=velocity,beta=beta,
                           **hydraulic(force,mass,velocity,beta)))
    conv=[dict(steps=n,**hydraulic(steps=n)) for n in (25,100,400)]
    assert abs(conv[-1]['max_mm']-conv[1]['max_mm'])<.001
    governors=[]
    for ratio,mu,weight,spring_scale in product((1.,5.,10.),(.02,.1),(.0016,.0024),(.8,1.2)):
        n,rf,rb,r,ve=2,.008,.01,.002,.05
        k=n*mu*weight*rf*rb*ratio**3/r**3
        added_mass=n*weight*rf**2*ratio**2/r**2
        preload=.002*rf*(ratio*ve/r)**2*spring_scale
        ve=r/ratio*math.sqrt(preload/(weight*rf))
        governors.append(dict(ratio=ratio,mu=mu,weight_kg=weight,
                              added_mass_kg=added_mass,return_preload_N=preload,
                              engagement_mm_s=ve*1000,
                              drag_at_point1_N=k*(.1**2-ve**2),
                              low_load_terminal_mm_s=math.sqrt(ve*ve+.02/k)*1000,
                              high_load_terminal_mm_s=math.sqrt(ve*ve+10/k)*1000))
    # Favorable no-friction pretrigger bound; any governor drag below trip delays it.
    trips=[dict(force=f,mass=m,trip_distance_mm=m*(.12**2-.1**2)/(2*f)*1000)
           for f,m in product((.02,10.),(.3,3.,6.7))]
    budgets=[]
    for speed in (.1,.3):
        for return_needed in (False,True):
            site=.04/speed*(1+return_needed)+.05
            h=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*site<30)
            budgets.append(dict(speed=speed,empty_return=return_needed,heads=h,
                                seconds=6+math.ceil(6400/h)*site,
                                max_bought_per_head_with_free_cells=250/h))
    # Source-independent clearances: no uniform arrest promise at arbitrary h,v.
    timing=[dict(mass=m,max_all_off_ms=allowed_delay(10.,m,.1,12.8,.012)*1000)
            for m in (.03,10/9.81,3.)]
    print(json.dumps(dict(checks=checks(),controls=controls(),spring=spring,spring_timing_gate=timing,hydraulic=fluids,
                          hydraulic_convergence=conv,governor=governors,
                          overspeed_trip=trips,budgets=budgets),indent=2))


if __name__=='__main__':
    main()
