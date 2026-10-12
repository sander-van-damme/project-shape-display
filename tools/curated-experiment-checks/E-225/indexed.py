"""E-225: synchronized indexed rail feed, necessary bounds, no physical claims.
Standard library. Bounded errors and kinematics are assumed scenarios.
Run from any directory; stdout only. No generated evidence files required.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'rails224', Path(__file__).resolve().parents[1] / 'E-224' / 'rails.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
move = prior.exchange.move
P = 5.08
W = 2.0


def parking(footprint=2., error=.35, phase=.1):
    # Local bar errors +/-error; common feed/rail phase error +/-phase.
    # Unlike relative headway, common phase bias DOES NOT cancel at a stop.
    return (P-W-footprint)/2-error-phase


def geometry(error=.35, slope=4):
    rise = 3.2+2*error
    tail = 2*(10-rise)/slope
    if 2*rise/W > slope:
        return None
    spacing = math.ceil((W+tail+2+2*error)/P)*P
    return dict(rise=rise, tail=tail, station_pitch=spacing,
                stages_in_pitches=round(4*spacing/P))


def step_seconds(error=.35, slope=4, feed_a=8000., vertical_a=100000.):
    """Conservative global derivative bound, smooth quintic feed each pitch.
    x=P*(10u^3-15u^4+6u^5), u=t/T.
    |x'|<=1.875P/T; |x''|<=10sqrt(3)P/(3T^2).
    z''=cam''*x'^2+cam'*x''. Include BOTH terms.
    20% timing allowance; not gravity-following or force qualification.
    """
    g=geometry(error,slope)
    if g is None: return None
    sx=max(2*g['rise']/W, slope)
    cx=max(2*math.pi*g['rise']/W**2,
           2*math.pi*(10-g['rise'])/g['tail']**2)
    vx=1.875*P
    ax=10*math.sqrt(3)*P/3
    T=max(vx/200, math.sqrt(ax/feed_a),
          math.sqrt((cx*vx**2+sx*ax)/vertical_a))/.8
    return T


def row(s, error=.35, phase=.1, footprint=2., slope=4, aux=.5,
        travel=65., arrest='continuous', vertical_a=100000., clear=4.):
    assert 80 % s == 0
    if parking(footprint,error,phase) <= 0: return None
    g=geometry(error,slope)
    if g is None: return None
    step=step_seconds(error,slope,vertical_a=vertical_a)
    # One input index per bar, then flush full four-station pipeline to flat
    # output rails. Phase-aligned stations at multiples of P; no offline write.
    ticks=80//s+g['stages_in_pitches']
    switch=move(g['rise'],8000)+.001
    scan=ticks*P
    writing=2*move(40,8000)+ticks*(step+switch)
    # Common comb closes before rail bank retracts SIDEWAYS. Return unloaded
    # feed only when rails are clear. Reinsert rails after next spare arrives.
    writing+=2*move(clear,8000)+move(scan,8000)
    if arrest=='continuous': lift=4*move(travel,8000)
    else: lift=2*travel*(move(1,8000)+.001)+2*move(travel,8000)
    total=writing+lift+2*move(2.4,8000)+move(P,8000)+aux
    return dict(seconds=total,ticks=ticks,scan_mm=scan,step_s=step,
                switch_s=switch,parking_margin=parking(footprint,error,phase),
                rail_overrun_mm=g['stages_in_pitches']*P)


def screen(**kw):
    out=[]
    for b,s in itertools.product((1,2,4,8,16),(1,2,4,8,16,40,80)):
        r=row(s,**kw)
        if r is None: continue
        seconds=2+(math.ceil(80/b)+1)*r['seconds']
        if seconds < 30:
            out.append(dict(banks=b,streams=s,gates=4*b*s,seconds=seconds,
                            row={k:v for k,v in r.items()}))
    return sorted(out,key=lambda x:(x['gates'],x['seconds']))


def replay(target, spacing=2):
    """Pipeline command causality; each bar reaches all four stages, one code
    at a time per station. Lower completed codes bypass higher stations.
    This proves bit routing only, not finite bypass geometry or sensing.
    """
    h=[0]*len(target)
    for tick in range(len(target)+3*spacing):
        at=[]
        for station in range(4):
            i=tick-station*spacing
            if 0 <= i < len(target):
                at.append(i)
                if target[i] > station:
                    assert h[i] == station*10
                    h[i]+=10
        assert len(at)==len(set(at))
    assert h == [10*x for x in target]
    return h


def checks():
    count=0
    for target in itertools.product(range(5),repeat=5):
        replay(target);count+=1
    # Independent finite-interval geometry: any two consecutive followers,
    # opposite/local errors and coherent phase errors at their four corners.
    half=(W+P)/2  # parked follower center; gate interval [0,W]
    for f,e,c in itertools.product((2.,3.4),(0.,.15,.35,.7),(0.,.1,.2)):
        expected=parking(f,e,c)>0
        actual=True
        for a,b,bias in itertools.product((-e,e),(-e,e),(-c,c)):
            ahead_left=half+a+bias-f/2
            behind_right=half-P+b+bias+f/2
            actual &= ahead_left>W and behind_right<0
        assert actual==expected
    # Plain bar bottom on stacked rails: every higher rail intersects its
    # 64-mm shaft. Side-projecting follower routing is a changed interface.
    collisions=sum(min(h+64,k)>max(h,k-1.6)
                   for h,k in itertools.product((0,10,20,30,40),repeat=2))
    assert collisions == 10
    assert parking(3.4,0,0)<0
    assert math.isclose(parking(2,.35,.1),.09)
    assert parking(2,.35,.2)<0
    # Full cell support replay independently inherited, not an independent review.
    for old,new in itertools.product(itertools.product((0,20,40),repeat=3),repeat=2):
        prior.exchange.replay(old,new)
    # Smooth feed finite differences converge to analytic x acceleration.
    # The cam composition bound is analytical, not a contact-dynamics check.
    errors=[]
    for n in (128,512,2048):
        values=[P*(10*(i/n)**3-15*(i/n)**4+6*(i/n)**5) for i in range(n+1)]
        fd=max(abs(values[i+1]-2*values[i]+values[i-1])*n*n for i in range(1,n))
        errors.append(abs(fd/(10*math.sqrt(3)*P/3)-1))
    assert errors[2]<errors[1]<errors[0]<.001
    # Counts & limiting cases. A single stream retains all 80 bar settings;
    # more independent streams shorten scan but are NOT freely spatially packed.
    assert row(1)['ticks']==88
    assert row(8)['ticks']==18
    assert row(1)['seconds']>row(8)['seconds']
    assert screen(footprint=3.4,error=0,phase=0)==[]
    return dict(pipeline_maps=count,old_new_triples=729,
                finite_interval_boxes=24,plain_bottom_upper_rail_collisions=collisions,
                quintic_acceleration_errors=errors)


def main():
    results=[]
    for e,phase,foot,travel,arrest in itertools.product(
        (0.,.15,.35,.7),(.1,),(2.,3.4),(45.,65.),('continuous','indexed')):
        found=screen(error=e,phase=phase,footprint=foot,travel=travel,arrest=arrest)
        results.append(dict(error=e,phase=phase,footprint=foot,travel=travel,
                            arrest=arrest,best=found[0] if found else None))
    print(json.dumps(dict(evidence='assumed-bound calculations; no hardware qualification',
        checks=checks(),grid=results,
        single_stream_s=2+6*row(1)['seconds'],
        favorable_45mm_sensitivity=[dict(aux=a,seconds=2+6*row(16,travel=45,aux=a)['seconds']) for a in (.25,.5,1.)],
        gravity_schedule_s=2+6*row(80,vertical_a=9810)['seconds'],
        sensitivities=[dict(aux=a,vertical_a=v,best=(screen(aux=a,vertical_a=v) or [None])[0])
            for a,v in itertools.product((.25,.5,1.),(9810.,20000.,100000.))]),indent=2))

if __name__=='__main__': main()
