"""E-087 finite rotary sections and carrier routes; mm, N, s.
All dimensions/errors/rates are declared scenarios, not fabrication priors.
Standard library; deterministic, no fitted distributions or dynamics solver.
"""
import itertools as it
import json
import math

P, D, W = 5.08, 1.2, .8


def clip(poly, normal, bound):
    if not poly:
        return []
    out = []
    a = poly[-1]
    da = sum(v*n for v,n in zip(a,normal))-bound
    for b in poly:
        db = sum(v*n for v,n in zip(b,normal))-bound
        if (da <= 0) != (db <= 0):
            u = da/(da-db)
            out.append(tuple(x+u*(y-x) for x,y in zip(a,b)))
        if db <= 0:
            out.append(b)
        a, da = b, db
    return out


def area(poly):
    return abs(sum(a[0]*b[1]-a[1]*b[0]
                   for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0.


def intersect(a,b):
    # b must be CCW; all constructors below are CCW.
    for p,q in zip(b,b[1:]+b[:1]):
        normal=(q[1]-p[1],p[0]-q[0])
        a=clip(a,normal,normal[0]*p[0]+normal[1]*p[1])
    return a


def rect(x0,x1,z0,z1):
    return [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]


def paddle(theta, height=3., length=3., width=.6, center=.6):
    # Pivot at s=0, radial coordinate s points down at theta=0.
    s,c=math.sin(theta),math.cos(theta)
    return [(center+u*c+v*s,height+u*s-v*c)
            for u,v in ((-width/2,length),(width/2,length),(width/2,0),(-width/2,0))]


def band(poly):
    return clip(clip(poly,(0,-1),0),(0,1),1)


def demand(poly, reset=False):
    b=band(poly)
    if not b:
        return None
    return min(x for x,z in b)-W/2 if reset else max(x for x,z in b)+W/2


def dog(x):
    return rect(x-W/2,x+W/2,0,1)


def root(f,lo,hi):
    assert f(lo)*f(hi)<=0
    for _ in range(70):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0:
            hi=mid
        else:
            lo=mid
    return (lo+hi)/2


THETA = root(lambda t:demand(paddle(t))-D,math.radians(-10),0)
APPROACH=math.radians(-35)
LIFT=1.5


def stopped_path(old,command,n):
    """Retained endpoint, unilateral quasi-static push, no compliance credit."""
    x=old*D
    reset=command=='reset'
    sign=-1 if reset else 1
    out=[]
    # Program while lifted; lower outside dog; turn; lift at terminal; neutral.
    for stage in range(5):
        for i in range(n+1):
            u=i/n
            start,terminal=sign*APPROACH,sign*THETA
            angle=(math.pi+(start-math.pi)*u if stage==0 else start if stage==1 else
                   start+(terminal-start)*u if stage==2 else terminal if stage==3
                   else terminal+(math.pi-terminal)*u)
            h=LIFT if stage in (0,4) else LIFT*(1-u) if stage==1 else LIFT*u if stage==3 else 0
            if command=='bypass':
                angle=math.pi
            poly=paddle(angle,height=3+h)
            if stage==2 and command!='bypass':
                q=demand(poly,reset)
                if q is not None:
                    x=min(x,q) if reset else max(x,q)
            assert -1e-9<=x<=D+1e-9
            assert area(intersect(poly,dog(x)))<1e-8
            for col,state in it.product((-1,1),(0,1)):
                assert area(intersect(poly,dog(col*P+state*D)))<1e-8
            out.append((angle,h,x))
    assert abs(x-(old*D if command=='bypass' else 0 if reset else D))<1e-8
    return out


def stopped_checks(n):
    paths={(o,c):stopped_path(o,c,n) for o,c in it.product((0,1),('set','reset','bypass'))}
    # Independently phased neighbors: global x envelopes are disjoint for all
    # theta in +/-35 deg during the active stroke; programming is below.
    lateral_radius=3*math.sin(abs(APPROACH))+.3*math.cos(APPROACH)
    assert 2*lateral_radius<P
    # All programming angles stay in [-35,180] degrees. A full radius-3.015
    # disk around the left pivot cannot reach the right paddle's swept sector:
    # closest centerline approach is P*cos(35), minus half-width. Common lift
    # keeps pivot heights equal. This proves arbitrary independent phases.
    assert P*math.cos(APPROACH)-.3>math.hypot(3,.3)
    maps=list(it.product((0,1),repeat=4))
    for old,new in it.product(maps,repeat=2):
        result=[round(paths[o,'bypass' if o==v else 'set' if v else 'reset'][-1][2]/D)
                for o,v in zip(old,new)]
        assert result==list(new)
    # A failed lift leaves the blade intersecting the next reset-state dog.
    stuck=area(intersect(paddle(THETA),dog(0)))
    assert stuck>0
    return dict(steps_per_stage=n,paths=6,maps=256,terminal_deg=math.degrees(THETA),
                active_paddle_x_gap_mm=P-2*lateral_radius,
                programming_circle_sector_gap_mm=P*math.cos(APPROACH)-.3-math.hypot(3,.3),
                stuck_lift_intersection_mm2=stuck,
                max_final_error_mm=max(abs(v[-1][2]-round(v[-1][2]/D)*D) for v in paths.values()))


def uncertainty():
    rows=[]
    for e in (0,.05,.10,.20):
        demands=[]
        insertion=[]
        for b,h,dw,t in it.product((-e,e),repeat=4):
            # Independent bounded pivot x/z, full blade width and dog endpoint.
            poly=paddle(THETA,height=3+h,width=.6+dw,center=.6+b)
            demands.append(demand(poly)-(D+t))
            insertion.append(t-demand(paddle(APPROACH,height=3+h,width=.6+dw,center=.6+b)))
        rows.append(dict(e_mm=e,min_endpoint_mismatch_mm=min(demands),
                         max_endpoint_mismatch_mm=max(demands),
                         min_capture_gap_mm=min(insertion)))
    # Independent straight-edge support function at the dog top, valid here.
    expected=.6+(3-1)*math.tan(THETA)+.3/math.cos(THETA)+W/2
    assert abs(expected-D)<1e-12
    coeff=2+abs(math.tan(THETA))+.5/math.cos(THETA)
    for row in rows:
        assert abs(row['max_endpoint_mismatch_mm']-row['e_mm']*coeff)<1e-12
        assert abs(row['min_endpoint_mismatch_mm']+row['e_mm']*coeff)<1e-12
    return rows


def retained_wedge(n=160):
    """Ternary fixed-angle paddle: stored +/-alpha/up; shared vertical energy.
    Only nominal edge contacts; individual retention/torque latch is absent.
    """
    alpha=math.radians(15)
    h=1+(.3-.2*math.cos(alpha))/math.sin(alpha)
    stroke=D/math.tan(alpha)
    clearance=1.5
    length=6.
    for old,reset in it.product((0,1),(False,True)):
        x=old*D
        for phase in (0,1):
            for i in range(n+1):
                u=i/n if phase==0 else 1-i/n
                poly=paddle(alpha if reset else -alpha,height=h+(stroke+clearance)*(1-u),length=length)
                q=demand(poly,reset)
                if phase==0 and q is not None:
                    x=min(x,q) if reset else max(x,q)
                assert -1e-9<=x<=D+1e-9
                assert area(intersect(poly,dog(x)))<1e-8
                for col,state in it.product((-1,1),(0,1)):
                    assert area(intersect(poly,dog(col*P+state*D)))<1e-8
        assert abs(x-(0 if reset else D))<1e-8
    up=paddle(math.pi,height=h,length=length)
    assert all(area(intersect(up,dog(x)))<1e-8 for x in (0,D))
    # To program reset(+15) -> bypass(180) in bounded [-15,180], sweep through
    # +90. Adjacent bypass arm intersects it even with all outputs cleared.
    witness=0
    angle_at=0
    for i in range(n+1):
        angle=alpha+(math.pi-alpha)*i/n
        a=paddle(angle,height=h+stroke+clearance,length=length)
        b=paddle(math.pi,height=h+stroke+clearance,length=length,center=.6+P)
        overlap=area(intersect(a,b))
        if overlap>witness:
            witness,angle_at=overlap,math.degrees(angle)
    assert witness>0
    # Program set -> reset passes through theta=0; at the lowered pivot it
    # intersects either endpoint, requiring a separate programming clearance.
    low_program=max(area(intersect(paddle(0,height=h,length=length),dog(x))) for x in (0,D))
    assert low_program>0
    return dict(alpha_deg=15,pivot_mm=h,contact_stroke_mm=stroke,total_lift_mm=stroke+clearance,length_mm=length,
                transit_pivot_mm=h+stroke+clearance,
                vertical_sweep_mm=stroke+clearance+math.hypot(length,.3)+length*math.cos(alpha)+.3*math.sin(alpha),
                bypass_program_collision_mm2=witness,collision_angle_deg=angle_at,
                lowered_program_collision_mm2=low_program,
                below_dog_tip_mm=h-length*math.cos(alpha)-.3*math.sin(alpha),
                shared_downforce_N_at_80_times_point3N={str(mu):80*.3*(math.tan(alpha)+mu)/(1-mu*math.tan(alpha)) for mu in (.1,.4)})


def route_checks():
    """Finite y-z payloads, distinct from ungenerated track/bearing structures.
    Racetrack centerlines have radius R; rigid carrier rotates with tangent.
    Rectangular ferry is lifted before horizontal travel, one per bank.
    """
    radius,depth,height=6.,1.2,3.6
    def turning(t,center_y=0,center_z=radius):
        # right semicircle starts at bottom theta=-pi/2, tangent along +y
        y,z=center_y+radius*math.cos(t),center_z+radius*math.sin(t)
        ty,tz=-math.sin(t),math.cos(t)
        ny,nz=-tz,ty
        return [(y+u*ty+v*ny,z+u*tz+v*nz) for u,v in
                ((-depth/2,-height/2),(depth/2,-height/2),(depth/2,height/2),(-depth/2,height/2))]
    # Active-bank turn leaving its last row at y=0 and a neighboring bank
    # parked on the bottom run at y=P. Find actual polygon intersection.
    parked=rect(P-depth/2,P+depth/2,-height/2,height/2)
    best=(0,0)
    for i in range(721):
        t=-math.pi/2+math.pi*i/720
        a=area(intersect(turning(t),parked))
        if a>best[0]: best=(a,t)
    # Nominal example may miss parked bottom but independent neighboring turn
    # has an exact crossing: two facing equal-radius arcs with centers P apart.
    y=P/2
    z=radius-math.sqrt(radius**2-y**2)
    t=math.atan2(z-radius,y)
    a=turning(t)
    # Mirror first payload about y=P/2, reverse to restore CCW.
    b=list(reversed([(P-y,z) for y,z in a]))
    cross=area(intersect(a,b))
    assert cross>0
    # Independent one-head rectangular ferry never leaves its bank row centers.
    # 1.2-mm longitudinal payload extent leaves this gap at the boundary,
    # with +/-e rigid rail offsets and full-depth error +/-e on both heads.
    gap={str(e):P-depth-3*e for e in (0,.1,.2)}
    assert min(gap.values())>0
    return dict(radius_mm=radius,payload_yz_mm=[depth,height],
                adjacent_turn_collision_mm2=cross,collision_center_yz_mm=[y,z],
                parked_bottom_collision_mm2=best[0],
                ferry_neighbor_gap_mm=gap,
                loop_longitudinal_extension_mm=2*math.hypot(radius+height/2,depth/2),
                loop_longitudinal_envelope_formula='(n-1)*5.08+2*hypot(6+1.8,.6) mm')


def move(distance_mm,acceleration):
    return 2*math.sqrt(distance_mm/1000/acceleration)


def timing():
    rows=[]
    for banks,a in it.product((1,4,8,16,20,40,80),(20,100)):
        n=80//banks
        # Favourable lower bounds: zero data-setting/readback/rotary time, no
        # velocity cap, actual nominal lifts, 6 s external allowance.
        # Retained wedge needs 4.478-mm contact stroke plus 1.5-mm clearance.
        # Ferry returns to stationary setter at row0 after EVERY written row.
        ferry_lift=D/math.tan(math.radians(15))+1.5
        ferry=43*sum(2*move(j*P,a)+2*move(ferry_lift,a) for j in range(n))+6
        # Stopped head can retain its position and write successive rows.
        stopped=43*(n*2*move(LIFT,a)+(n-1)*move(P,a))+6
        angular_accel=10000.  # rad/s2, unqualified scenario
        angular_time=sum(2*math.sqrt(d/angular_accel) for d in
                         (math.pi-APPROACH,THETA-APPROACH,math.pi-THETA))
        stopped_scenario=stopped+43*n*(angular_time+.004)
        rows.append(dict(banks=banks,a_m_s2=a,stopped_lower_bound_s=stopped,
                         stopped_serial_scenario_s=stopped_scenario,
                         ferry_lower_bound_s=ferry,channels=82*banks,
                         residual_channel_dollars=250/(82*banks)))
    # 35 writes in five-row local patch, seven mask changes. Most favorable
    # patch at setter rows0..4; farthest patch at rows5..9 in an eight-bank layout.
    local=[]
    for offset in (0,5):
        for a in (20,100):
            t=7*sum(2*move(j*P,a)+2*move(D/math.tan(math.radians(15))+1.5,a) for j in range(offset,offset+5))
            local.append(dict(first_row=offset,a_m_s2=a,ferry_motion_only_s=t))
    return rows,local


def self_review():
    assert abs(area(intersect(rect(0,2,0,2),rect(1,3,1,3)))-1)<1e-12
    assert area(intersect(rect(0,1,0,1),rect(2,3,0,1)))==0
    # Analytic rectangle area invariant under rotation.
    for angle in range(-180,181):
        assert abs(area(paddle(math.radians(angle)))-1.8)<1e-12
    # Demand agrees with independent straight edge equation across the driven
    # range; sampling is a calculation check, not continuous contact validation.
    for i in range(301):
        t=APPROACH+(THETA-APPROACH)*i/300
        exact=.6+2*math.tan(t)+.3/math.cos(t)+W/2
        assert abs(demand(paddle(t))-exact)<1e-12
    for command in ('set','reset'):
        stopped_path(.5,command,80)
    alpha=math.radians(15)
    assert abs((.3*math.tan(alpha))*(D/math.tan(alpha))-.3*D)<1e-12
    assert move(0,20)==0
    assert abs(move(4,20)/move(1,20)-2)<1e-12
    assert abs(move(1,80)/move(1,20)-.5)<1e-12


if __name__=='__main__':
    self_review()
    full,local=timing()
    print(json.dumps(dict(stopped=[stopped_checks(n) for n in (40,80,160)],
                          errors=uncertainty(),retained=[retained_wedge(n) for n in (80,160,320)],
                          routes=route_checks(),full_time_bounds=full,local_time_bounds=local),indent=2))
