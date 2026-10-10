"""E-099 grouping synthesis. mm/s/USD; allocations, never hardware predictions.
No random seed: exhaustive integer grouping and deterministic workload scenarios.
Moving packet and resident-writer layouts are topology grants, not generated CAD.
"""
import importlib.util
import itertools as it
import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rack', ROOT/'E-098/deck_rack.py')
rack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rack)
move = rack.move
MOTIONS = ((80,1000),(200,5000),(400,20000))
BANKS = (1,2,4,8,16)


@lru_cache(None)
def segment(rows, profiles, v, a):
    """One packet's nominal E-098 contact order, at local first-row home.
    Profiles are changed (old,target) pairs per row; no inactive cell writes.
    Paired rows must be increasing. Twenty scans for the adverse full map.
    """
    active = [(r,p) for r,p in zip(rows,profiles) if p]
    if not active:
        return dict(row_s=0.,lift_s=0.,dog=0,pad=0,proof=0,mm=0.)
    old = sorted({x for _,ps in active for x,y in ps})
    new = sorted({y for _,ps in active for x,y in ps},reverse=True)
    visits = [[r for r,p in active]]
    visits += [[r for r,p in active if any(x==h for x,y in p)] for h in old]
    visits += [[r for r,p in active if any(y==h for x,y in p)] for h in new]
    visits += [[r for r,p in active]]
    pos=rows[0]; travel=0.
    for i,rr in enumerate(visits):
        for r in sorted(rr,reverse=bool(i%2)):
            travel += move(5.08*(r-pos),v,a);pos=r
    travel += move(5.08*(pos-rows[0]),v,a)
    path=[-2.]+[5*h+2. for h in old]+[45.]
    for h in new:path += [5*h+2.,5*h]
    path += [-2.]
    return dict(row_s=travel,lift_s=sum(move(y-x,v,a) for x,y in zip(path,path[1:])),
                dog=sum(map(len,visits[1:-1])),pad=2*len(active),proof=len(old)+len(new),
                mm=sum(abs(y-x) for x,y in zip(path,path[1:])))


def profile(kind, row, start=0):
    if kind=='full':return tuple((x,y) for x,y in it.product(range(9),repeat=2) if x!=y)
    if kind=='local' and start<=row<start+5:return tuple((0,c+1) for c in range(5))
    return ()


def subtotal(s, dog, pad, proof):
    return s['row_s']+s['lift_s']+s['dog']*dog+s['pad']*pad+s['proof']*proof


@lru_cache(None)
def evaluate(kind,banks,g,start=0,v=200,a=5000,dog=.1,pad=.1,proof=.1,overhead=2.,couple=0.):
    """Movable g-row packet per bank; blocks [0:g], [g:2g] etc.
    Return local writer to packet origin before dispatch; dispatch and return
    rest-to-rest. For g>1 this GRANTS a second row axis + safe moving-deck
    passage. For g=1 comb/writer share row axis. No whole-board reset.
    One dog retry and one load retry per active bank, in-situ, no independence.
    couple includes packet lock/release beyond motions (zero is favorable).
    """
    n=80//banks
    assert 1<=g<=n
    reports=[]
    for bank in range(banks):
        pos=0;time=0.;packets=0;dv=hv=pv=0;motion=0.;lift=0.
        for first in range(0,n,g):
            rows=tuple(range(first,min(first+g,n)))
            pp=tuple(profile(kind,bank*n+r,start) for r in rows)
            if not any(pp):continue
            s=segment(rows,pp,v,a)
            dispatch=move(5.08*(first-pos),v,a)
            time += dispatch+subtotal(s,dog,pad,proof)+couple
            motion+=dispatch+s['row_s'];lift+=s['lift_s']
            dv+=s['dog'];hv+=s['pad'];pv+=s['proof'];packets+=1;pos=first
        if packets:
            back=move(pos*5.08,v,a);motion+=back
            time+=back+overhead+dog+proof+2*move(2.2,v,a)
        reports.append(dict(seconds=time,packets=packets,dog=dv,pad=hv,proof=pv,row_s=motion,lift_s=lift))
    worst=max(reports,key=lambda r:r['seconds'])
    # Same setting channel is granted to reach pad home and ground dog planes.
    # Moving g>1 packet has an additional dispatch axis; full-bank deck does not.
    channels=banks*(82+(1 if 1<g<n else 0))
    return dict(**worst,banks=banks,rows_per_packet=g,channels=channels,
                pickup_pads=80*banks*g,ground_dogs=6400,channel_cap=250/channels,
                accepted_machine=False)


def optimal_partition(n,v,a,dog=.1,pad=.1,proof=.1):
    """Exact DP over every ordered contiguous partition of n fully active rows.
    State (covered rows, previous packet start); shared driver serial packets.
    Zero coupling cost; arbitrary packet boundaries are optimistic hardware.
    Independent of fixed-g enumeration. Includes dispatch and return.
    """
    pp=profile('full',0)
    states={(0,0):(0.,())}
    for covered in range(n):
        for (end,previous),(cost,parts) in list(states.items()):
            if end!=covered:continue
            for stop in range(covered+1,n+1):
                rows=tuple(range(covered,stop))
                s=segment(rows,(pp,)*len(rows),v,a)
                candidate=cost+move(5.08*(covered-previous),v,a)+subtotal(s,dog,pad,proof)
                key=(stop,covered)
                if key not in states or candidate<states[key][0]:
                    states[key]=(candidate,parts+(stop-covered,))
    answer=min((cost+move(5.08*last,v,a),parts) for (end,last),(cost,parts) in states.items() if end==n)
    return dict(seconds_before_overhead_retry=answer[0],parts=answer[1],represented_partitions=2**(n-1))


def resident(kind,banks,writers,start=0,v=200,a=5000,dog=.1,proof=.1):
    """One deck shared by writers contiguous subbanks; conservatively synchronize
    E-098 routes. E-098 independent-bank time is an optimistic resident lower
    bound if sparse deck groups differ; exact full workload matches every lane.
    Each writer costs 80 settings + one row axis; one lift per larger bank.
    """
    assert 80%(banks*writers)==0
    r=evaluate(kind,banks*writers,80//(banks*writers),start,v,a,dog=dog,proof=proof)
    return dict(seconds_bound=r['seconds'],channels=81*banks*writers+banks,
                pickup_pads=6400,ground_dogs=6400,banks=banks,writers=writers,
                scope='full exact allocation; sparse optimistic bound',accepted_machine=False)


def direct(banks,v=200,a=5000,proof=.1,kind='full',start=0):
    l=rack.budget.ledger(kind,banks,start,v,a)
    return rack.budget.evaluate(l,support=proof)['direct']['seconds']


def checks():
    count=0
    for b,(v,a),dog in it.product(BANKS,MOTIONS,(0.,.02,.1,.5)):
        n=80//b;x=evaluate('full',b,n,v=v,a=a,dog=dog)
        ref=rack.ledger(*rack.workload('full'),b,v=v,a=a,dog=dog)
        assert math.isclose(x['seconds'],ref['seconds'])
        assert x['dog']==18*n and x['pad']==2*n and x['proof']==18
        # Fully row-local independent operation sum, including one stopped
        # dispatch per row and a single final home return.
        row=evaluate('full',b,1,v=v,a=a,dog=dog)
        dm=move(4,v,a)+8*move(5,v,a)+2*move(3,v,a)+9*move(2,v,a)+8*move(3,v,a)+move(2,v,a)
        expected=2+n*(dm+18*dog+.2+1.8)+(n-1)*move(5.08,v,a)+move((n-1)*5.08,v,a)+dog+.1+2*move(2.2,v,a)
        assert math.isclose(row['seconds'],expected)
        count+=1
    # This lower bound covers ALL contiguous partitions, including unequal ones:
    # k packets add (k-1)*(deck+18proof-20*pitch_move) + nonnegative dispatch.
    penalties=[]
    for v,a in MOTIONS:
        dm=segment((0,),(profile('full',0),),v,a)['lift_s']
        delta=dm-20*move(5.08,v,a)
        assert delta>0  # remains positive even at free support proofs.
        penalties.append(delta)
        dp=optimal_partition(20,v,a,proof=0.)
        assert dp['parts']==(20,)
    # Independently brute-force all 128 partitions of eight rows against DP.
    brute=[]
    for mask in range(128):
        cuts=[0]+[i for i in range(1,8) if mask>>(i-1)&1]+[8]
        t=0.;pos=0
        for lo,hi in zip(cuts,cuts[1:]):
            s=segment(tuple(range(lo,hi)),(profile('full',0),)*(hi-lo),200,5000)
            t+=move(5.08*(lo-pos))+subtotal(s,.1,.1,.1);pos=lo
        brute.append(t+move(5.08*pos))
    assert math.isclose(min(brute),optimal_partition(8,200,5000)['seconds_before_overhead_retry'])
    assert evaluate('none',4,1)['seconds']==0
    # All x starts are identical in this 80-parallel-column channel grant;
    # validate changed column level sets independently for 76 x 76 patches.
    alignments=0
    for r,c in it.product(range(76),repeat=2):
        cols=[0]*80
        for j in range(5):cols[c+j]=j+1
        assert tuple(x for x in cols if x)==(1,2,3,4,5)
        assert sum(bool(profile('local',i,r)) for i in range(80))==5
        alignments+=1
    return dict(reference_cases=count,partition_lower_bound_penalty_at_zero_proof_s=penalties,
                brute_partitions=128,all_patch_alignments=alignments,self_review_only=True)


def main():
    out=dict(checks=checks(),central=[],local=[],sensitivity=[],cost_boxes=[])
    for b in BANKS:
        n=80//b
        rows=[evaluate('full',b,g) for g in range(1,n+1)]
        # Non-dominated on time and pickup count, NOT whole-product frontier.
        front=[x for x in rows if not any(y['seconds']<=x['seconds'] and y['pickup_pads']<=x['pickup_pads'] and (y['seconds']<x['seconds'] or y['pickup_pads']<x['pickup_pads']) for y in rows)]
        out['central'].append(dict(banks=b,bank_deck=rows[-1],row_comb=rows[0],direct_s=direct(b),time_pickup_frontier=front))
        for g in sorted({1,n}):
            rr=[evaluate('local',b,g,start) for start in range(76)]
            out['local'].append(dict(banks=b,rows_per_packet=g,range_s=[min(x['seconds'] for x in rr),max(x['seconds'] for x in rr)]))
    for (v,a),dog,proof in it.product(MOTIONS,(.02,.05,.1,.2,.5),(0.,.05,.1,.2)):
        minima={}
        for mode in ('bank','row','direct'):
            passes=[]
            for b in BANKS:
                if mode=='direct':t=direct(b,v,a,proof)
                else:t=evaluate('full',b,80//b if mode=='bank' else 1,v=v,a=a,dog=dog,proof=proof)['seconds']
                if t<30:passes.append(b)
            minima[mode]=min(passes,default=None)
        out['sensitivity'].append(dict(v=v,a=a,dog_s=dog,proof_s=proof,min_banks=minima))
    out['local_sensitivity']=[]
    for b,(v,a),dog in it.product(BANKS,MOTIONS,(.02,.1,.2)):
        for g in sorted({1,80//b}):
            rr=[evaluate('local',b,g,start,v,a,dog=dog) for start in range(76)]
            out['local_sensitivity'].append(dict(banks=b,g=g,v=v,a=a,dog_s=dog,range_s=[min(x['seconds'] for x in rr),max(x['seconds'] for x in rr)]))
    out['row_B16_overhead_sensitivity']=[dict(overhead_s=h,seconds=evaluate('full',16,1,overhead=h)['seconds']) for h in (2.,6.)]
    out['resident']=[resident('full',b,w) for b in BANKS for w in (1,2,4,8,16) if b*w in BANKS]
    for reserve,cell in it.product((150,250,400),(0.,.02,.05)):
        out['cost_boxes'].append(dict(reserve=reserve,cell=cell,B16_comb_complete_channel_cap=(500-reserve-6400*cell)/(82*16),B4_direct_complete_head_cap=(500-reserve-6400*cell)/(80*4)))
    out['fixed_group_variants']=sum(80//b for b in BANKS)
    # Slot ceiling for fastest body count reduction, without extra grouping costs.
    for b in (8,16):
        zero=evaluate('full',b,1,dog=0.)
        out.setdefault('row_slot_ceilings',[]).append(dict(banks=b,dog_ceiling=(30-zero['seconds'])/(zero['dog']+1)))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
