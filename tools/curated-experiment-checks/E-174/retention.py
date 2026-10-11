"""E-174: finite lane-dog guide and clearance-index counterexamples.
mm, N, seconds. Deterministic rigid geometry/bounds, not a calibrated process.
Run from any directory; standard library. JSON output is disposable.
"""
import itertools as it
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-173'))
import lanes


def rectangle(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def rotate(poly, theta, pivot):
    c, s = math.cos(theta), math.sin(theta)
    return [(pivot[0]+c*(x-pivot[0])-s*(z-pivot[1]),
             pivot[1]+s*(x-pivot[0])+c*(z-pivot[1])) for x, z in poly]


def intersects(a, b):
    """Strict convex-polygon intersection, separating-axis theorem; no mesh."""
    for p in (a, b):
        for u, v in zip(p, p[1:]+p[:1]):
            n = (u[1]-v[1], v[0]-u[0])
            aa = [n[0]*x+n[1]*z for x, z in a]
            bb = [n[0]*x+n[1]*z for x, z in b]
            if min(max(aa), max(bb))-max(min(aa), min(bb)) <= 1e-10:
                return False
    return True


def root(f, lo=0., hi=.7):
    assert f(lo) <= 0 < f(hi)
    for _ in range(70):
        mid = (lo+hi)/2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo+hi)/2


def guide(length=1.8, height=5., gap=.2, spine_edge=.6):
    """Dog nose, descending tail and bottom carriage form one connected union.
    Floor x=[2.05,3.85], roof x=[2.85,3.85]. X registration is granted.
    Roof angle is an angular-play limit, NOT a predicted loaded trajectory.
    """
    pivot = (2.05, -height)
    nose = rectangle(1.2, 2.65, -1, 0)
    tail = rectangle(2.05, 2.65, -height, -.8)
    carriage = rectangle(2.05, 2.05+length, -height, -height+1)
    theta = root(lambda t: length*math.sin(t)+math.cos(t)-(1+gap))
    bodies = [rotate(p, theta, pivot) for p in (nose, tail, carriage)]
    spine = rectangle(-.6, spine_edge, -41.4, 94.4)
    collision = any(intersects(p, spine) for p in bodies)
    # The nose's upper inner corner is the first point reaching the spine.
    first = root(lambda t: spine_edge-(2.05-.85*math.cos(t)-height*math.sin(t)))
    roof_x = 2.05+length*math.cos(theta)-math.sin(theta)
    roof_contact_exists = 2.85 < roof_x < 3.85
    roof_remaining = 1+gap-(length*math.sin(first)+math.cos(first))
    # Hypothetical VERTICAL pressure, not the actual tilted-face contact law.
    reactions = []
    for x, force in it.product((1.2, 1.8), (.1, 1., 10.)):
        down = force*(2.05-x)/(roof_x-2.05)
        up = force+down
        assert up > 0 and down > 0
        assert abs(up-down-force) < 1e-12
        assert abs(down*(roof_x-2.05)-force*(2.05-x)) < 1e-12
        reactions.append((force, x, up, down))
    # A small explicit overtravel past first contact produces real area overlap.
    witness = rotate(nose, first+.001, pivot)
    assert intersects(witness, spine)
    # Independent contact holdout: horizontal tooth underside's RIGHT corner
    # bears on the tilted dog plane. Normal force on dog is (F*tan(t),-F).
    # About an X-registered bottom corner its moment vanishes when
    # (pivot_x-tooth_x)=H*sin(t). The lateral grounding reaction is a GRANT;
    # the two horizontal shelves do not by themselves construct this bearing.
    normal_t = math.asin((2.05-1.8)/height)
    contact_z = (1.8-2.05)*math.tan(normal_t)+height/math.cos(normal_t)
    normal_moment = (2.05-1.8)-contact_z*math.tan(normal_t)
    assert abs(normal_moment) < 1e-12
    normal_bodies = [rotate(p, normal_t, pivot) for p in (nose,tail,carriage)]
    assert not any(intersects(p,spine) for p in normal_bodies)
    tooth = rectangle(.2,1.8,contact_z-height,contact_z-height+1.2)
    assert not any(intersects(p,tooth) for p in normal_bodies)
    # Lowering that exact tooth makes contact, rather than leaving a gap.
    lowered_tooth = [(x,z-.0001) for x,z in tooth]
    assert intersects(normal_bodies[0],lowered_tooth)
    return dict(length=length, height=height, gap=gap,
                free_angle_deg=math.degrees(theta), first_spine_deg=math.degrees(first),
                roof_contact_exists=roof_contact_exists,
                spine_collision=collision, nose_min_x=min(x for x,z in bodies[0]),
                roof_gap_at_spine=roof_remaining, vertical_force_reactions=reactions,
                normal_equilibrium_deg=math.degrees(normal_t),
                normal_horizontal_force_ratio=math.tan(normal_t),
                normal_nose_min_x=min(x for x,z in normal_bodies[0]))


def index_bounds(e, amplification=1., follower=False):
    """Clearance peg: .05 insertion reserve, ±e datum and ±e face per part.
    d=(slot-pin)/2 >= 4e+.05. At opposite errors free travel is d+4e.
    Amplified variant grants exact r=A*q except explicit diagonal follower.
    """
    reserve = .05
    d = 4*e+reserve
    slot = .3+2*d
    drift = (d+4*e)/amplification
    # Same insertion bound on cam normal clearance. Project normal free play
    # onto Y for a slot centreline q=r/A; normal_y=A/sqrt(A*A+1).
    follower_drift = (d+4*e)*math.sqrt(1+1/amplification**2) if follower else 0
    return dict(e=e, A=amplification, pin=.3, slot=slot,
                web=.9*amplification-slot-2*e,
                drift=drift+follower_drift, ideal_link_drift=drift)


def finite_index():
    """Five fixed slots, one slider peg; capture and release are finite boxes.
    X-long slots deliberately do not act as an uncounted pitch key.
    """
    pin=.3; slot=.8; e=.05
    # Adverse but simultaneous legal corner: slot datum+.05, edge+.05;
    # peg datum-.05, edge recession .05. Resulting permitted q=[-.25,.45].
    holes = [(y-slot/2, y+slot/2+2*e) if i==2 else (y-.3,y+.4)
             for i,y in enumerate(lanes.LANES)]
    # left hole edge: datum+.05 minus expansion .05 => nominal left edge.
    walls=[]
    edges=[-2.5]+[x for hole in holes for x in hole]+[2.5]
    for a,b in zip(edges[::2], edges[1::2]):
        if b>a: walls.append(lanes.box((2.8,3.8),(a,b),(-8,-7.5)))
    def peg(q, dz=0.):
        return lanes.box((3.,3.5),(q-.15,q+.05),(-8.2+dz,-7.3+dz))
    # Tooth/dog faces remain nominal: joint error is not spent twice.
    poses=0
    for old,new in it.product(range(5),repeat=2):
        q0,q1=lanes.LANES[old],lanes.LANES[new]
        for q,dz in ([(q0,k*.05) for k in range(21)] +
                     [(q0+(q1-q0)*k/64,1.) for k in range(65)] +
                     [(q1,1-k*.05) for k in range(21)]):
            assert all(lanes.volume(peg(q,dz),wall)<1e-10 for wall in walls)
            poses+=1
    # .44 is reachable with peg still fully inserted; it is not commanded q.
    drift=.44
    assert all(lanes.volume(peg(drift),wall)==0 for wall in walls)
    assert any(lanes.volume(peg(.46),wall)>0 for wall in walls)
    h=lanes.supported_height(drift,(0.,)*5,0.)
    assert math.isclose(h,3*lanes.P)
    column,dog,_=lanes.solids(h-.05,drift,-2.,1.7,(0.,)*5,0.,1.)
    penetration=lanes.volume(column[4],dog)
    assert math.isclose(penetration,.6*.04*.05,abs_tol=1e-10)
    return dict(transition_poses=poses, drift=drift, actual_height=h,
                target_height=2*lanes.P, wrong_tooth_mm3=penetration,
                pin_withdrawal_mm=1., witness_minimum_web_mm=.1,
                bound_minimum_web_mm=0.)


def writer_access():
    # Previous column's nominal roof is immediately below this column's pad.
    # Rigid rails are grounded grants; adding their attachments cannot erase
    # this existing collision. This rejects the straight underside route only.
    roof=lanes.box((2.85-5.08,3.85-5.08),(-2.3,2.3),(-3.8,-3.4))
    finger=lanes.box((-2.15,-1.35),(-.35,.35),(-4.2,-3.))
    collision=lanes.volume(roof,finger)
    assert math.isclose(collision,.224,abs_tol=1e-10)
    # Same obstruction with the pad clear, before activation.
    clear_finger=lanes.box(finger[0],(1.7-.35,1.7+.35),finger[2])
    assert math.isclose(lanes.volume(roof,clear_finger),collision)
    return dict(underside_finger_roof_mm3=collision,
                nominal_roof_pad_gap=.4, bounded_gap=.2,
                assumed_finger_thickness=.4)


def main():
    # SAT limiting cases independent of the application.
    a=rectangle(0,1,0,1)
    assert not intersects(a,rectangle(1,2,0,1))
    assert intersects(a,rectangle(.999,2,0,1))
    assert intersects(rotate(a,.1,(0,0)),a)
    nominal=guide()
    adverse=guide(gap=.4)
    assert not nominal['spine_collision'] and adverse['spine_collision']
    # Continuous monotonic lower bound uses longest carriage and shortest tail.
    # This grid is a holdout, not a proof of every possible guide architecture.
    cases=[guide(L,H,.4) for L,H in it.product((1.2,1.4,1.6,1.8),(5.,6.,8.,10.))]
    assert all(c['spine_collision'] for c in cases)
    # H increases leftward displacement; shorter L increases angle on this root.
    assert all(c['nose_min_x'] <= adverse['nose_min_x']+1e-10 for c in cases)
    theta_safe=math.radians(adverse['first_spine_deg'])
    required_L=(1.4-math.cos(theta_safe))/math.sin(theta_safe)
    long_carriage=lanes.box((2.05,2.05+required_L),(-.5,.5),(-5.,-4.))
    low_neighbor_spine=lanes.box((5.08-.6,5.08+.6),(-2.3,2.3),(-41.4,50.))
    repair_collision=lanes.volume(long_carriage,low_neighbor_spine)
    assert repair_collision > .9
    # Writer force figures are explicit parameter sensitivities, no material prior.
    force_rows=[]
    for F,mu,ratio in it.product((.1,1.,10.),(.1,.3,.6),(0.,.1,.3)):
        H=ratio*F
        preload=.05
        force_rows.append(dict(F=F,mu=mu,H=H,
            keeper_release=preload+mu*H,
            unloaded_release=preload))
    slots={w:lanes.evaluate(4,word=w) for w in (.5,.8,1.)}
    # Added bank-wide access traverse: generous collision-free grant only.
    mv=lanes.control.r.move
    access=2*(2*mv(43.)+mv(5.08))
    out=dict(guide_nominal=nominal,guide_adverse=adverse,
             guide_variants=len(cases), required_length_at_H5=required_L,
             lengthened_carriage_neighbor_mm3=repair_collision,
             index=finite_index(),writer_access=writer_access(),
             indexing=[index_bounds(e,A,f) | {'diagonal_follower':f}
                       for e,A,f in it.product((.025,.05,.075),(1,2,4,8),(False,True))],
             release_force_bounds=force_rows,
             timing_B4=slots, granted_access_seconds=access,
             B4_word05_with_granted_access=slots[.5]+access,
             bundles=dict(shared_grant=328,shared_two_extra_bank_axes=336,
                          split=652,separate_B8=656,direct_B4=324))
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
