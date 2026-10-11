"""E-172 extension: supported co-scheduling; mm, s, USD. Standard library.
Constructive schedules, not global optima. No physical or process qualification.
"""
import itertools as it
import json
import math
from dataclasses import dataclass
from functools import lru_cache
import routing as r

checked_pose = lru_cache(maxsize=100000)(r.check_pose)

LEVELS = range(5)
PAIRS = tuple(it.product(LEVELS, repeat=2))
BANKS = (1, 2, 4, 8, 16)


@dataclass(frozen=True)
class Event:
    kind: str
    value: object = None
    ids: tuple = ()
    heights: tuple = ()  # nominal key heights at this write, not command bits


@lru_cache(None)
def key_events(pairs, e=.05):
    """All same-sign cells acquire together; deposit increasing |difference|.
    Each bridge microstroke moves EVERY carrier-selected cell, not just targets.
    Identity cells stay ground-selected. No mixed-sign overshoot is required.
    """
    a = 2*e+.1
    events = []
    def write(ids, state, heights):
        events.append(Event('write', state, tuple(ids), tuple(heights)))
    def move(d): events.append(Event('move', d))
    for sign in (-1, 1):
        ids = [i for i, (o,t) in enumerate(pairs) if sign*(t-o)>0]
        if not ids: continue
        write(ids, 'B', [pairs[i][0]*r.STEP for i in ids])
        move(a)
        events.append(Event('proof', 'carrier', tuple(ids)))
        write(ids, 'C', [pairs[i][0]*r.STEP+a for i in ids])
        for k in sorted({abs(pairs[i][1]-pairs[i][0]) for i in ids}):
            group = [i for i in ids if pairs[i][1]-pairs[i][0]==sign*k]
            delta = sign*k*r.STEP
            move(delta+a)
            write(group, 'B', [pairs[i][1]*r.STEP+a for i in group])
            move(delta-a)
            events.append(Event('proof', 'ground', tuple(group)))
            write(group, 'G', [pairs[i][1]*r.STEP for i in group])
        move(-a)
    return events


def replay(pairs, g, c, subdivisions=1, bias=0.):
    """Execute complete bank, all cells at each shared motion or key shift.
    Ideal prismatic joints/retention, unilateral gravity support and r's finite
    shelves. No brake implementation. Breakpoints plus midpoints check solids.
    bias is an uncorrected common carrier positioning error (mm).
    """
    a=.2; d=-a
    state=['G']*len(pairs)
    ground=[o for o,t in pairs]
    samples=0; reverse_microtravel=0.
    qmap={'G':-r.SHIFT,'B':0.,'C':r.SHIFT}
    def height(i, dd):
        o,_=pairs[i]
        gz=ground[i]*r.STEP+g[ground[i]]
        cz=o*r.STEP+c[o]+dd+bias
        return gz if state[i]=='G' else cz if state[i]=='C' else max(gz,cz)
    def pose(dd, override=None):
        nonlocal samples
        for i in range(len(pairs)):
            q=qmap[state[i]] if override is None or i not in override else override[i]
            checked_pose(q,height(i,dd),dd+bias,tuple(g),tuple(c))
            samples+=1
    pose(d)
    for event in key_events(pairs):
        if event.kind=='move':
            end=event.value
            ts={j/subdivisions for j in range(subdivisions+1)}
            if end!=d:
                # Every shelf/key vertical-face crossing, even for failed
                # bridge states, and every possible support switch.
                for i,(o,_) in enumerate(pairs):
                    for j in LEVELS:
                        for offset in (0., -r.FLOOR_T-r.KEY_T):
                            crossing=j*r.STEP+g[j]-o*r.STEP-c[o]-bias+offset
                            t=(crossing-d)/(end-d)
                            if 0<t<1: ts.add(t)
            ordered=sorted(ts)
            ts.update((x+y)/2 for x,y in zip(ordered,ordered[1:]))
            for t in sorted(ts): pose(d+(end-d)*t)
            if math.isclose(d-end,.4):
                reverse_microtravel += sum(state[i]=='C' for i in range(len(pairs)))*.4
            d=end
        elif event.kind=='write':
            ids=event.ids; new=event.value
            prior={i:state[i] for i in ids}
            if new=='B':
                for i in ids:
                    if state[i]=='C': ground[i]=pairs[i][1]
            # Shift only after geometric contact compatibility, not a bit flip.
            ts={j/subdivisions for j in range(subdivisions+1)}
            for i in ids:
                q0,q1=qmap[prior[i]],qmap[new]
                for edge in (-r.OUTER,-r.INNER,r.INNER,r.OUTER):
                    for side in (-r.HALF_KEY,r.HALF_KEY):
                        t=(edge-side-q0)/(q1-q0)
                        if 0<t<1:ts.add(t)
            ordered=sorted(ts);ts.update((x+y)/2 for x,y in zip(ordered,ordered[1:]))
            for t in sorted(ts):
                pose(d,{i:qmap[prior[i]]+(qmap[new]-qmap[prior[i]])*t for i in ids})
            for i in ids: state[i]=new
            pose(d)
        else:
            for i in event.ids:
                o,_=pairs[i]
                wanted=o*r.STEP+c[o]+d+bias if event.value=='carrier' else ground[i]*r.STEP+g[ground[i]]
                assert math.isclose(height(i,d),wanted,abs_tol=1e-9)
    assert state==['G']*len(pairs) and ground==[t for o,t in pairs]
    assert math.isclose(d,-a)
    return samples, reverse_microtravel


def workload(kind='full', start=0):
    unequal=[p for p in PAIRS if p[0]!=p[1]]
    if kind=='full': return [[unequal[c%20] for c in range(80)] for _ in range(80)]
    return [[(0,c%5) if kind=='local' and start<=row<start+5 and c<5 else (0,0)
             for c in range(80)] for row in range(80)]


@lru_cache(None)
def separate_events(pairs):
    """Five-height E-098 pad/dog order. Ground dogs at a fixed datum; pads
    written at deck home. Real dual-plane access remains an explicit grant.
    """
    ids=tuple(i for i,p in enumerate(pairs) if p[0]!=p[1])
    if not ids:return []
    ev=[Event('write','pad_on',ids)]
    for h in sorted({pairs[i][0] for i in ids}):
        group=tuple(i for i in ids if pairs[i][0]==h)
        ev += [Event('move',h*r.STEP+2),Event('proof','pickup',group),Event('write','dog_off',group)]
    ev.append(Event('move',4*r.STEP+5))
    for h in sorted({pairs[i][1] for i in ids},reverse=True):
        group=tuple(i for i in ids if pairs[i][1]==h)
        ev += [Event('move',h*r.STEP+2),Event('write','dog_on',group),Event('move',h*r.STEP),Event('proof','ground',group)]
    return ev+[Event('move',-2.),Event('write','pad_off',ids)]


def replay_separate(pairs, errors, dog=.05, lip=1.05, subdivisions=4):
    """Finite tooth/dog and lip/pad intervals, same X/Y lanes as E-098.
    Every body is replayed through shared stops/return. Wider 10.1-mm tooth
    pitch only; no inherited full-machine or writer geometry qualification.
    """
    pads=[False]*len(pairs);dogs=[True]*len(pairs)
    seats=[o for o,t in pairs]; d=-2.; count=0
    def pose(dd):
        nonlocal count
        for i,(o,t) in enumerate(pairs):
            grounded=seats[i]*r.STEP+dog-errors[seats[i]]
            assert pads[i] or dogs[i]
            z=max(grounded,dd-lip) if pads[i] and dogs[i] else dd-lip if pads[i] else grounded
            if pads[i]: assert z+lip>=dd-1e-9
            if dogs[i]:
                teeth=[(z-j*r.STEP+err,z-j*r.STEP+err+1.3) for j,err in enumerate(errors)]
                assert all(r.overlap(t,(dog-1,dog))<1e-9 for t in teeth)
            support=(pads[i] and abs(z+lip-dd)<1e-9) or (dogs[i] and abs(z-grounded)<1e-9)
            assert support
            count+=1
    for ev in separate_events(pairs):
        if ev.kind=='move':
            ts={j/subdivisions for j in range(subdivisions+1)}
            if d!=ev.value:
                for seat in seats:
                    x=(seat*r.STEP+dog-errors[seat]+lip-d)/(ev.value-d)
                    if 0<x<1:ts.add(x)
            for t in sorted(ts):pose(d+(ev.value-d)*t)
            d=ev.value
        elif ev.kind=='write':
            for i in ev.ids:
                if ev.value=='pad_on':pads[i]=True
                elif ev.value=='pad_off':pads[i]=False
                elif ev.value=='dog_off':dogs[i]=False
                else:dogs[i]=True;seats[i]=pairs[i][1]
            pose(d)
        else:pose(d)
    assert seats==[t for o,t in pairs] and not any(pads) and all(dogs)
    return count


@lru_cache(None)
def bank_time(rows, family, slot=.1, proof=.1, v=200, acc=5000, overhead=2.):
    pairs=tuple(p for row in rows for p in row)
    if all(o==t for o,t in pairs): return dict(seconds=0.,slots=0,scans=0)
    mv=lambda distance:r.move(distance,v,acc)
    if family=='direct':
        pos=0;elapsed=0.;rounds=0;worst=0.
        for row,ps in enumerate(rows):
            active=[(o,t) for o,t in ps if o!=t]
            if not active:continue
            # Ideal bilateral head acquires at old, lifts .2 to unload ground,
            # moves to target+.2, seats .2, releases, then returns home.
            # Two transfer slots include grounded-dog handling/readback.
            path=max(sum(mv(x) for x in (o*r.STEP,.2,abs(t-o)*r.STEP,.2,t*r.STEP)) for o,t in active)
            elapsed+=mv((row-pos)*r.PITCH)+path+2*proof
            pos=row;rounds+=1;worst=max(worst,path)
        return dict(seconds=overhead+elapsed+mv(pos*r.PITCH)+worst+2*proof,slots=2*rounds,scans=1)
    evs=separate_events(pairs) if family=='separate' else key_events(pairs)
    d=-2. if family=='separate' else -.2
    rowpos=0;zpos=0.;elapsed=0.;slots=scans=proofs=0
    for ev in evs:
        if ev.kind=='move':elapsed+=mv(ev.value-d);d=ev.value
        elif ev.kind=='proof':elapsed+=proof;proofs+=1
        else:
            # Point-height fork: one common Z axis for 80 lateral fingers.
            # Height-major serpentine, retracted before all row/Z/deck motion.
            # Fixed-access tongue is a favorable physical alternative, not free
            # independent Z heads. Unknown compliance/packing time not credited.
            groups={}
            for j,i in enumerate(ev.ids):
                h=ev.heights[j] if family=='key_tiers' else 0.
                groups.setdefault(h,set()).add(i//80)
            for height,rr in sorted(groups.items(),reverse=bool(scans%2)):
                elapsed+=mv(height-zpos);zpos=height
                for row in sorted(rr,reverse=bool(scans%2)):
                    elapsed+=mv((row-rowpos)*r.PITCH)+slot
                    rowpos=row;slots+=1
                scans+=1
    elapsed+=mv(rowpos*r.PITCH)+mv(zpos)
    stroke=2.2 if family=='separate' else .4
    retry=slot+proof+2*mv(stroke)
    return dict(seconds=overhead+elapsed+retry,slots=slots,scans=scans,proofs=proofs)


@lru_cache(None)
def evaluate(family,banks,kind='full',start=0,slot=.1,proof=.1,v=200,acc=5000,overhead=2.):
    rows=workload(kind,start);n=80//banks
    worst=max((bank_time(tuple(tuple(row) for row in rows[i:i+n]),family,slot,proof,v,acc,overhead) for i in range(0,80,n)),key=lambda x:x['seconds'])
    channels=banks*({'key_tiers':83,'key_tongue':82,'separate':82,'direct':81}[family])
    return dict(**worst,channels=channels,allowance=(500-250)/channels)


def main():
    checks={};states=0
    # All 32 level-error patterns and both correlated/anticorrelated ladders.
    # Prior routing.py retains all 1024 independent pattern isolated routes.
    for g in it.product((-.05,.05),repeat=5):
        for c in (g,tuple(-x for x in g)):
            states+=replay(PAIRS,g,c)[0]
    checks['bank_patterns']=64;checks['key_states']=states
    checks['refinement_states']=[replay(PAIRS,(.01,-.023,.042,-.037,.016),(-.032,.011,-.015,.043,-.049),n)[0] for n in (1,4,16)]
    checks['carried_reversal_mm_sum']=replay(PAIRS,(0,)*5,(0,)*5)[1]
    checks['separate_states']=sum(replay_separate(PAIRS,err,dog,lip) for err in it.product((-.05,.05),repeat=5) for dog,lip in it.product((-.05,.05),(.95,1.05)))
    # Every two-cell old/new map; mixed signs, empty groups, identities.
    for pairs in it.product(PAIRS,repeat=2):replay(pairs,(0,)*5,(0,)*5)
    checks['two_cell_maps']=625
    # A constant bias already blocks initial bridge entry. Separately inject
    # it after acquisition: deposition remains carried .01 mm above ground.
    actual_d=r.STEP-.2+.11
    carried_z=r.STEP+.05+actual_d
    grounded_z=2*r.STEP-.05
    r.check_pose(0.,carried_z,actual_d,(-.05,)*5,(.05,)*5)
    assert math.isclose(carried_z-grounded_z,.01,abs_tol=1e-9)
    try:r.check_pose(-r.SHIFT,carried_z,actual_d,(-.05,)*5,(.05,)*5)
    except AssertionError:checks['faulted_deposit_gap_mm']=carried_z-grounded_z
    else:raise AssertionError('ground release accepted without support')
    try:replay(PAIRS,(-.05,)*5,(.05,)*5,bias=.11)
    except AssertionError:checks['common_bias_011_rejected']=True
    else:raise AssertionError('missed common-drive fault')
    full=tuple(p for row in workload()[:1] for p in row)
    assert sum(e.kind=='write' for e in key_events(full))==20
    assert sum(e.kind=='write' for e in separate_events(full))==12
    # Independent count: 2*(two acquisition writes*4 tiers + two deposit
    # writes*(4+3+2+1) tiers) = 56 stopped row-height settings.
    assert bank_time(tuple(tuple(row) for row in workload()[:5]),'key_tiers')['slots']==56*5
    for family in ('key_tiers','key_tongue','separate','direct'):
        assert evaluate(family,16,'none')['seconds']==0
    # Independent hand sums for dense five-row banks; event counting and
    # stopped carrier itinerary must agree with a separate arithmetic route.
    mv=r.move; n=5
    key_lift=10*mv(.4)+2*mv(r.STEP)+3*(mv(r.STEP-.4)+mv(r.STEP+.4))+2*mv(4*r.STEP)
    expected=2+20*n*.1+20*(n-1)*mv(r.PITCH)+key_lift+1+.1+.1+2*mv(.4)
    assert math.isclose(expected,evaluate('key_tongue',16)['seconds'])
    deck_lift=mv(4)+4*mv(r.STEP)+2*mv(3)+5*mv(2)+4*mv(r.STEP-2)+mv(2)
    expected=2+12*n*.1+12*(n-1)*mv(r.PITCH)+deck_lift+1+.1+.1+2*mv(2.2)
    assert math.isclose(expected,evaluate('separate',16)['seconds'])
    checks['independent_dense_timing_sums']=2
    out=dict(checks=checks,central={b:{f:evaluate(f,b) for f in ('key_tongue','key_tiers','separate','direct')} for b in BANKS})
    out['sensitivity']=[dict(v=v,acc=a,slot=s,first_passing={f:next((b for b in BANKS if evaluate(f,b,slot=s,proof=s,v=v,acc=a)['seconds']<30),None) for f in ('key_tongue','key_tiers','separate','direct')}) for v,a in ((80,1000),(200,5000),(400,20000)) for s in (.02,.05,.1,.2)]
    out['local']={f:{b:[min(ts),max(ts)] for b in (4,8,16) for ts in [[evaluate(f,b,'local',start)['seconds'] for start in range(76)]]} for f in ('key_tongue','key_tiers','separate','direct')}
    out['overhead6_B16']={f:evaluate(f,16,overhead=6)['seconds'] for f in ('key_tongue','key_tiers','separate','direct')}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
