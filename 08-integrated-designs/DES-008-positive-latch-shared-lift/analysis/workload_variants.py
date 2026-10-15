#!/usr/bin/env python3
"""Revised one-ground-pawl/site model; preserves superseded crossed-comb screen."""
import importlib.util,itertools,json
from pathlib import Path
s=importlib.util.spec_from_file_location('comb',Path(__file__).with_name('timing_pulse.py'));comb=importlib.util.module_from_spec(s);s.loader.exec_module(comb)
tp=comb.tp

def suites(n,stroke):
    states,pairs,initial,local,extra=tp.maps(n)
    if stroke==50:return states,pairs,initial,local,extra
    # Explicit product encoding: neutral20, walls+20, ravine-20. Same physical
    # heights as inherited shallow states translated -10. 30mm deep ravine lost.
    states={k.replace('shallow:','40mm:'):[[h-10 for h in r] for r in v] for k,v in states.items() if k.startswith('shallow:')}
    flat=lambda h:[[h]*n for _ in range(n)]
    pairs={a+'>'+b:(states[a],states[b]) for a,b in itertools.permutations(states,2)}
    pairs.update({'neutral>'+k:(flat(20),v) for k,v in states.items()})
    initial={'cold>'+k:(flat(0),v) for k,v in states.items()}
    local={};step=n//8
    for name,h in states.items():
        for y in range(0,n,step):
            for x in range(0,n,step):
                target=flat(20)
                for yy in range(y,y+step):
                    for xx in range(x,x+step):target[yy][xx]=h[yy][xx]
                local[f'{name}@{x},{y}']=(flat(20),target)
    extra={'neutral_preparation':(flat(0),flat(20)),'dense40':(flat(0),flat(40)),
        'dense_opposite40':([[0 if (x+y)%2 else 40 for x in range(n)] for y in range(n)],[[40 if (x+y)%2 else 0 for x in range(n)] for y in range(n)])}
    return states,pairs,initial,local,extra
