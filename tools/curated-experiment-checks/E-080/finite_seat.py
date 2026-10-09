#!/usr/bin/env python3
"""Hypothetical finite magnetic flag / unilateral compliant seat; no process prior.
Python + NumPy. Deterministic bounded scenarios, not probability samples.
"""
import json
import math
import sys
import os
import pathlib
import subprocess
import tempfile
from itertools import product
import numpy as np

BETA = math.pi / 3

def V(q):
    return q*q*(1-q)**2/2

def dV(q):
    return q*(1-q)*(1-2*q)

def work(q):
    return (np.sin(BETA*(q-.5)) + math.sin(BETA/2))/BETA

GRID = np.linspace(1e-8, 1, 100001)
A_STEP = float(np.max(V(GRID)/work(GRID)))


def contact(q, v, K, eta, b):
    # Plane normal is tangent to circular trajectory at q=b; point radius R.
    # p=penetration/(R*beta). Valid near seat, cos remains positive.
    angle = BETA*(q-b)
    p = np.where(q < b, -np.sin(angle)/BETA, 0.)
    J = np.cos(angle)
    C = eta*K*p
    # Compression-only dashpot, no adhesive/tensile force on unloading.
    force = (K*p + C*np.maximum(-v*J, 0.))*J
    return np.where(q < b, force, 0.), K*p*p/2


def acceleration(q, v, K, eta, b, z, a, u):
    return a*u*np.cos(BETA*(q-.5)) - dV(q) - 2*z*v + contact(q,v,K,eta,b)[0]


def step(q,v,h,K,eta,b,z,a,u):
    def acc(x,y): return acceleration(x,y,K,eta,b,z,a,u)
    a1=acc(q,v); q2=q+h*v/2; v2=v+h*a1/2
    a2=acc(q2,v2); q3=q+h*v2/2; v3=v+h*a2/2
    a3=acc(q3,v3); q4=q+h*v3; v4=v+h*a3
    a4=acc(q4,v4)
    return q+h*(v+2*v2+2*v3+v4)/6, v+h*(a1+2*a2+2*a3+a4)/6


def equilibrium(K,b):
    # Initial no-field equilibrium, including finite seat preload when b>0.
    lo=np.zeros_like(b); hi=np.maximum(b,0)
    for _ in range(60):
        m=(lo+hi)/2
        f=contact(m,0,K,0,b)[0]-dV(m)
        lo=np.where(f>0,m,lo); hi=np.where(f>0,hi,m)
    return (lo+hi)/2


def run(rows,h=.0025,horizon=120,schedules=None,constant=False):
    p=np.array([r[:6] for r in rows],dtype=float)
    K,eta,b,z,f,signed=p.T
    a=f*A_STEP
    q=equilibrium(K,b);v=np.zeros(len(rows))
    low=q.copy();high=q.copy();peak=np.zeros(len(rows));cross=np.full(len(rows),np.nan)
    edges=[[] for _ in rows];previous=np.full(len(rows),9.);active=np.ones(len(rows),dtype=bool)
    idx=np.zeros(len(rows),dtype=int);fixed_u=np.zeros(len(rows))
    for n in range(round(horizon/h)):
        t=n*h
        if schedules is not None:
            for j,seq in enumerate(schedules):
                while idx[j]<len(seq) and t+1e-10>=seq[idx[j]][0]:
                    fixed_u[j]=seq[idx[j]][1];idx[j]+=1
            u=fixed_u.copy()
        else:
            u=np.where(v>=0,1.,np.where(signed, -1.,0.))
            if constant: u=np.ones(len(rows))
        u=np.where(active,u,0.)
        changed=np.where((u!=previous)&active)[0]
        for j in changed: edges[j].append([round(t,9),int(u[j])])
        previous=u.copy()
        nq,nv=step(q,v,h,K,eta,b,z,a,u)
        q=np.where(active,nq,q);v=np.where(active,nv,0.)
        low=np.minimum(low,q);high=np.maximum(high,q)
        peak=np.maximum(peak,contact(q,v,K,eta,b)[0])
        hit=active&(q>=.5)
        cross[hit]=(n+1)*h;active &= ~hit
        if not np.any(active): break
    return [dict(K=r[0],compression_damping=r[1],seat_offset=r[2],well_damping=r[3],
                 half_fraction=r[4],signed=bool(r[5]),step=h,horizon=horizon,
                 saddle_time=None if np.isnan(cross[j]) else float(cross[j]),
                 min_q=float(low[j]),max_q=float(high[j]),peak_seat_force=float(peak[j]),
                 pulse_edges=edges[j]) for j,r in enumerate(rows)]


def checks():
    # Exact tangent-plane penetration and torque work (finite-difference check).
    for q in (-.08,-.01,.01,.2):
        K=100.;b=.02;eps=1e-6
        force=contact(q,0,K,0,b)[0]
        grad=(contact(q+eps,0,K,0,b)[1]-contact(q-eps,0,K,0,b)[1])/(2*eps)
        assert abs(force+grad)<1e-7
        assert abs((work(q+eps)-work(q-eps))/(2*eps)-math.cos(BETA*(q-.5)))<1e-9
    # Contact is unilateral and damping cannot supply energy; no phantom attraction.
    for q,v in product((-.08,-.001,.0,.01),(-.3,0.,.3)):
        f,_=contact(q,v,100.,100.,0.)
        elastic,_=contact(q,v,100.,0.,0.)
        assert f>=0 and (f-elastic)*v<=1e-12
    # Independent numerical energy budget over impact; finer dt must converge.
    errors=[]
    for h in (.001,.0005,.00025):
        q=.01;v=-.2;K=100.;eta=10.;b=0.;z=.02
        E0=V(q)+v*v/2;loss=0.
        for _ in range(round(1/h)):
            def dissip(x,y):
                J=math.cos(BETA*x)
                return 2*z*y*y+(eta*K*(-math.sin(BETA*x)/BETA)*y*y*J*J if x<0 and y<0 else 0.)
            qn,vn=step(q,v,h,K,eta,b,z,0.,0.)
            loss+=h*(dissip(q,v)+dissip(qn,vn))/2
            q,v=qn,vn
        errors.append(abs(V(q)+v*v/2+contact(q,v,K,eta,b)[1]+loss-E0))
    assert errors[-1]<2e-6 and errors[-1]<errors[0]
    # Undamped rebound conserves total potential + kinetic energy.
    q=.01;v=-.2;E0=V(q)+v*v/2
    for _ in range(4000):q,v=step(q,v,.00025,100.,0.,0.,0.,0.,0.)
    assert abs(V(q)+v*v/2+contact(q,v,100.,0.,0.)[1]-E0)<1e-8
    # Seat transforms into opposite seat under q -> 1-q; dipole torque changes sign.
    for q,v in ((.1,.03),(-.01,-.1)):
        left=acceleration(q,v,100.,.5,0.,.02,.06,1.)
        # Independently write the right-seat force via mirrored normal coordinate.
        right=-.06*math.cos(BETA*(1-q-.5))-dV(1-q)+2*.02*v-contact(q,v,100.,.5,0.)[0]
        assert abs(left+right)<1e-12
    return dict(energy_budget_errors=errors,checks='geometry derivative, work, passivity, energy, reset symmetry')


def impact_limit(alpha, speed):
    """Exact flat-seat, no-detent compression-only damping limit; e -> 1 at v -> 0."""
    x=alpha*speed
    return 1. if x == 0 else math.sqrt(2*(x-math.log1p(x)))/x


def impact_holdouts():
    # Independent flat-seat calculation against the curved-contact full ODE.
    # K=1000 makes contact short; detent curvature gives a small discrepancy.
    results=[]
    for alpha,speed in product((0.,10.,100.),(.01,.1)):
        q=0.;v=-speed;h=.00005
        for _ in range(10000):
            q,v=step(q,v,h,1000.,alpha,0.,0.,0.,0.)
            if q>=0 and v>0:break
        else:raise AssertionError('impact did not unload')
        numerical=v/speed
        exact=impact_limit(alpha,speed)
        assert abs(numerical-exact)<.001
        results.append(dict(alpha=alpha,incoming_speed=speed,flat_exact_restitution=exact,
                            curved_ode_restitution=float(numerical)))
    return results


def fast_run(rows, h, binary, horizon=120, schedules=None):
    records=[]
    for i,r in enumerate(rows):
        line=" ".join(map(str,r))
        if schedules is not None:
            line+=" "+str(len(schedules[i]))+" "+" ".join(str(x) for edge in schedules[i] for x in edge)
        records.append(line)
    args=[str(binary),str(h),str(horizon),str(A_STEP)]
    if schedules is not None:args.append('fixed')
    result=subprocess.run(args,input="\n".join(records)+"\n",text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def main():
    verified=checks()
    verified['impact_holdouts']=impact_holdouts()
    selected=run([(1000.,100.,.02,.1,1.6,0)],h=.00125,constant=True,horizon=20)[0]
    assert selected['saddle_time'] is not None
    verified['selected_nominal']=selected
    if '--check' in sys.argv:
        print(json.dumps(verified,indent=2))
        return
    rows=list(product((10.,100.,1000.),(0.,10.,100.),(-.02,0.,.02),(.02,.1),(.8,.95),(0,1)))
    scratch=os.environ.get('PAPERCLIP_SCRATCH_DIR')
    # Build artifacts are transient; no compiled/generated output belongs in the repo.
    with tempfile.TemporaryDirectory(prefix='e080-',dir=scratch) as temp:
        binary=pathlib.Path(temp)/'sweep'
        subprocess.run(['c++','-O2','-std=c++17',str(pathlib.Path(__file__).with_name('seat_sweep.cpp')),
                        '-o',str(binary)],check=True)
        # Compare separately implemented RK4 runners before trusting the faster sweep.
        holdout=[(10.,10.,0.,.02,.95,0),(1000.,100.,.02,.1,.8,1)]
        fast=fast_run(holdout,.00125,binary,horizon=15)
        slow=run(holdout,h=.00125,horizon=15)
        for x,y in zip(fast,slow):
            assert x['saddle_time']==y['saddle_time']
            for key in ('min_q','max_q','peak_seat_force'):
                assert abs(x[key]-y[key])<1e-9
        base=fast_run(rows,.0025,binary);fine=fast_run(rows,.00125,binary)
        disagreements=[i for i,(a,b) in enumerate(zip(base,fine)) if (a['saddle_time'] is None)!=(b['saddle_time'] is None)]
        assert all(BETA*(r['seat_offset']-r['min_q'])<math.pi/2 for r in fine)
        print(json.dumps(dict(stage='population',cases=len(rows),classification_disagreements=disagreements,
                             base=base,refined_cases=fine)),flush=True)
        witnesses=[]
        for signed in (0,1):
            candidates=[i for i,r in enumerate(base) if rows[i][5]==signed and r['compression_damping']>.0 and r['saddle_time'] is not None]
            if candidates:
                i=max(candidates,key=lambda i:(rows[i][2]==0, rows[i][0],rows[i][1]))
                replay=[fast_run([rows[i]],h,binary,schedules=[base[i]['pulse_edges']],horizon=60)[0]
                        for h in (.00125,.000625,.0003125,.00015625)]
                # Independent Python fixed-time replay check, as well as pump holdouts above.
                python_replay=run([rows[i]],h=.00125,schedules=[base[i]['pulse_edges']],horizon=30)[0]
                assert replay[0]['saddle_time']==python_replay['saddle_time']
                assert abs(replay[0]['peak_seat_force']-python_replay['peak_seat_force'])<1e-8
                witnesses.append(dict(base=base[i],replay=replay))
    single=run([(100.,.5,0.,0.,f,0) for f in (.8,.95)],constant=True,horizon=20)
    assert all(r['saddle_time'] is None for r in single)
    summary=[]
    for eta,signed in product((0.,10.,100.),(False,True)):
        sub=[r for r in fine if r['compression_damping']==eta and r['signed']==signed]
        summary.append(dict(compression_damping=eta,signed=signed,crossings=sum(r['saddle_time'] is not None for r in sub),cases=len(sub)))
    print(json.dumps(dict(stage='verification',threshold=A_STEP,verification=verified,
        summary=summary,witnesses=witnesses)),flush=True)

if __name__=='__main__':main()
