#!/usr/bin/env python3
"""Finite frame/return exclusion, mm N MPa. Deterministic design bounds only.
No fitted material priors, contact solution, hardware qualification or yield.
"""
import importlib.util
import json
from itertools import product
from math import pi, sqrt, hypot, isclose
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tiered_support', ROOT/'E-102/tiered_support.py')
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
P = old.P
EPS = .1  # expansion of EACH opposing solid: bound, not measured tolerance
VALVE = (1.5*pi/4+1)/2
DENSE = 8*(.1+VALVE)
SPARSE = 8*.1+VALVE


def intersection(a, b):
    lengths = [min(u,v)-max(x,y) for x,u,y,v in zip(a.lo,a.hi,b.lo,b.hi)]
    return dict(a_lo=a.lo,a_hi=a.hi,b_lo=b.lo,b_hi=b.hi,
                overlap_mm=lengths,solid_collision=min(lengths)>0)


def frame(fork_width):
    """Changed follower: two 1.2-mm axial cheeks, variable transverse width.
    Finite guide portal above cams; clear window follows cheek envelope.
    Two feet sit atop the own bearing housings, carrying portal to those
    housings/necks and ground. It braces laterally, NOT a replacement axial
    load path. No guide fixity is credited to buckling/deflection acceptance.
    z=26..28 header clears high-tier swept cam top 24.6 and rail bottom 29.8.
    Test actual portal solids against the inherited upper-family ground necks.
    This selected-pair test is deliberately not an all-part clearance test.
    """
    x=P/2
    cheek_x=1.4  # .6 cam half-width + .2 gap + .6 cheek half-width
    inner_x=cheek_x+.6+.2
    inner_y=fork_width/2+.2
    wall=.6
    # Header runs to feet at x +/-pitch; leave central rectangular aperture.
    reach=P+.6
    bodies=[]
    for side in (-1,1):
        bodies.append(old.box('guide transverse wall',
            (x,side*(inner_y+wall/2),27), (2*reach,wall,2)))
        bodies.append(old.box('guide end wall',
            (x+side*(inner_x+(reach-inner_x)/2),0,27),
            (reach-inner_x,2*inner_y,2)))
        # Feet start at top of low-tier bearing envelope z=12.6.
        bodies.append(old.box('portal foot',(x+side*P,0,(12.6+26)/2),
                              (1.2,1.6,26-12.6)))
    # One real upper neck at x=0, y=half pitch is enough for a witness.
    # Full local lattice includes both +/- half-pitch neighbors.
    necks=[old.box('upper ground neck',
                   (i*P,(.5+2*(i%4))*P+k*8*P+side*P,55.4/2),
                   (1.6,1.2,55.4))
           for i,k,side in product(range(-2,4),range(-1,2),(-1,1))]
    witness=None
    gap=float('inf')
    for a,b in product(bodies,necks):
        gap=min(gap,max(a.gaps(b)))
        if a.collision(b) and witness is None:
            witness=intersection(a,b)
    assert 26-(18+old.R)>2*EPS
    assert (30-.2)-28>2*EPS
    return dict(fork_width_mm=fork_width,portal_solids=len(bodies),
                neck_checks=len(bodies)*len(necks),min_neck_separating_gap_mm=gap,
                actual_collision=witness,
                scope='finite portal/upper-neck subset; not complete crossing or guide contact')


def rail_loss(loads,E,G):
    """Midspan bending via exact simply-supported point-load Green function;
    shear via virtual work, kappa=5/6, constant 2x8-mm rectangular rail.
    This is a conditional reference load split, not contact redistribution.
    """
    L=8*P; x=L/2; I=2*8**3/12; A=2*8
    bending=0
    for a,F in loads:
        xx,aa=(x,a) if x<=a else (L-x,L-a)
        bending+=F*(L-aa)*xx*(L*L-(L-aa)**2-xx*xx)/(6*L*E*I)
    points=sorted(set([0,x,L]+[a for a,F in loads]))
    left=sum(F*(L-a)/L for a,F in loads)
    shear=0
    for lo,hi in zip(points,points[1:]):
        mid=(lo+hi)/2
        V=left-sum(F for a,F in loads if a<mid)
        unit=.5 if mid<x else -.5
        shear+=V*unit*(hi-lo)/((5/6)*G*A)
    return bending,shear


def mechanics():
    """Reference series-path displacement envelope: rigid guides/frame ties and
    zero contact indentation. Retain actual neck axial, local shaft bending,
    pin bending/shear, fork axial and rail bending/shear. Missing frame bending,
    fit and contact terms are nonnegative in this assumed series path;
    this is NOT a rigorous lower bound: finite pin contact, shaft continuity and
    load redistribution change the terms. No survivor is accepted. E/G are independent
    scenario allocations, not an isotropic or calibrated PLA law.
    """
    out=[]
    for E,G in ((500,200),(1500,600),(3000,1200)):
        for name,F in (('dense row',DENSE),('sparse column',SPARSE)):
            loads=[((i+.5)*P,.1+(VALVE if name=='dense row' else 0)) for i in range(8)]
            if name=='sparse column': loads.append((4*P,VALVE))
            rb,rs=rail_loss(loads,E,G)
            # The worst row-fork and row-neck lengths belong to DIFFERENT tiers.
            variants=[]
            for tier in (10,18):
                fork_L=30-(tier+2.8)
                neck_L=tier-2.6 if name=='dense row' else tier+40-2.6
                fork_ax=F*fork_L/(2*E*1.2*1.6)
                neck_ax=F*neck_L/(2*E*1.2*1.6)
                shaft=F*(2*P)**3/(48*E*(pi*3**4/64))
                pin_b=F*2.8**3/(48*E*(pi*1.2**4/64))
                pin_s=F*2.8/(4*.9*G*(pi*1.2**2/4))
                total=rb+rs+fork_ax+neck_ax+shaft+pin_b+pin_s
                weak_I=1.6*1.2**3/12
                pinned=2*pi*pi*E*weak_I/fork_L**2
                variants.append(dict(tier_z_mm=tier,
                    losses_mm=dict(rail_bending=rb,rail_shear=rs,fork_axial=fork_ax,
                        neck_axial=neck_ax,shaft_bending=shaft,pin_bending=pin_b,pin_shear=pin_s),
                    subtotal_mm=total,unbraced_pair_pinned_capacity_N=pinned))
            out.append(dict(path=name,E_MPa=E,G_MPa=G,load_N=F,variants=variants))
    # Independent exact midpoint concentrated-load identities including shear.
    b,s=rail_loss([(4*P,1)],1500,600)
    assert isclose(b,(8*P)**3/(48*1500*(2*8**3/12)))
    assert isclose(s,8*P/(4*(5/6)*600*16))
    # End load has zero bending/shear; linear scaling and reciprocity of averaging.
    assert all(abs(v)<1e-12 for v in rail_loss([(0,1)],500,200))
    # Offset row riser reaches from row rail top 38 to floor underside 84.
    # Column riser reaches 78..84. Both are 1.6 square. Contact point moves
    # along the diagonal; evaluate endpoints of its convex eccentricity norm.
    # Whole-transition eccentricity + full selected load is a conservative
    # envelope, not a claim that these extrema occur together.
    a=sqrt(2); slide=(4-sqrt(4**2-3.1**2))/2/sqrt(2)
    row_ex=a-P/2
    row_e2=max(((-a+t)-row_ex)**2+t*t for t in (0,slide))
    col_e2=2*slide*slide
    means=[]
    for E in (500,1500,3000):
        cases=[r for r in out if r['E_MPa']==E]
        mean=sum(max(v['subtotal_mm'] for v in r['variants']) for r in cases)/2
        # Fixed-base, unbraced eccentric-column linear formula: F L/EA +
        # F e^2 L/EI. Formal only; stability and contact are not guaranteed.
        risers=[(VALVE+.1)*L/E*(1/1.6**2+e2/(1.6**4/12))
                for L,e2 in ((46,row_e2),(6,col_e2))]
        mean+=sum(risers)/2
        means.append(dict(E_MPa=E,formal_row_column_riser_losses_mm=risers,
                          center_loss_subtotal_mm=mean,
                          residual_inside_inherited_point2_mm=.2-mean,
                          selected_lift_with_zero_other_loss_mm=.7-mean))
    assert isclose(means[0]['center_loss_subtotal_mm']/means[2]['center_loss_subtotal_mm'],6)
    return dict(scenarios=out,center_mean=means,
                omitted='frame/housing/contact/beam/stem losses; eccentric/guided stability; redistribution')


def capture():
    """Axis-aligned square captured-ball shoes; rods leave inward through a
    roof slot. Floors are finite SOLIDS. Opposing dimensional errors are each +/-EPS;
    clearance uses expansion, retention uses sphere shrink/aperture growth.
    At a roof section crossing the neck, necessary aperture half-width q must
    satisfy q >= neck_radius+2EPS and q <= ball_radius-2EPS to retain ball.
    Real tilted-neck aperture may be worse; these necessary bounds suffice.
    A .1 radial internal pocket gap and .4/.6 walls are design allocations.
    Both diagonal neighboring shoes are at the same z in 00, so overlapping
    floors are a genuine material collision, not swept-box overconservatism.
    """
    neck=.15; lateral_gap=.1
    # Displaced pad center covers inward ball slide, including cam+shoe reset lag.
    max_dz=2.5+2*.1+.4
    slide=(4-sqrt(4**2-max_dz**2))/2
    a=sqrt(2); projected_slide=slide/sqrt(2)
    center=a-projected_slide/2
    rows=[]
    for radius,wall in product((.25,.4,.55,.6),(.4,.6)):
        half_aperture_min=neck+2*EPS
        half_aperture_max=radius-2*EPS
        side=projected_slide+2*(radius+lateral_gap+wall)
        floor1=old.box('positive end floor',(center,center,0),(side,side,.6))
        floor2=old.box('diagonal neighbor negative end floor',
                       (P-center,P-center,0),(side,side,.6))
        nominal_gap=max(floor1.gaps(floor2))
        # z overlap is intentional test setup; max gaps is thus XY separation.
        algebraic=P-2*a-2*(radius+lateral_gap+wall)
        assert isclose(nominal_gap,algebraic,abs_tol=1e-12)
        rows.append(dict(ball_radius_mm=radius,wall_mm=wall,
            aperture_half_interval_mm=[half_aperture_min,half_aperture_max],
            aperture_possible=half_aperture_min<=half_aperture_max+1e-12,
            floor_side_mm=side,floor_gap_mm=nominal_gap,
            expanded_floor_gap_mm=nominal_gap-2*EPS,
            packing_possible=nominal_gap>=2*EPS,
            collision=intersection(floor1,floor2)))
    assert not any(r['aperture_possible'] and r['packing_possible'] for r in rows)
    # Inverse bounds exclude the CONTINUOUS radius family, not just sample grid.
    bounds=[]
    for wall in (.4,.6):
        rmin=neck+4*EPS
        rmax=(P-2*EPS)/2-a-lateral_gap-wall
        assert rmax<rmin
        bounds.append(dict(wall_mm=wall,r_min_capture_mm=rmin,r_max_packing_mm=rmax,
                           empty_interval_mm=rmin-rmax))
    # Zero-error control must admit a design, so the generator is not tautologically rejecting.
    nominal_r=.25; nominal_q=.2
    assert neck<nominal_q<nominal_r
    assert P-2*a-2*(nominal_r+lateral_gap+.4)>0
    riser=old.box('rerouted row riser',(a-P/2,-a,61),(1.6,1.6,46))
    # A finite cap below the floor joins riser to the negative shoe center.
    cap=old.box('offset cap',((a-P/2-center)/2,(-a-center)/2,83.7),
                (abs(a-P/2+center)+1.6,abs(a-center)+1.6,.6))
    assert riser.collision(cap)
    assert isclose(P/2-1.5-.8-2*EPS,.04)
    return dict(max_dz_mm=max_dz,slide_mm=slide,scenarios=rows,inverse_bounds=bounds,
                offset_riser=dict(lo=riser.lo,hi=riser.hi,cap_lo=cap.lo,cap_hi=cap.hi,
                    shaft_corridor_reserve_mm=.04),
                scope='square floor captured spheres, specified walls/neck/error; not all beam returns')



def relieved_footprint_control():
    """Do not confuse square-corner collision with impossibility of a shoe.
    Replace square floors by capsules around the entire sphere-center slide.
    Exact distance between parallel 2-D segments checks neighbor separation.
    Then inspect ACTUAL rod centerline against the finite floor in half-select.
    A point strictly inside both solids proves interference without meshing.
    """
    slide=(4-sqrt(16-3.1**2))/2
    floors=[]
    for i,j,sign in product(range(-1,2),range(-1,2),(-1,1)):
        u=(i+j)*P/sqrt(2); v=(j-i)*P/sqrt(2)
        lo,hi=sorted((u+sign*2,u+sign*(2-slide)))
        floors.append((lo,hi,v))
    gap=float('inf'); count=0
    for n,(a,b,v) in enumerate(floors):
        for c,d,w in floors[n+1:]:
            dist=hypot(max(c-b,a-d,0),v-w)
            gap=min(gap,dist-2*(.6+.1+.4));count+=1
    assert gap>2*EPS  # square footprint rejection is escapable
    # Reachable nominal half-select: high shoe=2.5, low=0, no errors or lag.
    dz=2.5; sin_angle=dz/4; cos_angle=sqrt(1-sin_angle**2)
    high_u=2*cos_angle
    t=1.  # inside beam between high-end ball and central ball, beyond sphere
    rod_u=high_u-t*cos_angle
    distance=max((2-slide)-rod_u,rod_u-2,0)
    witnesses=[]
    for radius,wall in product((.25,.4,.55,.6),(.4,.6)):
        rho=radius+.1+wall
        z=radius-t*sin_angle  # floor top at local z=0, bottom=-.6
        assert t>radius+.15  # witness is not just intended rod/sphere connection
        assert distance<rho and -.6<z<0
        witnesses.append(dict(ball_radius_mm=radius,wall_mm=wall,
            rod_center_in_floor_uvz_mm=[rod_u,0,z],
            floor_axis_u_interval_mm=[2-slide,2],floor_radius_mm=rho,
            floor_z_interval_mm=[-.6,0],in_plane_inside_margin_mm=rho-distance,
            vertical_inside_margin_mm=min(z+.6,-z)))
    return dict(capsule_floor_pairs=count,minimum_capsule_floor_gap_mm=gap,
        expanded_capsule_gap_mm=gap-2*EPS,nominal_half_select_dz_mm=dz,
        rod_point_distance_from_ball_mm=t,witnesses=witnesses,
        decision='capsule floor fixes corner packing but solid floors intersect the tilted beam')

def reset():
    rows=[]
    for cam,shoe in product((.1,.2,.3),repeat=2):
        lag=cam+shoe  # radial dwell gap and vertical pocket gap in series
        rows.append(dict(cam_gap_mm=cam,shoe_gap_mm=shoe,endpoint_lag_mm=lag,
            half_clearance_directed_mm=.15-lag/2,
            half_clearance_uncontrolled_mm=.15-lag,
            high_high_max_lift_mm=1.1+lag))
    assert isclose(rows[4]['half_clearance_directed_mm'],-.05)
    return rows


def main():
    broad,narrow=frame(2.4),frame(1.6)
    assert broad['actual_collision'] is not None
    assert narrow['actual_collision'] is None
    assert narrow['min_neck_separating_gap_mm']>2*EPS
    result=dict(frame=[broad,narrow],mechanics=mechanics(),capture=capture(),capsule_control=relieved_footprint_control(),reset=reset(),
                evidence='finite solid witnesses and necessary elastic/kinematic bounds; self-review')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
