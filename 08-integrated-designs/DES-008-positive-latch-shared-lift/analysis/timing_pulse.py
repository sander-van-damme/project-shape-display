#!/usr/bin/env python3
"""Screen crossed-comb support row elevators. Assumed durations only.
Fixed binary pulses vs optimized pulse subset-sum cover, exact inherited maps.
"""
import importlib.util,itertools,json,math,functools
from pathlib import Path
s=importlib.util.spec_from_file_location('tp',Path(__file__).with_name('timing_reference.py'));tp=importlib.util.module_from_spec(s);s.loader.exec_module(tp)
@functools.lru_cache(None)
def pulse_options(targets,quantum=2):
    if not targets:return [()]
    if any(t%quantum for t in targets):raise ValueError('height not representable')
    denominations=(2,4,8,10,16) if quantum==2 else (5,10,20)
    need=set(targets);best=[];minimum=math.ceil(max(targets)/max(denominations))
    # Enumerate first pulse count with subset-sum coverage. Dominated longer
    # masks may rarely win at zero write latency; screening assumes >.1s/mask.
    for count in range(minimum,9):
        for seq in itertools.combinations_with_replacement(denominations,count):
            if sum(seq)<max(targets):continue
            reachable={0}
            for d in seq:reachable|={v+d for v in reachable}
            if need<=reachable:best.append(seq)
        if best:return best
    raise AssertionError(targets)

def row_pulses(row,quantum=2,write=.2,event=.08,v=80,a=800):
    chosen=[]
    for sign in (1,-1):
        targets=tuple(sorted({sign*d for d in row if sign*d>0}))
        if not targets:continue
        # Every pulse: reader retract .04s; pickup capture .08s; column support
        # withdraw .08s; row support withdraw .08s; loaded move; row restore;
        # column restore; pickup retract; unloaded return; settle/check .08s.
        # Seven event slots: 6 mechanical strokes + check/settle. Writer
        # includes selecting, indexing, reset and verifying full 64-bit mask.
        seq=min(pulse_options(targets,quantum),key=lambda seq:sum(write+7*event+2*tp.move(d,v,a) for d in seq))
        chosen.extend(sign*d for d in seq)
    return chosen

def schedule(a,b,banks=8,quantum=2,write=.2,event=.08,v=80,accel=800,common=4,event_count=7,microtravel=0):
    n=len(a);delta=tp.stats(a,b)['delta'];bank=[]
    if not any(any(r) for r in delta):return dict(seconds=0,ledger={})
    for k in range(banks):
        lo=n*k//banks;hi=n*(k+1)//banks;pos=lo
        z=dict(seek=0,write=0,support=0,motion=0,home=0,retry=0);pulses=0;longest=0;maxpulse=0;retrypulses=0
        for y in range(lo,hi):
            row=delta[y]
            if not any(row):continue
            seq=row_pulses(tuple(row),quantum,write,event,v,accel)
            motion=sum(2*tp.move(d,v,accel)+2*tp.move(microtravel,20,accel) for d in seq)
            z['seek']+=tp.move((y-pos)*406.4/n);pos=y
            z['write']+=write*len(seq);z['support']+=event_count*event*len(seq);z['motion']+=motion
            pulses+=len(seq);maxpulse=max(maxpulse,len(seq))
            retry=(write+event_count*event)*len(seq)+motion
            if retry>longest:longest=retry;retrypulses=len(seq)
        z['home']=tp.move((pos-lo)*406.4/n);z['retry']=longest
        bank.append((z,pulses,maxpulse,retrypulses))
    critical,pulses,maxpulse,retrypulses=max(bank,key=lambda v:sum(v[0].values()))
    return dict(seconds=common+sum(critical.values()),ledger=dict(common=common,**critical),critical_bank_pulses=pulses,max_row_pulses=maxpulse,
        mask_write_budget_30s=min((30-common-sum(v for k,v in z.items() if k not in ('write','retry'))-z['retry']+write*rp)/(np+rp) for z,np,mp,rp in bank if np),retry_pulses=retrypulses)
