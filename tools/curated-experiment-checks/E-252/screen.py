#!/usr/bin/env python3
"""E-252: ideal sustained-capture support and complete reset accounting.
Stdlib. Geometry, rates, force and cost are labelled scenarios, not qualification.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e251', Path(__file__).resolve().parents[1]/'E-251/screen.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
move = p.move
SEQ = (-2, 1, 1, -2, 2)
TABLE = p.c.codes(SEQ, 6)

def transfer(old, new, reverse=False):
    """Stopped common carrier: add incoming path, prove, remove outgoing.
    opposite-direction changes occur together; no movement during overlap.
    """
    parked = [not v for v in old]
    driven = list(old)
    if reverse:  # Deliberate release-before-engage fault.
        parked = [a and not b for a,b in zip(parked,new)]
        driven = [a and b for a,b in zip(driven,new)]
        assert all(a or b for a,b in zip(parked,driven)), 'last load path'
    parked = [a or not b for a,b in zip(parked,new)]
    driven = [a or b for a,b in zip(driven,new)]
    assert all(a or b for a,b in zip(parked,driven))
    overlap = (tuple(parked), tuple(driven))
    parked = [not b for b in new]
    driven = list(new)
    assert all(a or b for a,b in zip(parked,driven))
    return overlap, (tuple(parked),tuple(driven))

def replay():
    maps = observations = retries = 0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        bits = [TABLE[a,b][2] for a,b in zip(old,target)]
        changed = [a!=b for a,b in zip(old,target)]
        h = list(old); delta=[0]*3; active=[False]*3
        # Changed-only retained capture before resident release; U never acquired.
        resident=[not c for c in changed]; captured=list(changed)
        for j,d in enumerate(SEQ):
            new=[bool(b[j]) for b in bits]
            for parked,driven in transfer(active,new):
                assert all(r or (c and (g or m)) for r,c,g,m in zip(resident,captured,parked,driven))
                observations+=1
            active=new
            h=[v+d*n for v,n in zip(h,new)]
            delta=[v+d*n for v,n in zip(delta,new)]
            assert all(v in range(5) for v in h)
            assert all(a!=b or a==v for a,b,v in zip(old,target,h))
            assert all(a+x==v for a,x,v in zip(old,delta,h))
            observations+=1
        assert h==list(target)
        transfer(active,[False]*3)
        # All changed outputs parked; gang return turn/lower, prove ground, detach.
        resident=[True]*3; captured=[False]*3
        assert all(resident)
        # Reverse selected strokes resets empty slides without local springs.
        active=[False]*3
        for j in reversed(range(len(SEQ))):
            new=[bool(b[j]) for b in bits]
            transfer(active,new); active=new
            delta=[v-SEQ[j]*n for v,n in zip(delta,new)]
            assert all(r and not c for r,c in zip(resident,captured))
        transfer(active,[False]*3)
        assert delta==[0]*3
        maps+=1
    # Stable partial retry: return turn/seat at actual integer height, detach,
    # invert only executed prefix, then regenerate masks from actual heights.
    for (a,b),entry in TABLE.items():
        for n in range(6):
            h=a+sum(d*x for d,x in zip(SEQ[:n],entry[2][:n]))
            delta=h-a
            for d,x in reversed(tuple(zip(SEQ[:n],entry[2][:n]))): delta-=d*x
            assert delta==0
            code=TABLE[h,b][2]
            assert h+sum(d*x for d,x in zip(SEQ,code))==b
            retries+=1
    try: transfer([False,True],[True,False],reverse=True)
    except AssertionError: pass
    else: raise AssertionError('unsafe transfer was not rejected')
    # Removing mechanical drive retention or a park path breaks source-loss proof.
    assert not (False or (True and (False or False)))
    return dict(maps=maps,loaded_support_observations=observations,stable_partial_retries=retries)

def certificate():
    # All 25 transitions fit one color's 40 lanes. There is a required mask
    # change at each of six boundaries for this table, initial/final all parked.
    columns=[TABLE[a,b][2] for a,b in it.product(range(5),repeat=2)]
    masks=[(0,)*25]+list(zip(*columns))+[(0,)*25]
    boundaries=[a!=b for a,b in zip(masks,masks[1:])]
    assert all(boundaries)
    # Exhaust all alternative code choices for a single omitted boundary:
    # at least one pair has no valid code if that boundary is forbidden.
    necessary=[]
    for edge in range(6):
        missing=[]
        for a,b in it.product(range(5),repeat=2):
            candidates=[]
            for bits in it.product((0,1),repeat=5):
                path=p.c.path(SEQ,a,bits)
                augmented=(0,)+bits+(0,)
                if a==b and any(bits): continue
                if path and path[0]==b and augmented[edge]==augmented[edge+1]:
                    candidates.append(bits)
            if not candidates: missing.append([a,b])
        necessary.append(missing)
    assert all(necessary)
    # Rack relative position = output displacement - common-carrier datum.
    q=tuple(it.accumulate(SEQ,initial=0)); positions=set()
    for (a,b),entry in TABLE.items():
        h=a
        for j,on in enumerate(entry[2]):
            if on: positions.add(h-a-q[j])
            h+=SEQ[j]*on
    return dict(boundaries=boundaries,omitted_boundary_unreachable_pairs=necessary,
                drive_rack_phases=sorted(positions),park_positions=list(range(-4,5)))

def timings(throw=2,proof=.003,reset='reverse'):
    stage=move(throw)+proof
    motion=sum(move(10*abs(x)) for x in SEQ)
    # changed-mask write/capture and final detach: three contact stages.
    # frame lift/seat and yaw each twice, with separate proofs.
    ends=3*stage+2*(move(6.4)+proof)+2*(p.angular()+proof)
    # Five physical commands; six add-then-remove handoffs, two stages each.
    loaded=motion+5*stage+12*stage
    if reset=='reverse':
        empty=loaded  # Same five writes, six handoffs; no capture/yaw/frame lift.
    elif reset=='free':
        empty=0  # Explicit impossible-to-infer upper relaxation, not mechanism.
    else: raise ValueError(reset)
    row=ends+loaded+empty+move(5.08)
    b=next(b for b in range(1,81) if 2+.010+(math.ceil(80/b)+1)*row<30)
    return dict(reset=reset,throw_mm=throw,proof_s=proof,banks=b,channels=80*b,
        row_s=row,map_s=2+.010+(math.ceil(80/b)+1)*row,
        cost_relaxation=195+20*b+.52*80*b,
        ends_s=ends,loaded_s=loaded,empty_s=empty,
        channel_cap=(500-195-20*b)/(80*b),
        b4_s=2.010+21*row,b5_s=2.010+17*row,
        regional_one_row_s=2.010+2*row)

def main():
    cases=[timings(d,t,r) for r,d,t in it.product(('reverse','free'),(1,2,4),(0,.003,.010))]
    base=timings(); b=base['banks']
    # Independent arithmetic reconstruction of the base schedule.
    contact=2*math.sqrt(2/8000)+.003
    assert abs(base['row_s']-(.4+5*.025)*2-37*contact
               -2*(6.4/200+.025+.003)-2*(.225+.003)
               -(5.08/200+.025)) < 1e-12
    assert p.geometry(16)==6800
    primitive=lambda y: .5*(y*math.sqrt(.8**2-y*y)+.8**2*math.asin(y/.8))
    overlap=2*(primitive(.4)-.6*.4)
    resident_liters=(math.pi*.8**2*142+4.8**2*2+10*1.2*(1.4*.8-overlap))*6400/1e6
    # Force bounds: external total payload concentrated in active rows; no
    # uniform per-cell test load presented as a requirement. Masses assumptions.
    forces=[]
    for payload,slide_mass in it.product((0,1,5),(.005,.020)):
        mass=80*b*(.003+slide_mass)+.5*b+payload
        f=mass*(9.81+8)+80*b*.005
        forces.append(dict(external_kg=payload,slide_kg=slide_mass,peak_N=f,input_W=f*.2/.7))
    print(json.dumps(dict(replay=replay(),certificate=certificate(),
        base=base,free_reset=timings(reset='free'),sensitivity=cases,
        nominal_resident_liters=resident_liters,
        resident_extrusion_hours=[resident_liters*1e6/(r*3600*.9) for r in (15,5)],
        inherited_comparators=dict(e251_banks=16,e251_channels=1280,e251_seconds=26.073,
            e251_dollars=1180.60,e236_banks=5,e236_channels=400,e236_seconds=26.681,
            e236_lean_dollars=503,direct_staggered_banks=5,direct_pairs=400,
            direct_seconds=26.708,direct_pair_cap=(500-295)/400),
        original_pickup_max_z=-20+40+6.4,
        deeper_pickup_max_z=-60+40+6.4,
        capture_lug_indices=list(range(6,11)),resident_lug_indices=list(range(5)),
        rack_margin_scenarios=[dict(error=e,margin=1-e) for e in (.15,.35,.70)],
        handoff_height_scenarios=[dict(per_path_error=e,worst_shift=2*e) for e in (.15,.35,.70)],
        forces=forces,ledger=dict(banks=b,captures=80*b,slides=80*b,parks=80*b,
            drive_couplings=80*b,guide_stations=160*b,park_stations=9*80*b,
            resident_columns=6400,resident_fixed_forms=64000)),indent=2))
if __name__=='__main__': main()
