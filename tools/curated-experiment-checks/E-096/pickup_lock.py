"""Finite rigid two-aperture pickup lock, mm. Deterministic error boxes.
Self-review, geometry only; no force, friction, process probability or hardware pass.
The lock is positively held vertically by a GRANTED boundary condition. A real
pin retainer/writer remains missing. Rejecting even this grant is informative.
"""
import itertools as it
import json
import math


def overlap(a, b):
    return max(0., min(a[1], b[1])-max(a[0], b[0]))


def volume(a, b):
    return math.prod(overlap(a[i:i+2], b[i:i+2]) for i in (0, 2, 4))


def translate(box, x=0., z=0.):
    return (box[0]+x, box[1]+x, *box[2:4], box[4]+z, box[5]+z)


def tail(width, errors=(0., 0., 0., 0.)):
    """Actual nonoverlapping boxes around two rectangular through apertures.
    Rear tail is in a separate y lane from the pickup lip and deck finger.
    """
    a, b = .5-width/2+errors[0], .5+width/2+errors[1]
    c, d = 1.9-width/2+errors[2], 1.9+width/2+errors[3]
    if not -.5 < a < b < c < d < 2.9:
        return None
    return [(-.5, 2.9, 1.2, 1.6, 1., 1.9),
            (-.5, 2.9, 2.4, 2.8, 1., 1.9),
            (-.5, a, 1.6, 2.4, 1., 1.9),
            (b, c, 1.6, 2.4, 1., 1.9),
            (d, 2.9, 1.6, 2.4, 1., 1.9)]


def bolt(width, x=1.9, z=0.):
    return (x-width/2, x+width/2, 1.7, 2.3, .7+z, 2.2+z)


def nominal_route(subdivisions):
    """Nominal unlock->translate->relock and reverse, finite guide rails/stops.
    Translations are prescribed, not a synthesized common writer. Rails bound
    translation but do not establish angular stability or a full column guide.
    """
    rails = [(a, b, y0, y1, z0, z1)
             for a, b in [(-.5, 2.9)]
             for y0, y1 in [(1.2, 1.6), (2.4, 2.8)]
             for z0, z1 in [(.2, .6), (2.3, 2.7)]]
    # End stops touch the tail at q=0 and 1.4, separate rear lane from deck.
    stops = [(-.9, -.5, 2.4, 2.8, .6, 2.3),
             (4.3, 4.7, 2.4, 2.8, .6, 2.3)]
    pieces = tail(1.)
    # Root, neck and lip are one body, no arbitrary overlapping housing grant.
    pieces += [(0., 2.4, 0., .8, 1., 1.9),
               (0., 2.4, .8, 1.2, 1., 1.9)]
    states = 0
    for start, end in [(0., 1.4), (1.4, 0.)]:
        route = [(start, 1.7*k/subdivisions) for k in range(subdivisions+1)]
        route += [(start+(end-start)*k/subdivisions, 1.7) for k in range(subdivisions+1)]
        route += [(end, 1.7*(1-k/subdivisions)) for k in range(subdivisions+1)]
        for q, unlock in route:
            moving = [translate(b, x=q) for b in pieces]
            p = bolt(.4, z=unlock)
            assert all(volume(b, p)<1e-12 for b in moving)
            assert all(volume(b, fixed)<1e-12 for b in moving for fixed in rails+stops)
            assert all(volume(p, fixed)<1e-12 for fixed in rails+stops)
            # Deck stays home while setting/clearing; at other heights front
            # rails terminate at x=2.9 and rear stops are outside its y lane.
            deck = (3.1, 4.3, 0., .8, -2.9, -2.)
            assert all(volume(deck, b)<1e-12 for b in moving+rails+stops+[p])
            states += 1
    # With pin left inserted, attempted reset penetrates the finite central web.
    collision = sum(volume(translate(b, x=.7), bolt(.4)) for b in tail(1.))
    assert collision > 0
    return dict(states=states,locked_midstroke_collision_mm3=collision)


def screen(e, width, pin):
    """Pin/slider datums separately bounded +/-e; each x face +/-0.1.
    Shared datum may cancel; all Cartesian corners include coherent/differential
    errors. Minima are set bounds, not joint occurrence or statistical yield.
    """
    min_fit=math.inf
    max_play=0.
    corners=0
    solid_checks=0
    for sd, pd, hl, hr, pl, pr in it.product((-e,e),(-e,e), *[(-.1,.1)]*4):
        # Aligned aperture at either endpoint, in global coordinates.
        hole=(1.9+sd-width/2+hl,1.9+sd+width/2+hr)
        p=(1.9+pd-pin/2+pl,1.9+pd+pin/2+pr)
        fit=min(p[0]-hole[0],hole[1]-p[1])
        min_fit=min(min_fit,fit)
        # End stop blocks outward motion; the remaining inward clearance can
        # move the active lip toward clear, or clear lip toward active.
        max_play=max(max_play,p[0]-hole[0],hole[1]-p[1])
        corners+=1
        solids=tail(width,(hl,hr,hl,hr))
        if solids is not None:
            actual_bolt=(*p,1.7,2.3,.7,2.2)
            for q in (0.,1.4):
                intrusion=sum(volume(translate(b,x=sd+q),actual_bolt) for b in solids)
                if fit>=-1e-12:assert intrusion<1e-12
                else:assert intrusion>1e-12
                solid_checks+=1
    min_web=min(1.9-width/2+cl-(.5+width/2+ar)
                for cl,ar in it.product((-.1,.1),repeat=2))
    assert math.isclose(min_fit,(width-pin)/2-2*e-.2,abs_tol=1e-12)
    assert math.isclose(max_play,(width-pin)/2+2*e+.2,abs_tol=1e-12)
    assert math.isclose(min_web,1.4-width-.2,abs_tol=1e-12)
    # Already at e=.2 the E-095 reserve is .1; at most .05 extra inward drift
    # fits its .05 geometry gate. This is a REQUIRED allocation, not an added
    # independent random variable or a claimed combined worst-case assembly.
    required_play=.05
    return dict(datum_bound_mm=e,aperture_mm=width,pin_mm=pin,corners=corners,
                min_insertion_clearance_mm=min_fit,min_web_mm=min_web,
                max_endpoint_inward_play_mm=max_play,finite_solid_checks=solid_checks,
                insertion_and_web_pass=min_fit>=.05-1e-12 and min_web>=.2-1e-12,
                pickup_reserve_pass=max_play<=required_play+1e-12)


def witness():
    # Nominal width=1, pin=.4: bolt fits, but retained active slider may move
    # inward .3 without any pin/solid contact. Use q=1.11, strictly inside.
    q=1.11
    assert all(volume(translate(b,x=q),bolt(.4))<1e-12 for b in tail(1.))
    # E-095 retained adverse capture uses lip [1.2,3.5], finger [3.4,4.6].
    lost=overlap((1.2+q-1.4,3.5+q-1.4),(3.4,4.6))
    assert lost==0
    # Differential datum corner causes an inserted bolt to hit the actual tail rim.
    finite=tail(1.,(0.,.1,-.1,0.))
    assert finite is not None
    penetration=sum(volume(translate(b,x=-.2),bolt(.4,x=2.1)) for b in finite)
    assert penetration>0
    return dict(nominal_allowed_inward_shift_mm=1.4-q,
                adverse_pickup_overlap_after_shift_mm=lost,
                differential_datum_tail_collision_mm3=penetration)


def main():
    routes=[nominal_route(n) for n in (1,16,64)]
    rows=[screen(e,w,p) for e,w,p in it.product((0.,.1,.2,.3),(.8,1.,1.2,1.6,2.),(.4,.6,.8))]
    # Independent continuous bound: w >= pin+4e+.5 for .05 per-face fit,
    # while w <= 1 for a .2 web. At e=.2 even pin=.4 needs w>=1.7.
    assert not any(r['insertion_and_web_pass'] for r in rows if r['datum_bound_mm']>=.1)
    assert not any(r['insertion_and_web_pass'] and r['pickup_reserve_pass'] for r in rows)
    # Fixed short tool cannot visit two handles separated by 40mm without
    # another coordinate. An all-height engagement blade must cover the span
    # plus the 1.5mm pin/handle engagement height (packaging bound only).
    reach=40.+1.5
    assert reach==41.5
    print(json.dumps(dict(routes=routes,parameter_cases=len(rows),corner_evaluations=sum(r['corners'] for r in rows),
        finite_solid_checks=sum(r['finite_solid_checks'] for r in rows),screens=rows,witness=witness(),all_height_tool_envelope_floor_mm=reach,
        disposition='Reject this unpreloaded rigid two-aperture lock at the E-095 bounds; open pickup principle remains. No assembled bank, pin retainer, common writer, force or hardware pass.'),indent=2))

if __name__=='__main__':main()
