"""E-212: finite external capture and rack guide counterfactuals; mm, N, MPa.
NumPy only. Deterministic geometry/uncertainty bounds; no material allowables.
Outputs are disposable. A later pose is diagnostic after any first failure.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('rock', Path(__file__).resolve().parents[1]/'E-208/rocking.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def box(x0,x1,y0,y1,z0,z1):
    return (r.R(y0,y1,z0,z1),(x0,x1))


def move(parts,q=(0.,0.,0.),dx=0.):
    return [(r.move(p,q[2])+q[:2],(x[0]+dx,x[1]+dx)) for p,x in parts]


def hits(a,b):
    lo=np.array([[x[0],*p.min(axis=0)] for p,x in a]);hi=np.array([[x[1],*p.max(axis=0)] for p,x in a])
    bl=np.array([[x[0],*p.min(axis=0)] for p,x in b]);bh=np.array([[x[1],*p.max(axis=0)] for p,x in b])
    pairs=np.argwhere(np.all(np.minimum(hi[:,None,:],bh[None,:,:])-np.maximum(lo[:,None,:],bl[None,:,:])>1e-10,axis=2))
    return [(int(i),int(j)) for i,j in pairs if r.p.hit(a[i],b[j])]


def toe(q=(0.,0.,0.)):
    # Fill the obsolete pocket. Retain pad, collar and keys from E-208.
    return move([box(-1.5,1.5,-1,1.6,0,2)]+r.bodies(0)[5:],q)


def cap(q=(0.,0.,0.),error=0.):
    # Integrated external mushroom on left upper wing. No tiny blind pocket.
    neck=box(-1.4,-1.,-.55,-.15,2,2.7)
    flange=box(-1.5-error,-.9+error,-.65-error,-.05+error,2.6-error,3.2+error)
    return move([neck,flange],q)


def cage(q=(0.,0.,0.),gap=.1,opening=0.):
    # Two split U shells; each supplies top/bottom, y end and x side stops.
    # Finite shell is positive lost-motion capture, NOT six driven pads.
    x0,x1=-1.5-gap,-.9+gap; y0,y1=-.65-gap,-.05+gap
    z0,z1=2.6-gap,3.2+gap; t=.4; mid=-1.2
    out=[]
    for lo,hi,sgn in [(x0-t,mid,-1),(mid,x1+t,1)]:
        dx=sgn*opening
        pieces=[box(lo,hi,y0-t,y1+t,z0-t,z0),
                box(lo,hi,y0-t,y1+t,z1,z1+t),
                box(lo,hi,y0-t,y0,z0,z1),box(lo,hi,y1,y1+t,z0,z1)]
        pieces.append(box(x0-t,x0,y0,y1,z0,z1) if sgn<0 else box(x1,x1+t,y0,y1,z0,z1))
        # Split lower plates require a neck slot: remove central y strip
        # only from bottom, leaving front/back rails linked via end walls.
        pieces[0:1]=[box(lo,hi,y0-t,-.55-gap,z0-t,z0),
                     box(lo,hi,-.15+gap,y1+t,z0-t,z0)]
        out += move(pieces,q,dx)
    return out


def wrap():
    # Whole-toe external cage; generous .1-mm clearance, .4-mm walls.
    return [box(-1.9,1.9,-1.4,2.,-.5,-.1),box(-1.9,1.9,-1.4,2.,2.1,2.5),
            box(-1.9,-1.6,-1.4,2.,-.5,2.5),box(1.6,1.9,-1.4,2.,-.5,2.5)]


def rack(h=0.,web=.4):
    parts=r.p.rack(h)
    # Actual moving web extends through the fixed guide over arbitrary travel.
    parts[-1]=box(-web,web,1.7,2.2,-42+h,46+h)
    return parts


def guide(web=.8,gap=.1,levels=(8.,20.)):
    # Two open-front rectangular guide stations, with a connected rear spine.
    # Front pads use widened web shoulders outside the .8-mm-wide teeth.
    out=[]
    for z in levels:
        out += [box(-1.3,1.3,2.2+gap,2.7+gap,z-.5,z+.5),
                box(-1.3,-web-gap,1.2,2.7+gap,z-.5,z+.5),
                box(web+gap,1.3,1.2,2.7+gap,z-.5,z+.5),
                box(-1.3,-.5,1.2,1.7-gap,z-.5,z+.5),
                box(.5,1.3,1.2,1.7-gap,z-.5,z+.5)]
    out += [box(-1.3,1.3,2.7+gap,3.1+gap,min(levels)-.5,max(levels)+.5)]
    return out


def split_guide(opening=0.,dy=0.):
    # Split each crossing beam at x=0; each half keeps its own rear spine.
    out=[]
    for p,(a,b) in guide(gap=.15):
        for lo,hi,sign in [(a,min(b,0.),-1),(max(a,0.),b,1)]:
            if hi>lo:
                out.append((p+[dy,0],(lo+sign*opening,hi+sign*opening)))
    return out


def wrench(points,normals):
    p=np.asarray(points); n=np.asarray(normals)
    return np.vstack((n.T,np.cross(p,n).T))


def positive_span(mat):
    # Opposite planar face corners sum to a strictly positive null vector.
    # With full row rank, adding this null vector gives nonnegative reactions
    # for every finite target in the row space. No arbitrary force capacity.
    assert np.linalg.norm(mat@np.ones(mat.shape[1]))<1e-10
    residual=0.; peak=0.
    for demand in np.vstack((np.eye(mat.shape[0]),-np.eye(mat.shape[0]))):
        f=np.linalg.pinv(mat)@demand
        f-=min(0.,float(f.min()))
        residual=max(residual,float(np.linalg.norm(mat@f-demand)))
        peak=max(peak,float(f.max()))
    return dict(rank=int(np.linalg.matrix_rank(mat)),unit_residual=residual,unit_peak=peak)


def restraint():
    # Six actively contacting rectangular cap faces, each with four corners.
    # This is the hypothetical independently closed pad repair, not loose cage.
    points=[]; normals=[]
    for axis in range(3):
        other=[a for a in range(3) if a!=axis]
        for side,a,b in itertools.product((-1,1),repeat=3):
            p=np.zeros(3);p[axis]=side*.3;p[other]=[a*.25,b*.25]
            n=np.zeros(3);n[axis]=-side
            points.append(p);normals.append(n)
    full=wrench(points,normals)
    # Guide shoulder and side contacts at both elevations; no z friction.
    gp=[];gn=[]
    for z in (-6.,6.):
        for y in (1.7,2.2):
            for x in (-.8,.8):
                gp.append([x,y,z]);gn.append([-np.sign(x),0,0])
        for x in (-.65,.65):
            for y,sign in [(1.7,1),(2.2,-1)]:
                gp.append([x,y,z]);gn.append([0,sign,0])
    g=wrench(gp,gn)
    # Guide handles Fx,Fy,Mx,My,Mz; height finger supplies Fz.
    reduced=np.delete(g,2,axis=0)
    assert np.max(abs(g[2]))==0
    return dict(cap_contacting=positive_span(full),guide_contacting=positive_span(reduced),
                loose_cap_initial_rank=0,loose_guide_initial_rank=0,
                clevis_without_antirotation_rank=5)


def finite(steps=32):
    frame=r.fixed(.2,0,.2)
    first={};counts={}
    def test(label,a,b,pose):
        pairs=hits(a,b)
        if pairs:
            counts[label]=counts.get(label,0)+1
            first.setdefault(label,dict(pose=pose,pair=pairs[0]))
    test('whole_toe_wrap',wrap(),frame,0)
    # Supported acquisition at nominal seated pose; cap is integrated.
    for i,f in enumerate(np.linspace(1,0,steps+1)):
        h=cage(opening=.8*f)
        test('cap_acquire',h,toe()+cap()+frame+rack(),i)
        for dx in (-5.03,5.03):
            test('cap_acquire_neighbor',h,move(toe()+cap()+frame+rack(),dx=dx),i)
        test('jaw_acquire',r.p.writer(dx=2*f),toe()+cap()+cage()+frame+rack(),i)
        test('rack_unload',rack(1.5*f)+r.p.writer(1.5*f),toe()+cap()+cage()+frame,i)
    poses=[(0.,0.,a) for a in np.linspace(0,.22,steps+1)]
    poses += [(-w,0.,.22) for w in np.linspace(0,1.2,steps+1)[1:]]
    poses += poses[-2::-1]
    for i,q in enumerate(poses):
        moving=toe(q)+cap(q)+cage(q)
        test('cap_path',moving,frame+rack(1.5)+r.p.writer(1.5),i)
        test('cage_self',cage(q),toe(q)+cap(q),i)
        for dx,dy in [(0,-5.03),(0,5.03),(-5.03,0),(5.03,0)]:
            neighbor=move(toe()+cap()+frame+rack(),(dy,0,0),dx)
            test('neighbor',moving,neighbor,i)
    # Twenty transitions; convex vertical sweep of each rack prism is exact.
    q=(-1.2,0.,.22)
    for dx,dy,da in itertools.product((-.05,.05),(-.05,.05),(-.02,.02)):
        test('open_pose_error_neighbor',move(cage((-1.2+dy,0.,.22+da)),dx=dx),
             move(rack(),(-5.03,0,0)),[dx,dy,da])
    # Flange-size corners: actual cavity clearance must stay positive.
    for err in (-.05,.05):
        assert hits(cap(error=err)[:1],cap(error=err)[1:]),'disconnected cap neck'
        test('cap_size_corner',cage(),cap(error=err),err)
    for a,b in itertools.permutations(range(0,41,10),2):
        swept=[]
        for p,x in rack(1.5):
            swept.append((r.R(p[:,0].min(),p[:,0].max(),p[:,1].min()+min(a,b),p[:,1].max()+max(a,b)),x))
        test('open_40mm',toe(q)+cap(q)+cage(q),swept,[a,b])
    # Guide moving-web corners include coherent root/guide offsets; no iid yield.
    guide_fail=0;guide_checks=0
    sweep_fail=0
    for dx,dy,err in itertools.product((-.05,.05),repeat=3):
        g=guide(web=.8,gap=.15)
        for h in np.linspace(0,40,steps+1):
            rr=move(rack(h,web=.8+err),(dy,0,0),dx)
            guide_checks+=1
            if hits(g,rr):guide_fail+=1
        swept=[(r.R(p[:,0].min(),p[:,0].max(),p[:,1].min(),p[:,1].max()+40),x)
               for p,x in move(rack(web=.8+err),(dy,0,0),dx)]
        sweep_fail+=bool(hits(g,swept))
    # A closed front guide for the original narrow web blocks tooth passage.
    closed_front=[box(-.4,.4,1.2,1.6,7.5,8.5)]
    test('narrow_web_front_guide',closed_front,rack(4),0)
    # Open front guide can enter from +y around rack; front shoulder pads
    # cannot slide through web: must open laterally before insertion.
    for i,dy in enumerate(np.linspace(2,0,steps+1)):
        test('rigid_guide_acquire',move(guide(),(dy,0,0)),rack(web=.8),i)
        test('split_guide_insert',split_guide(.9,dy),rack(web=.8),i)
        for x,y in [(0,-5.03),(0,5.03),(-5.03,0),(5.03,0)]:
            test('split_guide_neighbor',split_guide(.9,dy),move(rack(web=.8)+toe()+cap()+frame,(y,0,0),x),i)
    for i,op in enumerate(np.linspace(.9,0,steps+1)):
        test('split_guide_close',split_guide(op),rack(web=.8),i)
    # Existing jaw is a real moving body, not just its contact force.
    for i,h in enumerate(np.linspace(0,41.5,steps*4+1)):
        test('guide_vs_height_jaw',guide(gap=.15),r.p.writer(h),dict(index=i,lift=float(h)))
    assert set(first)=={'whole_toe_wrap','open_pose_error_neighbor','narrow_web_front_guide',
                        'rigid_guide_acquire','guide_vs_height_jaw'},first
    assert counts['open_pose_error_neighbor']==4 and guide_fail==sweep_fail==0
    return dict(steps=steps,first=first,collision_pose_counts=counts,
                widened_guide_collision_checks=guide_checks,widened_guide_collision_cases=guide_fail,
                widened_guide_exact_40mm_sweep_failures=sweep_fail)


def bounds():
    out=[]
    for H,slot in [(40,.15),(80,.30),(160,.60)]:
        # Map overhead includes traverse/index; head actions must fit slot.
        # Rest-to-rest 40mm triangular move: t=2 sqrt(d/a), no velocity cap.
        row=dict(H=H,strict_slot_s=slot,budget_per_head=250/H,
                 original_pocket_slides=4*H,cap_pad_slides=6*H,
                 rack_guide_pad_slides=8*H,height_and_takeover_axes=2*H,
                 head_pitch_one_row_mm=406.4/H,
                 longitudinal_zones_for_5_08_pitch=int(np.ceil(H/80)))
        row['timing_scenarios']=[]
        for a,t_aux in itertools.product((1000.,5000.,20000.),(.08,.16,.32)):
            t_move=2*np.sqrt(40/a)
            row['timing_scenarios'].append(dict(a_mm_s2=a,acquire_release_proof_s=t_aux,
                       cycle_s=float(t_move+t_aux),necessary_slot_pass=bool(t_move+t_aux<slot)))
        out.append(row)
    # Neck .4 square; favorable 0.6-mm arm to nominal lower flange edge.
    # Centroid loading at z=2.9 would have a 0.9-mm arm. Larger .8 is unbuilt.
    neck=[dict(F=F,width=b,stress=6*F*.6/b**3) for F,b in itertools.product((.514,7.56,14.8),(.4,.8))]
    # Moment from 10N load y=.8 to jaw y=1.5. Side guide force pair at 12mm.
    M=10*(1.5-.8)
    return dict(heads=out,cap_neck_bending_MPa=neck,guide_reaction_pair_N=M/12,
                passive_guide_pitch_slack_rad=.3/12,
                rack_40mm_tip_slack_mm=40*.3/12,
                resident_counts=dict(toes=6400,returns=6400,keys=12800,cap_necks=6400,widened_webs=6400))


def verify():
    a=box(0,1,0,1,0,1)
    assert not hits([a],[box(1,2,0,1,0,1)])
    assert hits([a],[box(.99,2,0,1,0,1)])
    rr=restraint()
    assert rr['cap_contacting']['rank']==6 and rr['cap_contacting']['unit_residual']<1e-10
    assert rr['guide_contacting']['rank']==5 and rr['guide_contacting']['unit_residual']<1e-10
    # Scalar moment balance independent of contact basis implementation.
    W=10.; lo=40.; up=30.
    assert abs(lo-up-W)<1e-12 and abs(lo*1.4-up*1.6-W*.8)<1e-12
    assert abs(12*bounds()['guide_reaction_pair_N']-7)<1e-12
    # Independent first-station affine vertical overlap boundary h=7.5-6.4.
    assert not hits(guide(gap=.15),r.p.writer(1.099))
    assert hits(guide(gap=.15),r.p.writer(1.101))
    return rr


if __name__=='__main__':
    print(json.dumps(dict(restraint=verify(),finite=[finite(n) for n in (16,32,64)],bounds=bounds()),indent=2))
