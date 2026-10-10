"""Finite support geometry rejection screen, mm/N/MPa; deterministic bounds.
No contact solver, manufacturing priors, dynamics or seal qualification.
Run directly; JSON is reproducible output and is intentionally not retained.
"""
from dataclasses import dataclass
from itertools import product
from math import sin, cos, tan, radians, sqrt, pi, isclose
import json

PITCH = 5.08
RISE = 2.5
ANGLE = radians(15)
LENGTH = 4.0  # beam sphere-center distance
PIN_RADIUS = .6
WEB = .6
TRACK_WIDTH = 2.0
FORK_SIDE_GAP = .2
FORK_WIDTH = TRACK_WIDTH + 2*(FORK_SIDE_GAP+WEB)
FORK_LENGTH = 2*(PIN_RADIUS+WEB)


@dataclass
class Box:
    name: str
    lo: tuple
    hi: tuple

    def overlap(self, other):
        return all(min(b,d)-max(a,c)>1e-9
                   for a,b,c,d in zip(self.lo,self.hi,other.lo,other.hi))


def box(name, x, y, z, dx, dy, dz):
    return Box(name, (x-dx/2,y-dy/2,z), (x+dx/2,y+dy/2,z+dz))


def groove(clearance, steps):
    """Closed straight slot translated -q: centerline z=base+tan(a)*(x+q).
    Pin at world x=0; low-flank contact z=base+t*q; upper adds c/cos(a).
    Slot is a capsule (centerline segment Minkowski sum disk radius r+c/2).
    End extensions exceed pin reach by 1 mm. Capsule outside web defines solid.
    Geometric gap checks distinguish contact, allowed free play and penetration.
    """
    t, ca = tan(ANGLE), cos(ANGLE)
    travel = RISE/t
    slot_radius = PIN_RADIUS+clearance/2
    center_base = 8+WEB+PIN_RADIUS+clearance/(2*ca)
    # Shift slot center so lower-flank pin center starts at this finite height.
    low_base = center_base-clearance/(2*ca)
    ext = 1.0 + slot_radius
    start = -ext
    end = travel+ext
    height = center_base+t*end+slot_radius+WEB
    minimum_gap = float('inf')
    sample_count = 0
    for i in range(steps+1):
        q = travel*i/steps
        # Include both driven flanks, free midpoint, and both stroke directions.
        for f in (0., .5, 1.):
            z = low_base+t*q+f*clearance/ca
            normal_offset = (z-center_base-t*q)*ca
            lower_gap = normal_offset+clearance/2
            upper_gap = clearance/2-normal_offset
            assert min(lower_gap, upper_gap) >= -1e-12
            if f in (0.,1.):
                assert abs(min(lower_gap,upper_gap)) < 1e-12
            # Project pin onto finite slot segment in the moving track frame.
            projection = (q+(z-center_base)*t)/(1+t*t)
            assert start < projection < end
            minimum_gap = min(minimum_gap,lower_gap,upper_gap)
            sample_count += 1
    # Worst-point extrema of the affine flanks are at stroke endpoints;
    # discretization only checks implementation, not a substitute for this bound.
    assert isclose((low_base+t*travel)-low_base,RISE)
    return dict(travel_mm=travel,normal_clearance_mm=clearance,
                reset_deadband_mm=clearance/ca,
                outer_height_mm=height,block_length_mm=end-start+2*(slot_radius+WEB),
                samples=sample_count,minimum_contact_gap_mm=minimum_gap)


def crossing(steps):
    """Finite conservative box envelopes for separate grounded support tiers.
    Local 3x3 periodic patch; rails extend across it. Every support is placed
    halfway between transverse rails; not at their geometric intersections.
    Rail bed/support depths are explicit allocations, not validated stiffness.
    Intentional shoe/rail and fork/slot contacts are handled separately.
    """
    a = sqrt(2)  # endpoints of a horizontal 4-mm diagonal beam
    rows = [-a+k*PITCH for k in (-1,0,1)]
    cols = [a+k*PITCH for k in (-1,0,1)]
    span = 4*PITCH
    tests = 0
    collision_witness = None
    # Tier allocations: row rail bottom 20, column bottom 48; each is 8 deep.
    # Column bed starts at 32; its grounded posts cross row tier in corridors.
    for ur,uc in product(range(steps+1),repeat=2):
        sr,sc = RISE*ur/steps,RISE*uc/steps
        rowrails=[box('row',0,y,20+sr,span,2,8) for y in rows]
        colrails=[box('column',x,0,48+sc,2,span,8) for x in cols]
        # Fixed support posts below upper ground bed. Rectangular footprint
        # wide across column, short along it, matching the capture-fork envelope.
        upperposts=[box('upper bed post',x, -a+PITCH/2,0,
                        FORK_WIDTH,FORK_LENGTH,32) for x in cols]
        # Actual fork side arms, not its solid bounding box. Row fork wraps
        # the 2-mm row track with .2 clearance and .6-mm walls. Its fixed x
        # station is in the transverse-column corridor. Upper posts already
        # occupy the lower tier: this can collide despite rail-only clearance.
        fork_x=a-PITCH/2
        rowarms=[box('row fork arm',fork_x,y+sign*(TRACK_WIDTH/2+FORK_SIDE_GAP+WEB/2),
                     9.2+sr,FORK_LENGTH,WEB,10.8)
                 for y in rows for sign in (-1,1)]
        for arm,post in product(rowarms,upperposts):
            if arm.overlap(post) and collision_witness is None:
                collision_witness=dict(row_lift_mm=sr,column_lift_mm=sc,
                    arm_lo=arm.lo,arm_hi=arm.hi,post_lo=post.lo,post_hi=post.hi,
                    penetration_xyz_mm=[min(b,d)-max(a,c) for a,b,c,d in
                        zip(arm.lo,arm.hi,post.lo,post.hi)])
        # Row risers must pass the upper column tier to lift the endpoint pad.
        rowrisers=[box('row shoe riser',-a,y,28+sr,1.6,1.6,34) for y in rows]
        for left,right in ((rowrails,colrails),(upperposts,rowrails),(rowrisers,colrails)):
            for u,v in product(left,right):
                assert not u.overlap(v), (u.name,v.name,sr,sc)
                tests += 1
    # Adjacent row support forks can coexist: transverse width 3.6 < pitch.
    # Upper posts corridor has 0.34 nominal edge clearance; two independent
    # +/-0.1 location/size envelope expansions leave 0.14 mm, not a fit prior.
    corridor_gap=(PITCH-2-FORK_LENGTH)/2
    assert corridor_gap-2*.1 > 0
    # Collision witness prevents the test from granting support at intersections.
    assert box('bad support',a,-a,0,FORK_WIDTH,FORK_LENGTH,32).overlap(
        box('row',0,-a,20,span,2,8))
    assert collision_witness is not None
    return dict(box_pair_tests=tests,corridor_edge_gap_mm=corridor_gap,
                fork_post_collision=collision_witness,
                accepted_crossing=False,
                edge_gap_after_two_point1_bounds_mm=corridor_gap-.2,
                neighboring_fork_gap_mm=PITCH-FORK_WIDTH,
                selector_top_mm=66.,
                excludes=['bed bending','lateral frame ties','valve/manifold',
                          'guide details','full-board edge drives','manufacturing fit'])


def beam_sweep(steps):
    """Capsule beam: endpoint balls r=.25, center ball r=.4; pads underneath.
    Pad contact uses sphere bottoms: finite beam thickness does not alter mean
    endpoint-center height. An anti-yaw guide is assumed, not synthesized here.
    Radius-.4 capsule bounds the smaller beam and all three contact spheres.
    Pad size is generated from full bounded endpoint travel, including errors.
    """
    e = .1
    max_dz = RISE+2*e
    slide = (LENGTH-sqrt(LENGTH**2-max_dz**2))/2
    r = .25
    # square pad spans inward travel in x and y plus .25 ball contact radius
    pad_size = slide/sqrt(2)+2*r+.2
    min_cover = float('inf')
    tests = 0
    for i,j,ea,eb in product(range(steps+1),range(steps+1),(-e,e),(-e,e)):
        za,zb = RISE*i/steps+ea,RISE*j/steps+eb
        h = sqrt(LENGTH**2-(za-zb)**2)
        ends=[(-h/(2*sqrt(2)),-h/(2*sqrt(2)),za),
              (h/(2*sqrt(2)),h/(2*sqrt(2)),zb)]
        assert isclose(sum((ends[0][k]-ends[1][k])**2 for k in range(3)),LENGTH**2)
        for sign,p in zip((-1,1),ends):
            center = sign*(LENGTH/2-slide/2)/sqrt(2)
            # Ball's complete footprint retained; true Hertz contact smaller.
            cover = pad_size/2-max(abs(p[0]-center),abs(p[1]-center))-r
            min_cover=min(min_cover,cover)
            assert cover >= -1e-12
        # Capsule box cannot hit neighboring translated beam capsule boxes.
        extent = h/sqrt(2)+.8
        assert extent < PITCH
        tests+=1
    return dict(states=tests,slide_per_end_mm=slide,pad_side_mm=pad_size,
                min_pad_coverage_mm=min_cover,minimum_neighbor_box_gap_mm=PITCH-(LENGTH/sqrt(2)+.8),
                pad_edge_allowance_mm=.1,reset_retention_not_generated=True)


def reset_bounds(clearance):
    # Preserve E-061 e=eg=.1, f=.2; ramp elasticity belongs inside f, not extra.
    deadband=clearance/cos(ANGLE)
    # Low can lag on the upper flank during forced return. Controlled rise
    # requires verified downward preload/no upward stiction energy at high.
    directed_half_clearance=1.6-.1-(RISE/2+.1+deadband/2)
    unrestricted_half_clearance=1.6-.1-(RISE/2+.1+deadband)
    return dict(clearance_mm=clearance,reset_lag_mm=deadband,
                half_clearance_directed_mm=directed_half_clearance,
                half_clearance_both_flanks_mm=unrestricted_half_clearance,
                min_selected_lift_mm=RISE-.1-(1.6+.1)-.2,
                max_selected_lift_both_flanks_mm=RISE+.1+deadband-(1.6-.1))


def rotary():
    """Necessary radial-cam envelope, including staggered neighboring shafts.
    Coaxial cam bore radius r, minimum web w; radial rise s forces R>=r+w+s.
    Disjoint coplanar swept lanes require 2R<=pitch. Staggered disks still must clear adjacent shafts:
    R+r<=pitch -> d<=pitch-web-rise. Radial groove dwell is not yet generated.
    """
    web=.6
    dmax=PITCH-web-RISE
    d=2.
    R=d/2+web+RISE
    # Comparison ONLY: uniform dense load, constant rise over pi radians.
    # A real dwell/rise cam requires higher maximum slope than this mean.
    load=40*(.1+(1.5*pi/4+1)/2)
    torque=load*RISE/pi
    length=40*PITCH
    scenarios=[]
    for G in (200.,600.,1200.):
        J=pi*dmax**4/32
        lag=torque*length/(2*G*J)
        scenarios.append(dict(G_MPa=G,mean_slope_twist_rad=lag,
            diameter_for_30deg_twist_mm=(torque*length/(2*G*(pi/6)) *32/pi)**.25))
    return dict(reference_shaft_diameter_mm=d,radial_sweep_radius_mm=R,
        co_phased_swept_lane_overlap_mm=2*R-PITCH,
        staggered_disk_to_neighbor_shaft_overlap_mm=R+d/2-PITCH,
        max_staggered_shaft_diameter_zero_clearance_mm=dmax,
        mean_rise_torque_Nmm=torque,twist=scenarios,
        conclusion='external-profile swept-lane screen only; staggered <=1.98-mm shaft unresolved',
        caveat='twist diagnostic is NOT a no-reach proof: dwells unload elastic shaft')


def captured_rotary():
    """A finite radial closed-groove cam with low/high dwells and two rises.
    Centerline is generated in polar coordinates, rlow=shaft_r+web+slot_r.
    Two 60-degree dwells; smooth half-cosine rise/fall over 120 degrees each.
    Web outside the high dwell is an exact annular sector; witness rotates it
    toward the neighboring shaft midway through a commanded half-turn.
    Groove offset/roller compatibility on the rise is NOT accepted: the exact
    dwell-wall collision already rejects this coplanar-axis layout.
    """
    clearance=.2
    slot_r=PIN_RADIUS+clearance/2
    rows=[]
    for shaft_d in (0.,1.,2.):
        shaft_r=shaft_d/2
        low=shaft_r+WEB+slot_r
        centers=[]
        for i in range(721):
            theta=2*pi*i/720
            # High dwell centered at pi/2; low at 3*pi/2.
            distance=abs((theta-pi/2+pi)%(2*pi)-pi)
            if distance<=pi/6:
                lift=RISE
            elif distance>=5*pi/6:
                lift=0.
            else:
                lift=RISE*(1+cos((distance-pi/6)*1.5))/2
            r=low+lift
            centers.append((r*cos(theta),r*sin(theta)))
        high=low+RISE
        assert isclose(centers[180][1],high)
        # Rotate -pi/2: high-dwell outer web lies on +x axis.
        web_inner=high+slot_r
        web_outer=web_inner+WEB
        near=PITCH-shaft_r
        far=PITCH+shaft_r
        overlap=min(web_outer,far)-max(web_inner,near)
        if shaft_d==0:
            assert web_inner < PITCH < web_outer  # degenerate shaft limit
        else:
            assert overlap>0
        rows.append(dict(shaft_d_mm=shaft_d,outer_radius_mm=web_outer,
                         neighbor_center_inside_web=web_inner<PITCH<web_outer,
                         radial_overlap_mm=max(0.,overlap),centerline_points=len(centers)))
    return dict(witnesses=rows,
        shaft_diameter_bound_mm=PITCH-2*WEB-2*PIN_RADIUS-clearance-RISE,
        conclusion='reject captured radial groove with coplanar neighboring shafts, even staggered disks',
        reopening='different axis tiers, outboard followers, smaller stroke/contact package, or changed reset topology')


def riser_bounds():
    force=.1+(1.5*pi/4+1)/2
    length=34.
    out=[]
    for E in (500.,1500.,3000.):
        b=1.6
        I=b**4/12
        out.append(dict(E_MPa=E,axial_loss_mm=force*length/(E*b*b),
                        ideal_pinned_buckling_N=pi*pi*E*I/length**2))
    return dict(load_N=force,width_mm=1.6,length_mm=length,scenarios=out,
                caveat='ideal straight pinned strut; no strength, guide or creep qualification')

def main():
    # Straight-contact refinement: sampled checks must preserve exact extrema.
    for c in (.1,.2,.3):
        a,b=groove(c,32),groove(c,128)
        assert isclose(a['reset_deadband_mm'],b['reset_deadband_mm'])
    assert groove(0,4)['reset_deadband_mm']==0
    assert reset_bounds(0)['half_clearance_directed_mm']>.149999
    assert reset_bounds(.3)['half_clearance_directed_mm']<0
    assert reset_bounds(.2)['half_clearance_both_flanks_mm']<0
    result=dict(grooves=[groove(c,128) for c in (.1,.2,.3)],
                crossing=crossing(16),beam=beam_sweep(32),
                reset=[reset_bounds(c) for c in (0,.1,.2,.3)],
                clearance_limits_mm=dict(directed=.3*cos(ANGLE),both_flanks=.15*cos(ANGLE)),
                rotary=rotary(),captured_rotary=captured_rotary(),riser=riser_bounds(),
                evidence='finite geometric envelopes + analytic bounds; self-review; no machine acceptance')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
