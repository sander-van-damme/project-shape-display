#!/usr/bin/env python3
"""E-161 necessary-condition witnesses. SI units; scenarios, not fitted hardware.
Run with Python 3 + NumPy. Printed JSON is reproducible and disposable.
"""
import json
import math
import numpy as np

LOADS = (0., .02, 1., 10.)
L = .04
N = 6400

def nullspace(a):
    a = np.array(a, dtype=float)
    _, s, vt = np.linalg.svd(a, full_matrices=True)
    rank = int(np.sum(s > 1e-10))
    return rank, vt[rank:].T

def row(angle):
    return [math.cos(angle), -math.sin(angle)]  # coordinates (z, s=R*theta)

def topology():
    out = []
    for name, angles in [('zero', [0.]), ('write', [math.radians(20)]),
                         ('matched_pair', [math.radians(20)]*2),
                         ('overlap_zero_write', [0., math.radians(20)]),
                         ('opposed_error', [math.radians(.1), -math.radians(.1)]),
                         ('crossed_park', [math.radians(20), -math.radians(20)])]:
        a = [row(x)+[0.] for x in angles] + [[0., 0., 1.]]
        rank, null = nullspace(a)
        assert np.max(np.abs(np.array(a)@null), initial=0.) < 1e-12
        assert np.max(np.abs(null[2]), initial=0.) < 1e-12
        out.append(dict(name=name, rank=rank, nullity=null.shape[1],
                        output_free=bool(np.linalg.norm(null[0]) > 1e-10)))
    # Reactions cannot support a nonzero load at nonzero pitch and zero torque.
    angle = math.radians(20)
    t = np.array([math.sin(angle), math.cos(angle), 0.])
    work = {str(f): float(np.array([-f, 0., 0.])@t) for f in LOADS}
    assert abs(np.dot(row(angle), t[:2])) < 1e-12
    # Two tops and one shared counterweight: z1+z2+y=constant.
    rank, ns = nullspace([[1, 1, 1]])
    exchange = np.array([1., -1., 0.])
    assert np.linalg.norm(np.array([[1., 1., 1.]])@exchange) == 0
    return dict(rolling=out, free_mode_work_N=work,
                shared_weight_nullity=ns.shape[1],
                shared_weight_exchange_work_N={str(f): .02-f for f in LOADS})

def return_angle(t, angle, tau, bias):
    # Exact critically damped centered torsional return, zero initial angular speed.
    x = t/tau
    a = bias+(angle-bias)*(1+x)*math.exp(-x)
    ad = -(angle-bias)*x*math.exp(-x)/tau
    return a, ad

def cut(f, vz, tau=.02, bias=0., dt=.0001, end=.4, angle=math.radians(20)):
    # Favorable pivot-at-contact swivel: steering has zero contact work.
    # m_s lumps circumferential rotor inertia J/R^2; roller spin inertia omitted.
    mz, ms = .02, .005
    state = np.array([0., 0., vz/math.tan(angle)])  # z, s, s_dot
    energy0 = .5*(ms+mz*math.tan(angle)**2)*state[2]**2
    residual = peak_traction = peak_z = low_z = 0.
    def rhs(t, q):
        a, ad = return_angle(t, angle, tau, bias)
        b, bd = math.tan(a), ad/math.cos(a)**2
        v = q[2]
        acc = (-f*b-mz*b*bd*v)/(ms+mz*b*b)
        return np.array([b*v, v, acc])
    count = round(end/dt)
    dt = end/count
    for i in range(count+1):
        t = i*dt
        a, ad = return_angle(t, angle, tau, bias)
        b, bd = math.tan(a), ad/math.cos(a)**2
        d = rhs(t, state)
        zacc = bd*state[2]+b*d[2]
        traction = (mz*zacc+f)/math.cos(a)
        peak_traction = max(peak_traction, abs(traction))
        energy = .5*(ms+mz*b*b)*state[2]**2+f*state[0]
        residual = max(residual, abs(energy-energy0))
        peak_z, low_z = max(peak_z, state[0]), min(low_z, state[0])
        if i == count:
            break
        k1 = d
        k2 = rhs(t+dt/2, state+dt*k1/2)
        k3 = rhs(t+dt/2, state+dt*k2/2)
        k4 = rhs(t+dt, state+dt*k3)
        state += dt*(k1+2*k2+2*k3+k4)/6
    return dict(F_N=f, cut_velocity_m_s=vz, tau_ms=1000*tau,
                bias_deg=math.degrees(bias), end_s=end,
                z_mm=1000*state[0], excursion_mm=[1000*low_z,1000*peak_z],
                residual_rotor_mJ=500*ms*state[2]**2,
                peak_traction_N=peak_traction, energy_error_J=residual)

def crossed():
    """Fixed +20-degree ring and returned -20-degree ring, preload never opened.
    Rank is a necessary frictional sticking condition, not an impact/brake model.
    """
    alpha=math.radians(20)
    cases=[]
    for f in LOADS:
        for second in (20.,19.9,19.,10.,0.,-10.,-20.):
            A=np.array([row(alpha), row(math.radians(second))])
            if np.linalg.matrix_rank(A,tol=1e-10)<2:
                cases.append(dict(F_N=f, second_deg=second, singular=True))
                continue
            traction=np.linalg.solve(A.T,np.array([f,0.]))
            assert np.max(np.abs(A.T@traction-[f,0.]))<1e-10
            cases.append(dict(F_N=f, second_deg=second,
                              tractions_N=traction.tolist(),
                              preload_each_at_mu_point2_N=float(max(abs(traction))/.2)))
    # All coherent + local angle error corners; no probabilistic interpretation.
    corners=[]
    for shared in (-2.,0.,2.):
        for e1 in (-1.,1.):
            for e2 in (-1.,1.):
                a1=math.radians(20+shared+e1); a2=math.radians(-20+shared+e2)
                A=np.array([row(a1),row(a2)])
                forces=np.linalg.solve(A.T,[10.,0.])
                corners.append(dict(shared_deg=shared, local_deg=[e1,e2],
                                    determinant=float(np.linalg.det(A)),
                                    peak_traction_N=float(max(abs(forces)))))
    # Reveal steering as an internal DOF, rather than silently fixing the return.
    # q=(z,s,alpha2,neighbor); contact-point steering coefficient e has units m/rad.
    swivel=[]
    for e in (0.,.00005,.0002):
        A=np.array([[math.cos(alpha),-math.sin(alpha),0.,0.],
                    [math.cos(alpha),math.sin(alpha),e,0.], [0.,0.,0.,1.]])
        rank,ns=nullspace(A)
        v=ns[:,0]/ns[2,0]
        assert np.max(np.abs(A@v))<1e-12
        assert abs(v[0]+e/(2*math.cos(alpha)))<1e-12
        swivel.append(dict(e_mm=e*1000, dz_dalpha_m_rad=float(v[0]),
                           load_torque_at_10N_Nm=abs(10*v[0]),
                           centered_return_k_Nm_rad=1e-8/.02**2))
    return dict(transfer=cases,park_angle_corners=corners,internal_swivel=swivel,
                write_mismatch_slip_mm_s={str(e):1000*abs(.1/math.tan(alpha)*math.sin(math.radians(e))/math.cos(alpha))
                                          for e in (.01,.1,.5)},
                parked_traction_per_load=1/(2*math.cos(alpha)),
                return_store=dict(inertia_kg_m2=1e-8,tau_s=.02,
                                  stiffness_Nm_rad=1e-8/.02**2,
                                  critical_damping_Nm_s=2e-8/.02,
                                  energy_J=.5*(1e-8/.02**2)*(2*alpha)**2,
                                  initial_torque_Nm=(1e-8/.02**2)*(2*alpha),
                                  offset_torque_Nm={str(e):6.079*e*.001 for e in (0,.05,.2)}))

def stores():
    weights = []
    for beta in (.25, 1., 4.):
        mass = 1/(9.81*beta)
        weights.append(dict(ratio=beta, mass_kg=mass, board_kg=N*mass,
                            travel_mm=1000*beta*L, reflected_kg=mass*beta**2,
                            residual_work_mJ=[1000*(f-1)*L for f in LOADS]))
    k=1000. # N/m, explicit comparison stiffness, not material data
    H=k*np.array([[1.,-1.],[-1.,1.]])
    assert np.linalg.norm(H@np.ones(2)) == 0
    springs = []
    for err in (.01,.05,.2):
        values = [(k*(1+e1)-k*(1+e2)) for e1 in (-err,err) for e2 in (-err,err)]
        springs.append(dict(fraction=err, net_stiffness_N_m=values,
                            max_force_change_over_40mm_N=max(values)*L))
    return dict(counterweights=weights, free_anchor_eigenvalues_N_m=np.linalg.eigvalsh(H).tolist(),
                balanced_spring_corners=springs,
                full_map_lift_J={str(f):N*f*L for f in LOADS})

def board():
    result=[]
    for speed in (.05,.1,.2):
        service=2*L/speed+.1  # 40mm output plus equal equivalent disengaged head return
        heads=next(h for h in range(1,N+1) if 6+math.ceil(N/h)*service<30)
        result.append(dict(speed_m_s=speed, minimum_heads=heads,
                           T_80_s=6+math.ceil(N/80)*service,
                           T_160_s=6+math.ceil(N/160)*service))
    alpha=math.radians(20)
    return dict(timing=result, shaft_turns=L/(.0015*math.tan(alpha)*2*math.pi),
                rpm_at_point1_m_s=.1/(.0015*math.tan(alpha))*60/(2*math.pi),
                shared_rotation_neighbor_mm={str(e):1000*L*math.tan(math.radians(e))/math.tan(alpha)
                                            for e in (.01,.1,.5)},
                free_site_allowance_USD={str(b):(b-250)/N for b in (200,400,500)})

def verify():
    # Constant-angle exact acceleration and signed work; no return limit tau -> infinity.
    b=math.tan(math.radians(20)); mass=.005+.02*b*b
    for f in LOADS:
        zdd=-f*b*b/mass
        acc=-f*b/mass
        assert abs(zdd-b*acc)<1e-12
    # Zero-force return conserves kinetic energy but changes direction, not speed energy.
    # Mirror skew reverses rotor direction while keeping the same vertical trace.
    nominal=cut(1.,-.1)
    mirror=cut(1.,-.1,angle=-math.radians(20))
    assert abs(nominal['z_mm']-mirror['z_mm'])<1e-10
    # Independent integrating-factor solution: w=sqrt(M)*s_dot; w'= -F*I',
    # I'=tan(alpha)/sqrt(M), z=w0*I-F*I^2/2. Simpson, not ODE replay.
    quadrature=[]
    for n in (1000,2000,4000):
        h=.4/n
        terms=[]
        for j in range(n+1):
            a,_=return_angle(j*h,math.radians(20),.02,0.)
            b=math.tan(a)
            terms.append(b/math.sqrt(.005+.02*b*b)*(1 if j in (0,n) else (4 if j%2 else 2)))
        integral=sum(terms)*h/3
        b0=math.tan(math.radians(20))
        w0=math.sqrt(.005+.02*b0*b0)*(-.1/b0)
        quadrature.append(1000*(w0*integral-.5*integral**2))
    assert abs(nominal['z_mm']-quadrature[-1])<1e-7
    convergence=[cut(1.,-.1,dt=d) for d in (.0004,.0002,.0001)]
    assert convergence[-1]['energy_error_J'] < 1e-9
    assert abs(convergence[-1]['z_mm']-convergence[-2]['z_mm'])<1e-5
    # Static parked perfect-zero constraint blocks output even if rotor is free.
    assert topology()['rolling'][0]['output_free'] is False
    return dict(rk4=convergence, independent_quadrature_z_mm=quadrature)

def main():
    convergence=verify()
    cases=[cut(f,v,tau=tau) for tau in (.005,.02,.1) for f in LOADS for v in (-.1,0.,.1)]
    # Return lasts 20 tau in these additional examples; not a long-time stability proof.
    slow=[cut(f,-.1,tau=.1,end=2.) for f in LOADS]
    errors=[cut(1.,-.1,bias=math.radians(e),end=2.) for e in (-.1,0.,.1)]
    print(json.dumps(dict(topology=topology(),stores=stores(),board=board(),crossed=crossed(),
                         cuts=cases,slow_return=slow,bias_cases=errors,
                         convergence=convergence),indent=2))

if __name__=='__main__':
    main()
