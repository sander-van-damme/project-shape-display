"""E-185 finite profile synthesis. SI; bounded scenarios, not hardware qualification.
Requires numpy. No stochastic priors, output files or global optimality claim.
"""
import argparse
import json
import math
import sys
from dataclasses import dataclass
import numpy as np

TAU = 2*math.pi
R = 6/.8
K = (6-R*.07)/(11500*TAU/60)
T0 = K*.07

@dataclass(frozen=True)
class Case:
    force: float = 1.
    jm: float = 1e-8
    mu: float = .05
    current: float = .8
    sink: float = 2.
    contact: float = 20.
    # Favorable ideal gears; extra drag at INPUT shaft is a sensitivity, not efficiency.
    drag: float = 0.


def path(family, n=256, extra=()):
    if family == 'geneva':
        length=20*TAU
        # Start/end at mid-dwell. Include both one-sided acceleration limits at edges.
        q=np.linspace(0,length,20*n+1)
        edges=np.array([TAU*j+x for j in range(20) for x in (3*math.pi/4,5*math.pi/4)])
        q=np.unique(np.r_[q,edges-1e-8,edges,edges+1e-8,extra])
        theta=(q%TAU)-math.pi
        c=.006; r=c/math.sqrt(2); a=math.pi/4; rp=.002*4/TAU
        active=np.abs(theta)<=a
        den=c*c+r*r-2*c*r*np.cos(theta)
        num=c*r*np.cos(theta)-r*r
        hp=np.where(active,rp*num/den,0.)
        hpp=np.where(active,rp*(-c*r*np.sin(theta)*den-num*2*c*r*np.sin(theta))/den**2,0.)
    else:
        hp0=.002 if family=='direct' else .0015*.04
        length=.04/hp0
        q=np.unique(np.r_[np.linspace(0,length,max(n*4,1024)+1),extra])
        hp=np.full_like(q,hp0); hpp=np.zeros_like(q)
    return q,hp,hpp,length


def profile(family, b, ramp, n=256):
    q,hp,hpp,L=path(family,n)
    # Linear squared-speed ramps give finite rest-to-rest acceleration.
    # Include ramp corners in evaluation, with both one-sided derivatives.
    knots=np.array([ramp*L,(1-ramp)*L])
    extra=np.r_[knots-1e-9,knots,knots+1e-9]
    q,hp,hpp,L=path(family,n,extra)
    # Finite samples and holdout refinements, not an interval certificate.
    mean=.04/L
    density=1+b*hp/mean
    dp=b*hpp/mean
    s=np.minimum(1,np.minimum(q/(ramp*L),(L-q)/(ramp*L)))
    sp=np.where(q<ramp*L,1/(ramp*L),np.where(q>(1-ramp)*L,-1/(ramp*L),0.))
    v=np.sqrt(np.maximum(0,s))/density
    acc=.5*sp/density**2-s*dp/density**3
    # Segment time exact for linearly interpolated v^2, converges under refinement.
    dt=2*np.diff(q)/(v[:-1]+v[1:])
    return q,hp,hpp,v,acc,dt


def signals(data,family,case,g,direction,k):
    q,hp,hpp,v,acc,dt=data
    speed=k*v; accel=k*k*acc
    zacc=direction*(hp*accel+hpp*speed**2)
    reaction=case.force+max(.002,case.force/9.81)*zacc
    if family=='screw':
        # Axial inertia participates in the sliding-thread contact reaction.
        t=.04; radius=.0015
        loadtorque=np.where(reaction*direction>=0,
            abs(reaction)*radius*(case.mu+t)/(1-case.mu*t),
            abs(reaction)*radius*(case.mu-t)/(1+case.mu*t))
    else:
        loadtorque=reaction*direction*hp
    tau=(1e-8+g*g*case.jm)*accel+loadtorque+case.drag
    current=(tau/g+T0)/K
    voltage=R*current+K*g*speed
    power=voltage*current
    return speed,accel,reaction,tau,current,voltage,power


def admissible(data,family,case,g,k):
    for direction in (1,-1):
        _,_,c,_,i,u,p=signals(data,family,case,g,direction,k)
        if (np.max(abs(c))>case.contact or np.max(abs(i))>case.current or
            np.max(abs(u))>6 or np.min(p)<-case.sink):
            return False
    return True


def fit(family,case,b,ramp,g,n=256):
    data=profile(family,b,ramp,n)
    # Finite scan allows nonmonotone feasible bands from signed inertia/load cancellation.
    grid=np.geomspace(.05,16000,80)
    good=[k for k in grid if admissible(data,family,case,g,k)]
    if not good: return None
    lo=max(good); j=np.searchsorted(grid,lo)
    hi=grid[min(j+1,len(grid)-1)]
    for _ in range(12):
        mid=(lo+hi)/2
        if admissible(data,family,case,g,mid): lo=mid
        else: hi=mid
    # 1% velocity reserve against sampling error; refine witness separately.
    k=lo*.99
    if not admissible(data,family,case,g,k): return None
    return dict(family=family,b=b,ramp=ramp,g=g,k=k,time_s=float(sum(data[-1])/k))


def synthesize(family,case,n=128,shaped=True):
    bs=(0,.25,1,4) if family=='geneva' and shaped else (0,)
    rows=[x for b in bs for ramp in (.005,.05,.25) for g in (.125,.25,.5,1,2,4,8,16,32,64)
          if (x:=fit(family,case,b,ramp,g,n))]
    return min(rows,key=lambda x:x['time_s']) if rows else None


def heads(service):
    return next((h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30),None)


def metrics(row,case,n=1024):
    data=profile(row['family'],row['b'],row['ramp'],n)
    k=row['k']; dt=data[-1]/k
    out=dict(row)
    out['fine_admissible']=admissible(data,row['family'],case,row['g'],k)
    out['fine_time_s']=float(sum(dt))
    # Same reversible trajectory must satisfy both directions; reusable linear carriage
    # also returns unloaded before next arbitrary site (loaded-speed return is conservative).
    strokes=2 if row['family']=='direct' else 1
    out['service_s']=.1+strokes*out['fine_time_s']
    out['heads']=heads(out['service_s'])
    out['head_allocation_USD']=250/out['heads'] if out['heads'] else None
    for direction,label in [(1,'up'),(-1,'down')]:
        speed,acc,c,tau,i,u,p=signals(data,row['family'],case,row['g'],direction,k)
        def integral(v): return float(np.sum((v[:-1]+v[1:])/2*dt))
        out[label]=dict(peak_current_A=float(max(abs(i))),peak_voltage_V=float(max(abs(u))),
                       reaction_range_N=[float(min(c)),float(max(c))],
                       peak_sink_W=float(max(0,-min(p))),input_J=integral(p),
                       copper_J=integral(R*i*i),motor_friction_J=T0*row['g']*data[0][-1],
                       mech_work_J=float(np.trapz(tau,data[0])),peak_motor_rpm=float(max(speed)*row['g']*60/TAU),
                       peak_output_m_s=float(max(abs(data[1]*speed))))
    out['energy_balance_error_J']=max(abs(out[z]['input_J']-out[z]['copper_J']-
        out[z]['motor_friction_J']-out[z]['mech_work_J']) for z in ('up','down'))
    if row['family']=='direct':
        unloaded=Case(force=0,jm=case.jm,current=case.current,sink=case.sink,
                      contact=case.contact,drag=case.drag)
        out['unloaded_return_admissible']=admissible(data,'direct',unloaded,row['g'],k)
        assert out['unloaded_return_admissible']
        returns=[fit('direct',unloaded,0,a,row['g'],1024) for a in (.005,.05,.25)]
        best=min((x for x in returns if x),key=lambda x:x['time_s'])
        return_data=profile('direct',0,best['ramp'],2048)
        assert admissible(return_data,'direct',unloaded,row['g'],best['k'])
        out['faster_unloaded_return_s']=float(sum(return_data[-1])/best['k'])
        out['return_profile']=best
        out['faster_return_service_s']=.1+out['fine_time_s']+out['faster_unloaded_return_s']
        out['faster_return_heads']=heads(out['faster_return_service_s'])
    # Independent rest-to-rest work bound, and reconstructed electric energy identity.
    assert out['up']['mech_work_J'] >= case.force*.04-1e-5
    assert out['energy_balance_error_J'] < 1e-5
    assert out['fine_time_s'] >= case.force*.04/((6-R*.07)**2/(4*R))
    return out


def checks():
    # Independent Cartesian output angle differentiates the Geneva law.
    derivative_error=0.
    for theta in (-.7,-.3,0.,.4,.7):
        eps=1e-4; c=.006; r=c/math.sqrt(2); rp=.002*4/TAU
        def height(x): return rp*math.atan2(r*math.sin(x),c-r*math.cos(x))
        q,hp,hpp,_=path('geneva',128,[math.pi+theta])
        j=np.argmin(abs(q-(math.pi+theta)))
        second=(height(theta+eps)-2*height(theta)+height(theta-eps))/eps**2
        derivative_error=max(derivative_error,abs(second-hpp[j]))
    assert derivative_error<1e-9
    # Rest-to-rest kinetic work telescopes to zero; signed variable-inertia term included.
    errors=[]
    for n in (128,512,2048):
        data=profile('geneva',1,.05,n)
        q,hp,hpp,v,a,dt=data
        errors.append(float(np.trapz(hp,q)-.04))
        e=.5*(1e-6+.1*hp*hp)*v*v
        de=(1e-6+.1*hp*hp)*a+.1*hp*hpp*v*v
        err=float(np.trapz(de,q)-(e[-1]-e[0]))
        assert abs(err)<1e-10 # reflection-symmetric path, signed terms cancel
    assert abs(errors[-1])<5e-8
    assert abs(errors[0]/errors[1]-16)<.1 and abs(errors[1]/errors[2]-16)<.1
    # Independent analytical trapezoid duration for a constant ratio profile.
    d=profile('direct',0,.05,256)
    assert abs(sum(d[-1])-d[0][-1]*(1+2*.05))<1e-10
    # Square-thread limiting cases, positive dissipation and hold criterion.
    for mu in (0,.02,.05,.2):
        t=.04; up=(mu+t)/(1-mu*t); down=(mu-t)/(1+mu*t)
        assert up>=t and down>=-t
        assert (down>=0)==(mu>=t)
    # Motor power identity at arbitrary signed current/speed.
    for i in (-.8,0,.8):
        for w in (0,120,1200):
            assert abs((R*i+K*w)*i-(R*i*i+K*i*w))<1e-12
    return dict(geneva_travel_errors_m=errors,geneva_second_derivative_error=derivative_error,constant_ratio_time_check=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sweep',action='store_true'); args=ap.parse_args()
    report={'checks':checks(),'motor':dict(R=R,K=K,T0=T0,peak_shaft_W=(6-R*.07)**2/(4*R)),'cases':[]}
    cases=[('base',Case()),('heavy',Case(force=10)),('inertia',Case(jm=1e-7))]
    if args.sweep:
        cases += [('heavy_inertia',Case(force=10,jm=1e-7)),('low_sink',Case(sink=.2)),
                  ('derated',Case(current=.2)),('friction',Case(mu=.2)),
                  ('drag',Case(drag=.001))]
    for name,case in cases:
        rows=[]
        for family in ('direct','screw','geneva'):
            row=synthesize(family,case)
            if row:
                row=fit(family,case,row['b'],row['ramp'],row['g'],1024)
            result=metrics(row,case,n=2048) if row else {'family':family,'no_sampled_profile':True}
            if row:
                assert result['fine_admissible'],(name,result)
                if family=='geneva':
                    base=synthesize(family,case,shaped=False)
                    if base:
                        base=fit(family,case,0,base['ramp'],base['g'],1024)
                    result['uniform_input_control_s']=base['time_s'] if base else None
                    result['refined_fixed_shape_s']=[fit(family,case,row['b'],row['ramp'],row['g'],n)['time_s'] for n in (256,1024)]
            rows.append(result)
        report['cases'].append(dict(name=name,scenario=case.__dict__,results=rows))
        print(name,[(r['family'],r.get('fine_time_s'),r.get('heads')) for r in rows],file=sys.stderr,flush=True)
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
