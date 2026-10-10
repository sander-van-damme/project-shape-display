#!/usr/bin/env python3
"""Finite split cage, long sleeve and common-retractor witnesses. mm, N.
Explicit uncertainty boxes; no priors, yield estimates or hardware validation.
Standard library, deterministic; prints results without generating files.
"""
from dataclasses import dataclass
from itertools import product
from math import isclose
import json

EPS = 1e-9


@dataclass(frozen=True)
class Box:
    x: tuple
    y: tuple
    z: tuple

    def collides(self, other):
        return all(min(a[1], b[1])-max(a[0], b[0]) > EPS
                   for a, b in zip((self.x, self.y, self.z),
                                   (other.x, other.y, other.z)))


def collar(q, s=0.):
    return Box((s-1.8, s+1.8), (6.2, 9.8), (q+17., q+18.))


def dog(q, s=0.):
    return Box((s-1., s+1.), (7., 9.), (q, q+17.))


def command(r, opening=0., s=0.):
    # Independent transverse jaw opening, not displacement of frozen command r.
    return [Box((s-2., s+2.), y, z)
            for y in ((6.3-opening, 6.8-opening),
                      (9.2+opening, 9.7+opening))
            for z in ((r+16.2, r+16.6), (r+18.4, r+18.8))]


def retractor(h, gap=.7, opening=0., s=0.):
    # Orthogonal split fingers; retract in x, command jaws retract in y.
    # h is the aperture's dog-coordinate center; gap is permitted q-h.
    return [Box(x, (7.2, 8.8), z)
            for x in ((s-1.7-opening, s-1.3-opening),
                      (s+1.3+opening, s+1.7+opening))
            for z in ((h+16.6-gap, h+17.-gap),
                      (h+18.+gap, h+18.4+gap))]


def tongue():
    return [Box(x, (6.5,9.5), (2.,2.8))
            for x in ((-3.,-1.8),(1.8,3.))]


def sleeve(s=0.):
    # Two finite opposed x lands, continuous over 4..10; through y aperture.
    return [Box((x[0]+s,x[1]+s),(6.8,9.2),(4.,10.))
            for x in ((-1.6,-1.05),(1.05,1.6))]


def force_ratio(a,b,c,w,mt,ma,mb):
    # Reconstructed equilibrium, not imported from E-118. +F at -w/2,c;
    # -A at +w/2,a; +B at -w/2,b. Axial friction opposes extraction.
    den=b-a+w/2*(ma-mb)
    num=a-c+w/2*(mt-ma)
    assert den > 0 and num > 0
    B=num/den; A=1+B
    pull=mt+ma*A+mb*B
    assert abs(1-A+B) < EPS
    assert abs(c-a*A+b*B+w/2*(-mt+ma*A-mb*B)) < EPS
    return pull, den


def local_path(n):
    # Favorable single site: retractor is independently registered to actual q.
    # External drives are prescribed positive coordinates, not completed routing.
    checks=0
    for r in (-1.,1.5,3.6):
        # Collar at either allowed command-fork endpoint, including intermediate.
        for q0 in (r-.4,r,r+.4):
            h0=q0
            # Insert retractor fingers, then open frozen command cage.
            for i in range(n+1):
                u=i/n
                for q,h,jaw,ropen in ((q0,h0,0.,1.-u),
                                      (q0,h0+.7*u,0.,0.),
                                      (q0,h0+.7,u,0.)):
                    parts=command(r,jaw)+retractor(h,.7,ropen)
                    assert not any(collar(q).collides(v) or dog(q).collides(v)
                                   for v in parts)
                    assert not any(a.collides(b) for a in command(r,jaw)
                                   for b in retractor(h,.7,ropen))
                    checks+=1
            # Lift lower finger to collar, then lift dog. Downward friction
            # holds q until positive contact; this is not a gravity completion.
            q=q0
            for i in range(n+1):
                h=h0+.7+(5.-h0-.7)*i/n
                q=max(q,h-.7)
                assert not any(collar(q).collides(v) or dog(q).collides(v)
                               for v in command(r,1.)+retractor(h))
                assert q <= 4.3+EPS
                # Dog spans the full sleeve while tongue load can exist.
                if q <= 2.8:
                    assert q <= 4. and q+17. >= 10.
                assert not any(dog(q).collides(v) for v in sleeve())
                checks+=1
            assert isclose(q,4.3)
            assert all(not dog(q,s).collides(w)
                       for s in (0.,.8,4.5) for w in tongue())
            # Positive downward reset: upper finger contacts and pushes dog.
            # With a private h axis it can return exactly to original q0.
            for i in range(n+1):
                h=5.+(q0-.7-5.)*i/n
                q=min(q,h+.7)
                assert not any(collar(q).collides(v) or dog(q).collides(v)
                               for v in command(r,1.)+retractor(h))
                checks+=1
            assert isclose(q,q0,abs_tol=EPS)
            # Recapture at original command; retractor then withdraws sideways.
            for i in range(n+1):
                u=i/n
                for jaw,ropen in ((1.-u,0.),(0.,u)):
                    assert not any(collar(q).collides(v) or dog(q).collides(v)
                                   for v in command(r,jaw)+retractor(h,.7,ropen))
                    checks+=1
    return checks


def main():
    e=.1
    # Loaded/stalled extraction at exact dog/tongue wall contact, with the
    # working sled stopped at s=.8. All z paths affine; the touching x plane
    # and separated sleeve x planes prove nonpenetration continuously.
    for n in (32,128,512):
        for i in range(n+1):
            q=-1.+5.3*i/n
            assert not any(dog(q,.8).collides(w) for w in tongue()+sleeve(.8))
            if q <= 2.8:
                assert q <= 4. and q+17. >= 10.
    # Actual generated finite path plus endpoint geometry certificates:
    # every segment is axis-aligned translation, separating x/y projections
    # certify command/retractor mutual clearance for every intermediate step.
    path_counts={n:local_path(n) for n in (32,128,512)}
    assert 7.2-6.8 > 0 and 9.2-8.8 > 0
    # Relative face bounds. Open-jaw nearest y and collar y each err by ±e;
    # jaw stroke errs by ±e. e is an epistemic face bound, not machine accuracy.
    open_margins=[]; capture=[]
    for datum,stroke,edge in product((-e,e),repeat=3):
        open_margins.append((6.2+edge)-(6.8+datum-(1.+stroke)))
    for qerr,herr,face in product((-e,e),repeat=3):
        # commanded q0 plus each possible retained ±.4 slack endpoint.
        for slack in (-.4,.4):
            capture.append(.7+face-abs(slack+qerr-herr))
    assert min(open_margins) > 0
    assert min(capture) >= -EPS  # zero reserve, not a robust clearance pass!

    # Long sleeve edge-contact model: common datum and local edge errors.
    # Loaded q ends at tongue top <=2.9; sleeve begins >=3.8. The dog length
    # ensures full sleeve support even at lowest selected q=-1.5.
    forces=[]; dens=[]
    for common,da,db,dc,dw in product((-e,e),repeat=5):
        a=4.+common+da; b=10.+common+db; w=2.+dw
        for c in (2.+dc,2.8+dc):
            for mt,ma,mb in product((0.,.1,.3,.5,.7),repeat=3):
                f,den=force_ratio(a,b,c,w,mt,ma,mb)
                forces.append(f); dens.append(den)
                translated=force_ratio(a+100,b+100,c+100,w,mt,ma,mb)[0]
                assert isclose(f,translated,abs_tol=EPS)
                if mt==ma==mb:
                    assert isclose(f,2*mt*(b-c)/(b-a),abs_tol=EPS)
    # Continuous-box denominator certificate; vertex friction grid is only
    # sensitivity, not an exhaustive force bound. Conservative independent
    # interval bound encloses every permitted coefficient and geometry.
    den_bound=5.8-1.05*.7
    B_bound=(2.3+1.05*.7)/den_bound
    pull_bound=.7+.7*(1+B_bound)+.7*B_bound
    assert isclose(min(dens),den_bound)
    assert max(forces) <= pull_bound

    # Shared tight retractor: finite collar containment means h belongs to
    # [q-gap,q+gap]. Common absolute z bias cancels from interval separation.
    # Even granting exact known q, two unlike collars cannot fit simultaneously.
    deficits=[]
    for common,l1,l2,g1,g2 in product((-e,e),repeat=5):
        q1=-1.+common+l1; q2=3.6+common+l2
        left=q2-(.7+g2); right=q1+(.7+g1)
        deficits.append(left-right)
        assert left > right
    # Also fails with two engaged dogs: q=-1 and intermediate-stuck q=1.5.
    assert 1.5-(-1.)-2*.7 > 0
    # Nominal collision at symmetric h: fingers intersect collars, not merely
    # a failed scalar inequality. Aperture fingers must pass their x envelopes.
    h=1.3
    assert any(collar(-1.).collides(v) for v in retractor(h,2.0))
    assert any(collar(3.6).collides(v) for v in retractor(h,2.0))

    # Widening IS a valid takeover counterexample; do not call the tight-fork
    # exclusion a universal impossibility. Wide fork encloses both, then lifts.
    gap=2.7; h=1.3
    qs=[-1.,3.6]
    assert all(not any(collar(q).collides(v) for v in retractor(h,gap)) for q in qs)
    for i in range(513):
        h=1.3+(7.-1.3)*i/512
        qs=[max(q,h-gap) for q in qs]
        assert all(not any(collar(q).collides(v) for v in retractor(h,gap)) for q in qs)
    assert all(isclose(q,4.3) for q in qs)
    # This erases dog-coordinate differences, not separately retained r values.
    # With both command cages open, common downward reset keeps dogs coincident.
    # Closing a selected command cage first leaves its upper finger in the
    # descending collar's path. q=r+1.8 is first contact with that finger's top.
    r=-1.; first_contact=r+1.8
    assert not any(collar(first_contact).collides(v) for v in command(r))
    assert any(collar(first_contact-.01).collides(v) for v in command(r))
    assert first_contact > r+.4  # collision before retained aperture reached
    # Simultaneous cage closure requires overlap of [r_i-.4,r_i+.4].
    assert 3.6-.4 > -1.+.4
    reset_deficits=[]
    for face,thickness,bottom,top in product((-e,e),repeat=4):
        hit=r+1.8+face+thickness-bottom
        latest_capture=r+.4+face-top
        reset_deficits.append(hit-latest_capture)
    assert min(reset_deficits) > 0
    # Equal-command control: common retractor can capture/reset all sites
    # when they require the same q; exclusion depends on mixed commands.
    assert max(-1.-.7,-1.-.7) <= min(-1.+.7,-1.+.7)
    # Sequential closure could escape, but introduces a conditional local
    # closing drive/interlock absent from the evaluated shared topology.
    result=dict(evidence='finite section and conditional planar statics; self-review',
                paths=path_counts,open_jaw_margin=min(open_margins),
                tight_capture_margin=min(capture),
                contact_cases=len(forces),min_contact_denominator=min(dens),
                max_sampled_pull_per_transverse_load=max(forces),
                continuous_box_pull_upper_bound=pull_bound,
                common_tight_retractor_deficit=[min(deficits),max(deficits)],
                engaged_pair_deficit=1.5+1.-1.4,
                wide_retractor_all_clear_q=qs,
                closed_selected_cage_reset_collision_q=first_contact,
                closed_cage_reset_deficit=[min(reset_deficits),max(reset_deficits)],
                decision='retain local split cage/long sleeve; stop synchronous shared reset embodiment')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
