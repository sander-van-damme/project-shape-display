"""E-236: finite supported moving-datum synthesis. Stdlib, stdout only.
All physical motion, prices, proof, force and error inputs are unqualified bounds.
No CAD or hardware acceptance. Run from any directory.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e229', Path(__file__).resolve().parents[1]/'E-229'/'screen.py')
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
move = control.move
LEVELS = range(5)


def path(seq, old, bits):
    h, q, depth, travel = old, 0, 5, 0  # resident combs need shelves 0..-50 mm
    heights = [h]
    for d, on in zip(seq, bits):
        if on:
            depth = max(depth, 2+h-q)  # pickup plane -20+10q, material z=plane-10h
        q += d
        h += d*on
        travel += abs(d)*on
        if h not in LEVELS:
            return None
        heights.append(h)
    return h, depth, travel, tuple(heights)


def codes(seq, shelf_depth=None):
    """Exhaust all masks; unchanged output must never move, not just return.
    Choose least shelf depth, then least travel, then deterministic bit order.
    No independence probability or physical reader is implied.
    """
    result = {}
    for old, target in it.product(LEVELS, repeat=2):
        candidates = []
        for bits in it.product((0,1), repeat=len(seq)):
            if old == target and any(bits):
                continue
            p = path(seq, old, bits)
            if p and p[0] == target and (shelf_depth is None or p[1] <= shelf_depth):
                candidates.append((p[1], p[2], bits, p[3]))
        if not candidates:
            return None
        result[old,target] = min(candidates)
    return result


def reachable(seq, old):
    """Independent dynamic-programming check without shelf constraints."""
    reach = {old}
    for d in seq:
        reach |= {h+d for h in reach if h+d in LEVELS}
    return reach


def synthesize():
    counts, finalists = [], []
    for n in range(2,6):
        tested = valid = retained = 0
        best = None
        # Closed pickup walk inside -40..0 mm; at most 40 mm per stroke.
        for middle in it.product(range(-4,1), repeat=n-1):
            q = (0,)+middle+(0,)
            seq = tuple(b-a for a,b in zip(q,q[1:]))
            if 0 in seq:
                continue
            tested += 1
            if not all(len(reachable(seq,h)) == 5 for h in LEVELS):
                continue
            valid += 1
            table = codes(seq,6)
            if table is None:
                continue
            retained += 1
            score = (sum(move(10*abs(d)) for d in seq)+n*control.transfer(),
                     max(c[1]-abs(b-a) for (a,b),c in table.items()), seq)
            if best is None or score < best:
                best = score
        counts.append(dict(pulses=n,tested=tested,reachable=valid,
                           seven_shelf_survivors=retained,best=best))
        if best:
            finalists.append(best)
    winner = min(finalists)
    # To reach both 0->4 and 4->0, total positive and negative motion each
    # >=40 mm. Every nonzero stroke is >=10 mm, hence trapezoidal here:
    # motion >=80/200+n*.025. At n>=6 even FREE writing loses to winner.
    assert .4+6*.025+6*control.transfer() > winner[0]
    return counts, winner[2]


def replay(seq, table, old, target, fault=None):
    h = list(old); q = 0; row = True
    col = [True]*len(h); pickup = [False]*len(h)
    masks = [table[a,b][2] for a,b in zip(old,target)]
    observations = 0
    def check():
        nonlocal observations
        assert all(row or c or f for c,f in zip(col,pickup)), 'last load path'
        assert all(a!=b or x==a for a,b,x in zip(old,target,h)), 'unchanged moved'
        assert all(x in LEVELS for x in h)
        observations += 1
    for j,d in enumerate(seq):
        assert row and all(col) and not any(pickup), 'unsafe overwrite'
        mask = [bool(bits[j]) for bits in masks]
        actual = mask[:]
        if fault == 'write': actual[0] = not actual[0]
        assert actual == mask, 'mask proof'
        pickup[:] = actual
        for x,on in zip(h,pickup):
            if on: assert 0 <= 2+x-q <= 6, 'missing shelf'
        check()
        if fault == 'pickup': pickup[:] = [False]*len(h)
        assert pickup == mask, 'pickup proof'
        row = False; col[:] = [not on for on in mask]; check()
        if fault == 'brake': assert not any(pickup), 'arrest absent'
        if fault == 'active_rewrite': pickup[:] = [False]*len(h); check()
        q += d
        h[:] = [x+d*on for x,on in zip(h,mask)]; check()
        row = True; col[:] = [True]*len(h); check()
        if fault == 'reseat': row = False; col[:] = [False]*len(h)
        assert row and all(col), 'resident support proof'
        pickup[:] = [False]*len(h); check()
    assert q == 0 and h == list(target)
    return observations


def schedule(seq, w, banks, buffered=False, throw=2, rows=None):
    visits = math.ceil(80/banks) if rows is None else rows
    # One complete causal retry from measured stable heights, plus empty return
    # from deepest partial datum after safe support reseat/finger withdrawal.
    qs = list(it.accumulate(seq, initial=0))
    recovery = move(10*max(abs(q) for q in qs))+.010
    services = [move(10*abs(d))+control.transfer(throw)+
                (move(5.08) if k==len(seq)-1 else 0)
                for _ in range(visits+1) for k,d in enumerate(seq)]
    if not buffered:
        return 2+recovery+sum(services)+len(services)*w
    select = move(2)+.003
    ready, end = [], []
    for i,s in enumerate(services):
        ready.append(max(ready[-1] if ready else 0,
                         end[i-2] if i>=2 else 0)+w+select)
        end.append(max(ready[-1],end[-1] if end else 0)+select+s)
    assert end[-1] >= len(services)*(w+select)
    assert end[-1] >= sum(services)+len(services)*select+w
    return 2+recovery+end[-1]


def main():
    counts, seq = synthesize()
    table = codes(seq,6)
    assert all(len(reachable(seq,h))==5 for h in LEVELS)
    # Four-pulse sum/subset arithmetic alone is insufficient under output bounds.
    false_code = (3,-1,-3,1)
    assert {sum(d*b for d,b in zip(false_code,bits))
            for bits in it.product((0,1),repeat=4)} >= set(range(-4,5))
    assert codes(false_code) is None
    cases = obs = 0
    for old,target in it.product(it.product(LEVELS,repeat=3),repeat=2):
        obs += replay(seq,table,old,target); cases += 1
    for fault in ('write','pickup','brake','active_rewrite','reseat'):
        try: replay(seq,table,(0,4,2),(4,0,2),fault)
        except AssertionError: pass
        else: raise AssertionError('fault escaped: '+fault)
    # Every partial stable output and every desired level gets a newly generated
    # code after empty reset; unchanged cells of that retry receive all-zero masks.
    retries = 0
    for (old,target), entry in table.items():
        for h in entry[3]:
            replay(seq,table,(h,),(target,)); retries += 1
    # Conservative sequential four-stage time cross-check and predecessor.
    w = control.writer('direct',80)['seconds']
    qmax = max(abs(q) for q in it.accumulate(seq,initial=0))
    for b in (1,5,80):
        cycle = sum(move(10*abs(d)) for d in seq)+len(seq)*(control.transfer()+w)+move(5.08)
        assert abs(schedule(seq,w,b)-(2+move(10*qmax)+.010+(math.ceil(80/b)+1)*cycle))<1e-9
    assert abs(control.schedule(w,8)-26.080)<.001
    survivors=[]
    for kind in ('direct','scan','matrix'):
        for q in (1,2,4,5,8,10,16,20,40,80):
            if kind=='direct' and q!=80: continue
            for buffered in (False,True):
                for b in range(1,81):
                    t=schedule(seq,control.writer(kind,q,error=.35)['seconds'],b,buffered)
                    if t<30:
                        inv=control.inventory(kind,q,b,buffered)
                        survivors.append(dict(kind=kind,q=q,banks=b,buffered=buffered,
                            seconds=t,cost=control.bom(kind,q,b,buffered)['total'],
                            channels=inv['data_actuators'],bits=inv['retained_bits']))
    bests={k:min((s for s in survivors if s['kind']==k),key=lambda s:s['cost'])
           for k in ('direct','scan','matrix')}
    # Monotone signed groups also avoid returns, but retain six transfers.
    monotone = (-1,-1,-2,1,1,2)
    assert codes(monotone,6) is not None
    # Shared-drive architecture: copy E-230's explicit lean category allocation;
    # not a quotation, a force-rated drive, or a saving granted to baseline D.
    shared_bom = dict(controller=15,power=20,frame=25,wiring=15,freight_spares=10,
        common_lift_motor_driver=30,common_brake=10,common_phase_drive=10,
        common_feed_drive=10,common_writer_drives=20,common_shafts_bearings=30)
    shared_cases=[]
    for b in (4,5):
        inv=control.inventory('direct',80,b,False)
        items=dict(shared_bom,bank_readers=10*b,bank_enable=3*b,local_arrest=3*b,
                   bank_mounts_guides=4*b,data_channels=.5*80*b,media_hardware=.02*80*b)
        load=3.27; mass=.5*b+.003*80*b
        force=80*b*load*1.2+.5*b*9.81+mass*8
        torque=force*.01
        shared_cases.append(dict(banks=b,cost=sum(items.values()),items=items,
            seconds=schedule(seq,w,b),force_N=force,output_torque_Nm=torque,
            peak_input_W=force*.2/.7,
            d12_shaft_height_twist_mm=.01*torque*.4/(80e9*(math.pi*.012**4/32))*1000))
    sensitivity=[]
    for throw in (1,2,4):
        b=next(b for b in range(1,81) if schedule(seq,w,b,throw=throw)<30)
        sensitivity.append(dict(throw=throw,banks=b,seconds=schedule(seq,w,b,throw=throw),
                                cost=control.bom('direct',80,b,False)['total']))
    print(json.dumps(dict(search=counts,chosen=seq,
        codes=[dict(old=a,target=b,depth=c[0],travel=c[1],bits=c[2],heights=c[3])
               for (a,b),c in table.items()],
        checks=dict(maps=cases,support_observations=obs,partial_retries=retries,
                    injected_interlocks=5),best_by_writer=bests,
        fewest_channels=min(survivors,key=lambda s:(s['channels'],s['cost'])),
        contact_sensitivity=sensitivity, shared_drive_scenarios=shared_cases,
        six_pulse_monotone_B5=schedule(monotone,w,5),
        six_pulse_monotone_B6=schedule(monotone,w,6),
        four_bank_max_extra_write_per_pulse=(30-schedule(seq,0,4))/(21*5),
        direct_B4=schedule(seq,w,4),direct_B5=schedule(seq,w,5),
        regional_five_rows=schedule(seq,w,5,rows=5),
        free_writing_B4=schedule(seq,0,4),
        direct_B5_bom=control.bom('direct',80,5,False),
        direct_B5_inventory=control.inventory('direct',80,5,False)),indent=2))

if __name__=='__main__': main()
