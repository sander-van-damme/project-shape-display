"""Joint conditional envelope; no prices, process priors or hardware claims.
Retains row_screen's per-station index allocation to isolate head-count/cost
coupling. Full-station retries include motion/contact/read, but no re-index.
"""
import itertools
import json
import math
import importlib.util
from pathlib import Path
from fractions import Fraction

_spec = importlib.util.spec_from_file_location(
    "row_screen", Path(__file__).with_name("row_screen.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def cycle(s):
    return max(sum(base.move(d, s['v'], s['a']) for d in
                   (old, abs(new-old), new))
               for old, new in itertools.product(range(0, 41, 10), repeat=2)
               if old != new) + s['contact'] + s['read']


def seconds(rows, scenario, retries, stations=None):
    s = base.SCENARIOS[scenario]
    index = max(s['index'], base.move(base.PITCH*rows, s['v'], s['a']))
    return s['overhead'] + (math.ceil(80/rows) if stations is None else stations)*(cycle(s)+index) + retries*cycle(s)


def allowance(rows, ceiling, reserve, cell):
    return (Fraction(str(ceiling))-reserve-6400*Fraction(str(cell)))/(80*rows)


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


def retry_limit(rows, scenario, stations=None):
    # Strict <30: equality rejects. Correct a near-integer estimate by direct
    # evaluation using the same floating motion calculation as the schedule.
    t = seconds(rows, scenario, 0, stations)
    if t >= 30:
        return -1
    k = max(0, math.ceil((30-t)/cycle(base.SCENARIOS[scenario]))-1)
    while seconds(rows, scenario, k, stations) >= 30:
        k -= 1
    while seconds(rows, scenario, k+1, stations) < 30:
        k += 1
    return k


def main():
    verify()
    result=[]
    for scenario,retries in itertools.product(base.SCENARIOS,(0,1,8)):
        candidates=[]
        for r in range(1,81):
            counts=[regional_stations(r,i) for i in range(76)]
            workloads={'full': math.ceil(80/r), 'aligned_5x5': counts[0],
                       'adversarial_5x5': max(counts)}
            assert counts[0] == min(counts)
            timings={name: dict(stations=n, seconds=seconds(r,scenario,retries,n),
                     timing_pass=seconds(r,scenario,retries,n)<30,
                     max_full_station_retries=retry_limit(r,scenario,n))
                     for name,n in workloads.items()}
            for name,n in workloads.items():
                k=timings[name]['max_full_station_retries']
                assert seconds(r,scenario,k+1,n)>=30
                assert k==-1 or seconds(r,scenario,k,n)<30
                assert seconds(r,scenario,retries,n)<=seconds(r,scenario,retries)+1e-12
            candidates.append(dict(rows=r,heads=80*r,workloads=timings))
        feasible=[x for x in candidates if x['workloads']['full']['timing_pass']]
        result.append(dict(scenario=scenario,retries=retries,
            minimum=min(feasible,key=lambda x:x['heads']) if feasible else None,
            rejected_head_counts=[x['heads'] for x in candidates
                                  if not x['workloads']['full']['timing_pass']],
            banks=candidates))
    budgets=[]
    for r,c,b,p in itertools.product(range(1,81),(200,400,500),(150,250,350),(0,.02,.05)):
        cap=allowance(r,c,b,p)
        assert cap*(80*r)+b+6400*Fraction(str(p))==c
        budgets.append(dict(rows=r,ceiling=c,reserve=b,cell=p,
            channel_ceiling_exact_usd=str(cap), channel_ceiling_usd=float(cap),
            positive_channel_budget=cap>0,
            ceiling_inclusive=c!=200))
    print(json.dumps(dict(evidence='deterministic conditional bounds; not BOM or qualification',
        cases=720, regional_start_combinations=6080,
        budget_cases=len(budgets),scenarios=result,budgets=budgets),indent=2))

if __name__=='__main__':
    main()
