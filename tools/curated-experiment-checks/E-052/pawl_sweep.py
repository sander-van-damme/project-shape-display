"""Conservative 2-D rectangle swept-volume synthesis; mm, no fitted priors."""
import itertools
import json
from collections import Counter

PITCH = 5.08
GAP = 0.10
SUPPORT = 0.40
STATES = tuple(range(5))
ERRORS = {'tight': .15, 'middle': .35, 'wide': .60}


def intersects(a, b):
    """Positive-area intersection; boundary touch is allowed support contact."""
    return min(a[1], b[1]) > max(a[0], b[0]) + 1e-9 and min(a[3], b[3]) > max(a[2], b[2]) + 1e-9


def swept(a, b):
    # Exact union for a rectangle translated along ONE coordinate.
    assert abs(a[0]-b[0]) < 1e-9 or abs(a[2]-b[2]) < 1e-9
    return min(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), max(a[3], b[3])


def screen(w, r, length, overlap, tooth, pawl, lift, e):
    # Each rack/pawl x placement +/-e/2, plus common bank placement +/-e/2.
    # Relative x error <=e; absolute edge error <=e. Stroke uncertainty is
    # included in that placement envelope, not an additional unknown term.
    x0 = e + GAP
    tip = x0+w+r
    engaged = tip-overlap
    stroke = overlap+e+GAP
    right = engaged+stroke+length+e
    failures = []
    if right > PITCH + 1e-9:
        failures.append('pitch')
    worst_overlap = float('inf')
    for dr, dp in itertools.product((-e/2, e/2), repeat=2):
        left, end = engaged+dp, engaged+dp+length
        contact = max(0., min(tip+dr, end)-max(x0+w+dr, left))
        worst_overlap = min(worst_overlap, contact)
        if left < x0+w+dr+GAP-1e-9:
            failures.append('pawl_into_web')
        if left+stroke < tip+dr+GAP-1e-9:
            failures.append('retracted_clearance')
    if worst_overlap < SUPPORT-1e-9:
        failures.append('support_overlap')
    if lift-e < GAP-1e-9:
        failures.append('unload_clearance')
    if failures:
        return sorted(set(failures)), None

    # Pawl-tooth swept boxes. Every state seats on its own actual tooth;
    # other tooth origins differ from nominal by <=e relative to that tooth.
    # Actual thickness <= nominal+e. Lift positioning error <=e.
    # These are envelopes, not probability distributions or meshed CAD.
    for old, new in itertools.product(STATES, repeat=2):
        if old == new:  # Non-target pawl remains seated; no release command.
            continue
        for dr, dp in itertools.product((-e/2, e/2), repeat=2):
            p0 = (engaged+dp, engaged+dp+length, -pawl-e, 0.)
            p1 = (p0[0]+stroke, p0[1]+stroke, p0[2], p0[3])
            for state in (old, new):
                for k in STATES:
                    base = (state-k)*10.
                    err = 0. if k == state else e
                    # Lift/seat: conservatively sweep all intermediate z.
                    vertical = (x0+w+dr, tip+dr,
                                base-err, base+err+tooth+e+lift+e)
                    if intersects(vertical, p0):
                        failures.append('lift_seat_collision')
                    # At unload height pawl translates horizontally.
                    lifted = (vertical[0], vertical[1], base-err+lift-e,
                              base+err+tooth+e+lift+e)
                    if intersects(lifted, swept(p0,p1)):
                        failures.append('release_insert_collision')
            # Full vertical relocation; swept rack covers all five teeth.
            moving = (x0+w+dr, tip+dr, -40.+min(old,new)*10.-e,
                      max(old,new)*10.+lift+tooth+3*e)
            if intersects(moving, p1):
                failures.append('relocation_collision')
    return sorted(set(failures)), {'width': round(right,4),
        'stroke': round(stroke,4), 'overlap_min': round(worst_overlap,4),
        'lift': lift, 'web':w, 'tooth_reach':r, 'pawl_length':length,
        'nominal_overlap':overlap, 'tooth_thickness':tooth, 'pawl_thickness':pawl}


def run():
    assert not intersects((0,1,0,1),(1,2,0,1))
    assert intersects((0,1,0,1),(.9,2,0,1))
    # Endpoint-only testing would miss this transit collision.
    a,b=(0,1,0,1),(3,4,0,1)
    obstacle=(1.5,2.5,0,1)
    assert not intersects(a,obstacle) and not intersects(b,obstacle)
    assert intersects(swept(a,b),obstacle)
    output={}
    for name,e in ERRORS.items():
        rejects=Counter(); survivors=[]; n=0
        grid=itertools.product((1.6,2.,2.4),(.8,1.2,1.6),(.8,1.2,1.6),
                               (.6,.9,1.2),(1.,2.),(1.,2.),(.3,.6,1.))
        for args in grid:
            n+=1
            reasons, result=screen(*args,e)
            if reasons: rejects.update(reasons)
            else: survivors.append(result)
        # Independent packing lower bound with these web/reach/length minima:
        lower=1.6+.8+.8+3*e+2*GAP
        assert all(x['width'] >= lower-1e-9 for x in survivors)
        if lower>PITCH: assert not survivors
        best=min(survivors,key=lambda x:(x['width'],x['stroke'],x['lift'])) if survivors else None
        # Solve overlap and web-clearance inequalities at equality, rather than
        # confusing a coarse grid miss with a topology rejection.
        o=SUPPORT+e
        r=max(.8,o+e+GAP)
        exact_lower=1.6+r+.8+3*e+2*GAP
        why,witness=screen(1.6,r,.8,o,1.,1.,e+GAP,e)
        assert bool(why) == (exact_lower > PITCH+1e-9)
        output[name]={'continuous_packing_bound':round(exact_lower,4),
                      'boundary_witness':witness if not why else None,
                      'boundary_failures':why,'error':e,'candidates':n,'survivors':len(survivors),
                      'failure_counts_nonexclusive':dict(rejects),
                      'packing_lower_bound':round(lower,4),'compact_survivor':best}
    # A selected nominal geometry must fail with inadequate unload travel.
    assert 'unload_clearance' in screen(1.6,1.2,1.2,.9,1.,1.,.3,.35)[0]
    # Force adjacent tooth interference despite ample lateral packaging.
    assert 'lift_seat_collision' in screen(1.6,1.2,1.2,.9,5.,5.,.6,.15)[0]
    reasons, interior=screen(1.6,1.24,.8,.77,2.,2.,.47,.35)
    assert not reasons and interior['overlap_min'] > SUPPORT
    output['middle_interior_witness']=interior
    # Analytic threshold of this packaging class (w>=1.6, L>=.8).
    for e, feasible in ((.395,True),(.397,False)):
        reasons,_=screen(1.6,SUPPORT+2*e+GAP,.8,SUPPORT+e,1.,1.,e+GAP,e)
        assert (not reasons) == feasible
    return output

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
