#!/usr/bin/env python3
"""Purchased M4/open-tube route: conditional schedules and manufacturing bounds.

Catalog observations and source URLs live in E-278. No rated speed, fitted
process prior, currency forecast, delivered quote or physical qualification.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parents[1]/relative)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


c = load('coarse', 'E-276/coarse.py')
g = load('guidance', 'E-277/guidance.py')


def stock(n, stroke=50):
    # Same 80-mm guide span and 10-mm bottom/2-mm roof allocations as E-277.
    # Ends are concept envelopes, not finished joint geometry.
    length = stroke+80+6-12
    kerf, trim = 1., 2.  # mm; explicit saw/setup assumptions
    per_bar = math.floor((1000-trim)/(length+kerf))
    bars = math.ceil(n*n/per_bar)
    return dict(n=n, sites=n*n, tube_length_mm=length, pieces_per_m=per_bar,
                bars_1m=bars, tube_EUR=bars*4.95, tube_liters=n*n*36*length/1e6,
                kerf_liters=n*n*36*kerf/1e6,
                unused_stock_liters=(bars*1000-n*n*(length+kerf))*36/1e6,
                screws_INR=n*n*8.47, cuts=n*n, deburred_faces=2*n*n,
                joins=2*n*n, nut_insertions=n*n, end_parts=2*n*n,
                # Cut, deburr both ends together, nut insertion, two joins.
                extra_handling_h=[5*n*n*t/3600 for t in (10,30)],
                fine_pitch_threading_h=[n*n*turns/rps/3600 for rps in (2,1)
                                       for turns in (10/.7,)],
                # Same body replication only; does NOT fit fine/quarter pitch.
                fits_pitch=(406.4/n)>10)


def economics(n=32, k=4):
    a=stock(n); base=c.d.cost(n,k)
    # Explicit stress-test conversion factors, NOT observed exchange rates.
    # Nuts have dimensions sourced but no usable quote: USD .10-.50 allocation.
    costs=[]
    for j,(usd_eur,usd_inr,nut) in enumerate(((1.,.010,.10),(1.3,.015,.50))):
        add=a['tube_EUR']*usd_eur+a['screws_INR']*usd_inr+n*n*nut
        costs.append(dict(USD_per_EUR=usd_eur,USD_per_INR=usd_inr,nut_USD=nut,
                          added_resident_USD=add,total_USD=base['bought_USD'][j]+add,
                          # Price-per-meter allowance after all other listed terms.
                          tube_USD_per_m_limit_at1500=(1500-base['bought_USD'][j]
                              -a['screws_INR']*usd_inr-n*n*nut)/a['bars_1m']))
    return dict(n=n,k=k,base_USD=base['bought_USD'],scenarios=costs,
                maker_h=[base['maker_hours'][j]+a['extra_handling_h'][j]
                         for j in (0,1)])


def speed_threshold(k,stroke):
    _,local,_,_=c.workloads(32,stroke,True)
    # Geometry is invariant with lead/RPM; don't reroute during root finding.
    traces=[]
    for delta in local.values():
        if not any(map(any,delta)):continue
        a=c.d.schedule(delta,k,stroke,rpm=850,lead=.7)
        turns=[max(abs(v) for _,_,v in cells)/.7 for _,_,cells in c.d.stations(delta,k)]
        fixed=a['seconds']-a['spin_s']-a['retry_s']+.38
        traces.append((fixed,turns))
    def worst(rpm):
        return max(fixed+sum(c.d.h.a.r.spin(t,rpm) for t in turns)
                   +c.d.h.a.r.spin(stroke/.7,rpm) for fixed,turns in traces)
    assert math.isclose(worst(850),c.d.summary(local,k,stroke,rpm=850,lead=.7)['max_s'])
    floor=worst(1e9)  # triangular profile at inherited1000 rev/s², not free acceleration
    if floor>30:return dict(k=k,stroke=stroke,unlimited_rpm_s=floor,rpm_for30=None)
    lo,hi=1.,100000.
    for _ in range(32):
        mid=(lo+hi)/2
        if worst(mid)>30:lo=mid
        else:hi=mid
    return dict(k=k,stroke=stroke,unlimited_rpm_s=floor,rpm_for30=hi)


def checks():
    # Packing independently replayed through a finite stock length.
    for n in (32,64,80):
        a=stock(n)
        assert a['pieces_per_m']==7  # 8*125+2 exceeds 1000
        assert a['bars_1m']*a['pieces_per_m']>=n*n
        assert (a['bars_1m']-1)*a['pieces_per_m']<n*n
        assert math.isclose(a['tube_liters']+a['kerf_liters']+a['unused_stock_liters'],
                            a['bars_1m']*.036)
        assert a['fits_pitch']==(n==32)
    assert stock(32,40)['pieces_per_m']==8
    # Independent spin closed form and dense station count, two stroke ranges.
    for S in (40,50):
        for k in (4,8):
            delta=c.s.flat(32,S)
            d=c.d.schedule(delta,k,S,rpm=850,lead=.7)
            spin=(S/.7)/(850/60)+(850/60)/1000
            assert d['stations']==1024/k
            assert math.isclose(d['spin_s'],1024/k*spin)
            assert math.isclose(d['retry_s'],.38+spin)
            assert d['seconds']>=d['transaction_lower_s']
            assert d['seconds']>c.d.schedule(delta,k,S,rpm=850,lead=3)['seconds']
    # Changing only lead leaves addressing, support intent and nonspin time fixed.
    _,local,_,_=c.workloads(32,50,True)
    witness=next(v for v in local.values() if any(map(any,v)))
    a=c.d.schedule(witness,4,50,lead=3);b=c.d.schedule(witness,4,50,lead=.7)
    for key in ('stations','changed','unchanged','seek_s','return_s','dock_read_s','common_s'):
        assert a[key]==b[key]
    # Exact simultaneous linear-rate/acceleration scaling requires both changes.
    ratio=3/.7
    for mm in (.1,10,50):
        assert math.isclose(c.d.h.a.r.spin(mm/3,850,1000),
                            c.d.h.a.r.spin(mm/.7,850*ratio,1000*ratio))
    # New10mm tube nominal control inherits bound formula, not qualified error.
    fit=g.envelope(12.7,2.7,.5,80,50,.1,.1)
    assert fit['gap']>0 and fit['min_fit']>0
    assert g.envelope(12.7,2.7,.5,80,50,.3,.1)['min_fit']<0
    return 'packing/material conservation, dense independent time/count, invariant routing, lead/rate scaling, guide sensitivity'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    check=checks()
    if args.check:print(check)
    else:
        print(json.dumps(dict(checks=check,stock=[stock(n) for n in (32,64,80)],
            economics=[economics(32,k) for k in (4,8)],
            guidance=[dict(clearance=cl,width_error=e,**g.envelope(12.7,2.7,cl,80,50,e,.1))
                      for cl,e in ((.5,.1),(.5,.3),(.8,.3))],
            timings=[c.case(32,k,S,True,rpm,lead) for k in (4,8) for S in (40,50)
                     for rpm,lead in ((850,3),(850,.7),(2000,.7),(850*3/.7,.7))],
            pitch_controls=[c.case(n,4,50,True,850,.7) for n in (64,80)],
            thresholds=[speed_threshold(k,S) for k in (4,8) for S in (40,50)]),indent=2))
