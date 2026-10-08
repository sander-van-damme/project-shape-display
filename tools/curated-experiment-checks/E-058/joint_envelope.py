"""Joint conditional envelope; no prices, process priors or hardware claims.
Retains row_screen's per-station index allocation to isolate head-count/cost
coupling. Full-station retries include motion/contact/read, but no re-index.
"""
import itertools
import json
import math
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "row_screen", Path(__file__).resolve().parents[1]/"E-050"/"row_screen.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def cycle(s):
    return max(sum(base.move(d, s['v'], s['a']) for d in
                   (old, abs(new-old), new))
               for old, new in itertools.product(range(0, 41, 10), repeat=2)
               if old != new) + s['contact'] + s['read']


def seconds(rows, scenario, retries):
    s = base.SCENARIOS[scenario]
    index = max(s['index'], base.move(base.PITCH*rows, s['v'], s['a']))
    return s['overhead'] + math.ceil(80/rows)*(cycle(s)+index) + retries*cycle(s)


def allowance(rows, ceiling, reserve, cell):
    return (ceiling-reserve-6400*cell)/(80*rows)


def regional_stations(rows, start, height=5):
    # Fixed row partition: do not repack the bank to favor each request.
    return (start+height-1)//rows-start//rows+1


def verify():
    for name, s in base.SCENARIOS.items():
        for rows in (1, 2):
            assert math.isclose(seconds(rows,name,s['retry']),
                                base.evaluate('rack',rows*80,name)[0])
        for rows in range(1,81):
            assert math.isclose(seconds(rows,name,1)-seconds(rows,name,0),cycle(s))
            assert math.isclose(allowance(rows,500,250,.02)*80*rows+250+128,500)
            for start in range(76):
                assert regional_stations(rows,start)==len({r//rows for r in range(start,start+5)})
    # Independent triangular/trapezoidal calculation for fast 80-head case.
    assert math.isclose(seconds(1,'fast',0),2+80*(.12+.07+.07+.05+2*math.sqrt(5.08/20000)))
    assert allowance(1,500,250,.05)<0
    assert regional_stations(2,1)==3
    assert regional_stations(3,2)==3 and regional_stations(3,0)==2


def main():
    verify()
    result=[]
    for scenario,retries in itertools.product(base.SCENARIOS,(0,1,8)):
        candidates=[dict(rows=r,heads=80*r,seconds=seconds(r,scenario,retries)) for r in range(1,81)]
        feasible=[x for x in candidates if x['seconds']<30]
        best=min(feasible,key=lambda x:x['heads']) if feasible else None
        # With positive channel price and fixed reserve/cell spend, the fewest
        # timing-feasible heads maximize price allowance, even if T is nonmonotone.
        result.append(dict(scenario=scenario,retries=retries,minimum=best,
            rejected_head_counts=[x['heads'] for x in candidates if x['seconds']>=30],
            allowances=[] if best is None else [dict(ceiling=c,reserve=b,cell=p,
                channel_usd=allowance(best['rows'],c,b,p))
                for c,b,p in itertools.product((400,500),(150,250,350),(0,.02,.05))],
            regional_station_range=None if best is None else [
                min(regional_stations(best['rows'],i) for i in range(76)),
                max(regional_stations(best['rows'],i) for i in range(76))]))
    print(json.dumps(dict(evidence='deterministic conditional bounds; not BOM or qualification',
        cases=720,scenarios=result),indent=2))

if __name__=='__main__':
    main()
