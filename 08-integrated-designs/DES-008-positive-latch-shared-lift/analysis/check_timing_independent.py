#!/usr/bin/env python3
"""Independent scheduler/replay; C modules supply inherited maps, not timing code.
All actuator rates remain assumptions. No hardware performance inference.
"""
from pathlib import Path
import importlib.util, math, json, itertools
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('workload_source',BASE/'workload_variants.py')
ws=importlib.util.module_from_spec(spec);spec.loader.exec_module(ws)

def duration(distance, speed, acceleration):
    distance=abs(distance)
    rise=math.sqrt(distance/acceleration)
    if acceleration*rise<=speed:return 2*rise
    return 2*speed/acceleration+(distance-speed*speed/acceleration)/speed

def model(old,new,banks=8,writers=8,mask_kind='retire',continuous=False,admission=.16,retirement=.24,set_only=False):
    n=len(old);pitch=406.4/n;stations=math.ceil(n/writers);logs=[]
    if old==new:return dict(seconds=0,bank=None,counts={})
    for bank in range(banks):
        first=n*bank//banks;end=n*(bank+1)//banks
        rowpos=first;writerpos=0;forward=True;stored=[False]*n;rows=[]
        for y in range(first,end):
            difference=[new[y][x]-old[y][x] for x in range(n)]
            if not any(difference):continue
            r=dict(row=y,seek=duration((y-rowpos)*pitch,150,1500),program=0,support=0,
                   loaded_motion=0,microtravel=0,empty_return=0,masks=0,addresses=0,admissions=0,retirements=0)
            rowpos=y;physical=old[y].copy()
            for sign in (1,-1):
                levels=sorted({sign*d for d in difference if sign*d>0})
                if not levels:continue
                active={x for x,d in enumerate(difference) if sign*d>0}
                r['admissions']+=1
                words=[[x in active for x in range(n)]]
                words.extend([[sign*d==h if mask_kind=='retire' else sign*d>h for d in difference] for h in levels])
                last=0
                for phase,word in enumerate(words):
                    changed=[j for j in range(stations) if any(stored[x]!=word[x] for x in range(j,n,stations))]
                    if set_only:
                        if word==stored:changed=[]
                        else:
                            if any(stored):r['program']+=2*duration(1.8,100,4000)
                            changed=[j for j in range(stations) if any(word[x] for x in range(j,n,stations))]
                    r['masks']+=1
                    if continuous:
                        r['program']+=max(duration((stations-1)*pitch,400,4000),stations*.04)
                        r['addresses']+=stations
                        writerpos=stations-1 if writerpos==0 else 0
                    else:
                        changed.sort(reverse=not forward)
                        for j in changed:
                            r['program']+=duration((j-writerpos)*pitch,400,4000)+.04
                            writerpos=j
                        r['addresses']+=len(changed)
                        if changed:forward=not forward
                    stored=word.copy()
                    if phase==0:
                        r['support']+=admission;r['microtravel']+=duration(.3,20,800)
                    else:
                        h=levels[phase-1]
                        r['loaded_motion']+=duration(h-last,80,800)
                        for x in active:physical[x]+=sign*(h-last)
                        retired={x for x in active if sign*difference[x]==h}
                        if mask_kind=='remain':assert {x for x,w in enumerate(word) if w}==active-retired
                        else:assert {x for x,w in enumerate(word) if w}==retired
                        for x in retired:assert physical[x]==new[y][x]
                        active-=retired;last=h
                        assert all(physical[x]==old[y][x] for x,d in enumerate(difference) if d==0)
                        r['retirements']+=1;r['support']+=retirement
                        r['microtravel']+=2*duration(.3,20,800)
                assert not active
                r['empty_return']+=duration(levels[-1],80,800)
            assert physical==new[y]
            r['seconds']=sum(r[k] for k in ('seek','program','support','loaded_motion','microtravel','empty_return'))
            rows.append(r)
        if not rows:
            logs.append(dict(seconds=4,bank=bank,rows=[],counts={},ledger={}))
            continue
        fields=('seek','program','support','loaded_motion','microtravel','empty_return')
        ledger={k:sum(r[k] for r in rows) for k in fields}
        ledger['home']=duration((rowpos-first)*pitch,150,1500)+duration(writerpos*pitch,400,4000)
        retry=max(rows,key=lambda r:r['seconds']);ledger['retry']=retry['seconds'];ledger['common']=4
        logs.append(dict(seconds=sum(ledger.values()),bank=bank,rows=rows,ledger=ledger,
            retry_row=retry['row'],counts={k:sum(r[k] for r in rows) for k in ('masks','addresses','admissions','retirements')}))
    return max(logs,key=lambda x:x['seconds'])

def main():
    states,pairs,initial,local,extra=ws.suites(64,40)
    source=json.loads((BASE/'timing-audit-anchors.json').read_text())
    # Source schedulers are not called. Reproduce all nine cases from own loops.
    out={'workloads':{'states':{k:sorted({h for r in a for h in r}) for k,a in states.items()},'transitions':len(pairs)},'runs':{}}
    cases=[('B8W8_paper',dict(), 'B8_W8_indexed_dirty'),('B8W8_paper_continuous',dict(continuous=True),'B8_W8_continuous_full'),('B16W32_paper',dict(banks=16,writers=32),'B16_W32_indexed_dirty')]
    for name,kw,key in cases:
        result={n:model(*a,**kw) for n,a in pairs.items()};worst=max(result,key=lambda x:result[x]['seconds']);got=result[worst]
        assert abs(got['seconds']-source[key]['seconds'])<1e-10
        assert worst==source[key]['worst']
        out['runs'][name]=dict(worst=worst,**got)
    # Explicit read-exchange scenario. Gate2mm +3mmkeytravel +1mm approach/gap=6mm.
    exchange=2*duration(6,200,8000)+2*duration(.6,100,8000)+.010
    out['explicit_exchange_s']=exchange
    for banks,writers in ((8,8),(16,32)):
        for label,ad,rt in [('compressed',.16,.24),('dimensioned_fast',2*exchange,2*exchange+.020),('eight_80ms_strokes',.64,.64)]:
            result={n:model(*a,banks=banks,writers=writers,mask_kind='remain',admission=ad,retirement=rt) for n,a in pairs.items()}
            worst=max(result,key=lambda x:result[x]['seconds'])
            out['runs'][f'B{banks}W{writers}_2key_{label}']=dict(worst=worst,**result[worst])
    result={n:model(*a,mask_kind='remain',admission=2*exchange,retirement=2*exchange+.020,set_only=True) for n,a in pairs.items()}
    worst=max(result,key=lambda x:result[x]['seconds'])
    out['runs']['B8W8_2key_fast_global_reset']=dict(worst=worst,**result[worst])
    # Pulse reachability, independently enumerate subsets of source candidates.
    pulse_checks=[]
    for q,limit in ((5,40),(5,50),(2,40)):
        target=tuple(range(q,limit+1,q));choices=ws.comb.pulse_options(target,q)
        for seq in choices:
            sums={sum(seq[i] for i in range(len(seq)) if mask>>i&1) for mask in range(1<<len(seq))}
            assert set(target)<=sums
        pulse_checks.append(dict(quantum=q,maximum=limit,minimum_count=len(choices[0]),choices=[list(x) for x in choices]))
    out['pulse_checks']=pulse_checks
    # Explicit nine-level stress missing from retirement paper main().
    old=[[5*(x%9) if x%2 else 0 for x in range(64)] for y in range(64)]
    new=[[0 if x%2 else 5*(x%9) for x in range(64)] for y in range(64)]
    out['dense_9level_B8W8_paper']=model(old,new)
    out['dense_9level_B8W8_2key_fast']=model(old,new,mask_kind='remain',admission=2*exchange,retirement=2*exchange+.020)
    (BASE/'timing-audit-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Independent replay agrees with3published extrema; all9transition pairs simulated percase.')
    print('Explicit fast key-exchange seconds',round(exchange,6))
    for k,v in out['runs'].items():print(k,round(v['seconds'],6),v['worst'],v['counts'])
    print('Dense9levels',round(out['dense_9level_B8W8_paper']['seconds'],6),round(out['dense_9level_B8W8_2key_fast']['seconds'],6))
    print('Pulse checks',pulse_checks)
if __name__=='__main__':main()
