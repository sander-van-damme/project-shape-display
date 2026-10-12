"""E-224: necessary rail-writer/vertical-cassette bounds, not finite CAD.
All process/dynamic/economic inputs are labelled scenarios, not measurements.
Standard library; stdout only. Run from any directory. No stochastic priors.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'exchange218', Path(__file__).resolve().parents[1] / 'E-218' / 'exchange.py')
exchange = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exchange)
PITCH = 5.08
BANKS = (1, 2, 4, 8, 16)
STREAMS = (1, 2, 4, 8, 16, 40, 80)


def limits(error=.35, run=2, footprint=2, a=8000, follower_a=100000,
           slope=4, n=10, x_error=None):
    """mm, s. Per-face error +/-e: opposing vertical and x errors add 2e.
    A removable rising tongue lifts follower clear of a 1.6-mm fixed rail;
    follower vertical thickness 1.6 mm. Finite x footprint occupies the tongue
    from its leading edge's arrival until its trailing edge's departure.
    Cycloidal rise has peak slope 2d/L, acceleration 2*pi*d*(v/L)^2.
    Only isolated one-follower streams avoid adjacent arbitrary-bit switching.
    """
    rise = 3.2 + 2*error
    xe = error if x_error is None else x_error
    gap = PITCH - run - footprint - 2*xe
    if 2*rise/run > slope or (n > 1 and gap <= 0):
        return None
    remaining = 10-rise
    tail = 2*remaining/slope
    assert remaining > 0 and tail > 0
    coefficient = max(2*math.pi*rise/run**2, 2*math.pi*remaining/tail**2)
    cam_v = math.sqrt(follower_a/coefficient)
    switch_s = exchange.move(rise, a) + .001
    gate_v = gap/switch_s if n > 1 else math.inf
    v = .8*min(200, cam_v, gate_v)
    length = 4*(run+tail)+(n-1)*PITCH+footprint+2*xe
    return dict(rise=rise, gap=gap, run=run, tail=tail, speed=v,
                scan_length=length, switch_s=switch_s,
                peak_slope=max(2*rise/run, slope))


def row_time(b, s, *, error=.35, footprint=2, a=8000, slope=4,
             follower_a=100000, arrest='continuous', aux=.5, travel=45, x_error=None):
    """Optimistic split-row streams, own writer/head per bank, all serial.
    No free offline writing: unlock unloaded spare, common 40-mm reset plus
    return; set gates; scan; common keeper/read; empty feed return; exchange.
    Feed return traverses the same granted split-stream length.
    Split-stream physical fanout and rail extraction are NOT constructed.
    travel=45 is E-218's favorable borrowed lift allowance, not proved here.
    """
    assert 80 % s == 0
    n = 80//s
    options=[]
    for run in (2.,3.,4.):
        lim=limits(error,run,footprint,a,follower_a,slope,n,x_error)
        if lim is None: continue
        writing=2*exchange.move(40,a) + lim['switch_s']
        writing+=exchange.move(lim['scan_length'],a,lim['speed'])
        writing+=exchange.move(lim['scan_length'],a)
        if arrest == 'continuous':
            lift=4*exchange.move(travel,a)
        else:
            lift=2*travel*(exchange.move(1,a)+.001)+2*exchange.move(travel,a)
        total=writing+lift+2*exchange.move(2.4,a)+exchange.move(PITCH,a)+aux
        options.append(dict(seconds=total, **lim))
    return min(options,key=lambda x:x['seconds']) if options else None


def screen(**kw):
    feasible=[]
    for b,s in itertools.product(BANKS,STREAMS):
        row=row_time(b,s,**kw)
        if row is None: continue
        total=2+(math.ceil(80/b)+1)*row['seconds']
        if total < 30:
            feasible.append(dict(banks=b,streams_per_head=s,gates=4*b*s,
                                 seconds=total, **{k:v for k,v in row.items()
                                                     if k!='seconds'}))
    return sorted(feasible,key=lambda r:(r['gates'],r['seconds']))


def routes(targets):
    """Each gate passes remaining upward codes; completed codes travel below
    later stages. Four branch rails supply 0/10/20/30/40 positions. This checks
    command semantics only, not finite bypass clearance or rail extraction.
    """
    h=[0]*len(targets)
    for k in range(1,5):
        for i,t in enumerate(targets):
            if t >= k: h[i]+=10
    return h


def interval_conflict(run, footprint, error):
    # First needs ON, next OFF; positional errors make minimum headway p-2e.
    first=(0,run+footprint)
    second=(PITCH-2*error, PITCH-2*error+run+footprint)
    return max(first[0],second[0]) < min(first[1],second[1])


def authorize_target(actual, requested, *, keeper=True, rail_clear=True, arrest=True):
    # Proof obligations only: no claim that sensors or mechanisms are constructed.
    assert actual == requested and keeper and rail_clear and arrest


def checks():
    codes=list(itertools.product(range(5),repeat=3))
    transitions=0
    for old,new in itertools.product(codes,repeat=2):
        # Common unloaded reset must discard the complete old spare code.
        rewritten=routes(new)
        assert rewritten == [10*n for n in new]
        exchange.replay(tuple(10*x for x in old),tuple(rewritten))
        transitions+=1
    requested=[0,40,20]
    authorize_target(routes([0,4,2]), requested)
    faults=[([0,30,20],{}), (requested,{'keeper':False}),
            (requested,{'rail_clear':False}), (requested,{'arrest':False})]
    for actual,kw in faults:
        try: authorize_target(actual,requested,**kw)
        except AssertionError: pass
        else: raise AssertionError('unproved target released old support')
    # A common comb at z=-8 meets one of five notches in every code. Two
    # guide stations at -16 and 0 remain covered by all 64-mm bars.
    for h in (0,10,20,30,40):
        assert (4+h)-(12+h) == -8
        assert 4+h-64 <= -16 < 0 <= 4+h
    # Rerun predecessor's exact event checks (same author; no independence claim).
    assert exchange.checks()==15625
    # Opposing adjacent commands cannot occupy the same rigid gate concurrently.
    assert interval_conflict(2,2,.70)
    assert not interval_conflict(2,2,.35)
    assert math.isclose(5.08-2-2-2*.35,.38)
    # Point follower is an optimistic relaxation; adding footprint never speeds
    # adjacent-stream service at fixed geometry/error.
    for e,run in itertools.product((0,.15,.35,.7),(2,3,4)):
        point=limits(e,run,0,slope=8)
        finite=limits(e,run,2,slope=8)
        if finite:
            assert point and point['speed'] >= finite['speed']
    # Independent slope and acceleration limits from analytic cycloid derivative;
    # finite differences converge as resolution increases.
    d,L,v=3.9,2.,10.
    expected=2*math.pi*d*(v/L)**2
    errors=[]
    for steps in (64,256,1024):
        dt=L/v/steps
        z=[d*(i/steps-math.sin(2*math.pi*i/steps)/(2*math.pi))
           for i in range(steps+1)]
        measured=max(abs(z[i+1]-2*z[i]+z[i-1])/dt**2
                     for i in range(1,steps))
        errors.append(abs(measured/expected-1))
    assert errors[2] < errors[1] < errors[0] < .001
    # Bar stock and envelope independent calculations: top 4+h, length64.
    assert min(4+h-64 for h in (0,10,20,30,40)) == -60
    assert max(4+h for h in (0,10,20,30,40)) == 44
    assert math.isclose(64*3.4*1.6*7680/1e6,2.6738688)
    return dict(old_target_triples=transitions,gate_overlap_counterexample=True,blocked_proof_faults=len(faults),
                cycloid_relative_errors=errors)


def main():
    validation=checks()
    cases=[]
    for error,fp,slope,arrest in itertools.product(
            (0,.15,.35,.70),(0,2),(4,8),('continuous','indexed')):
        rows=screen(error=error,footprint=fp,slope=slope,arrest=arrest)
        cases.append(dict(error=error,footprint=fp,slope=slope,arrest=arrest,
                          best=rows[0] if rows else None))
    coherent=screen(error=.35,x_error=0,footprint=2,slope=8)
    sensitivity=[]
    for e in (0,.15,.35,.70):
        lim=limits(error=e,run=2,footprint=2,slope=8)
        sensitivity.append(dict(error=e,limits=lim))
    mid=limits(error=.35,run=2,footprint=2,slope=8)
    rate_streams=math.floor(6400*PITCH/(28*mid['speed']))+1
    print(json.dumps(dict(rate_only_stream_floor=rate_streams,
                         rate_only_gate_floor=4*rate_streams,
                         evidence='necessary calculations / assumed bounds only',
                         checks=validation,grid=cases,gate_sensitivity=sensitivity,
                         coherent_x_best=coherent[0] if coherent else None),indent=2))

if __name__=='__main__': main()
