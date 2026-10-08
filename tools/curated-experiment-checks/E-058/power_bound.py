"""Necessary SI energy/force bounds, deterministic scenarios, no measured priors."""
import importlib.util
import itertools
import json
import math
from pathlib import Path
spec = importlib.util.spec_from_file_location('joint', Path(__file__).parents[1]/'E-050/joint_envelope.py')
j = importlib.util.module_from_spec(spec)
spec.loader.exec_module(j)
G, TRAVEL = 9.81, .040


def bound(rows, scenario, mass, resistance, electrical_watts, efficiency):
    s = j.base.SCENARIOS[scenario]
    stations = math.ceil(80/rows)
    index = max(s['index'], j.base.move(5.08*rows, s['v'], s['a']))
    move = j.base.move(40, s['v'], s['a'])
    # Uniform 0 -> 40: each bank starts at zero, lifts, seats, returns empty.
    # Energy bound ignores acceleration losses and empty-head energy. Power
    # means electrical budget actually available to lift, excluding auxiliaries.
    force = mass*G+resistance
    work = 6400*force*TRAVEL
    lift = sum(max(move, min(rows,80-r)*80*force*TRAVEL /
                   (electrical_watts*efficiency)) for r in range(0,80,rows))
    uniform = s['overhead'] + stations*(move+s['contact']+s['read']+index)+lift
    nominal = j.seconds(rows, scenario, 0)
    return dict(rows=rows, scenario=scenario, mass_kg=mass, resistance_N=resistance,
                electrical_W=electrical_watts, efficiency=efficiency,
                lift_work_J=work, uniform_lower_s=uniform,
                arbitrary_lower_s=max(nominal,uniform),
                rejected=max(nominal,uniform)>=30,
                peak_channel_force_N=force+mass*s['a']/1000,
                synchronized_peak_input_W=80*rows*(force+mass*s['a']/1000)*s['v']/1000/efficiency)


def verify():
    # Independent work conservation and limiting cases.
    x=bound(3,'central',.02,1,25,.5)
    assert math.isclose(x['lift_work_J'],6400*(.02*9.81+1)*.04)
    assert bound(3,'central',0,0,25,.5)['arbitrary_lower_s']==j.seconds(3,'central',0)
    for r in (1,2,3):
        assert sum(min(r,80-i)*80 for i in range(0,80,r))==6400
        a=bound(r,'central',.05,10,25,.25)
        b=bound(r,'central',.05,10,50,.25)
        assert a['arbitrary_lower_s']>=b['arbitrary_lower_s']
        assert a['uniform_lower_s']>=a['lift_work_J']/(25*.25)
    # Force capacity alone cannot establish speed/power feasibility.
    assert bound(3,'central',.05,10,25,.25)['rejected']


if __name__=='__main__':
    verify()
    cases=[bound(*v) for v in itertools.product((1,2,3),('fast','central'),
           (.005,.020,.050),(0,1,10),(25,50,100),(.25,.50,.75))]
    print(json.dumps(dict(cases=len(cases), rejected=sum(x['rejected'] for x in cases),
          new_power_rejections=sum(x['rejected'] and j.seconds(x['rows'],x['scenario'],0)<30 for x in cases),
          examples=[bound(3,'central',.02,r,50,.5) for r in (0,1,10)],
          results=cases),indent=2))
