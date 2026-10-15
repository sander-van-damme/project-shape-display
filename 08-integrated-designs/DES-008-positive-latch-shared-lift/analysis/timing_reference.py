#!/usr/bin/env python3
"""Independent architecture throughput screen, 2026-10-14. Stdlib only.
Uses unchanged historical scene generators. All rates are assumptions, not tests.
"""
import importlib.util,itertools,json,math,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def source(name, path):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
des=source('des007','08-integrated-designs/DES-007-radial-pinch-belt-row-head/analysis/system.py')
mask=source('mask083','tools/curated-experiment-checks/E-083/bank_schedule.py')

def move(d,v=150,a=1500):
    d=abs(d)
    return 2*math.sqrt(d/a) if d<v*v/a else d/v+v/a

def maps(n):
    m,l=des.pv.s.v.variants(n);m,l=des.pv.s.connected_walls(m,l,n)
    states={f'{mode}:{k}':v[k] for mode,v in [('shallow',des.pv.aligned(m,30,20)),('deep',des.pv.aligned(m,30,30))] for k in des.pv.s.SUITES['relief']}
    flat=lambda h:[[h]*n for _ in range(n)]
    pairs={a+'>'+b:(states[a],states[b]) for a,b in itertools.permutations(states,2)}
    pairs.update({'neutral>'+k:(flat(30),v) for k,v in states.items()})
    initial={'cold>'+k:(flat(0),v) for k,v in states.items()}
    local={};k=n//16
    for name,h in states.items():
        for y in range(0,n,2*k):
            for x in range(0,n,2*k):
                target=flat(30)
                for yy in range(y,min(y+2*k,n)):
                    for xx in range(x,min(x+2*k,n)):target[yy][xx]=h[yy][xx]
                local[f'{name}@{x},{y}']=(flat(30),target)
    extra={'neutral_preparation':(flat(0),flat(30)), 'dense50':(flat(0),flat(50)),
        'dense_opposite50':([[0 if (x+y)%2 else 50 for x in range(n)] for y in range(n)],[[50 if (x+y)%2 else 0 for x in range(n)] for y in range(n)])}
    # Dense nonzero changes spanning 21 absolute levels: stress for mask rewriting.
    old=[[2*(x%21) for x in range(n)] for y in range(n)]
    new=[[2*((x+10)%21) for x in range(n)] for y in range(n)]
    extra['dense21_cyclic']=(old,new)
    old=[[2*(x%21) if x%2 else 0 for x in range(n)] for y in range(n)]
    new=[[0 if x%2 else 2*(x%21) for x in range(n)] for y in range(n)]
    extra['dense21_all_deltas']=(old,new)
    return states,pairs,initial,local,extra

def stats(a,b):
    n=len(a);d=[[y-x for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    counts=[sum(x!=0 for x in r) for r in d]
    return dict(changed=sum(counts),rows=sum(x>0 for x in counts),travel_mm=sum(abs(x) for r in d for x in r),
        signed_delta_levels=sorted({x for r in d for x in r if x}),row_max_sum_mm=sum(max(map(abs,r)) for r in d),
        row_posneg_sum_mm=sum(max(r+[0])-min(r+[0]) for r in d),max_row_changed=max(counts),delta=d)

def row_writer(a,b,banks=2,v=80,accel=800,mode='independent',approach=.20,check=.15,select=.08,common=4,return_to_origin=True):
    """Independent linear outputs, or common displacement with stopped retirements.
    Every active row: finite seek, .20s approach+withdrawal, .15s checking,
    stop-to-stop vertical move(s), selection and final all-clear if shared.
    Common lift returns unloaded after each sign; independent shafts need no reset.
    One longest full row retry per bank, no pipelining assumed.
    """
    n=len(a);d=stats(a,b)['delta'];bank=[]
    if not any(any(r) for r in d):return {'seconds':0,'ledger':{}}
    for k in range(banks):
        lo=n*k//banks;hi=n*(k+1)//banks;pos=lo
        z=dict(seek=0,engage_check=0,selection=0,loaded_motion=0,reset=0,retry=0,home=0)
        longest=0
        for y in range(lo,hi):
            r=d[y]
            if not any(r):continue
            seek=move((y-pos)*406.4/n);pos=y
            if mode=='independent':
                spin=move(max(map(abs,r)),v,accel);sel=0;reset=0
            elif mode=='shared':
                ev=des.events(r);spin=sum(move(h,v,accel) for h,_ in ev)
                sel=(len(ev)+1)*select
                reset=sum(move(max([sign*h for h in r if sign*h>0]+[0]),v,accel) for sign in (1,-1))
            else:raise ValueError(mode)
            fixed=approach+check
            z['seek']+=seek;z['engage_check']+=fixed;z['selection']+=sel;z['loaded_motion']+=spin;z['reset']+=reset
            longest=max(longest,fixed+sel+spin+reset)
        z['retry']=longest
        if return_to_origin:z['home']=move((pos-lo)*406.4/n)
        bank.append(z)
    critical=max(bank,key=lambda x:sum(x.values()))
    return dict(seconds=common+sum(critical.values()),ledger=dict(common=common,**critical),bank_seconds=[sum(x.values()) for x in bank],active_output_channels=n*banks)

def global_mask(a,b,banks=1,row_write=.08,seek=True,vertical_speed=60,vertical_accel=600,common=4,policy='displacement'):
    """Optimistic rigid common elevator with arbitrary-height grips and ground catches.
    Reuses E081 exact support replay; every phase writes transient mask including
    stale zeros. No overlapping writer and elevator motion. Bank writers each
    have n parallel data drives. 'seek=False' means stationary mechanical row
    decoder; row_write MUST include all data/row sequencing. 'seek=True' is
    moving head, each bank begins/ends at its origin, alternating phase sweep.
    Per-command support handoff check/settle .10s, 1 full mask rewrite retry.
    """
    n=len(a);seq=mask.commands(a,b,policy);replay=mask.schedule.replay(a,b,policy=policy)
    if not seq:return dict(seconds=0,ledger={},phases=0,rounds=0,row_writes=0)
    phases=mask.transactions(seq,n,banks)
    old=[set() for _ in range(n)];pos=[n*k//banks for k in range(banks)];travel=0
    for number,newmask in enumerate(seq+[set()]):
        goal=[set() for _ in range(n)]
        for r,c in newmask:goal[r].add(c)
        dirty=[r for r in range(n) if old[r]!=goal[r]]
        times=[]
        for bank in range(banks):
            rows=[r for r in dirty if n*bank//banks<=r<n*(bank+1)//banks]
            rows.sort(reverse=number%2==1)
            t=0
            for r in rows:t+=move((r-pos[bank])*406.4/n);pos[bank]=r
            times.append(t)
        travel+=max(times)
        old=goal
    travel+=max(move((pos[k]-n*k//banks)*406.4/n) for k in range(banks))
    vertical=sum(move(y-x,vertical_speed,vertical_accel) for x,y in zip(replay['elevator_path'],replay['elevator_path'][1:]))
    retry=math.ceil(n/banks)*row_write
    if seek:retry+=math.ceil(n/banks)*move(406.4/n)
    ledger=dict(common=common,mask_writes=phases['rounds']*row_write,mask_seek=travel if seek else 0,
        elevator_motion=vertical,handoffs=.10*len(seq),retry=retry)
    return dict(seconds=sum(ledger.values()),ledger=ledger,phases=len(seq)+1,rounds=phases['rounds'],row_writes=phases['row_writes'],
        elevator_path_mm=replay['elevator_path'],active_data_channels=n*banks,passive_grips=n*n,passive_supports=n*n,
        max_row_write_for_30s=(30-sum(v for k,v in ledger.items() if k not in ('mask_writes','retry')))/(phases['rounds']+math.ceil(n/banks)))

def summarize(pairs,fn,**kw):
    records={name:fn(*ab,**kw) for name,ab in pairs.items()};worst=max(records,key=lambda k:records[k]['seconds'])
    return dict(worst=worst,**records[worst],mean_seconds=sum(x['seconds'] for x in records.values())/len(records))

def checks():
    assert move(0)==0 and math.isclose(move(100,10,20),10.5)
    for r in itertools.product((-20,-10,0,10,20),repeat=4):
        actual=[0]*4
        for step,chosen in des.events(r):
            for i in chosen:actual[i]+=step
        assert tuple(actual)==r
    assert row_writer([[0]],[[0]])['seconds']==0
    # Common lift cannot reset mismatched old heights in one rigid motion.
    assert [x-40 for x in [10,40]]==[-30,0]
    for a,b in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
        for policy in ('reset','displacement'):
            rr=global_mask([a],[b],policy=policy)
            assert rr['seconds']>=0
    return '625 signed row replays; 162 mask support replays; motion anchors'
