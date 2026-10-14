#!/usr/bin/env python3
"""DES-007: explicit conditional schedules, contact bounds and accounting. No measurements."""
import argparse, importlib.util, itertools, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('pv',ROOT/'tools/curated-experiment-checks/E-258/player_view.py')
pv=importlib.util.module_from_spec(spec);spec.loader.exec_module(pv)

def motion(distance, speed, accel):
    distance=abs(distance)
    return 2*math.sqrt(distance/accel) if distance<speed*speed/accel else distance/speed+speed/accel

def events(row):
    """Stopped selection; each item is (signed increment, output indices)."""
    out=[]
    for sign in (1,-1):
        last=0
        for level in sorted({sign*d for d in row if sign*d>0}):
            out.append((sign*(level-last),[i for i,d in enumerate(row) if sign*d>=level]))
            last=level
    return out

def schedule(a,b,banks=4,rpm=850,lead=3,change=.15,verify=.15,overhead=5,rewind=False):
    """Return to bank origin every transaction; no free preposition or future knowledge.
    0.20 s lower/raise head per row, 0.10 s settling, explicit inspection allowance.
    Rewind=True models finite strip rather than endless loop (paid unloaded return).
    """
    n=len(a);p=406.4/n; d=[[v-u for u,v in zip(ar,br)] for ar,br in zip(a,b)]
    if not any(any(r) for r in d): return dict(seconds=0,ledger={},changed=0)
    bank_ledgers=[]
    for bank in range(banks):
        lo=n*bank//banks;hi=n*(bank+1)//banks;pos=lo
        totals=dict(seek=0,approach=0,selection=0,rotation=0,settle_verify=0,return_home=0,retry=0,rewind=0)
        longest=0
        for y in range(lo,hi):
            if not any(d[y]): continue
            totals['seek']+=motion((y-pos)*p,150,1500);pos=y
            es=events(d[y]);tspin=sum(motion(abs(h)/lead,rpm/60,150) for h,_ in es)
            tsel=(len(es)+1)*change # includes clearing all selectors
            totals['approach']+=.20
            totals['selection']+=tsel;totals['rotation']+=tspin
            totals['settle_verify']+=.10+verify
            reset=motion(abs(sum(h for h,_ in es))/lead,rpm/60,150) if rewind else 0
            totals['rewind']+=reset
            longest=max(longest,.20+tsel+tspin+.10+verify+reset)
        totals['return_home']=motion((pos-lo)*p,150,1500)
        totals['retry']=longest # one complete affected-row retry per head, in parallel
        bank_ledgers.append(totals)
    critical=max(bank_ledgers,key=lambda t:sum(t.values()))
    return dict(seconds=overhead+sum(critical.values()),ledger=dict(common=overhead,**critical),
                changed=sum(x!=0 for r in d for x in r),bank_seconds=[sum(t.values()) for t in bank_ledgers])

def suite(n=64):
    maps,labs=pv.s.v.variants(n);maps,labs=pv.s.connected_walls(maps,labs,n)
    deep=pv.aligned(maps,30,30);shallow=pv.aligned(maps,30,20)
    states={mode+':'+k:m[k] for mode,m in [('shallow',shallow),('deep',deep)] for k in pv.s.SUITES['relief']}
    flat=lambda h:[[h]*n for _ in range(n)]
    pairs={a+'>'+b:(states[a],states[b]) for a,b in itertools.permutations(states,2)}
    pairs.update({'neutral>'+k:(flat(30),v) for k,v in states.items()})
    local={}
    k=n//16
    for name,h in states.items():
        for y in range(0,n,2*k):
            for x in range(0,n,2*k):
                target=[r[:] for r in flat(30)]
                for yy in range(y,min(y+2*k,n)):
                    for xx in range(x,min(x+2*k,n)):target[yy][xx]=h[yy][xx]
                local[f'{name}@{x},{y}']=(flat(30),target)
    stress=(flat(0),flat(50))
    mixed=([[0 if (x+y)%2 else 50 for x in range(n)] for y in range(n)],
           [[50 if (x+y)%2 else 0 for x in range(n)] for y in range(n)])
    result={}
    for banks,rpm,lead,rewind in itertools.product((2,4,6,8),(400,850,1500),(2,3),(False,True)):
        kw=dict(banks=banks,rpm=rpm,lead=lead,rewind=rewind)
        runs={k:schedule(*v,**kw) for k,v in pairs.items()}
        worst=max(runs,key=lambda k:runs[k]['seconds'])
        ls={k:schedule(*v,**kw) for k,v in local.items()}
        wl=max(ls,key=lambda k:ls[k]['seconds'])
        init=max(schedule(flat(0),h,**kw)['seconds'] for h in states.values())
        prep=schedule(flat(0),flat(30),**kw)['seconds']
        first=max(schedule(flat(30),h,**kw)['seconds'] for h in states.values())
        seq=[states['deep:'+k] for k in pv.s.SUITES['relief']]
        sustained=sum(schedule(seq[i],seq[(i+1)%3],**kw)['seconds'] for i in range(3))/3
        result[f'B{banks}_rpm{rpm}_L{lead}_'+('strip' if rewind else 'loop')]=dict(
            worst_case=worst,scene=runs[worst],local_max=ls[wl]['seconds'],local_case=wl,
            initial_direct=init,neutral_preparation=prep,neutral_then_first=prep+first,
            sustained_cycle_mean=sustained,dense=schedule(*stress,**kw)['seconds'],
            mixed_dense=schedule(*mixed,**kw)['seconds'],selectors=n*banks,
            **cost(n,banks))
    return result

def cost(n,banks):
    """USD before sales tax: dated catalog selectors + explicit allocations; no quote."""
    resident=n*n
    items={
      'selector_servos':(n*banks,9.35,9.95),
      'selector_driver_wiring_links':(n*banks,2.0,5.0),
      'shoes_and_guides':(n*banks,1.0,3.0),
      'bus_motor_encoder':(banks,56.95,56.95),
      'bus_driver':(banks,12,25),
      'belt_end_pulleys_tensioner_guards':(banks,35,100),
      'transport_y_z':(banks,60,140),
      'resident_print_material_and_scrap':(resident,.04,.12),
      'guide_bed_frame_and_service_panels':(1,150,400),
      'power_distribution_fusing':(1,100,250),
      'controller_switches_harness':(1,70,180),
      'inspection_instruments_allowance':(1,30,150),
      'wall_panels_and_clips':(1,20,80),
      'jigs_and_fasteners':(1,60,180),
    }
    low=sum(q*l for q,l,h in items.values());high=sum(q*h for q,l,h in items.values())
    return dict(cost_usd=[round(low*1.1+20,2),round(high*1.2+60,2)],
                assembly_hours=[resident*12/3600+n*banks*4/60+8,
                                resident*30/3600+n*banks*10/60+20],
                cost_items=items)

def contact():
    # Tangential force also loads journals; conservative vector upper bound N+T/R.
    out=[]
    for mu,muj,N,T0 in itertools.product((.2,.4,.6),(.1,.25,.4),(.4,.8,1.2),(.1,.35,1.0)):
        R=2.5;rj=1.2
        # T = T0 + mu_j*rj*(N+T/R)
        required=(T0+muj*rj*N)/(1-muj*rj/R)
        out.append(dict(mu=mu,mu_j=muj,normal_N=N,base_torque_Nmm=T0,
                        required_Nmm=required,capacity_Nmm=mu*N*R,passes=mu*N*R>=required))
    return out

def checks():
    count=0
    for row in itertools.product((-6,-3,0,3,6),repeat=4):
        state=[0]*4
        for step,indices in events(row):
            for i in indices:
                assert row[i]*step>0
                state[i]+=step
                assert abs(state[i])<=abs(row[i])
            assert all(state[i]==0 for i,d in enumerate(row) if d==0)
        assert state==list(row);count+=1
    assert motion(0,10,20)==0
    assert abs(motion(100,10,20)-10.5)<1e-9
    a=[[0]*4 for _ in range(4)]
    assert schedule(a,a)['seconds']==0
    b=[[6]*4 for _ in range(4)]
    f=schedule(a,b,banks=2);r=schedule(b,a,banks=2)
    assert f==r and f['changed']==16
    assert schedule(a,b,banks=2,rewind=True)['seconds']>f['seconds']
    assert all(c['required_Nmm']>c['base_torque_Nmm'] for c in contact())
    return count

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    count=checks()
    if args.check:print(f'{count} signed four-output replays and timing/contact anchors passed (ideal model)')
    else:
        data=dict(evidence='conditional calculation, not physical validation',checks=count,
                  grids={str(n):suite(n) for n in (64,80)},contact=contact())
        out=json.dumps(data,indent=2)
        if args.output:args.output.write_text(out+'\n')
        else:print(out)
