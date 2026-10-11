#!/usr/bin/env python3
"""Finite prescribed braid path and bounding return laws, SI units.
Requires numpy. Not a rod/contact equilibrium solver or a material calibration.
"""
import json
import math
import numpy as np

PITCH = .00508


def centerline(L, radius, omega, strand_d, n, hand=1, phase=0., anchor=.002):
    t = np.linspace(0., 1., n + 1)
    # Smooth end transitions occupy 15% at each end; anchor radii fixed.
    u = np.clip(np.minimum(t, 1-t)/.15, 0., 1.)
    blend = u*u*(3-2*u)
    base = anchor + (radius-anchor)*blend
    # Eight strands each hand; alternating over/under at each crossing.
    ripple = 1.25*strand_d*np.maximum(hand*np.cos(8*omega*t), 0.)**2
    r = base+ripple
    phi = phase+hand*omega*t
    return np.column_stack((r*np.cos(phi), r*np.sin(phi), L*t))


def measures(points):
    edges = np.diff(points, axis=0)
    ds = np.linalg.norm(edges, axis=1)
    tangent = edges/ds[:,None]
    dual = (ds[:-1]+ds[1:])/2
    # Discrete curvature-vector norm, converges on smooth curve.
    curvature = np.linalg.norm(np.diff(tangent,axis=0),axis=1)/dual
    return ds, curvature, dual


def length(L, r, omega, d, n):
    return sum(measures(centerline(L,r,omega,d,n,h))[0].sum() for h in [-1,1])/2


def bisect(fn, lo, hi):
    flo, fhi = fn(lo), fn(hi)
    assert flo*fhi <= 0, (flo,fhi,lo,hi)
    for _ in range(55):
        mid = (lo+hi)/2
        if fn(mid)*flo>0: lo=mid
        else: hi=mid
    return (lo+hi)/2


def segments_distance(a,b):
    """Exact minimum over every polyline segment pair (interior + endpoints)."""
    p=a[:-1,None,:];q=b[None,:-1,:]
    u=np.diff(a,axis=0)[:,None,:];v=np.diff(b,axis=0)[None,:,:]
    w=p-q
    aa=(u*u).sum(2);bb=(u*v).sum(2);cc=(v*v).sum(2)
    dd=(u*w).sum(2);ee=(v*w).sum(2)
    denom=aa*cc-bb*bb
    safe=np.where(denom>1e-30,denom,1.)
    s=(bb*ee-cc*dd)/safe;t=(aa*ee-bb*dd)/safe
    valid=(denom>1e-30)&(s>=0)&(s<=1)&(t>=0)&(t<=1)
    best=np.where(valid,((w+s[:,:,None]*u-t[:,:,None]*v)**2).sum(2),np.inf)
    for se in [0.,1.]:
        te=np.clip((ee+se*bb)/cc,0,1)
        best=np.minimum(best,((w+se*u-te[:,:,None]*v)**2).sum(2))
    for te in [0.,1.]:
        se=np.clip((te*bb-dd)/aa,0,1)
        best=np.minimum(best,((w+se[:,:,None]*u-te*v)**2).sum(2))
    return float(np.sqrt(best.min()))


class Path:
    def __init__(self, r=.0015, angle=45., gap=.00015, d=.0001, n=384,
                 preload=.1, spring_k=20., EA=20., EI=1e-9):
        self.r,self.rc,self.gap,self.d,self.n=r,r+d/2,gap,d,n
        self.L0=.020;self.omega=self.L0*math.tan(math.radians(angle))/self.rc
        self.P,self.k,self.EA,self.EI=preload,spring_k,EA,EI
        self.S=length(self.L0,self.rc,self.omega,d,n)
        # Mean total length is preserved; separate hand stretch is counted below.
        self.base=[measures(centerline(self.L0,self.rc,self.omega,d,n,h)) for h in [-1,1]]
        self.Lopen=self.at(gap)['L']

    def at(self,q):
        r=self.rc+q
        L=bisect(lambda L:length(L,r,self.omega,self.d,self.n)-self.S,.002,self.L0*1.001)
        ms=[measures(centerline(L,r,self.omega,self.d,self.n,h)) for h in [-1,1]]
        bend=8*sum(.5*self.EI*np.sum(c*c*dual) for ds,c,dual in ms)
        # Fixed material at prescribed crossings: initial uniform tensile strain.
        cos0=self.L0/self.S
        e0=self.P/(16*self.EA*cos0)
        maxstrain,minstrain,inventory,jamenergy=0.,1.,0.,0.
        freeenergy=0.;free_strains=[]
        for (ds,c,dual),(ds0,_,_) in zip(ms,self.base):
            rest=ds0/(1+e0);strain=ds/rest-1
            efree=ds.sum()/rest.sum()-1
            free_strains.append(float(efree))
            freeenergy+=8*.5*self.EA*rest.sum()*max(efree,0)**2
            maxstrain=max(maxstrain,float(strain.max()))
            minstrain=min(minstrain,float(strain.min()))
            inventory=max(inventory,float(np.ptp(np.cumsum(ds-ds0))))
            jamenergy+=8*.5*self.EA*np.sum(rest*np.maximum(strain,0)**2)
        x=self.L0-L
        return dict(q=q,L=L,x=x,bend_J=float(bend),spring_J=self.P*x+.5*self.k*x*x,
                    jam_max_strain=maxstrain,jam_min_strain=minstrain,
                    migration_m=inventory,jam_stretch_J=float(jamenergy),
                    free_stretch_J=float(freeenergy),free_hand_strains=free_strains)

    def sweep(self,steps=101):
        rows=[self.at(q) for q in np.linspace(0,self.gap,steps)]
        x=np.array([a['x'] for a in rows]);U=np.array([a['bend_J']+a['spring_J']+a.get('free_stretch_J',0.) for a in rows])
        restoring=np.gradient(U,x,edge_order=2)
        for a,f in zip(rows,restoring):a['return_N']=float(f)
        return rows

    def geometry(self,q):
        a=self.at(q);L=a['L'];r=self.rc+q
        p=centerline(L,r,self.omega,self.d,self.n,1)
        cross=min(segments_distance(p,centerline(L,r,self.omega,self.d,self.n,-1,2*math.pi*k/8)) for k in range(8))
        same=segments_distance(p,centerline(L,r,self.omega,self.d,self.n,1,2*math.pi/8))
        # Polyline stalk penetration converges away as segments refine.
        edges=np.diff(p,axis=0);v=edges[:,:2];xy=p[:-1,:2]
        t=np.clip(-(xy*v).sum(1)/(v*v).sum(1),0,1)
        minrad=float(np.linalg.norm(xy+t[:,None]*v,axis=1).min())
        radius=float(np.linalg.norm(p[:,:2],axis=1).max()+self.d/2)
        return dict(cross_surface_gap_m=cross-self.d,same_surface_gap_m=same-self.d,
                    stalk_surface_gap_m=minrad-self.d/2-self.r,
                    outer_radius_m=radius,neighbor_envelope_gap_m=PITCH-2*radius)


def return_trace(rows,drag,mass=.001):
    """Quasistatic friction law on a prescribed path. Kinetic inventory from work.
    A negative initial force sticks; later zero KE stops. No impact/bounce credit.
    """
    x=np.array([a['x'] for a in rows]);U=np.array([a['bend_J']+a['spring_J']+a.get('free_stretch_J',0.) for a in rows])
    out=[]
    for fraction in [.25,.5,.75,1.]:
        j=round(fraction*(len(rows)-1));K=0.;t=0.;stuck=False
        start=j
        for k in range(j,0,-1):
            dx=x[k]-x[k-1];dK=U[k]-U[k-1]-drag*dx
            new=K+dK
            if new<=0:
                stuck=True;break
            v0=math.sqrt(2*K/mass);v1=math.sqrt(2*new/mass)
            t+=2*dx/(v0+v1);K=new
            assert math.isclose(K+drag*(x[start]-x[k-1]),U[start]-U[k-1],rel_tol=1e-10,abs_tol=1e-15)
        out.append(dict(cut_fraction=fraction,stuck=stuck,closure_s=None if stuck else t,
                        available_work_J=float(U[start]-U[0]-drag*x[start]),
                        impact_J=None if stuck else K))
    return out


def strength_bound(F,P,angle,EA=20.,d=.0001):
    # Necessary bound only: peak individual strand force exceeds equal sharing if uneven.
    f=(F+P)/(16*math.cos(math.radians(angle)))
    return dict(anchor_N=F+P,total_strand_N=16*f,per_strand_N=f,
                axial_strain=f/EA,solid_circle_stress_Pa=f/(math.pi*d*d/4),
                termination_shear_2mm_Pa=f/(math.pi*d*.002))


def capacity_extrapolation(mu,angle,r,P,L,contact_fraction):
    K=mu*L*math.tan(math.radians(angle))**2/r*contact_fraction
    return dict(down_N=P*math.expm1(K),up_N=P*-math.expm1(-K))


def cut_bound(t,F,v,C,up,m=.02,elastic=0.):
    # Favorable instantaneous capacity only after actual return time. Not braid dynamics.
    x=v*t+.5*F/m*t*t;u=v+F/m*t
    denom=(C-F) if u>=0 else (up+F)
    if denom<=0:return dict(gap_m=x,stop_m=None)
    coast=math.copysign((.5*m*u*u+elastic)/denom,u)
    return dict(gap_m=x,stop_m=x+coast)


def checks():
    # Exact skew and parallel segment distance examples.
    assert abs(segments_distance(np.array([[0.,0,0],[1,0,0]]),np.array([[.5,-1,1],[.5,1,1]]))-1)<1e-12
    assert abs(segments_distance(np.array([[0.,0,0],[1,0,0]]),np.array([[0.,2,0],[1,2,0]]))-2)<1e-12
    assert capacity_extrapolation(0,45,.0015,.1,.02,1)['down_N']==0
    assert capacity_extrapolation(.2,45,.0015,0,.02,1)['down_N']==0
    assert capacity_extrapolation(.2,45,.0015,.1,.02,0)['down_N']==0
    # Constant force return reduces to exact kinematics independent of subdivision.
    rows=[dict(x=x,bend_J=0.,spring_J=.1*x) for x in np.linspace(0,.002,101)]
    tr=return_trace(rows,.02)[-1]
    assert math.isclose(tr['closure_s'],math.sqrt(2*.002*.001/.08),rel_tol=1e-12)
    assert return_trace(rows,.12)[-1]['stuck']
    # Energy: final KE + dissipated work = released potential.
    assert math.isclose(tr['impact_J']+.02*.002,.1*.002,rel_tol=1e-12)
    d=cut_bound(0,1,.1,2,.1)['stop_m']
    assert math.isclose(2*d,.5*.02*.1**2+d)
    return True


def main():
    out=dict(checks=checks(),evidence='prescribed geometry/energy bounds; no equilibrium, material or reliability qualification')
    p=Path();rows=p.sweep()
    out['nominal']={k:rows[-1][k] for k in rows[-1]}
    out['nominal']['opening_elastic_J']=sum(rows[-1][k]-rows[0][k] for k in ['bend_J','spring_J','free_stretch_J'])
    out['nominal']['return_N_range']=[min(a['return_N'] for a in rows),max(a['return_N'] for a in rows)]
    out['nominal']['geometry']={str(q):p.geometry(q) for q in [0,p.gap/2,p.gap]}
    out['return_laws']={str(d):return_trace(rows,d) for d in [0,.05,.12,.2]}
    # An entire braid cannot share one identical free redistribution tension if
    # +/- paths have unequal length; print discrepancy rather than hide it.
    out['hand_length_difference_m']=float(p.base[0][0].sum()-p.base[1][0].sum())
    # Taut-yarn axial stiffness at fixed radius, not a finished assembly stiffness.
    kz=16*p.EA*(p.L0/p.S)**2/p.S
    out['collar_stops']=dict(open_stop_m=.004,closed_stop_reserve_m=.0002,
        mean_helix_axial_stiffness_estimate_N_per_m=kz,extension_for_preload_m=p.P/kz,
        reserve_after_common_plus_local_error_m={str(e):.0002-e for e in [0,.0001,.0002,.0003]},
        consequence='closing stop intercepting required extension can divert spring force to frame; zero strand preload is allowed')
    out['convergence']=[]
    for n in [192,384,768]:
        a=Path(n=n); rr=a.sweep(51)
        out['convergence'].append(dict(n=n,stroke_m=rr[-1]['x'],bend_delta_J=rr[-1]['bend_J']-rr[0]['bend_J'],
            max_strain=rr[-1]['jam_max_strain'],geometry=a.geometry(a.gap),return_s=return_trace(rr,.05)[-1]['closure_s']))
    out['bend_sensitivity']={}
    for EI in [0,1e-10,1e-9,1e-8]:
        r=Path(EI=EI).sweep(51)
        out['bend_sensitivity'][str(EI)]=dict(return_N_range=[min(a['return_N'] for a in r),max(a['return_N'] for a in r)],
            work_J=sum(r[-1][k]-r[0][k] for k in ['bend_J','spring_J','free_stretch_J']))
    out['coherent_bounds']={}
    for name,r,angle,gap,mu,P in [('weak',.0016,40,.0003,.1,.05),('nominal',.0015,45,.00015,.2,.1),('strong',.0014,50,.00005,.3,.15)]:
        a=Path(r=r,angle=angle,gap=gap,preload=P);rr=a.sweep(51)
        out['coherent_bounds'][name]=dict(stroke_m=rr[-1]['x'],jam_strain=rr[-1]['jam_max_strain'],
            migration_m=rr[-1]['migration_m'],neighbor=a.geometry(gap),
            all_core_contact_extrapolation=capacity_extrapolation(mu,angle,r,P,.014,1),
            half_core_contact_extrapolation=capacity_extrapolation(mu,angle,r,P,.014,.5),
            return_drag012=return_trace(rr,.12)[-1])
    out['strength']={str((F,a)):strength_bound(F,.1,a) for F in [0,1,10] for a in [45,55]}
    t=return_trace(rows,.05)[-1]['closure_s']
    cap=capacity_extrapolation(.2,45,.0015,.1,.014,.5)
    out['cuts_favorable']={str((F,v)):cut_bound(t,F,v,cap['down_N'],cap['up_N']) for F in [0,.02,1,10] for v in [-.1,0,.1]}
    # Plain clamp has equal nominal downward capacity; no leverage credit.
    C=cap['down_N'];N=C/.2;gap=.00015;k=20.;m=.001
    out['plain_clamp']=dict(capacity_N=C,normal_preload_N=N,stroke_m=gap,
        spring_work_J=N*gap+.5*k*gap*gap,
        closure_upper_s=math.sqrt(2*gap*m/(N-.12)),
        direction='symmetric',assumptions='direct jaw; same .12 N guide drag, 1 g moving mass, no rebound')
    # Capturing shoe lower-bound access: stalk r=1.5 mm, moving shoe thickness .30 mm,
    # registration .10 mm, neighbor stalk r=1.5; resident collar OD=4.6 mm.
    out['head_access']=dict(radial_shoe_outer_m=.0015+.0003+.0001,
        shoe_to_neighbor_stalk_gap_m=PITCH-(.0015+.0003+.0001)-.0015,
        collar_radial_margin_m=PITCH/2-.0023,
        bilateral_shoulder='absent on smooth stalk: side shoe remains a friction clamp',
        end_capture='bottom end spans 40 mm; release collar stationary; needs independent reach coordinate')
    out['full_capacity_plain_clamp']={str(C):dict(normal_N=C/.2,work_J=C/.2*.00015+.5*20*.00015**2,
        return_s=math.sqrt(2*.00015*.001/(C/.2-.12))) for C in [1,10]}
    # Different nonfluid search axis: cancel screw torques instead of amplifying friction.
    # Height is the differential coordinate. Common-mode torque cancellation has zero stroke.
    a=.0005/(2*math.pi)
    out['opposed_thread_inversion']={str(F):dict(torque_each_Nm=F*a/2,
        differential_rotation_rad_for_40mm=.04/a,
        common_mode_height_m=0.,raise_work_J=F*.04,
        counterweight_travel_m_for_equal_weight=.04,
        residual_work_J_with_fixed_1N_counterweight=(F-1)*.04) for F in [0,.02,1,10]}
    for F in [0,.02,1,10]:
        assert math.isclose(2*(F*a/2)*(.04/a),F*.04,abs_tol=1e-12)
    out['frame_neighbor_bound']={str((F,k)):F/k for F in [1,10] for k in [1e4,1e5,1e6]}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
