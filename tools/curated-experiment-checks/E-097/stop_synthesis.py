"""E-097: finite upright compression stops, mm/radians; no hardware claim.
Convex polygon prisms, deterministic bounds; no random process prior.
The full-bearing screen is sufficient, not a universal necessity for support.
"""
import itertools as it
import json
import math

PITCH = 5.08
N = 9
ALPHA = math.pi / N
LEVELS = tuple(5.0*i for i in range(N))


def rotate(poly, a):
    c, s = math.cos(a), math.sin(a)
    return [(c*x-s*y, s*x+c*y) for x, y in poly]


def cross(a, b, p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])


def clip(subject, boundary):
    """Convex CCW clipping; contact alone has zero area."""
    out = subject
    for a, b in zip(boundary, boundary[1:]+boundary[:1]):
        before, out = out, []
        if not before:
            break
        for p, q in zip(before, before[1:]+before[:1]):
            cp, cq = cross(a, b, p), cross(a, b, q)
            if cp >= -1e-12:
                out.append(p)
            if (cp > 0) != (cq > 0):
                t = cp/(cp-cq)
                out.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    return out


def area(poly):
    if not poly:
        return 0.0
    return abs(sum(x*v-y*u for (x,y),(u,v) in zip(poly,poly[1:]+poly[:1])))/2


def square(x, y, side):
    h = side/2
    return [(x-h,y-h),(x+h,y-h),(x+h,y+h),(x-h,y+h)]


def rect(x0, x1, y0, y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]


def overlap_volume(a, b):
    pa, za = a
    pb, zb = b
    dz = max(0, min(za[1],zb[1])-max(za[0],zb[0]))
    return dz*area(clip(pa,pb))


def sector(r, halfband=1.0, alpha=ALPHA):
    lo, hi = max(.2, r-halfband), r+halfband
    return [(lo*math.cos(alpha),-lo*math.sin(alpha)),
            (hi*math.cos(alpha),-hi*math.sin(alpha)),
            (hi*math.cos(alpha),hi*math.sin(alpha)),
            (lo*math.cos(alpha),lo*math.sin(alpha))]


def carousel(r, phase, halfband=1.0):
    # Upright prismatic sectors; connected by a base plate z=-3..0,
    # whose separate bearing/shaft and lock are not credited here.
    return [(rotate(sector(r,halfband),phase+2*ALPHA*j),(-2.0,h))
            for j,h in enumerate(LEVELS)]


def signed_clearance(foot, pad):
    return min(cross(a,b,p)/math.dist(a,b)
               for a,b in zip(pad,pad[1:]+pad[:1]) for p in foot)


def bearing_margin(r, side, e, phase_deg, subdivisions=64, halfband=1.0):
    """All relative XY datum corners ±2e; foot faces +.1, pad faces -.1.
    Phase is a continuous bounded uncertainty, not a qualified indexer.
    Lipschitz remainder bounds between angle samples; rotations preserve norms.
    """
    bound = math.radians(phase_deg)
    angles = [0.] if not bound else [-bound+2*bound*k/subdivisions
                                     for k in range(subdivisions+1)]
    worst = math.inf
    for a in angles:
        pad = rotate(sector(r,halfband), a)
        for dx,dy in it.product((-2*e,2*e), repeat=2):
            worst = min(worst, signed_clearance(square(r+dx,dy,side+.2),pad)-.1)
    # Distance to a rotating unit-normal edge changes at most |point| per rad.
    maxnorm = math.hypot(r+2*e+(side+.2)/2, 2*e+(side+.2)/2)
    remainder = maxnorm*bound/subdivisions if bound else 0.
    return worst-remainder


def staircase(b, target):
    return [(rect((j-target-.5)*b,(j-target+.5)*b,-1,1),(-2,h))
            for j,h in enumerate(LEVELS)]


def evaluate():
    # Parameter variants within TWO topologies, not distinct mechanisms.
    records=[]
    for r,band,side,e,angle in it.product((1.1,1.5,2.,3.,4.,5.),(1.,1.5,2.),(.6,1.2),(0.,.1,.2), (0.,2.,5.)):
        margin=bearing_margin(r,side,e,angle,halfband=band)
        # Full circular base plate radius r+band; independent rotor datums ±e
        # and outward radial edge error .1 on each rotor.
        adjacent_gap=PITCH-2*(r+band)-2*e-.2
        records.append(dict(radius=r,halfband=band,foot=side,datum=e,phase_deg=angle,
                            bearing_margin=round(margin,6),
                            same_plane_gap=round(adjacent_gap,6),
                            bearing_pass=margin>=.05,
                            pitch_pass=adjacent_gap>=.05))
    # Finite all-pair unloaded rotations with both motion directions. Rotation
    # only changes XY: z<=40.2 and elevated foot z>=43.8 proves entire paths.
    checks=0
    min_gap=43.8-40.2
    for old,new,direction in it.product(range(N),range(N),(-1,1)):
        steps=(direction*(new-old))%N
        for k in range(17):
            phase=-2*ALPHA*old-direction*2*ALPHA*steps*k/16
            for pad,z in carousel(3.,phase):
                assert overlap_volume((pad,(z[0],z[1]+.2)),
                                      (square(3,0,1.4),(43.8,103.8)))<1e-10
                checks+=1
    # Neighbor's low column is a real obstruction to long translating stairs.
    stair=staircase(2.,0)
    neighbor=(square(PITCH,0,.6),(0,60))
    stair_witness=sum(overlap_volume(s,neighbor) for s in stair)
    assert stair_witness>0
    # Small crown: a shifted low-state foot overlaps the high wraparound pad.
    foot=(square(1.1,-.4,.8),(0,60))
    crown_witness=overlap_volume(carousel(1.1,0)[8],foot)
    assert crown_witness>0
    # Finite grounded axial key in an outer index flange. The rotor's flange
    # occupies z=-6..-3, with a bridge plate above; radial trapezoid pockets
    # are through-cut. A 32-gon peg is at (4,0), nominal radius .3,
    # z=-7..-4. Withdrawal 4 mm downward clears the flange before rotation.
    # Axial retention, carrier and actuator are granted; angular lock fails
    # even with perfect retention. No need to generate those failed refinements.
    key_slot=sector(4.25,1.25,math.radians(16)) # radii 3..5.5
    def peg(rad,x=4.,y=0.):
        return [(x+rad*math.cos(2*math.pi*k/32),
                 y+rad*math.sin(2*math.pi*k/32)) for k in range(32)]
    # Circumscribed polygon contains the actual radius .4 bounded circular pin.
    insert=min(signed_clearance(peg(.4/math.cos(math.pi/32),4+dx,dy),key_slot)-.1
               for dx,dy in it.product((-.4,.4),repeat=2))
    assert insert>=.05
    # The nominal peg fits through every state along the 8-degree lost-motion
    # witness. A Lipschitz remainder covers intervals between angular samples.
    lock_min=min(signed_clearance(peg(.3/math.cos(math.pi/32)),rotate(key_slot,math.radians(k/2)))
                 for k in range(17)) - 4.31*math.radians(.25)
    assert lock_min>0
    drift_foot=(square(4,-.4,.8),(0,60))
    drift_collision=overlap_volume(carousel(4,math.radians(8),1.5)[8],drift_foot)
    assert drift_collision>0
    # Unlock/rotate/relock prescribed trajectory clears by 2 mm vertically;
    # inserted axial stroke stays in the nominal void (same XY polygon).
    flange=[(5.5*math.cos(2*math.pi*k/128),5.5*math.sin(2*math.pi*k/128))
            for k in range(128)]
    key_routes=0
    for leg in range(3):
        for k in range(17):
            t=k/16
            phase=0 if leg==0 else (2*ALPHA*t if leg==1 else 2*ALPHA)
            shift=-4*t if leg==0 else (-4 if leg==1 else -4*(1-t))
            key=(peg(.3/math.cos(math.pi/32)),(-7+shift,-4+shift))
            solid=overlap_volume((rotate(flange,phase),(-6,-3)),key)
            voids=sum(overlap_volume((rotate(key_slot,phase+j*2*ALPHA),(-6,-3)),key)
                      for j in range(N))
            assert abs(solid-voids)<1e-10
            key_routes+=1
    assert -4-4 < -6
    # Translating stair: all arbitrary endpoint transitions at elevated foot.
    stair_checks=0
    for old,new in it.product(range(N),repeat=2):
        for k in range(17):
            target=old+(new-old)*k/16
            for poly,z in staircase(2.,target):
                assert overlap_volume((poly,(z[0],z[1]+.2)),
                                      (square(0,0,.8),(43.8,103.8)))<1e-10
                stair_checks+=1
    # Maximum admissible phase error for a wider candidate: a specification
    # for a positive indexer, NOT a scalar replacement for an actual joint.
    index=[]
    for r in (3.,4.,5.):
        for e in (0.,.1,.2):
            lo,hi=0.,20.
            for _ in range(20):
                mid=(lo+hi)/2
                if bearing_margin(r,.6,e,mid,64,halfband=1.5)>=.05:lo=mid
                else:hi=mid
            index.append(dict(radius=r,datum=e,max_phase_deg=round(lo,4),
                              outer_radius=r+1.5))
    # Refinement holdouts: the conservative margin approaches sampled minimum.
    holdouts=[]
    for r,side,e,angle,band in ((1.1,.6,.2,2,1),(3.,.6,.2,2,1),(3.,.6,.2,5,1),(4.,.6,.2,5,1),(4.,.6,.2,2,1.5),(5.,.6,.2,5,1.5)):
        vals=[bearing_margin(r,side,e,angle,n,halfband=band) for n in (16,64,256)]
        assert vals[0]<=vals[1]+1e-10<=vals[2]+1e-10
        assert abs(vals[2]-vals[1])<.007
        holdouts.append(dict(params=(r,side,e,angle,band),margins=vals))
    # Independent exact nominal angular and radial face distances.
    r=3.; side=.6
    analytic=min(r*math.sin(ALPHA)-(side/2+.1)*(math.sin(ALPHA)+math.cos(ALPHA)),
                 (r+1)*math.cos(ALPHA)-r-(side/2+.1),
                 r-(side/2+.1)-(r-1)*math.cos(ALPHA))-.1
    assert abs(bearing_margin(r,side,0,0)-analytic)<1e-10
    assert abs(area(clip(square(0,0,2),square(1,0,2)))-2)<1e-12
    assert overlap_volume((square(0,0,2),(0,1)),(square(0,0,2),(1,2)))==0
    assert abs(sum(area(p) for p,_ in carousel(3,0))-
                   N*math.sin(2*ALPHA)*((3+1)**2-(3-1)**2)/2)<1e-10
    assert math.isclose(min_gap,3.6)
    return dict(parameter_cases=len(records),unloaded_prism_checks=checks,stair_prism_checks=stair_checks,
                key_route_states=key_routes,key_insertion_margin_mm=insert,key_8deg_route_margin_mm=lock_min,
                key_8deg_high_step_collision_mm3=drift_collision,
                continuous_vertical_gap_mm=min_gap,
                full_bearing_and_pitch_survivors=[x for x in records if x['bearing_pass'] and x['pitch_pass']],
                middle_bound_bearing_survivors=[x for x in records if x['bearing_pass'] and x['datum']==.2 and x['foot']==.6],
                nominal_small_crown_high_step_collision_mm3=crown_witness,
                nominal_stair_neighbor_collision_mm3=stair_witness,
                carousel_r4_band1_5_core_litres_6400=6400*sum(area(p)*(z[1]-z[0]) for p,z in carousel(4,0,1.5))/1e6,
                stair_b2_core_litres_6400=6400*sum(area(p)*(z[1]-z[0]) for p,z in staircase(2,0))/1e6,
                staircase_b2_material_length=18.,staircase_b2_swept_length=34.,
                admissible_index_error=index,refinement=holdouts)


if __name__=='__main__':
    print(json.dumps(evaluate(),indent=2))
