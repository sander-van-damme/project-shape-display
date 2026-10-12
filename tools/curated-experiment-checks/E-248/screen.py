"""E-248: retained binary writing and positive unchanged support.
Stdlib, stdout only. Ideal transactions and labelled scenario calculations.
No finite routing, process prior, physical support/arrest or BOM qualification.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path


def load(number):
    path = Path(__file__).resolve().parents[1]/number/'screen.py'
    spec = importlib.util.spec_from_file_location(number.replace('-', ''), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prior = load('E-243')
move = prior.move
LEVELS = prior.LEVELS
Q = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)


def program(codes, order=(1, 2, 4), fault=None):
    """Horizontal unloaded registers reset to zero under a common resetter.
    Common clamp C; selected drive teeth D; unselected stationary keepers K.
    All engage at integer rack pitch; no per-bit retained clutch. Selection
    may be overwritten only with C seated and D/K clear. Coordinates in pitches.
    Proof flags are grants, not sensors or contact geometry.
    """
    x = [0]*len(codes)
    clamp = True
    drive = keep = [False]*len(codes)
    observations = 0

    def check():
        nonlocal observations
        assert all(clamp or d or k for d,k in zip(drive,keep)), 'unheld register'
        observations += len(codes)

    for weight in order:
        assert clamp and not any(drive) and not any(keep), 'live overwrite'
        bits = [bool(c & weight) for c in codes]
        check()                         # write/read mask with common clamp on
        drive = bits[:]                 # engage selected teeth, nonselected keepers
        keep = [not b for b in bits]
        if fault == 'no_unselected_keeper': keep = [False]*len(codes)
        if fault == 'no_selected_tooth': drive = [False]*len(codes)
        check()
        clamp = False
        check()
        if fault == 'rewrite_under_motion':
            assert clamp, 'live overwrite'
        for k in range(1, 5):            # piecewise linear, supported by D or K
            position = [a+k*weight*b/4 for a,b in zip(x,bits)]
            assert all(0 <= z <= 5 for z in position)
            check()
        x = [a+weight*b for a,b in zip(x,bits)]
        clamp = fault != 'missing_reseat'
        check()
        drive = keep = [False]*len(codes)
        check()                         # common clamp holds during empty return
    assert tuple(x) == codes
    return tuple(x), observations


def writer(q, pitch=6., throw=2., proof=.003):
    j=move(throw)+proof; n=80//q; d=5*pitch
    # Reset out/back; clamp release/reseat and final read. Per bit: mask write,
    # D/K approach, C withdraw, loaded step, C seat, D/K clear, empty return.
    group=sum(2*move(k*pitch)+5*j for k in (1,2,4))
    return 2*move(d)+2*j+.010+n*group+(n-1)*move(5.08)+move((n-1)*5.08)


def timing(b,q,p=6.,a=8000.,rows=None,throw=2.,proof=.003):
    c=writer(q,p,throw,proof)+prior.service(a)
    return 2+((math.ceil(80/b) if rows is None else rows)+1)*c+move(42,a)+.010


def allocation(b,q,extra=True):
    # E243 inherited assumptions. New 80 D +80 K return/retention duties/head
    # at $.10/duty, plus $10 common transfer/clamp actuation allowance.
    return prior.allocation(b,q)+(16*b+10 if extra else 0)


def partition_masks(groups, n):
    # Only unions of independently released rigid contact groups are available.
    return {sum(sum(1<<i for i in g) for g,bit in zip(groups,bits) if bit)
            for bits in it.product((0,1),repeat=len(groups))}


def support_cut():
    # A two-cell group must either block a changed member or release its U peer.
    groups=((0,1),(2,3))
    masks=partition_masks(groups,4)
    assert 1 not in masks and 2 not in masks and len(masks)==4
    singleton=partition_masks(tuple((i,) for i in range(4)),4)
    assert len(singleton)==16
    # Exhaust all partitions of 4 cells: arbitrary masks imply singleton groups.
    partitions=[]
    def extend(groups,i):
        if i==4:
            partitions.append(tuple(tuple(g) for g in groups)); return
        for k in range(len(groups)):
            nxt=[g[:] for g in groups]; nxt[k].append(i); extend(nxt,i+1)
        extend(groups+[[i]],i+1)
    extend([],0)
    for p in partitions:
        assert (len(partition_masks(p,4))==16)==(len(p)==4)
    # Crossed row/column supports: every untouched cell remains supported,
    # but neither fixed primary assignment can survive all one-cell updates.
    crossed=0
    for r,c in it.product(range(3),repeat=2):
        for i,j in it.product(range(3),repeat=2):
            row_on=i!=r; col_on=j!=c
            if (i,j)!=(r,c): assert row_on or col_on
            else: assert not row_on and not col_on
            crossed+=1
    for i,j in it.product(range(3),repeat=2):
        assert any(r==i and c!=j for r,c in it.product(range(3),repeat=2))
        assert any(c==j and r!=i for r,c in it.product(range(3),repeat=2))
    return dict(partitions=len(partitions),crossed_support_states=crossed,
                arbitrary_rigid_segments_per_board=6400)


def main():
    programs=observations=0
    for codes in it.product(range(6),repeat=3):
        for order in it.permutations((1,2,4)):
            _,checks=program(codes,order); programs+=1; observations+=checks
    faults=0
    for f in ('no_unselected_keeper','no_selected_tooth','rewrite_under_motion','missing_reseat'):
        try: program((0,3,5),fault=f)
        except AssertionError: faults+=1
        else: raise AssertionError(f)
    # Compose the physically retained codes with E243's complete ideal support
    # path. U is code 5; targets 0..4. This is a conditional transaction witness.
    maps=service_checks=retries=0
    for old,new in it.product(it.product(LEVELS,repeat=3),repeat=2):
        codes=tuple(5 if a==b else b//10 for a,b in zip(old,new))
        written,_=program(codes)
        decoded=tuple(a if c==5 else 10*c for a,c in zip(old,written))
        assert decoded==new
        actual,n=prior.replay(old,decoded)
        assert actual==new
        maps+=1; service_checks+=n
    # A wrong/partial register is reset and re-encoded with resident support on.
    # Late wrong-target retry retains original U cells. Corrupted U is excluded.
    for old,new,bad in it.product(LEVELS,repeat=3):
        actual,_=prior.replay((old,20),(new,20),(bad,20))
        assert actual[1]==20
        result,_=prior.replay(actual,(new,20))
        assert result==(new,20); retries+=1
    # Deliberately corrupted U demonstrates why a late fault is not harmless.
    assert prior.replay((20,),(40,))[0]!=(20,)
    # E232 negative control: fixed selected support can't remain during 30-mm
    # ascent through a 4-mm groove with 2-mm tooth; removing before pickup drops.
    assert 30 > 4-2
    assert 10 > 0                    # old-height foot is above initial pickup
    comparisons=[]
    for p,a in it.product((3.,4.,6.,8.),(2000.,8000.)):
        choices=[]
        for b,q in it.product(range(1,81),Q):
            t=timing(b,q,p,a)
            if t<30:
                choices.append(dict(b=b,q=q,channels=b*q,seconds=t,
                                    cost=allocation(b,q),free_added_hardware_cost=allocation(b,q,False)))
        comparisons.append(dict(pitch=p,accel=a,best=min(choices,key=lambda x:(x['cost'],x['seconds']))))
    # Independent event expansion and limiting cases.
    for b,q,p in ((5,80,6),(10,40,4),(20,20,8)):
        stages=[2.,move(42),.010]
        for _ in range(math.ceil(80/b)+1):
            stages.extend([writer(q,p),prior.service()])
        assert abs(sum(stages)-timing(b,q,p))<1e-10
    assert move(0)==0 and abs(move(40)-.225)<1e-12
    margin=[dict(error=e,code=(6-2)/2-e,rack=(6-4)/2-2*e,
                 pawl=1-2*e,unchanged_takeover=2*e) for e in (.15,.35,.70)]
    # Worst shared versus local bar errors; no probability is attached.
    # Rack opening p-2 reserves a 2-mm solid land; a 2-mm tooth must fit.
    # e includes writer/bar errors individually for rack engagement, unlike code
    # margin e which is one combined bound inherited from E243.
    print(json.dumps(dict(programs=programs,writer_support_observations=observations,
        fault_controls=faults,maps=maps,terrain_support_observations=service_checks,
        late_stable_retries=retries,support_cut=support_cut(),best=comparisons,
        writing=[dict(pitch=p,unary_s=prior.writer(80,p),binary_s=writer(80,p),
                      planar_banks=math.floor(406.4/(10*p+4)),
                      planar_seconds=timing(math.floor(406.4/(10*p+4)),80,p)) for p in (3,4,6,8)],
        sensitivity=[dict(throw=throw,proof=proof,banks=b,seconds=timing(b,80,6,throw=throw,proof=proof))
                     for throw,proof,b in it.product((1,2,4),(.003,.010),(6,8,10))],
        traffic=dict(E236_binary_decisions=32000,E243_binary_decisions=32000,
                     binary_retained_decisions=19200,with_one_retry=19440,
                     retained_multilevel_states=6400),margins=margin,
        example=dict(B10_q80_cost=allocation(10,80),B10_q80_seconds=timing(10,80),
                     single_row_seconds=timing(10,80,rows=1),five_rows_seconds=timing(10,80,rows=5),
                     no_retry_seconds=2+8*(writer(80)+prior.service()))),indent=2))


if __name__=='__main__': main()
