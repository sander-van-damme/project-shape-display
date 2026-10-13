#!/usr/bin/env python3
"""Slotted-row elastic bounds and paid module-aligned sensing; no qualification.

mm/N/MPa. Material, force and geometry inputs are competing bounds, not priors.
Euler-Bernoulli center deflection by virtual work; section changes are a beam
approximation, excluding hole-edge stress, cross-section distortion and creep.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('readback', Path(__file__).with_name('readback.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
h = r.head


def aligned(delta, width):
    """One writer/reader window per structural bay; no crossbar in its field."""
    n = len(delta)
    assert n % width == 0
    return [(x0,y,tuple((x,row[x]) for x in range(x0,x0+width) if row[x]))
            for y,row in enumerate(delta)
            for x0 in (range(0,n,width) if y%2==0 else range(n-width,-1,-width))
            if any(row[x0:x0+width])]


def beam(pitch, count, slot, aperture, thickness, modulus, per_site,
         shape='circle', mode='variable', steps_per_cell=400):
    """Symmetric point loads at each cell center; output is center displacement.

    A solid strip is the stiff control. A constant minimum net-width strip is
    the flexible control *within this beam model*. Neither is a hardware bound.
    """
    L=pitch*count; b=pitch-slot
    assert b>aperture and shape in ('circle','square')
    assert thickness>0 and modulus>0 and per_site>=0
    dx=L/(steps_per_cell*count); total=0.; stress=0.
    sites=[(i+.5)*pitch for i in range(count)]
    for k in range(steps_per_cell*count):
        x=(k+.5)*dx
        dist=abs((x % pitch)-pitch/2)
        removed=(2*math.sqrt(max(0.,(aperture/2)**2-dist**2)) if shape=='circle'
                 else aperture if dist<aperture/2 else 0.)
        w={'solid':b,'net':b-aperture,'variable':b-removed}[mode]
        I=w*thickness**3/12
        M=per_site*(count*x/2-sum(max(0,x-a) for a in sites))
        mv=min(x,L-x)/2
        total+=M*mv/(modulus*I)*dx
        stress=max(stress,M*(thickness/2)/I)
    return total,stress


def optical_bay(width=16, thickness=2., crossbar=1., error=.1, stroke=50):
    """E-268 rays plus finite X end ribs and thicker bed (guide stays2mm).

    Camera centered within bay, at global z=-10; thicker thrust plate grows down
    from +1. Target/plate/crossbar X allocation added independently. No full CAD.
    """
    p=6.35; cy=p/2; datum=stroke+9; L=width*p
    min_x=1e9; slot=0.; blocked=0; rays=0; interior_witness=None
    for sy,sz,sc,st,sp,sa in itertools.product((-1,1),repeat=6):
        for j,track,dx,dz in itertools.product(range(width),(-1.2,-.4,.4,1.2),(-.08,.08),(-.08,.08)):
            target=((j+.5)*p+track+dx,2.2+st*error,dz)
            camera=(L/2,cy+sc*error+sp*.25,-datum-10)
            mirror,_=r.old.ray(target,camera,cy+sy*error,sz*error,sa*.5)
            rays+=1
            for z in (-5,-3,-datum+1-thickness,-datum+1):
                t=(z-camera[2])/(mirror[2]-camera[2]); assert 0<t<1
                q=r.old.add(camera,r.old.mul(t,r.old.sub(mirror,camera)))
                slot=max(slot,2*(abs(q[1]-cy)+error))
                margin=min(q[0],L-q[0])-crossbar/2-2*error
                min_x=min(min_x,margin); blocked+=margin<=0
            # A crossbar inside an arbitrary field is not transparent. A rib
            # from thrust bed through guide height at x=L/2 is a concrete witness.
            if interior_witness is None and r.old.hit_box(camera,mirror,
                    (L/2-crossbar/2,0,-datum+1),(L/2+crossbar/2,p,-3)):
                interior_witness={'target':target,'camera':camera,'mirror':mirror}
    return dict(width=width,stroke_mm=stroke,thrust_thickness_mm=thickness,rays=rays,
                required_slot_mm=slot,end_rib_margin_mm=min_x,blocked_samples=blocked,
                interior_crossbar_witness=interior_witness)


def checks():
    # Closed-form symmetric point-load sum at center, independent of quadrature.
    p=6.35; count=16; L=p*count; b=p-.9; t=2.; E=1000.; F=.05
    I=b*t**3/12
    exact=sum(F*min((i+.5)*p,L-(i+.5)*p)*(3*L**2-4*min((i+.5)*p,L-(i+.5)*p)**2)
              /(48*E*I) for i in range(count))
    got,_=beam(p,count,.9,3.6,t,E,F,mode='solid')
    assert math.isclose(got,exact,rel_tol=2e-7)
    assert beam(p,count,.9,3.6,t,E,0)[0] == 0
    anchors=[]
    for shape,a in [('circle',3.6),('square',4.64)]:
        vals=[beam(p,count,.9,a,t,E,F,shape,m)[0] for m in ('solid','variable','net')]
        assert vals[0]<vals[1]<vals[2]
        fine=beam(p,count,.9,a,t,E,F,shape,steps_per_cell=800)[0]
        assert abs(fine-vals[1])/fine<.001
        assert math.isclose(beam(p,count,.9,a,4,E,F,shape)[0]*8,vals[1])
        assert math.isclose(beam(p,count,.9,a,t,E*2,F,shape)[0]*2,vals[1])
        anchors.append({'shape':shape,'deflection_mm':vals,'refined_mm':fine})
    # Replaying aligned jobs must preserve every signed changed cell exactly.
    replay=0
    for n,S in itertools.product((64,80),(40,50)):
        for d in h.local_cases(n,S).values():
            for width in (8,16):
                seen={(x,y):v for x0,y,items in aligned(d,width) for x,v in items}
                assert seen=={(x,y):v for y,row in enumerate(d) for x,v in enumerate(row) if v}
                replay+=1
    # Explicit boundary reveal: two changed cells fit one free window, two bays.
    d=[[0]*32 for _ in range(32)]; d[0][15]=10; d[0][16]=-10
    assert len(h.stations(d,16))==1 and len(aligned(d,16))==2
    assert h.schedule(d,16,station_builder=aligned)['seconds']>h.schedule(d,16)['seconds']
    return dict(beam_anchors=anchors,signed_replays=replay,boundary_witness=True)


def main():
    geometry=[optical_bay(w,t,stroke=S) for S in (40,50)
              for w,t in ((16,2),(16,4),(16,6),(8,2))]
    assert all(g['blocked_samples']==0 and g['interior_crossbar_witness'] for g in geometry)
    rows=[]
    for count,E,t,F in itertools.product((8,16),(1000,3000,200000),(2,4,6),(.02,.05,.2)):
        # .90 nominal slot encompasses .887-mm E-268 optical sample, but is not
        # a qualified manufacturing aperture. See independent error scenarios.
        d,s=beam(6.35,count,.9,3.6,t,E,F)
        rows.append(dict(count=count,E_MPa=E,t_mm=t,F_per_cell_N=F,
                         center_mm=d,nominal_bending_MPa=s,
                         linear_warning=d>count*6.35/20))
    times=[]
    for n,S,w in itertools.product((64,80),(40,50),(8,16)):
        cases=h.local_cases(n,S)
        free={k:h.schedule(d,w,extra_dock=.08)['seconds'] for k,d in cases.items() if any(map(any,d))}
        fixed={k:h.schedule(d,w,extra_dock=.08,station_builder=aligned)['seconds'] for k,d in cases.items() if any(map(any,d))}
        worst=max(fixed,key=fixed.get)
        scenes={k:d for k,d in h.a.workloads(n).items() if S==50 or 'deep:' not in k}
        times.append(dict(n=n,stroke=S,width=w,free_max_s=max(free.values()),aligned_max_s=fixed[worst],
                          aligned_worst=worst,within30=sum(v<=30 for v in fixed.values()),cases=len(fixed),
                          max_individual_penalty_s=max(fixed[k]-free[k] for k in fixed),
                          scene_max_s=max(h.schedule(d,w,extra_dock=.08,station_builder=aligned)['seconds'] for d in scenes.values()),
                          cold_neutral_s=h.schedule(h.a.c.v.s.flat(n,S-20),w,extra_dock=.08,station_builder=aligned)['seconds']))
    print(json.dumps(dict(checks=checks(),optics=geometry,thrust_beams=rows,timing=times,
                         ledger={n:{'row_spans_per_slotted_layer':n*n//16,'two_slotted_layers':2*n*n//16,
                                    'sixteen_square_modules_per_layer':(n//16)**2,
                                    'support_grid_vertices':(n//16+1)**2,
                                    'marked_faces':n*n,'shared_crossrails':n//16+1} for n in (64,80)}),indent=2))

if __name__=='__main__': main()
