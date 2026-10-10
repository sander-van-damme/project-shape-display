#!/usr/bin/env python3
"""E-106 deterministic shared-pressure vs independently throttled control.
Units mm, N, s, MPa. All coefficients/loads/delays are bounded assumptions.
No component, sealing, sensor or manufacturing qualification is implied.
"""
from functools import lru_cache
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('e104', Path(__file__).parents[1]/'E-104/valve_head_screen.py')
e104 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = e104
spec.loader.exec_module(e104)
AREA = math.pi  # 2-mm bore
PUMP = 8e6/60


@lru_cache(maxsize=4096)
def loss(v, cd=.6, mu=.001):
    """E-105 full .35-mm lift: inertial serial ports + radial seat viscosity."""
    areas = (math.pi*(1.4**2-.8**2)/4, math.pi*1.4*.35, math.pi*.8**2/4)
    q = AREA*v*1e-9
    inertial = 500*q*q*sum(1/(cd*a*1e-6)**2 for a in areas)
    viscous = 6*mu*math.log(1.1/.7)/(math.pi*(.35e-3)**3)*q
    return (inertial+viscous)/1e6


def speed(dp, cd=.6, mu=.001):
    if dp <= 0: return 0.
    linear = 2*loss(1,cd,mu)-loss(2,cd,mu)/2
    quad = loss(1,cd,mu)-linear
    return 2*dp/(linear+math.sqrt(linear*linear+4*quad*dp))


def events(heights, velocity):
    """Exact completion events at piecewise constant pressure/flow; no latency.
    velocity(active indices) recomputes speeds after individual closure.
    """
    left = list(heights)
    elapsed = volume = 0.
    while (active := [i for i,h in enumerate(left) if h>1e-10]):
        vs = velocity(active)
        if min(vs.values()) <= 0: raise ValueError('stall/reverse-risk')
        dt = min(left[i]/vs[i] for i in active)
        for i in active:
            dh = min(left[i],vs[i]*dt)
            volume += AREA*dh
            left[i] -= dh
        elapsed += dt
    assert math.isclose(volume,AREA*sum(heights),abs_tol=1e-7)
    return elapsed


def pressure_rates(bs, u, active, cd, mu):
    """Signed pressure u: supply for up, minus return for down; b similarly.
    Pump saturation reduces u, rather than scaling unequal-load flows equally.
    Reject if the source cannot keep ALL opened channels moving forward.
    """
    def rates(p): return {i:speed(p-bs[i],cd,mu) for i in active}
    vs = rates(u)
    if AREA*sum(vs.values()) > PUMP:
        lo, hi = max(bs[i] for i in active), u
        if AREA*sum(rates(lo).values()) >= PUMP:
            raise ValueError('pump-induced stall/reverse-risk')
        for _ in range(45):
            mid = (lo+hi)/2
            if AREA*sum(rates(mid).values()) > PUMP: hi=mid
            else: lo=mid
        vs = rates(lo)
    return vs


def cohorts(intervals):
    """Minimum point cover of closed 1D intervals; fastest allowed first point.
    Empty individual interval is a robust control failure, not another group.
    """
    if any(lo>hi for lo,hi in intervals): raise ValueError('empty fine-pressure interval')
    todo = set(range(len(intervals)))
    groups=[]
    while todo:
        p = min(intervals[i][1] for i in todo)
        group = sorted(i for i in todo if intervals[i][0] <= p <= intervals[i][1])
        groups.append((p,group))
        todo.difference_update(group)
    return groups


def thresholds(channels, sign, spread, bias=.3, drag=.05, common_drag=0.):
    # Explicit load levels correlated across each row; no iid or probabilities.
    # Adjacent up/down pairs receive the same level; both signs sample the range.
    return [((bias+spread*((c//2)%8)/7 + (drag+common_drag if sign==1 else -drag-common_drag))/AREA)*sign
            for c,h in channels]


@lru_cache(maxsize=4096)
def phase(channels, sign, mode, error=.3, spread=.1, eps=0., cd=.6, mu=.001,
          transition=.01, common_drag=0., delay=.002):
    if not channels: return (0.,0,0.)
    hs=[abs(h) for _,h in channels]
    bs=thresholds(channels,sign,spread,common_drag=common_drag)
    lower,upper=(.01,.5) if sign==1 else (-.5,-.01)
    slow=(error-.05)/delay
    if mode=='binary':
        u=min(upper-eps,max(lower+eps,max(bs)+loss(400,cd,mu)+eps))
        if u-eps<=max(bs): raise ValueError('unloaded lowering/pressure range')
        vmax=[speed(u+eps-b,cd,mu) for b in bs]  # no inherited 400-mm/s cap
        bands=[min(h,v*delay+.05) for h,v in zip(hs,vmax)]
        coarse=[h-band for h,band in zip(hs,bands)]
        t=events(coarse,lambda active:pressure_rates(bs,u-eps,active,cd,mu))
        cycles=int(max(coarse)>0)
        # Lower speed floor controls finite completion time; upper bounds error.
        intervals=[(max(lower+eps,b+loss(slow/2,cd,mu)+eps),
                    min(upper-eps,b+loss(slow,cd,mu)-eps)) for b in bs]
        groups=cohorts(intervals)
        for p,idx in groups:
            local_bs=[bs[i] for i in idx]
            t+=events([bands[i] for i in idx],lambda active:pressure_rates(local_bs,p-eps,active,cd,mu))
        cycles+=len(groups)
    else:
        # Optimistic independently throttled heads: per-channel regulation exists,
        # can hold speeds below available pressure capacity. No gap accuracy claim.
        fast=[min(400.,speed(upper-eps-b,cd,mu)) for b in bs]
        if min(fast)<=0: raise ValueError('unloaded lowering/pressure range')
        bands=[min(h,v*delay+.05) for h,v in zip(hs,fast)]
        def regulated(caps):
            def rates(active):
                scale=min(1.,PUMP/(AREA*sum(caps[i] for i in active)))
                return {i:caps[i]*scale for i in active}
            return rates
        coarse=[h-band for h,band in zip(hs,bands)]
        t=events(coarse,regulated(fast))
        t+=events(bands,regulated([min(slow,v) for v in fast]))
        cycles=int(max(coarse)>0)+1
    # First pressure direction charges inherited 10 ms; each additional stopped
    # group charges transition for pressure settle/open/close, including extra
    # reopen. Channels completing early wait isolated, then rejoin fine cohorts.
    return t+.010+transition*(cycles-1),cycles,max(bands)


def evaluate(work,mode,**kwargs):
    sc=e104.Scenario(bore=2.)
    total=sc.global_setup+e104.route(work,0,sc)
    retry=0.; cycles=0; band=0.
    for channels in work.values():
        row=sc.acquire_withdraw+sc.row_read_settle
        for sign in (1,-1):
            t,n,b=phase(tuple((c,h) for c,h in channels if h*sign>0),sign,mode,**kwargs)
            row+=t;cycles+=n;band=max(band,b)
        total+=row
        recovery=sc.acquire_withdraw+sc.row_read_settle
        for sign in (1,-1):
            t,_,_=phase(tuple((c,40*sign) for c,_ in channels),sign,mode,**kwargs)
            recovery+=t
        retry=max(retry,recovery)
    return dict(seconds=total+retry,cycles=cycles,max_band=band,retry=retry)


def holdout():
    # Independent fixed-step pressure-law integration and SI pressure recovery.
    bs=[.1,.102,.104];hs=[1.,4.,2.];u=.12
    exact=events(hs,lambda a:pressure_rates(bs,u,a,.6,.001))
    for dt in (.0001,.00005,.000025):
        left=hs[:];t=0.
        while max(left)>1e-10:
            for i,h in enumerate(left):
                if h>1e-10:
                    # Independent inversion by scalar bisection, no speed().
                    lo,hi=0.,2000.
                    for _ in range(35):
                        m=(lo+hi)/2
                        if loss(m)<u-bs[i]:lo=m
                        else:hi=m
                    left[i]=max(0.,h-lo*dt)
            t+=dt
        assert abs(t-exact)<=3*dt
    assert math.isclose(AREA*40*1e-9, math.pi*.001**2*.04)
    for v in (1.,75.,400.,1000.):
        assert math.isclose(speed(loss(v)),v,rel_tol=1e-10)
    assert speed(0)==0 and events([],lambda a:{})==0
    assert len(cohorts([(0,1),(.5,1.5),(2,3)]))==2
    # Independent brute-force cover validates greedy for overlapping intervals.
    ints=[(0,2),(1,3),(2.5,4),(3.5,5)]
    ends=[hi for _,hi in ints]
    best=min(n for n in range(1,5) if any(all(any(lo<=p<=hi for p in ps) for lo,hi in ints)
             for ps in itertools.combinations(ends,n)))
    assert len(cohorts(ints))==best
    bs=[.1]*80
    vs=pressure_rates(bs,.2,list(range(80)),.6,.001)
    assert math.isclose(AREA*sum(vs.values()),PUMP,rel_tol=1e-10)
    assert math.isclose(events([40.]*80,lambda a:pressure_rates(bs,.2,a,.6,.001)),80*AREA*40/PUMP)
    # Single branch pressure change matches equivalent opposite load change.
    assert math.isclose(speed(.2-.1),speed(.21-.11))
    # Necessary pressure-window obstruction, independent of group algorithm.
    assert .1/7 > AREA*loss(225)  # all 8 levels need separate fine settings
    try:
        cohorts([(1.,0.)])
        raise AssertionError('invalid interval accepted')
    except ValueError:
        pass
    return 'PASS: inverse/SI units, volume, pump limit, interval cover, event/step refinement'


def main():
    report={'checks':holdout(),'pressure_windows':[],'cases':[]}
    for error,cd,mu in itertools.product((.2,.3,.5),(.4,.6,.8),(.001,.1)):
        slow=(error-.05)/.002
        width=loss(slow,cd,mu)-loss(slow/2,cd,mu)
        report['pressure_windows'].append(dict(error=error,cd=cd,mu=mu,width_pa=width*1e6,
                                               force_width_n=width*AREA,half_error_limit_pa=width*5e5,
                                               positive_speed_force_width_n=loss(slow,cd,mu)*AREA))
    workloads=e104.workloads()
    for mode,error,spread,eps,name in itertools.product(('binary','throttled'),(.2,.3,.5),(0.,.01,.1),(0.,.0001,.001),('checkerboard','minority_down','graded_mixed','mixed_sparse')):
        try: result=evaluate(workloads[name],mode,error=error,spread=spread,eps=eps)
        except ValueError as exc: result={'reject':str(exc)}
        report['cases'].append(dict(mode=mode,error=error,spread=spread,pressure_bound_pa=eps*1e6,work=name,**result))
    report['fast_transition'] = []
    for mode,error,spread,name in itertools.product(('binary','throttled'),(.2,.3,.5),(0.,.01,.1),('checkerboard','minority_down','graded_mixed','mixed_sparse')):
        try: result=evaluate(workloads[name],mode,error=error,spread=spread,transition=.002)
        except ValueError as exc: result={'reject':str(exc)}
        report['fast_transition'].append(dict(mode=mode,error=error,spread=spread,work=name,**result))
    report['local'] = []
    patch={r:[(c,40*(-1 if (r+c)%2 else 1)) for c in range(10)] for r in range(10)}
    for mode in ('binary','throttled'):
        report['local'].append(dict(mode=mode,**evaluate(patch,mode,error=.5,spread=.1,transition=.002)))
    report['sensitivity']=[]
    for mode,cd,mu,drag,transition in itertools.product(('binary','throttled'),(.4,.8),(.001,.1),(0.,.22),(.002,.01)):
        try: result=evaluate(workloads['checkerboard'],mode,error=.5,spread=.1,cd=cd,mu=mu,common_drag=drag,transition=transition)
        except ValueError as exc: result={'reject':str(exc)}
        report['sensitivity'].append(dict(mode=mode,cd=cd,mu=mu,common_drag=drag,transition=transition,**result))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
