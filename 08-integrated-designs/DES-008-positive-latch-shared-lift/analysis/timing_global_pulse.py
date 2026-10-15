#!/usr/bin/env python3
"""Stationary row decoder + resident pulse mask + two independently moving platens.
Timing-only discriminator. Does not prove the mechanical AND selector or masks.
"""
import importlib.util,itertools,math
from pathlib import Path
s=importlib.util.spec_from_file_location('p',Path(__file__).with_name('workload_variants.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
tp=p.tp

def row_write_cycle(total=.08):
    """Assumed serial four-stroke cycle; every duration needs physical tests.
    Establish the currently stored data vector before selecting a row, raise
    that row's gate, move data to the new vector, then lower the row gate.
    Equal quarter allocations are a timing placeholder, not motor specifications.
    """
    if not math.isfinite(total) or total<=0:raise ValueError('positive finite row-write time required')
    return dict(old_data=total/4,row_up=total/4,new_data=total/4,row_down=total/4)

def decomposition(target,seq):
    for bits in itertools.product((0,1),repeat=len(seq)):
        if sum(x*v for x,v in zip(bits,seq))==target:return bits
    raise AssertionError((target,seq))

def bank_schedule(delta,row_write=.08,quantum=5,event=.08,full_row_scan=False):
    nr=len(delta);n=len(delta[0]);flag=[[False]*n for _ in range(nr)]
    ledger=dict(program=0,support=0,motion=0,retry=0);writes=0;pulses=0;longest=0
    for sign in (1,-1):
        targets=tuple(sorted({sign*x for row in delta for x in row if sign*x>0}))
        if not targets:continue
        options=[]
        for seq in p.comb.pulse_options(targets,quantum):
            representations={v:decomposition(v,seq) for v in targets}
            masks=[[[sign*x>0 and representations[sign*x][i] for x in row] for row in delta] for i in range(len(seq))]
            previous=flag;w=0
            for mask in masks:w+=nr if full_row_scan else sum(a!=b for a,b in zip(previous,mask));previous=mask
            cost=w*row_write+sum(5*event+2*tp.move(v,80,800)+2*tp.move(.3,20,800) for v in seq)
            options.append((cost,seq,masks,w))
        _,seq,masks,_=min(options,key=lambda x:x[0])
        for row in range(nr):
            for col in range(n):
                realized=sum(step for step,mask in zip(seq,masks) if mask[row][col])
                assert realized==max(0,sign*delta[row][col]), 'pulse replay differs from request'
                if delta[row][col]==0:assert not any(mask[row][col] for mask in masks), 'unselected output admitted'
        for d,mask in zip(seq,masks):
            w=nr if full_row_scan else sum(a!=b for a,b in zip(flag,mask));writes+=w;pulses+=1
            program=w*row_write;support=5*event;motion=2*tp.move(d,80,800)+2*tp.move(.3,20,800)
            ledger['program']+=program;ledger['support']+=support;ledger['motion']+=motion
            longest=max(longest,program+support+motion);flag=mask
    # Final mask clear prevents stale admission on a subsequent command.
    w=nr if full_row_scan and pulses else sum(any(row) for row in flag);writes+=w;ledger['program']+=w*row_write
    flag=[[False]*n for _ in range(nr)]
    assert not any(any(row) for row in flag)
    # One complete widest-row-count mask + full pulse retry. Counts n rows,
    # not only observed dirty rows, so recovery does not assume stale knowledge.
    maxpulse=max((2*tp.move(v,80,800)+2*tp.move(.3,20,800)+5*event for v in (2,4,8,10,16) if quantum==2),default=0) if quantum==2 else 2*tp.move(20,80,800)+2*tp.move(.3,20,800)+5*event
    ledger['retry']=nr*row_write+maxpulse if pulses else 0
    return ledger,writes,pulses

def schedule(a,b,banks=2,row_write=.08,quantum=5,common=4,full_row_scan=False):
    n=len(a)
    if not 1<=banks<=n or int(banks)!=banks:raise ValueError('integer banks between 1 and row count required')
    if not all(len(row)==n for grid in (a,b) for row in grid) or len(b)!=n:raise ValueError('matching square arrays required')
    cycle=row_write_cycle(row_write)
    d=tp.stats(a,b)['delta']
    if not any(any(r) for r in d):return dict(seconds=0,ledger={},row_writes=0,pulses=0)
    records=[bank_schedule(d[n*k//banks:n*(k+1)//banks],row_write,quantum,full_row_scan=full_row_scan) for k in range(banks)]
    led,writes,pulses=max(records,key=lambda x:sum(x[0].values()))
    budgets=[(30-common-led['support']-led['motion']-led['retry']+math_rows*row_write)/(w+math_rows) for k,(led,w,_) in enumerate(records) for math_rows in [n*(k+1)//banks-n*k//banks] if w]
    return dict(seconds=common+sum(led.values()),ledger=dict(common=common,**led),row_writes=writes,pulses=pulses,row_write_budget_30s=min(budgets),
        active_data_channels=banks*n,resident_mask_bits=n*n,resident_ground_pawls=n*n,resident_lifting_dogs=n*n,
        row_write_cycle_seconds=cycle,full_row_scan=full_row_scan,
        critical_program_stage_seconds={k:v*writes for k,v in cycle.items()},
        bank_ledgers=[dict(seconds=sum(l.values()),ledger=l,row_writes=w,pulses=pulse) for l,w,pulse in records])
