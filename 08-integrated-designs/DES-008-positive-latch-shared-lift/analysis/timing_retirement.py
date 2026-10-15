#!/usr/bin/env python3
"""Stopped threshold retirement with three-state passive lane memory.
Conditional timing only; no proof of latch/ground-pawl geometry.
"""
import importlib.util,itertools,json,math
from pathlib import Path
s=importlib.util.spec_from_file_location('pawl',Path(__file__).with_name('workload_variants.py'));pawl=importlib.util.module_from_spec(s);s.loader.exec_module(pawl)
tp=pawl.tp

def schedule(a,b,banks=8,writers=8,dwell=.04,event=.08,mode='indexed',v=80,accel=800,common=4,dirty_only=False):
    n=len(a);p=406.4/n;groups=math.ceil(n/writers);d=tp.stats(a,b)['delta'];banks_ledgers=[]
    if not any(any(r) for r in d):return dict(seconds=0,ledger={})
    for bank in range(banks):
        lo=n*bank//banks;hi=n*(bank+1)//banks;pos=lo
        ledger=dict(seek=0,program=0,support=0,loaded_motion=0,microtravel=0,empty_return=0,home=0,retry=0)
        flag=[False]*n;writerpos=0;direction=1;masks=0;dirtywrites=0;longest=0;rows=0
        for y in range(lo,hi):
            if not any(d[y]):continue
            rowstart=sum(ledger.values());rows+=1
            ledger['seek']+=tp.move((y-pos)*p);pos=y
            for sign in (1,-1):
                targets=sorted({sign*x for x in d[y] if sign*x>0})
                if not targets:continue
                phase_masks=[[sign*x>0 for x in d[y]]]+[[sign*x==h for x in d[y]] for h in targets]
                for phase,mask in enumerate(phase_masks):
                    addresses=[j for j in range(groups) if not dirty_only or any(mask[x]!=flag[x] for x in range(j,n,groups))]
                    if mode=='indexed':
                        addresses.sort(reverse=direction<0);t=0
                        for j in addresses:t+=tp.move((j-writerpos)*p,400,4000)+dwell;writerpos=j
                        if addresses:direction*=-1
                    elif mode=='continuous':
                        # Favorable physics comparator: a moving synchronized
                        # writer writes over each pitch interval; dwell is
                        # minimum time per address, no free impossible bit rate.
                        # Requires qualified on-the-fly mechanism; not assumed built.
                        span=(groups-1)*p
                        t=max(tp.move(span,400,4000),groups*dwell)
                        writerpos=groups-1 if writerpos==0 else 0
                    else:raise ValueError(mode)
                    ledger['program']+=t;masks+=1;dirtywrites+=len(addresses);flag=mask[:]
                    if phase==0:
                        # dog capture, frame-height release tongue withdraw
                        ledger['support']+=2*event
                        ledger['microtravel']+=tp.move(.3,20,accel)
                    else:
                        h=targets[phase-1];last=targets[phase-2] if phase>1 else 0
                        ledger['loaded_motion']+=tp.move(h-last,v,accel)
                        # Ground-pawl restore, dog retract; one settle/check.
                        ledger['support']+=3*event
                        # Conservative .3mm seat and .3mm lift to retain support
                        # separation at the next stop; final lift overcounts.
                        ledger['microtravel']+=2*tp.move(.3,20,accel)
                ledger['empty_return']+=tp.move(targets[-1],v,accel)
            longest=max(longest,sum(ledger.values())-rowstart)
        ledger['home']=tp.move((pos-lo)*p)+tp.move(writerpos*p,400,4000)
        ledger['retry']=longest
        banks_ledgers.append((ledger,masks,dirtywrites,rows))
    critical,masks,dirtywrites,rows=max(banks_ledgers,key=lambda x:sum(x[0].values()))
    return dict(seconds=common+sum(critical.values()),ledger=dict(common=common,**critical),critical_bank_masks=masks,
        critical_bank_address_writes=dirtywrites,critical_bank_rows=rows,active_writers=writers*banks,
        passive_3state_lanes=n*banks,writer_positions=groups)
