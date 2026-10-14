#!/usr/bin/env python3
"""End-joining bounds: illustrative manual timings, no process qualification."""
import json
import math
from closed_stock import route, ledger


def schedule(n, seats, carriers, touch_s, dwell_s, batch_s=0):
    """One operator; whole carriers held until dwell and unloading finish.

    touch_s covers all per-body work including unload/gauge. Charging it before
    dwell conservatively withholds reuse; no separate cure operator is invented.
    """
    free=[0.]*carriers
    operator=0.; busy=0.
    for start in range(0,n,seats):
        k=min(seats,n-start)
        i=min(range(carriers),key=free.__getitem__)
        operator=max(operator,free[i])
        work=k*touch_s+batch_s
        operator+=work; busy+=work
        free[i]=operator+dwell_s
    return dict(hands_h=busy/3600, elapsed_h=max(free)/3600,
                cure_wait_h=(operator-busy)/3600)


def comparison(n, route_name, carriers=1):
    # Explicit candidate operation lists, not measured time-motion data.
    # Both: deburr twice, load tube/cap/nut, seat, unload, gauge = 8 touches.
    # Adhesive adds two doses; stake adds two shared press/reorientation cycles.
    touches=10 if route_name=='adhesive' else 8
    dwell=10800 if route_name=='adhesive' else 0
    outputs=[]
    for j,sec in enumerate((5,15)):
        old=route(n); base=ledger(n)['base_maker_h'][j]
        cut=(old['gang_groups']*(60,180)[j]+old['saw_strokes']*(5,15)[j])/3600
        run=schedule(n,16,carriers,touches*sec,dwell,
                     0 if route_name=='adhesive' else (20,60)[j])
        # Retain cutting/setup base; extra shared joining fixture setup is explicit.
        fixed=base+cut+(4,12)[j]+(2,4)[j]
        outputs.append(dict(**run,total_maker_h=fixed+run['hands_h'],
                            serial_build_h=fixed+run['elapsed_h'],
                            touches=n*touches,carrier_seats=16*carriers))
    return outputs


def checks():
    # One carrier has no overlap; independent closed-form boundary.
    for n in (1,16,17,1024):
        r=schedule(n,16,1,50,10800)
        assert math.isclose(r['elapsed_h'],(n*50+math.ceil(n/16)*10800)/3600)
        assert math.isclose(schedule(n,16,1,40,0,20)['elapsed_h'],
                            (n*40+math.ceil(n/16)*20)/3600)
    # Unlimited carriers hides waiting between loads, not the final dwell.
    assert math.isclose(schedule(1024,16,64,50,10800)['elapsed_h'],1024*50/3600+3)
    previous=float('inf')
    for carriers in (1,4,8,16,64):
        r=schedule(1024,16,carriers,50,10800)
        assert r['elapsed_h']<=previous
        assert math.isclose(r['hands_h'],1024*50/3600)
        previous=r['elapsed_h']
    # Batch parallelism cannot erase individual handling.
    assert schedule(1024,1024,1,50,0)['hands_h']==schedule(1024,16,1,50,0)['hands_h']
    for n in (1024,4096,6400):
        assert comparison(n,'stake')[0]['touches']==8*n


if __name__=='__main__':
    checks()
    print(json.dumps({str(n):{'adhesive_1':comparison(n,'adhesive'),
                               'adhesive_16':comparison(n,'adhesive',16),
                               'stake':comparison(n,'stake')}
                      for n in (1024,4096,6400)},indent=2))
