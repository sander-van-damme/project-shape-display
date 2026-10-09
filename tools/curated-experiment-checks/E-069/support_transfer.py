#!/usr/bin/env python3
"""E-069: bounded quasistatic contact paths, mm; no strength or sensor model.
Finite extruded latch section, a common rail, and two extreme bank sites.
No random priors. --all retains rejected parameter cases in stdout.
"""
from dataclasses import dataclass
from itertools import product
import json
import math
import sys

EPS = 1e-9
@dataclass(frozen=True)
class Rect:
    y0: float
    y1: float
    z0: float
    z1: float
    def move(self, y=0., z=0.):
        return Rect(self.y0+y, self.y1+y, self.z0+z, self.z1+z)
    def sweep(self, y=0., z=0.):
        assert y == 0 or z == 0
        b = self.move(y,z)
        return Rect(min(self.y0,b.y0),max(self.y1,b.y1),
                    min(self.z0,b.z0),max(self.z1,b.z1))
    def hits(self,b):
        return min(self.y1,b.y1)>max(self.y0,b.y0)+EPS and min(self.z1,b.z1)>max(self.z0,b.z0)+EPS


def pocket(stroke, free):
    # 0.8-mm tongue, two finite 0.8-mm shelves per pocket; 0.8-mm backbone.
    # Local y-z section extruded 0.8 mm in x; placement with dog not qualified.
    shelves=[]
    for offset in (0., -stroke):
        shelves += [Rect(0,1.2,offset,offset+.8),
                    Rect(0,1.2,offset-free-1.6,offset-free-.8)]
    return shelves+[Rect(1.2,2.,-stroke-free-1.6,.8)]


def path(stroke, old_d, new_d, free, mouth, margin=.05, probe=.05,
         failed=None):
    """Exact axis-aligned sweeps plus piecewise contact equations.
    d = dog-bottom elevation when resting on the local endpoint latch.
    Dog always remains deployed until EVERY seat is proven.
    failure model: nominated destination tongue is absent, reader truthful.
    """
    tongue=Rect(-.8,.6,-.8,0)
    parked=tongue.move(y=-.8)  # outer edge -0.2; 0.15 relative fit leaves .05
    solids=pocket(stroke,free)
    reasons=[]
    peak_new=max(new_d)+margin
    proof=min(new_d)-probe
    # old/new are the two endpoint pockets; reverse travel is symmetric.
    for start,end,ds,dt in [(0.,stroke,old_d,new_d),(stroke,0.,new_d,old_d)]:
        for j,(d,t) in enumerate(zip(ds,dt)):
            lift=max(ds)+margin-d
            unload=max(dt)+margin-t
            if lift > free+EPS or unload > free+EPS:
                reasons.append('pocket_overtravel_collision'); continue
            # Finite tongue/shelves during acquisition and lateral release.
            if any(s.move(z=start).sweep(z=lift).hits(tongue) for s in solids):
                reasons.append('acquisition_solid_collision')
            if any(s.move(z=start+lift).hits(tongue.sweep(y=-.8)) for s in solids):
                reasons.append('release_solid_collision')
            # Entire motion at retracted tongue: exact sweep, including endpoints.
            travel=end+unload-start-lift
            if any(s.move(z=start+lift).sweep(z=travel).hits(parked) for s in solids):
                reasons.append('travel_solid_collision')
            if any(s.move(z=end+unload).hits(parked.sweep(y=.8)) for s in solids):
                reasons.append('insertion_solid_collision')
            if any(s.move(z=end).sweep(z=unload).hits(tongue) for s in solids):
                reasons.append('deposition_solid_collision')
    gaps=[d-proof for d in new_d]
    if max(gaps)+margin>mouth+EPS:
        reasons.append('upper_fork_collision_at_proof')
    # Dog withdrawal uses the same Rect primitive with first coordinate x.
    # A 1.2-mm dog retracts 0.8 mm from the fork; finite cheeks/web remain.
    for gap in gaps:
        dog=Rect(-.6,.6,gap,gap+1.2)
        fork=[Rect(0,.85,-.8,0), Rect(0,.85,1.2+mouth,2.+mouth),
              Rect(.85,1.25,-.8,2.+mouth)]
        if any(dog.sweep(y=-.8).hits(s) for s in fork):
            reasons.append('withdrawal_solid_collision')
    # Deposition contact: z_j=max(R,d_j) for a present tongue, z_j=R if absent.
    # At every R each present site rests on tongue OR rail (both at equality).
    # Check all slope breakpoints; between them both equations are affine.
    breakpoints=sorted({proof,peak_new,*new_d})
    support=[]
    for rail in breakpoints:
        for j,d in enumerate(new_d):
            seat_present = j != failed
            z=max(rail,d) if seat_present else rail
            on_rail=abs(z-rail)<EPS
            on_seat=seat_present and abs(z-d)<EPS
            support.append(on_rail or on_seat)
    assert all(support)
    # A truthful displacement proof vetoes withdrawal on any absent tongue.
    withdraw=failed is None and not reasons
    failure_excursion=0 if failed is None else new_d[failed]-proof
    return dict(reasons=sorted(set(reasons)),withdraw=withdraw,
                support_equations_hold=all(support),
                max_fork_gap=max(gaps),failed_site_downward_excursion=failure_excursion)


def checks():
    assert not Rect(0,1,0,1).hits(Rect(0,1,1,2))
    assert Rect(0,1,0,1).sweep(z=3).hits(Rect(0,1,2,3))
    # Finite lower shelf independently detects the analytic unload limit.
    t=Rect(-.8,.6,-.8,0)
    for q in [0,.2,.65,.651]:
        collision=any(s.move(z=q).hits(t) for s in pocket(10,.65))
        assert collision == (q > .65)
    assert path(40,[-.3,.3],[-.3,.3],.75,.85)['reasons']==[]
    assert 'pocket_overtravel_collision' in path(40,[-.3,.3],[-.3,.3],.35,.85)['reasons']
    assert 'upper_fork_collision_at_proof' in path(10,[-.1,.1],[-.1,.1],.75,.25)['reasons']
    # Adverse endpoint reversal and an interior holdout, not only same-seat errors.
    for old,new in [([-.3,.3],[.3,-.3]),([-.217,.071],[.19,-.083])]:
        ok=path(40,old,new,.75,.85)
        assert not ok['reasons'] and ok['withdraw']
        for j in (0,1):
            bad=path(40,old,new,.75,.85,failed=j)
            assert bad['support_equations_hold'] and not bad['withdraw']
    # Free vertical float with a single load-carrying hard stop merely adds L
    # to every engagement height; pair mismatch is invariant.
    for length in [0,.3,.6,1.2]:
        assert math.isclose((.3+length)-(-.3+length),.6)


def main():
    checks()
    rows=[]
    e=.15  # extra internal pocket/mouth erosion bound, NOT a calibrated prior
    for layer,correlation,nominal_u in product(range(3),['coherent','split'],[.3,.5,.7,.9]):
        delta=2*(layer+1)*(.05 if correlation=='coherent' else .10)
        a=.05+(layer+1)*e
        # Retain .05 proof gap and .05 fork clearance, including erosion.
        widened_a=max(a,(delta+.10+e)/2)
        d=[-delta/2,delta/2]
        result=path((10,20,40)[layer],d,list(reversed(d)),nominal_u-e,2*widened_a-e)
        rows.append(dict(layer=layer,correlation=correlation,nominal_u=nominal_u,
                         delta=delta,original_a=a,required_a=widened_a,**result))
    out={'evidence':'finite isolated latch sweeps and quasistatic support equations; not assembled CAD',
         'generated':len(rows),'passed':sum(not r['reasons'] for r in rows),
         'smallest_passing_nominal_u':{},'mouth_half_height_by_layer':[],
         'reader_separation':[]}
    for corr in ['coherent','split']:
        out['smallest_passing_nominal_u'][corr]=[
            min(r['nominal_u'] for r in rows if r['layer']==i and r['correlation']==corr and not r['reasons'])
            for i in range(3)]
    for i in range(3):
        r=next(r for r in rows if r['layer']==i and r['correlation']=='split')
        out['mouth_half_height_by_layer'].append(r['required_a'])
    for probe,r,c in product([.05,.10,.15],[.01,.03,.05],[0.,.02,.05]):
        out['reader_separation'].append(dict(probe=probe,error_bound=r,seat_deflection_bound=c,
                                             distinguishable=probe>2*r+c+EPS))
    out['failed_proof_example']=path(40,[-.3,.3],[.3,-.3],.75,.85,failed=0)
    out['floating_dog']={'single_hard_stop':'same mismatch at load-bearing stop; no positive-support advantage',
                        'independent_lock':'potential escape; adds 19200 load locks and per-site proof, not generated'}
    # This is only the deliberately disjoint orthogonal-lane embedding.
    out['disjoint_lane_embedding']={'dog_y':2.,'latch_swept_y':3.6,
        'separation':.2,'outer_relative_error':e,'required_pitch':2.+3.6+.2+e,
        'fits_5.08':False}
    if '--all' in sys.argv: out['population']=rows
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
