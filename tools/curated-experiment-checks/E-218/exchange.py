"""E-218: direct-support exchange; ideal rigid contacts and labelled bounds.
Standard library, stdout only. No FDM priors, CAD, sensors or hardware validation.
"""
import itertools
import json
import math

HEIGHTS = (0, 10, 20, 30, 40)
TRAVEL = 45  # 40 height + 4 solid base + 1 insertion clearance, mm


def move(d, a, v=200):
    d = abs(d)
    return 2 * math.sqrt(d / a) if d <= v*v/a else d/v + v/a


def states(old, new):
    """Exact contact events plus interval midpoints, not a time discretization.
    Each height is max(old support, incoming support). Between events it is
    affine: endpoint tests establish support/neighbor/monotonicity invariants.
    Disjoint lateral bearing lanes and an arrested carriage are assumptions.
    """
    events = []
    for phase in ('incoming_up', 'outgoing_down'):
        cuts = {-TRAVEL, 0}
        cuts.update(o-n if phase == 'incoming_up' else n-o for o,n in zip(old,new))
        cuts = sorted(x for x in cuts if -TRAVEL <= x <= 0)
        samples = sorted(set(cuts) | {(x+y)/2 for x,y in zip(cuts,cuts[1:])})
        if phase == 'outgoing_down': samples.reverse()
        for z in samples:
            a, b = (0,z) if phase == 'incoming_up' else (z,0)
            supports = [(o+a,n+b) for o,n in zip(old,new)]
            events.append((phase,z,tuple(max(s) for s in supports),supports))
    return events


def replay(old,new):
    previous = old
    for phase,z,h,supports in states(old,new):
        for o,n,p,x,s in zip(old,new,previous,h,supports):
            assert min(o,n) <= x <= max(o,n)
            assert x in s
            assert (n-o)*(x-p) >= 0
            if o == n: assert x == o
        previous = h
    assert tuple(previous) == tuple(new)


def authorize(stage, old, new, *, target_read=True, keeper=True, arrested=True):
    """Interlocks specify required proof; booleans are NOT implemented sensing."""
    if stage == 'insert':
        assert target_read and keeper and arrested
        assert max(new)-TRAVEL <= -4-1  # below resident solid base
    elif stage == 'release_old_dock':
        assert keeper and arrested  # old cradle takes load before dock opens
    elif stage == 'withdraw_old':
        assert max(old)-TRAVEL <= -4-1
        assert target_read and keeper  # new frame dock closed and target proved
    else:
        raise ValueError(stage)


def row_time(q,a,aux=.5,arrest='continuous',terrace=8):
    """80 targets; no old-code rewrite. Optimistic integrated under-row writer.
    No 406-mm side feed: old cassette becomes next spare on the moving head.
    All operations serial; programming, empty returns and one row hop charged.
    Common dock/proof/release/read allowance is unresolved, not measured.
    """
    groups = math.ceil(80/q)
    writing = groups*(move(4*terrace,a)+2*move(2,a)+.005)
    writing += (groups-1)*move(5.08,a)
    if arrest == 'continuous':
        vertical = 4*move(TRAVEL,a)  # two loaded strokes and two empty resets
    else:
        # Constructed fallback: common 1-mm indexed rack escapement;
        # each loaded step stops and takes 1-ms dog proof, empty resets continuous.
        vertical = 2*TRAVEL*(move(1,a)+.001)+2*move(TRAVEL,a)
    # 2.4-mm lane change and its return, then bank row travel.
    return writing+vertical+2*move(2.4,a)+move(5.08,a)+aux


def schedule(b,q,a,**kwargs):
    # Slowest contiguous bank; 2 s global allowance plus one full-row retry.
    return 2+(math.ceil(80/b)+1)*row_time(q,a,**kwargs)


def packing(terrace=8,error=.7,foot=2,frame=4):
    # Five terraces; selection shifts by four terraces. Union of all positions.
    sweep = 9*terrace+frame
    return dict(terrace_mm=terrace,swept_row_depth_mm=sweep,
                phases=math.ceil(sweep/5.08),
                terrace_margin_mm=(terrace-foot)/2-error,
                # An independent full vertical exchange envelope per phase:
                vertical_envelope_mm=44+TRAVEL+1,
                staggered_depth_mm=math.ceil(sweep/5.08)*(44+TRAVEL+1))


def adjacent_collisions(pitch=5.08, terrace=8):
    # Solid 4-mm bases share z and x. Independent code shifts are discrete.
    collisions = 0
    for a,b in itertools.product(range(5), repeat=2):
        left = (-a*terrace, (5-a)*terrace)
        right = (pitch-b*terrace, pitch+(5-b)*terrace)
        collisions += min(left[1],right[1]) > max(left[0],right[0])
    return collisions


def checks():
    count = 0
    for six in itertools.product(HEIGHTS,repeat=6):
        replay(six[:3],six[3:]); count += 1
    witness = ((40,0,20),(0,40,20))
    assert [max(o,n) for o,n in zip(*witness)] == [40,40,20]
    for stage in ('insert','release_old_dock','withdraw_old'):
        authorize(stage,*witness)
    faults = [('insert',dict(target_read=False)),('insert',dict(keeper=False)),
              ('release_old_dock',dict(arrested=False)),('withdraw_old',dict(keeper=False))]
    for stage,kw in faults:
        try: authorize(stage,*witness,**kw)
        except AssertionError: pass
        else: raise AssertionError('fault escaped')
    # Common-height alignment cannot simultaneously touch all old heights.
    assert len({o-n for o,n in zip(*witness)}) == 3
    # Endpoints suffice for affine support branches; compare dense holdout.
    for o,n in itertools.product(HEIGHTS,repeat=2):
        for k in range(451):
            z = -45+k/10
            assert min(o,n) <= max(o,n+z) <= max(o,n)
            assert min(o,n) <= max(o+z,n) <= max(o,n)
    # Ideal 1-mm positive arrest bounds displacement by 1 mm because max is
    # 1-Lipschitz. Capacity/impact/spring dogs are explicitly unqualified.
    for phase,z,h,_ in states(*witness):
        a,b = (0,z-1) if phase == 'incoming_up' else (z-1,0)
        after = [max(o+a,n+b) for o,n in zip(*witness)]
        assert all(0 <= x-y <= 1 for x,y in zip(h,after))
    # Independent scalar limiting checks.
    assert math.isclose(move(40,2000),.3)
    assert packing(8)['phases'] == 15
    assert adjacent_collisions() == 25
    assert adjacent_collisions(pitch=72) == 0
    # Even ZERO frame and zero error cannot fit a 2-mm foot's five-step medium.
    assert 9*2 > 5.08
    return count


def main():
    n = checks()
    rows=[]
    for arrest,a,b in itertools.product(('continuous','indexed'),(2000,8000),(1,2,4,8,16)):
        passing=[q for q in (1,2,4,8,16,40,80) if schedule(b,q,a,arrest=arrest)<30]
        if passing:
            q=min(passing)
            rows.append(dict(arrest=arrest,a=a,b=b,q=q,channels=b*q,
                             seconds=round(schedule(b,q,a,arrest=arrest),3)))
    b=16
    sliders=80*(80+b)
    print(json.dumps(dict(
        evidence='ideal contact replay and calculations; all engineering bounds assumed',
        checks=dict(three_column_maps=n,interlock_faults=len(('read','keeper','arrest','dock'))),
        witness=[dict(phase=p,z=z,height=h) for p,z,h,_ in states((40,0,20),(0,40,20))],
        timing_relaxation_survivors=rows,
        timing_sensitivity={str((q,aux)):round(schedule(16,q,8000,aux=aux),3)
                            for q,aux in itertools.product((8,16),(.25,.5,1,2))},
        packing=[packing(t) for t in (2,4,8)],
        adjacent_static_code_collisions=adjacent_collisions(),
        resident_cassettes=80,spares_at_16_heads=16,slider_total=sliders,
        terrace_faces=5*sliders,retention_notches=5*sliders,
        stock_cm3=sliders*1.6*8*sum(4+h for h in HEIGHTS)/1000,
        media_print_hours={str(rate):round(sliders*1.6*8*sum(4+h for h in HEIGHTS)/rate/3600,3) for rate in (5,15)},
        media_assembly_hours={str(sec):round(sliders*sec/3600,3) for sec in (10,30)},
        tolerance=[dict(error=e,overlap=1.6-e,terrace_margin=3-e,
                        unchanged_difference_bound=2*e) for e in (.15,.35,.70)],
        force=[dict(F=f,row_N=80*f,step_work_J=80*f*.04,
                    ideal_torque_Nm=80*f*.01) for f in (1,3.27,10)],
        comparison=dict(e216_channels=256,e216_s=21.167,e217_binary_channels=384,e217_binary_s=23.929),
    ),indent=2))

if __name__ == '__main__': main()
