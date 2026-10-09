"""Conditional system allocation, NOT feasible-machine timing or sourced prices.
All distances mm, times s. Deterministic competing bounds; no random priors.
Sources implement the workload/support controller and binary transaction ledger.
"""
import importlib.util
import itertools as it
import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def source(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

controller = source('retained', 'E-089/retained_controller.py')
binary = source('binary', 'E-083/bank_schedule.py')
direct_reference = source('direct_reference', 'E-050/joint_envelope.py')


def move(d, v=200., a=5000.):
    """Rest to rest, capped speed. No jerk, flexible response or force credit."""
    d = abs(d)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def path_time(path, v, a):
    return sum(move(b-a0, v, a) for a0,b in zip(path,path[1:]))


def retained_paths(old, target):
    deltas = {5*(b-a) for r,s in zip(old,target) for a,b in zip(r,s) if a != b}
    elevator, reader = [0.], [0.]
    groups = 0
    for sign in (-1,1):
        qs = sorted((d for d in deltas if sign*d>0), key=abs)
        if not qs:
            continue
        elevator += [2.2]
        for q in qs:
            elevator += [q+2.2, q]
            reader += [q]
        elevator += [0.]
        reader += [0.]
        groups += 1+len(qs)
    return elevator, reader, groups


def writer_route(rows, banks, scans, v=200., a=5000.):
    """Fixed contiguous banks, one home at first row in each bank.
    Retained: set forward, clear backward, 2 traversals. Deck: hook forward,
    rotor backward, clear forward, return home: 4 traversals. Sparse gaps and
    dispatch from home are charged. All banks run in parallel, barrier per scan.
    Row-local engage/withdraw is inside the unknown write slot, not this route.
    """
    n=80//banks
    visits=[[r%n for r in rows if r//n==b] for b in range(banks)]
    rounds=max(map(len,visits),default=0)
    times=[]
    for vs in visits:
        if not vs:
            times.append(0.); continue
        points=[0]+vs
        one=sum(move(5.08*(y-x),v,a) for x,y in zip(points,points[1:]))
        # Reverse path has the same stopped legs. Returning from last row on
        # odd scans may skip intermediate stops, but this schedule stops there.
        times.append(scans*one)
    return rounds, max(times,default=0.)


@lru_cache(maxsize=None)
def deck_trace(kind):
    old,new=controller.workload(9, "local" if kind=="local" else "all_deltas")
    return controller.replay(old,new,"stepped_deck")


@lru_cache(maxsize=None)
def ledger(kind, banks, start=0, v=200., a=5000.):
    old,new=controller.workload(9, 'local' if kind=='local' else 'all_deltas')
    if kind=='local' and start:
        old=old[start:]+old[:start]  # old is flat
        new=[[0]*80 for _ in range(80)]
        for r in range(start,start+5):
            for c in range(5):new[r][c]=1+c
    rows=[r for r in range(80) if old[r]!=new[r]]
    changed=sum(x!=y for r,s in zip(old,new) for x,y in zip(r,s))
    e,r,g=retained_paths(old,new)
    rounds,route=writer_route(rows,banks,2,v,a)
    _,deck_route=writer_route(rows,banks,4,v,a)
    deck=deck_trace(kind)  # row translation leaves deck support path unchanged
    masks=binary.transactions(binary.commands(old,new,'displacement'),80,banks)
    d=binary.drive(banks,.005,.5,20.)
    # Fresh direct-writer itinerary: independent heads, per-bank row scan,
    # home->old->target->home at each row; all unchanged heads stay idle.
    n=80//banks
    direct_times=[]
    for b in range(banks):
        rr=[x for x in rows if x//n==b]
        t=0.; last=0
        for row in rr:
            t+=move((row%n-last)*5.08,v,a)
            pairs=zip(old[row],new[row]) if kind=="local" else it.product(range(9),repeat=2)
            t+=max((sum(move(z,v,a) for z in (5*x,5*abs(y-x),5*y))
                    for x,y in pairs if x!=y),default=0.)
            last=row%n
        t+=move(last*5.08,v,a)  # explicit final head-carriage home
        direct_times.append(t)
    return dict(kind=kind,banks=banks,v=v,a=a,changed=changed,word_rounds=2*rounds,
        hook_rounds=2*rounds,rotor_rounds=rounds,binary_rounds=masks['rounds'],
        binary_row_writes=masks['row_writes'],direct_rounds=rounds,
        support_groups=g,deck_groups=deck['counts'].get('grip_proof',0)+deck['counts'].get('ground_proof',0),
        elevator_mm=sum(abs(y-x) for x,y in zip(e,e[1:])),
        reader_mm=sum(abs(y-x) for x,y in zip(r,r[1:])),
        retained_motion_s=path_time(e,v,a)+path_time(r,v,a)+route,
        # Counterfactual charge the SAME finite support itinerary to binary.
        # This is not inherited mechanical compatibility or E-083's old 6 s.
        binary_motion_s=path_time(e,v,a)+masks['rounds']*d['cycle_s'],
        deck_motion_s=path_time([5*x for x in deck['path']],v,a)+deck_route,
        direct_motion_s=max(direct_times),
        observation_floors=dict(retained=2*changed+160*len(rows),deck=2*changed+80*(3*len(rows)),
            binary=2*changed+80*masks['row_writes'],direct=2*changed))


def evaluate(L, word=.5, hook=.1, rotor=.5, support=.1, overhead=2.,
             row_proof=.004, retry_rounds=1, retry_groups=1):
    """All grants explicit: writes include set/unlock/lock/individual state proof,
    row engagement/withdrawal; support slots include decode, cam, actual load
    proof, output withdrawal, reset and local settling beyond axial travel.
    Extra detected-row retry repeats its full slot. Extra support retry pays a
    2.2-mm up/down motion plus slot; diagnosis/persistent faults are excluded.
    This recovery grant must be physically demonstrated before timing credit.
    """
    b=L['banks']; rw=retry_rounds; rg=retry_groups
    recovery=rg*(support+2*move(2.2,L["v"],L["a"]))
    out={}
    t=overhead+L['retained_motion_s']+(L['word_rounds']+rw)*word+L['support_groups']*support+recovery
    out['retained']=dict(seconds=t,channels=83*b,
        word_ceiling_s=(30-overhead-L['retained_motion_s']-L['support_groups']*support-recovery)/(L['word_rounds']+rw))
    d=binary.drive(b,.005,.5,20.)
    t=overhead+L['binary_motion_s']+L['binary_rounds']*row_proof+L['support_groups']*support+rw*(d['cycle_s']+row_proof)+recovery
    out['binary']=dict(seconds=t,channels=80*b+80)
    t=overhead+L['deck_motion_s']+L['hook_rounds']*hook+(L['rotor_rounds']+rw)*rotor+L['deck_groups']*support+recovery
    out['deck']=dict(seconds=t,channels=82*b,
        rotor_ceiling_s=(30-overhead-L['deck_motion_s']-L['hook_rounds']*hook-L['deck_groups']*support-recovery)/(L['rotor_rounds']+rw))
    # A direct retry repeats the adverse complete head path plus both transfers;
    # use independent enumeration over nine levels rather than count two writes.
    worst=max(sum(move(z,L["v"],L["a"]) for z in (x,abs(y-x),y)) for x,y in it.product(range(0,41,5),repeat=2) if x!=y)
    t=overhead+L['direct_motion_s']+2*L['direct_rounds']*support+rw*(worst+2*support)
    out['direct']=dict(seconds=t,channels=80*b)
    for family,x in out.items():
        x['channel_ceiling_usd']=250/x['channels']
        x['conditional_time_pass']=x['seconds']<30
        x['machine_accepted']=False
    return out


def checks():
    assert move(0)==0
    assert math.isclose(move(8),.08) # velocity crossover
    full=ledger('full',8)
    assert math.isclose(full['elevator_mm'],199.6)
    assert full['reader_mm']==160 and full['support_groups']==18
    assert full['binary_row_writes']==1520 and full['binary_rounds']==190
    assert full['word_rounds']==20 and full['deck_groups']==18
    # Unchanged physical writes and support work are exactly absent.
    z=[[0]*80 for _ in range(80)]
    assert retained_paths(z,z)==([0.],[0.],0)
    assert writer_route([],8,2)==(0,0.)
    # Independent counting at every patch alignment and bank count.
    alignments=0
    for b in (1,2,4,8,16):
        for start in range(76):
            rr=list(range(start,start+5));n=80//b
            visits=max(sum(r//n==k for r in rr) for k in range(b))
            assert writer_route(rr,b,2)[0]==visits
            alignments+=1
    for b in (1,2,4,8,16):
        L=ledger('full',b)
        E=evaluate(L)
        cap=E['retained']['word_ceiling_s']
        assert math.isclose(evaluate(L,word=cap)['retained']['seconds'],30.)
        assert evaluate(L,word=cap+1e-6)['retained']['seconds']>30
        assert evaluate(L,word=cap-1e-6)['retained']['seconds']<30
        # Exact binary count from complete H=9 masks; no workload speedup credit.
        assert L['binary_rounds']==1520//b
        for row in E.values():
            assert math.isclose(row['channel_ceiling_usd']*row['channels']+250,500)
        assert L['observation_floors']['retained']==25600
    assert ledger('local',8)['observation_floors']['retained']==850
    return dict(alignment_cases=alignments,gate='no complete machine accepted')


def main():
    out=dict(checks=checks(),central_full=[],central_local=[])
    for b in (1,2,4,8,16):
        L=ledger('full',b);out['central_full'].append(dict(ledger=L,budgets=evaluate(L)))
        # Home position and alignment both matter; enumerate all legal patches.
        local=[(start,evaluate(ledger('local',b,start))) for start in range(76)]
        out['central_local'].append(dict(banks=b,range_s={f:[min(x[f]['seconds'] for _,x in local),max(x[f]['seconds'] for _,x in local)] for f in ('retained','deck','binary','direct')}))
    out['sensitivity']=[]
    for word,support,overhead,retries in it.product((.05,.2,.5,.9),(.05,.2,.5),(2.,6.),(0,1)):
        rows=[]
        for b in (1,2,4,8,16):
            e=evaluate(ledger('full',b),word=word,rotor=word,support=support,overhead=overhead,retry_rounds=retries,retry_groups=retries)
            rows.append((b,e))
        out['sensitivity'].append(dict(word_s=word,support_s=support,overhead_s=overhead,retries=retries,
            minimum_tested_banks={f:next((b for b,e in rows if e[f]['conditional_time_pass']),None) for f in ('retained','deck','binary','direct')}))
    out['motion_sensitivity']=[dict(v=v,a=a,banks=b,budgets=evaluate(ledger('full',b,v=v,a=a))) for v,a in ((80.,1000.),(200.,5000.),(400.,20000.)) for b in (1,2,4,8,16)]
    out['conditional_frontiers']=[]
    price_boxes=(dict(retained=.3,binary=.2,deck=.5,direct=1.),
                 dict(retained=.6,binary=.2,deck=.5,direct=.5))
    for prices,cell in it.product(price_boxes,(0.,.02)):
        options=[]
        for b in (1,2,4,8,16):
            for family,x in evaluate(ledger('full',b)).items():
                cost=250+6400*cell+prices[family]*x['channels']
                if x['seconds']<30 and cost<500:
                    options.append(dict(family=family,banks=b,seconds=x['seconds'],cost=cost))
        frontier=[x for x in options if not any(y['cost']<=x['cost'] and y['seconds']<=x['seconds'] and (y['cost']<x['cost'] or y['seconds']<x['seconds']) for y in options)]
        out['conditional_frontiers'].append(dict(hypothetical_complete_channel_prices=prices,cell_purchase=cell,offers=options,time_cost_frontier=frontier,feasible_machine_frontier=[]))
    out['cost_sensitivity']=[dict(banks=b,reserve=reserve,cell_purchase=p,retained_channel_ceiling=(500-reserve-6400*p)/(83*b)) for b,reserve,p in it.product((1,4,8,16),(150,250,400),(0,.02,.05))]
    # Sensitivity proxies, not a bill of material, sliced volume or measured labor.
    out['slider_burden']=[dict(sliders=n,average_slider_mm3=vol,volume_l=n*vol/1e6,
        extrusion_hours=[n*vol/(rate*3600) for rate in (15,5)],
        assembly_hours=[n*s/3600 for s in (2,10,30)]) for n,vol in it.product((44800,57600),(5,20,80))]
    out['legacy_controls']=dict(binary_B16_H21=6+215*binary.drive(16,.005,.5,20.)['cycle_s'],
        direct_fast_80=direct_reference.seconds(1,'fast',0),direct_central_240=direct_reference.seconds(3,'central',0))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
