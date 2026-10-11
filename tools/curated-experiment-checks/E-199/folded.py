"""E-199. N, mm, MPa. Quasistatic planar Ritz beams + rigid floating bar.
Bounded scenarios, no measured process distributions. Run with Python/NumPy.
"""
import itertools
import json
import importlib.util
from pathlib import Path
import numpy as np
from numpy.polynomial import Polynomial as Poly

spec = importlib.util.spec_from_file_location('control', Path(__file__).parents[1]/'E-198/islands.py')
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)


def operators(L, modes):
    s, weights = np.polynomial.legendre.leggauss(24)
    s, weights = (s+1)/2, weights/2
    h, j = Poly([0,0,3,-2]), Poly([0,0,-1,1])
    bubbles = [Poly([0,0,1,-2,1])*Poly([-1,2])**k for k in range(modes)]
    basis = [h, L*j] + bubbles
    D = np.array([p.deriv()(s)/L for p in basis]).T
    DD = np.array([p.deriv(2)(s)/L**2 for p in basis]).T
    return basis, L*D.T@(weights[:,None]*D), L*DD.T@(weights[:,None]*DD)


def solve(q, widths=(.1,.1), lengths=(41.,42.), bias=0., modes=2, E=200000., t=.4, preload=.2):
    # x=[bar translation, bar rise, bar rotation, shape bubbles beam A/B].
    # Small-angle rigid crossbar: half-spacing .4; angle is free, not guided.
    n=3+2*modes
    parts=[]
    delta=q-preload
    for i,(w,L) in enumerate(zip(widths,lengths)):
        basis,G,K=operators(L,modes)
        T=np.zeros((2+modes,n));T[0,0]=1;T[1,2]=1
        if modes: T[2:,3+i*modes:3+(i+1)*modes]=np.eye(modes)
        off=np.zeros(2+modes);off[0]=0 if i==0 else -delta
        a=np.zeros(n);a[1]=-1;a[2]=-.4 if i==0 else .4
        parts.append((L,w,basis,G,K,T,off,a,0 if i==0 else bias))
    def evaluate(x, details=False):
        U=0.;g=np.zeros(n);H=np.zeros((n,n));data=[]
        for L,w,basis,G,K,T,off,a,b in parts:
            c=T@x+off; ext=a@x+b+.5*c@G@c
            de=a+T.T@G@c; EA=E*t*w;EI=E*t*w**3/12
            U+=.5*EI*c@K@c+EA/(2*L)*ext**2
            g+=EI*T.T@K@c+EA/L*ext*de
            H+=EI*T.T@K@T+EA/L*(np.outer(de,de)+ext*T.T@G@T)
            data.append((c,ext,EA/L*ext,EI))
        return (U,g,H,data) if details else (U,g,H)
    x=np.zeros(n);x[0]=delta/2;x[1]=.6*(delta/2)**2/41
    for it in range(100):
        U,g,H=evaluate(x)
        if np.max(np.abs(g))<1e-10: break
        eig=np.linalg.eigvalsh(H)
        step=np.linalg.solve(H+np.eye(n)*max(0.,1e-8-eig[0]),-g)
        alpha=1.
        while evaluate(x+alpha*step)[0]>U+1e-4*alpha*(g@step):
            alpha*=.5
            if alpha<1e-10: raise AssertionError(('line search',q,g))
        x+=alpha*step
    U,g,H,data=evaluate(x,True)
    assert np.max(np.abs(g))<1e-8,(q,g)
    assert np.linalg.eigvalsh(H)[0]>0,('unstable',q)
    L,w,basis,G,K,T,off,a,b=parts[1]
    c,ext,N,EI=data[1]
    # Variation of output top x gives -h; root rotation gives L(s-2s²+s³).
    # Force on island is minus derivative of minimized energy.
    Hx=(EI*K@c+N*G@c)[0]
    s,weights=np.polynomial.legendre.leggauss(24);s=(s+1)/2;weights=weights/2
    root=Poly([0,1,-2,1])*L
    poly=sum((ci*p for ci,p in zip(c,basis)),Poly([0]))
    dUphi=EI/L**3*np.sum(weights*poly.deriv(2)(s)*root.deriv(2)(s))+N/L*np.sum(weights*poly.deriv()(s)*root.deriv()(s))
    M=-dUphi
    Fz=-N
    # Wrench about lower guide plane z=-2, x=0. Output attachment x=-1.45+q.
    W=np.array([Hx,Fz,M+(-1.45+q)*Fz-bias*Hx])
    shapes=[]
    strains=[]
    for i,((L,w,basis,G,K,T,off,a,b),(c,ext,N,EI)) in enumerate(zip(parts,data)):
        p=sum((ci*v for ci,v in zip(c,basis)),Poly([0]))
        u=np.linspace(0,1,129)
        # Uniform axial strain minus geometric shortening, integrated exactly.
        dp=p.deriv()/L
        axial=(Poly([ext/L])-.5*dp*dp).integ()*L
        ztop=-44+L+(bias if i else 0)
        xpos=(-.45 if i==0 else -1.45+q)+p(u)
        zpos=ztop-L*u-axial(u)
        shapes.append(np.column_stack((xpos,zpos)))
        strains.append(float(max(abs(ext/L-w/2*p.deriv(2)(u)/L**2).max(),abs(ext/L+w/2*p.deriv(2)(u)/L**2).max())))
    return dict(q=q,H=float(Hx),Fz=float(Fz),M=float(M),W=W,bar=x[:3],energy=U,
                residual=float(np.max(abs(g))),strain=max(strains),shapes=shapes,x=x,evaluate=evaluate)


# Unilateral contact endpoints: (x, z relative to -2, normal sign).
CONTACTS=[(-.25,0,1),(.15,0,1),(-1.7,2,-1),(-1.4,2,-1),(-.25,2,-1),(.15,2,-1)]

def reactions(W, lam, stiffness=None):
    # Vanishing-compliance regularization removes arbitrary zero-play self-stress.
    # Six unilateral endpoint springs, same default normal stiffness. Friction
    # opposes +x with a common traction/normal ratio lam on every active face.
    k=1e6*(np.ones(6) if stiffness is None else np.array(stiffness,float))
    contact=np.array(CONTACTS);xx,zz,nn=contact.T
    gap_rows=np.column_stack((nn,nn*xx))
    wrench_rows=np.array([nn,xx*nn+zz*lam])
    for active_tuple in itertools.product([False,True],repeat=6):
        active=np.array(active_tuple)
        C=-k[:,None]*gap_rows*active[:,None]
        mat=wrench_rows@C
        if abs(np.linalg.det(mat))<1e-8: continue
        displacement=np.linalg.solve(mat,-W[1:])
        gaps=gap_rows@displacement
        if np.any(gaps[active]>1e-10) or np.any(gaps[~active]<-1e-10): continue
        N=np.maximum(-k*gaps,0)
        residual=wrench_rows@N+W[1:]
        assert max(abs(residual))<1e-8
        return N, displacement
    return None


def threshold(W, stiffness=None):
    # Smallest uniform resisting traction ratio on this compliant branch.
    if W[0]<=0: return None
    lo=0.;hi=None
    for trial in np.geomspace(1e-6,1.,80):
        r=reactions(W,trial,stiffness)
        if r is None: break
        if trial*sum(r[0])>=W[0]:
            hi=trial;break
        lo=trial
    if hi is None:return None
    for _ in range(35):
        mid=(lo+hi)/2;r=reactions(W,mid,stiffness)
        if r is None: return None
        if mid*sum(r[0])<W[0]: lo=mid
        else: hi=mid
    r=reactions(W,hi,stiffness)
    if abs(hi*sum(r[0])-W[0])>1e-8:return None
    return hi


def static_witness(W,mu):
    critical=threshold(W)
    if critical is None or critical>mu:return None
    N,disp=reactions(W,critical)
    f=-critical*N
    xx,zz,nn=np.array(CONTACTS).T
    residual=np.array([sum(f),sum(nn*N),sum(xx*nn*N-zz*f)])+W
    assert max(abs(residual))<1e-8
    return dict(traction_ratio=critical,normals=N.tolist(),friction=f.tolist(),
                normal_sum=float(sum(N)),regularized_displacement=disp.tolist(),
                residual=float(max(abs(residual))))


def geometry(n):
    # Borrow rack/island and backed guide from E-198, replacing bottom spine.
    f=control.frame()
    for name in ['spine','spine_foot']: del f[name]
    f['root_bridge']=control.box(-.65,.15,-1.4,1.4,-3,-2.5)
    f['spine']=control.box(-2.54,2.54,-.2,.2,-46,-45)
    f['fixed_rib']=control.box(.05,.15,-.2,.2,-45,-3)
    # A separate grounded bridge captures/bonds the anchor end at z=-3.
    poses=0;mingap=100.
    for q in np.linspace(-.75,0,n+1):
        r=solve(float(q));pad=control.island(q)
        beam_boxes=[]
        for shape in r['shapes']:
            for a,b in zip(shape[:-1],shape[1:]):
                beam_boxes.append(control.box(min(a[0],b[0])-.05,max(a[0],b[0])+.05,-.2,.2,min(a[1],b[1]),max(a[1],b[1])))
        ends=np.array([s[-1] for s in r['shapes']])
        turn=control.box(ends[:,0].min()-.05,ends[:,0].max()+.05,-.2,.2,ends[:,1].min()-.3,ends[:,1].max())
        # Conservative turnaround envelope includes the beam bonds.
        movers=[pad,*beam_boxes,turn]
        for name,ground in f.items():
            for solid in movers: assert not control.penetration(solid,ground),(q,name,solid)
        # Cross-leg segment AABBs; same-leg continuity and intended bar bonds excluded.
        assert max(b[0,1] for b in beam_boxes[128:]) < min(b[0,0] for b in beam_boxes[:128]), (q,'legs')
        for dx in [-5.08,0,5.08]:
            for dy in [-5.08,0,5.08]:
                if dx==0 and dy==0: continue
                neighbor=control.box(.4+dx,2.2+dx,-.8+dy,.8+dy,-42,42.2)
                for solid in movers: assert not control.penetration(solid,neighbor),(q,'neighbor')
        for h in [0,10,20,30,40]:
            for solid in control.rack(h+.2):
                for mover in movers: assert not control.penetration(solid,mover),(q,h)
            poses+=1
        mingap=min(mingap,float(turn[2,0]+45))
    for old,new in itertools.permutations([0,10,20,30,40],2):
        for h in np.linspace(old+.2,new+.2,n+1):
            for solid in control.rack(h):
                for ground in f.values(): assert not control.penetration(solid,ground)
                assert not control.penetration(solid,control.island(-.75))
            poses+=1
    return {'poses':poses,'turnaround_spine_clearance':mingap}


def clean(r):
    return {k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in r.items() if k not in ['shapes','x','evaluate']}


def main():
    out={}
    out['geometry']={n:geometry(n) for n in [4,16,64]}
    nominal=[]
    for q in [0,-.3,-.75]:
        r=solve(q,modes=4);d=clean(r);d['critical_mu']=threshold(r['W']);d['sticking_mu_005']=static_witness(r['W'],.05);nominal.append(d)
        # Independent work derivative and analytic Hessian finite difference.
        eps=1e-5
        fd=-(solve(q+eps,modes=4)['energy']-solve(q-eps,modes=4)['energy'])/(2*eps)
        assert abs(fd-r['H'])<1e-8
        U,g,H=r['evaluate'](r['x']);step=np.linspace(-1,1,len(g))*1e-6
        dg=(r['evaluate'](r['x']+step)[1]-r['evaluate'](r['x']-step)[1])/2
        assert np.max(abs(dg-H@step))<1e-8
    out['nominal']=nominal
    out['contact_stiffness_ratios']={str(k):threshold(solve(-.75)['W'],[k,1,1,1,1,1/k]) for k in [.1,1.,10.]}
    out['common_modulus_scale']={str(E):threshold(solve(-.75,E=E)['W']) for E in [160000.,220000.]}
    sym=solve(-.75,lengths=(41.,41.),modes=4)
    expected=.5*200000*.4*.1**3*.95/41**3
    assert abs(sym['H']/expected-1)<1e-10
    assert abs(sym['M']/sym['H']-41/2)<1e-9
    assert abs(threshold(sym['W'])-.4/(41+2))<1e-8
    out['shape_convergence']={m:[clean(solve(q,modes=m)) for q in [0,-.75]] for m in [0,2,4,6]}
    # Equal legs: bar shortening is free, but end moments still need guide reactions.
    out['symmetric_control']=clean(solve(-.75,lengths=(41.,41.),modes=4))
    cases=[]
    for common,opposed,bias in itertools.product([-.01,.01],[-.01,.01],[-.025,0,.025]):
        widths=(.1+common+opposed,.1+common-opposed)
        for q in [0,-.75]:
            r=solve(q,widths=widths,bias=bias,modes=4)
            cases.append(dict(widths=widths,bias=bias,q=q,H=r['H'],Fz=r['Fz'],M=r['M'],bar_angle=float(r['bar'][2]),strain=r['strain'],critical_mu=threshold(r['W'])))
    out['bounded_scenarios']=cases
    out['bounded_summary']={k:[min(x[k] for x in cases),max(x[k] for x in cases)] for k in ['H','Fz','M','bar_angle','strain']}
    mus=[x['critical_mu'] for x in cases if x['critical_mu'] is not None]
    out['bounded_summary'].update(return_reversals=sum(x['H']<=0 for x in cases),critical_mu_range=[min(mus),max(mus)],positive_force_cases=len(mus))
    # A pure force through the guide center does not inherit a leaf end couple.
    assert static_witness(np.array([1.,0.,0.]),.05) is None
    out['carrier_control']={'horizontal_force_without_couple_sticks_mu_005':False}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
