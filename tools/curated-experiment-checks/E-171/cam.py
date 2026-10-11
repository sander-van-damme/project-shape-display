#!/usr/bin/env python3
"""Finite cap and helical-sector cam discriminator. Units mm, N, rad.
Rigid bounded scenarios; Coulomb friction is a scenario, not a process prior.
No material, manufacturing, dynamic arrest or whole-machine qualification.
"""
import json
import math

P, D = 5.08, 4.6

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def box(theta=0.,h=0.,e=0.,c=0.,neighbor=False):
    half=(D/2+e,D/2+e,1+e)
    if neighbor:
        alpha=math.atan(2*c/25)
        axes=((math.cos(alpha),0,math.sin(alpha)),(0,1,0),
              (-math.sin(alpha),0,math.cos(alpha)))
        center=(P-e-c*(1+2*43/25),0,43.)
    else:
        axes=((math.cos(theta),math.sin(theta),0),
              (-math.sin(theta),math.cos(theta),0),(0,0,1))
        center=(0,0,43+h)
    return center,axes,half

def hit(a,b):
    ca,aa,ha=a; cb,ab,hb=b
    for axis in (*aa,*ab,*(cross(x,y) for x in aa for y in ab)):
        if dot(axis,axis)<1e-20: continue
        reach=sum(h*abs(dot(axis,u)) for h,u in zip(ha,aa))
        reach+=sum(h*abs(dot(axis,u)) for h,u in zip(hb,ab))
        if abs(dot(sub(ca,cb),axis))>=reach-1e-11: return False
    return True

def bisect_first(pred,lo,hi):
    assert not pred(lo) and pred(hi)
    for _ in range(45):
        mid=(lo+hi)/2
        if pred(mid): hi=mid
        else: lo=mid
    return (lo+hi)/2

def axial_interval(a,b):
    # Independent continuous SAT interval for translating A along +z.
    ca,aa,ha=a; cb,ab,hb=b
    lo,hi=-math.inf,math.inf
    for axis in (*aa,*ab,*(cross(x,y) for x in aa for y in ab)):
        if dot(axis,axis)<1e-20: continue
        reach=sum(h*abs(dot(axis,u)) for h,u in zip(ha,aa))
        reach+=sum(h*abs(dot(axis,u)) for h,u in zip(hb,ab))
        d=dot(sub(ca,cb),axis); az=axis[2]
        if abs(az)<1e-12:
            if abs(d)>=reach: return None
        else:
            ends=sorted(((-reach-d)/az,(reach-d)/az))
            lo=max(lo,ends[0]);hi=min(hi,ends[1])
    return (lo,hi) if lo<hi else None

def clearance(e,c,n):
    neighbor=box(e=e,c=c,neighbor=True)
    onset=bisect_first(lambda t:hit(box(t,e=e),neighbor),0,math.pi/4)
    alpha=math.atan(2*c/25)
    # Exact top envelope gives a sufficient lift at every angle.
    clear=(1+e)*(1+math.cos(alpha))+(D/2+e)*math.sin(alpha)
    # At a fixed angle, the collision interval is convex in axial translation.
    # Resolve its upper end, including onset-adjacent holdouts.
    angles=[onset+(math.pi/4-onset)*i/n for i in range(1,n+1)]
    angles += [onset+d for d in (1e-8,1e-7,1e-6,1e-5)]
    worst=(0.,0.,0.)
    for t in angles:
        if not hit(box(t,e=e),neighbor): continue
        interval=axial_interval(box(t,e=e),neighbor)
        assert interval is not None and interval[0]<0<interval[1]
        height=interval[1]
        worst=max(worst,(height/t,t,height))
    k,t,h=worst
    return dict(e=e,c=c,intervals=n,onset_deg=math.degrees(onset),
                sufficient_clear_lift=clear,necessary_k_witness=k,
                witness_angle_deg=math.degrees(t),witness_lift=h,
                sufficient_k=clear/onset,
                friction_ceiling_circle=P/2/k,friction_ceiling_square=P/math.sqrt(2)/k)

def reaction(k,r,mu,F,sign):
    # Local unwrapped helix: tangent (1,m), normal (-m,1).
    # +/- sliding gives R=N*(normal -/+ mu*tangent)/sqrt(1+m*m).
    m=k/r; den=1-sign*mu*m
    if den<=0: return None
    N=F*math.sqrt(1+m*m)/den
    torque=F*r*(m+sign*mu)/den
    rx=N*(-m-sign*mu)/math.sqrt(1+m*m)
    rz=N*(1-sign*mu*m)/math.sqrt(1+m*m)
    assert abs(rx+torque/r)<1e-9 and abs(rz-F)<1e-9
    return dict(normal=N,torque=torque)

def sectors(k,H,n):
    # Two opposed finite annular shoes, r=1.75..2.25, u=0..0.2 rad.
    # Ground top z=k*(phi-beta). Shoe bottom z=h+k*(u-beta),
    # flat top z=h+1.2. At rotation theta, phi=u+theta and h=k*theta.
    # All solids terminate below/above these respective contact surfaces.
    beta=.2; rin=1.75; rout=2.25; end=H/k
    max_residual=0.; checks=0
    for i in range(n+1):
        theta=end*i/n; h=k*theta
        for j in range(17):
            u=beta*j/16
            for r in (rin,(rin+rout)/2,rout):
                for phase in (0,math.pi):
                    phi=u+theta+phase
                    # Actual Cartesian surface points, finite radial/angle extent.
                    p=(r*math.cos(phi),r*math.sin(phi),h+k*(u-beta))
                    ground=k*(math.atan2(p[1],p[0])-phase-beta)
                    # atan2 wraps second sector; unwrap to its known interval.
                    while ground < -k*beta-1e-9: ground+=2*math.pi*k
                    max_residual=max(max_residual,abs(p[2]-ground)); checks+=1
        assert beta+end<math.pi # opposed shoe/ground sectors remain disjoint
    assert max_residual<1e-10
    # 10-mm station spacing leaves finite gap under matching periodic shoes.
    thickness=1.2+k*beta
    # Attempt to continue rotation at the desired 2.3-mm plateau. A finite
    # shoe remains over the rising track: this interior point penetrates.
    theta=end+beta/2; u=beta/4
    ground_z=k*(theta+u-beta)
    bottom_z=H+k*(u-beta)
    penetration=ground_z-bottom_z
    assert abs(penetration-k*beta/2)<1e-12 and penetration>0
    return dict(k=k,lift=H,angle_deg=math.degrees(end),checks=checks,
                contact_residual=max_residual,shoe_max_thickness=thickness,
                station_axial_gap=10-thickness,
                projected_contact_area=(rout*rout-rin*rin)*beta,
                lowest_cap_intrusion=H-2,plateau_penetration=penetration,
                height_at_last_ground_contact=H+k*beta,
                # The crest endpoint lies within the stationary lowest cap.
                crest_xy=(rout*math.cos(beta+end),rout*math.sin(beta+end)))

def main():
    a=box(); assert hit(a,a)
    assert not hit(a,box(h=2)) and hit(a,box(h=2-1e-6))
    assert not hit(a,box(neighbor=True))
    results=[clearance(e,c,n) for e,c in ((0,0),(.025,0),(.05,0),(.025,.025),(.05,.025))
             for n in (64,256,1024)]
    # Independent nominal projection formula and prism lift bound.
    nominal=results[2]
    theta=math.radians(nominal['onset_deg'])
    assert abs(D/2*(math.cos(theta)+math.sin(theta)+1)-P)<1e-9
    assert abs(nominal['necessary_k_witness']-2/theta)<2e-6
    for e,c in ((0,0),(.05,.025)):
        row=[x for x in results if x['e']==e and x['c']==c][-1]
        t=math.radians(row['witness_angle_deg']); h=row['witness_lift']
        neighbor=box(e=e,c=c,neighbor=True)
        assert hit(box(t,h-1e-6,e=e),neighbor)
        assert not hit(box(t,h+1e-6,e=e),neighbor)
        independent=bisect_first(lambda z:not hit(box(t,z,e=e),neighbor),0,3)
        assert abs(independent-h)<1e-6
        # Even the steepest raisable sliding cam at mu=.2 and maximal radius
        # lies below the collision height in the adverse case.
        if e:
            assert hit(box(t,(P/math.sqrt(2)/.2)*t,e=e),neighbor)
    # Robust off-threshold counterexample, independently checked by a point
    # strictly inside BOTH oriented prisms (not another SAT invocation).
    t=math.radians(6); height=P/math.sqrt(2)/.2*t
    active=box(t,height,e=.05); neighbor=box(e=.05,c=.025,neighbor=True)
    x=2.35*(math.cos(t)+math.sin(t))-.005
    y=2.35*(math.sin(t)-math.cos(t))+.005
    point=(x,y,43.95)
    margins=[]
    for center,axes,halves in (active,neighbor):
        local=[abs(dot(sub(point,center),axis)) for axis in axes]
        margins.extend(h-q for h,q in zip(halves,local))
    assert min(margins)>0 and hit(active,neighbor)
    interior_witness=dict(angle_deg=6,lift=height,point=point,
                          minimum_face_margin=min(margins))
    # Desired cap-only path with saturated lift; actual 3-D cap prisms,
    # both advance and exact retrace, neighbor stays grounded. This is NOT
    # a cam-driven witness: finite shoes reject the plateau below.
    path_checks=[]
    for e,c,k in ((0,0,10.),(.05,.025,24.)):
        for n in (64,256,1024):
            hits=0
            for i in range(n+1):
                t=math.pi/2*i/n
                hits+=hit(box(t,min(k*t,2.3),e=e),box(e=e,c=c,neighbor=True))
            assert hits==0
            path_checks.append(dict(e=e,c=c,k=k,intervals=n,hits=hits))
    contact=[sectors(k,2.3,n) for k in (10.,24.) for n in (16,64,256)]
    for row in contact:
        assert max(abs(x) for x in row['crest_xy'])<D/2
        assert row['lowest_cap_intrusion']>0 # finite crest penetrates cap
    forces=[]
    for k in (10.,24.):
        for mu in (0.,.05,.1,.2,.4):
            for F in (.1,1.,10.):
                forces.append(dict(k=k,mu=mu,F=F,r=2.,
                    raising=reaction(k,2.,mu,F,1),lowering=reaction(k,2.,mu,F,-1)))
    # Work and dimensional checks. Zero friction: tau*dtheta = F*dh.
    for k in (10.,24.):
        assert abs(reaction(k,2.,0,10,1)['torque']*(2.3/k)-23)<1e-12
    # A small-slope self-hold control vs steep backdriving transfer cams.
    assert reaction(.2,2.,.2,1,-1)['torque']<0
    assert reaction(10,2.,.2,1,-1)['torque']>0
    # In raising, exact dissipation plus potential equals motor work.
    k,r,mu,F,H=10.,2.,.1,1.,2.3
    rr=reaction(k,r,mu,F,1); sliding=H/k*math.sqrt(r*r+k*k)
    assert abs(rr['torque']*H/k-F*H-mu*rr['normal']*sliding)<1e-10
    print(json.dumps(dict(interior_collision_witness=interior_witness,clearance=results,target_cap_paths=path_checks,finite_sectors=contact,
        force_scenarios=forces,free_return_energy_Nmm={str(F):F*2.3 for F in (.1,1,10)},
        sites=6400,opposed_cam_tracks=12800,periodic_shoes=128000),indent=2))

if __name__=='__main__': main()
