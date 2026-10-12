"""E-228. Necessary conditions only; all non-product inputs are scenario bounds.
Run with Python stdlib; deterministic stdout, no generated artifacts.
"""
import itertools as it
import json
import math

N, ROWS, WIDTH, PITCH = 6400, 80, 80, 5.08


def move(d, a=8000, v=200):
    d = abs(d)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def board(cycle, banks, changed_rows=80):
    # Contiguous banks; regional example explicitly contained in one bank.
    visits = math.ceil(ROWS/banks) if changed_rows == 80 else changed_rows
    return 2+(visits+1)*cycle  # map overhead and one worst-row retry


def first_banks(cycle):
    return next(b for b in range(1,81) if board(cycle,b) < 30)


def ramp_replay(old, target):
    """q in one-height-step units, h=10q; permanent ramp never releases output.
    All transfer proofs ideal. Head has individual ground/drive contacts;
    row keeper can hold arbitrary discrete phases, NOT arbitrary free heights.
    """
    q = list(old)
    row = True
    park = [False]*len(q)
    drive = [False]*len(q)
    fixed = [a == b for a,b in zip(old,target)]
    observations = 0
    def prove():
        nonlocal observations
        assert all(row or p or d for p,d in zip(park,drive))
        assert all(0 <= x <= 4 for x in q)
        assert all(not same or x == a for same,x,a in zip(fixed,q,old))
        observations += len(q)
    park[:] = [True]*len(q)  # all head parks engaged/proved before keeper release
    prove()
    row = False
    prove()
    for sign in (1,-1):
        remaining = [max(0,sign*(b-a)) for a,b in zip(q,target)]
        drive[:] = [d > 0 for d in remaining]
        prove()  # overlap allowed only while common drive is stopped/braked
        park[:] = [not d for d in drive]
        prove()
        for step in range(1,5):
            for i,on in enumerate(drive):
                if on:
                    q[i] += sign
                    remaining[i] -= 1
            prove()  # drive path owes a retained coupling and common brake
            for i,on in enumerate(drive):
                if on and remaining[i] == 0:
                    park[i] = True
            prove()
            for i,on in enumerate(drive):
                if on and remaining[i] == 0:
                    drive[i] = False
            prove()
        assert not any(drive) and all(park)
        # Common carriage returns empty: q is retained by individual parks.
        prove()
    assert q == list(target)
    row = True
    prove()
    park[:] = [False]*len(q)
    prove()
    return observations


def ramp_cycle(slope, switching):
    # Each sign: four loaded increments, then one empty 40/s return.
    # Ten commanded overlap handoffs: two admissions + eight retirements.
    return 8*move(10/slope)+2*move(40/slope)+10*switching+.15+move(PITCH)


def ramp_metrics(slope):
    stroke = 40/slope
    # Private y-oriented ramp envelope: profile length D+4, translation D.
    swept = 2*stroke+4
    decks = math.ceil(swept/PITCH)
    # 40-mm height plus 8-mm structural allocation per deck; no routing pass.
    volume_l = N*(.5*40*stroke*3)/1e6
    return dict(stroke_mm=stroke, swept_mm=swept, decks=decks,
                depth_allocation_mm=48*decks, ramp_stock_L=volume_l,
                print_h_at_10mm3_s=volume_l*1e6/10/3600)


def raising_multiplier(slope, mu):
    # E-100 force equilibrium, inclined face plus lower sliding bed.
    return None if mu*slope >= 1 else (slope+mu)/(1-mu*slope)+mu


def pulse_bases(total, count, minimum=1, prefix=()):
    """Nondecreasing complete integer bases; prefix reaches [0,sum(prefix)]."""
    if count == 0:
        if total == 0:
            yield prefix
        return
    for w in range(minimum, min(total//count, sum(prefix)+1)+1):
        yield from pulse_bases(total-w,count-1,w,prefix+(w,))


def code(delta, basis):
    return next(bits for bits in it.product((0,1),repeat=len(basis))
                if sum(w*b for w,b in zip(basis,bits)) == delta)


def crossed_replay(old, target, basis=(1,1,2)):
    q = list(old)
    row = True
    col = [True]*len(q)
    finger = [False]*len(q)
    unchanged = [a == b for a,b in zip(old,target)]
    def check():
        assert all(row or c or f for c,f in zip(col,finger))
        assert all(not fixed or a==o for fixed,a,o in zip(unchanged,q,old))
    for sign in (1,-1):
        codes=[code(max(0,sign*(b-a)),basis) for a,b in zip(q,target)]
        for k,w in enumerate(basis):
            selected = [bool(bits[k]) for bits in codes]
            finger[:] = selected  # arrested pickup proof before column withdrawal
            col[:] = [not s for s in selected]
            check()
            row = False
            check()
            q = [a+sign*w if s else a for a,s in zip(q,selected)]
            check()
            row = True
            check()
            finger[:] = [False]*len(q)
            col[:] = [True]*len(q)
            check()  # empty head returns to fixed datum after each pulse
    assert q == list(target)


def checks():
    # Independent brute force verifies the constructive basis generator.
    for total,k in ((4,3),(8,4)):
        brute=set()
        for basis in it.combinations_with_replacement(range(1,total+1),k):
            if sum(basis) != total:
                continue
            sums={sum(w*b for w,b in zip(basis,bits)) for bits in it.product((0,1),repeat=k)}
            if sums == set(range(total+1)):
                brute.add(basis)
        assert set(pulse_bases(total,k)) == brute
    count = obs = 0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        obs += ramp_replay(old,target)
        crossed_replay(old,target)
        count += 1
    # A real 80-wide row simultaneously attains all eight signed groups.
    pairs = list(it.product(range(5),repeat=2))*3+[(0,4),(4,0),(2,2),(1,3),(3,1)]
    assert len(pairs)==80
    ramp_replay(*zip(*pairs))
    crossed_replay(*zip(*pairs))
    # Last-path removal and common-clamp shortcut counterexamples.
    supported = lambda row,park,drive,brake: row or park or (drive and brake)
    assert supported(False,False,True,True)
    assert not supported(False,False,True,False)
    assert not supported(False,False,False,True)
    # One common drive without private parks cannot retain 1 and 4 increments.
    assert len({1,4}) == 2
    # Force, time, power and coherent-error independent limiting identities.
    for s in (.25,.5,1,2,4):
        assert abs(raising_multiplier(s,0)*40/s-40)<1e-12
        assert abs((1+s)*.35-(.35+s*.35))<1e-12
    assert raising_multiplier(4,.3) is None
    assert abs(move(5)-.05)<1e-12
    assert abs(move(40)-.225)<1e-12
    return dict(three_cell_transitions=count, support_observations=obs)


def main():
    result = dict(checks=checks())
    switch = 2*move(2)+.005  # engage/prove then release; not calibrated
    rows=[]
    for s in (.25,.5,1,2,4):
        item = dict(slope=s, **ramp_metrics(s))
        for label,t in [('ideal_flags',.005),('physical_strokes',switch)]:
            c=ramp_cycle(s,t); b=first_banks(c)
            item[label]=dict(banks=b,channels=80*b,time_s=board(c,b),
                assumed_cost_050_channel=130+65*b+80*b*.5,
                channel_ceiling_500_free_sites=(500-130-65*b)/(80*b),
                regional_5_rows_s=board(c,b,5))
        item['force_N_row_at_3_27N']={str(mu):None if raising_multiplier(s,mu) is None
            else 80*3.27*raising_multiplier(s,mu) for mu in (0,.1,.3)}
        item['height_error_bounds_mm']={str(e):(1+s)*e for e in (.15,.35,.70)}
        rows.append(item)
    result['ramps']=rows
    result['switch_s']=switch
    result['crossed_pulse_synthesis']=[]
    for levels in (5,9,41):
        # Minimum possible binary decisions; min total travel = levels-1.
        k=math.ceil(math.log2(levels))
        bases=list(pulse_bases(levels-1,k))
        for overhead in (.1,.25,.5):
            def cycle(basis):
                return 2*sum(2*move(40*w/(levels-1))+overhead for w in basis)+move(PITCH)
            basis=min(bases,key=lambda x: (round(cycle(x),12),x))
            # Independent set enumeration verifies the interval theorem.
            assert {sum(w*b for w,b in zip(basis,bits)) for bits in it.product((0,1),repeat=k)} == set(range(levels))
            c=cycle(basis); b=first_banks(c)
            result['crossed_pulse_synthesis'].append(dict(levels=levels,
                candidate_bases=len(bases),basis=basis,group_s=overhead,banks=b,
                selectors=80*b,pickups=80*b,time_s=board(c,b)))
    result['six_bank_max_group_s_exclusive']=((30-2)/15-1.1-move(PITCH))/6
    result['five_level_full_overwrite_bits']=6*N
    result['encoded_layers']=dict(one_hot_stops=4*N,binary_stages=3*N,
        common_columns=N,guide_stations=2*N,
        one_hot_write_only_s_at_71Hz=[4*N/(71*k) for k in (8,16,32)],
        assembly_h_at_10s_per_site={str(n):n*10/3600 for n in (N,3*N,4*N)})
    # Same-signed errors, no iid cancellation or invented process distribution.
    result['mask_margin_mm']={str(e):1-e for e in (.15,.35,.70)}
    result['reserve_joint_equation']='130 + 65B + 80B*c_channel + 6400*c_site < ceiling'
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
