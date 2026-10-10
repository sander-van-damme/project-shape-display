#!/usr/bin/env python3
"""E-121 deterministic finite routing screen. Units mm, N, radians.
Primitive CAD + conservative swept clearance, not contact/durability qualification.
No stochastic priors. All process/material numbers are epistemic scenarios.
"""
import argparse
import json
from itertools import product
from math import atan2, cos, exp, hypot, isclose, pi, sin, sqrt, tanh
from pathlib import Path

PITCH = 5.08
TRAVEL = 40.
R = 1.5
D = .3
H = 48.
Y = -1.3


def box(x0, x1, y0, y1, z0, z1):
    return ((x0, x1), (y0, y1), (z0, z1))


def translate(b, v):
    return tuple((a+v[i], c+v[i]) for i, (a, c) in enumerate(b))


def sweep(b, dz):
    return (b[0], b[1], (b[2][0], b[2][1]+dz))


def box_gap(a, b):
    # Separating-axis lower bound on distance. Positive => disjoint.
    return max(max(x[0]-y[1], y[0]-x[1]) for x, y in zip(a, b))


def point_box_sq(p, b):
    return sum(max(lo-v, 0., v-hi)**2 for v, (lo, hi) in zip(p, b))


def segment_box_distance(a, b, obstacle):
    # Exact convex piecewise quadratic minimization; no vertical samples.
    v = [y-x for x, y in zip(a, b)]
    cuts = [0., 1.]
    for i, (lo, hi) in enumerate(obstacle):
        if v[i]:
            cuts += [t for edge in (lo, hi) if 0 < (t := (edge-a[i])/v[i]) < 1]
    cuts = sorted(set(cuts))
    candidates = list(cuts)
    for lo, hi in zip(cuts, cuts[1:]):
        mid = (lo+hi)/2
        terms = []
        for i, (bot, top) in enumerate(obstacle):
            p = a[i]+v[i]*mid
            if p < bot:
                terms.append((a[i]-bot, v[i]))
            elif p > top:
                terms.append((a[i]-top, v[i]))
        den = sum(d*d for c, d in terms)
        if den:
            candidates.append(min(hi, max(lo, -sum(c*d for c, d in terms)/den)))
    return sqrt(min(point_box_sq([a[i]+t*v[i] for i in range(3)], obstacle)
                    for t in candidates))


def arc(xc, zc, start, end, n):
    return [(xc+R*cos(start+(end-start)*i/n), Y,
             zc+R*sin(start+(end-start)*i/n)) for i in range(n+1)]


def loop_path(h, n=96):
    """One cord, both ends clamped to the carriage, with finite 0.8-mm end gap.
    Intended pulley contact. Path order goes up right, across top, down left,
    under bottom, up right to lower clamp. No accumulating winding/layer passage.
    """
    z = 4+h
    return ([(R,Y,z+.4)] + arc(0,H,0,pi,n) +
            arc(0,0,pi,2*pi,n) + [(R,Y,z-.4)])


def poly_length(points):
    return sum(sqrt(sum((a-b)**2 for a,b in zip(p,q))) for p,q in zip(points,points[1:]))


def hardware(h=0.):
    """AABBs for finite extruded guide/column/clamp pieces. Pulley boxes are
    conservative hulls of the SCAD cylinders, not claims that grooves are solid.
    Axles are conservative hulls of radius .4 cylinders along y.
    """
    static = {}
    for name, z in [('lower',0.),('upper',H)]:
        static[name+'_pulley'] = box(-1.85,1.85,-1.8,-.8,z-1.85,z+1.85)
        static[name+'_axle'] = box(-.4,.4,-2.3,-.3,z-.4,z+.4)
        # Two separated finite bearing cheeks; bore contact intentionally omitted
        # from independent obstacle checks against its own axle.
        for side, (a,b) in enumerate([(-2.3,-1.9),(-.7,-.3)]):
            static[f'{name}_bearing{side}'] = box(-.8,.8,a,b,z-.8,z+.8)
    for z in (10.,40.):
        for side in (-1,1):
            xx = (-1.4,-1.) if side < 0 else (1.,1.4)
            static[f'guide{z}_side{side}'] = box(*xx,.7,2.2,z-.8,z+.8)
            xx = (-1.4,-.6) if side < 0 else (.6,1.4)
            static[f'guide{z}_lip{side}'] = box(*xx,-.1,.7,z-.8,z+.8)
        static[f'guide{z}_back'] = box(-1.4,1.4,1.8,2.2,z-.8,z+.8)
    moving = {
        'stem_flange':box(-.7,.7,1.,1.5,h-34,h+52),
        'stem_web':box(-.3,.3,.1,1.2,h-34,h+52),
        'top':box(-2.34,2.34,-2.34,2.34,h+52,h+53.2),
        'clamp_bridge':box(-.3,1.95,-1.8,-.5,h+3.,h+5.),
        'clamp_finger':box(-.3,.3,-.7,.3,h+3.,h+5.),
    }
    return static, moving


def swept_loop_checks(n=96):
    static, moving = hardware()
    swept = {k:sweep(b,40) for k,b in moving.items()}
    pair_gaps = {(a,b):box_gap(x,y) for a,x in swept.items() for b,y in static.items()}
    pair, gap = min(pair_gaps.items(),key=lambda x:x[1])
    assert gap > 0, (pair,gap)
    # Static cord envelope is the union over all h: omit clamp gaps, conservative.
    path = [(R,Y,0)] + arc(0,H,0,pi,n) + arc(0,0,pi,2*pi,n) + [(R,Y,H)]
    sagitta = R*(1-cos(pi/(2*n)))
    # Own pulley is intended groove contact; bearing and guide pieces are not.
    obstacles = {k:b for k,b in static.items() if not k.endswith('_pulley')}
    obstacles.update({k:b for k,b in swept.items() if not k.startswith('clamp')})
    cable_gaps = {name:min(segment_box_distance(a,b,ob) for a,b in zip(path,path[1:]))
                       - D/2-sagitta for name,ob in obstacles.items()}
    assert min(cable_gaps.values()) > 0, cable_gaps
    # Separate cells: complete swept hulls including cord, bearings, guides and
    # arbitrary-height caps stay within these boxes. Covers any old/new transition
    # and all neighbor heights continuously, not just the nine-state workload.
    objects = list(static.values())+list(swept.values())
    objects.append(box(-R-D/2,R+D/2,Y-D/2,Y+D/2,-R-D/2,H+R+D/2))
    hull = tuple((min(b[i][0] for b in objects),max(b[i][1] for b in objects)) for i in range(3))
    neighbor = min(box_gap(hull,translate(hull,(i*PITCH,j*PITCH,0)))
                   for i,j in product((-1,0,1),repeat=2) if i or j)
    assert isclose(neighbor,.4,abs_tol=1e-12)
    # Under-map vertical access corridor, reserved for next task, not a head.
    # Its roof stops below pulley; no private coupling or lock is credited here.
    access = box(-1.,1.,-1.8,-.8,-38.,-1.95)
    clearance = min(box_gap(access,b) for b in objects)
    assert clearance > 0
    # Captured terminal beads are wholly inside the clamp envelope. These
    # deliberate seat contacts are excluded from free-clearance checks.
    for dz in (-.4,.4):
        bead=box(1.2,1.8,Y-.3,Y+.3,4+dz-.3,4+dz+.3)
        assert all(a <= c <= d <= b for (a,b),(c,d) in zip(moving['clamp_bridge'],bead))
    assert .3 > .17  # bead cannot pass the cord bore in rigid geometry
    # Independent analytic lengths, endpoints and full nine-height transition set.
    exact = 2*H+2*pi*R-.8
    lengths = [poly_length(loop_path(h,n)) for h in range(0,41,5)]
    assert max(lengths)-min(lengths) < 1e-10
    assert all(abs(x-exact) < 2*pi*R*(pi/n)**2/24+1e-10 for x in lengths)
    for old,new in product(range(0,41,5),repeat=2):
        assert isclose(R*((new-old)/R),new-old,abs_tol=1e-12)
        # Upper free leg contracts exactly as lower free leg grows.
        assert isclose((H-(4+new+.4))+(4+new-.4),H-.8)
    # Tangents at the four straight/arc joins are parallel, radii exactly R.
    assert isclose(hypot(loop_path(0,n)[1][0],loop_path(0,n)[1][2]-H),R)
    return dict(internal_solid_gap_mm=gap,limiting_pair=pair,
                cord_obstacle_gap_lower_mm=min(cable_gaps.values()),
                arc_chord_sagitta_mm=sagitta,neighbor_swept_gap_mm=neighbor,
                occupied_sweep_mm=hull,access_box_mm=access,access_gap_mm=clearance,
                cord_length_mm=exact,polygon_length_mm=lengths[0],
                turns_per_stroke=40/(2*pi*R),height_pairs=81,
                full_board_cord_m=6400*exact/1000,
                bend_centerline_radius_mm=R,bend_diameter_over_cord_diameter=2*R/D,
                guide_engagement_end_margin_mm=3.2)


def winding_route(h, layer, n=192):
    """Finite four-plane seed, axis z. Anchor at fixed material groove end;
    contact departure world angle zero, finite helix pitch .6 and cord .3.
    The changing exit elevation is included; no fictitious fixed exit point.
    h uses exact taut length: winding gain minus upward-exit free-leg loss.
    Stop at certified intersite solid contact before any reach/force acceptance.
    """
    r = 40/(4*pi)
    pitch = .6
    a = pitch/(2*pi)
    theta = h/(sqrt(r*r+a*a)-a)
    wraps = 2*pi+theta  # one dead turn plus takeup, finite anchor included
    zbase = -12.-layer*5.
    helix = [(r*cos(u),r*sin(u),zbase+a*(u+theta))
             for i in range(n+1) for u in [-wraps+wraps*i/n]]
    alpha = atan2(a,r)
    bend = r/2
    endz = helix[-1][2]
    bendpts = [(r,bend*(sin(t+alpha)-sin(alpha)),
                endz+bend*(cos(alpha)-cos(t+alpha)))
               for i in range(n+1) for t in [(pi/2-alpha)*i/n]]
    yy = bendpts[-1][1]
    riser = [bendpts[-1],(r,yy,48.)]
    top = [(r-bend*(1-cos(pi*i/n)),yy,48.+bend*sin(pi*i/n)) for i in range(n+1)]
    tail = [(0.,yy,4.+h)]
    return helix+bendpts[1:]+riser[1:]+top[1:]+tail, riser


def layered_witness():
    # Colors c=x%2+2*(y%2), ordered top to bottom. Bottom site (1,1) has
    # right neighbor (2,1), color2, immediately above. Translation canceled.
    outer = 40/(4*pi)+1.5
    points,riser = winding_route(0,3)
    x,y,z = riser[0]
    dist = hypot(x-PITCH,y)
    disk_z = -12.-2*5.
    assert riser[0][2] < disk_z < riser[1][2]
    assert dist+D/2 < outer  # cord section is wholly INSIDE neighbor disk hull
    # Core radius excludes the surface groove; this is solid core contact too.
    core = 40/(4*pi)-D/2
    assert dist+D/2 < core
    # Witness persists at every h, and riser XY is independent of h continuously.
    for h in range(41):
        _,rs = winding_route(h,3)
        assert rs[0][2] < disk_z < rs[1][2]
        assert isclose(rs[0][0],x) and isclose(rs[0][1],y)
    # Antagonistic split-spool variant retains this lifting branch and adds a
    # return member. Retaining the offending subcurve cannot remove its contact.
    # Verify corrected taut payout: helix slope moves exit toward upper bend.
    l0=poly_length(winding_route(0,3)[0]); l40=poly_length(winding_route(40,3)[0])
    r=40/(4*pi); a=.6/(2*pi); metric=sqrt(r*r+a*a)
    for h in (0.,13.7,40.):
        theta=h/(metric-a)
        assert isclose(metric*theta-a*theta-h,0.,abs_tol=1e-12)
    errors=[abs(poly_length(winding_route(40,3,n)[0])-poly_length(winding_route(0,3,n)[0]))
            for n in (96,192,384,768)]
    assert all(errors[i+1] < errors[i]/3.9 for i in range(3))
    return dict(topology='four-plane helical gravity spool; inherited by split antagonistic spool',
                rejected_by='upward finite riser intersects shallower neighbor core',
                witness_xyz_mm=[x,y,disk_z],neighbor_center_xy_mm=[PITCH,0],
                radial_distance_mm=dist,core_radius_mm=core,
                core_containment_margin_mm=core-dist-D/2,
                polyline_total_length_discrepancy_mm=l40-l0,
                exact_total_length_change_mm=0.,
                winding_length_discretization_errors_mm=errors,
                commanded_theta_per_mm=1/(sqrt((40/(4*pi))**2+(.6/(2*pi))**2)-.6/(2*pi)),
                groove_pitch_mm=.6,cord_diameter_mm=D,dead_turns=1,
                max_wound_turns=1+40/(2*pi*(sqrt((40/(4*pi))**2+(.6/(2*pi))**2)-.6/(2*pi))),
                note='Exact helix/free-leg length closure; no compliant contact model. Stop at collision; no force pass.')


def forces():
    # Applied loads, friction, loss, EA and length mismatch are ASSUMPTION boxes.
    # Output ranges are feasibility conditions, not sampled yield or properties.
    gravity=[]
    for guide,bearing,motor in product((.005,.03,.1),(.001,.01,.05),(0.,.01)):
        drag=guide+bearing+motor
        gravity.append(dict(guide_N=guide,routing_N=bearing,residual_drive_N=motor,
                            minimum_moving_mass_g=1000*drag/9.81))
    loop=[]
    for load,drag,mu in product((.05,.2,.5),(0.,.05,.15),(.05,.15,.3)):
        f=load+drag
        preload=f/(2*tanh(mu*pi/2))
        hi=preload+f/2; lo=preload-f/2
        assert lo > 0 and isclose(hi/lo,exp(mu*pi),rel_tol=1e-10)
        # Work/torque reciprocity (ideal; parasitic losses charged in f).
        assert isclose((R*f)*(40/R),40*f)
        loop.append(dict(load_N=load,all_drag_N=drag,mu=mu,
                         required_mean_preload_N=preload,
                         high_tension_N=hi,low_tension_N=lo,
                         drive_torque_Nmm=R*f,shaft_reaction_upper_N=2*preload))
    exact=2*H+2*pi*R-.8
    compliance=[]
    # Fixed centers / imposed loop length; length common bias does NOT cancel.
    for ea,delta in product((20.,200.,2000.),(-.5,0.,.5)):
        compliance.append(dict(EA_N=ea,excess_free_length_mm=delta,
                               preload_change_N=-ea*delta/exact,
                               required_center_adjustment_mm=delta/2,
                               conservative_height_error_mm_at_delta_tension_065N=.65*exact/ea))
    mismatch=[]
    for differential in (0.,.01,.05,.1):
        mismatch.append(dict(relative_opposed_radius_error=differential,
                             antagonistic_length_mismatch_mm=40*differential))
    # Instantaneous mean drive preload is an interface requirement, NOT a
    # free consequence of a chosen cut length. Fixed-length bad corner is real.
    required=.65/(2*tanh(.05*pi/2))
    slack_corner=4.5-2000*.5/exact
    assert slack_corner < 0
    free_cut_length=exact/(1+4.5/2000)
    exact_slack=free_cut_length+.5-exact
    assert exact_slack > 0  # independent finite-extension check, no negative tension
    force_capacity=2*4.5*tanh(.05*pi/2)
    assert force_capacity > .65
    return dict(gravity_return=gravity,loop=loop,compliance=compliance,
                conditional_interface=dict(mean_drive_preload_N=[4.5,5.0],
                    worst_tension_with_additional_idler_loss_N=5.+.65/2+.15,
                    shaft_reaction_bound_N=2*5.+2*.15,
                    transmitted_force_at_min_preload_min_mu_N=force_capacity,
                    torque_bound_Nmm=R*.65,
                    total_signed_rotation_rad=40/R,
                    admissible_positive_free_length_drift_mm_at_EA2000=(4.5-required)*exact/2000,
                    fixed_length_slack_corner_N=slack_corner,
                    independent_excess_free_length_mm=exact_slack,
                    guide_friction_from_offset_N_at_mu03_load05=2*.3*.5*hypot(1.5,2.5)/30,
                    solid_monofilament_outer_bending_strain=D/(2*R),
                    axial_strain_at_max_tension={ea:5.475/ea for ea in (20,200,2000)}),
                paired_spool_mismatch=mismatch,
                zero_friction='No finite preload transmits nonzero load when mu=0.',
                gravity_mass_box_g=[.3,3.],
                force_box_max_N=.65,
                minimum_EA_N_for_conservative_05mm_load_error=.65*exact/.5)


def idler_reaction_bounds():
    """Necessary bounds for a hypothetical movable UPPER sheave, not its design.
    S is its upward frame/spring reaction. F is the signed column tension
    difference, positive for upward support. Lossless upper sheave only:
    Tupper=Tleft=S/2; Tbottom=S/2-F; drive mean P=(S-F)/2.
    A force with fixed direction is not the same as a motion direction.
    """
    fmax = .65
    mu = .05
    pmin, pmax = 4.5, 5.
    # No ONE constant reaction maintains the old narrow P interface for both
    # signs. This does NOT exclude a load-reacting or wider-envelope mechanism.
    lower = 2*pmin+fmax
    upper = 2*pmax-fmax
    assert lower > upper
    # Direct capstan ratio, independently equivalent to mean-tension bound.
    s_required = 2*fmax/(1-exp(-mu*pi))
    assert isclose(s_required, fmax+fmax/tanh(mu*pi/2))
    assert isclose((s_required/2)/(s_required/2-fmax), exp(mu*pi))
    cases=[]
    for s,f in product((9.,9.7,10.),(-fmax,0.,fmax)):
        top=left=s/2
        bottom=top-f
        mean=(left+bottom)/2
        assert isclose(top-bottom,f) and isclose(top+left,s)
        assert isclose(mean,(s-f)/2)
        assert isclose((left-bottom)*R,f*R)
        ratio=max(left,bottom)/min(left,bottom)
        cases.append(dict(upper_reaction_N=s,signed_column_force_N=f,
                          drive_mean_N=mean,top_terminal_N=top,
                          bottom_terminal_N=bottom,drive_shaft_reaction_N=left+bottom,
                          traction_ratio=ratio,ideal_no_slip=ratio < exp(mu*pi)))
    # Exact uniform axial-extension closure at ZERO column load, where all
    # tensions are equal. L changes by 2x as the top sheave translates upward.
    # S(x)=S0-k*x; positive stiffness unloads on extension. A physical spring,
    # slide, stops and reaction frame are NOT supplied by this scalar model.
    length=2*H+2*pi*R-.8
    s0=9.7
    mismatch=[]
    for ea,k,dl in product((20.,200.,2000.),(0.,.5,5.),(-.5,.5)):
        free0=length/(1+s0/(2*ea))
        free=free0+dl
        x=(free*(1+s0/(2*ea))-length)/(2+free*k/(2*ea))
        s=s0-k*x
        residual=(length+2*x)-free*(1+s/(2*ea))
        assert abs(residual) < 1e-12 and s > 0
        if k==0:
            assert isclose(2*x,dl*(1+s0/(2*ea)))
        mismatch.append(dict(EA_N=ea,spring_slope_N_per_mm=k,
                             free_length_error_mm=dl,idler_shift_mm=x,
                             zero_load_reaction_N=s,
                             reaction_exceeds_bidirectional_traction_threshold=s > s_required,
                             nominal_axial_strain=s0/(2*ea),
                             model_limit='Large strain: linear EA is not credible' if ea==20 else
                                         'Uncalibrated elastic scenario; no creep/bend/contact model'))
    # Mechanism equilibrium: upper support S up, drive support S-F down,
    # external column load F down sum to zero. 6400*S is summed reaction, NOT net
    # externally applied board load. Support-sheet/internal stress still matters.
    assert isclose(s0-(s0-fmax)-fmax,0.,abs_tol=1e-12)
    return dict(evidence='Necessary lossless statics and uniform-extension bounds; no finite tensioner',
                old_mean_interface_constant_reaction_lower_N=lower,
                old_mean_interface_constant_reaction_upper_N=upper,
                minimum_upper_reaction_N_at_mu005_F065=s_required,
                reaction_cases=cases,zero_load_length_adjustment=mismatch,
                summed_local_upper_reactions_N_at_S97=6400*s0,
                net_external_preload_force_N=0.,
                limitation='Signed F reverses only if demanded force reverses; motion reversal alone need not do so. '
                           'Upper bearing loss, finite bends, slide friction, spring/frame compliance and terminals remain unqualified.')


def uncertainty():
    # Independent opposing surface errors; 2e placement + e effective size.
    # Box corner enumeration, not a distribution. Coherent checkerboard attains
    # neighbor worst case, so failures must not be averaged over 6400 sites.
    rows=[]
    for e in (.025,.05,.1,.2):
        worst=min(a-b-c for a,b,c in product((-e,e),repeat=3))
        assert isclose(worst,-3*e)
        rows.append(dict(e_mm=e,neighbor_gap_lower_mm=.4+worst,
                         internal_gap_lower_mm=.1+worst,
                         sliding_guide_gap_lower_mm=.3+worst,
                         spool_groove_separation_lower_mm=.3+worst,
                         loop_flange_side_gap_lower_mm=.1+worst))
    # Internal .1 gap is bearing-to-pulley axial clearance. Moving solids vs
    # unrelated solids have .3 nominal gap; pulley bearing interface .1 matters.
    return dict(relative_boxes=rows,
                common_translation='Exactly invariant if frame, loop and guides move together.',
                common_growth_005_mm='Opposing solid surfaces reduce .1 bearing gap to zero; .3 guide gap to .2.',
                common_radius_bias_01_mm='At fixed angular command: full-stroke scale error 40*.1/1.5=2.666667 mm.',
                common_loop_length_bias='Does not cancel; preload shifts by -EA*deltaL/L.',
                distribution='None. No machine yield or reliability estimate.')


def scad(path):
    static,moving=hardware()
    def cube(b):
        return f'translate({[a for a,b in b]}) cube({[b-a for a,b in b]});'
    lines=['// E-121 generated geometry; mm. Deliberate groove/axle contacts.', '$fn=64;',
           'module rod(a,b,r){hull(){translate(a)sphere(r);translate(b)sphere(r);}}',
           'module pulley(z){translate([0,-1.3,z]) rotate([90,0,0]) difference(){',
           'cylinder(h=1,r=1.85,center=true);',
           'difference(){cylinder(h=.5,r=2,center=true);cylinder(h=.7,r=1.35,center=true);}',
           'cylinder(h=2,r=.4,center=true);}}']
    for name,b in static.items():
        if name.endswith('_pulley'):
            lines.append('color("gray") pulley(%s);' % ((b[2][0]+b[2][1])/2))
        elif name.endswith('_axle'):
            z=(b[2][0]+b[2][1])/2
            lines.append(f'color("silver") translate([0,-1.3,{z}]) rotate([90,0,0]) cylinder(h=2,r=.4,center=true);')
        elif '_bearing' in name:
            z=(b[2][0]+b[2][1])/2
            yy=(b[1][0]+b[1][1])/2
            lines.append('color("gray") difference(){'+cube(b)+f'translate([0,{yy},{z}]) rotate([90,0,0]) cylinder(h=1,r=.5,center=true);'+'}')
        else:
            lines.append('color("gray") '+cube(b))
    for name,b in moving.items():
        if name=='clamp_bridge':
            # Two captured .6-mm terminal beads; two-piece clamp assembly is
            # required. Joining method and bead strength are not qualified.
            lines.append('color("orange") difference(){'+cube(b)+
                         'translate([1.5,-1.3,2.9]) cylinder(h=2.2,r=.17);'+
                         'translate([1.5,-1.3,3.6]) sphere(.32);'+
                         'translate([1.5,-1.3,4.4]) sphere(.32);}')
            for z in (3.6,4.4):
                lines.append(f'color("red") translate([1.5,-1.3,{z}]) sphere(.3);')
        else:
            lines.append('color("orange") '+cube(b))
    for a,b in zip(loop_path(0),loop_path(0)[1:]):
        lines.append(f'color("blue") rod({list(a)},{list(b)},{D/2});')
    path.write_text('\n'.join(lines)+'\n')



def winding_scad(path):
    points, _ = winding_route(0,3)
    r=40/(4*pi)
    lines=['// Failed E-120 four-plane route at h=0, lower site translated to XY origin.',
           '$fn=64;', 'module rod(a,b,r){hull(){translate(a)sphere(r);translate(b)sphere(r);}}']
    # Finite core and axle cylinders. The actual solid core suffices for
    # rejection; rims and groove-wall detail are not generated after failure.
    for x,z in [(0.,-27.),(PITCH,-22.)]:
        lines.append(f'color("gray") translate([{x},0,{z+.325}]) cylinder(r={r-D/2},h=2.45,center=true);')
        lines.append(f'color("silver") translate([{x},0,{z}]) cylinder(r=.6,h=4.4,center=true);')
    for a,b in zip(points,points[1:]):
        lines.append(f'color("blue") rod({list(a)},{list(b)},{D/2});')
    lines.append(f'color("red") translate({list(points[0])}) sphere(.3);')
    path.write_text('\n'.join(lines)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--winding-scad',type=Path,help='Optional failed layered winding witness')
    parser.add_argument('--scad',type=Path,help='Optional reproducible assembly, do not commit generated output')
    args=parser.parse_args()
    # Independent segment-distance limiting cases and translation invariance.
    ob=box(-1,1,-1,1,-1,1)
    assert segment_box_distance((-2,0,0),(2,0,0),ob)==0
    assert isclose(segment_box_distance((2,2,-2),(2,2,2),ob),sqrt(2))
    checks=[swept_loop_checks(n) for n in (24,48,96,192)]
    assert all(checks[i+1]['cord_obstacle_gap_lower_mm'] >= checks[i]['cord_obstacle_gap_lower_mm']-1e-12 for i in range(3))
    static,moving=hardware()
    shift=(12.3,-54.2,9.87)
    assert isclose(box_gap(moving['stem_web'],static['guide10.0_lip1']),
                   box_gap(translate(moving['stem_web'],shift),translate(static['guide10.0_lip1'],shift)),abs_tol=1e-12)
    if args.winding_scad:
        winding_scad(args.winding_scad)
    if args.scad:
        scad(args.scad)
    print(json.dumps(dict(evidence='finite primitive geometry, analytical bounds, self-review; not physical validation',
                          layered_winding=layered_witness(),loop=checks[-1],
                          discretization=checks,forces=forces(),uncertainty=uncertainty(),
                          upper_idler_bounds=idler_reaction_bounds(),
                          repeated_per_board=dict(cords=6400,terminations=12800,pulleys=12800,
                              axles=12800,bearing_interfaces=25600,guide_stations=12800,
                              translating_columns=6400,clamps=6400,local_locks_required=6400,
                              preload_settings_required=6400)),indent=2))


if __name__=='__main__':
    main()
