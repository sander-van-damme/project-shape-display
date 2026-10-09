#!/usr/bin/env python3
"""Finite stationary split-guide construction. mm; bounded geometry, not hardware."""
import importlib.util
import json
import math
from pathlib import Path
from itertools import product

p = Path(__file__).resolve().parents[1] / 'E-070' / 'guide_packing.py'
spec = importlib.util.spec_from_file_location('guide_packing', p)
gp = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = gp
spec.loader.exec_module(gp)


def extent(parts, axis):
    return min(s.lo[axis] for s in parts), max(s.hi[axis] for s in parts)


def frame(layer, station=4., extra_slot=0.):
    g = gp.geometry('captured_t', .15, .2, .4, 1.6, layer)
    stroke = g['stroke']
    # Five required codes; continuous envelope includes every connecting path.
    heights = (0, 10, 20, 30, 40)
    offsets = sorted({h % int(stroke) for h in heights})
    max_absolute = max(h % int(2*stroke) for h in heights)
    qlo, qhi = -g['failed_drop'], max_absolute + g['unload']
    bore = [s for s in g['moving'] if s.name.startswith('bore_')]
    blo, bhi = extent(bore, 2)
    # Leave running gap beyond worst supported transfer and parked positions.
    bottom_top = blo + qlo - g['gap'] - extra_slot
    top_bottom = bhi + qhi + g['gap'] + extra_slot
    bottom = (bottom_top-station, bottom_top)
    top = (top_bottom, top_bottom+station)
    moving = [s for s in g['moving'] if s.name not in ('neck','flange')]
    neck = next(s for s in g['moving'] if s.name == 'neck')
    low = min(neck.lo[2], bottom[0]-qhi-g['gap'])
    high = top[1]-qlo+g['gap']
    moving += [gp.box('neck', 0, g['spine'], 1.2, 2., low, high),
               gp.box('flange_lower', -g['wing'], g['spine']+g['wing'], 1.6, 2., low, blo),
               gp.box('flange_upper', -g['wing'], g['spine']+g['wing'], 1.6, 2., bhi, high)]
    profiles = [s for s in g['fixed'] if s.name.startswith(('guide_', 'lip_'))]
    fixed = [gp.box(s.name+'_'+name, s.lo[0], s.hi[0], s.lo[1], s.hi[1], *interval)
             for name, interval in [('lower',bottom),('upper',top)] for s in profiles]
    # Finite left jamb connects the stations outside the dog/bore sweep.
    left = next(s for s in profiles if s.name == 'guide_left')
    fixed += [gp.box('slot_jamb',left.lo[0],left.hi[0],left.lo[1],left.hi[1],bottom[0],top[1])]
    # Latch remains attached to its LOWER stage. Move its carrier into the
    # existing forward lane; the old rear-reaching backplate hits the jamb.
    carrier = [s for s in g['fixed'] if s.name.startswith('tongue_') or s.name=='mount_bridge']
    carrier += [gp.box('carrier_front_cheek',g['left'],g['left']+.4,-1.6,-.2,-1.4,.6)]
    g.update(moving=moving, fixed=fixed, carrier=carrier, bore=bore,
             bottom=bottom, top=top, qlo=qlo, qhi=qhi, lower_offsets=offsets,
             max_absolute=max_absolute, station=station)
    return g


def guidance(g, q):
    """Finite station must remain covered by its matching continuous flange."""
    for name, interval in [('lower',g['bottom']),('upper',g['top'])]:
        f = next(s for s in g['moving'] if s.name=='flange_'+name)
        if f.lo[2]+q > interval[0]+1e-9 or f.hi[2]+q < interval[1]-1e-9:
            return False
    return True


def evaluate(layer, station=4., extra_slot=0.):
    g=frame(layer,station,extra_slot)
    hits={}
    def test(name,a,b,lo,hi,e=.15):
        pairs=gp.collisions(a,b,2,lo,hi,e)
        if pairs: hits[name]=pairs
    test('carriage_frame',g['moving'],g['fixed'],g['qlo'],g['qhi'])
    test('fork_frame',g['rail'],g['fixed'],-g['failed_drop'],g['stroke']+g['unload'])
    retract=g['gap']+.4+.15
    dog=g['dog'].sweep(0,-retract)
    test('dog_frame',[dog],g['fixed'],g['qlo'],g['qhi'])
    test('carrier_frame',g['carrier'],g['fixed'],0,max(g['lower_offsets']))
    test('carrier_carriage',g['moving'],g['carrier'],-g['failed_drop'],g['stroke']+g['unload'])
    test('parked_tongue_carriage',g['moving'],[g['tongue'].move(1,-.8)],-g['failed_drop'],g['stroke']+g['unload'])
    test('carrier_fork',g['rail'],g['carrier'],-g['failed_drop']-max(g['lower_offsets']),g['stroke']+g['unload'])
    # Every independently parked carriage/fork pose is separated by x.
    parked=[s.move(2,g['qlo']).sweep(2,g['qhi']-g['qlo']) for s in g['moving']+[g['dog'].move(0,-retract)]]
    test('parked_bypass',g['rail'],parked,-g['failed_drop'],g['stroke']+g['unload'])
    # Envelope accounting contains separate relative-error reserve, not samples.
    all_parts=g['moving']+g['fixed']+g['carrier']+g['rail']+[g['dog'],g['tongue'].move(1,-.8)]
    w=extent(all_parts,0); d=extent(all_parts,1)
    swept=[s.move(2,g['qlo']).sweep(2,g['qhi']-g['qlo']) for s in g['moving']]
    z=extent(swept+g['fixed'],2)
    # Same admissible clearance play as E-070; no tilt or invented tolerance.
    moved=[s.move(0,.19) for s in g['moving']]
    biased=[s.move(0,-.15) for s in g['rail']]
    play_mount=gp.collisions(moved,g['fixed'],2,g['qlo'],g['qhi'])
    play_rail=gp.collisions(moved,biased,2,0,0)
    # Ideal datum bound only: dog housing stays BETWEEN fixed contact stations.
    # Affine lateral error is interpolated rather than extrapolated. Vertical
    # z interval includes errors allocated to overtravel/failed-proof envelope.
    datum_span=g['top'][0]-g['bottom'][1]
    return dict(layer=layer,stroke=g['stroke'],lower_offsets=g['lower_offsets'],
                absolute_motion=[g['qlo'],g['qhi']],slot=[g['bottom'][1],g['top'][0]],
                datum_span=datum_span,guide_station=station,
                moving_length=extent(g['moving'],2)[1]-extent(g['moving'],2)[0],
                swept_height=z[1]-z[0],width_with_error=w[1]-w[0]+.15,
                depth_with_error=d[1]-d[0]+.15,
                connected_carriage=gp.connected(g['moving']),connected_frame=gp.connected(g['fixed']),
                connected_latch_carrier=gp.connected(g['carrier']),
                retained_guidance=all(guidance(g,q) for q in (g['qlo'],g['qhi'])),
                prescribed_path_collisions=hits,free_play_frame_collisions=play_mount,
                free_play_fork_collisions=play_rail,
                minimum_x_with_free_play=g['width']+2*g['gap'])


def section_I(parts, z):
    """Area-union second moment about y; exact rectangular integration."""
    live=[s for s in parts if s.lo[2]<z<s.hi[2]]
    xs=sorted({x for s in live for x in (s.lo[0],s.hi[0])})
    ys=sorted({y for s in live for y in (s.lo[1],s.hi[1])})
    A=S=J=0.
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            if any(s.lo[0]< (x0+x1)/2 <s.hi[0] and s.lo[1]<(y0+y1)/2<s.hi[1] for s in live):
                A+=(x1-x0)*(y1-y0)
                S+=(x1*x1-x0*x0)*(y1-y0)/2
                J+=(x1**3-x0**3)*(y1-y0)/3
    assert A>0
    return J-S*S/A


def integrate(pieces, fn, limit=math.inf):
    # Piecewise integrands are at most cubic; Simpson is exact up to roundoff.
    total=0.
    for lo,hi,I in pieces:
        hi=min(hi,limit)
        if hi>lo:
            total+=(hi-lo)*(fn(lo)+4*fn((lo+hi)/2)+fn(hi))/(6*I)
    return total


def beam_response(pieces, L, a, force, modulus):
    # Fixed-fixed EB beam, unit load at a. M=m+r*x+max(0,x-a).
    # Zero integrated curvature and zero end displacement determine m,r.
    A=integrate(pieces,lambda x:1.)
    B=integrate(pieces,lambda x:x)
    C=integrate(pieces,lambda x:x*x)
    D=integrate(pieces,lambda x:max(0,x-a))
    F=integrate(pieces,lambda x:x*max(0,x-a))
    det=A*C-B*B
    m=(-D*C+B*F)/det
    r=(-A*F+B*D)/det
    M=lambda x:m+r*x+max(0,x-a)
    def y(z):
        return force/modulus*integrate(pieces,lambda x:(z-x)*M(x),z)
    energy=force/modulus*integrate(pieces,lambda x:M(x)**2)
    assert abs(y(L))<1e-8
    assert math.isclose(y(a),energy,rel_tol=1e-8)
    return y


def bending(layer, modulus=4000., force=.2):
    g=frame(layer)
    # Load at bore midpoint when housing is centered in the fixed-frame slot.
    q=(g['qlo']+g['qhi'])/2
    moving=[s.move(2,q) for s in g['moving']]
    lo,hi=g['bottom'][1],g['top'][0]
    a=g['dog_z']+.6+q-lo
    cuts=sorted({lo,hi,lo+a}|{v for s in moving for v in (s.lo[2],s.hi[2]) if lo<v<hi})
    pieces=[(x-lo,y-lo,section_I(moving,(x+y)/2)) for x,y in zip(cuts,cuts[1:])]
    response=beam_response(pieces,hi-lo,a,force,modulus)
    walls={s.name:response((s.lo[2]+s.hi[2])/2-lo) for s in moving if s.name in ('bore_floor','bore_roof')}
    worst=max(walls.values())
    return dict(layer=layer,force_N=force,modulus_MPa=modulus,position=q,
                section_I_min_mm4=min(I for x,y,I in pieces),
                dog_deflection_mm=response(a),bore_wall_deflection_mm=walls,
                error_consumed_bypass_gap_mm=.05,
                force_for_005_mm=force*.05/worst,
                modulus_for_005_mm=modulus*worst/.05)


def checks():
    gp.checks()
    # Independent uniform-beam closed form; off-center load and off-grid length.
    for L,a,I in [(44.25,22.125,.2457),(31.137,9.213,.3)]:
        y=beam_response([(0.,a,I),(a,L,I)],L,a,.2,4000.)
        expected=.2*a**3*(L-a)**3/(3*4000*I*L**3)
        assert math.isclose(y(a),expected,rel_tol=1e-10)
    for i in range(3):
        b=bending(i)
        assert math.isclose(bending(i,2000.)['dog_deflection_mm'],2*b['dog_deflection_mm'])
        assert math.isclose(bending(i,force=.1)['dog_deflection_mm'],b['dog_deflection_mm']/2)
    assert max(bending(2)['bore_wall_deflection_mm'].values())>.05

    for i,L,extra in product(range(3),(1.6,4.,7.137),(0.,.037)):
        r=evaluate(i,L,extra);g=frame(i,L,extra)
        assert not r['prescribed_path_collisions'],r
        assert r['connected_carriage'] and r['connected_frame'] and r['connected_latch_carrier']
        assert r['retained_guidance']
        assert not r['free_play_frame_collisions'] and r['free_play_fork_collisions']
        assert r['width_with_error']<=5.08 and r['depth_with_error']<=5.08
        # Monotone interval endpoint coverage is exact; sample as a cross-check.
        for n in (4,17,64):
            assert all(guidance(g,g['qlo']+(g['qhi']-g['qlo'])*k/n) for k in range(n+1))
        # Removing the slot restores an actual bore/guide collision.
        uncut=[gp.box(s.name,s.lo[0],s.hi[0],s.lo[1],s.hi[1],g['bottom'][0],g['top'][1])
               for s in g['fixed'] if s.name.endswith('_lower')]
        assert gp.collisions(g['moving'],uncut,2,g['qlo'],g['qhi'])
        # Old rear-reaching moving carrier collides with stationary slot jamb.
        old=gp.geometry('captured_t',.15,.2,.4,1.6,i)
        carrier=[s for s in old['fixed'] if s.name=='mount_backplate']
        assert gp.collisions(carrier,g['fixed'],2,0,max(g['lower_offsets']))
        # Independent affine-error bound for ideal datum faces +/-a, correlated
        # with remaining rail registration budget e-a. No probability assigned.
        for a,lo,hi in product((0.,.01,.025,.05,.15),(-1,1),(-1,1)):
            for t in (0.,.137,.5,1.):
                error=a*((1-t)*lo+t*hi)+(.15-a)
                assert abs(error)<=.15+1e-12
        # Independent swept-length identity: carriage span + absolute range.
        assert math.isclose(r['swept_height'],r['moving_length']+g['qhi']-g['qlo'])
    # A common shift cancels; an independent rail shift plus guide play does not.
    g=frame(2)
    for dx in (-.15,.15):
        assert not gp.collisions([s.move(0,dx) for s in g['moving']],
                                 [s.move(0,dx) for s in g['rail']],2,0,0)


def main():
    checks()
    rows=[evaluate(i) for i in range(3)]
    print(json.dumps(dict(evidence='finite prescribed-path geometry and bounded counterexample; no preload or assembled machine',
                          layers=rows,
                          favorable_fixed_end_bending=[bending(i) for i in range(3)],
                          separated_layer_swept_height_sum=sum(r['swept_height'] for r in rows),
                          repeated_guide_stations=6400*3*2,
                          repeated_stage_dogs_and_latches=6400*3),indent=2))

if __name__=='__main__':main()
