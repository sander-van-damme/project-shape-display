"""E-140: bounded Weston stack model, SI units; no hardware qualification.

Implicit Euler with enumerated sliding/sticking thread and disc contacts.
Ratchet is already seated and grounded. Only nonpositive shaft speeds admitted;
raising/ratchet engagement are separate analytical screens, not simulated here.
JSON is disposable. Requires NumPy only.
"""
from dataclasses import dataclass, replace
from itertools import product
import json
import math
import numpy as np


@dataclass(frozen=True)
class Brake:
    lead: float = .0005
    rt: float = .002
    ri: float = .0025
    ro: float = .005
    radius: float = .002  # output rack/pinion conversion, m/rad
    mu: float = .1       # both discs, static = kinetic bounded scenario
    mut: float = .02     # square thread, static = kinetic
    stiffness: float = 1e5  # N/m, total axial stack compliance
    ji: float = 1e-6
    jo: float = 2e-7     # includes translating load's reflected inertia

    @property
    def a(self):
        return self.lead / (2 * math.pi)

    @property
    def b(self):
        return self.mu * 2 / 3 * (self.ro**3-self.ri**3)/(self.ro**2-self.ri**2)

    @property
    def hs(self):
        s = self.a / self.rt
        return (self.rt*(s-self.mut)/(1+s*self.mut),
                self.rt*(s+self.mut)/(1-s*self.mut))


def operators(p, dt):
    """Unknowns vi, vo, N, thread torque, input friction, output friction."""
    ops = []
    for si, so, st in product((-1, 0), (-1, 0), (-1, 0, 1)):
        if si == so == st == 0:
            continue  # fully static thread torque is an interval, handled in step
        m = np.zeros((6, 6))
        m[0] = [p.ji/dt, 0, 0, 1, -1, 0]
        m[1] = [0, p.jo/dt, 0, -1, 0, -1]
        m[2] = [-p.stiffness*p.a*dt, p.stiffness*p.a*dt, 1, 0, 0, 0]
        if si:
            m[3, 2], m[3, 4] = -p.b, 1
        else:
            m[3, 0] = 1
        if so:
            m[4, 2], m[4, 5] = -p.b, 1
        else:
            m[4, 1] = 1
        if st:
            m[5, 2], m[5, 3] = -p.hs[st > 0], 1
        else:
            m[5, 0], m[5, 1] = 1, -1
        ops.append(((si, so, st), np.linalg.inv(m)))
    return ops


def step(p, dt, ops, vi, vo, x, load):
    # x is signed axial compression; negative = real open gap. No return spring.
    vi_free, vo_free = vi, vo-load*dt/p.jo
    x_free = x+p.a*dt*(vi_free-vo_free)
    if x_free <= 0:
        return vi_free, vo_free, x_free, 0., 0., 0., 0.
    rhs = np.array([p.ji*vi/dt, p.jo*vo/dt-load, p.stiffness*x, 0, 0, 0])
    valid = []
    n = max(0.,p.stiffness*x)
    lo = max(p.hs[0]*n, -p.b*n+p.ji*vi/dt, load-p.jo*vo/dt-p.b*n)
    hi = min(p.hs[1]*n, p.b*n+p.ji*vi/dt, load-p.jo*vo/dt+p.b*n)
    if lo <= hi:
        t = (lo+hi)/2
        valid.append(np.array([0.,0.,n/p.stiffness,n,t,t-p.ji*vi/dt,
                               load-t-p.jo*vo/dt]))
    for (si, so, st), inv in ops:
        u, v, n, t, fi, fo = inv @ rhs
        if n < -1e-8 or u > 1e-8 or v > 1e-8 or fi+fo < -1e-10:
            continue
        if not si and abs(fi) > p.b*n+1e-10:
            continue
        if not so and abs(fo) > p.b*n+1e-10:
            continue
        if st and st*(u-v) < -1e-8:
            continue
        if not st and not p.hs[0]*n-1e-10 <= t <= p.hs[1]*n+1e-10:
            continue
        valid.append(np.array([u, v, n/p.stiffness, n, t, fi, fo]))
    if not valid:
        raise RuntimeError('No admissible lowering mode; do not extrapolate')
    # Reject physically distinct simultaneous solutions rather than hide ambiguity.
    for row in valid[1:]:
        assert np.max(np.abs(row[:4]-valid[0][:4])) < 1e-6, (row, valid[0])
    return tuple(valid[0])


def simulate(p, force=1., height=.012, speed=.1, dt=1e-4, duration=2., gap=None, thread_state=1.):
    load = force*p.radius
    # Valid steady lowering; default thread reaction at closing boundary.
    h0 = p.hs[0]+thread_state*(p.hs[1]-p.hs[0])
    n0 = load/(h0+p.b) if gap is None else 0.
    x = n0/p.stiffness if gap is None else -gap
    vi = vo = -speed/p.radius
    if gap is not None:
        vo = 0.  # bounded mismatch, not derived from the nominal lowering trace
    qi = qo = 0.
    e0 = .5*p.ji*vi*vi + .5*p.jo*vo*vo + .5*p.stiffness*max(x,0)**2
    diss = 0.
    nmax = n0
    opened = False
    ops = operators(p, dt)
    status = 'time_limit'
    residual = numerical = 0.
    for j in range(round(duration/dt)):
        old_x = x
        ui, uo, x, n, t, fi, fo = step(p, dt, ops, vi, vo, x, load)
        qi += ui*dt
        qo += uo*dt
        # Friction work: shaft discs plus thread work in excess of spring storage.
        diss += (-fi*ui-fo*uo+(t-p.a*n)*(ui-uo))*dt
        numerical += (.5*p.ji*(ui-vi)**2+.5*p.jo*(uo-vo)**2
                      +n*(x-old_x)-.5*p.stiffness*(max(x,0)**2-max(old_x,0)**2))
        vi, vo = ui, uo
        nmax = max(nmax, n)
        opened |= n < 1e-10
        energy = .5*p.ji*vi*vi+.5*p.jo*vo*vo+.5*p.stiffness*max(x,0)**2
        residual = e0-load*qo-energy-diss
        assert abs(residual-numerical) < 1e-8, (residual,numerical)
        assert residual >= -1e-8, residual  # backward Euler dissipation allowed
        if height+p.radius*qo <= 0:
            status = 'stroke_end'
            break
        if max(abs(vi), abs(vo)) < 1e-7:
            status = 'rest'
            # No hidden motor torque: both free shafts remain at rest next step.
            nxt = step(p, dt, ops, vi, vo, x, load)
            assert max(abs(nxt[0]),abs(nxt[1])) < 1e-7
            break
    return dict(status=status, seconds=(j+1)*dt, drop_mm=-p.radius*qo*1000,
                input_travel_rad=-qi, max_N=nmax, final_N=n, opened=bool(opened),
                numerical_loss_J=residual, dissipated_J=diss,
                final_speeds=[vi,vo])


def screens():
    p = Brake()
    # Threadless friction limit recovers spring torque exactly.
    assert replace(p, mut=0).hs == (p.a,p.a)
    # Branch identities: output, input, and combined power, with both moving down.
    rows = []
    for force, mu, mut in product((.02,.2,1.,10.), (.02,.05,.1,.3), (0.,.02,.1,.3)):
        b = replace(p, mu=mu, mut=mut)
        h = b.hs[1]
        n = force*b.radius/(h+b.b)
        ti = (h-b.b)*n
        assert abs(ti-force*b.radius+2*b.b*n) < 1e-12
        rows.append(dict(force=force,mu=mu,mut=mut,N=n,
                         forced_lowering_torque=ti,free_input_braking=b.b>h))
    # Exact frictionless-thread common-acceleration runaway witness.
    b = replace(p, mu=.02, mut=0)
    load = b.radius
    den = b.ji*(b.a+b.b)-b.jo*(b.b-b.a)
    n = b.ji*load/den
    acc = (b.b-b.a)*load/den
    assert acc < 0
    assert abs((b.b+b.a)*n-load-b.jo*acc) < 1e-12
    # Independently exact open-gap catch; input coasts, output accelerates under load.
    gaps = []
    for force, gap in product((.02,.2,1.,10.), (0.,.00005,.0001)):
        alpha = force*p.radius/p.jo
        w = .1/p.radius
        t = (w+math.sqrt(w*w+2*alpha*gap/p.a))/alpha
        drop = .5*p.radius*alpha*t*t
        gaps.append(dict(force=force,gap_um=gap*1e6,first_contact_s=t,
                         first_contact_drop_mm=drop*1e3))
    geometry=[]
    for mu in (.02,.1):
        margins=[]
        for dl,dr,di,do in product((-.00005,.00005),repeat=4):
            c=replace(p,mu=mu,lead=p.lead+dl,rt=p.rt+dr,ri=p.ri+di,ro=p.ro+do)
            margins.append(c.b-c.hs[1])
        geometry.append(dict(mu=mu,corners=len(margins),
                             min_margin_mm=min(margins)*1e3,max_margin_mm=max(margins)*1e3))
    schedule=[]
    for t in (.45,.85):
        heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*t<30)
        schedule.append(dict(site_seconds=t,min_heads=heads,
                             time_at_80=6+80*t,budget_per_head=250/heads))
    return dict(geometry=geometry,schedule=schedule,branch_cases=len(rows), robust_sign_cases=sum(r['free_input_braking'] for r in rows),
                nominal=[r for r in rows if r['mu']==.1 and r['mut']==.02],
                runaway=dict(N=n,acc_rad_s2=acc,linear_acc_m_s2=acc*b.radius),
                gaps=gaps)


def holdout():
    p = Brake()
    h,b,load=p.hs[1],p.b,p.radius
    n0=load/(h+b)
    d=(b+h)/p.jo-(b-h)/p.ji
    ns=load/p.jo/d
    omega=math.sqrt(p.stiffness*p.a*d)
    time=.005
    integ=ns*time+(n0-ns)*math.sin(omega*time)/omega
    exact=np.array([-50+(b-h)*integ/p.ji,-50+((b+h)*integ-load*time)/p.jo])
    errors=[]
    for dt in (2e-4,1e-4,5e-5):
        vi=vo=-50.
        x=n0/p.stiffness
        ops=operators(p,dt)
        for _ in range(round(time/dt)):
            vi,vo,x,n,t,fi,fo=step(p,dt,ops,vi,vo,x,load)
            assert vi-vo >= -1e-8 and abs(t-h*n)<1e-10
        errors.append(float(np.max(np.abs(np.array([vi,vo])-exact))))
    assert errors[2]<errors[1]<errors[0]
    # Exact co-accelerating runaway, independent of integration or compliance.
    q=replace(p,mu=.02,mut=0.)
    den=q.ji*(q.a+q.b)-q.jo*(q.b-q.a)
    n=q.ji*load/den
    acc=(q.b-q.a)*load/den
    dt=1e-4
    vi,vo,x,*_=step(q,dt,operators(q,dt),-50.,-50.,n/q.stiffness,load)
    assert abs(vi-(-50+acc*dt))<1e-10 and abs(vi-vo)<1e-10
    return dict(analytic_first_segment_speed_errors_rad_s=errors,
                exact_runaway_acc_rad_s2=acc)


def main():
    p = Brake()
    convergence = [dict(dt=dt,**simulate(p,dt=dt)) for dt in (2e-4,1e-4,5e-5)]
    runs = []
    for force,height in product((.02,.2,1.,10.),(.012,.034)):
        runs.append(dict(force=force,height=height,**simulate(p,force,height)))
    sensitivity = []
    for field,values in [('mu',(.02,.05,.3)),('mut',(0.,.1,.3)),
                         ('stiffness',(1e4,1e6)),('ji',(1e-7,1e-5))]:
        for value in values:
            sensitivity.append(dict(field=field,value=value,
                                    **simulate(replace(p,**{field:value}))))
    gap_convergence = [dict(dt=dt, **simulate(p,gap=.0001,dt=dt)) for dt in (2e-4,1e-4,5e-5)]
    history = [dict(thread_state=t, **simulate(p,thread_state=t)) for t in (0.,.5)]
    gap_runs = [dict(force=f, **simulate(p,force=f,gap=.0001)) for f in (.02,.2,1.)]
    # Independent no-friction ballistic holdout, before any compression/contact.
    f,dt=.02,1e-4
    ops=operators(p,dt)
    u,v,x,*_=step(p,dt,ops,-50.,0.,-.0001,f*p.radius)
    assert u == -50. and abs(v+f*p.radius*dt/p.jo)<1e-12
    assert x < -.0001
    print(json.dumps(dict(screens=screens(),convergence=convergence,
                          loads_heights=runs,sensitivity=sensitivity,gap_runs=gap_runs,history=history,gap_convergence=gap_convergence,holdout=holdout()),indent=2))


if __name__ == '__main__':
    main()
