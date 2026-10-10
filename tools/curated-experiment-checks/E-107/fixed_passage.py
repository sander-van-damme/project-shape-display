#!/usr/bin/env python3
"""E-107: deterministic discrete valve restriction synthesis; mm,N,s,MPa.
Straight Newtonian no-slip passages; all process/fluid/load ranges are assumptions.
No CFD, fabrication, probability, seal or hardware qualification.
"""
from dataclasses import dataclass, asdict
from functools import lru_cache
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

spec=importlib.util.spec_from_file_location('e106',Path(__file__).parents[1]/'E-106/pressure_control.py')
e106=importlib.util.module_from_spec(spec);sys.modules[spec.name]=e106;spec.loader.exec_module(e106)
A=e106.AREA

@dataclass(frozen=True)
class Passage:
    family:str
    small:float
    length:float
    width:float=.8

    def section(self,delta=0.):
        d=(self.small+delta)*1e-3
        w=(self.width+delta)*1e-3
        if d<=0 or w<=0: raise ValueError('nonpositive passage')
        if self.family=='round': return math.pi*d*d/4,d
        h,w=sorted((d,w))
        return h*w,2*h*w/(h+w)

    def resistance(self,mu,delta=0.,length_scale=1.,terms=101):
        d=(self.small+delta)*1e-3;L=self.length*length_scale*1e-3
        if d<=0: raise ValueError('nonpositive passage')
        if self.family=='round': return 128*mu*L/(math.pi*d**4)
        h,w=sorted((d,(self.width+delta)*1e-3))
        f=1-192*h/(math.pi**5*w)*sum(math.tanh(n*math.pi*w/(2*h))/n**5 for n in range(1,2*terms,2))
        return 12*mu*L/(w*h**3*f)


@lru_cache(maxsize=20000)
def coefficients(p,mu,delta=0.,length_scale=1.,entry=2.,cd=.6):
    # dp = r*v + k*v^2, includes E-105 full-open ports in series.
    base_r=2*e106.loss(1,cd,mu)-e106.loss(2,cd,mu)/2
    base_k=e106.loss(1,cd,mu)-base_r
    area,_=p.section(delta)
    return (base_r+p.resistance(mu,delta,length_scale)*A*1e-15,
            base_k+entry*500*(A*1e-9/area)**2/1e6)


def loss(v,co):
    r,k=co;return r*v+k*v*v


def speed(dp,co):
    if dp<=0:return 0.
    r,k=co
    return 2*dp/(r+math.sqrt(r*r+4*k*dp))


@dataclass(frozen=True)
class Bounds:
    name:str
    delta:float
    mu_lo:float
    mu_hi:float
    entry_lo:float=0.
    entry_hi:float=2.
    length_error:float=.02
    eps:float=.001
    drag_extra:float=0.


def extrema(p,b):
    # Larger cross-section, shorter length, lower viscosity/entry => fastest.
    fast=coefficients(p,b.mu_lo,b.delta,1-b.length_error,b.entry_lo)
    slow=coefficients(p,b.mu_hi,-b.delta,1+b.length_error,b.entry_hi)
    return fast,slow


def fine_pressure(bs,fast,sign,error,eps):
    lower,upper=(.01,.5) if sign==1 else (-.5,-.01)
    cap=(error-.05)/.002
    # Fastest geometry + pressure upper error cannot exceed terminal speed cap.
    u=min(upper-eps,min(bs)+loss(cap,fast)-eps)
    if u<lower+eps or u-eps<=max(bs):raise ValueError('empty forward/accuracy pressure window')
    return u


@lru_cache(maxsize=8192)
def coarse_phase(channels,sign,b,coarse):
    hs=[abs(h) for _,h in channels]
    bs=e106.thresholds(channels,sign,.1,common_drag=b.drag_extra)
    upper=.5 if sign==1 else -.01
    # E-105 full-open ports, selected fluid. Pressure targets 400 at hardest load.
    u=min(upper-b.eps,max(bs)+e106.loss(400,.6,b.mu_hi)+b.eps)
    if u-b.eps<=max(bs):raise ValueError('unloaded lowering')
    vmax=[e106.speed(u+b.eps-x,.6,b.mu_lo) for x in bs]
    if coarse=='ideal':vmax=[min(400.,v) for v in vmax]
    bands=[min(h,v*.002+.05) for h,v in zip(hs,vmax)]
    def coarse_rates(active):
        if coarse=='binary':return e106.pressure_rates(bs,u-b.eps,active,.6,b.mu_hi)
        vs={i:min(400.,e106.speed(u-b.eps-bs[i],.6,b.mu_hi)) for i in active}
        scale=min(1.,e106.PUMP/(A*sum(vs.values())))
        return {i:v*scale for i,v in vs.items()}
    t=e106.events([h-g for h,g in zip(hs,bands)],coarse_rates)
    return t,bands,bs,any(h>g for h,g in zip(hs,bands))


@lru_cache(maxsize=65536)
def phase(channels,sign,p,b,error=.5,coarse='binary',transition=.002):
    if not channels:return (0.,0.,0.)
    t,bands,bs,has_coarse=coarse_phase(channels,sign,b,coarse)
    fast,slow=extrema(p,b)
    uf=fine_pressure(bs,fast,sign,error,b.eps)
    speeds=[speed(uf-b.eps-x,slow) for x in bs]
    # Even 80 channels at the tested terminal caps fit 8 L/min.
    assert A*len(bs)*(error-.05)/.002 < e106.PUMP
    t+=e106.events(bands,lambda active:{i:speeds[i] for i in active})
    return t+.010+transition*int(has_coarse),max(bands),min(speeds)


def evaluate(work,p,b,**kw):
    sc=e106.e104.Scenario(bore=2.)
    total=sc.global_setup+e106.e104.route(work,0,sc);retry=0.;band=0.;vmin=math.inf
    for channels in work.values():
        row=sc.acquire_withdraw+sc.row_read_settle
        for sign in (1,-1):
            t,g,v=phase(tuple((c,h) for c,h in channels if sign*h>0),sign,p,b,**kw)
            row+=t;band=max(band,g)
            if v:vmin=min(vmin,v)
        total+=row
        recovery=sc.acquire_withdraw+sc.row_read_settle
        for sign in (1,-1):
            t,_,_=phase(tuple((c,sign*40) for c,_ in channels),sign,p,b,**kw)
            recovery+=t
        retry=max(retry,recovery)
    return dict(seconds=total+retry,retry=retry,band=band,min_fine_speed=vmin)


def population():
    # Two cross-section families of the SAME restriction topology. Deterministic;
    # axial straight passages extend beyond 5.08 pitch, no serpentines assumed.
    for family,d,L in itertools.product(('round','slot'),(.15,.2,.25,.3,.4,.5,.6,.8),(2.,5.,10.,20.,40.)):
        yield Passage(family,d,L)


def checks():
    p=Passage('round',.4,10.)
    # Independent SI Poiseuille and quadratic pressure reconstruction.
    q=1e-7;dp=p.resistance(.01)*q
    assert math.isclose(q,math.pi*(.4e-3/2)**4*dp/(8*.01*.01))
    assert math.isclose(Passage('round',.8,10).resistance(.01)*16,p.resistance(.01))
    assert math.isclose(Passage('round',.4,20).resistance(.01),2*p.resistance(.01))
    slot=Passage('slot',.2,10)
    assert math.isclose(slot.resistance(.01,terms=51),slot.resistance(.01,terms=101),rel_tol=1e-9)
    # Square duct normalized resistance 28.454..., independent published shape limit.
    square=Passage('slot',.8,10,.8)
    assert abs(square.resistance(.01)*(.8e-3)**4/(.01*.01)-28.454154)<1e-5
    co=coefficients(p,.01)
    for v in (1.,75.,225.,400.):assert math.isclose(speed(loss(v,co),co),v,rel_tol=1e-12)
    # Independent time-step holdout, roots by bisection instead of speed().
    hs=[.4,.9,.6];dps=[.04,.06,.08]
    exact=e106.events(hs,lambda ids:{i:speed(dps[i],co) for i in ids})
    errors=[]
    for dt in (1e-4,5e-5,2.5e-5):
        left=hs[:];elapsed=0.
        while max(left)>1e-10:
            for i in range(3):
                lo,hi=0.,2000.
                for _ in range(35):
                    mid=(lo+hi)/2
                    if loss(mid,co)<dps[i]:lo=mid
                    else:hi=mid
                left[i]=max(0.,left[i]-lo*dt)
            elapsed+=dt
        errors.append(abs(elapsed-exact));assert errors[-1]<=dt+1e-10
    assert speed(0,co)==0
    # Reconstruct corner guarantees at all 16 dimension/fluid/length/entry corners.
    b=Bounds('check',.025,.008,.012)
    fast,slow=extrema(p,b)
    for d,mu,le,k in itertools.product((-.025,.025),(.008,.012),(.98,1.02),(0.,2.)):
        c=coefficients(p,mu,d,le,k)
        for v in (75.,225.):assert loss(v,fast)<=loss(v,c)+1e-12<=loss(v,slow)+2e-12
    bs=[.35/A,.45/A];u=fine_pressure(bs,fast,1,.5,b.eps)
    assert max(speed(u+b.eps-x,fast) for x in bs)<=225+1e-8
    assert min(speed(u-b.eps-x,slow) for x in bs)>0
    return dict(status='PASS',step_errors=errors)


def main():
    report={'checks':checks(),'input_revision':'8c479c2','population':80,'scenarios':[]}
    detailed=[]
    workloads=e106.e104.workloads()
    bounds=[Bounds('nominal',0,.01,.01,2,2,0,0),
            Bounds('tight',.025,.008,.012),Bounds('wide_dimension',.05,.008,.012),
            Bounds('broad_fluid',.025,.001,.1),Bounds('extra_drag',.025,.008,.012,drag_extra=.22)]
    survivors=[]
    for b,coarse in itertools.product(bounds,('binary','ideal')):
        results=[];rejections={}
        for p in population():
            try:
                r=evaluate(workloads['checkerboard'],p,b,coarse=coarse)
                results.append((r['seconds'],p,r))
                detailed.append(dict(bound=b.name,coarse=coarse,passage=asdict(p),**r))
            except ValueError as exc:
                rejections[str(exc)]=rejections.get(str(exc),0)+1
                detailed.append(dict(bound=b.name,coarse=coarse,passage=asdict(p),reject=str(exc)))
        results.sort(key=lambda x:x[0]);best=results[0] if results else None
        survivors.append((b,coarse,best))
        report['scenarios'].append(dict(bounds=asdict(b),coarse=coarse,completed=len(results),rejected=rejections,
            under30=sum(t<30 for t,_,_ in results),best=None if not best else dict(passage=asdict(best[1]),**best[2])))
    report['survivor_workloads']=[]
    for b,coarse,best in survivors:
        if not best:continue
        p=best[1]
        for name in ('minority_down','graded_mixed','mixed_sparse'):
            try:r=evaluate(workloads[name],p,b,coarse=coarse)
            except ValueError as exc:r={'reject':str(exc)}
            report['survivor_workloads'].append(dict(bound=b.name,coarse=coarse,work=name,**r))
    report['sensitivity']=[]
    extra=[Bounds('known_mu',.025,.01,.01),
           Bounds('known_entry',.025,.008,.012,2,2),
           Bounds('zero_pressure_error',.025,.008,.012,eps=0.)]
    for b,error in [(x,.5) for x in extra]+[(bounds[1],e) for e in (.2,.3,1.)]:
        results=[];rejected=0
        for p in population():
            try:
                # Discriminate BOTH adverse direction splits before selection.
                rs=[evaluate(workloads[n],p,b,error=error) for n in ('checkerboard','minority_down')]
                results.append((max(r['seconds'] for r in rs),p,rs))
            except ValueError:rejected+=1
        results.sort(key=lambda x:x[0])
        report['sensitivity'].append(dict(bound=b.name,error=error,rejected=rejected,
            under30=sum(t<30 for t,_,_ in results),best=None if not results else dict(
                passage=asdict(results[0][1]),seconds=results[0][0],workloads=results[0][2])))
    # Exact nominal/bounded pressure-law envelopes, not probabilistic yield.
    # Re and L/D report where fully developed laminar interpretation is weak.
    report['model_domain']=[]
    for b,coarse,best in survivors:
        if not best:continue
        p=best[1];ar,dh=p.section(-b.delta)
        re=1000*(A*225e-9/ar)*dh/b.mu_lo
        report['model_domain'].append(dict(bound=b.name,coarse=coarse,
            cap_reynolds_upper=re,min_length_over_dh=p.length*(1-b.length_error)*1e-3/p.section(b.delta)[1]))
    # 10x10 patch at each extreme starting row and bank edge, one tight winner.
    p=next(best[1] for b,c,best in survivors if b.name=='tight' and c=='binary')
    b=bounds[1];report['local']=[]
    for row in (0,70):
        patch={r:[(c,40*(-1 if (r+c)%2 else 1)) for c in range(10)] for r in range(row,row+10)}
        for start in (0,79):
            r=evaluate(patch,p,b)
            sc=e106.e104.Scenario(bore=2.)
            r['seconds']+=e106.e104.route(patch,start,sc)-e106.e104.route(patch,0,sc)
            report['local'].append(dict(row=row,start=start,**r))
    if '--all' in sys.argv:report['population_results']=detailed
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
