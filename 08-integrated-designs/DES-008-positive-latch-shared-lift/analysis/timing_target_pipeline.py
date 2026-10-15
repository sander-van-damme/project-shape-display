#!/usr/bin/env python3
"""Conditional double-buffer target-programming flow-shop lower comparator."""
import importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('r',Path(__file__).with_name('timing_retirement.py'));r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
tp=r.tp

def action(row,event=.08):
    t=0
    for sign in (1,-1):
        levels=sorted({sign*d for d in row if sign*d>0})
        if not levels:continue
        t+=2*event+tp.move(.3,20,800);last=0
        for h in levels:t+=tp.move(h-last,80,800)+3*event+2*tp.move(.3,20,800);last=h
        t+=tp.move(levels[-1],80,800)
    return t

def schedule(a,b,banks=8,program=2,undock=0):
    n=len(a);d=tp.stats(a,b)['delta'];records=[]
    if not any(any(row) for row in d):return dict(seconds=0)
    for k in range(banks):
        lo=n*k//banks;hi=n*(k+1)//banks;last=lo;durations=[]
        for y in range(lo,hi):
            if not any(d[y]):continue
            durations.append(action(d[y])+tp.move((y-last)*406.4/n)+2*tp.move(undock,80,800));last=y
        if not durations:records.append(0);continue
        elapsed=program+sum(max(program,a) for a in durations[:-1])+durations[-1]+.15*len(durations)
        elapsed+=tp.move((last-lo)*406.4/n)+max(durations)+program # complete row retry includes new programming
        records.append(elapsed)
    return dict(seconds=4+max(records),banks=records)
