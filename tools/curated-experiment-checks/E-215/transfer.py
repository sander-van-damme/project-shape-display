"""Co-located support falsifiers. mm, N, s. Explicit bounds; no process priors.
Analytic annular/rectangular prisms, exact axial sweeps, rigid necessary reactions.
No physical, actuator, compliant-contact or complete-machine qualification.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

ROOT = Path(__file__).parents[1]

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cheeks = load('cheeks215', 'E-054/side_cheeks.py')
equilibrium = load('equilibrium215', 'E-056/contact_equilibrium.py')
EPS = 1e-10
PITCH = 5.08
STEP = 10.1
LEVELS = [STEP*i for i in range(5)]


def clip(poly, axis, bound, sign):
    """Clip convex polygon to sign*(coordinate-bound)>=0."""
    out = []
    for a,b in zip(poly, poly[1:]+poly[:1]):
        da, db = sign*(a[axis]-bound), sign*(b[axis]-bound)
        if da >= 0: out.append(a)
        if (da < 0) != (db < 0):
            t = da/(da-db)
            out.append(tuple(a[i]+t*(b[i]-a[i]) for i in range(2)))
    return out


def area(poly):
    return abs(sum(a[0]*b[1]-a[1]*b[0]
                   for a,b in zip(poly,poly[1:]+poly[:1])))/2


def radius_range(poly):
    far = max(x*x+y*y for x,y in poly)
    crosses = [a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])]
    if min(crosses) >= -EPS or max(crosses) <= EPS:
        near = 0.
    else:
        near = float('inf')
        for a,b in zip(poly,poly[1:]+poly[:1]):
            d = (b[0]-a[0], b[1]-a[1]); dd = d[0]**2+d[1]**2
            t = max(0., min(1., -(a[0]*d[0]+a[1]*d[1])/dd)) if dd else 0.
            near = min(near, sum((a[i]+t*d[i])**2 for i in range(2)))
    return near, far


def ring_hit(box, angle=math.pi/2, inner=1., outer=2.2,
             half_length=2.05, half_width=.6, z=(-1.4,0.), shift=(0.,0.)):
    if min(box[5],z[1])-max(box[4],z[0]) <= EPS: return False
    ca,sa = math.cos(angle), math.sin(angle)
    poly=[]
    for x,y in ((box[0],box[2]),(box[1],box[2]),(box[1],box[3]),(box[0],box[3])):
        x-=shift[0]; y-=shift[1]
        poly.append((ca*x+sa*y,-sa*x+ca*y))
    # Ring = circular annulus minus finite rectangular slot. Four convex
    # outside-slot pieces; continuous radius range on each convex polygon.
    for axis,bound,sign in ((0,half_length,1),(0,-half_length,-1),
                            (1,half_width,1),(1,-half_width,-1)):
        p=clip(poly,axis,bound,sign)
        if len(p)<3 or area(p)<EPS: continue
        near,far=radius_range(p)
        if near < outer**2-EPS and far > inner**2+EPS: return True
    return False


def annulus_hit(box, inner, outer, z):
    return ring_hit(box,0,inner,outer,0,0,z)


def lug(j,h,e=0.,dx=0.,dy=0.):
    return (-2-e+dx,2+e+dx,-.4-e+dy,.4+e+dy,h-STEP*j,h-STEP*j+1.2)


def sweep_z(box, dz):
    return (*box[:4],min(box[4],box[4]+dz),max(box[5],box[5]+dz))


def box_hit(a,b):
    return all(min(a[2*i+1],b[2*i+1])-max(a[2*i],b[2*i])>EPS for i in range(3))


def control():
    g=cheeks.geometry(.35,1.6,.4,.4,.8)
    assert not g['failures']
    old=equilibrium.run()
    # Explicit directly pushed rear face: positive x is pawl withdrawal.
    # 1-mm-long rod/nose stays attached to rear face during 1.22-mm stroke.
    x0=.45; tip=x0+1.6+1.24; start=tip-.77
    rod=(start+.8,start+1.8,-.3,.3,-1.5,-.5)
    rod_sweep=(rod[0],rod[1]+g['stroke'],*rod[2:])
    neighbor=(PITCH+x0,PITCH+x0+1.6,-.8,.8,-45,45)
    assert box_hit(rod_sweep,neighbor)
    penetration=rod_sweep[1]-neighbor[0]
    # Pawl shelves do not restrain column: tooth contact x=[0,.8],
    # web-centered service resultant lies behind the tooth pad in this frame.
    # Generic signed external couple exposes the inherited zero margin.
    reactions=equilibrium.reactions(10.,-.001,0.,2.,0.,.8)
    assert min(reactions)<0
    return {'geometry':g,'rear_rod_neighbor_penetration_mm':penetration,
            'edge_pressure_reactions_N':reactions,
            'prior_equilibrium_checks':old['equilibrium_checks']}


def ground_frame():
    # Continuous square deck with R=2.05 hole at z=-2.2..-1.8;
    # annular ledge above, four corner columns and two pairs of upper bridges.
    # Flat contacts ground forces; thickness/stiffness remain unqualified.
    posts=[]; bridges=[]
    for sx,sy in it.product((-1,1),repeat=2):
        x=sorted((sx*2.1,sx*2.5)); y=sorted((sy*2.1,sy*2.5))
        posts.append((*x,*y,-2.2,57.))
    for z,sgn in it.product((44.,56.),(-1,1)):
        y=sorted((sgn*1.5,sgn*2.5))
        b=(-2.5,2.5,*y,z-.5,z+.5); bridges.append(b)
        assert annulus_hit(b,.65,2.2,(z-.5,z+.5))
        assert sum(box_hit(b,p) for p in posts)==2
    # Whole-motion conservative envelopes, including unload and any old/target.
    rack=(-2,2,-.4,.4,-40.4,43.1)
    cap=(-2.3,2.3,-2.3,2.3,70,113.9)
    for body in posts+bridges:
        assert not box_hit(body,rack)
        assert not box_hit(body,cap)
    # Deck exists beneath each post: every point is outside the aperture.
    assert math.hypot(2.1,2.1)>2.05
    # Contact ledge and rotor overlap in radius, not a floating reaction arrow.
    assert 2.2-2.05>0
    return {'corner_posts':posts,'bridges':bridges,'radial_ring_bearing_mm':.15,
            'nominal_frame_width_mm':5.,'cap_bottom_min_mm':70.}


def gate_only(n):
    """Necessary nominal gate kinematics, with writer removed (NOT takeover)."""
    poses=0
    for old,new in it.product(range(5),repeat=2):
        if old==new:
            for j in range(5):
                assert not ring_hit(lug(j,LEVELS[old]))
            continue
        ho,hn=LEVELS[old],LEVELS[new]
        # Column lifts 1.5; ring lifts .4 to unkey; ring turns; height changes;
        # ring turns closed, seats, then column lowers. Axial key not built.
        phases=[(ho,ho+1.5,math.pi/2,math.pi/2,0,0),
                (ho+1.5,ho+1.5,math.pi/2,math.pi/2,0,.4),
                (ho+1.5,ho+1.5,math.pi/2,0,.4,.4),
                (ho+1.5,hn+1.5,0,0,.4,.4),
                (hn+1.5,hn+1.5,0,math.pi/2,.4,.4),
                (hn+1.5,hn+1.5,math.pi/2,math.pi/2,.4,0),
                (hn+1.5,hn,math.pi/2,math.pi/2,0,0)]
        for ha,hb,aa,ab,za,zb in phases:
            for k in range(n+1):
                t=k/n; h=ha+(hb-ha)*t; a=aa+(ab-aa)*t; z=za+(zb-za)*t
                for j in range(5):
                    b=lug(j,h)
                    assert not ring_hit(b,a,z=(-1.4+z,z))
                    assert not annulus_hit(b,2.05,2.5,(-1.8,-1.4))
                    # Upper stem-only guide bands. All lugs remain below them.
                    for gz in (44.,56.):
                        assert not annulus_hit(b,.65,2.2,(gz-.5,gz+.5))
                    poses+=1
    return poses


def acquisition():
    # Outer pads would contact two opposite lug underside patches; connected
    # down-stems remain inside their XY sections to an underframe carrier.
    # At acquisition their upper faces must reach z=0.
    outer=(1.25,1.85,-.3,.3,-2.,0.)
    assert ring_hit(outer)
    # Width/placement corners: enlarge/recess face by e, shift centers +/-e;
    # ring radius and slot width also +/-e. All include nominal z.
    results=[]
    for e in (.01,.025,.05):
        fails=0; grounded_lug_failures=0; count=0
        for sx,sy,sw,sr,sg in it.product((-1,1),repeat=5):
            b=(1.25+sx*e-sw*e,1.85+sx*e+sw*e,
               -.3+sy*e-sw*e,.3+sy*e+sw*e,-2.,0.)
            fails+=ring_hit(b,inner=1+sr*e,half_width=.6+sg*e)
            count+=1
        for sx,sy,sw,sr in it.product((-1,1),repeat=4):
            l=lug(0,0,sw*e,sx*e,sy*e)
            l=(*l[:4],-1.8,0.)
            grounded_lug_failures+=annulus_hit(l,2.05+sr*e,2.5,(-1.8,-1.4))
        results.append({'e':e,'corners':count,'outer_pickup_blocked':fails,
                        'ledge_corners':16,'lug_ledge_crossing_failures':grounded_lug_failures})
    # Move the pad radially inward, wholly within permanent center aperture.
    inner=(.68,.88,-.15,.15,-2.,0.)
    assert not ring_hit(inner)
    assert math.hypot(inner[1],inner[3])<1
    first=[]
    for old,h in enumerate(LEVELS):
        # From below ALL lugs, first positive contact is the bottom lug j=4.
        contacts=sorted((lug(j,h)[4],j) for j in range(5))
        z,j=contacts[0]
        assert j==4
        # Nose extended to nominal co-located contact intersects lower lugs.
        stem=(*inner[:4],-50.,0.)
        blocked=[i for i in range(5) if box_hit(stem,lug(i,h))]
        first.append({'old':old,'first_contact_z':z,'first_lug':j,
                      'intervening_lugs':blocked,'requested_lug':old})
        assert len(blocked)==4-old
    # Straight stems cannot cross a lower lug: exact axial union independently
    # confirms the ordering calculation. No time-step gap can bypass it.
    for old,h in enumerate(LEVELS[:-1]):
        path=sweep_z((*inner[:4],-52.,-50.),50.)
        assert box_hit(path,lug(4,h))
    # If the ring is opened first to admit an outer tool, neither tool nor
    # gate supplies vertical reaction: actual geometry, not command flags.
    assert not ring_hit(lug(0,-.01),angle=0)
    return {'manufactured':results,'first_contact':first,
            'outer_radial_overlap_with_gate_mm':.6,
            'inner_pad_total_area_mm2':2*(.88-.68)*.3,
            'open_gate_before_capture_supported':False}


def release_access():
    # Four axial spanner posts seat in .30-square, .30-deep blind underside
    # pockets at (+/-1.3,+/-1.3). Connected carrier below lowest lugs; only
    # these posts approach the rotor. Square flanks can provide signed torque.
    # They cannot pull the rotor downward out of its lifted state.
    t=.25
    radius=math.sqrt(2)*(1.3+t/2)
    assert radius<2.05
    # Exact circular bound on every angle of the 90-degree sweep.
    limit=2*(2.05/math.sqrt(2)-1.3)
    failures=[]
    for e in (.01,.025,.05):
        # Coherent radial post-placement + edge bias, frame aperture recession.
        r=math.sqrt(2)*(1.3+t/2+2*e)
        failures.append({'e':e,'post_outer_radius':r,'frame_aperture':2.05-e,
                         'collides':r>2.05-e,
                         'pocket_insertion_margin':(.30-.25)/2-4*e})
    assert all(x['pocket_insertion_margin']<0 for x in failures)
    # The positive-torque posts need stems to their carrier. At a 45-degree
    # turn one diagonal stem crosses the lower lug train, despite clearing the
    # circular frame bore. Explicit rotated finite .25-square section.
    ang=-math.pi/4; ca,sa=math.cos(ang),math.sin(ang)
    poly=[(ca*x-sa*y,sa*x+ca*y) for x,y in
          ((1.175,1.175),(1.425,1.175),(1.425,1.425),(1.175,1.425))]
    stem_hits=[]
    for old,h in enumerate(LEVELS):
        hits=[]
        for j in range(5):
            l=lug(j,h+1.5)
            p=poly
            for ax,bd,sgn in ((0,l[0],1),(0,l[1],-1),(1,l[2],1),(1,l[3],-1)):
                p=clip(p,ax,bd,sgn)
                if not p: break
            if p and area(p)>EPS and min(l[5],-.7)>max(l[4],-50)+EPS:
                hits.append(j)
        stem_hits.append(hits)
        assert len(hits)==4-old
    return {'nominal_post_radial_clearance':2.05-radius,
            'square_post_width_ceiling':limit,'corners':failures,
            'positive_axial_return_constructed':False,'rotating_stem_lug_hits_by_old':stem_hits,
            'gravity_return_1g_drag_0_02N_required_push_N':.001*9.81-.02}


def force_and_proof():
    # Columns have their own resident guide contacts: sleeve walls at z=44,56.
    # Required signed reactions; their actual loaded pose is NOT constructed.
    rows=[]
    for F,y,H in it.product((.1,1.,10.),(-1.,0.,1.),(-.05,0.,.05)):
        q56=(-F*y-26*H)/12
        q44=-H-q56
        assert abs(q44+q56+H)<1e-10
        assert abs(44*q44+56*q56+F*y+70*H)<1e-10
        rows.append((F,y,H,q44,q56))
    # Inward nose only pushes up. Signed lowering balance N=m(g-a)-D.
    lowering=[]
    for m,D,a in it.product((.005,.02), (0.,.06,.2), (0.,1.,5.)):
        N=m*(9.81-a)-D
        lowering.append({'m_kg':m,'drag_N':D,'a_m_s2':a,'required_upward_N':N,
                         'push_only_possible':N>=0})
    # Actual support is derived from vertical overlap below a lug, not sensor
    # output. A wrong-angle ring has no contact even if report says 'locked'.
    faults=[]
    for actual_locked,reported_locked in it.product((False,True),repeat=2):
        supported=ring_hit(lug(0,-.001),math.pi/2 if actual_locked else 0)
        assert supported==actual_locked
        faults.append({'actual_locked':actual_locked,'reported_locked':reported_locked,
                       'head_depart_command':reported_locked,
                       'unsupported_departure':reported_locked and not supported})
    return {'max_abs_guide_reaction_N':max(abs(x) for row in rows for x in row[3:]),
            'lowering':lowering,'false_proof':faults,
            'guide_reactions_are_necessary_not_loaded_pose':True}


def machine():
    # Fixed-datum hypothetical head motion, crediting as-yet-unbuilt capture.
    # Two 1.5-mm unload/reseat, |delta h|, return selected capture to datum.
    # Pair worst distance sum sqrt(|delta|)+sqrt(|delta|) at full excursion.
    times=[]
    for a,alpha,aux in it.product((1000.,5000.,20000.),(7200.,28800.,115200.),(.08,.16,.32)):
        linear=4*math.sqrt(1.5/a)+4*math.sqrt(40.4/a)+4*math.sqrt(.4/a)
        rotation=4*math.sqrt(90/alpha)
        slot=linear+rotation+aux
        times.append({'linear_a':a,'angular_a':alpha,'aux':aux,'slot_s':slot,
                      'passes':[H for H in (40,80,160) if 6+(6400//H)*slot<30]})
    # Motor/cable body width sensitivity: minimum integer spacing, entire
    # simultaneous row count. Finite actuator geometry remains unconstructed.
    packing=[]
    for width in (5.,8.,12.):
        stride=math.ceil(width/PITCH)
        sites=math.ceil(80/stride)
        packing.append({'envelope_mm':width,'stride':stride,'per_row':sites,
                        'rows':{H:math.ceil(H/sites) for H in (40,80,160)}})
    alloc=[]
    for cap,cell,H in it.product((200.,400.,500.),(0.,.01,.02,.04),(40,80,160)):
        alloc.append({'cap':cap,'resident_each':cell,'heads':H,
                      'strict_head_allocation':(cap-250-6400*cell)/H})
    return {'slot_limits':{H:(30-6)/(6400//H) for H in (40,80,160)},
            'timing_min_s':min(x['slot_s'] for x in times),
            'timing_max_s':max(x['slot_s'] for x in times),
            'timing_pass_counts':{H:sum(H in x['passes'] for x in times) for H in (40,80,160)},
            'times':times,'packing':packing,'allocations':alloc,
            # Completed proposal: height z, height capture, ring z, ring angle,
            # and positive ring return capture. Shared XY axes additional.
            'ring_output_lower_bound':{H:5*H+2 for H in (40,80,160)},
            'slider_output_lower_bound':{H:4*H+2 for H in (40,80,160)}}


def run():
    # Predicate holdouts: touch, penetration, center hole, connected outer rim.
    assert not ring_hit((1.2,1.8,-.2,.2,0,1))
    assert ring_hit((1.2,1.8,-.2,.2,-.001,1))
    assert not ring_hit((-.3,.3,-.3,.3,-2,1))
    assert not ring_hit((1.2,1.8,-.2,.2,-2,1),0)
    assert ring_hit((2.06,2.15,-.1,.1,-2,1),0)
    assert not annulus_hit((-.5,.5,-.5,.5,-2,1),1,2,(-1,0))
    assert annulus_hit((1.5,1.6,-.1,.1,-2,1),1,2,(-1,0))
    # Continuous open-slot fit independent of angular sampling.
    assert math.hypot(2,.4)<2.05
    assert 2<2.05 and .4<.6
    # Scope: rigid nominal ring-only transitions, no support claim.
    out={'control':control(),'ground_frame':ground_frame(),'gate_only_pose_counts':{n:gate_only(n) for n in (8,32,128)},
         'acquisition':acquisition(),'release_access':release_access(),
         'force_proof':force_and_proof(),'machine':machine()}
    print(json.dumps(out,indent=2))

if __name__=='__main__': run()
