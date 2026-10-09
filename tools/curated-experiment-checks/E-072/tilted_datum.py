#!/usr/bin/env python3
"""E-072: finite rigid pad/carriage geometry; continuous convex sweeps, mm/N.
Deterministic bounded cases, not process probabilities or assembled qualification.
"""
import importlib.util
import json
import math
from itertools import product
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[1] / 'E-071' / 'datum_restraint.py'
spec = importlib.util.spec_from_file_location('datum_e071', p)
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)
gp = dr.gp


def hull(points):
    points = sorted(set(points))
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        out = []
        for p in seq:
            while len(out)>1 and cross(out[-2], out[-1], p)<=0:
                out.pop()
            out.append(p)
        return out
    return half(points)[:-1]+half(points[::-1])[:-1]


def polygon(s):
    return [(s.lo[0],s.lo[2]),(s.hi[0],s.lo[2]),
            (s.hi[0],s.hi[2]),(s.lo[0],s.hi[2])]


def overlap(a, b):
    # Exact separating-axis test on convex x-z polygons, with touching allowed.
    for poly in (a,b):
        for u,v in zip(poly,poly[1:]+poly[:1]):
            nx,nz=-(v[1]-u[1]),v[0]-u[0]
            norm=math.hypot(nx,nz)
            if norm<1e-14: continue
            pa=[(nx*x+nz*z)/norm for x,z in a]
            pb=[(nx*x+nz*z)/norm for x,z in b]
            if min(max(pa),max(pb))<=max(min(pa),min(pb))+1e-9:
                return False
    return True


def pose(g, length, lower, upper):
    # Equal-height finite flat pads. A tilted straight flange touches their
    # lower corners for positive slope, upper corners for negative slope.
    separation=length-.4
    slope=(upper-lower)/separation
    angle=math.atan(slope)
    zl=2. if slope>=0 else 2.4
    return -g['wing'],zl,lower,angle


def transformed(s, datum, travel=0., rail_relative=False):
    xl,zl,dx,theta=datum
    c,ss=math.cos(theta),math.sin(theta)
    # Motion follows the flange axis to retain both datum contacts.
    # Subtract simultaneous VERTICAL rail travel for acquisition/motion sweep.
    return [(xl+dx+c*(x-xl)+ss*(z+travel-zl),
             zl-ss*(x-xl)+c*(z+travel-zl)-(travel if rail_relative else 0.))
            for x,z in polygon(s)]


def sweep_hits(parts, fixed, datum, lo, hi, relative=False):
    hits=[]
    for a,b in product(parts,fixed):
        if min(a.hi[1],b.hi[1])<=max(a.lo[1],b.lo[1])+1e-9: continue
        swept=hull(transformed(a,datum,lo,relative)+transformed(a,datum,hi,relative))
        if overlap(swept,polygon(b)): hits.append([a.name,b.name])
    return hits


def pads(g, length, lower, upper):
    # Pad bases fill guide gap; modify ONLY the finite datum-face location.
    xl=-g['wing']
    return [gp.box('pad_'+str(i),xl-g['gap'],xl+e,1.6,2.,z,z+.4)
            for i,(z,e) in enumerate([(2.,lower),(2.+length-.4,upper)])]


def screen(length, a, error=.15, layer=2, direction=1):
    assert 0<=a<=error
    g=gp.geometry('captured_t',error,.2,.4,length,layer)
    lower,upper=-direction*a,direction*a
    datum=pose(g,length,lower,upper)
    # Keep error accounting bounded: pad face errors consume a of e, rail
    # registration consumes e-a. No additional +/-e expansion is applied.
    rail_bias=-direction*(error-a)
    rail=[s.move(0,rail_bias) for s in g['rail']]
    mount_hits=sweep_hits(g['moving'],g['fixed']+pads(g,length,lower,upper),
                          datum,-g['failed_drop'],g['stroke']+g['unload'])
    rail_hits=sweep_hits(g['moving'],rail,datum,0.,g['stroke'],True)
    endpoint_hits=sweep_hits(g['moving'],rail,datum,g['stroke'],g['stroke'],True)
    # Plane extrapolation bound, independent of SAT. Evaluate right bore-roof
    # corner including exact rotation; rail begins at core+gap+bias.
    roof=next(s for s in g['moving'] if s.name=='bore_roof')
    maxx=max(x for x,z in transformed(roof,datum,g['stroke'],True))
    gap=g['core']+g['gap']+rail_bias-maxx
    return dict(length=length,pad_half_mismatch=a,layer=layer,sign=direction,
                angle_deg=math.degrees(datum[-1]),rail_bias=rail_bias,
                mount_collisions=mount_hits,rail_collisions=rail_hits,
                endpoint_collisions=endpoint_hits,roof_bypass_gap_mm=gap,
                result='collision' if mount_hits or rail_hits else 'no_collision_in_slice')


def threshold(length):
    # Bisection of the exact finite witness roof edge, NOT a probability.
    lo,hi=0.,.15
    for _ in range(50):
        mid=(lo+hi)/2
        if screen(length,mid)['roof_bypass_gap_mm']<0: hi=mid
        else: lo=mid
    return (lo+hi)/2


def leaf_bound(length, modulus=3000., deflection=.6):
    # Two clamped-guided vertical leaves replace the right guide wall.
    # Finite slots separate them from front lip and back wall. Full-width roots
    # anchor both ends; a rigid middle shoe joins the moving leaf tips.
    g=gp.geometry('captured_t',.15,.2,.4,length)
    wall=next(s for s in g['fixed'] if s.name=='guide_right')
    front=next(s for s in g['fixed'] if s.name=='lip_right')
    back=next(s for s in g['fixed'] if s.name=='guide_back')
    y0,y1=front.hi[1]+g['gap'],back.lo[1]-g['gap']
    width=y1-y0
    t=wall.hi[0]-wall.lo[0]
    ell=(length-1.2)/2  # .4-mm roots at both ends and .4-mm middle shoe
    xm=wall.lo[0]; zc=2.+length/2
    leaves=[gp.box('leaf_lower',xm,xm+t,y0,y1,2.4,zc-.2),
            gp.box('leaf_upper',xm,xm+t,y0,y1,zc+.2,2.+length-.4),
            gp.box('shoe',g['spine']+g['wing'],xm+t,y0,y1,zc-.2,zc+.2)]
    roots=[gp.box('root_lower',xm,xm+t,wall.lo[1],wall.hi[1],2.,2.4),
           gp.box('root_upper',xm,xm+t,wall.lo[1],wall.hi[1],2.+length-.4,2.+length)]
    assert gp.connected(leaves+roots)
    others=[s for s in g['fixed'] if s.name!='guide_right']
    assert gp.connected(others+leaves+roots)
    assert not gp.collisions(g['moving'],leaves+roots,2,-g['failed_drop'],g['stroke']+g['unload'])
    assert not gp.collisions(leaves,others,0,0,0)
    # F = 2*(12EI/l^3)*deflection, bending-only clamped-guided beam model.
    # Installed straight skeleton is NOT a verified prestrained configuration.
    # At delta/t=1.5, compare a tensile-stretch benchmark for initially straight
    # beams: +2*.72*E*A*delta^3/l^3. This benchmark is not the packed geometry;
    # rest curvature, assembly prestrain and axial release change its sign/size.
    k=2*modulus*width*t**3/ell**3
    required=dr.screen(length,.6,1.,.2)['minimum_preload_N']
    return dict(length=length,leaf_length=ell,leaf_width=width,leaf_thickness=t,
                modulus_bound_MPa=modulus,deflection_bound=deflection,
                linear_force_N=k*deflection,
                tensile_benchmark_force_N=k*deflection+1.44*modulus*width*t*deflection**3/ell**3,
                required_preload_N=required,
                required_modulus_MPa=modulus*required/(k*deflection),
                required_deflection_mm=required/k,
                linear_result='below_required' if k*deflection<required else 'force_only')


def checks():
    unit=gp.box('unit',0,1,0,1,0,1)
    assert not overlap(polygon(unit),polygon(unit.move(0,1)))
    assert overlap(polygon(unit),polygon(unit.move(0,.999)))
    # Axis-aligned limit independently reproduces original box collision tests.
    for d in [-1.,-.99,0.,.99,1.]:
        b=unit.move(0,d)
        assert overlap(polygon(unit),polygon(b))==unit.hits(b)
    for L in [12.,20.,17.137]:
        g=gp.geometry('captured_t',.15,.2,.4,L)
        assert not screen(L,0.)['rail_collisions']
        for sign in [-1,1]:
            r=screen(L,.025,direction=sign)
            assert not r['mount_collisions'],r
        bad=screen(L,.025)
        assert bad['endpoint_collisions'],bad
        # Every discretized overlap lies in the exact continuous sweep. The
        # converse is deliberately not required: a grid can miss collisions.
        datum=pose(g,L,-.025,.025)
        rail=[s.move(0,-.125) for s in g['rail']]
        exact={tuple(x) for x in sweep_hits(g['moving'],rail,datum,0,40,True)}
        for n in [4,17,64]:
            for i in range(n+1):
                found={tuple(x) for x in sweep_hits(g['moving'],rail,datum,40*i/n,40*i/n,True)}
                assert found<=exact
        # Exact rotation preserves lengths, area and two pad-line contacts.
        xl,zl,dx,theta=datum
        span=L-.4
        assert math.isclose(dx+math.tan(theta)*span,.025,abs_tol=1e-12)
        poly=transformed(unit,datum,23.7)
        assert math.isclose(math.dist(poly[0],poly[1]),1.)
        assert math.isclose(math.dist(poly[1],poly[2]),1.)
        roof=next(s for s in g['moving'] if s.name=='bore_roof')
        excursion=-.025+(math.cos(theta)-1)*(g['core']-xl)+math.sin(theta)*(roof.hi[2]+40-zl)
        assert math.isclose(g['gap']-.125-excursion,bad['roof_bypass_gap_mm'],abs_tol=1e-12)
    # Both coherence limits: equal pad errors imply no tilt; common assembly
    # translation of rail and carriage cancels exactly.
    g=gp.geometry('captured_t',.15,.2,.4,20.)
    for bias in [-.15,.15]:
        datum=pose(g,20.,bias,bias)
        rail=[s.move(0,bias) for s in g['rail']]
        assert not sweep_hits(g['moving'],rail,datum,0.,40.,True)
    # The required .025-mm failure is not confined to a grid-selected L.
    assert screen(17.137,.025)['result']=='collision'
    # Independent strain-energy integral for guided shape f(u)=3u^2-2u^3.
    # Two leaves: U=E I delta^2 integral(f''^2) / ell^3; F=2U/delta.
    for L in [12.,20.]:
        r=leaf_bound(L)
        EI=r['modulus_bound_MPa']*r['leaf_width']*r['leaf_thickness']**3/12
        for n in [10,100]:
            integral=sum((1 if i in [0,n] else 4 if i%2 else 2)*(6-12*i/n)**2
                         for i in range(n+1))/(3*n)
            force=2*EI*.6*integral/r['leaf_length']**3
            assert math.isclose(force,r['linear_force_N'],rel_tol=1e-10)


def main():
    checks()
    rows=[screen(L,a,layer=i,direction=s) for L,a,i,s in
          product([12.,20.],[0.,.01,.025,.05],range(3),[-1,1])]
    out=dict(evidence='bounded finite rotated geometry and finite leaf model comparison',
             cases=len(rows),colliding=sum(r['result']=='collision' for r in rows),
             upper_layer_positive=[r for r in rows if r['layer']==2 and r['sign']==1],
             upper_layer_zero_bypass_gap_thresholds=[dict(length=L,pad_half_mismatch=threshold(L)) for L in [12.,20.]],
             finite_leaf_bounds=[leaf_bound(L) for L in [12.,20.]])
    if '--all' in sys.argv: out['population']=rows
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
