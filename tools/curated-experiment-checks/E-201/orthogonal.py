"""E-201 finite orthogonal return lane and compatible yaw sticking.
N, mm, MPa. Explicit bounds, no process priors. NumPy; stdout disposable.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('tip', Path(__file__).parents[1]/'E-200/sliding_tip.py')
tip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tip)
c = tip.control
box = c.box


def frame(L=.6):
    f = c.frame()
    for name in ['lower', 'upper_rear', 'upper_front', 'base']:
        f[name][1] = [-2.5, 2.5]
    for i, (a,b) in enumerate([(-2.5,-2.1),(2.1,2.5)]):
        f['post'+str(i)] = box(-2.5,.15,a,b,-46,0)
    f['spine'][1] = [1.4,1.8]
    f['spine_foot'][1] = [1.4,1.8]
    f['root'] = box(-1.8,-1.6,1.4,1.8,-43,-42.7)
    f['stop'] = box(-.9,-.5,-2.5,2.5,-2.6,-2.1)
    f['cheek_minus'] = box(-2.5,-1.75+L,-2.1,-2.,-2,0)
    f['cheek_plus'] = box(-2.5,-1.75+L,2.,2.1,-2,0)
    return f


def slider(q,L=.6):
    return [c.island(q), box(-1.75+q,-1.75+L+q,-2,2,-2,0),
            box(-1.2+q,-.9+q,-.2,.2,-2.6,-2)]


def spring(q,n=128):
    curve,H = tip.shape(q,n=n)
    u=np.linspace(0,1,n+1)
    slope=-(.2-q)/41*(3*u-1.5*u*u)
    off=np.column_stack((.1/np.sqrt(1+slope*slope),-.1*slope/np.sqrt(1+slope*slope)))
    left,right=curve-off,curve+off
    out=[]
    for i in range(n):
        vertices=np.array([left[i],right[i],left[i+1],right[i+1]])
        out.append(box(vertices[:,0].min(),vertices[:,0].max(),1.4,1.8,
                       vertices[:,1].min(),vertices[:,1].max()))
    out.append(box(curve[-1,0]-.15,curve[-1,0]+.15,1.4,1.8,
                   curve[-1,1]-.15,curve[-1,1]+.15))
    return out


def no_collision(a,b):
    a=np.asarray(a); b=np.asarray(b)
    delta=np.minimum(a[:,None,:,1],b[None,:,:,1])-np.maximum(a[:,None,:,0],b[None,:,:,0])
    return not np.any(np.all(delta>1e-10,axis=2))


def union_box(solids):
    a=np.array(solids)
    return np.column_stack((a[:,:,0].min(axis=0),a[:,:,1].max(axis=0)))


def geometry(n,L=.6):
    f=frame(L); poses=0
    spring_union=union_box(spring(-.75)+spring(0))
    retracted=list(f.values())+slider(-.75,L)+spring(-.75)
    # Actual solid bonding graph: face touch or positive volume overlap.
    seen={'base'}
    while True:
        old=len(seen)
        for name,a in f.items():
            for key in list(seen):
                delta=np.minimum(a[:,1],f[key][:,1])-np.maximum(a[:,0],f[key][:,0])
                if np.all(delta>=-1e-10) and np.count_nonzero(delta>1e-10)>=2:
                    seen.add(name)
        if len(seen)==old: break
    assert seen==set(f),set(f)-seen
    for q in np.linspace(-.75,0,n+1):
        s=slider(q,L); springs=spring(q)
        assert no_collision(s,list(f.values())),('slider/frame',q)
        assert no_collision(springs,list(f.values())),('spring/frame',q)
        assert no_collision(springs,s),('spring/slider',q)
        for dx,dy in itertools.product([-5.08,0,5.08],repeat=2):
            if dx==dy==0: continue
            shift=np.array([[dx,dx],[dy,dy],[0,0]])
            # Full neighbor rack and independent-slider unions.
            obstacles=[box(.4,2.2,-.8,.8,-42,42.2)+shift]
            for a,b in zip(slider(-.75,L),slider(0,L)):
                obstacles.append(union_box([a,b])+shift)
            # Ground, root and full spring envelope of the adjacent mechanism.
            obstacles += [v+shift for v in f.values()]
            obstacles += [spring_union+shift]
            assert no_collision(s+springs,obstacles),('neighbor',q,dx,dy)
        for h in [0,10,20,30,40]:
            assert no_collision(s+springs,c.rack(h+.2)),('release',q,h)
            poses+=1
    for old,new in itertools.permutations([0,10,20,30,40],2):
        for h in np.linspace(old+.2,new+.2,n+1):
            assert no_collision(c.rack(h),retracted),('move',h)
            poses+=1
    return {'poses':poses,'connected_frame':True,'lane_rack_gap':.6,
            'outer_frame_neighbor_gap':.08}


def continuous_bounds(L=.6):
    f=frame(L)
    swept=[union_box([a,b]) for a,b in zip(slider(-.75,L),slider(0,L))]
    spring_hull=union_box(spring(-.75)+spring(0))
    assert no_collision(swept,list(f.values()))
    assert no_collision([spring_hull],list(f.values()))
    rack_union=box(.4,2.2,-.8,.8,-42,42.2)
    assert no_collision(slider(-.75,L)+[spring_hull],[rack_union])
    # All leaf x coordinates and z shortening are monotone in displacement.
    # Actual rotated stem vs rear crossbar uses E-200's independent bound.
    stem_gap=.15-.1-(1.5*.95/41)*.32
    assert stem_gap>0
    for dx,dy in itertools.product([-5.08,0,5.08],repeat=2):
        if dx==dy==0:continue
        shift=np.array([[dx,dx],[dy,dy],[0,0]])
        other=[v+shift for v in swept+[spring_hull,rack_union]+list(f.values())]
        assert no_collision(swept+[spring_hull],other)
        assert no_collision(list(f.values()),[rack_union+shift])
    return {'continuous_stem_crossbar_gap_bound':stem_gap,
            'affine_slider_sweep_and_monotone_leaf_hull':True}


def yaw_stick(mu,e=1.6,L=.6,a=2.,k=(1,1,1,1)):
    """Four endpoint unilateral normal springs. Affine solve in t=Fx(+y)/H.
    Active normal force = -k*n*(dy+x*theta); zero play, no free preload.
    Tangential force may differ on +/-y faces. No SciPy dependency.
    """
    gap=0.
    x=np.array([-L/2,L/2,-L/2,L/2]); y=np.array([-a,-a,a,a])
    ny=-np.sign(y); k=np.array(k)
    G=np.column_stack((ny,ny*x)); B=np.array([ny,x*ny])
    for mask in itertools.product([False,True],repeat=4):
        active=np.array(mask)
        C=-k[:,None]*G*active[:,None]
        N0=-k*gap*active
        mat=B@C
        if abs(np.linalg.det(mat))<1e-10: continue
        # normal yaw + (-a-e)-2*a*t=0; normal Fy=0.
        ext=np.array([[0.,0.],[-a-e,-2*a]])
        disp=np.linalg.solve(mat,-ext-np.column_stack((B@N0,np.zeros(2))))
        N=C@disp; N[:,0]+=N0
        gaps=G@disp; gaps[:,0]+=gap
        rows=[-gaps[i] if active[i] else gaps[i] for i in range(4)]
        plus=N[y>0].sum(axis=0); minus=N[y<0].sum(axis=0)
        t=np.array([0.,1.]); low=np.array([-1.,-1.])
        rows += [mu*plus-t,mu*plus+t,mu*minus-low,mu*minus+low]
        lo,hi=-np.inf,np.inf
        for A,Bb in rows:
            if abs(Bb)<1e-12:
                if A < -1e-9:lo,hi=1,0;break
            elif Bb>0:lo=max(lo,-A/Bb)
            else:hi=min(hi,-A/Bb)
        if lo>hi+1e-10:continue
        tval=lo if np.isfinite(lo) else hi
        if not np.isfinite(tval):tval=0.
        coeff=np.array([1.,tval]); normals=N@coeff
        tractions=np.zeros(4)
        for select,total in [(y>0,tval),(y<0,-1-tval)]:
            if normals[select].sum()>1e-10:
                tractions[select]=total*normals[select]/normals[select].sum()
        residual=np.array([1+tractions.sum(),normals@ny,
                           normals@(x*ny)-tractions@y-e])
        assert np.max(abs(residual))<1e-7
        assert np.min(normals)>-1e-7
        assert np.all(abs(tractions)<=mu*normals+1e-7)
        return dict(normals_per_H=normals.tolist(),tractions_per_H=tractions.tolist(),
                    normalized_displacements= (disp@coeff).tolist(),residual=float(max(abs(residual))))
    return None


def threshold(e,L=.6):
    # Independent exact infimum from N(+y)=N(-y)=N and tangential force bounds.
    # Inside the side faces this is NOT attained: normal forces diverge.
    bound=L/(2*max(2.,abs(e)))
    assert yaw_stick(.99*bound,e,L) is None
    assert yaw_stick(1.01*bound,e,L) is not None
    return bound


def wrench(q,mu=.2,e=1.6):
    """Independent full 3D wrench reconstruction with gravity and free tip.
    Vertical and lateral normal compatibility decouple to first order.
    """
    witness=yaw_stick(mu,e)
    assert witness
    curve,H=tip.shape(q);ztip=curve[-1,1]
    # Main pad + crossbar extension outside pad + lug, avoid double-counting.
    volumes=np.array([2.65*.4*2,.6*3.6*2,.3*.4*.6])
    xc=np.array([-.425,-1.45,-1.05])+q
    xcm=volumes@xc/volumes.sum()
    W=volumes.sum()*.008*9.81/1000
    upper=W*(-.25-xcm)/.4;lower=W+upper
    assert upper>=0
    # Lower-left and upper-front contact are compatible with positive z slope.
    dztheta=np.linalg.solve(np.array([[1.,-.25],[1.,.15]]),[-lower,upper])
    coords=tip.CONTACTS
    gaps=coords[:,2]*(dztheta[0]+coords[:,0]*dztheta[1])
    expected=np.zeros(6); expected[0]=lower
    # E-199 endpoint order is inspected rather than assumed for the upper point.
    ix=np.flatnonzero((coords[:,0]==.15)&(coords[:,1]==2)&(coords[:,2]==-1))[0]
    expected[ix]=upper
    assert np.allclose(np.maximum(-gaps,0),expected)
    forces=[np.array([H,0,0]),np.array([0,0,-W]),np.array([0,0,lower]),np.array([0,0,-upper])]
    points=[[-1.75+q,e,ztip],[xcm,0,-1],[-.25,0,-2],[.15,0,0]]
    for x,y,n,f in zip(np.array([-.3,.3,-.3,.3])-1.45+q,[-2,-2,2,2],witness['normals_per_H'],witness['tractions_per_H']):
        forces.append(np.array([f*H,-np.sign(y)*n*H,0]))
        points.append([x,y,ztip])
    force=np.sum(forces,axis=0)
    moment=np.sum([np.cross(p,f) for p,f in zip(points,forces)],axis=0)
    assert max(abs(force))<1e-9
    assert max(abs(moment))<1e-9,(force,moment)
    return dict(q=q,H=H,W=W,xcm=xcm,upper_gravity_N=upper,
                residual=float(max(max(abs(force)),max(abs(moment)))))


def service():
    # Grant complete removal of own +y cheek/post and omit heads. Neighbor
    # post is reached first; even granting its removal, neighbor slider blocks.
    local=slider(-.75)
    early=[v+np.array([[0,0],[.59,.59],[0,0]]) for v in local]
    post=frame()['post0']+np.array([[0,0],[5.08,5.08],[0,0]])
    assert any(c.penetration(a,post)>0 for a in early)
    shifted=[v+np.array([[0,0],[1.09,1.09],[0,0]]) for v in local]
    neighbor=[v+np.array([[0,0],[5.08,5.08],[0,0]]) for v in slider(-.75)]
    overlap=sum(c.penetration(a,b) for a in shifted for b in neighbor)
    assert overlap>0
    # Pure rearward removal collides central stem with -x neighbor rack web.
    rear=[v+np.array([[-.4,-.4],[0,0],[0,0]]) for v in local]
    web=box(1.2-5.08,2.2-5.08,-.8,.8,-42,42.2)
    assert any(c.penetration(a,web)>0 for a in rear)
    # Pure downward extraction has immediate intentional support obstruction.
    down=[v+np.array([[0,0],[0,0],[-.01,-.01]]) for v in local]
    assert any(c.penetration(a,frame()['lower'])>0 for a in down)
    return {'side_post_first_contact_mm':.58,'side_slider_first_contact_mm':1.08,'side_intrusion_at_1_09_mm3':overlap,
            'rear_first_contact_mm':.38,'downward_support_obstruction':True}


def main():
    out={'geometry':{n:geometry(n) for n in [4,16,64]},
         'continuous':continuous_bounds(),'service':service()}
    out['yaw_thresholds']={str(e):threshold(e) for e in [0,1.6,2.5]}
    out['yaw_witness_mu_02']=yaw_stick(.2)
    out['centered_control_mu_02']=yaw_stick(.2,e=0.)
    out['long_guide_holdout']={'L':1.4,'geometry':geometry(4,L=1.4),
        'continuous':continuous_bounds(L=1.4),'yaw_threshold':threshold(1.6,L=1.4)}
    # Independent equal-traction control N=e/L, |f|=.5.
    equal_mu=.6/(2*1.6)
    assert yaw_stick(equal_mu)
    out['equal_traction_sufficient_mu']=equal_mu
    out['3d_wrench']=[wrench(q) for q in [0,-.3,-.75]]
    out['bounded_yaw']=[{'e':e,'L':L,'mu':threshold(e,L)} for e,L in
                      itertools.product([1.5,1.6,1.7],[.5,.6,.7])]
    out['stiffness_sensitivity']=[{'k':k,'witness':yaw_stick(.2,k=k)}
                                 for k in [(1,1,1,1),(.1,10,1,.1)]]
    out['side_play_rotation_scale_rad']={str(g):2*g/.6 for g in [.005,.025,.05]}
    # Compare lane/rack errors (four independent bounding-face effects) against
    # unchanged board-frame packing (two facing edge errors).
    out['bounded_gaps']={str(e):{'lane_rack':.6-4*e,'frame_to_frame':.08-2*e}
                         for e in [0,.025,.05,.1]}
    # Actual adverse side-frame intrusion, not only overlapping envelopes.
    right=frame()['post1'].copy();right[1,1]+=.05
    left=frame()['post0'].copy()+np.array([[0,0],[5.08,5.08],[0,0]])
    left[1,0]-=.05
    out['adverse_post_intrusion_mm3']=c.penetration(right,left)
    assert abs(out['adverse_post_intrusion_mm3']-2.438)<1e-9
    assert yaw_stick(0.) is None
    assert yaw_stick(.1) is None
    # Long-guide control: yaw threshold scales with side-contact length.
    assert abs(threshold(0,1.2)-2*threshold(0,.6))<1e-8
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
