"""E-229: causal writer/transfer screen, stdlib, stdout only.
All numerical non-product inputs are deliberately unqualified scenario bounds.
No prices, probability priors, force ratings, or physical acceptance implied.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e228', Path(__file__).resolve().parents[1]/'E-228'/'screen.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
move = base.move
P, WIDTH = 5.08, 80
STROKES = (10, 10, 20, 10, 10, 20)


def transfer(throw=2, proof=.003):
    # Arrested fingers in/prove; paired row+selected-column supports out;
    # after loaded stroke paired supports in/prove; fingers out/prove.
    return 4*(move(throw)+proof)


def writer(kind, lanes, error=0):
    """80 stationary retained bits/bank, no loaded bits overwritten.
    Direct: parallel endpoint command. Scan: common reset shoe, selective
    set cam, trailing optical read, retract/return/re-engage. Matrix: global
    reset, q data rails, m indexed group dogs; connect only with rails home,
    extend selected rails, retract, disconnect, index (cyclic return included).
    Each bit has two retained endpoints; a clamp-free endpoint detent is owed.
    """
    assert WIDTH % lanes == 0
    n = WIDTH//lanes
    if kind == 'direct':
        assert lanes == WIDTH
        return dict(seconds=move(2)+.003, channels=80, readers=80,
                    extra_dogs=0, writer_axes=0, span_mm=0, speed=0)
    if kind == 'matrix':
        t = 2*move(2)+n*(4*move(2)+.006+move(P))+.010
        return dict(seconds=t, channels=lanes, readers=lanes,
                    extra_dogs=80, writer_axes=2, span_mm=n*P, speed=0)
    assert kind == 'scan'
    width = 2.
    # Adverse differential position error at adjacent sites. Common x bias
    # affects absolute registration, not this gap; counted separately in text.
    gap = P-width-2*error
    assert gap > 0
    speed = .8*min(200, gap/(move(2)+.001),
                     width*math.sqrt(20000/(2*math.pi*2)))
    length = (n-1)*P+4+2*P  # reset, set, trailing read stations
    span = length+speed**2/8000
    t = length/speed+2*speed/8000+move(span)+2*move(2)+.010
    return dict(seconds=t, channels=lanes, readers=lanes,
                extra_dogs=0, writer_axes=2, span_mm=span, speed=speed)


def schedule(w, banks, buffered=False, throw=2, changed=None):
    """Two-buffer flow shop; buffers retain mask until entire pulse finishes.
    Writer may use freed buffer only after service i-2. Buffer switching owes
    a common 2-mm register-select stroke+proof, before each service. All writes
    begin after map receipt, including first. One whole worst row is replayed.
    A row retry must be detected at its final proof, assumed here. Hard faults
    safely stop and have no 30-s recovery claim. No unbounded retry loop.
    """
    visits = math.ceil(80/banks) if changed is None else changed
    services = [2*move(d)+transfer(throw)+(move(P) if k == 5 else 0)
                for _ in range(visits+1) for k,d in enumerate(STROKES)]
    if not buffered:
        return 2+sum(services)+len(services)*w
    # A separate physical writer selector reaches the inactive register. It
    # cannot be the service selector currently holding the active register.
    w += move(2)+.003
    ready, end = [], []
    for i,s in enumerate(services):
        begin = max(ready[-1] if ready else 0, end[i-2] if i >= 2 else 0)
        ready.append(begin+w)
        end.append(max(ready[-1],end[-1] if end else 0)+move(2)+.003+s)
    # Independent capacity lower bounds, including startup and selector time.
    assert end[-1] >= len(services)*w
    assert end[-1] >= w+sum(services)+len(services)*(move(2)+.003)-1e-9
    return 2+end[-1]


def inventory(kind, q, b, buffered):
    w=writer(kind,q)
    bits=80*b*(2 if buffered else 1)
    return dict(banks=b, data_actuators=b*w['channels'], retained_bits=bits,
        bit_endpoint_faces=2*bits, bar_axes=80*b, pickup_slides=80*b,
        routing_contacts=2*80*b, matrix_coupling_dogs=w['extra_dogs']*b*(2 if buffered else 1),
        writer_drive_axes=w['writer_axes']*b, register_select_axes=2*b if buffered else 0,
        reader_lanes=b*w['readers'], row_comb_axes=80,
        resident_support_sites=12800, column_shelves=44800, column_guides=12800)


def bom(kind,q,b,buffered,channel=.5,bit=.05):
    """Whole bought allocation; force/routing unqualified, NOT market prices.
    Explicit common/base ledger equals E-228's 130+65B before writer purchases.
    Readers are granted included in base $15/head even when 80 lanes are owed.
    """
    inv=inventory(kind,q,b,buffered)
    items=dict(controller=20,power=30,frame_mounts=35,wiring_distribution=25,
        freight_spares=20,row_transport=20*b,phase_dock_drive=5*b,
        output_reader=15*b,lift_motor_driver=12*b,source_loss_brake=8*b,
        shafts_bearings=5*b,data_channels=channel*inv['data_actuators'],
        retained_bit_hardware=bit*inv['retained_bits'],
        writer_drives=8*inv['writer_drive_axes'],
        buffer_select=8*inv['register_select_axes'])
    return dict(total=sum(items.values()),items=items)


def replay(old,target,fault=None):
    """Support truth table plus ideal mask reader interlocks; physical proof owed."""
    h=list(old); row=True; col=[True]*len(h); fingers=[False]*len(h)
    obs=0
    def check():
        nonlocal obs
        assert all(row or c or f for c,f in zip(col,fingers)), 'last path'
        assert all(a!=b or x==a for a,b,x in zip(old,target,h)), 'neighbor motion'
        obs+=1
    for sign in (1,-1):
        codes=[base.code(max(0,sign*(b-a)),(1,1,2)) for a,b in zip(h,target)]
        for k,d in enumerate((1,1,2)):
            assert row and all(col) and not any(fingers)
            mask=[bool(c[k]) for c in codes]  # physical overwrite while grounded
            actual=mask[:]
            if fault=='write': actual[0]=not actual[0]
            assert actual==mask, 'mask read'
            fingers[:]=actual; check()
            if fault=='pickup': fingers[:]=[False]*len(h)
            assert fingers==mask, 'pickup proof'
            row=False; col[:]=[not s for s in mask]; check()
            if fault=='brake':
                assert not any(fingers), 'source-loss brake required'
            if fault=='rewrite_active':
                fingers[:]=[False]*len(h); check()
            h[:]=[x+sign*d if s else x for x,s in zip(h,mask)]; check()
            row=True; col[:]=[True]*len(h); check()
            if fault=='reseat': row=False; col[:]=[False]*len(h)
            assert row and all(col), 'support proof'
            fingers[:]=[False]*len(h); check()
    assert h==list(target)
    return obs


def checks():
    cases=0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        replay(old,target); cases+=1
    for fault in ('write','pickup','brake','rewrite_active','reseat'):
        try: replay((0,4,2),(4,0,2),fault)
        except AssertionError: pass
        else: raise AssertionError('fault escaped: '+fault)
    # Four-site/two-rail matrix: reset, connect selected dogs with rails home,
    # push, retain before retract, disconnect. Previously written groups must
    # survive later data and address changes; rails are not independent memory.
    for initial,target in it.product(it.product((0,1),repeat=4),repeat=2):
        state=list(initial); state[:]=[0]*4
        rails=[0,0]
        for group in (0,1):
            assert rails==[0,0]
            dogs=[i//2==group for i in range(4)]
            before=state[:]
            rails[:]=target[2*group:2*group+2]
            for i,on in enumerate(dogs):
                if on: state[i]=rails[i%2]
            retained=state[:]
            rails[:]=[0,0]  # pushing-only dogs; retention bears return reaction
            assert state==retained
            assert all(on or state[i]==before[i] for i,on in enumerate(dogs))
            dogs[:]=[False]*4
        assert tuple(state)==target
    # Recover predecessor exactly without our physical overhead replacement.
    assert abs(base.board(1.1+6*.1+move(P),6)-28.256)<1e-9
    for w in (.01,.2,2):
        unbuffered=schedule(w,8)
        independent=2+11*(6*w+1.1+6*transfer()+move(P))
        assert abs(unbuffered-independent)<1e-9
        for b in (1,6,80):
            assert schedule(w,b,True)>2+6*(math.ceil(80/b)+1)*w
    return dict(three_cell_maps=cases, binary_overwrites=256, injected_faults=5)


def main():
    output=dict(checks=checks(),evidence='assumptions + calculations + ideal replay only',
        transfer_s=transfer(),six_bank_transfer_only_s=schedule(0,6),
        six_bank_max_total_pulse_s=((30-2)/15-1.1-move(P))/6)
    frontier=[]
    for kind in ('direct','scan','matrix'):
        for buffered in (False,True):
            candidates=[]
            for q in ((80,) if kind=='direct' else (1,2,4,5,8,10,16,20,40,80)):
                w=writer(kind,q)
                for b in range(1,81):
                    t=schedule(w['seconds'],b,buffered)
                    if t<30:
                        candidates.append(dict(kind=kind,buffered=buffered,lanes=q,
                            banks=b,time_s=t,write_s=w['seconds'],writer=w,
                            inventory=inventory(kind,q,b,buffered),
                            allocation=bom(kind,q,b,buffered)))
                        break
            # Keep distinct smallest actuator burden and lowest assumed cost.
            picks={}
            if candidates:
                for key in ('gates','cost'):
                    pick=min(candidates,key=lambda c: (c['inventory']['data_actuators'],c['allocation']['total'])
                             if key=='gates' else (c['allocation']['total'],c['inventory']['data_actuators']))
                    picks[key]=pick
            frontier.append(dict(kind=kind,buffered=buffered,best=picks))
    output['finite_grid']=frontier
    output['throw_sensitivity']={str(d):dict(transfer_s=transfer(d),
        six_bank_zero_writer_s=schedule(0,6,throw=d)) for d in (1,2,4)}
    output['scan_position_bound']={str(e):writer('scan',8,e) for e in (0,.15,.35,.70)}
    output['force_scenarios']={str(r):dict(bit_reset_80_N=80*r,
        per_scan_lane_peak_N=3*r) for r in (.3,1,3)}
    output['loaded_head_N']={str(f):80*f for f in (1,3.27,10)}
    output['conditional_undetected_union_bound']=38400*1e-6
    print(json.dumps(output,indent=2))


if __name__=='__main__': main()
