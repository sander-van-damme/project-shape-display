"""E-177. Finite cam section and optimistic guided-follower screen; mm/N/s.
No calibrated process distributions. Leaf law is linear elastic, quasistatic.
The shoe's ideal X guide is explicitly an additional unresolved interface.
"""
import itertools as it
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-176'))
import reset
lane = reset.lane

# Connected cam/pad; the flat shoe broadens the apex into a .8-mm plateau.
# Cam is a convex XY polygon extruded through Z.
PITCH=5.08
SLOPE=.4
HALFWIDTH=.4
YC=1.3
PEAK=.45
X0=-1.85

def profile(u):
    return -1.75+.34-SLOPE*abs(u-PEAK)

def front(q):
    u=min(max(PEAK,YC-q-HALFWIDTH),YC-q+HALFWIDTH)
    return profile(u)

def poly_box(x,y):
    return [(x[0],y[0]),(x[1],y[0]),(x[1],y[1]),(x[0],y[1])]

def cam(q,d):
    # Extend .2 mm beyond both actual corner-contact positions.
    us=(-.2,PEAK,1.1)
    return ([(-2.2,q+us[0]),*( (profile(u),q+u) for u in us),
             (-2.2,q+us[-1])],(d-2.4,d-1.4))

def boxpart(b):return (poly_box(b[0],b[1]),b[2])

def intersects(a,b):
    # Strict separating-axis polygon test, exact for convex sections.
    if lane.overlap(a[1],b[1])<1e-10:return False
    for p in (a[0],b[0]):
        for u,v in zip(p,p[1:]+p[:1]):
            axis=(u[1]-v[1],v[0]-u[0])
            pa=[x*axis[0]+y*axis[1] for x,y in a[0]]
            pb=[x*axis[0]+y*axis[1] for x,y in b[0]]
            if min(max(pa),max(pb))-max(min(pa),min(pb))<=1e-10:return False
    return True

def shift(part,dx,dy):return ([(x+dx,y+dy) for x,y in part[0]],part[1])

def section(q,d):
    face=front(q)
    # Conservative envelope of the monotonically deflected .6 x .8 leaf.
    # The root is 8 mm below the shoe; profile tilt/coupling not qualified.
    return dict(cam=cam(q,d),
        neck=boxpart(lane.box((-2.2,-1.85),(q-.4,q+.4),(d-1.4,d-1))),
        shoe=boxpart(lane.box((face,face+.6),(.9,1.7),(d-2.4,d-1.4))),
        leaf_envelope=boxpart(lane.box((X0,face+.6),(.9,1.7),(d-10.4,d-2.4))),
        root=boxpart(lane.box((-1.85,-.8),(.9,1.7),(d-10.9,d-10.4))),
        rail=boxpart(lane.box((-1.1,-.8),(-8,8),(d-10.9,d-10.4))))

def geometry(n):
    # Best-case local keeper section, all neighbor heights and pad extremes.
    # Full leaf envelope is intentionally conservative, cam geometry exact.
    count=0;collisions=set()
    qs=sorted(set([0.,.45,.85,1.25,1.7]+[1.7*i/n for i in range(n+1)]))
    for q,d in it.product(qs,(-2.,0.,8.,20.,45.4)):
        parts=section(q,d)
        for name,part in parts.items():
            for comb_part in reset.comb(-.9):
                if intersects(part,boxpart(comb_part)):collisions.add((name,'parked_comb'))
            for dx,dy in it.product((-PITCH,0,PITCH),repeat=2):
                for j,p in it.product(range(5),(0.,1.7)):
                    # Columns may occupy any intended height. Excludes pad/lip
                    # intended support collision by testing keeper additions only.
                    col,dog,pad=lane.solids(j*lane.P,lane.LANES[j],d,p,(0.,)*5,0.,1.)
                    for obj in col+[dog]:
                        if intersects(part,shift(boxpart(obj),dx,dy)):
                            collisions.add((name,'column_or_dog'))
                    if (dx or dy) and intersects(part,shift(boxpart(pad),dx,dy)):
                        collisions.add((name,'neighbor_pad'))
            count+=1
        # Cam and shoe touch; they never penetrate in the granted X guide.
        assert not intersects(parts['cam'],parts['shoe'])
        assert abs(front(q)-max(profile(YC-q-HALFWIDTH),profile(YC-q+HALFWIDTH),
            profile(PEAK) if YC-q-HALFWIDTH<=PEAK<=YC-q+HALFWIDTH else -math.inf))<1e-12
    return dict(poses=count,collisions=sorted(collisions))

def stiffness(E=2000.,w=.8,t=.6,L=8.):return E*w*t**3/(4*L**3)

def flank_force(delta,mu=.2,drag=.001,k=None,m=SLOPE):
    """Force on an inclined flank; delta is spring deflection, not pad state."""
    k=stiffness() if k is None else k
    spring=k*delta
    return dict(spring=spring,drive=spring*(m+mu)/(1-mu*m)+drag,
                completion=spring*(m-mu)/(1+mu*m)-drag)

def mechanical_checks():
    k=stiffness();delta_end=front(0)-X0;delta_peak=front(.85)-X0
    # Independent unit-load integral: int M^2/(2EI) dz = F^2 L^3/(6EI).
    E,w,t,L=2000.,.8,.6,8.;I=w*t**3/12
    f=k*delta_peak
    u=.5*k*delta_peak**2
    assert math.isclose(u,f*f*L**3/(6*E*I))
    # Independent 2D contact equilibrium for ascent and descent of a ramp.
    for mu in (0.,.1,.2,.4,.6):
        for sgn in (-1,1):
            m=.4;S=.07
            normal=S*math.sqrt(1+m*m)/(1-sgn*mu*m)
            x=normal*(1-sgn*mu*m)/math.sqrt(1+m*m)
            y=normal*(m+sgn*mu)/math.sqrt(1+m*m)
            assert math.isclose(x,S)
            assert math.isclose(y,S*(m+sgn*mu)/(1-sgn*mu*m))
    # Friction-free work integrated across each affine flank.
    def energy(q):return .5*k*(front(q)-X0)**2
    for a,b in ((0.,.45),(1.25,1.7)):
        derivative=(energy(b)-energy(a))/(b-a)
        signed=SLOPE if a==0 else -SLOPE
        hand=k*((front(a)+front(b))/2-X0)*signed
        assert math.isclose(derivative,hand,abs_tol=1e-12)
    return dict(k=k,end_deflection=delta_end,peak_deflection=delta_peak,
        barrier_Nmm=u-energy(0),root_strain=1.5*t*delta_peak/L**2,
        tip_rotation=1.5*delta_peak/L,
        free_tip_y_drift_flank_mu02=(flank_force(front(.45)-X0)['drive']-.001)/(E*t*w**3/(4*L**3)))

def routes():
    # Opposite-side arm finger pushes q downward, same height as pad.
    # A positive-volume witness defeats a full-column outer shaft route.
    outer=lane.box((-2.8,-2.5),(2.5,2.9),(-45.,-2.2))
    overlap=lane.volume(outer,reset.comb(-.9)[2])
    assert overlap>0
    inner=boxpart(lane.box((-1.1,-.8),(1.35,1.75),(-45.,-2.2)))
    assert intersects(inner,section(.85,-2.)['shoe'])
    # Thin alternative in the .3-mm corridor between rail and pad/cam.
    thin=(-2.45,-2.25)
    assert math.isclose(thin[0]-(-2.5),.05)
    # Crest width causes .8-mm capture plateau: reset must exceed q=1.25.
    windows=[]
    for e,b in it.product((0.,.025,.05,.075,.1),(.0,.025,.05,.1)):
        lo=1.25+e+b;hi=1.7-e-b
        windows.append(dict(e=e,b=b,low=lo,high=hi,positive=lo<hi,
                            inherited_command_135=(lo<1.35<hi)))
    return dict(outer_post_comb_intersection_mm3=overlap,
                inner_post_shoe_collision=True,thin_post_mm=.2,nominal_thin_post_gap_mm=.05,
                positive_independent_edge_bound_below_mm=.0125,
                capture_windows=windows)

def interface_checks(n):
    count=0
    for q0 in (0.,1.7):
        # Shared reset at home, followed by independent opposite-side arm.
        for i in range(n+1):
            face=-.9+2.1*i/n
            q=max(q0,face+.5)
            assert all(not intersects(p,boxpart(c)) for p in section(q,-2.).values()
                       for c in reset.comb(face))
            count+=1
        for i in range(n+1):
            face=2.6-2.1*i/n
            q=min(q0,face-.5)
            tooth=lane.box((-2.15,-1.35),(face,face+.4),(-2.8,-2.2))
            assert all(not intersects(p,boxpart(tooth)) for p in section(q,-2.).values())
            pad=lane.solids(0,lane.LANES[0],-2.,q,(0.,)*5,0.,1.)[2]
            assert lane.volume(tooth,pad)<1e-10
            count+=1
    # Continuous keeper-neighbor separation follows XY envelopes and shared Z.
    # Test all piecewise-linear breakpoints as a separate neighbor holdout.
    for q,r in it.product((0.,.45,1.25,1.7),repeat=2):
        a=section(q,-2.);b=section(r,-2.)
        for dx,dy in it.product((-PITCH,0,PITCH),repeat=2):
            if dx==dy==0:continue
            for an,ap in a.items():
                for bn,bp in b.items():
                    # Shared rail/root bonds are intentional along Y.
                    if dx==0 and {an,bn}<={'rail','root'}:continue
                    assert not intersects(ap,shift(bp,dx,dy)),(an,bn,dx,dy)
    return count


def rail_bound():
    # Favorable simply supported continuous bank rail; no transverse bracing.
    E=2000.;I=.5*.3**3/12;EI=E*I;L=20*PITCH
    load=stiffness()*(front(.85)-X0)
    distributed=load/PITCH
    # Compute compliance numerator before dividing by EI. Limit displacement
    # to .05 mm; huge linear extrapolations are NOT physical deflection claims.
    smooth=5*distributed*L**4/384
    discrete=sum(load*min(a,L-a)*(3*L*L-4*min(a,L-a)**2)/48
                 for a in [(i+.5)*PITCH for i in range(20)])
    assert abs(discrete/smooth-1)<.01
    return dict(rail_EI_Nmm2=EI,required_EI_for_005mm=discrete/.05,
        stiffness_shortfall_factor=discrete/(.05*EI),
        max_uniform_unbraced_span_mm=(.05*384*EI/(5*distributed))**.25,
        point_vs_uniform_ratio=discrete/smooth)

def main():
    geom=[geometry(n) for n in (1,4,16)]
    assert all(not g['collisions'] for g in geom)
    mech=mechanical_checks()
    cases=[]
    # Bounded epistemic scenarios; corners may be coherent across all bank cells.
    for E,t,L,mu,drag,preload_error in it.product((1000.,3000.),(.5,.7),(7.5,8.5),
                                (.1,.3,.6),(0.,.005),(-.1,.1)):
        k=stiffness(E,t=t,L=L)
        dmin=mech['end_deflection']+preload_error
        dmax=mech['peak_deflection']+preload_error
        min_completion=k*max(0.,dmin)*(.4-mu)/(1+.4*mu)-drag
        peak_drive=k*max(0.,dmax)*(.4+mu)/(1-.4*mu)+drag
        cases.append((min_completion,peak_drive))
    out=dict(geometry=geom,mechanical=mech,routes=routes(),
        interface_poses=[interface_checks(n) for n in (1,4,16)],rail=rail_bound(),
        central=[dict(mu=mu,**flank_force(front(1.7)-X0,mu=mu),peak_drive=flank_force(front(.85)-X0,mu=mu)['drive'])
                 for mu in (0.,.1,.2,.3,.4,.6)],
        bounded_scenarios=dict(count=len(cases),completion_range=[min(x[0] for x in cases),max(x[0] for x in cases)],
            peak_drive_range=[min(x[1] for x in cases),max(x[1] for x in cases)],
            coherent_B4_force_range=[1600*min(x[1] for x in cases),1600*max(x[1] for x in cases)]),
        stalled_reset=dict(q=.85,cam_slope=0.,spring_force=stiffness()*(front(.85)-X0),
                           required_action='inhibit ascent; actual pad readback; explicit drive across crest'),
        controls=dict(explicit_B4_s=lane.evaluate(4),broadcast_B4_s=reset.evaluate(4),
                      direct_B4_s=lane.control.evaluate('direct',4)['seconds']))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
