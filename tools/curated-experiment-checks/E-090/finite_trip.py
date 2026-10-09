"""E-090: finite single-slot contact sections, mm/N; bounded scenarios, no priors.
No contact elasticity, frictional dynamics, support mechanism or hardware claim.
Deterministic enumeration; SAT polygon holdouts independently check the reduced
insertion law. Run directly; no generated artifacts are required.
"""
import itertools
import json
import math


def overlap(a, b):
    """Strict positive-area convex polygon intersection via separating axes."""
    for poly in (a, b):
        for u, v in zip(poly, poly[1:] + poly[:1]):
            nx, ny = -(v[1]-u[1]), v[0]-u[0]
            aa = [nx*x+ny*y for x,y in a]
            bb = [nx*x+ny*y for x,y in b]
            if min(max(aa),max(bb))-max(min(aa),min(bb)) <= 1e-10:
                return False
    return True


def rectangle(x0, x1, y0, y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]


def probe(dx, depth, width, tip=.2, chamfer=.4):
    return [(dx-width/2,depth-3),(dx+width/2,depth-3),
            (dx+width/2,depth-chamfer),(dx+tip/2,depth),
            (dx-tip/2,depth),(dx-width/2,depth-chamfer)]


def collision(dx, depth, width, slot, half_body):
    pin = probe(dx, depth, width)
    return any(overlap(pin, wall) for wall in
               [rectangle(-half_body,-slot/2,0,1),
                rectangle(slot/2,half_body,0,1)])


def depth_polygon(dx, width, slot, half_body, stroke=1.5):
    # Stops at first contact. No teleported penetration. Contact is monotone
    # over this stroke: the 3-mm shank still crosses the 1-mm plate at its end.
    if not collision(dx,stroke,width,slot,half_body):
        return stroke
    lo,hi=0.,stroke
    for _ in range(38):
        mid=(lo+hi)/2
        if collision(dx,mid,width,slot,half_body):hi=mid
        else:lo=mid
    return lo


def depth_reduced(dx,width,slot,stroke=1.5):
    """Infinite side lands; NOT valid when a finite plate end can be bypassed."""
    available=slot-2*abs(dx)
    if available >= width-1e-10:return stroke
    return max(0., min(.4, .4*(available-.2)/(width-.2)))


def geometry_screen():
    records=[]
    comparisons=0
    for alpha,E0,size,ratio in itertools.product((.5,1.),(.1,.2,.4),(.05,.1),(0.,.01)):
        p=2*alpha  # H=21, 40-mm output travel
        # Both independent width deviations have magnitude size. Error E0 is
        # common+spatial+local relative datum bound, before gain uncertainty.
        E=E0+40*alpha*ratio
        slot=.4+p  # midpoint between target containment and wrong-state fit
        capture=(slot-size-(.4+size))/2-E
        reject=p-E-(slot+size-(.4-size))/2
        full=partial=false=0
        max_wrong_depth=0.
        # Fixed manufactured width corners; datum endpoint deviations and
        # common gain corners; all actual command/reader positions.
        for q,r,dw,ds,datum,gain in itertools.product(range(-20,21),range(-20,21),
                (-size,size),(-size,size),(-E0,E0),(-ratio,ratio)):
            dx=(r-q)*p+datum+r*p*gain
            d=depth_reduced(dx,.4+dw,slot+ds)
            comparisons+=1
            if q==r:full+=d>=1.5-1e-9
            else:
                partial+=0<d<1.5-1e-9
                false+=d>=1.5-1e-9
                max_wrong_depth=max(max_wrong_depth,d)
        # A nominal slot width can solve both only if this gap is positive.
        width_interval=(.4+2*E+2*size, .4+2*(p-E)-2*size)
        # Conservative end-to-end face envelope for all q/r including opposite
        # extremes: body half-length >= max |reader-cursor| + widest half pin.
        half_body=40*p+E+(.4+size)/2
        records.append(dict(alpha=alpha,datum_bound_mm=E0,width_bound_each_mm=size,
            gain_bound=ratio,pitch_mm=p,slot_mm=slot,worst_error_mm=E,
            capture_margin_mm=round(capture,6),reject_margin_mm=round(reject,6),
            retunable=width_interval[0]<width_interval[1]-1e-9,
            width_feasible_interval_mm=width_interval,
            robust=capture>1e-9 and reject>1e-9,
            intended_full_corner_cases=full,wrong_full_corner_cases=false,
            wrong_partial_corner_cases=partial,max_wrong_depth_mm=max_wrong_depth,
            body_length_mm=2*half_body,swept_length_mm=2*half_body+40*p,
            sign_gated_body_length_mm=38*p+2*E+.4+size,
            sign_gated_swept_length_mm=78*p+2*E+.4+size))
    return records,comparisons


def independent_checks():
    checked=0
    # Polygon halfspaces, not the insertion formula, generate contact depths.
    # Deterministic holdouts include interior errors and partial chamfer capture.
    for w,s,dx in itertools.product((.3,.4,.5),(1.3,1.4,1.5,2.3,2.4,2.5),
                                   (-3.,-.93,-.65,-.57,-.41,0.,.41,.57,.65,.93,3.)):
        a=depth_reduced(dx,w,s)
        b=depth_polygon(dx,w,s,100)
        assert abs(a-b)<1e-7,(w,s,dx,a,b)
        checked+=1
    assert depth_polygon(3.,.4,1.4,1.)==1.5  # finite short tag bypass
    assert depth_reduced(3.,.4,1.4)==0.
    assert depth_reduced(.6,.3,1.5)==1.5  # wrong neighbor, alpha=.5 adverse corner
    assert depth_reduced(.4,.5,1.3)==1.5  # target just tangent: zero reserve
    assert 0<depth_reduced(.6,.4,1.5)<.4  # partial chamfer entry
    # Query motion is forbidden while inserted. For this witness the shank
    # hits the slot land before the next 1-mm reader station is reached.
    assert not collision(0,1.5,.4,1.4,100)
    assert collision(1.,1.5,.4,1.4,100)
    assert not collision(1.,-.1,.4,1.4,100)
    # Rigid carrier advances only to minimum local contact depth. A blocked
    # neighbor prevents a selected pin reaching the depth-gated output.
    depths=[depth_reduced(x,.4,2.4) for x in (0.,2.)]
    assert depths==[1.5,0.]
    assert min(depths)<.8
    # Global return stop caps insertion below a depth-gate's earliest opening.
    # This is a contact envelope only, not proof of a constructed interlock.
    assert .3+.1 < .8-.1
    assert .4+.1 < .8-.1 < 1.5-.1  # partial/full depth discrimination
    carrier, jammed_probe = 1.5, 0.
    assert carrier >= .8 and jammed_probe < .8  # carrier proof false accept
    return checked


def finite_face_checks():
    checked=0
    for alpha,sign_gate in itertools.product((.5,1.),(False,True)):
        p=2*alpha
        E=.4+40*alpha*.01
        half_body=(19 if sign_gate else 40)*p+E+.25
        for q,r,datum,gain in itertools.product(range(-20,21),range(-20,21),
                                                (-.4,.4),(-.01,.01)):
            # The sign gate is an explicit unproved prerequisite, not silently
            # credited geometry. Acquisition at zero uses a separate sign cam.
            if sign_gate and q*r<=0:continue
            dx=(r-q)*p+datum+r*p*gain
            expected=depth_reduced(dx,.5,.4+p-.1)>=1.5
            actual=not collision(dx,1.5,.5,.4+p-.1,half_body)
            assert actual==expected,(alpha,sign_gate,q,r,dx)
            checked+=1
    # Failed opposite-sign inhibition defeats the shorter face.
    assert depth_polygon(80.,.4,2.4,39.05)==1.5
    return checked


def main():
    checks=independent_checks()
    face_checks=finite_face_checks()
    rows,count=geometry_screen()
    # Exact critical-alpha inversion (strict inequality).
    critical=(2*.4+2*.1)/(2-80*.01)
    assert math.isclose(critical,5/6)
    adverse=[r for r in rows if r['datum_bound_mm']==.4 and r['width_bound_each_mm']==.1]
    assert all(not r['retunable'] for r in adverse if r['alpha']==.5)
    assert all(r['robust'] for r in adverse if r['alpha']==1.)
    # Representative passive probe isolators: assumed spring + preload only.
    forces=[]
    for k,f0 in ((.05,.02),(.2,.1),(.8,.1)):
        blocked=f0+k*1.5
        forces.append(dict(k_N_per_mm=k,preload_N=f0,blocked_pin_N=blocked,
            bank800_all_blocked_N=800*blocked,board6400_all_blocked_N=6400*blocked,
            board_spring_energy_J=6400*.5*k*1.5**2/1000))
    print(json.dumps(dict(evidence='bounded rigid contact calculation; no hardware qualification',
        state_width_error_corner_cases=count,polygon_holdouts=checks,
        finite_face_state_error_checks=face_checks,
        robust_scenarios=sum(r['robust'] for r in rows),scenarios=len(rows),
        alpha_strictly_above_for_adverse_1pct_gain=critical,
        adverse_scenarios=adverse,probe_isolation_force_scenarios=forces,
        all_scenarios=rows),indent=2))

if __name__=='__main__':main()
