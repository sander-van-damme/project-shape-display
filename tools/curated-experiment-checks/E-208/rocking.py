"""E-208; mm, N, MPa. Finite rocking seat and clamped intrinsic-curvature rod.
Deterministic bounds, no measured material or manufacturing distributions.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location('prior',Path(__file__).resolve().parents[1]/'E-207/keyed_toe.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
R=p.R
P=np.array([-1.,0.])
A=np.array([-.6,-.2])


def collides(left,right):
    # Batched broad phase; exact convex SAT only for overlapping finite AABBs.
    lo=np.array([[x[0],*q.min(axis=0)] for q,x in left]);hi=np.array([[x[1],*q.max(axis=0)] for q,x in left])
    rl=np.array([[x[0],*q.min(axis=0)] for q,x in right]);rh=np.array([[x[1],*q.max(axis=0)] for q,x in right])
    pairs=np.argwhere(np.all(np.minimum(hi[:,None,:],rh[None,:,:])-np.maximum(lo[:,None,:],rl[None,:,:])>1e-10,axis=2))
    return any(p.hit(left[i],right[j]) for i,j in pairs)


def move(poly,angle,withdraw=0.):
    c,s=math.cos(angle),math.sin(angle)
    return (poly-P)@np.array([[c,s],[-s,c]])+P+[-withdraw,0.]


def bodies(angle,withdraw=0.,depth=.2,t=.4):
    # Pocket in the left wing: finite blind socket open toward -x. Its two
    # opposing horizontal faces allow reusable tool force and couple input.
    out=[(R(-1,1.6,0,2),(-.9,1.5)),
         (R(-1,-.6,0,2),(-1.5,-.9)),(R(-.3,1.6,0,2),(-1.5,-.9)),
         (R(-.6,-.3,0,.8),(-1.5,-.9)),(R(-.6,-.3,1.2,2),(-1.5,-.9)),
         (R(.8,1.2,2,3.4),(-.4,.4)),
         (np.array([[-.6-t/2,-.2],[-.6+t/2,-.2],[-.2,.4],[-1,.4]]),(-.4,.4))]
    out.extend((R(.85,1.15,-depth,0),x) for x in [(-1.5,-.85),(.85,1.5)])
    return [(move(q,angle,withdraw),x) for q,x in out]


def tool(angle,withdraw=0.,dx=0.):
    # Favorable exact closed fit, not an actuator or tolerance qualification.
    # Blade and external shank connect through positive finite volume.
    return [(move(R(-.6,-.3,.8,1.2),angle,withdraw),(-2.+dx,-.9+dx)),
            (move(R(-.7,-.2,.6,1.4),angle,withdraw),(-2.2+dx,-1.8+dx))]


def fixed(gap=.1,shift=0.,depth=.2,D=12.):
    out=p.frame(gap,shift,depth)
    # Add actual heel ledges, separated from forward bearing by tool-free bay.
    out.extend((R(-1.05,-.7,-.8,0),x) for x in [(-1.7,-.85),(.85,1.7)])
    # Replace original root crossbar and ledge to meet the curved leaf root.
    out[10]=(R(-1.5,-1.1,-D-1,-D-.2),(-1.7,1.7))
    out[11]=(R(-1.5,-.3,-D-1,-D-.2),(-.4,.4))
    return out


def path(steps=64,gap=.1,shift=0.,depth=.2):
    f=fixed(gap,shift,depth)
    first=None; counts={k:0 for k in ['toe_frame','tool_frame','toe_rack','tool_rack','toe_writer','tool_writer']}
    poses=[(a,0.) for a in np.linspace(0,.22,steps+1)]
    poses += [(.22,w) for w in np.linspace(0,1.4,steps+1)[1:]]
    # Lift rack farther than E-207 to accommodate rocking pad rise.
    rack=p.rack(1.5);writer=p.writer(1.5)
    for i,(a,w) in enumerate(poses):
        b=bodies(a,w,depth);t=tool(a,w)
        for key,left,right in [('toe_frame',b,f),('tool_frame',t,f),('toe_rack',b,rack),('tool_rack',t,rack),('toe_writer',b,writer),('tool_writer',t,writer)]:
            bad=collides(left,right)
            counts[key]+=bad
            if bad and first is None:first={'pose':i,'angle':a,'withdraw':w,'pair':key}
        assert not collides(b,t)
    open_gap=.6-max(q[:,0].max() for q,x in b)
    # All rack travel heights excluded by y projection, not endpoint samples.
    assert open_gap>0
    return {'steps':steps,'first':first,'collision_poses':counts,'open_gap':float(open_gap)}


def rod_reference(n,L,amp):
    th=-amp*np.sin(np.linspace(0,2*math.pi,n+1))
    ds=L/n
    pos=np.vstack(([0.,0.],np.cumsum(ds/2*np.c_[np.sin(th[:-1])+np.sin(th[1:]),np.cos(th[:-1])+np.cos(th[1:])],axis=0)))
    return th,pos


def rod(angle,withdraw=0.,n=32,L=12.,amp=.5,initial=None):
    ref,rpos=rod_reference(n,L,amp);ds=L/n
    root=A-rpos[-1]
    target=move(A[None,:],angle,withdraw)[0]-root
    # theta is measured from +z; rigid body positive angle means theta=-angle.
    th=ref.copy() if initial is None else initial.copy();th[-1]=-angle
    v=th[1:-1].copy();lam=np.zeros(2)
    B=np.diag(np.full(n-1,2/ds))+np.diag(np.full(n-2,-1/ds),1)+np.diag(np.full(n-2,-1/ds),-1)
    weights=np.ones(n+1);weights[[0,-1]]=.5
    def values(v,lam):
        th=np.r_[ref[0],v,-angle];sn,cs=np.sin(th),np.cos(th)
        err=np.diff(th-ref)
        grad=(err[:-1]-err[1:])/ds
        J=ds*np.vstack((cs[1:-1],-sn[1:-1]))
        residual=np.array([ds*np.dot(weights,sn),ds*np.dot(weights,cs)])-target
        g=grad+J.T@lam
        H=B+np.diag(ds*(-lam[0]*sn[1:-1]-lam[1]*cs[1:-1]))
        K=np.block([[H,J.T],[J,np.zeros((2,2))]])
        return np.r_[g,residual],K,th,J,H
    for iteration in range(70):
        res,K,th,J,H=values(v,lam)
        if max(abs(res))<2e-10:break
        try: step=np.linalg.solve(K,-res)
        except np.linalg.LinAlgError:return None
        base=np.linalg.norm(res);fac=1.
        while fac>1e-7:
            nv=v+fac*step[:-2];nl=lam+fac*step[-2:]
            if np.linalg.norm(values(nv,nl)[0])<base: v,lam=nv,nl;break
            fac*=.5
        else:return None
    else:return None
    pos=root+np.vstack(([0.,0.],np.cumsum(ds/2*np.c_[np.sin(th[:-1])+np.sin(th[1:]),np.cos(th[:-1])+np.cos(th[1:])],axis=0)))
    # Tangent-space Hessian tests this discrete constrained local minimum.
    _,_,V=np.linalg.svd(J,full_matrices=True);Z=V[2:].T
    eig=float(np.linalg.eigvalsh(Z.T@H@Z)[0])
    kappa=np.diff(th-ref)/ds
    endgrad=(th[-1]-ref[-1]-th[-2]+ref[-2])/ds
    endjac=ds*.5*np.array([math.cos(th[-1]),-math.sin(th[-1])])
    # Normalized external end load and moment (multiply by EI).
    force=-lam;moment=-(endgrad+endjac@lam) # positive rigid-body pitch
    return {'theta':th,'pos':pos,'curvature_change':kappa,'force_over_EI':force,'moment_over_EI':moment,'energy_over_EI':float(np.dot(np.diff(th-ref),np.diff(th-ref))/(2*ds)), 'residual':float(max(abs(res))), 'eig':eig,'D':float(rpos[-1,1])}


def rod_bodies(a,t=.4):
    normal=np.c_[np.cos(a['theta']),-np.sin(a['theta'])]
    left=a['pos']-t/2*normal;right=a['pos']+t/2*normal
    return [(np.array([left[i],right[i],right[i+1],left[i+1]]),(-.4,.4)) for i in range(len(left)-1)]


def rod_path(n=32,steps=32,L=12.,amp=.5,t=.4,neighbor_bias=0.):
    initial=None;peak=0.;min_eig=1e10;max_force=0.;max_moment=0.;max_socket_force=0.;first=None
    poses=[(a,0.) for a in np.linspace(0,.22,steps+1)]+[(.22,w) for w in np.linspace(0,1.4,steps+1)[1:]]
    for i,(angle,w) in enumerate(poses):
        a=rod(angle,w,n,L,amp,initial)
        if a is None:return {'failure':'equilibrium_not_found','pose':i,'angle':angle,'withdraw':w,'amp':amp}
        assert a['eig']>0
        initial=a['theta'];peak=max(peak,float(max(abs(a['curvature_change']))*t/2));min_eig=min(min_eig,a['eig'])
        max_force=max(max_force,float(np.linalg.norm(a['force_over_EI'])));max_moment=max(max_moment,abs(a['moment_over_EI']))
        c,s=math.cos(angle),math.sin(angle)
        F=a['force_over_EI']@np.array([[c,-s],[s,c]])
        arm=A-np.array([-.45,1.])
        M=a['moment_over_EI']+arm[0]*F[1]-arm[1]*F[0]
        vertical=[F[1]/2-M/.2,F[1]/2+M/.2]
        # Signed reactions select opposing pocket walls; lever arms lie inside.
        assert abs(sum(vertical)-F[1])<1e-12
        assert abs(.1*(vertical[1]-vertical[0])-M)<1e-12
        max_socket_force=max(max_socket_force,*map(abs,vertical),abs(F[0]))
        leaf=rod_bodies(a,t)
        # Full-area leaf/collar join, including rotated finite face.
        collar=bodies(angle,w,t=t)[6][0]
        assert np.max(abs(leaf[-1][0][[3,2]]-collar[[0,1]]))<1e-9
        obstacles=fixed(D=a['D'])+p.rack(1.5)+p.writer(1.5)+tool(angle,w)
        collision=collides(leaf,obstacles)
        # Also check toe except intentional leaf/collar join; adjacent rows.
        collision |= collides(leaf,bodies(angle,w)[:6])
        for dy in (-5.08,5.08):
            neighbor=[(q+[dy+neighbor_bias,0],x) for q,x in bodies(0)+fixed(D=a['D'])+p.rack()]
            collision |= collides(leaf,neighbor)
        if collision and first is None:first={'pose':i,'angle':angle,'withdraw':w}
    assert max(q[:,0].max() for q,x in leaf+bodies(angle,w)+tool(angle,w))<.6
    return {'n':n,'steps':steps,'L':L,'amp':amp,'t':t,'first_collision':first,'peak_strain':peak,'min_reduced_hessian':min_eig,'max_force_over_EI':max_force,'max_moment_over_EI':max_moment,'max_socket_reaction_over_EI':max_socket_force,'neighbor_bias':neighbor_bias,'D':a['D'],'root_slack':L-a['D']}


def verify():
    rest=rod(0,0,n=64,amp=.3)
    assert rest['energy_over_EI']<1e-20
    assert np.max(abs(rest['force_over_EI']))<1e-12
    # Independent energy/work holdouts test both force and moment signs.
    errors=[]
    for angle,w in [(.1,0),(.22,.7),(.22,1.4)]:
        b=rod(angle,w,n=64,amp=.3);eps=1e-5
        q1=rod(angle+eps,w,n=64,amp=.3);q0=rod(angle-eps,w,n=64,amp=.3)
        de=(q1['energy_over_EI']-q0['energy_over_EI'])/(2*eps)
        da=(move(A[None,:],angle+eps,w)[0]-move(A[None,:],angle-eps,w)[0])/(2*eps)
        errors.append(abs(de-(b['force_over_EI']@da+b['moment_over_EI'])))
        q1=rod(angle,w+eps,n=64,amp=.3);q0=rod(angle,w-eps,n=64,amp=.3)
        errors.append(abs((q1['energy_over_EI']-q0['energy_over_EI'])/(2*eps)+b['force_over_EI'][0]))
    assert max(errors)<1e-7
    # Tool acquisition and supported rack takeover before rocking.
    for dx in np.linspace(-.7,0,33):
        assert not collides(tool(0,dx=dx),bodies(0)+fixed()+p.rack())
    for dx in np.linspace(2,0,33):
        assert not collides(p.writer(dx=dx),bodies(0)+fixed()+p.rack()+tool(0))
    for lift in np.linspace(0,1.5,33):
        assert not collides(p.writer(lift),bodies(0)+fixed()+p.rack(lift)+tool(0))
        assert not collides(p.rack(lift),bodies(0)+fixed()+tool(0))
    # Finite neighboring row/column checks for toe and tool at all phases.
    for angle,w in [(a,0.) for a in np.linspace(0,.22,33)]+[(.22,w) for w in np.linspace(0,1.4,33)]:
        moving=bodies(angle,w)+tool(angle,w)
        neighbor=bodies(0)+fixed()+p.rack()
        for dy in [-5.08,5.08]:
            assert not collides(moving,[(q+[dy,0],x) for q,x in neighbor])
        for dx in [-5.08,5.08]:
            assert not collides(moving,[(q,(x[0]+dx,x[1]+dx)) for q,x in neighbor])
    # Closed-form key front excursion during rocking, deepest bounded key.
    key_outward=math.sqrt(2.15**2+.25**2)-2.15
    # The key rear boundary travels forward while still below z=0; its
    # rear-wall clearance cannot decrease. The front maximum is above.
    assert key_outward<.02
    min_key_height=1.85*math.sin(.22)-.25*math.cos(.22)
    assert min_key_height>0
    # A straight inextensible rod cannot reach the lifted attachment.
    moved=move(A[None,:],.22)[0]
    direct_distance=np.linalg.norm(moved-(A-[0,12]))
    assert direct_distance>12
    return {'energy_work_max_error':max(errors),'key_outward_max':key_outward,
            'key_lift_clearance':min_key_height,
            'straight_min_extension_strain':direct_distance/12-1,
            'contacts':p.contacts()}


def main():
    out={'verification':verify(),'geometry':[path(s) for s in (32,64,128)],
         'corners':[path(64,g,s,d) for g,s,d in itertools.product((.07,.13),(-.05,.05),(.15,.25))],
         'rods':[rod_path(32,32,amp=a) for a in (.3,.5,.7)],
         'convergence':[rod_path(n,n,amp=.3) for n in (16,64,128)],
         'extensible_holdouts':[extensible_holdout(n=n,L=L,amp=a,t=t) for n in (32,64) for L,a,t in [(12.,.3,.4),(11.5,.25,.45)]],
         'return_bounds':[rod_path(32,32,L=L,amp=a,t=t,neighbor_bias=.05)
                          for L,a,t in itertools.product((11.5,12.5),(.25,.35),(.35,.45))]}
    print(json.dumps(out,indent=2))



def extensible_holdout(angle=.22,withdraw=1.4,n=32,L=11.5,amp=.25,t=.45):
    """Independent richer KKT: segment axial stretch plus nodal bending.
    Dimensionless stiffness EA/EI=12/t². No new calibrated material claim.
    Only endpoint holdouts; does not certify the extensible swept path.
    """
    ref,rpos=rod_reference(n,L,amp);ds=L/n;k=12/t**2
    target=move(A[None,:],angle,withdraw)[0]-(A-rpos[-1])
    seed=rod(angle,withdraw,n,L,amp)
    x=np.r_[seed['theta'][1:-1],np.ones(n),-seed['force_over_EI']]
    B=np.diag(np.full(n-1,2/ds))+np.diag(np.full(n-2,-1/ds),1)+np.diag(np.full(n-2,-1/ds),-1)
    def value(x):
        th=np.r_[0.,x[:n-1],-angle];e=x[n-1:2*n-1];lam=x[-2:]
        sn,cs=np.sin(th),np.cos(th)
        tangent=.5*np.c_[sn[:-1]+sn[1:],cs[:-1]+cs[1:]]
        err=np.diff(th-ref);g=(err[:-1]-err[1:])/ds
        v=ds*.5*np.c_[cs[1:-1],-sn[1:-1]]
        Jth=(e[:-1]+e[1:])[:,None]*v
        ge=ds*(k*(e-1)+tangent@lam)
        residual=np.r_[g+Jth@lam,ge,ds*(e@tangent)-target]
        H=B+np.diag(ds*.5*(e[:-1]+e[1:])*(-lam[0]*sn[1:-1]-lam[1]*cs[1:-1]))
        cross=np.zeros((n-1,n));couple=v@lam
        for i in range(n-1):cross[i,i:i+2]=couple[i]
        J=np.vstack((Jth,ds*tangent))
        hess=np.block([[H,cross],[cross.T,ds*k*np.eye(n)]])
        K=np.block([[hess,J],[J.T,np.zeros((2,2))]])
        return residual,K,th,e,lam,tangent
    for iteration in range(70):
        res,K,th,e,lam,tangent=value(x)
        if max(abs(res))<2e-10:break
        step=np.linalg.solve(K,-res);fac=1.
        while fac>1e-7:
            candidate=x+fac*step
            if min(candidate[n-1:2*n-1])>0 and np.linalg.norm(value(candidate)[0])<np.linalg.norm(res):x=candidate;break
            fac*=.5
        else:raise AssertionError('extensible line search')
    else:raise AssertionError('extensible convergence')
    # Independent finite-difference residual Jacobian at converged state.
    eps=1e-6;err=0.
    for j in range(len(x)):
        d=np.zeros(len(x));d[j]=eps
        err=max(err,float(max(abs((value(x+d)[0]-value(x-d)[0])/(2*eps)-K[:,j]))))
    assert err<1e-6
    curvature=np.diff(th-ref)/ds
    total=max(np.max(abs(e-1+t/2*curvature)),np.max(abs(e-1-t/2*curvature)))
    J=K[:-2,-2:];_,_,V=np.linalg.svd(J.T,full_matrices=True);Z=V[2:].T
    eig=float(np.linalg.eigvalsh(Z.T@K[:-2,:-2]@Z)[0]);assert eig>0
    force=float(np.linalg.norm(lam))
    return {'n':n,'L':L,'amp':amp,'t':t,'force_over_EI':force,'max_axial_strain':float(max(abs(e-1))),
            'peak_combined_fiber_strain':float(total),'jacobian_error':err,'residual':float(max(abs(res))),
            'min_reduced_hessian':eig,'inextensible_force_over_EI':float(np.linalg.norm(seed['force_over_EI']))}


if __name__=='__main__':main()
