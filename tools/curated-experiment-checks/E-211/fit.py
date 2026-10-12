"""E-211 finite seat/expanding writer comparison. mm, N, MPa.
Deterministic assumed bounds, frictionless quasistatics; no qualified process.
Run OPENBLAS_NUM_THREADS=1 python fit.py [--quick]. JSON lines are disposable.
"""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import nnls, minimize

spec=importlib.util.spec_from_file_location('contact',Path(__file__).resolve().parents[1]/'E-210/contact.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
r=c.r


def clip(poly,normal,bound):
    """Clip a convex solid, retaining n dot p <= bound."""
    out=[]
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        da,db=np.dot(a,normal)-bound,np.dot(b,normal)-bound
        if da<=1e-12: out.append(a)
        if (da<0<db) or (db<0<da): out.append(a+(b-a)*da/(da-db))
    return np.array(out)


def cut(poly,kind):
    if kind=='short': return clip(poly,np.array([1.,0.]),1.35)
    if kind=='chamfer': return clip(poly,np.array([1.,.15]),1.6)
    assert kind=='web'; return poly


def bodies(q,kind='chamfer',depth=.2,t=.4,pocket=(-.85,-.05,.6,1.4)):
    # Same collar index as E-210. Widen side pocket to .8 x .8 mm.
    # Add .2-mm-thick retaining lips at the mouth, no resident moving guide.
    y0,y1,z0,z1=pocket
    out=[(cut(r.R(-1,1.6,0,2),kind),(-.9,1.5)),
         (r.R(-1,y0,0,2),(-1.5,-.9)),
         (cut(r.R(y1,1.6,0,2),kind),(-1.5,-.9)),
         (r.R(y0,y1,0,z0),(-1.5,-.9)),
         (r.R(y0,y1,z1,2),(-1.5,-.9)),
         (r.R(.8,1.2,2,3.4),(-.4,.4)),r.bodies(0,t=t)[6],
         (r.R(y0,y1,z0,.8),(-1.5,-1.3)),
         (r.R(y0,y1,1.2,z1),(-1.5,-1.3))]
    out += [(r.R(.85,1.15,-depth,0),x) for x in [(-1.5,-.85),(.85,1.5)]]
    return [(c.moved(p,q),x) for p,x in out]


class Model(c.Model):
    def __init__(self,kind='chamfer',pocket=(-.85,-.05,.6,1.4),**kw):
        super().__init__(**kw); self.kind=kind; self.pocket=pocket
        self.toe[0]=(cut(self.toe[0][0],kind),self.toe[0][1])
    def actual_bodies(self,q):
        return bodies(q,self.kind,self.depth,self.t,self.pocket)
    def solve(self,initial=None):
        bounds=[(-.3,.3),(-.05,.4),(-.12,.12),(-.3,.8)]
        sol=minimize(self.objective,np.zeros(4) if initial is None else initial,
                     jac=self.gradient,method='SLSQP',bounds=bounds,
                     constraints=[{'type':'ineq','fun':self.gaps}],
                     options={'ftol':1e-10,'maxiter':80})
        q=sol.x
        if self.W==0:q[3]=max(c.moved(np.array([[.8,3.4],[1.2,3.4]]),q)[:,1])-3.4
        assert all(lo+1e-5<v<hi-1e-5 for v,(lo,hi) in zip(q,bounds)),('search-bound',q)
        row=self.report(q,sol.nit)
        row['solver_success']=bool(sol.success)
        if not sol.success:
            row['solver_note']=sol.message+'; independent contact certificate and local perturbations'
            row['perturbation']=c.perturbation_check(self,row)
        return row


def penetrating(left,right,tol=2e-7):
    lo=np.array([[x[0],*p.min(axis=0)] for p,x in left]); hi=np.array([[x[1],*p.max(axis=0)] for p,x in left])
    rl=np.array([[x[0],*p.min(axis=0)] for p,x in right]); rh=np.array([[x[1],*p.max(axis=0)] for p,x in right])
    pairs=np.argwhere(np.all(np.minimum(hi[:,None,:],rh[None,:,:])-np.maximum(lo[:,None,:],rl[None,:,:])>tol,axis=2))
    return any(c.separation(left[i][0],right[j][0])<-tol for i,j in pairs)


def tool(q,ez=.3,ey=.2,dx=0.):
    # Four independently driven expanding shoes and a .12-mm stem.
    # Slider/drive envelopes explicitly require reusable precision guidance;
    # the drives, bearings and compliant force control are NOT synthesized.
    zu,zl=np.broadcast_to(ez,(2,));yl,yr=np.broadcast_to(ey,(2,))
    out=[(r.R(-.65,-.25,.94,1.06),(-2.,-1.05)),
         (r.R(-.7,-.2,1+zu,1.1+zu),(-1.25,-1.0)),
         (r.R(-.7,-.2,.9-zl,1-zl),(-1.25,-1.0)),
         (r.R(-.65-yl,-.55-yl,.85,1.15),(-1.25,-1.0)),
         (r.R(-.35+yr,-.25+yr,.85,1.15),(-1.25,-1.0)),
         (r.R(-.7,-.2,.6,1.4),(-2.2,-1.8))]
    # Telescoping links: swept material envelopes, not a claimed buildable
    # internal mechanism. Each meets stem and its driven shoe by finite volume.
    out += [(r.R(-.6,-.3,1.0,1.05+zu),(-1.2,-1.05)),
            (r.R(-.6,-.3,.95-zl,1.0),(-1.2,-1.05)),
            (r.R(-.6-yl,-.55,.95,1.05),(-1.2,-1.05)),
            (r.R(-.35,-.3+yr,.95,1.05),(-1.2,-1.05))]
    return [(c.moved(p,q),(x[0]+dx,x[1]+dx)) for p,x in out]


def closure(m):
    y0,y1,z0,z1=m.pocket
    return np.array([z1-1.1,.9-z0]),np.array([-.65-y0,y1+.25])


def fitted_tool(m,q,scale=1.,dx=0.):
    ez,ey=closure(m)
    return tool(q,ez*scale,ey*scale,dx)


def wrench_fit(m,q,ez=None,ey=None):
    if ez is None: ez,ey=closure(m)
    # Actual blade-wall contacts. Positive reaction basis must span arbitrary
    # signed planar wrench; no friction, no face contacts across an open gap.
    points=[];cols=[]
    for aa,x in tool(q,ez,ey)[1:5]:
        for bb,y in m.actual_bodies(q):
            if min(x[1],y[1])-max(x[0],y[0])<1e-9: continue
            if c.separation(aa,bb)>2e-6: continue
            for p,n in c.contact_points(aa,bb):
                arm=p-(r.P+q[:2]); cols.append([*n,arm[0]*n[1]-arm[1]*n[0]])
                points.append(p.tolist())
    mat=np.array(cols).T if cols else np.zeros((3,0))
    targets=list(np.vstack((np.eye(3),-np.eye(3))))
    # Reactions on the writer balance the return's opposite end wrench.
    demand=-m.gradient(np.r_[q[:3],0.])[:3]
    targets.append(demand)
    fits=[nnls(mat,x,maxiter=1000) if cols else (np.array([]),np.linalg.norm(x)) for x in targets]
    return dict(rank=int(np.linalg.matrix_rank(mat)) if cols else 0,
                basis_residual=max(float(x[1]) for x in fits[:-1]),
                demanded_residual=float(fits[-1][1]),
                reaction_peak=float(max(fits[-1][0],default=0)),
                demand=demand.tolist())


def acquisition(m,row,steps=24):
    q=np.array(row['q']); toe=m.actual_bodies(q)
    obs=toe+m.frame+r.p.rack(q[3]); fail=[]
    for dx in np.linspace(-.8,0,steps+1):
        if penetrating(tool(q,0,0,dx),obs): fail.append('insert')
    for f in np.linspace(0,1,steps+1):
        if penetrating(fitted_tool(m,q,f),obs): fail.append('expand')
    # Expanded shoulders must hit mouth lips before axial escape; stem must
    # have finite gap to mouth. Closed tools must withdraw. Actual prisms.
    axial_block=penetrating(fitted_tool(m,q,dx=-.08),toe)
    free_slack=not penetrating(fitted_tool(m,q,dx=-.04),toe)
    fit=wrench_fit(m,q)
    assert fit['basis_residual']<1e-8 and axial_block and free_slack
    # Registration uncertainty is additional to following the released pose.
    # +/- .05 mm y,z and +/- .02 rad are labelled head error bounds.
    misses=0
    for dy,dz,da in itertools.product((-.05,.05),(-.05,.05),(-.02,.02)):
        qt=q+np.array([dy,dz,da,0.])
        misses+=penetrating(tool(qt,0,0),obs)
    return dict(collisions=sorted(set(fail)),registration_corner_collisions=misses,
                axial_retention=True,fit=fit)


def jaw(lift,bounds=(1.35,1.65),dx=0.):
    out=[]
    for p,x in r.p.writer(lift,dx):
        p=p.copy();p[:,0]=bounds[0]+(p[:,0]-1.35)*(bounds[1]-bounds[0])/.3
        out.append((p,x))
    return out


def sequence(m,row,steps=32,bow=0.,jaw_bounds=(1.35,1.65),withdraw=1.4):
    # Oracle pose acquisition is deliberately distinguished from implemented
    # sensing. Hold the released pose, take rack, lift, bring toe to seated
    # datum, rock/withdraw/return, restore released pose, transfer rack, depart.
    q=np.array(row['q']); seq=[]
    for h in np.linspace(q[3],1.5,steps+1): seq.append(('lift',np.r_[q[:3],h]))
    for f in np.linspace(0,1,steps+1)[1:]:
        v=(1-f)*q[:3];v[1]+=bow*np.sin(np.pi*f)
        seq.append(('register',np.r_[v,1.5]))
    out=[np.array([0.,0.,a,1.5]) for a in np.linspace(0,.22,steps+1)]
    out += [np.array([-w,0.,.22,1.5]) for w in np.linspace(0,withdraw,steps+1)[1:]]
    seq += [('rock-withdraw',v) for v in out]
    seq += [('return',v) for v in out[-2::-1]]
    for f in np.linspace(0,1,steps+1):
        v=f*q[:3];v[1]+=bow*np.sin(np.pi*f)
        seq.append(('restore',np.r_[v,1.5]))
    for h in np.linspace(1.5,q[3],steps+1)[1:]:seq.append(('lower',np.r_[q[:3],h]))
    fail=None;peak=0.;force=0.;reaction=0.;residual=0.;stem_stress=0.
    for phase,v in seq:
        b=m.actual_bodies(v); t=fitted_tool(m,v); rack=r.p.rack(v[3]); cj=jaw(v[3],jaw_bounds)
        for name,left,right in [('toe',b,m.frame+rack+cj),('tool',t,b+m.frame+rack+cj)]:
            if penetrating(left,right) and fail is None:fail=dict(phase=phase,body=name,q=v.tolist())
        a=m.state(v);leaf=r.rod_bodies(a,m.t)
        if penetrating(leaf,m.frame+rack+cj+t+b[:6]) and fail is None:fail=dict(phase=phase,body='leaf',q=v.tolist())
        assert np.max(abs(leaf[-1][0][[3,2]]-b[6][0][[0,1]]))<1e-8
        peak=max(peak,float(np.max(abs(a['fiber']))));force=max(force,float(np.linalg.norm(a['force'])*m.EI))
        fit=wrench_fit(m,v); assert fit['basis_residual']<1e-8
        reaction=max(reaction,fit['reaction_peak']);residual=max(residual,fit['demanded_residual'])
        # Favorable gross-section beam screen for the actual .4 x .12-mm
        # stem, unsupported .55 mm from shank to first internal shoe edge.
        # Ignores transferred torsion, stress concentrations and drive cutouts.
        co,si=np.cos(v[2]),np.sin(v[2])
        local_force=m.EI*a['force']@np.array([[co,-si],[si,co]])
        stress=.55*(abs(local_force[1])/(.4*.12**2/6)+abs(local_force[0])/(.12*.4**2/6))
        stem_stress=max(stem_stress,float(stress))
        # Adjacent stationary sites: no deliberate reset or head there.
        for dy in (-5.03,5.13):
            neighbor=[(p+[dy,0],x) for p,x in m.actual_bodies(q)+m.frame+r.p.rack(q[3])]
            if penetrating(b+t+leaf,neighbor) and fail is None:fail=dict(phase=phase,body='row-neighbor',q=v.tolist())
        for dx in (-5.08,5.08):
            neighbor=[(p,(x[0]+dx,x[1]+dx)) for p,x in m.actual_bodies(q)+m.frame+r.p.rack(q[3])]
            if penetrating(b+t,neighbor) and fail is None:fail=dict(phase=phase,body='column-neighbor',q=v.tolist())
    # Open geometry excludes rack's full 40-mm movement by y projection.
    op=out[-1];parts=m.actual_bodies(op)+fitted_tool(m,op)+r.rod_bodies(m.state(op),m.t)
    travel_gap=.6-max(p[:,0].max() for p,x in parts)
    assert travel_gap>0
    open_toe_frame_gap=min(c.separation(a,b) for a,x in m.actual_bodies(op)
                           for b,y in m.frame if min(x[1],y[1])-max(x[0],y[0])>1e-9)
    jaw_travel_gap=jaw_bounds[0]-max(p[:,0].max() for p,x in parts)
    assert jaw_travel_gap>0
    # Exact vertical unions include all twenty unequal five-height moves.
    swept=[(r.R(p[:,0].min(),p[:,0].max(),p[:,1].min()-40,p[:,1].max()+40),x)
           for p,x in r.p.rack(1.5)+jaw(1.5,jaw_bounds)]
    assert not penetrating(parts+m.frame,swept)
    # Jaw inserts from +x at the actual rack height; inherited exact jaw
    # closure remains a separate grant, not solved by the new toe tool.
    for dx in np.linspace(2,0,steps+1):
        if penetrating(jaw(q[3],jaw_bounds,dx),m.actual_bodies(q)+m.frame+r.p.rack(q[3])+fitted_tool(m,q)) and fail is None:
            fail=dict(phase='rack-acquire',body='jaw')
    lower_y,upper_y=jaw_bounds[0]+.05,jaw_bounds[1]-.05
    upper=10*(lower_y-.8)/(upper_y-lower_y)
    return dict(first_collision=fail,bow=bow,withdraw=withdraw,jaw_bounds=jaw_bounds,
                jaw_lower_N_at_10N=10+upper,jaw_upper_N_at_10N=upper,poses=len(seq),peak_strain=peak,force_N=force,
                max_contact_N=reaction,stem_bending_MPa=stem_stress,open_toe_frame_gap=open_toe_frame_gap,wrench_residual=residual,open_rack_gap=travel_gap,jaw_travel_gap=jaw_travel_gap,
                lower_jaw_pressure_MPa_at_10N=(10+upper)/(.75*(jaw_bounds[1]-jaw_bounds[0])))


def verify():
    # Independent corner excursion and full finite prescribed release path.
    trials=0
    for kind,gap,shift,depth in itertools.product(('web','chamfer'),(.17,.23),(-.05,.05),(.15,.25)):
        frame=r.fixed(gap,shift,depth)
        for angle,w in [(a,0.) for a in np.linspace(0,.22,65)]+[(.22,w) for w in np.linspace(0,1.2,65)]:
            q=np.array([-w,0.,angle,1.5]);b=bodies(q,kind,depth);t=tool(q)
            assert not penetrating(b+t,frame+r.p.rack(1.5)+jaw(1.5,(1.45,1.68)))
            assert not penetrating(t,b)
            trials+=1
    # Distinct failure controls: old end stroke penetrates neighbor web;
    # wide .6-mm shoes miss at combined pocket/pose error; .5-mm shoes clear.
    q=np.array([-1.4,0.,.22,1.5]);old=bodies(q,'web')
    prev=[(p+[-5.03,0],x) for p,x in r.p.rack()]
    penetration=max(-c.separation(a[0],b[0]) for a in old for b in prev
                    if min(a[1][1],b[1][1])-max(a[1][0],b[1][0])>0)
    assert abs(penetration-.0064592461617385)<1e-10
    # Direct centered rod checks preserve E-209 units and energy/work tests.
    m=Model(n=16);q=np.zeros(4);m.pocket=(-.8,0.,.65,1.45)
    qt=np.array([-.05,-.05,.02,0.]);wide=tool(qt,0,0)
    wide[1]=(c.moved(r.R(-.75,-.15,1,1.1),qt),(-1.25,-1.0))
    assert penetrating(wide,m.actual_bodies(q))
    assert not penetrating(tool(qt,0,0),m.actual_bodies(q))
    echeck=c.e.verify()
    return dict(finite_release_poses=trials,old_neighbor_penetration=penetration,
                inherited_rod_checks=echeck)


def holdouts(emit):
    # Refinement of accepted interface, plus adverse registration/return stock.
    for kind in ('web','chamfer'):
        previous=None
        for n,steps in ((32,32),(64,64)):
            m=Model(kind=kind,gap=.2,offset=(-.1,.1),W=.1,E=2200.,n=n)
            row=m.solve();out=sequence(m,row,steps=steps,bow=.02,jaw_bounds=(1.35,1.65) if kind=='web' else (1.45,1.68),withdraw=1.2)
            if previous is not None:
                out['pose_refinement']=float(np.max(abs(np.array(row['q'])-previous)))
            previous=np.array(row['q']);out['perturbation']=c.perturbation_check(m,row)
            emit('holdout',inputs=dict(kind=kind,n=n,steps=steps),released=row,result=out)
    for L,amp,t,offset in ((12.,.3,.4,(.1,-.1)),(11.5,.25,.45,(-.1,.1)),(11.5,.25,.45,(.1,-.1))):
        m=Model(kind='chamfer',gap=.2,offset=offset,W=.1,E=2200.,n=32,L=L,amp=amp,t=t)
        row=m.solve();out=sequence(m,row,steps=32,bow=.02,jaw_bounds=(1.45,1.68),withdraw=1.2)
        emit('stock_holdout',inputs=dict(L=L,amp=amp,t=t,offset=offset),released=row,result=out)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--suite',choices=('all','released','sequence','fit','verify','holdouts'),default='all');args=parser.parse_args()
    def emit(s,**x):print(json.dumps(dict(suite=s,**x)),flush=True)
    if args.suite in ('all','verify'):emit('verification',result=verify())
    if args.suite in ('all','holdouts'):holdouts(emit)
    # Analytical continuous key release bound; .10 mm improvement independent
    # of rod/contact optimizer. Forward support width is traded against it.
    excursion=np.hypot(2.15,.25)-2.15
    emit('bounds',old_reserve=.07-.05-excursion,new_reserve=.17-.05-excursion,
         new_front_bearing_min=1.6-(1.15+.23+.05),short_front_bearing=1.35-(1.15+.23+.05),
         rear_pocket_wall_range=[-.85+error-(-1.) for error in (-.05,.05)])
    for kind,fit,offset,W in itertools.product(('web','short','chamfer'),((.17,-.05,.15),(.23,.05,.25)),((-.1,.1),(.1,-.1),(0.,0.)),(0.,.1,10.)):
        if args.suite not in ('all','released'):continue
        gap,shift,depth=fit
        if args.quick and (gap,shift,depth,offset,W)!=(.17,-.05,.15,(-.1,.1),.1):continue
        kw=dict(kind=kind,gap=gap,shift=shift,depth=depth,offset=offset,W=W,E=2200.,n=16)
        try:
            m=Model(**kw);row=m.solve();acq=acquisition(m,row)
            emit('released',inputs=kw,result=row,acquisition=acq)
        except (AssertionError,RuntimeError) as err:emit('unresolved',inputs=kw,error=str(err))
    for kind in ('web','short','chamfer'):
        if args.suite not in ('all','sequence'):continue
        kw=dict(kind=kind,gap=.2,offset=(-.1,.1),W=.1,E=2200.,n=32)
        m=Model(**kw);row=m.solve()
        for bow,jb,w in ((0.,(1.35,1.65),1.4),(.02,(1.35,1.65),1.4),(.02,(1.35,1.65),1.2),(.02,(1.45,1.68),1.2)):
            emit('sequence',inputs=kw,result=sequence(m,row,steps=16 if args.quick else 32,bow=bow,jaw_bounds=jb,withdraw=w))
    if args.suite in ('all','fit'):
        kw=dict(kind='chamfer',gap=.2,offset=(-.1,.1),W=.1,E=2200.,n=32)
        m=Model(**kw);row=m.solve()
        for errors in itertools.product((-.05,.05),repeat=4):
            m.pocket=tuple(np.array([-.85,-.05,.6,1.4])+errors)
            acq=acquisition(m,row)
            emit('pocket_fit',pocket=m.pocket,strokes=[x.tolist() for x in closure(m)],result=acq)
    # A one-axis split blade positively retains x, yet has no y reactions.
    m=Model(offset=(0,0),W=0,n=16);q=np.zeros(4)
    emit('tool_controls',loose=wrench_fit(m,q,0,0),z_only=wrench_fit(m,q,.3,0),four_shoe=wrench_fit(m,q))

if __name__=='__main__':main()
