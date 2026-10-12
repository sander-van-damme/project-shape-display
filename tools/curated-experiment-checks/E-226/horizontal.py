"""E-226: horizontal unloaded state writing; bounded geometry/schedules only.
Stdlib, stdout only. No calibrated FDM, contact, sensor or hardware claims.
"""
import itertools
import json
import math

PITCH = 5.08
LEVELS = (0, 10, 20, 30, 40)
BANKS = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)
RADIUS = math.hypot(52, .8) + 4  # bar union about comb plus frame allocation
BAY = 2 * RADIUS
DEPTH_STEP = BAY + 4
TRAVEL = math.ceil(RADIUS + 56)  # pivot=-8; other bars reach -60; clearance=4


def move(d, v=200, a=8000):
    assert d >= 0 and v > 0 and a > 0
    return 2 * math.sqrt(d/a) if d <= v*v/a else d/v + v/a


def write(target):
    """Horizontal stationary tray. Reset, common sweep, stopped release.
    A granted passive drag window holds released unloaded bars. Closing the
    common positive comb BEFORE any tray motion is mandatory.
    """
    offsets = [0] * len(target)
    active = [True] * len(target)
    for k in LEVELS:
        for i, h in enumerate(target):
            if active[i]: offsets[i] = k
            if h == k: active[i] = False
            assert offsets[i] <= h
    assert not any(active) and offsets == list(target)
    return offsets


def turnover_allowed(height_read=True, comb_read=True, writer_clear=True):
    return height_read and comb_read and writer_clear


def row(travel=TRAVEL, aux=.5, rotation=.375, indexed=False):
    # Reset and platen return; four stopped sweep increments; empty sweep
    # return; one pusher preset and five stopped release commands/proofs.
    writing = 3*move(40) + 4*move(10) + 6*(move(3)+.002)
    # Distinguish loaded 40-mm support moves from empty clearance travel.
    # Splitting at 40 conservatively charges a stop at load-free crossover.
    if indexed:
        exchange = 2*40*(move(1)+.001) + 2*move(travel-40) + 2*move(travel)
    else:
        exchange = 2*(move(40)+move(travel-40)) + 2*move(travel)
    transport = 2*move(2.4)+move(PITCH)
    return dict(writing=writing, exchange=exchange, rotation=2*rotation,
                transport=transport, auxiliary=aux,
                seconds=writing+exchange+2*rotation+transport+aux)


def schedule(banks, stacked=False, **kw):
    assert 80 % banks == 0
    rows = 80//banks
    # Fixed bays equally spaced at bank centers. Exact arbitrary-code bar
    # collision at horizontal pose rules out widths <104 mm. BAY adds frame.
    decks = min(banks, math.ceil(BAY/(rows*PITCH))) if stacked else 1
    travel = TRAVEL + (decks-1)*DEPTH_STEP
    r = row(travel=travel, **kw)
    return dict(banks=banks, selectors=80*banks, decks=decks,
                travel_mm=travel, seconds=2+(rows+1)*r['seconds'], row=r)


def interval(h, pivot=0):
    # Horizontal bar section: original z [-60+h,4+h], relative to comb -8.
    return pivot+h-52, pivot+h+12


def overlap(a, b):
    return min(a[1], b[1]) > max(a[0], b[0])


def drag_window(mass=.001, tilt_deg=2, disturbance=.005,
                mu_min=.1, mu_max=.4, normal_nominal=.1, spread=.5):
    """Explicit competing bounds, not a probability or material prior.
    Shared-pad force spread means each bar gets N in N0*(1+/-spread).
    Tray is stationary while unlocked; disturbance bounds coupled vibration.
    """
    needed = mass*9.81*abs(math.sin(math.radians(tilt_deg)))+disturbance
    holding = mu_min*normal_nominal*(1-spread)
    push = mu_max*normal_nominal*(1+spread)+mass*8
    return dict(needed_N=needed, holding_N=holding, margin_N=holding-needed,
                push_N_per_bar=push, push_N_row=80*push)


def checks():
    n=0
    for old, target in itertools.product(itertools.product(LEVELS,repeat=3),repeat=2):
        # Erase on horizontal table, so output independent of spare's old state.
        assert write(target)==list(target)
        for o,t in zip(old,target):
            # Ideal two-cassette support: new rise then old fall; untouched
            # height unchanged, changed height monotone across piecewise events.
            path=[max(o,t-40+x) for x in range(41)]
            path += [max(o-x,t) for x in range(1,41)]
            assert path[0]==o and path[-1]==t
            assert all(min(o,t)<=h<=max(o,t) for h in path)
            if o==t: assert all(h==o for h in path)
        n+=1
    for flags in itertools.product((False,True),repeat=3):
        assert turnover_allowed(*flags) == all(flags)
    # Independent angular corner sampling against analytical radius envelope.
    peak=0
    for h,u,theta in itertools.product(LEVELS,(-.8,.8),range(901)):
        angle=math.radians(theta/10)
        for v in (h-52,h+12):
            y=u*math.cos(angle)+v*math.sin(angle)
            z=-u*math.sin(angle)+v*math.cos(angle)
            peak=max(peak,abs(y),abs(z))
            assert abs(y)<=RADIUS-4+1e-10 and abs(z)<=RADIUS-4+1e-10
    assert peak > 52
    assert -8-TRAVEL+RADIUS < -64
    assert -8-45+RADIUS > -60  # borrowed 45-mm clearance is not usable
    # Adjacent unequal codes witness collision; at 104 mm interiors separate.
    assert overlap(interval(40), interval(0,100))
    assert not any(overlap(interval(a),interval(b,104)) for a,b in itertools.product(LEVELS,repeat=2))
    for b in BANKS:
        s=schedule(b,stacked=True)
        centers=[((i+.5)*(80//b)*PITCH, -(i%s['decks'])*DEPTH_STEP) for i in range(b)]
        for (y1,z1),(y2,z2) in itertools.combinations(centers,2):
            assert abs(y1-y2)>=BAY or abs(z1-z2)>=BAY
    assert math.isclose(move(5),.05)
    assert math.isclose(move(40),.225)
    assert math.isclose(move(math.pi/2,2*math.pi,16*math.pi),.375)
    service=row()['writing']
    assert math.ceil(81*service/28)==4
    assert math.ceil(81*(service+.75)/28)==6
    assert row(indexed=True)['seconds'] > row()['seconds']
    assert row(travel=200)['seconds'] > row()['seconds']
    return dict(replays=n, proof_combinations=8, angular_peak_mm=peak,
                geometry='bar corners and bank envelope allocations checked')


if __name__=='__main__':
    out=dict(checks=checks(),geometry=dict(radius=RADIUS,bay=BAY,travel=TRAVEL,deck_step=DEPTH_STEP))
    out['grant_free_routing']=[schedule(b) for b in BANKS]
    out['stacked_bays']=[schedule(b,stacked=True) for b in BANKS]
    out['sensitivity']={}
    for key,kw in [('slow_rotation',dict(rotation=.75)),('indexed',dict(indexed=True)),('aux1',dict(aux=1))]:
        candidates=[schedule(b,**kw) for b in BANKS]
        out['sensitivity'][key]=next((c for c in candidates if c['seconds']<30),None)
    out['drag']=[dict(normal_N=n,disturbance_N=d,**drag_window(normal_nominal=n,disturbance=d))
                 for n,d in itertools.product((.1,.3,1),(.005,.05,.1))]
    print(json.dumps(out,indent=2))
