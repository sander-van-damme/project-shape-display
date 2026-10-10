#!/usr/bin/env python3
"""E-118 finite relocated follower / captive dog rejection. mm, N, MPa.
Deterministic epistemic bounds, not X1C priors or reliability probabilities.
Run directly with Python standard library. No files generated.
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

    def overlap(self, other):
        return tuple(min(a[1], b[1])-max(a[0], b[0])
                     for a, b in zip((self.x, self.y, self.z),
                                     (other.x, other.y, other.z)))

    def collides(self, other):
        return min(self.overlap(other)) > EPS


def dog(s, q, width=2.):
    return Box((s-width/2, s+width/2), (7., 9.), (q, q+8.))


def collar(s, q, height_error=0.):
    return Box((s-1.5, s+1.5), (6.2, 9.8), (q+6., q+7.+height_error))


def tongue(t=0., half=1.8, z=(2., 2.8)):
    # Through aperture with two finite load walls. Deliberately generous
    # out-of-plane aperture: only the x faces carry working force.
    return [Box((t-3., t-half), (6.5, 9.5), z),
            Box((t+half, t+3.), (6.5, 9.5), z)]


def fork(r, gap=.4, face_error=0.):
    # Two pairs of fingers above/below the enlarged collar. They span the
    # full x working stroke, retain q, and avoid the narrower dog shaft in y.
    return [Box((-2., 6.5), y, z)
            for y in ((6.3, 6.8), (9.2, 9.7))
            for z in ((r+5.-gap, r+6.-gap),
                      (r+7.+gap+face_error, r+8.+gap+face_error))]


def reactions(a, b, c, force=1.):
    """Signed bearing reactions for transverse load +force at c.
    Negative means reaction against the applied load. Opposing signs require
    opposite guide faces and amplify axial sliding friction.
    """
    assert b > a
    return -force*(b-c)/(b-a), -force*(c-a)/(b-a)


def withdrawal(a,b,c,width,mu_t,mu_a,mu_b):
    """Finite-width planar Coulomb contacts during upward extraction.
    Tongue +F at x=-w/2, lower guide -A at +w/2, upper +B at -w/2.
    Axial friction is downward at all contacts. A-B=F. Include the moments
    of those axial friction forces, which cancel only for equal coefficients.
    """
    denom=b-a+width/2*(mu_a-mu_b)
    numerator=a-c+width/2*(mu_t-mu_a)
    if denom <= 0 or numerator < 0:
        return dict(ok=False,denominator=denom,numerator=numerator)
    B=numerator/denom; A=1+B
    pull=mu_t+mu_a*A+mu_b*B
    moment=c-A*a+B*b+width/2*(-mu_t+mu_a*A-mu_b*B)
    assert abs(moment) < 1e-8
    assert isclose(-1+A-B,0.,abs_tol=EPS)
    return dict(ok=True,A=A,B=B,pull=pull,denominator=denom)


def ray_entry(moving, fixed, axis):
    """Exact first positive translation contact, without a time-step sweep."""
    aa=(moving.x, moving.y, moving.z)
    bb=(fixed.x, fixed.y, fixed.z)
    if any(min(aa[i][1], bb[i][1]) <= max(aa[i][0], bb[i][0])+EPS
           for i in range(3) if i != axis):
        return None
    entry=bb[axis][0]-aa[axis][1]
    leave=bb[axis][1]-aa[axis][0]
    return max(0., entry) if leave > max(0., entry)+EPS else None


def main():
    # Permanent power follower: square post spans z=-2..6, guides at -1..0
    # and 4..5; cam load layer 1.5..2.5. Cam motion y=0..9 gives x=-.5*y;
    # reversing coordinate direction gives sled s=0..4.5 used below.
    # The post does not perform axial selection. Dog is a different part at y=8.
    e=.1
    straddle_margin=1e9
    for common, low, high, cam in product((-e, e), repeat=4):
        lower=(-1.+common+low, common+low)
        upper=(4.+common+high, 5.+common+high)
        load=(1.5+cam, 2.5+cam)
        straddle_margin=min(straddle_margin, load[0]-lower[1], upper[0]-load[1])
        assert -2. <= lower[0] and upper[1] <= 6.
        for c in load:
            ra, rb=reactions(sum(lower)/2, sum(upper)/2, c)
            assert ra < 0 and rb < 0
            assert isclose(abs(ra)+abs(rb), 1.)
    assert straddle_margin > 0
    # Actual square follower vertices against the finite oblique slot planes.
    # Relative cam y=2*s, follower x=-s, slope .5; z load layer above.
    cam_margin=1e9
    for dw,dx,dy,dh in product((-e,e),repeat=4):
        for s in (0.,4.5):
            for vx,vy in product((-(2.+dw)/2,(2.+dw)/2),repeat=2):
                x=-s+dx+vx; y=2*s+dy+vy
                cam_margin=min(cam_margin,1.9+dh-abs(x+.5*y))
                assert -1.5 <= y <= 10.5
    assert cam_margin > 0

    # Favorable registered home insertion is granted to isolate the new fault
    # gate. These nominal paths are NOT a tolerance/ground-support acceptance.
    path_min=1e9
    for q in (-1., 1.5, 3.6):
        for s in (0., 4.5):
            assert not any(collar(s,q).collides(f) for f in fork(q))
            assert not any(dog(s,q).collides(f) for f in fork(q))
    for n in (32, 128, 512):
        for i in range(n+1):
            q=-1.+4.6*i/n
            assert not any(dog(0.,q).collides(w) for w in tongue())
            assert not any(collar(0.,q).collides(f) for f in fork(q))
        # Bidirectional contact after finite backlash; play operator follows
        # tongue only when the dog touches a wall, never by hidden centering.
        for initial in (-.8, .8):
            t=initial
            for s in [4.5*i/n for i in range(n+1)]+[4.5*(1-i/n) for i in range(n+1)]:
                t=max(s-.8, min(s+.8, t))
                assert not any(dog(s,-1.).collides(w) for w in tongue(t))
                assert not any(collar(s,-1.).collides(f) for f in fork(-1.))
                path_min=min(path_min, .8-abs(s-t))
            assert isclose(t,.8,abs_tol=EPS)

    # Nominal jam is tested while blade is immobilized (keeper not withdrawn,
    # mechanical obstruction, or residual service-load stall). The first
    # collision forbids jumping through a wall to a later clear position.
    jam_dog=dog(0.,1.5)
    contact=min(v for w in tongue() if (v:=ray_entry(jam_dog,w,0)) is not None)
    assert isclose(contact,.8)
    assert dog(1.,1.5).collides(tongue()[1])
    c=collar(0.,1.5)
    fork_contact=min(v for f in fork(1.5) if (v:=ray_entry(c,f,2)) is not None)
    assert isclose(fork_contact,.4)
    assert collar(0.,1.5+.5).collides(fork(1.5)[1])

    # Enclose local dog/slot width and datum errors: all relative corners may
    # occur in one cell or coherently across a bank. No independent-cell prior.
    jam_cases=[]
    for dw, dh, dx, dz, dr, df, dc in product((-e,e),repeat=7):
        r=1.5+dr
        qmax=r+.4+df-dc
        z=(2.+dz,2.8+dz)
        clear_q=z[1]+.1
        d=dog(0.,r,2.+dw)
        walls=tongue(dx,1.8+dh,z)
        hit=min(v for w in walls if (v:=ray_entry(d,w,0)) is not None)
        assert 0 < hit < 4.5
        # Explicit collar vertices against upper jaw recover qmax.
        actual_c=collar(0.,r,dc)
        fs=fork(r,face_error=df)
        up=min(v for f in fs if (v:=ray_entry(actual_c,f,2)) is not None)
        assert isclose(r+up,qmax)
        assert qmax < z[1]  # Still overlaps load layer, even before reserve.
        jam_cases.append((hit,clear_q-qmax))

    # Even widening the one rigid retaining aperture cannot guarantee both
    # selected full-depth bearing and withdrawal with the command frozen.
    # Apply exact nominal constraints first; errors only enlarge this conflict.
    selected=-1.; full_depth_q=2.-.1; release_q=2.8+.1
    gap_max=full_depth_q-selected
    gap_needed=release_q-selected
    assert gap_needed > gap_max
    for gap in (.4, gap_max, gap_needed, 4.5):
        full_depth=selected+gap <= full_depth_q+EPS
        override=selected+gap >= release_q-EPS
        assert not (full_depth and override)

    # During extraction the lower dog guide (0..0.8) is already lost before
    # clearing tongue (2..2.8). For every z-error corner there is a finite
    # loaded overhung interval, independent of integration time-step.
    force_cases=[]; overhang_min=1e9
    for bias, alo, ahi, tz, lhi in product((-e,e),repeat=5):
        a=4.+bias+alo; b=4.8+bias+ahi
        low_top=.8+bias+lhi
        for c in (2.+tz,2.8+tz):
            overhang_min=min(overhang_min,2.+tz-low_top)
            ra,rb=reactions(a,b,c)
            assert ra < 0 < rb
            assert isclose(ra+rb,-1.)
            assert isclose(ra*a+rb*b,-c)
            amp=abs(ra)+abs(rb)
            for mu in (0.,.1,.3,.5,.7):
                # Tongue friction + the two opposing guide-face reactions.
                pull=mu*(1+amp)
                # Independent moment balance about lower bearing face:
                upper=(a-c)/(b-a)
                independent_pull=mu*(1+(1+upper)+upper)
                assert isclose(pull,independent_pull,abs_tol=EPS)
                finite_width=withdrawal(a,b,c,2.,mu,mu,mu)
                assert finite_width['ok'] and isclose(pull,finite_width['pull'])
                force_cases.append(dict(a=a,b=b,c=c,mu=mu,amplification=amp,pull_per_load=pull))
    assert overhang_min > 0
    nominal_ra,nominal_rb=reactions(4.,4.8,2.4)
    nominal_gain=.7*(1+abs(nominal_ra)+abs(nominal_rb))
    # Common translation cancels; both force and moment checks use relative z.
    translated=reactions(104.,104.8,102.4)
    assert all(isclose(a,b) for a,b in zip(translated,(nominal_ra,nominal_rb)))
    # Simply supported zero-friction and endpoint-load controls.
    assert reactions(0.,4.,0.) == (-1.,0.)
    assert reactions(0.,4.,2.) == (-.5,-.5)
    assert all(f['pull_per_load']==0 for f in force_cases if f['mu']==0)
    # Positive clearance after an INDEPENDENT extraction is geometrically
    # possible, but the existing closed fork obstructs that very motion.
    for i in range(513):
        s=4.5*i/512
        assert not any(dog(s,3.6).collides(w) for w in tongue())
    section_modulus=1.9**3/6
    bending=[dict(sigma=sigma,force_limit=sigma*section_modulus/2.3)
             for sigma in (5.,10.,20.)]
    # 2.3 = max upper-guide lower face 4.2 - min tongue load plane 1.9.
    worst=max(force_cases,key=lambda v:v['pull_per_load'])
    # Relax equal friction using bounded scenarios, not an invented prior.
    # In the adverse permitted geometry a/b/c=4.2/4.8/1.9, width=2.1.
    # Check independent coefficients and the singular boundary analytically.
    independent=[]
    for mt,ma,mb in product((0.,.1,.3,.5,.7),repeat=3):
        independent.append(withdrawal(4.2,4.8,1.9,2.1,mt,ma,mb))
    friction_jam=withdrawal(4.2,4.8,1.9,2.1,.3,0.,.7)
    assert not friction_jam['ok'] and friction_jam['denominator'] < 0
    near_singular=withdrawal(4.2,4.8,1.9,2.1,.3,.1,.67)
    assert near_singular['ok'] and near_singular['pull'] > 1000
    assert isclose(2*(4.8-4.2)/2.1,4/7)
    print(json.dumps(dict(
        evidence='finite rejection witnesses; self-review; no physical evidence',
        permanent_follower_straddle_margin=straddle_margin,
        finite_cam_vertex_margin=cam_margin,
        nominal_play_clearance=path_min, nominal_return_tongue_x=.8,
        nominal_jam_first_contact=contact, nominal_fork_lift_limit=fork_contact,
        jam_corner_cases=len(jam_cases),jam_first_contact_range=[min(v[0] for v in jam_cases),max(v[0] for v in jam_cases)],
        residual_disconnect_deficit=[min(v[1] for v in jam_cases),max(v[1] for v in jam_cases)],
        nominal_gap_max_full_depth=gap_max,nominal_gap_needed_escape=gap_needed,
        minimum_full_depth_overhung_extraction_interval=overhang_min,
        nominal_pull_per_load_mu07=nominal_gain,worst_pull_case=worst,
        force_corner_mu_cases=len(force_cases),bending_scenarios=bending,
        independent_friction_cases=len(independent),independent_friction_mode_failures=sum(not f['ok'] for f in independent),
        friction_jam=friction_jam,near_singular_pull_per_load=near_singular['pull'],
        repeated_lower_bound=dict(permanent_followers=6400,dogs=6400,collars=6400,
                                  dog_guide_lands=12800,permanent_follower_lands=12800),
        decision='reject closed captive command fork as an independent dog disconnect'
    ),indent=2))


if __name__ == '__main__':
    main()
