"""E-198: finite backed sheet islands and constrained beam return; N, mm, MPa.
Deterministic bounded scenarios, no process priors. stdout is disposable.
"""
import itertools
import json
import math
import numpy as np

PITCH = 5.08


def beam(d, L=41., w=.1, t=.4, E=200000.):
    """Two fixed-guided extensible beams; von Karman compatibility.
    Solve exact transverse tension-beam shape, not assumed cubic deflection.
    a=kL/2; integral of dimensionless slope shape squared is B.
    """
    if d == 0:
        return dict(H=0., N=0., strain=0., C=0., a=0., L=L, d=d)
    def terms(a):
        if a < .01:
            # Stable series: D/L=1-tanh(a)/a; B=int(shape^2)/L.
            D = a*a/3 - 2*a**4/15 + 17*a**6/315
            B = 2*a**4/15 - 34*a**6/315 + 62*a**8/945
        else:
            D = 1 - math.tanh(a)/a
            B = 1 + .5/math.cosh(a)**2 - 1.5*math.tanh(a)/a
        return D, B
    A, I = t*w, t*w**3/12
    def balance(a):
        D,B=terms(a)
        C=d/(L*D)
        return 4*a*a/L**2 - A*C*C*B/(2*I)
    lo,hi=1.e-5,1.
    while balance(hi)<0: hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if balance(mid)>0: hi=mid
        else: lo=mid
    a=(lo+hi)/2
    D,B=terms(a)
    C=d/(L*D)
    N=E*I*(2*a/L)**2
    H=N*C
    strain=N/(E*A)+w/2*C*2*a/L*math.tanh(a)
    return dict(H=2*H,N=2*N,strain=strain,C=C,a=a,L=L,d=d)


def shape(b,n=128):
    u=np.linspace(0,1,n+1)
    a,L,d=b['a'],b['L'],b['d']
    if d==0: return u, np.zeros_like(u),np.zeros_like(u)
    # End displacement d; slope is dw/dz.
    C=b['C']
    v=C*(1-np.cosh(2*a*(u-.5))/math.cosh(a))
    y=C*L*(u-(np.sinh(2*a*(u-.5))+math.sinh(a))/(2*a*math.cosh(a)))
    return u,y,v


def box(x0,x1,y0,y1,z0,z1):
    return np.array([[x0,x1],[y0,y1],[z0,z1]],float)


def penetration(a,b):
    delta=np.minimum(a[:,1],b[:,1])-np.maximum(a[:,0],b[:,0])
    return float(np.prod(delta)) if np.all(delta>1e-10) else 0.


def frame():
    # Ground bridges are connected to side posts outside the sheet and rack.
    return {
        'lower':box(-.25,.15,-1.4,1.4,-2.5,-2),
        'upper_rear':box(-1.7,-1.4,-1.4,1.4,0,.4),
        'upper_front':box(-.25,.15,-1.4,1.4,0,.4),
        'base':box(-2.54,2.54,-1.4,1.4,-47,-46),
        'post0':box(-1.7,.15,-1.4,-1.,-46,0),
        'post1':box(-1.7,.15,1.,1.4,-46,0),
        'spine':box(-2.54,2.54,-.2,.2,-45,-43),
        'spine_foot':box(-2.54,2.54,-.2,.2,-46,-45),
    }


def rack(h):
    return [box(1.2,2.2,-.8,.8,h-42,h+2)]+[
        box(.4,1.2,-.8,.8,h-40+10*j,h-39+10*j) for j in range(5)]


def island(q):
    return box(-1.75+q,.9+q,-.2,.2,-2,0)


def leaves(q,n=64):
    # Roots lie .2 mm to the right of the unshifted attachment positions.
    # Constant axial tension keeps both end heights fixed. Axial interior
    # displacement omitted here but bounded by N L/(EA); pad z is exact.
    b=beam(.2-q)
    u,y,v=shape(b,n)
    out=[]
    for x in [-1.45,-.65]:
        xs=x+.2-y
        for j in range(n):
            out.append(box(min(xs[j:j+2])-.05,max(xs[j:j+2])+.05,
                           -.2,.2,-43+41*u[j],-43+41*u[j+1]))
    return out


def geometry(n):
    f=frame(); poses=0
    # Each key is attached to two separate leaves and the common lower spine.
    # Intended touching roots/pad/ground faces do not count as penetration.
    for q in np.linspace(-.75,0,n+1):
        pad=island(q)
        for name,solid in f.items(): assert not penetration(pad,solid),(q,name)
        for leaf in leaves(q):
            for name,solid in f.items(): assert not penetration(leaf,solid),(q,name)
        # Unloaded rack raised .2; all parked heights.
        for h in [0,10,20,30,40]:
            for solid in rack(h+.2):
                assert not penetration(pad,solid)
                for leaf in leaves(q,8): assert not penetration(leaf,solid)
            poses+=1
    # All unequal moves with fully withdrawn island; support is granted to head.
    for old,new in itertools.permutations([0,10,20,30,40],2):
        for h in np.linspace(old+.2,new+.2,n+1):
            for solid in rack(h):
                for name,ground in f.items(): assert not penetration(solid,ground),(h,name)
                assert not penetration(island(-.75),solid)
            poses+=1
    # Adjacent rack swept envelopes cover every neighbor height, not only endpoints.
    for q in np.linspace(-.75,0,n+1):
        for dx in [-PITCH,PITCH]:
            neighbor=box(.4+dx,2.2+dx,-.8,.8,-42,42.2)
            assert not penetration(island(q),neighbor)
            for leaf in leaves(q,8): assert not penetration(leaf,neighbor)
    # Eight independent selected/unselected local patterns.
    for qs in itertools.product([0,-.75],repeat=3):
        pads=[island(q)+np.array([[i*PITCH,i*PITCH],[0,0],[0,0]]) for i,q in enumerate(qs)]
        for a,b in itertools.combinations(pads,2): assert not penetration(a,b)
    return poses


def checks():
    assert penetration(box(0,1,0,1,0,1),box(.5,1.5,0,1,0,1))==.5
    assert penetration(box(0,1,0,1,0,1),box(1,2,0,1,0,1))==0
    b=beam(.0001)
    k=2*200000*.4*.1**3/41**3
    assert abs(b['H']/(k*.0001)-1)<1.e-4
    # Independent numerical integration of compatibility, shear/work, and length.
    conv=[]
    for n in [64,256,1024]:
        b=beam(.95);u,y,v=shape(b,n);a=b['a'];L=b['L']
        mean=float(np.trapz(v*v,u))
        Ncheck=200000*.4*.1*mean  # two beams, each EA*mean/2
        exact=float(np.trapz(np.sqrt(1+v*v)-1,u))
        conv.append([n,abs(Ncheck/b['N']-1),abs(exact/(mean/2)-1)])
    assert conv[-1][1]<1.e-8
    assert conv[-1][2]<.001
    assert abs(y[-1]-.95)<1.e-10
    # Independent finite-difference derivative of integrated strain energy.
    def energy(d):
        b=beam(d); u=np.linspace(0,1,4097)
        a,L,C=b['a'],b['L'],b['C']
        curvature=-C*2*a/L*np.sinh(2*a*(u-.5))/math.cosh(a)
        I=.4*.1**3/12; A=.4*.1; E=200000.
        return E*I*L*float(np.trapz(curvature**2,u))+(b['N']/2)**2*L/(E*A)
    for d in [.2,.5,.95]:
        derivative=(energy(d+1e-5)-energy(d-1e-5))/(2e-5)
        assert abs(derivative/beam(d)['H']-1)<1e-4
    # Service-only independent balance control; full leaf end couples and
    # distributed guide pressure are not computed by this check.
    for F in [.1,1,10]:
        upper=.6*F/1.55
        lower=F+upper
        assert abs(lower-upper-F)<1.e-12
        assert abs(1.55*upper-.6*F)<1.e-12
    return conv


def main():
    out={'checks':checks(),'geometry_poses':{n:geometry(n) for n in [4,16,64]}}
    out['nominal']={str(d):beam(d) for d in [.2,.5,.95]}
    # Return near engagement with lower rail: even grant an external moment
    # reaction with no extra friction. N alone is a favorable normal-force bound.
    # If upper contact is needed, total guide reaction can only be larger.
    out['return_upper_bound_N']={str(mu):{
        str(d):beam(d)['H']-mu*beam(d)['N'] for d in [.2,.5,.95]}
        for mu in [0,.005,.01,.02,.05,.1,.3,.6]}
    corners=[]
    for E,w,t,L,pre,stroke in itertools.product(
        [160000.,220000.],[.08,.12],[.35,.45],[40.,42.],[.15,.25],[.7,.8]):
        vals=[beam(d,L,w,t,E) for d in np.linspace(pre,pre+stroke,65)]
        corners.append(dict(min_ratio=min(v['C'] for v in vals),
                            max_ratio=max(v['C'] for v in vals),
                            peak_H=max(v['H'] for v in vals),
                            peak_N=max(v['N'] for v in vals),
                            strain=max(v['strain'] for v in vals)))
    out['bounded_64_corners']={k:[min(c[k] for c in corners),max(c[k] for c in corners)] for k in corners[0]}
    out['corner_count']=len(corners)
    # Alternative material-like family; not a fabrication/material assignment.
    out['free_shortening_control']={'relative_drop_mm':.6*(.95**2-.2**2)/41,
        'force_at_full_release_N':2*200000*.4*.1**3*.95/41**3,
        'shelf_penetration_mm3':.4*.4*.6*(.95**2-.2**2)/41}
    out['polymer_like']={str(d):beam(d,w=.4,t=.8,E=2000.) for d in [.2,.95]}
    # Common rigid geometry error: each facing surface may shift ±e. Translation
    # of the entire assembly cancels; slot-vs-pad relative bias remains.
    out['slot_boxes']={str(e):{'min_gap':-.0-4*e,'max_gap':4*e} for e in [.025,.05,.1]}
    out['board']={'sheet_placements':160,'leaves':12800,'guide_faces':19200,
                  'allocated_sheet_m2':160*.2032*.045,
                  'seconds_at_160_heads_service_05':6+math.ceil(6400/160)*.5,
                  'resident_allowance_with_250_elsewhere':250/6400}
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
