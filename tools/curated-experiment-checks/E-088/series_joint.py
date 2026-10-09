"""E-088 finite series-torsion rotary joint. mm, N, seconds; explicit bounds.
No fabrication priors, fitted distributions, friction compensation or dynamics.
Reuses E-087 convex clipping; all new solids are finite convex prism pieces.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec=importlib.util.spec_from_file_location('e087',Path(__file__).resolve().parents[1]/'E-087/rotary_carrier.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
P,D=5.08,1.2
APP=-math.pi/4
LENGTH=2.7


def blade(t,h=3,b=0,w=.6,length=LENGTH):
    return g.paddle(t,height=h,center=.6+b,width=w,length=length)


def demand(t,err,height=0):
    b,h,w,tstop,v,z,l=err
    poly=blade(t,3+h+height,b,.6+w,LENGTH+l)
    band=g.clip(g.clip(poly,(0,-1),0),(0,1),1+z)
    return max((x for x,z in band),default=-1e6)+(.8+v)/2


def terminal(err):
    return g.root(lambda t:demand(t,err)-(D+err[3]),APP,math.radians(30))


def geometry(e,n):
    capture=1e9;theta=[];guidegap=1e9;miss=0.;count=0
    for err in it.product((-e,e),repeat=7):
        b,h,w,t,v,z,l=err
        end=terminal(err);theta.append(end)
        x=t
        for stage in (0,1,2):
            for i in range(n+1):
                u=i/n
                angle=APP if stage==0 else APP+(end-APP)*u if stage==1 else end
                lift=1.5*(1-u) if stage==0 else 0 if stage==1 else 1.5*u
                poly=blade(angle,3+h+lift,b,.6+w,LENGTH+l)
                q=demand(angle,err,lift)
                if stage==0:
                    capture=min(capture,t-q)
                if stage==1: x=max(x,q)
                dog=g.rect(x-(.8+v)/2,x+(.8+v)/2,0,1+z)
                miss=max(miss,g.area(g.intersect(poly,dog)))
                # Reserved dog-guide material lies at or below z=0.
                guidegap=min(guidegap,min(z for x,z in poly))
                for col,state in it.product((-1,1),(0,1)):
                    neighbor=g.rect(col*P+state*D+t-(.8+v)/2,col*P+state*D+t+(.8+v)/2,0,1+z)
                    assert g.area(g.intersect(poly,neighbor))<1e-8
            if stage==1: assert abs(x-(D+t))<1e-8
        count+=1
    # Continuous whole-sector and raised-circle bounds include independent
    # neighboring pivot x/z errors; no sampling credit for neighbor isolation.
    radius=math.hypot(LENGTH+e,(.6+e)/2)
    sector_gap=P*math.cos(APP)-(.6+e)/2-radius-2*math.sqrt(2)*e
    raised_gap=4.5-e-radius-(1+e)
    assert miss<1e-8 and capture>0 and guidegap>0 and sector_gap>0 and raised_gap>0
    return dict(error_mm=e,steps=n,corners=count,min_capture_mm=capture,
                terminal_deg=[math.degrees(min(theta)),math.degrees(max(theta))],
                min_guide_gap_mm=guidegap,sector_gap_mm=sector_gap,
                raised_gap_mm=raised_gap,max_intersection_mm2=miss)


def circle(r,n=48):
    return [(.6+r*math.cos(2*math.pi*i/n),3+r*math.sin(2*math.pi*i/n)) for i in range(n)]


def annulus(r0,r1,start=-math.pi,end=math.pi,n=48):
    return [[(.6+r*math.cos(t),3+r*math.sin(t)) for r,t in
            ((r0,a),(r1,a),(r1,b),(r0,b))]
            for a,b in zip([start+(end-start)*i/n for i in range(n)],
                           [start+(end-start)*(i+1)/n for i in range(n)])]


def package(length=2.4,diameter=.8,theta=math.pi,relative=0,n=48):
    """Rotor blade/hub/cage and input slot ring plus two captured bearing plates.
    Torsion rod connects rotor to input. Bearings have true polygonal holes.
    All parts translate in z together; axial shoulders give a positive lift path.
    theta is output angle, relative=input-output; +/-30 degree lost-motion stops.
    y placements intentionally expose depth instead of hiding bearings in boxes.
    """
    out=[]
    def add(name,polys,y0,y1): out.extend((name,p,y0,y1) for p in polys)
    add('blade',[blade(theta)],-.6,.6)
    add('front_collar',[circle(1.2,n)],.6,1.2)
    add('output_shaft',[circle(.6,n)],1.2,2.6)
    add('front_bearing',annulus(.9,1.9,n=n),1.5,2.3)
    add('rotor_hub',[circle(1.2,n)],2.6,3.2)
    add('spring',[circle(diameter/2,n)],3.2,3.2+length)
    # Lug is a 0.6-mm radial, 24-degree tangential cage rooted at rotor hub.
    a=theta-math.pi/2
    add('return_cage',annulus(1.1,1.7,a-math.radians(12),a+math.radians(12),8),2.6,4.+length)
    # Ring slot: lug half-width 12 deg + 30 deg relative travel.
    c=a+relative
    add('input_slot',annulus(1.0,2.0,c+math.radians(42),c+2*math.pi-math.radians(42),n),3.5+length,4.+length)
    add('input_spoke',annulus(.7,1.1,c+math.pi-.3,c+math.pi+.3,8),3.5+length,4.+length)
    add('input_hub',[circle(.8,n)],3.2+length,4.6+length)
    add('rear_collar',[circle(1.2,n)],4.+length,4.6+length)
    add('rear_shaft',[circle(.6,n)],4.6+length,6.+length)
    add('rear_bearing',annulus(.9,1.9,n=n),4.9+length,5.7+length)
    add('rear_cap',[circle(1.2,n)],6.+length,6.6+length)
    for y0,y1 in ((1.5,2.3),(4.9+length,5.7+length)):
        add('bearing_post',[g.rect(.2,1.,4.8,6.8)],y0,y1)
    add('frame_bridge',[g.rect(-1.9,3.1,6.2,6.8)],1.5,5.7+length)
    return out


def collision(a,b,dy=0,dz=0):
    best=(0,None)
    bb=[(name,[(x,z+dz) for x,z in poly],y0+dy,y1+dy) for name,poly,y0,y1 in b]
    bounds=lambda poly:(min(x for x,z in poly),max(x for x,z in poly),min(z for x,z in poly),max(z for x,z in poly))
    bb=[(*v,bounds(v[1])) for v in bb]
    for an,ap,ay0,ay1 in a:
        ax0,ax1,az0,az1=bounds(ap)
        for bn,bp,by0,by1,(bx0,bx1,bz0,bz1) in bb:
            overlap=min(ay1,by1)-max(ay0,by0)
            if overlap<=0 or ax0>=bx1 or bx0>=ax1 or az0>=bz1 or bz0>=az1: continue
            v=overlap*g.area(g.intersect(ap,bp))
            if v>best[0]:best=(v,[an,bn])
    return dict(volume_mm3=best[0],parts=best[1])


def packing(n=48):
    p=package(n=n)
    # Actual input ring/lug contacts: no overlap inside stop interval; a one
    # degree attempted overtravel is a positive finite collision witness.
    slot=lambda rel:[x for x in package(relative=rel,n=n) if x[0]=='input_slot']
    cage=[x for x in p if x[0]=='return_cage']
    inside=max(collision(cage,slot(math.radians(a)))['volume_mm3'] for a in (-30,-15,0,15,30))
    outside=collision(cage,slot(math.radians(31)))['volume_mm3']
    assert inside<1e-8 and outside>0
    same=collision(p,p,dy=P)
    assert same['volume_mm3']>0
    # Staggered high parking is an alternative schedule. All output angles
    # fit the blade radius about pivot; frame top is z=6.8. Includes
    # 0.1-mm size and opposing 0.1-mm z errors, plus a 0.1-mm separation reserve.
    clearance_lift=6.8+.1-(3-.1-math.hypot(LENGTH+.1,.35))+.1
    assert clearance_lift>5.9
    high=collision(p,p,dy=P,dz=clearance_lift)
    assert high['volume_mm3']<1e-8
    # During shared lowering of an active head all neighboring idle heads stay
    # at H. Active ordinary 1.5-mm raised motion needs additional 1.5 clearance.
    parking=clearance_lift+1.5
    return dict(facets=n,depth_mm=max(x[3] for x in p)-min(x[2] for x in p),
                axial_shoulder_nominal_radial_overlap_mm=.3,
                axial_face_gap_mm=.3,angular_stop_deg=30,
                bearing_radial_gap_and_shoulder_overlap_mm={str(e):.3-3*e for e in (.05,.1)},
                inside_stop_collision_mm3=inside,overtravel_collision_mm3=outside,
                adjacent_head_collision=same,park_lift_mm=parking,
                parked_collision=high)


def force_envelope():
    """Series circular PLA torsion rod: T=G J delta/L, J=pi d^4/32.
    G=E/[2(1+nu)] here is an assumed isotropic competitor, not printed PLA.
    Exact side contact gives torque/force Jx = (h-z)*sec(t)^2 + w/2*sec(t)*tan(t).
    Horizontal sliding resistance is [0,Freq]; contact friction is excluded,
    making rejection optimistic. G interval 3:1, shear cap 10 or 20 MPa.
    """
    rows=[]
    contacts={}
    for e in (.05,.1):
        contact=[]
        for err in it.product((-e,e),repeat=7):
            t=terminal(err);b,h,w,ts,v,z,l=err
            jac=((2+h-z)/math.cos(t)**2+(.6+w)/2*math.sin(t)/math.cos(t)**2 if t<0
                 else (LENGTH+l)*math.cos(t)-(.6+w)/2*math.sin(t))
            eps=1e-7
            if abs(t)<2*eps:
                # At the zero-angle corner, left/right derivatives differ.
                # Keep both one-sided contact-lever limits.
                contact.extend(((t,2+h-z),(t,LENGTH+l)))
            else:
                assert abs(jac-(demand(t+eps,err)-demand(t-eps,err))/(2*eps))<1e-6, (err,t,jac)
                contact.append((t,jac))
        contacts[e]=contact
    for e,diameter,length,required in it.product((.05,.1),(.6,.8,1.),(1.2,2.4,4.8,9.6),(.1,.3)):
        contact=contacts[e]
        # Also bound rod diameter and length independently; coherent material
        # bias spans the whole row. Nu fixed .35 is a scenario, not a prior.
        kmin=1000/2.7*math.pi*(diameter-e)**4/(32*(length+e))
        kmax=3000/2.7*math.pi*(diameter+e)**4/(32*(length-e))
        drive=max(t+required*j/kmin for t,j in contact)
        loads=[(kmax*(drive-t)/j,kmax*(drive-t),drive-t) for t,j in contact]
        fmax,_,_=max(loads)
        torque=max(x[1] for x in loads);delta=max(x[2] for x in loads)
        # Maximum shear with same thick-diameter corner as kmax.
        shear=16*torque/(math.pi*(diameter+e)**3)
        energy=.5*kmax*delta**2 # N mm, numerically mJ
        minwall=diameter-e
        known_k=2000/2.7*math.pi*diameter**4/(32*length)
        known_drive=max(t+required*j/known_k for t,j in contact)
        known_peak=max(known_k*(known_drive-t)/j for t,j in contact)
        rows.append(dict(e_mm=e,diameter_mm=diameter,length_mm=length,required_N=required,
                         known_spring_peak_force_N=known_peak,
                         k_min_Nmm_rad=kmin,k_max_Nmm_rad=kmax,drive_deg=math.degrees(drive),
                         peak_force_N=fmax,shear_MPa=shear,stored_mJ=energy,
                         deflection_deg=math.degrees(delta),min_diameter_mm=minwall,
                         recoil_stop_deg=math.degrees(math.asin((P-2*e)/(2*math.hypot(LENGTH+e,(.6+e)/2)))-math.atan((.6+e)/(2*(LENGTH+e))))-45,
                         pass_force=fmax<=1,pass_stress10=shear<=10,pass_stress20=shear<=20,
                         pass_stop=delta<=math.radians(30),pass_min_section=minwall>=.6))
    return rows


def withdrawal():
    # If a dog clamps the output, input reverse motion reaches a HARD shoulder;
    # it must not be mistaken for successful blade return or lift. Witness a
    # blade that stays low while bank indexes into a zero-state next-row dog.
    t=terminal((0,)*7)
    angle=math.radians(75)
    right=[(x+P,z) for x,z in blade(-angle)]
    recoil=g.area(g.intersect(blade(angle),right))
    assert recoil>0
    witness=g.area(g.intersect(blade(t),g.dog(0)))
    assert witness>0
    # Upward tangent contact: vertical force per unit normal force,
    # assuming t remains negative. Absolute bound avoids crediting assistance.
    # Coherent all-80 jam (1N normal scenario), not independent fault averaging.
    ratios={str(mu):abs(math.sin(t))+mu*abs(math.cos(t)) for mu in (.1,.4)}
    return dict(recoil_at_return_shoulders_mm2=recoil,stuck_blade_area_mm2=witness,terminal_deg=math.degrees(t),
                extraction_N_per_80_at_1N_normal={k:80*v for k,v in ratios.items()},
                note='Normal force is a declared 1 N contact scenario, not actuator qualification.')


def timing(park):
    out=[]
    for banks,a in it.product((8,16,20,40,80),(20,100)):
        n=80//banks
        # Same serial reference as E087, now 45 deg approach and 0 terminal
        # as a reference itinerary proxy. Force-dependent overdrive/unwind
        # is omitted; this is not a rigorous timing lower bound.
        angles=(math.pi-APP,-APP,math.pi)
        rotation=sum(2*math.sqrt(q/10000) for q in angles)
        base=6+43*(n*(2*g.move(1.5,a)+rotation+.004)+(n-1)*g.move(P,a))
        # High parking is safe only at row-zero home. Return there raised
        # after 43 serpentine masks; lifting at the final row collides with
        # the neighboring parked package. All full-map banks run in phase.
        parking=2*g.move(park-1.5,a)+g.move((n-1)*P,a)
        out.append(dict(banks=banks,a_m_s2=a,full_reference_s=base+parking,
                        max_masks_under_30_reference=math.floor(math.nextafter((30-6-parking)/((base-6)/43),-math.inf)),
                        synchronous_y_clearance_mm=n*P-9.6,
                        full_route_nominal_clear=n*P>9.6,
                        per_row_unmodelled_time_margin_ms=(30-base-parking)/(43*n)*1000,
                        local35_writer_s=(2*g.move(park-1.5,a)+g.move(4*P,a)+35*(2*g.move(1.5,a)+rotation+.004)+28*g.move(P,a)) if n>=5 else None,
                        complete_channel_allowance_dollars=250/(82*banks)))
    return out


def controls():
    g.self_review()
    # Circular torsion limit and numerical energy derivative independently
    # recover T. Isotropic assumption intentionally does not establish X1C.
    G,J,L,d=500,math.pi*.8**4/32,2.4,.1
    energy=lambda x:G*J*x*x/(2*L)
    h=1e-6
    assert abs((energy(d+h)-energy(d-h))/(2*h)-G*J*d/L)<1e-9
    assert energy(0)==0
    # Independent straight-edge equation against polygon demand in contact.
    for t in (-.2,-.1,0):
        assert abs(demand(t,(0,)*7)-(.6+2*math.tan(t)+.3/math.cos(t)+.4))<1e-12
    for t in (.01,.1,.2):
        assert abs(demand(t,(0,)*7)-(.6+LENGTH*math.sin(t)+.3*math.cos(t)+.4))<1e-12


if __name__=='__main__':
    controls()
    geom=[geometry(e,n) for e,n in it.product((.05,.1),(20,40,80))]
    pack=[packing(n) for n in (24,48,96)]
    forces=force_envelope()
    survivors=[r for r in forces if all(r[k] for k in ('pass_force','pass_stress20','pass_stop','pass_min_section'))]
    print(json.dumps(dict(geometry=geom,package=pack,force_cases=forces,
                         survivors=survivors,withdrawal=withdrawal(),timing=timing(pack[-1]['park_lift_mm'])),indent=2))
