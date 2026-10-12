"""E-210 released toe: mm/N/MPa, frictionless finite-prism contact.
Python, NumPy, SciPy. Explicit bounded scenarios, not process distributions.
OPENBLAS_NUM_THREADS=1 python tools/curated-experiment-checks/E-210/contact.py
"""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, nnls

spec = importlib.util.spec_from_file_location('return_path', Path(__file__).resolve().parents[1]/'E-209/return_path.py')
e = importlib.util.module_from_spec(spec); spec.loader.exec_module(e)
r = e.r


def moved(poly, q):
    return r.move(poly, q[2])+q[:2]


def separation(a, b):
    """Exact convex SAT signed separation; positive iff disjoint in this plane."""
    edges = np.vstack((np.roll(a, -1, axis=0)-a, np.roll(b, -1, axis=0)-b))
    axes = np.c_[-edges[:, 1], edges[:, 0]].astype(float)
    axes /= np.linalg.norm(axes, axis=1)[:, None]
    pa, pb = a@axes.T, b@axes.T
    return float(np.max(np.maximum(pa.min(axis=0)-pb.max(axis=0), pb.min(axis=0)-pa.max(axis=0))))


def contact_points(a, b, tol=2e-6):
    """Contact on a: vertex/face witnesses, with b's outward normal.
    Includes both ends of coincident faces so no arbitrary pressure centroid.
    """
    out = []
    for vertex_poly, edge_poly, sign in ((a, b, 1), (b, a, -1)):
        area = np.sum(edge_poly[:, 0]*np.roll(edge_poly[:, 1], -1)-edge_poly[:, 1]*np.roll(edge_poly[:, 0], -1))
        for u, v in zip(edge_poly, np.roll(edge_poly, -1, axis=0)):
            d = v-u; norm = np.linalg.norm(d)
            normal = np.sign(area)*np.array([d[1], -d[0]])/norm
            for p in vertex_poly:
                s = (p-u)@d/(norm*norm)
                if -tol <= s <= 1+tol and abs((p-u)@normal) < tol:
                    out.append((p, sign*normal))
    return out


class Model:
    def __init__(self, offset=(0., .1), gap=.1, shift=0., depth=.2,
                 L=12., amp=.3, t=.4, E=700., W=.1, n=32):
        self.offset = np.array(offset); self.t=t; self.W=W; self.n=n
        self.L=L; self.amp=amp; self.EI=E*.8*t**3/12
        self.depth=depth; self.gap=gap; self.shift=shift
        _, pos = r.rod_reference(n, L, amp)
        self.frame=r.fixed(gap, shift, depth, float(pos[-1,1]))
        for i in (10,11):
            p,x=self.frame[i]; self.frame[i]=(p+self.offset,x)
        # Pocket void does not meet any frame/rack contact in this domain.
        # Use actual pocket pieces for subsequent independent finite checks.
        self.toe=[(r.R(-1,1.6,0,2),(-1.5,1.5)),
                  (r.R(.8,1.2,2,3.4),(-.4,.4)),
                  r.bodies(0,t=t)[6], (r.R(.85,1.15,-depth,0),(-1.5,-.85))]
        # The two keys are symmetric; combine their reactions in the plane.
        pairs=[]; seen=set()
        for i,(a,x) in enumerate(self.toe):
            for j,(b,y) in enumerate(self.frame):
                if min(x[1],y[1])-max(x[0],y[0]) <= 1e-9: continue
                if separation(a,b)>1.0: continue
                key=(i,tuple(b.ravel()))
                if key not in seen: pairs.append((i,j)); seen.add(key)
        self.pairs=pairs; self.cache={}

    def state(self,q):
        key=tuple(q[:3])
        if key not in self.cache:
            a=e.solve(q[2], -q[0], n=self.n,L=self.L,amp=self.amp,t=self.t,
                      offset=self.offset-[0.,q[1]])
            a['pos']=a['pos']+[0.,q[1]]
            a['root']=a['root']+[0.,q[1]]
            self.cache[key]=a
        return self.cache[key]

    def objective(self,q):
        return self.EI*self.state(q)['energy']+self.W*q[3]

    def gradient(self,q):
        a=self.state(q); f=self.EI*a['force']
        arm=r.move(r.A[None,:],q[2])[0]-r.P
        return np.r_[f, self.EI*a['moment']+arm[0]*f[1]-arm[1]*f[0],self.W]

    def gaps(self,q):
        toe=[moved(a,q) for a,x in self.toe]
        g=[separation(toe[i],self.frame[j][0]) for i,j in self.pairs]
        # Rack shelf horizontal; both transformed top vertices must lie below.
        # Checked y coverage and full rack geometry after solving.
        top=moved(np.array([[.8,3.4],[1.2,3.4]]),q)
        g.extend(3.4+q[3]-top[:,1])
        for i in (0,1,2):
            g.append(separation(toe[i],r.p.rack(q[3])[-1][0]))
        return np.array(g)

    def solve(self,initial=None,writer_k=0.):
        # Bounds delimit this local retained-contact branch, not hidden stops.
        bounds=[(-.3,.3),(-.05,.4),(-.12,.12),(-.3,.8)]
        starts=[np.zeros(4)] if initial is None else [np.array(initial)]
        candidates=[]
        for seed in starts:
            objective=lambda v: self.objective(v)+writer_k*np.dot(v[:3],v[:3])/2
            gradient=lambda v: self.gradient(v)+writer_k*np.r_[v[:3],0.]
            sol=minimize(objective,seed,jac=gradient,method='SLSQP',bounds=bounds,
                         constraints=[{'type':'ineq','fun':self.gaps}],
                         options={'ftol':1e-12,'maxiter':180})
            if not sol.success:
                # SAT is nonsmooth at perfectly aligned, coincident faces.
                # Resolve only near-zero stagnation with an exact seated
                # contact-wrench certificate and feasible energy perturbations.
                if np.max(abs(sol.x))<1e-7 and writer_k==0.:
                    exact=self.report(np.zeros(4),sol.nit)
                    perturbation_check(self,exact)
                    exact['solver_note']='aligned-face stagnation; exact seated wrench certificate'
                    return exact
                raise RuntimeError(('contact solver',sol.message,sol.x.tolist(),min(self.gaps(sol.x))))
            if min(self.gaps(sol.x)) < -2e-7:
                raise RuntimeError(('penetrating solution',sol.x.tolist()))
            candidates.append(sol)
        sol=min(candidates,key=lambda s:s.fun); q=sol.x
        if self.W == 0:
            # Rack is neutral at zero load: report its lowest touching height.
            q[3]=max(moved(np.array([[.8,3.4],[1.2,3.4]]),q)[:,1])-3.4
        # A reached artificial search bound is an unresolved branch, not support.
        assert all(lo+1e-5 < v < hi-1e-5 for v,(lo,hi) in zip(q,bounds)), q
        return self.report(q,sol.nit,writer_k)

    def report(self,q,nit,writer_k=0.):
        a=self.state(q); columns=[]; labels=[]; points=[]
        pivot=r.P+q[:2]
        for i,j in self.pairs:
            aa=moved(self.toe[i][0],q); bb=self.frame[j][0]
            if separation(aa,bb)>2e-6: continue
            for p,n in contact_points(aa,bb):
                arm=p-pivot
                columns.append([n[0],n[1],arm[0]*n[1]-arm[1]*n[0],0.])
                labels.append('frame:'+str(j)); points.append(p.tolist())
        for i in (0,1,2):
            aa=moved(self.toe[i][0],q); bb=r.p.rack(q[3])[-1][0]
            if separation(aa,bb)>2e-6: continue
            for p,n in contact_points(aa,bb):
                arm=p-pivot
                columns.append([n[0],n[1],arm[0]*n[1]-arm[1]*n[0],-n[1]])
                labels.append('rack-web'); points.append(p.tolist())
        top=moved(np.array([[.8,3.4],[1.2,3.4]]),q)
        assert np.all((top[:,0]>.6)&(top[:,0]<1.7)),top
        for p in top:
            if abs(3.4+q[3]-p[1])<2e-6:
                columns.append([0.,-1.,-(p[0]-pivot[0]),1.])
                labels.append('rack'); points.append(p.tolist())
        mat=np.array(columns).T
        required=self.gradient(q)+writer_k*np.r_[q[:3],0.]
        loads,residual=nnls(mat,required,maxiter=500) if columns else (np.zeros(0),np.linalg.norm(required))
        assert residual<2e-5, ('wrench imbalance',q,residual)
        actual=[(p+q[:2],x) for p,x in r.bodies(q[2],depth=self.depth,t=self.t)]
        rack=r.p.rack(q[3]); leaf=r.rod_bodies(a,self.t)
        # Finite solids checked independently of optimization constraints.
        # SAT tolerance accommodates the optimizer's sub-nm penetration.
        def penetrating(left,right,skip_neighbors=False):
            # Conservative vectorized broad phase; SAT decides every survivor.
            lo=np.array([[x[0],*p.min(axis=0)] for p,x in left])
            hi=np.array([[x[1],*p.max(axis=0)] for p,x in left])
            rl=np.array([[x[0],*p.min(axis=0)] for p,x in right])
            rh=np.array([[x[1],*p.max(axis=0)] for p,x in right])
            pairs=np.argwhere(np.all(np.minimum(hi[:,None,:],rh[None,:,:])-
                                     np.maximum(lo[:,None,:],rl[None,:,:])>2e-7,axis=2))
            return any(separation(left[i][0],right[j][0])<-2e-7 for i,j in pairs
                       if not skip_neighbors or abs(i-j)>1)
        assert not penetrating(leaf,leaf,skip_neighbors=True)
        assert not penetrating(actual,self.frame+rack)
        assert not penetrating(leaf,self.frame+rack+actual[:6])
        assert np.max(abs(leaf[-1][0][[3,2]]-actual[6][0][[0,1]]))<1e-8
        for dy in (-5.03,5.13):
            neighbors=[(p+[dy,0],x) for p,x in actual+self.frame+rack+leaf]
            assert not penetrating(actual+leaf,neighbors)
        key=actual[-1][0]
        overlap=max(0., min(0.,key[:,1].max())-max(-self.depth-.15,key[:,1].min()))
        active=[dict(surface=k,point=p,N=float(v)) for k,p,v in zip(labels,points,loads) if v>1e-7]
        # Ground reaction required by the imposed vertical-only rack guide.
        # Moments about (y,z)=(0,3.4+height); two load-centroid scenarios.
        rack_wrench=np.zeros(3)
        for col,p,k,v in zip(columns,points,labels,loads):
            if k.startswith('rack'):
                fy,fz=-v*np.array(col[:2]); arm=np.array(p)-[0.,3.4+q[3]]
                rack_wrench += [fy,fz,arm[0]*fz-arm[1]*fy]
        guide=[dict(load_y=y,Fy=float(-rack_wrench[0]),
                    M=float(self.W*y-rack_wrench[2])) for y in (.8,1.2)]
        return dict(q=q.tolist(),W=self.W,EI=self.EI,offset=self.offset.tolist(),
                    key_overlap=overlap, strain=float(np.max(abs(a['fiber']))),
                    spring_force=(self.EI*a['force']).tolist(), spring_moment=float(self.EI*a['moment']),
                    contacts=active, rack_guide=guide, balance_residual=float(residual),min_gap=float(min(self.gaps(q))),
                    energy=self.objective(q),iterations=nit, n=self.n,L=self.L,t=self.t,
                    gap=self.gap,shift=self.shift,depth=self.depth,writer_k=writer_k,
                    writer_wrench=(-writer_k*q[:3]).tolist())


def verify():
    # Independent analytical unloaded limit: stress-free rigid translation.
    m=Model(offset=(0.,.1),W=0.,n=32)
    z=m.solve(); assert np.max(abs(np.array(z['q'])-[0.,.1,0.,.1]))<2e-6
    assert abs(z['key_overlap']-.1)<2e-6 and z['strain']<1e-7
    # Check energy derivatives in all three toe coordinates, not just the
    # inherited prescribed heel path. Rack term is exactly W*h.
    m=Model(offset=(-.1,.1),W=.1,n=32)
    q=np.array([.01,.05,-.01,.05]); eps=1e-5; errors=[]
    for j in range(4):
        d=np.eye(4)[j]*eps
        errors.append(abs((m.objective(q+d)-m.objective(q-d))/(2*eps)-m.gradient(q)[j]))
    assert max(errors)<1e-7,errors
    # Analytical SAT controls: separation, penetration, touching and rotation.
    a=r.R(-1,1,0,1); b=r.R(-1,1,-1,0)
    assert separation(a,b)==0 and abs(separation(a+[0,.1],b)-.1)<1e-12
    assert abs(separation(a-[0,.1],b)+.1)<1e-12
    # A two-ended flat support can react a centered vertical load with no
    # tension; tipping outside that support cannot satisfy the same wrench.
    mat=np.array([[0.,0.],[1.,1.],[-1.,1.]])
    react,res=nnls(mat,[0,1,0]); assert res<1e-12 and np.max(abs(react-.5))<1e-12
    assert nnls(mat,[0,1,2])[1]>.5
    # Preserve the independently discovered omitted-rack-web failure.
    bad=np.array([.10166569,.08591169,-.03305210,.02457176])
    overlap=-separation(moved(r.R(-1.,1.6,0.,2.),bad),r.p.rack(bad[3])[-1][0])
    assert overlap>.066
    return dict(unloaded=z,energy_gradient_error=max(errors),
                omitted_web_penetration=overlap,
                evidence='self-review; no independent validation')


def perturbation_check(m,row):
    # Deterministic feasible directions; sampling is not a stability proof.
    q=np.array(row['q']); base=m.objective(q); lowest=0.; feasible=0
    for direction in itertools.product((-1.,0.,1.),repeat=3):
        if not any(direction): continue
        d=np.array(direction); d/=np.linalg.norm(d)
        for size in (1e-5,1e-3):
            v=q.copy(); v[:3]+=size*d
            v[3]=max(moved(np.array([[.8,3.4],[1.2,3.4]]),v)[:,1])-3.4
            if min(m.gaps(v))>=-1e-10:
                feasible+=1; lowest=min(lowest,m.objective(v)-base)
    assert lowest>-1e-8,(q,lowest)
    return dict(feasible_directions=feasible,minimum_energy_change=lowest)


def release(offset=(-.1,.1),W=.1,E=2200.,n=32):
    # Reversible compliance-removal witness, not the actual blade trajectory.
    # k has N/mm on translations and N mm/rad on angle (1-mm lever scaling).
    m=Model(offset=offset,W=W,E=E,n=n); q=np.zeros(4); out=[]
    for k in [1000.,100.,10.,3.,1.,.3,.1,.03,.01,.003,0.]:
        row=m.solve(q,writer_k=k); out.append(row); q=np.array(row['q'])
    direct=m.solve()
    assert np.max(abs(q-np.array(direct['q'])))<2e-4,(q,direct['q'])
    return dict(states=out,direct_pose_difference=float(np.max(abs(q-np.array(direct['q'])))))


def cases():
    # Scenario grids are deterministic bounds; no random seed or yield count.
    for geom,dy,dz,E,W in itertools.product(((12.,.3,.4),(11.5,.25,.45)),
            (-.1,0.,.1),(-.2,-.1,0.,.1),(700.,2200.),(0.,.1,1.,10.)):
        yield 'core',dict(L=geom[0],amp=geom[1],t=geom[2],offset=(dy,dz),E=E,W=W,n=16)
    for gap,shift,depth,offset,W in itertools.product((.07,.13),(-.05,.05),
            (.15,.25),((-.1,.1),(.1,-.2)),(0.,.1,10.)):
        yield 'fit',dict(gap=gap,shift=shift,depth=depth,offset=offset,E=2200.,W=W,n=32)
    for geom,offset,W,n in itertools.product(((12.,.3,.4),(11.5,.25,.45)),
            ((-.1,.1),(.1,-.2)),(.1,10.),(32,64)):
        yield 'holdout',dict(L=geom[0],amp=geom[1],t=geom[2],offset=offset,E=2200.,W=W,n=n)
    for geom,n in itertools.product(((12.,.3,.4),(11.5,.25,.45)),(32,64,128)):
        yield 'bias',dict(L=geom[0],amp=geom[1],t=geom[2],offset=(0.,-.1),W=0.,E=2200.,n=n)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    # JSON lines allow interrupted runs to preserve completed scenario evidence.
    print(json.dumps(dict(suite='verification',result=verify())),flush=True)
    if args.verify_only: return
    for group,kw in cases():
        m=Model(**kw); row=m.solve()
        if group in ('holdout','bias'): row['perturbation']=perturbation_check(m,row)
        print(json.dumps(dict(suite=group,inputs=kw,result=row)),flush=True)
    for offset,W in itertools.product(((-.1,.1),(.1,-.2)),(0.,.1)):
        print(json.dumps(dict(suite='release',offset=offset,W=W,result=release(offset,W))),flush=True)

if __name__=='__main__': main()
