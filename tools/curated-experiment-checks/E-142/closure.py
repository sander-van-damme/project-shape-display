"""E-142 SI screens: finite coil/plate closure and freely moving elastic output.

NumPy only. Bounds, not manufacturing priors. JSON stdout is disposable.
Normal contact: mass, spring, one annular friction face, coil flux, compressive
contact spring/damper and unilateral powered-open stop. Output uses a passive
backward-Euler Coulomb impulse; its numerical dissipation is reported explicitly.
"""
import json
import math
from itertools import product
import numpy as np

MU0 = 4*math.pi*1e-7
PROFILES = {
    'clamped': dict(g=.0002, d=.0002, N=100., ks=2000., m=.02,
                    kc=2e6, zeta=.3, R=12., clamp=48., hold=1.2),
    'diode_soft': dict(g=.0004, d=.0003, N=80., ks=1600., m=.03,
                    kc=.5e6, zeta=.02, R=12., clamp=.7, hold=1.2),
}


def _normal(p, dt=2e-6, duration=.3):
    """Flux lambda=L(q)i; L=a/(d+q); lambda_dot=-Ri-Vclamp.

    q=0 powered-open stop, q=g first contact; N is spring force at contact.
    Magnetic closing-opposition = lambda^2/(2a), derived from coenergy.
    Contact damping acts only during compression, hence cannot pull the faces.
    """
    a = MU0*300**2*150e-6
    lam = math.sqrt(2*a*p['hold']*(p['N']+p['ks']*p['g']))
    q = u = heat = 0.
    c = 2*p['zeta']*math.sqrt(p['m']*p['kc'])
    n = round(duration/dt)
    forces = np.zeros(n+1)
    gaps = np.zeros(n+1)
    def energy():
        return (.5*p['m']*u*u + .5*p['ks']*q*q
                -(p['N']+p['ks']*p['g'])*q
                +.5*p['kc']*max(q-p['g'],0)**2
                +lam*lam*(p['d']+q)/(2*a))
    e0 = energy()
    peak_error = 0.
    for j in range(n):
        L = a/(p['d']+q)
        old_lam = lam
        lam = max(0., (lam+p['clamp']*L/p['R'])*math.exp(-p['R']*dt/L)
                       -p['clamp']*L/p['R'])
        # Exact electrical loss for frozen q; mechanical splitting error refined.
        heat += (old_lam*old_lam-lam*lam)/(2*L)
        pen = max(q-p['g'],0.)
        damp = c*max(u,0.) if pen>0 else 0.
        f = p['kc']*pen+damp
        heat += damp*max(u,0.)*dt
        u += dt*(p['N']+p['ks']*(p['g']-q)-lam*lam/(2*a)-f)/p['m']
        q += dt*u
        if q<0:  # rigid coil-side stop; impact removes, never adds, energy
            heat += .5*p['m']*u*u
            q=u=0.
        forces[j+1] = p['kc']*max(q-p['g'],0.) + (c*max(u,0.) if q>p['g'] else 0.)
        gaps[j+1] = q
        peak_error=max(peak_error,abs(energy()+heat-e0))
    steady=p['kc']*p['N']/(p['kc']+p['ks'])
    first=np.flatnonzero(forces>0)[0]*dt
    low=np.flatnonzero(forces<.95*steady)
    settled=(low[-1]+1)*dt
    separation=np.count_nonzero((forces[1:]==0)&(forces[:-1]>0))
    current0=math.sqrt(2*a*p['hold']*(p['N']+p['ks']*p['g']))*p['d']/a
    pull_current=math.sqrt(2*p['N']/a)*(p['d']+p['g'])
    eq=p['g']+p['N']/(p['kc']+p['ks'])
    amplitude=math.sqrt((q-eq)**2+p['m']*u*u/(p['kc']+p['ks']))
    tail_floor=p['kc']*max(eq-p['g']-amplitude,0.) if lam==0 else 0.
    return forces, dict(first_ms=first*1e3, sustained_95_ms=settled*1e3,
        steady_N=steady, tail_floor_N=tail_floor, peak_N=float(max(forces)), separations=int(separation),
        max_closure_mm=float(max(gaps)*1e3), end_N=float(forces[-1]), hold_A=current0,
        hold_W=current0**2*p['R'], pull_at_contact_A=pull_current,
        release_work_J=p['N']*p['g']+.5*p['ks']*p['g']**2,
        max_energy_residual_J=peak_error, normal_initial_energy_J=e0)


_NORMAL_CACHE = {}


def normal(p, dt=2e-6, duration=.3):
    key=(tuple(sorted(p.items())),dt,duration)
    if key not in _NORMAL_CACHE:
        _NORMAL_CACHE[key]=_normal(p,dt,duration)
    return _NORMAL_CACHE[key]


def scenarios():
    # F is net external force including gravity; m is load-side effective inertia.
    # It may include output gearing. No free counterbalance/vertical ballast is
    # built by these scenarios; high force/light m requires an external load.
    return [dict(profile=profile, F=f, m=m, M=M, K=K, mu=mu, mode=mode)
            for profile,f,m,M,K,mu,mode in product(
                PROFILES,(.02,10.),(.05,1.1),(.3,3.),(100.,1000.,10000.),(.02,.1),
                ('raise','lower','reverse'))]


def coupled(rows, dt=20e-6, duration=1.5):
    """Downward x; y=r*theta, reflected M=J/r^2. No motor torque after t=0.

    Steady drive preload F/K, reversal preload (F-m*a)/K with a=-2 m/s^2.
    Bilateral dead-zone spring represents the two retained eye walls with .5-mm
    total play and series transmission compliance. Dense routing separately fails.
    """
    n=len(rows)
    F,m,M,K,mu=(np.array([r[key] for r in rows]) for key in ('F','m','M','K','mu'))
    c=np.zeros(n)  # undamped elastic holdout; no invented mechanical settling
    play=.00025  # nominal half-play of generated pin/eye; both faces retained
    pidx=np.array([0 if r['profile']=='clamped' else 1 for r in rows])
    v=np.array([-.1 if r['mode']=='raise' else .1 if r['mode']=='lower' else 0. for r in rows])
    w=v.copy(); x=np.zeros(n)
    preload=F+np.array([2*r['m'] if r['mode']=='reverse' else 0. for r in rows])
    y=-preload/K-play
    e0=.5*m*v*v+.5*M*w*w+.5*K*np.maximum(abs(x-y)-play,0)**2
    heat=np.zeros(n); numeric=np.zeros(n); lo=x.copy(); hi=x.copy()
    stop_t=np.full(n,np.nan); stop_x=np.zeros(n); after_hi=np.full(n,-np.inf)
    max_force=np.abs(preload); all_stopped=np.zeros(n,dtype=bool)
    packets={name:normal(p,dt=min(dt/10,2e-6)) for name,p in PROFILES.items()}
    normals={name:packet[0] for name,packet in packets.items()}
    ndt=min(dt/10,2e-6)
    worst_res=0.
    for j in range(round(duration/dt)):
        t=j*dt
        nn=np.array([normals[name][round(t/ndt)] if round(t/ndt)<len(normals[name])
                     else packets[name][1]['tail_floor_N'] for name in PROFILES])
        normal_f=nn[pidx]
        D=mu*normal_f*.016/.002  # one face; use minimum annulus radius
        delta=x-y
        oldstretch=np.sign(delta)*np.maximum(abs(delta)-play,0.)
        side=np.where(abs(delta)>play,np.sign(delta),0.)
        for attempt in range(4):
            ke=np.where(side==0,0.,K)
            alpha=dt*dt*ke
            a11=m+alpha; a12=-alpha; a22=M+alpha
            denom=a22-a12*a12/a11
            fs=ke*(delta-side*play)
            b1=m*v+dt*(F-fs); b2=M*w+dt*fs
            rhs=b2-a12*b1/a11
            wn=np.sign(rhs)*np.maximum(np.abs(rhs)-dt*D,0.)/denom
            vn=(b1-a12*wn)/a11
            xn=x+dt*vn; yn=y+dt*wn
            newdelta=xn-yn
            nextside=np.where(abs(newdelta)>play,np.sign(newdelta),0.)
            if np.array_equal(side,nextside): break
            side=nextside
        else: raise AssertionError('joint active set did not converge')
        stretch=np.sign(newdelta)*np.maximum(abs(newdelta)-play,0.)
        bregman=.5*K*(oldstretch**2-stretch**2)+K*stretch*(newdelta-delta)
        assert min(bregman)>-1e-10
        numeric += .5*m*(vn-v)**2+.5*M*(wn-w)**2+bregman
        heat += dt*(D*np.abs(wn)+c*(vn-wn)**2)
        stopped=wn==0.
        new=stopped&(~all_stopped)
        stop_t[new]=(j+1)*dt;stop_x[new]=xn[new];after_hi[new]=xn[new]
        # If it restarts, the last stop is no longer final; reset on re-arrest.
        all_stopped=stopped
        after_hi=np.where(stopped,np.maximum(after_hi,xn),-np.inf)
        x,y,v,w=xn,yn,vn,wn
        lo=np.minimum(lo,x);hi=np.maximum(hi,x)
        max_force=np.maximum(max_force,np.abs(K*stretch+c*(v-w)))
        if j%1000==0:
            e=.5*m*v*v+.5*M*w*w+.5*K*stretch**2
            worst_res=max(worst_res,float(max(abs(e+heat+numeric-e0-F*x))))
    output=[]
    for i,r in enumerate(rows):
        # Exact infinite future bound conditional on rotor never slipping again.
        d=x[i]-y[i]
        elastic=.5*K[i]*max(abs(d)-play,0)**2
        E=.5*m[i]*v[i]**2+elastic-F[i]*d
        roots=[]
        for side in (-1,1):
            disc=(F[i]/K[i])**2+2*(E+side*F[i]*play)/K[i]
            if disc>=0:
                for sign in (-1,1):
                    root=side*play+F[i]/K[i]+sign*math.sqrt(disc)
                    if side*root>=play-1e-12: roots.append(root)
        root=-E/F[i]
        if abs(root)<=play: roots.append(root)
        assert len(roots)>=2
        tail_lo,tail_hi=y[i]+min(roots),y[i]+max(roots)
        peak_tail=K[i]*max(max(abs(d)-play,0) for d in roots)
        finalN=packets[r['profile']][1]['tail_floor_N']
        future_hold=bool(w[i]==0 and peak_tail<=mu[i]*finalN*8)
        if future_hold:
            lo[i]=min(lo[i],tail_lo);hi[i]=max(hi[i],tail_hi)
            after_hi[i]=max(after_hi[i],tail_hi)
        output.append(dict(**r,min_mm=lo[i]*1e3,max_mm=hi[i]*1e3,
             rotor_stopped=bool(w[i]==0), certified_tail=future_hold,
             last_stop_ms=float(stop_t[i]*1e3),
             after_stop_extra_mm=float((after_hi[i]-stop_x[i])*1e3) if w[i]==0 else None,
             peak_joint_N=max_force[i], numeric_loss_J=numeric[i], heat_J=heat[i],
             fits_heights={str(h):bool(lo[i]>=-(40-h)/1000 and hi[i]<=h/1000) for h in (12,34)}))
    return output,worst_res


def geometry():
    """Finite prisms in mm: four eye walls, pin, head and retained collar.

    Pin inserted before collar installation; automatic keeper/docking not built.
    Check solid overlap at entry, both vertical contacts, axial retaining stops,
    and actual positive penetration when pushed beyond an axial stop.
    """
    def overlap(a,b):
        return math.prod(max(0.,min(a[i][1],b[i][1])-max(a[i][0],b[i][0]))
                         for i in range(3))
    def shift(a,dx=0.,dz=0.):
        return ((a[0][0]+dx,a[0][1]+dx),a[1],(a[2][0]+dz,a[2][1]+dz))
    sweeps=[]
    for bias in (.0,.05,.1):
        bh=1-bias;ph=.75+bias
        walls=[((-1,1),(-2,2),(bh,2)),((-1,1),(-2,2),(-2,-bh)),
               ((-1,1),(bh,2),(-bh,bh)),((-1,1),(-2,-bh),(-bh,bh))]
        pin=((-2,2),(-ph,ph),(-ph,ph))
        entry=sum(overlap(shift(pin,dz=bias),wall) for wall in walls)
        max_collision=0.;stop_witness=0.
        for z in np.linspace(0,40,161):
            for side in (-1,1):
                takeup=side*(bh-ph)
                solids=[pin,((-2.5,-2),(-1.5,1.5),(-1.5,1.5)),
                             ((2,2.5),(-1.5,1.5),(-1.5,1.5))]
                for dx in (-1.,0.,1.):
                    total=sum(overlap(shift(a,dx,z+takeup),shift(w,dz=z))
                              for a in solids for w in walls)
                    max_collision=max(max_collision,total)
                stop_witness=max(stop_witness,sum(
                    overlap(shift(a,1.05,z+takeup),shift(w,dz=z))
                    for a in solids for w in walls))
        assert max_collision<1e-10 and stop_witness>0
        assert (entry>0)==(bias>.25/3)
        sweeps.append(dict(bias_mm=bias,entry_margin_mm=.25-3*bias,
                          entry_overlap_mm3=entry,swept_overlap_mm3=max_collision,
                          axial_overtravel_overlap_mm3=stop_witness,
                          diametral_play_mm=2*(bh-ph)))
    inertia=[.5*rho*math.pi*.001*(.020**4-.004**4)/.002**2
             for rho in (1000.,8000.)]  # density bounds, not process priors
    return dict(eye_sweeps=sweeps, axial_shoulder_overlap_mm=.5,
                rotor_only_reflected_kg=inertia,
                annulus_area_mm2=math.pi*(20**2-16**2),coil_pole_area_mm2=150.,
                routing='E-132 collision remains; isolated capture only')


def cam():
    # Constant-slope cylindrical sliding cam, R=6mm, lift .2mm over .35rad.
    # Exact inclined-plane lowering torque, separate minimum torsion return.
    R,g,phi=.006,.0002,.35
    s=g/(R*phi);ret=.8*.00706155
    return [dict(mu=mu,normal_N=N,return_Nm=ret,
           available_return_Nm=ret+N*R*(s-mu)/(1+mu*s),
           opening_Nm=N*R*(s+mu)/(1-mu*s)+ret,
           spring_lift_J=N*g,extra_return_J=ret*phi,
           releases=bool(ret+N*R*(s-mu)/(1+mu*s)>0),
           releases_with_5mNm_detent=bool(ret+N*R*(s-mu)/(1+mu*s)>.005))
           for N,mu in product((80.,120.),(.02,.1,.3))]


def limits():
    # Independent ballistic first-contact limit: no coil, constant spring force.
    p=dict(PROFILES['clamped'],hold=0.,ks=0.,zeta=0.)
    _,r=normal(p,dt=1e-6,duration=.001)
    exact=math.sqrt(2*p['m']*p['g']/p['N'])*1000
    assert abs(r['first_ms']-exact)<=.002
    # A stiff coupled pair with zero brake recovers free combined-mass motion.
    row=dict(profile='clamped',F=.02,m=1.1,M=.3,K=1e8,mu=0.,mode='lower')
    rr,err=coupled([row],dt=10e-6,duration=.002)
    expected=(.1*.002+.5*.02/1.4*.002**2)*1000
    assert abs(rr[0]['max_mm']-expected)<2e-5
    return dict(ballistic_first_contact_ms=exact,
                numerical_first_ms=r['first_ms'],
                free_pair_mm=rr[0]['max_mm'],free_pair_exact_mm=expected)


def main():
    geom=geometry(); cams=cam()
    normal_results={}
    for name,p in PROFILES.items():
        normal_results[name]=[dict(dt_us=dt*1e6,**normal(p,dt)[1]) for dt in (4e-6,2e-6,1e-6)]
    rows=scenarios()
    results,res=coupled(rows)
    # Refine the largest downward excursion after the final rotor stop.
    eligible=[r for r in results if r['certified_tail']]
    witness=max(eligible,key=lambda r:r['after_stop_extra_mm'])
    key={k:witness[k] for k in rows[0]}
    refinement=[]
    for dt in (40e-6,20e-6,10e-6):
        rr,err=coupled([key],dt)
        refinement.append(dict(dt_us=dt*1e6,energy_residual_J=err,**rr[0]))
    assert res<1e-7
    # Independent ideal locked-rotor oscillator: amplitude v*sqrt(m/K).
    control=dict(m=1.1,K=100.,speed=.1,amplitude_mm=.1*math.sqrt(1.1/100.)*1000)
    # Permanent-pad control from E-132; genuinely cannot stop at adverse corner.
    pads=dict(net_acceleration=(10-4.4-2*.02*80)/.5)
    assert abs(pads['net_acceleration']-4.8)<1e-12
    print(json.dumps(dict(limiting_checks=limits(),geometry=geom,cam=cams,normal=normal_results,
        count=len(results),energy_residual_J=res,refinement=refinement,
        ideal_locked_rotor=control,permanent_pad=pads,results=results),indent=2))

if __name__=='__main__':
    import sys
    if '--checks' in sys.argv:
        print(json.dumps(dict(limits=limits(),geometry=geometry(),cam=cam()),indent=2))
    else:
        main()
