"""E-243: ideal head-only overrunning support and retained target cam screen.
Stdlib, stdout only. Dimensions, dynamics, prices and errors are labelled bounds.
No contact, manufacture, sensing, arrest or hardware qualification.
"""
import itertools as it
import json
import math

LEVELS = tuple(range(0, 41, 10))
U = None


def move(mm, a=8000., v=200.):
    d = abs(mm)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def replay(old, target, wrong=None, gate=True):
    """Unilateral ideal supports. Pawls carry from below and overrun upward.
    Conditional mode/cam release is explicit; admission is not an oracle.
    Fixed pickup mask is derived from retained U vs target code.
    """
    code = tuple(U if a == b else b for a,b in zip(old,target))
    if wrong is not None:
        code = tuple(wrong[i] if code[i] is not U else U for i in range(len(old)))
    h = list(old)
    checks = 0
    # All head pawls engage before resident row-comb withdrawal.
    for plane in range(0, 43):
        for i,c in enumerate(code):
            if c is not U:
                h[i] = max(old[i], plane)
                # If below its original foot, pickup cannot carry: fixed pawl does.
                support = plane >= old[i] or h[i] == old[i]
            else:
                support = h[i] == old[i]
            assert support
            if old[i] == target[i]: assert h[i] == old[i]
            checks += 1
    # Selected pawls forcibly clear at apex; U pawls remain engaged.
    for plane in range(42, -1, -1):
        for i,c in enumerate(code):
            if c is not U:
                # Ungated ratchet catches the highest available level instead.
                stop = c if gate else 40
                h[i] = max(plane, stop)
                assert h[i] == plane or h[i] == stop
            else:
                assert h[i] == old[i]
            checks += 1
    # Prove all discrete seats, insert resident comb, then remove head.
    assert all(x in LEVELS for x in h)
    return tuple(h), checks


def writer(q, pitch=6.):
    # One horizontal target register, six positions (U plus five targets).
    # Common reset out/back, clamp open/close. q selectable pushing fingers.
    # Each group uses five stopped increments; early-released bars need drag.
    # All group outputs preset, five selective releases and final clear, empty return, group index.
    n=80//q; d=5*pitch; j=move(2)+.003
    return 2*move(d)+2*j+.010+n*(5*move(pitch)+7*j+move(d))+(n-1)*move(5.08)+move((n-1)*5.08)


def service(a=8000., proof=.003):
    j=move(2)+proof
    # Pickup mask on/off, pawl approach/withdraw, resident comb out/in,
    # common ascent/descent mode out/back: eight actual contact-stage grants.
    # Rise stopped at every old level to prove takeover, including zero.
    ascent=4*move(10,a)+move(2,a)+5*proof
    # At target+1: cam allows 2-mm pawl return then prove; move final 1 mm,
    # prove bearing before pickup continues. Cam phase tied to descent, no
    # independent phase-carriage teleportation or five command rewrites.
    descent=move(1,a)+5*(move(1,a)+j+proof)+4*move(9,a)
    return 8*j+ascent+descent+move(5.08)+.020


def timing(b,q,pitch=6.,a=8000.,rows=None):
    c=writer(q,pitch)+service(a)
    # No buffer overlap; code is needed throughout service. One causal full
    # retry after stable resident reseating; independent empty reset/read added.
    return 2+(math.ceil(80/b) if rows is None else rows)*c+c+move(42,a)+.010


def allocation(b,q):
    # Comparator allocations, NOT quotes: common reserve E239 categories,
    # bank reader/arrest/mounts, $.50 complete binary writers, $.02 media holds,
    # $.10 per pawl spring/pivot and per cam/pickup return = 160 duties/head.
    return 195+20*b+.50*b*q+.02*80*b+.10*160*b


def main():
    maps=observations=retries=0
    for old in it.product(LEVELS,repeat=3):
        for new in it.product(LEVELS,repeat=3):
            actual,n=replay(old,new); assert actual==new
            maps+=1; observations+=n
    for old in it.product(LEVELS,repeat=2):
        for new in it.product(LEVELS,repeat=2):
            for bad in LEVELS:
                actual,_=replay(old,new,(bad,bad))
                final,_=replay(actual,new); assert final==new
                retries+=1
    # Negative control: one-way support alone does NOT encode target.
    assert replay((10,30,20),(20,0,20),gate=False)[0]==(40,40,20)
    # Every stable partial position can be recovered by absolute re-encoding.
    partial_retries=0
    for actual in it.product(LEVELS,repeat=2):
        for target in it.product(LEVELS,repeat=2):
            assert replay(actual,target)[0]==target
            partial_retries+=1
    # Interrupted ascent must use actual seated state, not old requested delta.
    partial=(40,40,20); target=(20,0,20)
    assert replay(partial,target)[0]==target
    assert tuple(x+b-a for x,a,b in zip(partial,(10,30,20),target)) != target
    assert abs(move(40)-.225)<1e-12 and move(0)==0
    rows=[]
    for p,a in it.product((4.,6.,8.),(2000.,8000.)):
        choices=[]
        for q in (1,2,4,5,8,10,16,20,40,80):
            for b in range(1,81):
                t=timing(b,q,p,a)
                if t<30:
                    choices.append(dict(pitch=p,accel=a,banks=b,q=q,channels=b*q,
                        seconds=t,cost=allocation(b,q),pawls=80*b,cam_bars=80*b,
                        full_row_cycle=writer(q,p)+service(a),writer=writer(q,p),service=service(a)))
                    break
        rows.append(min(choices,key=lambda x:(x['cost'],x['seconds'])))
    # Planar register swept length: six-state bar length D+4 plus D setting
    # excursion plus global 4p reader sweep; 14p+4 mm (union bound allocation).
    # Global sweep direction can share slider excursion; simple nested enclosure
    # grants maximum instead of sum: bar D+4 + max(D,4p) = 10p+4 mm.
    # Both are layout allocations, not finite CAD. Test the more favorable one.
    packing=[]
    for p in (4.,6.,8.):
        depth=10*p+4; maxbanks=math.floor(406.4/depth)
        q=80
        packing.append(dict(pitch=p,depth_mm=depth,max_banks=maxbanks,
                            best_same_plane_s=timing(maxbanks,q,p)))
    # Independent schedule expansion proves retry included rather than prefetched.
    for b,q in ((5,80),(8,40),(16,20)):
        clock=2.
        for _ in range(math.ceil(80/b)):clock+=writer(q)+service()
        clock+=move(42)+.010
        clock+=writer(q)+service()
        assert abs(clock-timing(b,q))<1e-10
    # Old support ratchet clicks: h crosses each higher level once, for changed.
    clicks=sum((40-o)//10 for o,t in it.product(LEVELS,repeat=2) if o!=t)
    print(json.dumps(dict(checks=dict(maps=maps,support_observations=observations,
        stable_wrong_code_retries=retries,stable_partial_retries=partial_retries,expanded_schedules=3),best=rows,
        same_plane=packing,common= dict(J=move(2)+.003,service=service(),
        writer_q80=writer(80),writer_q40=writer(40),writer_q20=writer(20),
        negative_ungated=[40,40,20],ratchet_clicks_all_20_changed_pairs=clicks),
        margin=[dict(error=e,code_pitch=p,code_margin=(p-2)/2-e,
             insertion_margin=1-2*e,opposed_takeover_mm=2*e)
             for e,p in it.product((.15,.35,.70),(4,6,8))],
        sensitivity=[dict(extra_seconds_per_row=x,banks=b,
           seconds=timing(b,80)+(math.ceil(80/b)+1)*x)
           for b,x in it.product((5,6,8), (0,.1,.25))]),indent=2))

if __name__=='__main__': main()
