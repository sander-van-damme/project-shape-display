"""E-200: finite free-tip return and no-preload guide sticking. N, mm, MPa.
Explicit bounded scenarios, not process priors. Python + NumPy; JSON disposable.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


control = module('islands', Path(__file__).parents[1]/'E-198/islands.py')
folded = module('folded', Path(__file__).parents[1]/'E-199/folded.py')
CONTACTS = np.array(folded.CONTACTS)
X, Z, NORMAL = CONTACTS.T
GAPS = np.column_stack((NORMAL, NORMAL*X))
BALANCE = np.array([NORMAL, X*NORMAL])


def shape(q, n=512, w=.2, r=.15, preload=.2, L=41.):
    # Small-slope, free-moment Euler-Bernoulli cantilever. Positive d bends left.
    d = preload-q
    u = np.linspace(0, 1, n+1)
    f = 1.5*u*u-.5*u**3
    # Integral of (f')^2: 3u^3 - 2.25u^4 + .45u^5.
    shortening = d*d/(2*L)*(3*u**3-2.25*u**4+.45*u**5)
    xroot = -1.75-r+preload
    x = xroot-d*f
    z = -1.7-L+L*u-shortening
    H = 200000.*.4*w**3*d/(4*L**3)
    return np.column_stack((x,z)), H


def geometry(n):
    # A round integral button supplies setback so the inclined stem misses the
    # island. A square bounding box around it is conservative for collision.
    poses = 0
    gap = 1e9
    f = control.frame()
    # Clamp the root through a fixed short rib to the E-198 bottom spine.
    f['root_rib'] = control.box(-1.8,-1.6,-.2,.2,-43,-42.7)
    f['seated_stop'] = control.box(-.9,-.5,-1.4,1.4,-2.6,-2.1)
    def no_collision(solids, other):
        a=np.asarray(solids)
        delta=np.minimum(a[:,:,1],other[:,1])-np.maximum(a[:,:,0],other[:,0])
        return not np.any(np.all(delta>1e-10,axis=1))
    for q in np.linspace(-.75,0,n+1):
        curve,H = shape(q)
        pad = control.island(q)
        boss = control.box(curve[-1,0]-.15,curve[-1,0]+.15,-.2,.2,
                           curve[-1,1]-.15,curve[-1,1]+.15)
        u=np.linspace(0,1,len(curve))
        slope=-(.2-q)/41*(3*u-1.5*u*u)
        offsets=np.column_stack((.1/np.sqrt(1+slope*slope),
                                 -.1*slope/np.sqrt(1+slope*slope)))
        left,right=curve-offsets,curve+offsets
        stems=[]
        for i in range(len(curve)-1):
            vertices=np.array([left[i],right[i],left[i+1],right[i+1]])
            stems.append(control.box(vertices[:,0].min(),vertices[:,0].max(),
                                     -.2,.2,vertices[:,1].min(),vertices[:,1].max()))
        lug=control.box(-1.2+q,-.9+q,-.2,.2,-2.6,-2)
        movers=[pad,lug,boss,*stems]
        assert not control.penetration(boss,pad)
        assert no_collision(stems,pad),('stem/island',q)
        assert no_collision(stems,lug),('stem/lug',q)
        for name,ground in f.items():
            assert no_collision(movers,ground),(name,q)
        for dx,dy in itertools.product([-5.08,0,5.08],repeat=2):
            if dx==dy==0: continue
            neighbor=control.box(.4+dx,2.2+dx,-.8+dy,.8+dy,-42,42.2)
            assert no_collision(movers,neighbor),('neighbor',q)
        gap=min(gap,boss[0,0]-(-2.88))
        for h in [0,10,20,30,40]:
            for rack in control.rack(h+.2):
                assert no_collision(movers,rack)
            poses+=1
    for old,new in itertools.permutations([0,10,20,30,40],2):
        for h in np.linspace(old+.2,new+.2,n+1):
            for rack in control.rack(h):
                for ground in f.values(): assert not control.penetration(rack,ground)
                assert not control.penetration(rack,control.island(-.75))
            poses+=1
    return {'poses':poses,'boss_neighbor_gap':gap,'root_connected':True}


def branches(q, c, gravity_ratio=0., stiffness=None):
    # Unknowns y=[tip vertical/H, upper-guide horizontal/H]. Lower horizontal
    # force is -1-y[1]. Solve each normal spring active set as an affine map.
    # k=1 scaling; displacements divide by physical k for interpretation.
    k=np.ones(6) if stiffness is None else np.array(stiffness)
    x=-1.75+q
    xcm=(5.3*(-.425)+.18*(-1.05))/5.48+q
    W=np.array([[-gravity_ratio,1,0],[-c-xcm*gravity_ratio,x,-2]])
    for active_tuple in itertools.product([False,True],repeat=6):
        active=np.array(active_tuple)
        C=-k[:,None]*GAPS*active[:,None]
        mat=BALANCE@C
        if abs(np.linalg.det(mat))<1e-10: continue
        disp=np.linalg.solve(mat,-W)
        N=C@disp
        gap=GAPS@disp
        # Each row represents affine expression >=0, columns [constant,v,phi].
        constraints=[-gap[i] if active[i] else gap[i] for i in range(6)]
        yield N,disp,constraints


def polygon_feasible(rows):
    a=np.array(rows)
    # Enumerate finite vertices, including degenerate line-segment endpoints.
    # v is bounded and activity/friction inequalities bound phi on at least one
    # side here. Wedged branches may extend to infinite force on the other side;
    # no artificial force cap is imposed or interpreted as physical strength.
    pairs=np.array(list(itertools.combinations(range(len(a)),2)))
    p,r=a[pairs[:,0]],a[pairs[:,1]]
    det=p[:,1]*r[:,2]-p[:,2]*r[:,1]
    valid=abs(det)>1e-12
    p,r,det=p[valid],r[valid],det[valid]
    ys=np.column_stack(((-p[:,0]*r[:,2]+p[:,2]*r[:,0])/det,
                        (-p[:,1]*r[:,0]+p[:,0]*r[:,1])/det))
    valid=np.all(a[:,0,None]+a[:,1:]@ys.T>=-1e-9,axis=0)
    if np.any(valid): return ys[np.flatnonzero(valid)[0]]
    return None


def sticking(q,c,mu,tip_mu,gravity_ratio=0.,stiffness=None):
    for N,D,rows in branches(q,c,gravity_ratio,stiffness):
        low=N[Z==0].sum(axis=0); high=N[Z==2].sum(axis=0)
        phi=np.array([0.,0.,1.]); lower=np.array([-1.,0.,-1.])
        rows=rows+[mu*high-phi,mu*high+phi,mu*low-lower,mu*low+lower,
                   np.array([tip_mu,1.,0.]),np.array([tip_mu,-1.,0.])]
        y=polygon_feasible(rows)
        if y is None: continue
        coeff=np.r_[1.,y]; normals=N@coeff
        v,p=y
        x=-1.75+q; xcm=(5.3*(-.425)+.18*(-1.05))/5.48+q
        residual=np.array([1+(-1-p)+p,
                           normals@NORMAL+v-gravity_ratio,
                           normals@(X*NORMAL)-2*p+x*v-c-xcm*gravity_ratio])
        assert max(abs(residual))<1e-7
        assert min(normals)>-1e-8
        return {'tip_vertical_ratio':float(v),'upper_friction_ratio':float(p),
                'normals_per_H':normals.tolist(),'residual':float(max(abs(residual)))}
    return None


def threshold(q,c,tip_mu,gravity_ratio=0.,stiffness=None):
    if sticking(q,c,1.,tip_mu,gravity_ratio,stiffness) is None: return None
    lo,hi=0.,1.
    for _ in range(25):
        mid=(lo+hi)/2
        if sticking(q,c,mid,tip_mu,gravity_ratio,stiffness) is None:lo=mid
        else:hi=mid
    return hi


def clipped_area(poly, bounds):
    # Sutherland-Hodgman clipping of actual x/z polygon against a rectangle.
    for axis,sign,edge in bounds:
        result=[]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            da,db=sign*(a[axis]-edge),sign*(b[axis]-edge)
            if da>=0: result.append(a)
            if (da>=0)!=(db>=0): result.append(a+(b-a)*da/(da-db))
        poly=result
        if not poly:return 0.
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2


def main():
    out={'geometry':{n:geometry(n) for n in [4,16,64]}}
    nominal=[]
    for q in [0,-.3,-.75]:
        curve,H=shape(q);c=curve[-1,1]+2
        # Explicit steel-like density scenario 0.008 g/mm^3, not sourced prior.
        weight=(2.65*2+.3*.6)*.4*.008*9.81/1000
        nominal.append({'q':q,'H':H,'contact_height_above_lower':c,
                        'weight':weight,'g_over_H':weight/H,
                        'threshold_no_weight':threshold(q,c,.3),
                        'threshold_with_weight':threshold(q,c,.3,weight/H)})
    out['nominal']=nominal
    # Independent finite difference of cantilever energy and shortening integral.
    L=41.;d=.95;EI=200000.*.4*.2**3/12
    eps=1e-5
    fd=(1.5*EI*(d+eps)**2/L**3-1.5*EI*(d-eps)**2/L**3)/(2*eps)
    assert abs(fd-shape(-.75)[1])<1e-10
    out['shortening_quadrature']={}
    for n in [32,128,512]:
        u=np.linspace(0,1,n+1);s=d/L*(3*u-1.5*u*u)
        drop=.5*L*np.trapz(s*s,u)
        out['shortening_quadrature'][n]=float(drop)
        assert abs(drop-.6*d*d/L)<1e-7
    # Recover E-199's analytic equal-leg witness with the opposite external M.
    analytic=.4/43
    actual=threshold(0.,-20.5,0.)
    assert abs(actual-analytic)<1e-7,(actual,analytic)
    out['folded_control_threshold']=actual
    # No gravity/couple does not eliminate friction-induced drawer wedging.
    # Lower x=-.25, upper x=.15 at z=2: equal normals N=2.5H and
    # each friction=-.5H balance at mu=.2, independently of a spring preload.
    assert sticking(0.,0.,.05,0.) is None
    assert abs(threshold(0.,0.,0.)-.2)<1e-7
    out['pure_horizontal_control']=sticking(0.,0.,.2,0.)
    out['bounded_cases']=[]
    for q,c,tip_mu,g in itertools.product([0.,-.75],[.15,.45],[.0,.3,.5],[0.,.5,2.,10.]):
        out['bounded_cases'].append({'q':q,'c':c,'tip_mu':tip_mu,'g_over_H':g,
                                    'mu005_stick':sticking(q,c,.05,tip_mu,g) is not None,
                                    'mu03_stick':sticking(q,c,.3,tip_mu,g) is not None})
    out['stiffness_sensitivity']={str(k):threshold(0.,.3,.3,.36,[k,1,1,1,1,1/k]) for k in [.1,1,10]}
    # Finite bad-control stem: remove the button setback but keep a physical stem.
    curve,_=shape(-.75,r=.1)
    u=np.array([511/512,1.]); slope=-.95/41*(3*u-1.5*u*u)
    offsets=np.column_stack((.1/np.sqrt(1+slope*slope),-.1*slope/np.sqrt(1+slope*slope)))
    a,b=curve[-2:];oa,ob=offsets
    poly=[a-oa,a+oa,b+ob,b-ob]
    overlap=.4*clipped_area(poly,[(0,1,-2.5),(0,-1,.15),(1,1,-2),(1,-1,0)])
    assert overlap>0
    out['no_setback_stem_collision_mm3']=overlap
    # Independent opposed-error neighbor boundary: rear datum and neighbor each
    # +/-e, button radius +/-e. Four e erode the .08 nominal gap.
    out['neighbor_error_gaps']={str(e):.08-4*e for e in [0,.01,.025,.05]}
    # Actual circle against the adjacent rack web, not only a box overlap:
    # leftmost circle point lies .02 mm inside the web at e=.025.
    e=.025
    center=-2.5-e-(.15+e)
    rack_right=-2.88+e
    intrusion=rack_right-(center-(.15+e))
    assert abs(intrusion-.02)<1e-12
    out['adverse_button_intrusion_mm']=intrusion
    out['example_gravity_sticking']=sticking(0.,.3,.3,.3,2.)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
