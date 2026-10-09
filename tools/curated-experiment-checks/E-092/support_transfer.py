"""Finite opposing pocket-dog transfer; mm, N, J. Explicit bounds, no priors.
Separate ground/elevator rack lanes. Quasistatic, frictionless vertical support;
one elastic elevator load path with bounded full-load deflection. No cam credited.
"""
import importlib.util
from pathlib import Path
import itertools as it
import json
from dataclasses import dataclass

spec=importlib.util.spec_from_file_location("trip", Path(__file__).resolve().parents[1]/"E-090/finite_trip.py")
trip=importlib.util.module_from_spec(spec)
spec.loader.exec_module(trip)

EPS = 1e-9
C = .05

@dataclass(frozen=True)
class Cell:
    hg: float
    tg: float
    he: float
    te: float
    datum: float
    deflection: float
    tooth_error: float

    @property
    def cg(self): return self.hg-self.tg
    @property
    def ce(self): return self.he-self.te
    @property
    def gap(self): return self.ce/2+self.datum


def population(h, dmax=.2, r=.2):
    # Feature errors may all share a bank bias or vary locally. Keep correlation
    # between elevator clearance and its center-set acquisition gap explicitly.
    return [Cell(*x) for x in it.product((h-.1,h+.1),(.7,.9),
            (h-.1,h+.1),(.7,.9),(-.2,.2),(0.,dmax),(-r,r))]


def envelope(cells):
    # u: high insertion/unloading coordinate relative to target displacement.
    # v: low ground-seated coordinate at which elevator dog can withdraw.
    return dict(u_lo=max(x.gap+x.tooth_error+x.deflection+C for x in cells),
                u_hi=min(x.gap+x.tooth_error+x.deflection+x.cg-C for x in cells),
                v_lo=max(x.gap+x.tooth_error-x.ce+C for x in cells),
                v_hi=min(x.gap+x.tooth_error-C for x in cells))


def rect(x0,x1,z0,z1): return (x0,x1,z0,z1)

def hit(a,b):
    return min(a[1],b[1])-max(a[0],b[0])>EPS and min(a[3],b[3])-max(a[2],b[2])>EPS


def walls(h, z, errors):
    # Blind pockets open to x<0, 0.8-mm depth, 1.2-mm rack with .4-mm spine.
    # Nine actual pockets, every ceiling separately represented.
    holes=sorted((z-5*k+errors[k]-h,z-5*k+errors[k]) for k in range(9))
    lo,hi=holes[0][0]-1,holes[-1][1]+1
    edges=[lo]+[a for hole in holes for a in hole]+[hi]
    return [rect(0,.8,a,b) for a,b in zip(edges[::2],edges[1::2])]+[rect(.8,1.2,lo,hi)]


def sweep_clear(h,t,ceiling,top,errors):
    # Exact swept union of a horizontal dog from x=[-1.2,-.2] to [-.5,.5].
    # Includes endpoints and all intermediate positions, unlike snapshots.
    swept=rect(-1.2,.5,top-t,top)
    return not any(hit(swept,w) for w in walls(h,ceiling,errors))


def transfer(x,old,target,u,v,steps=8):
    """Ground insertion at high u, continuous load transfer, elevator withdrawal.
    A force ratio resolves support; closing a dog alone is never called proof.
    Interpolate at contact breakpoints as well as a convergence grid.
    """
    delta=5*(target-old)
    errors=[0.]*9
    errors[target]=-x.tooth_error
    # For unchanged transfer the datum must be identical (not independent errors).
    if old==target: errors[target]=0.
    dt=-errors[target]
    z0=5*old
    lift=u-x.gap-x.deflection
    z=z0+delta+lift
    assert sweep_clear(x.hg,x.tg,z,0.,errors), 'ground insertion collision'
    assert lift-dt>=C-EPS, 'ground not unloaded'
    # Elevator lane acquisition tooth uses datum zero independently of ground lane.
    eerrors=[0.]*9
    assert sweep_clear(x.he,x.te,z,delta+u-x.gap-x.deflection,eerrors)
    n=0
    points={v,u,x.gap+dt,x.gap+dt+x.deflection}
    points.update(v+(u-v)*i/steps for i in range(steps+1))
    for a in sorted(p for p in points if v-EPS<=p<=u+EPS):
        # Normalize downward load F to one; exact series spring + hard ground.
        compression=max(0.,min(x.deflection,a-x.gap-dt))
        f= float(a>x.gap+dt) if x.deflection==0 else compression/x.deflection
        rack=z0+delta+max(dt,a-x.gap-x.deflection)
        etop=delta+a-x.gap-compression
        gtop=0.
        assert not any(hit(rect(-.5,.5,gtop-x.tg,gtop),w) for w in walls(x.hg,rack,errors))
        assert not any(hit(rect(-.5,.5,etop-x.te,etop),w) for w in walls(x.he,rack,eerrors))
        # Nonzero load only at contact; ground + elevator equals applied load.
        if f>EPS: assert abs(etop-(rack-5*old))<EPS
        if 1-f>EPS: assert abs(rack-5*target-dt)<EPS
        assert 0<=f<=1 and abs(f+(1-f)-1)<EPS
        n+=1
    final=z0+delta+dt
    assert sweep_clear(x.he,x.te,final,delta+v-x.gap,eerrors), 'grip withdrawal collision'
    assert dt-(v-x.gap)>=C-EPS, 'grip still loaded'
    return n


def check():
    rows=[]
    for h in (1.4,1.8,2.4,3.0):
        cells=population(h); b=envelope(cells)
        # Independent closed form with these bounds, maintaining gap/ce correlation.
        assert abs(b['u_lo']-(h/2+.35))<EPS
        assert abs(b['u_hi']-(1.5*h-1.95))<EPS
        assert abs(b['v_lo']-(-h/2+.95))<EPS
        assert abs(b['v_hi']-(h/2-.95))<EPS
        rows.append(dict(pocket_mm=h,**b,passes=b['u_lo']<=b['u_hi'] and b['v_lo']<=b['v_hi']))
    h=3.; cells=population(h); b=envelope(cells)
    u=(b['u_lo']+b['u_hi'])/2; v=0.
    cases=states=0
    # Acquisition is the same contact path reversed at delta zero, tooth error zero.
    # All distinct pairs include mixed initial levels; common u/v cover every cell.
    for x,old,target in it.product(cells,range(9),range(9)):
        if old==target: continue
        states+=transfer(x,old,target,u,v)
        cases+=1
    acquisitions=0
    for x,old in it.product(cells,range(9)):
        transfer(x,old,old,u,v)
        acquisitions+=1
    # Exact contact events + two grid refinements challenge equilibrium and geometry.
    holdouts=0
    for x in cells[::7]:
        for steps in (1,16,64):
            transfer(x,8,0,u,v,steps); transfer(x,0,8,u,v,steps); holdouts+=2
    # Failure witnesses: dog inserted but not bearing; loaded withdrawal; jamb hit.
    x=cells[0]
    assert x.gap>0 # At e=0 elevator dog is inserted, ground alone supports load.
    assert 0-x.gap<0
    failures=0
    for badu,badv in ((0.,0.),(u,u),(10.,0.)):
        try: transfer(x,8,0,badu,badv)
        except AssertionError: failures+=1
    assert failures==3
    # A dog-depth confirmation at e=0 precedes load contact in every case.
    # Ground release at that instant creates a free drop, not a valid transfer.
    premature_drop=[x.gap+x.deflection for x in cells]
    assert min(premature_drop)>0
    # Directly attaching the H=9 reader to e changes its query by u. Concrete
    # target-miss, neighbor-entry, and engaged-probe reseat collision witnesses.
    miss_dx=u+.65+(40+u)*.01
    wrong_dx=-5+u+.65+(35+u)*.01
    initial_dx=-.65-40*.01
    final_dx=initial_dx-u*.99
    decoder=dict(target_depth=trip.depth_polygon(miss_dx,.5,5.3,42),
                 wrong_depth=trip.depth_polygon(wrong_dx,.3,5.5,42),
                 before_reseat=trip.depth_polygon(initial_dx,.5,5.3,42),
                 after_reseat=trip.depth_polygon(final_dx,.5,5.3,42))
    assert decoder['target_depth']<1.5 and decoder['wrong_depth']==1.5
    assert decoder['before_reseat']==1.5 and decoder['after_reseat']<1.5
    # Sensitivity to common vs differential compliance / tooth datum uncertainty.
    sensitivity=[]
    for dm,r in it.product((0.,.2,.5),(0.,.2,.4)):
        env=envelope(population(3.,dm,r)); sensitivity.append(dict(dmax=dm,tooth_bound=r,
            unload_window=round(env['u_hi']-env['u_lo'],6)))
    # Eight groups/sign for nine levels. Every deposit dips u; positive route must
    # climb back between groups. Both routes include acquisition and empty return.
    paths={}
    for sign in (-1,1):
        p=[0,u]
        for k in range(1,9):p += [sign*5*k+u,sign*5*k+v]
        p += [0]
        paths[str(sign)]=dict(travel_mm=sum(abs(a-b) for a,b in zip(p,p[1:])),path=p)
    return dict(synthesis=rows,chosen=dict(h=h,u=u,v=v),
        deposition_cases=cases,acquisition_cases=acquisitions,contact_states=states,
        refined_holdouts=holdouts,fault_witnesses=failures,sensitivity=sensitivity,
        premature_release_drop_mm=[min(premature_drop),max(premature_drop)],decoder=decoder,
        paths=paths,macro_plus_unload_mm=sum(x['travel_mm'] for x in paths.values()),
        bank_load_N={str(f):800*f for f in (.1,.5,1.)},
        initial_take_up_drive_work_J={str(f):6400*f*u/1000 for f in (.1,.5,1.)})

if __name__=='__main__': print(json.dumps(check(),indent=2))
