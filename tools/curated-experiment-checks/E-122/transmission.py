#!/usr/bin/env python3
"""Finite rejection screens, mm/N/MPa. Deterministic bounds, not hardware proof.
Two operating principles: spring-maintained smooth cord / perforated metal strip.
Parameter variants are not new topologies. No third-party modules or random draws.
"""
import importlib.util
import json
from itertools import product
from functools import lru_cache
from math import atan2, cos, exp, isclose, pi, sin, sqrt
from pathlib import Path

spec = importlib.util.spec_from_file_location('routes', Path(__file__).resolve().parents[1]/'E-121/finite_routes.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
L = 2*old.H+2*pi*old.R-.8


def spring(d=.4, D=1.8, n=40, S0=9.7):
    # Classical close-coiled torsion model, G is a labelled steel scenario.
    G = 77000.
    k = G*d**4/(8*D**3*n)
    # Independent torsion-energy reconstruction of the close-coiled rate.
    J=pi*d**4/32
    wire_length=pi*D*n
    torque=S0*D/2
    assert isclose(torque**2*wire_length/(2*G*J),S0**2/(2*k))
    C = D/d
    wahl = (4*C-1)/(4*C-4)+.615/C
    return dict(wire_mm=d,mean_diameter_mm=D,active_turns=n,
                k_N_mm=k,outer_diameter_mm=D+d,solid_height_mm=(n+2)*d,
                installed_height_mm=34.,free_height_mm=34+S0/k,
                wahl_stress_MPa_at_S0=wahl*8*S0*D/(pi*d**3))


def loaded(hcmd, ea, dl, S0, k, F, b=0., loss=0., frame=0., arc_bias=0., bottom_bias=0.):
    """Loaded closure including drive-indexed bottom material and movable idler.
    b=Tupper-Tleft: upper bend/bearing hysteresis, either sign.
    F=Tupper-Tbottom: column load + guide drag. |F-b|<=.65 keeps E-121 box.
    loss is spring relaxation/slide stiction force deficit, not extra drive drag.
    frame is relative upper support displacement under internal load, mm.
    arc_bias is natural-length discrepancy of reduced arc partition, mm.
    Linear EA material law: 20-N scenario is diagnostic, not credible large strain.
    Quarter arcs are assigned adjacent branch tensions; bounds vary arc_bias.
    """
    free = L/(1+S0/(2*ea))
    grow = (free+dl)/free
    c0 = (4+hcmd-.4+pi*old.R/2)/(1+S0/(2*ea))*grow
    c0 += bottom_bias
    total = free+dl+arc_bias

    def state(x):
        S = S0-k*(x-frame)-loss
        u=(S+b)/2; left=(S-b)/2; bot=u-F
        # Exact finite extension for this piecewise-uniform reduced model.
        h=c0*(1+bot/ea)-3.6-pi*old.R/2
        a=old.H+x-4-h-.4+pi*old.R/2
        mid=old.H+x+pi*old.R
        residual=a/(1+u/ea)+mid/(1+left/ea)+c0-total
        return residual, h, S, u, left, bot
    lo,hi=-10.,10.
    assert state(lo)[0] < 0 < state(hi)[0]
    for _ in range(64):
        m=(lo+hi)/2
        if state(m)[0]<0: lo=m
        else: hi=m
    x=(lo+hi)/2
    residual,h,S,u,left,bot=state(x)
    assert abs(residual)<1e-10
    assert isclose(u-bot,F,abs_tol=1e-12)
    assert isclose(u+left,S,abs_tol=1e-12)
    assert isclose(left-bot,F-b,abs_tol=1e-12)
    ratio=max(left,bot)/min(left,bot) if min(left,bot)>0 else float('inf')
    return dict(x_mm=x,height_mm=h,height_error_mm=h-hcmd,S_N=S,
                upper_N=u,left_N=left,bottom_N=bot,
                drive_ratio=ratio,traction_margin_ratio=exp(.05*pi)-ratio,
                drive_reaction_N=left+bot,residual_mm=residual,
                within_stops=abs(x)<=1.5,taut=min(u,left,bot)>0)


def keeper_cases():
    s=spring()
    rows=[]
    # Original cut error +/- .5, then explicit additional irreversible seating/
    # creep drift 0/.5. Relaxation/stiction deficit and frame movement are bounds.
    # F=.55, b=-.1 -> drive .65; no double count of E-121's all-drag budget.
    for ea,dl,loss,F,b,frame,arc_bias,bottom_bias,rate,h in product(
            (20.,200.,2000.),(-.5,0.,.5,1.),(-.5,0.,.5),
            (-.55,.55),(-.1,.1),(-.1,.1),(-.05,.05),(-.01,.01),(.8,1.,1.2),(0.,20.,40.)):
        r=loaded(h,ea,dl,9.7,s['k_N_mm']*rate,F,b,loss,frame,arc_bias,bottom_bias)
        rows.append(dict(EA_N=ea,free_error_mm=dl,force_deficit_N=loss,
                         F_N=F,b_N=b,frame_mm=frame,arc_bias_mm=arc_bias,
                         bottom_bias_mm=bottom_bias,rate_multiplier=rate,hcmd_mm=h,**r))
    credible=[r for r in rows if r['EA_N']>=200]
    worst=min(credible,key=lambda r:r['traction_margin_ratio'])
    sensitivity=[]
    for S0 in (9.7,12.,14.):
        r=loaded(40,2000,1.,S0,s['k_N_mm'],.55,-.1,.5,-.1,.05)
        sensitivity.append(dict(S0_N=S0,**r))
    # Independent zero-load constant-force limit, and exact old zero-load model.
    for ea,dl in product((20.,200.,2000.),(-.5,.5)):
        r=loaded(17,ea,dl,9.7,0.,0.)
        assert isclose(2*r['x_mm'],dl*(1+9.7/(2*ea)),abs_tol=1e-10)
        k=s['k_N_mm']; free=L/(1+9.7/(2*ea))+dl
        exact=(free*(1+9.7/(2*ea))-L)/(2+free*k/(2*ea))
        assert isclose(loaded(17,ea,dl,9.7,k,0.)['x_mm'],exact,abs_tol=1e-10)
    assert worst['traction_margin_ratio']<0
    return dict(spring=s,cases=len(rows),credible_small_strain_cases=len(credible),
                worst=worst,force_sensitivity=sensitivity,
                x_range_mm=[min(r['x_mm'] for r in credible),max(r['x_mm'] for r in credible)],
                max_sampled_trial_height_error_mm=max(abs(r['height_error_mm']) for r in credible),
                arc_free_length_discrepancy_bound_mm_at_EA200=pi*old.R*(.1+.65)/200,
                bottom_quarter_discrepancy_bound_mm_at_EA200=pi*old.R*.65/(2*200),
                warning='Force-only 12/14-N repairs are NOT geometric or terminal survivors.')


def keeper_geometry():
    """Finite new central cartridge and conservative relocation screen.
    z=6 fixed seat, z=40+x moving seat; y=-1.3, spring mean radius .9.
    Two yoke plates join moving seat to upper axle at z=48+x. Their exact
    manufacture is unnecessary after a certified collision of the spring wire.
    """
    s=spring(); r=s['mean_diameter_mm']/2; d=s['wire_mm']
    solids={
      'front_seat_post':old.box(-.6,.6,-2.5,-2.3,-.8,6.),
      'back_seat_post':old.box(-.6,.6,-.3,-.1,-.8,6.),
      'fixed_seat':old.box(-1.2,1.2,-2.5,-.1,5.,6.),
      'moving_seat':old.box(-1.2,1.2,-2.5,-.1,40.,41.),
      'front_yoke':old.box(-.6,.6,-2.3,-1.9,41.,48.8),
      'back_yoke':old.box(-.6,.6,-.7,-.3,41.,48.8),
      'front_slide_rail':old.box(-.9,.9,-2.8,-2.6,38.,51.),
      'back_slide_rail':old.box(-.9,.9,0.,.2,38.,51.),
      'front_frame_tie':old.box(-.6,.6,-2.8,-2.6,0.,38.),
      'back_frame_tie':old.box(-.6,.6,0.,.2,0.,38.),
    }
    # Coil centerline, finite tube radius d/2. Point at phase zero lies inside
    # original moving bridge, not merely in an overlapping bounding cylinder.
    points=[(r*cos(2*pi*i/64),old.Y+r*sin(2*pi*i/64),
             6+d/2+(34-d)*i/(s['active_turns']*64))
            for i in range(s['active_turns']*64+1)]
    point=points[8*64]  # exact phase-zero wire point
    h=point[2]-4.
    bridge=old.hardware(h)[1]['clamp_bridge']
    margins=[min(v-a,b-v) for v,(a,b) in zip(point,bridge)]
    assert 0<h<40 and min(margins)>d/2
    assert old.point_box_sq(point,bridge)==0
    # E-121 bridge is cut by terminal seats and a cord bore. Witness must lie
    # in remaining material, not merely its bounding box.
    cavity_margins=[abs(point[0]-1.5)-.17-d/2]
    assert cavity_margins[0]>0
    for dz in (-.4,.4):
        distance=sqrt((point[0]-1.5)**2+(point[1]-old.Y)**2+(point[2]-(h+4+dz))**2)
        cavity_margins.append(distance-.32-d/2)
        assert cavity_margins[-1]>0
    # Continuous h interval for this fixed material wire section to lie in bridge.
    h_interval=[point[2]-5+d/2,point[2]-3-d/2]
    # Moving this whole cartridge to left/right escapes bridge only outside loop;
    # under independent-column top pitch it overlaps adjacent swept cells.
    offsets=[]
    for pitch in (5.08,10.16):
        for x in (-3.,3.):
            # Full radial cartridge extent plus unchanged column sweep, no claim
            # that larger internal pitch can be assigned without fanout.
            left=min(-2.34,x-1.2);right=max(2.34,x+1.2)
            offsets.append(dict(internal_pitch_mm=pitch,cartridge_x_mm=x,
                                x_hull_separation_mm=pitch-(right-left)))
    # Existing terminal throat containment under opposed diameter errors:
    # .3 bead radius - .17 bore radius, each surface can err e.
    seats=[dict(e_mm=e,retention_radius_margin_mm=.3-.17-2*e,
                minimum_seat_wall_mm=.13-2*e,
                inherited_axial_fit_gap_mm=.1-3*e)
           for e in (.025,.05,.1,.2)]
    return dict(solids_mm=solids,coil_centerline_point_mm=point,
                collision_height_mm=h,wire_to_outer_bridge_margin_mm=min(margins)-d/2,
                wire_to_terminal_cavities_margin_mm=min(cavity_margins),
                continuous_collision_height_interval_mm=h_interval,
                collision_interval_for_all_idler_stops_mm=[h_interval[0]+.3,h_interval[1]-.3],
                solid_clearance_at_lower_stop_mm=34-1.5-s['solid_height_mm'],
                coil_free_height_mm=s['free_height_mm'],relocation_screens=offsets,
                inherited_terminal_and_fit_scenarios=seats,
                disposition='Stop central cartridge at real wire/bridge collision; relocation hulls are not fanout geometry.')


def clip(poly,axis,bound,lower):
    """Sutherland-Hodgman clipping; exact line intersections, convex polygon."""
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da=(a[axis]-bound)*(1 if lower else -1)
        db=(b[axis]-bound)*(1 if lower else -1)
        if da>=0: out.append(a)
        if (da>=0)!=(db>=0):
            q=da/(da-db);out.append(tuple(x+q*(y-x) for x,y in zip(a,b)))
    return out


def tooth_polygon(r,height,width,tip,angle):
    p=[(r-.2,-width/2),(r+height,-tip/2),
       (r+height,tip/2),(r-.2,width/2)]
    return [(x*cos(angle)-z*sin(angle),x*sin(angle)+z*cos(angle)) for x,z in p]


def entry_extent(r,t,height,width,tip,angle):
    """Actual polygon inside finite straight tape slab, before tangent entry.
    Tape neutral material coordinate of this hole = R*angle, from no-slip arc
    indexing. Polygon/tape-slab intersection must fit the open hole interval.
    Returns necessary longitudinal half-window, and a finite witness point.
    """
    p=tooth_polygon(r,height,width,tip,angle)
    for axis,bound,lower in ((0,r-t/2,True),(0,r+t/2,False),(1,0.,True)):
        p=clip(p,axis,bound,lower)
        if not p:return (0.,None)
    point=max(p,key=lambda v:abs(v[1]-r*angle))
    return abs(point[1]-r*angle),point


@lru_cache(maxsize=None)
def entry_peak(r,t,height,width,tip,n=2048):
    # Samples locate a REJECTION witness only. No sampled pass is certified.
    best=(0.,0.,None)
    for i in range(n+1):
        a=i*pi/(2*n);extent,point=entry_extent(r,t,height,width,tip,a)
        if extent>best[0]:best=(extent,a,point)
    return best


def wrapped_extent(r,t,height,width,tip):
    """Exact polygon/circle intersections through the finite tape thickness.
    Arc-coordinate envelope of a fully seated tooth; used to calculate the
    load-bearing phase instead of assuming every tooth is centered in its hole.
    """
    poly=tooth_polygon(r,height,width,tip,0.)
    points=[]
    for radius in (r-t/2,r+t/2):
        for a,b in zip(poly,poly[1:]+poly[:1]):
            dx,dz=b[0]-a[0],b[1]-a[1]
            A=dx*dx+dz*dz; B=2*(a[0]*dx+a[1]*dz)
            C=a[0]**2+a[1]**2-radius**2
            determinant=B*B-4*A*C
            if determinant>=0:
                for u in ((-B-sqrt(determinant))/(2*A),(-B+sqrt(determinant))/(2*A)):
                    if 0<=u<=1: points.append((a[0]+u*dx,a[1]+u*dz))
    assert points
    return max(abs(r*atan2(z,x)) for x,z in points)


def mesh_comparison():
    # Generated open strip loop on two sheaves; p=2, n=5/8/12, 40-mm stroke
    # covers exactly 20 teeth, hence every entry phase recurs in each direction.
    # Slots leave >=.4 mm longitudinal web. This is a design bound, not a process
    # minimum. Includes tapered teeth as an explicit attempted entry repair.
    population=[]
    for n,height,tip,slot,e in product((5,8,12),(.4,.8,1.3),(.8,.2),
                                    (1.,1.3,1.6),(0.,.025,.05,.1,.2)):
        r=2*n/(2*pi);t=.025
        peak=entry_peak(r,t,height,.8,tip,512)
        # independent phase offset +/-2e and opposed slot/tooth edges e total:
        # reserve 3e on each longitudinal side; no assumed normal distribution.
        margin=slot/2-peak[0]-3*e
        # Anti-lift edge rails: clearance g>3e to avoid pinch; height-g>3e to
        # retain tape on the finite tooth. Most favorable g=height/2.
        capture=height/2-3*e
        population.append(dict(teeth=n,R_mm=r,tooth_height_mm=height,
            tip_mm=tip,slot_mm=slot,e_mm=e,entry_margin_mm=margin,
            capture_margin_mm=capture,phase_rad=peak[1],witness_mm=peak[2],
            minimum_internal_pitch_mm=2*(r+height+.3),
            reason='entry_collision' if margin<0 else
                   'pinch_or_lift_off' if capture<=0 else 'necessary_screens_only'))
    # Challenge the two e=.1 necessary survivors under real flank loading.
    # Centered slots carry no tangential load. Required phase shift to touch a
    # fully seated tooth is slot/2 - wrapped_extent. One signed load/motion
    # combination puts that shift against the incoming tooth. Hole enlargement
    # then cancels: loaded entry overrun = entry_extent - wrapped_extent.
    load_transfer=[]
    for n in (8,12):
        r=n/pi; peak=entry_peak(r,.025,.8,.8,.2,2048)
        wrapped=wrapped_extent(r,.025,.8,.8,.2)
        overrun=peak[0]-wrapped
        # Favorable distributed strain over ENTIRE half-wrap between contacts;
        # holes leave .6 mm total side-band width, t=.025, E=200 GPa scenario.
        ea=200000*.6*.025
        stretch=.65*pi*r/ea
        assert overrun>stretch+.01  # explicit extra 10-um discrepancy allowance
        load_transfer.append(dict(teeth=n,entry_half_extent_mm=peak[0],
            seated_half_extent_mm=wrapped,load_phase_shift_mm=.8-wrapped,
            loaded_entry_overrun_mm=overrun,
            favorable_intercontact_extension_mm=stretch,
            residual_after_001mm_discrepancy_mm=overrun-stretch-.01,
            scope='Taut circle/tangent path. Lift/bowing, tooth bending or conjugate profiles are NOT covered.'))
    loaded_error_screens=[]
    for e in (0.,.025,.05,.1,.2):
        margins=[]
        for n,height,tip in product((5,8,12),(.4,.8,1.3),(.8,.2)):
            r=n/pi
            overrun=entry_peak(r,.025,height,.8,tip,2048)[0]-wrapped_extent(r,.025,height,.8,tip)
            # An incoming hole and the already seated reference hole carry
            # opposed location errors +/-e. This survives global phase setting.
            # Keep hole sizes nominal: the differential 2e alone is a witness.
            margins.append(overrun+2*e-.65*pi*r/3000-.01)
        loaded_error_screens.append(dict(e_mm=e,
            min_interference_after_elastic_and_discrepancy_mm=min(margins),
            profile_sections=len(margins),
            all_taut_path_sections_rejected=min(margins)>0))
        if e>=.025: assert min(margins)>0
    rows=[]
    for e in (0.,.025,.05,.1,.2):
        sub=[r for r in population if r['e_mm']==e]
        rows.append(dict(e_mm=e,variants=len(sub),entry_failures=sum(r['reason']=='entry_collision' for r in sub),
                         capture_failures=sum(r['reason']=='pinch_or_lift_off' for r in sub),
                         necessary_only=sum(r['reason']=='necessary_screens_only' for r in sub)))
    assert all(r['reason']!='necessary_screens_only' for r in population if r['e_mm']==.2)
    # Wide/tall tapered profile is the best attempt in the full .2 box.
    wide=[r for r in population if r['e_mm']==.2 and r['capture_margin_mm']>0]
    closest=max(wide,key=lambda r:r['entry_margin_mm'])
    # Nominal rectangular-tooth jam reconstructed at a fixed angle, independent
    # analytic intersection of the radial outer edge with tape's center plane.
    r=5/pi; a=.7; height=.8; half=.4
    # Outer radial face crosses the finite tape slab at this angle.
    tangent=((r+height)*cos(a)-r)/sin(a)
    z=(r+height)*sin(a)+tangent*cos(a)
    assert -half<tangent<half
    witness_extent=abs(z-r*a)
    assert witness_extent>.65  # 1.3-mm hole, nominal collision
    ext,point=entry_extent(r,.025,height,.8,.8,a)
    assert ext>=witness_extent
    # Refinement is of the maximum witness, not a no-collision certificate.
    convergence=[dict(steps=n,peak_mm=entry_peak(r,.025,.8,.8,.8,n)[0])
                 for n in (256,512,1024,2048)]
    assert all(convergence[i+1]['peak_mm']>=convergence[i]['peak_mm'] for i in range(3))
    return dict(generated_variants=len(population),summaries=rows,
                full_box_closest=closest,nominal_rectangle_witness=dict(
                  teeth=5,R_mm=r,angle_rad=a,point_mm=[r,z],hole_center_mm=r*a,
                  hole_halfwidth_mm=.65,interference_mm=witness_extent-.65),
                convergence=convergence,loaded_transfer_witnesses=load_transfer,
                loaded_differential_error_screens=loaded_error_screens,
                seed='None; exhaustive stated Cartesian products',
                screening_population=population)


def strip_material_and_scale():
    # E=200 GPa is a labelled bound, not the Alleima datasheet value.
    # 1900 MPa proof strength is Alleima 20C nominal <.125-mm hardened strip.
    bending=[]
    for n,t in product((5,8,12),(.015,.025,.05)):
        r=n/pi
        bending.append(dict(teeth=n,thickness_mm=t,radius_mm=r,
                            elastic_outer_strain=t/(2*r),
                            elastic_bending_stress_MPa=200000*t/(2*r),
                            exceeds_nominal_1900MPa_proof=200000*t/(2*r)>1900,
                            net_section_tensile_stress_MPa_at065N=.65/(.6*t)))
    scales=[]
    for cells in (80,1600,6400):
        scales.append(dict(cells=cells,smooth_cords=cells,ends=2*cells,
                           sheaves=2*cells,shaft_bearing_interfaces=4*cells,
                           compression_springs=cells,sliding_yokes=cells,
                           spring_seats=2*cells,preload_setups=cells,
                           local_retainers_still_required=cells,
                           positive_tapes=cells,tape_end_joints=2*cells,
                           edge_retention_rail_halves=2*cells,
                           tape_holes_range=[53*cells,60*cells]))
    return dict(bending=bending,repeated_hardware_lower_bounds=scales,
                bought_per_cell_absolute_ceiling_USD=500/6400,
                bought_per_cell_ceiling_with_250_elsewhere_USD=250/6400,
                loop_material_length_m=6400*L/1000,
                tape_length_range_m=[6400*(2*48+2*n-.8)/1000 for n in (5,12)],
                dense_full_sweep_volume_L=6400*5.08**2*127.2/1e6,
                fourfold_internal_footprint_slab_volume_L=6400*10.16**2*127.2/1e6,
                warning='Volume allocation, not material volume. Wider pitch needs fanout/staggered depths, not free packing.')


def main():
    # Independent clip limiting cases and mirrored direction symmetry.
    square=[(-1,-1),(1,-1),(1,1),(-1,1)]
    assert all(p[0]>=0 for p in clip(square,0,0,True))
    assert len(clip(square,0,2,True))==0
    assert len(clip(square,0,-2,True))==4
    for a in (.1,.4,.8):
        p=tooth_polygon(2,.8,.8,.2,a)
        q=tooth_polygon(2,.8,.8,.2,-a)
        assert all(any(abs(x-X)<1e-12 and abs(z+Z)<1e-12 for X,Z in q) for x,z in p)
    mesh=mesh_comparison()
    # Keep full rejected population available only in reproducible stdout; no
    # checked-in generated files. Compact default summary avoids bulky reports.
    population=mesh.pop('screening_population')
    import sys
    if '--population' in sys.argv: mesh['screening_population']=population
    print(json.dumps(dict(evidence='reduced loaded closure and finite collision witnesses; self-review only',
                          keeper=keeper_cases(),geometry=keeper_geometry(),
                          mesh=mesh,scale=strip_material_and_scale()),indent=2))

if __name__=='__main__':main()
