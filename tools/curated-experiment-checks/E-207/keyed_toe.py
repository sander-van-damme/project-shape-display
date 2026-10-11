"""E-207 finite monolithic toe/comb: mm, N, MPa; bounded scenarios, no yield.
Python + NumPy. Imports E-166's checked elastica and convex contact predicates.
The first interference stops the physical sequence; later poses are controls.
"""
import importlib.util
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('hook', Path(__file__).resolve().parents[1]/'E-166/probe.py')
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)
R = hook.rectangle


def prism(poly, x):
    return (np.asarray(poly), x)


def hit(a, b):
    if min(a[1][1], b[1][1])-max(a[1][0], b[1][0]) <= 1e-10:
        return False
    if np.any(np.minimum(a[0].max(axis=0),b[0].max(axis=0))-np.maximum(a[0].min(axis=0),b[0].min(axis=0)) <= 1e-10):
        return False
    return hook.overlap(a[0], b[0])


def transform(p, a, L):
    th = -a['tip_angle']
    c, s = math.cos(th), math.sin(th)
    pivot = np.array([-.6, -.2])
    return (p-pivot) @ np.array([[c,s],[-s,c]]) + pivot + [a['y'],a['z']-L]


def toe(a, L=12., depth=.2, thickness=.4, keys=True):
    # Single connected printed body: thick toe, inset rack pad, tapered collar,
    # and shared bending sheet. Collar face and leaf end share full finite area.
    parts = [(R(-1.,1.6,0.,2.),(-1.5,1.5)),
             (R(.8,1.2,2.,3.4),(-.4,.4)),
             (np.array([[-.6-thickness/2,-.2],[-.6+thickness/2,-.2],[-.2,.4],[-1.,.4]]),(-.4,.4))]
    if keys:
        parts += [(R(.85,1.15,-depth,0.), x) for x in [(-1.5,-.85),(.85,1.5)]]
    return [prism(transform(p,a,L),x) for p,x in parts]


def frame(gap=.1, shift=0., depth=.2):
    parts=[]
    # Paired side ledges; socket ends are positive horizontal key stops.
    # Rear wall and bottom beam ground both ledges without entering rack sweep.
    for x in [(-1.7,-.85),(.85,1.7)]:
        for p in [R(.4,.85-gap+shift,-.8,0.),R(1.15+gap+shift,1.7,-.8,0.),
                  R(.85-gap+shift,1.15+gap+shift,-.8,-depth-.15),
                  R(-1.5,1.7,-1.6,-.8), R(-1.5,-1.1,-13.,-.8)]:
            parts.append(prism(p,x))
    parts.append(prism(R(-1.5,-1.1,-13.,-12.2),(-1.7,1.7)))
    # Root ledge connects the leaf to the same rear frame.
    parts.append(prism(R(-1.5,-.3,-13.,-12.2),(-.4,.4)))
    return parts


def leaf(a,L=12.,t=.4):
    # Reconstruct centerline independently of endpoint integral in the solver.
    th=np.r_[0.,a['theta']]; ds=L/(len(th)-1)
    y=-.6+np.r_[0.,np.cumsum(ds*.5*(np.sin(th[:-1])+np.sin(th[1:])))]
    z=-L-.2+np.r_[0.,np.cumsum(ds*.5*(np.cos(th[:-1])+np.cos(th[1:])))]
    p=np.c_[y,z]; normal=np.c_[np.cos(th),-np.sin(th)]
    left,right=p-t/2*normal,p+t/2*normal
    assert np.linalg.norm(p[-1]-[-.6+a['y'],-.2+a['z']-L])<1e-10
    return [prism(np.array([left[i],right[i],right[i+1],left[i+1]]),(-.4,.4)) for i in range(len(th)-1)]


@lru_cache(maxsize=None)
def state(q,n=64,L=12.):
    # q = |H| L²/EI; geometry independent of E and thickness in this model.
    a=hook.equilibrium(1.,L,H=-q/L**2,n=n)
    assert a is not None
    return a


def writer(lift=0.,dx=0.):
    # C jaws enter from +x. Lower finger lies in the 1.4-mm pad-height recess.
    # Final jaw gap is prescribed 2 mm: a real closing actuator/fit is still owed.
    return [prism(R(1.35,1.65,2.4+lift,3.4+lift),(-.35+dx,.8+dx)),
            prism(R(1.35,1.65,5.4+lift,6.4+lift),(-.35+dx,.8+dx)),
            prism(R(1.35,1.65,2.4+lift,6.4+lift),(.55+dx,.8+dx))]


def rack(lift=0.):
    return [prism(R(.6,1.7,3.4+lift+10*j,5.4+lift+10*j),(-.4,.4)) for j in range(-4,5)] + [prism(R(1.7,2.2,-42,46),(-.4,.4))]


def contacts():
    # Four contact points inside actual ledge/toe overlap, enclosing inset pad.
    # Load-sharing weights establish compressive reaction existence, not pressure.
    max_res=0.
    for W,x,y in itertools.product((.1,1.,10.),(-.4,.4),(.8,1.2)):
        fx=(x+1.1)/2.2; fy=(y-.5)/.95
        forces=[W*(1-fx)*(1-fy),W*fx*(1-fy),W*(1-fx)*fy,W*fx*fy]
        points=[(-1.1,.5),(1.1,.5),(-1.1,1.45),(1.1,1.45)]
        assert min(forces)>0
        max_res=max(max_res,abs(sum(forces)-W),abs(sum(f*p[0] for f,p in zip(forces,points))-W*x),abs(sum(f*p[1] for f,p in zip(forces,points))-W*y))
    head=[]
    for W,y in itertools.product((1.,10.),(.8,1.2)):
        upper=W*(1.4-y)/.2; lower=W+upper
        assert lower>0 and upper>0
        assert abs(lower*1.4-upper*1.6-W*y)<1e-12
        head.append({'W':W,'load_y':y,'lower':lower,'upper':upper})
    return {'force_moment_residual':max_res,'cases':12,'nominal_pad_margins_xy':[.7,.25], 'head_reactions':head}


def path(n=64,steps=64,gap=.1,shift=0.,depth=.2,L=12.,full=True):
    fixed=frame(gap,shift,depth)
    # Each dimensional corner uses its own correctly connected root elevation.
    fixed[-1]=prism(R(-1.5,-.3,-L-1.,-L-.2),(-.4,.4))
    first=None; unkeyed_hits=0; sample=None
    for i in range(steps+1):
        q=.34*i/steps; a=state(q,n,L)
        bodies=toe(a,L,depth)
        collision=any(hit(p,f) for p in bodies for f in fixed)
        if collision and first is None:
            first={'q':q,'withdrawal':-a['y'],'angle_deg':-math.degrees(a['tip_angle'])}
            sample=min(float(p[0][:,1].min()) for p in bodies[-2:])
        # Counterfactual control without keys: can it clear the ledges and rack?
        free=toe(a,L,depth,keys=False)
        unkeyed_hits += any(hit(p,f) for p in free for f in fixed)
        if not full:
            continue
        assert not any(hit(p,r) for p in free for r in rack(.8))
        assert not any(hit(p,w) for p in free for w in writer(.8))
        # All leaf sections clear frame except the intended touching root.
        assert not any(hit(p,f) for p in leaf(a,L) for f in fixed)
    open_body=toe(a,L,depth,keys=False)
    # Projection disjointness with full rack z envelope covers all 20 transitions.
    open_gap=.6-max(float(p[0][:,0].max()) for p in open_body)
    assert open_gap>0
    assert first is not None and unkeyed_hits==0, (first,unkeyed_hits)
    return {'n':n,'steps':steps,'first_collision':first,'key_bottom_at_collision':sample,'keyless_collision_poses':unkeyed_hits,'keyless_open_gap':open_gap}


def main():
    hook.verify()
    a=state(0.)
    # Actual joint face continuity at rest and after bending, no loose insert.
    for q in (0.,.1,.34):
        b=state(q); sheet=leaf(b)[-1][0]; collar=toe(b)[2][0]
        assert np.max(abs(sheet[[3,2]]-collar[[0,1]]))<1e-10
    assert not any(hit(p,f) for p in toe(a) for f in frame())
    # Nominal supported takeover until the decisive release obstruction.
    for dx in np.linspace(2.,0.,33):
        assert not any(hit(w,p) for w in writer(dx=dx) for p in toe(a)+frame()+rack())
    for lift in np.linspace(0.,.8,33):
        assert not any(hit(w,p) for w in writer(lift) for p in toe(a)+frame()+rack(lift))
        assert not any(hit(r,p) for r in rack(lift) for p in toe(a)+frame())
    convergence=[path(n,s) for n,s in [(32,32),(64,64),(128,128)]]
    # L, socket size, relative print/registration bias, key-depth errors are bank
    # coherent. No independent-cell distribution or calibrated process prior.
    corners=[path(64,64,g,s,d,L,full=False) for L,g,s,d in itertools.product((11.5,12.5),(.07,.13),(-.05,.05),(.15,.25))]
    # Independent local small-angle holdout for first release: slope at key
    # rear edge is 3*(.85+.6)/(2L), versus finite key depth before wall crossing.
    slopes=[3*1.45/(2*L) for L in (11.5,12.5)]
    # Toe transverse beam check, deliberately assumed effective strip breadth.
    toe_stress=[{'W':W,'breadth':b,'stress_MPa':3*W*2.2/(2*b*2.**2)} for W,b in itertools.product((1.,10.),(.4,1.))]
    # Inextensible geometries are not force qualification of printed PLA.
    force=[]
    b=state(.34,128)
    for E,t,L in itertools.product((700.,2200.),(.35,.45),(11.5,12.5)):
        EI=E*.8*t**3/12
        force.append(.34*EI/L**2)
    out={'evidence':'finite rigid prisms + inextensible elastica; self-review only',
         'contacts':contacts(),'convergence':convergence,'coherent_corners':len(corners),
         'blocked_corners':sum(c['first_collision'] is not None for c in corners),
         'first_collision_withdrawal_range':[min(c['first_collision']['withdrawal'] for c in corners),max(c['first_collision']['withdrawal'] for c in corners)],
         'collision_key_bottom_range':[min(c['key_bottom_at_collision'] for c in corners),max(c['key_bottom_at_collision'] for c in corners)],
         'linear_key_rise_per_withdrawal':slopes,'toe_stress_scenarios':toe_stress,
         'unblocked_counterfactual_force_range_N':[min(force),max(force)],
         'counterfactual_peak_outer_strain':.4/2*max(abs(np.diff(np.r_[0.,b['theta']])))/(12/128),
         'counts':{'comb_placements':160,'toes':6400,'flexure_necks':6400,'keys':12800,'sockets':12800,'separate_joints_pins_bearings':0},
         'disposition':'stop keyed monolithic construction; keyless control is not positive retention'}
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
