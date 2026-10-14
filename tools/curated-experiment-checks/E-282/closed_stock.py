#!/usr/bin/env python3
"""Closed hollow-stock extension of E-282; bounds, not production qualification."""
import json
import math
from forming import ledger


def route(n, bar=2600., price=4.93, gang=8, usable=1.):
    length, kerf, trim = 124., 1., 2.
    attempts = math.ceil(n/usable)
    per_bar = math.floor((bar-trim)/(length+kerf))
    bars = math.ceil(attempts/per_bar)
    groups = math.ceil(bars/gang)
    # Conservative full-bar batches; extra blanks become spares, not free yield.
    strokes = groups*per_bar
    produced = bars*per_bar
    base = ledger(n)['base_maker_h']
    maker = [base[j]+(4,12)[j]+(groups*(60,180)[j]+strokes*(5,15)[j]
             +attempts*4*(10,30)[j])/3600 for j in (0,1)]
    return dict(sites=n, attempts=attempts, per_bar=per_bar, bars=bars,
                tube_EUR=bars*price, stock_m=bars*bar/1000,
                gang_groups=groups, saw_strokes=strokes, blanks=produced,
                end_joins=2*attempts, manual_body_operations=4*attempts,
                # Assumed density 2.7 g/cm3; nominal square wall section only.
                finished_tube_kg=n*36*length*2.7/1e6,
                self_weight_N_per_tube=36*length*2.7/1e6*9.81,
                maker_h=maker, retained_nut_shank_comparison_h=n*2211/10800,
                removed_channel_comparison_h=n*4057/10800,
                fits_pitch=406.4/math.isqrt(n)>10,
                waste_mm3=(bars*bar-n*length)*36)


def checks():
    for n in (1024,4096,6400):
        a=route(n)
        # Independent sequential cut replay, including initial end trim.
        remaining=2600-2; count=0
        while remaining>=125:
            remaining-=125; count+=1
        assert count==a['per_bar']==20
        assert (a['bars']-1)*count<n<=a['bars']*count
        assert a['saw_strokes']*8>=a['blanks']>=n
        assert a['fits_pitch']==(n==1024)
        assert math.isclose(n*36*124+a['waste_mm3'],a['stock_m']*1000*36)
        assert route(n,usable=.8)['bars']>=a['bars']
    assert route(1024)['bars']==52
    assert route(1024,bar=1000,price=2.75)['bars']==147
    assert route(1024)['saw_strokes']==140
    assert route(1024,usable=.8)['bars']==64
    # Cap/nut joins remain individual even with arbitrary cutting parallelism.
    assert route(1024,gang=1)['end_joins']==route(1024,gang=1024)['end_joins']==2048


if __name__=='__main__':
    checks()
    print(json.dumps(dict(routes=[route(n) for n in (1024,4096,6400)],
                         one_m_control=route(1024,bar=1000,price=2.75),
                         yield_control=route(1024,usable=.8)),indent=2))
