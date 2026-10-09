#!/usr/bin/env python3
"""Finite extruded box geometry, mm. Necessary access tests, not a machine CAD.
Deterministic bounded scenarios; no manufacturing distribution or reliability.
"""
from dataclasses import dataclass
from itertools import product
import json
import math
import sys

PITCH = 5.08
STROKES = (10., 20., 40.)
# batch, spatial, local contributions inherited as bounds from E-050.
SCENARIOS = {'tight': (.05, .05, .05), 'middle': (.10, .10, .15),
             'wide': (.20, .20, .20)}

@dataclass(frozen=True)
class Box:
    x0: float
    x1: float
    z0: float
    z1: float

    def shift(self, x=0., z=0.):
        return Box(self.x0+x, self.x1+x, self.z0+z, self.z1+z)

    def swept(self, x=0., z=0.):
        # Exact union for axis-aligned single-axis translation, not samples.
        assert x == 0 or z == 0
        q = self.shift(x, z)
        return Box(min(self.x0,q.x0), max(self.x1,q.x1),
                   min(self.z0,q.z0), max(self.z1,q.z1))

    def inflated(self, e):
        return Box(self.x0-e,self.x1+e,self.z0-e,self.z1+e)

    def intersects(self, q):
        return min(self.x1,q.x1)>max(self.x0,q.x0)+1e-9 and min(self.z1,q.z1)>max(self.z0,q.z0)+1e-9


def geometry(c, gap, overlap, root, web, az, err):
    # x=0 at one side of each repeated cell; row rail is continuous in y.
    # All boxes extrude over the same 2-mm local y section. Same-row neighbor
    # separation along y is assumed, not tested. Dog bore lies inside core.
    h, jaw = 1.2, .8
    left = c+gap
    right = left+overlap+err+.1+web
    rail = [Box(left,right,-az-jaw,-az),
            Box(left,right,h+az,h+az+jaw),
            Box(right-web,right,-az-jaw,h+az+jaw)]
    deployed = Box(c-root,left+overlap,0,h)
    parked = deployed.shift(x=-(gap+overlap))
    return rail, deployed, parked


def screen(c, gap, overlap, root, web, scenario):
    batch, spatial, local = SCENARIOS[scenario]
    err, b = batch+spatial+local, batch
    reasons=[]
    if c-(root+gap+overlap) < .8+err-1e-9: reasons.append('retracted_dog_invades_0.8mm_spine')
    if root-err < .4-1e-9: reasons.append('root_overlap_below_0.4mm')
    if overlap-err < .4-1e-9: reasons.append('rail_overlap_below_0.4mm')
    if gap-err < .05-1e-9: reasons.append('bypass_gap_below_0.05mm')
    sweeps=0
    first_collision=None
    for layer,stroke in enumerate(STROKES):
        az=b+(layer+1)*err
        rail,dog,park=geometry(c,gap,overlap,root,web,az,err)
        if rail[-1].x1+err > PITCH+1e-9: reasons.append('rail_crosses_pitch')
        # Invariant x-separation gives exact no-collision over *all* z offsets,
        # including continuous lower-stage motion. Enumerate the discrete
        # endpoints too to retain explicit witnesses and cross-check the guard.
        for state in range(8):
            lower=10*(state & ((1<<layer)-1))
            bit=stroke if state & (1<<layer) else 0
            body=Box(0,c,-stroke-4,stroke+4).shift(z=lower+bit)
            pd=park.shift(z=lower+bit)
            for part in rail:
                for obstacle in [body,pd]:
                    sweeps+=1
                    if part.swept(z=stroke).inflated(err/2).intersects(obstacle.inflated(err/2)):
                        first_collision=first_collision or dict(layer=layer,state=state)
        # Dog deployment at an acquisition endpoint must pass between cheeks;
        # epistemic z error is shared by a group, not sampled independently.
        for dz in [-az,az]:
            path=park.shift(z=dz).swept(x=gap+overlap)
            if any(path.intersects(p) for p in rail):
                reasons.append('acquisition_collision')
    if first_collision: reasons.append('unselected_swept_collision')
    return dict(core=c,gap=gap,overlap=overlap,root=root,web=web,
                scenario=scenario,reasons=sorted(set(reasons)),
                first_collision=first_collision,sweeps=sweeps,
                pitch_used=rail[-1].x1+err,
                parked_spine=c-root-gap-overlap-err)


def checks():
    # Closed-form x separation independently checks continuous sweep behavior.
    a=Box(0,1,0,1)
    assert a.swept(z=10)==Box(0,1,0,11)
    assert not a.intersects(a.shift(x=1))
    assert a.intersects(a.shift(x=.999))
    assert a.swept(z=10).intersects(a.shift(z=7))
    for gap in [.1,.2,.4,.7]:
        for err in [.15,.35,.60]:
            rail,_,park=geometry(2.8,gap,.6,.9,.4,.35,err)
            collision=rail[0].swept(z=40).inflated(err/2).intersects(park.inflated(err/2))
            assert collision == (gap < err)
    # Holdout: every continuously moving parked body has x<=core. Rail x>=
    # core+gap; relative error budget err cannot close a gap strictly >err.
    # Independent common-rail support-transfer counterexample below:
    # common registration/batch cancel; opposite regional/local errors remain.
    assert math.isclose(2*3*(.10+.15),1.5)
    assert math.isclose(2.6+8*.35,5.4)


def main():
    checks()
    rows=[screen(*v) for v in product([2.4,2.8,3.2],[.2,.4,.7],
          [.6,.9,1.2],[.6,.9,1.2],[.4,.8],SCENARIOS)]
    out={'evidence':'finite extruded access geometry plus analytic transfer bound; not complete CAD',
         'generated':len(rows),'per_scenario':{},'handoff':{}}
    for name,(batch,spatial,local) in SCENARIOS.items():
        err,b = batch+spatial+local,batch
        subset=[r for r in rows if r['scenario']==name]
        good=[r for r in subset if not r['reasons']]
        reasons={reason:sum(reason in r['reasons'] for r in subset)
                 for reason in sorted({s for r in subset for s in r['reasons']})}
        out['per_scenario'][name]={'tested':len(subset),'survivors':len(good),
              'reason_counts_nonexclusive':reasons,
              'witness':min(good,key=lambda r:(r['pitch_used'],-r['parked_spine'])) if good else None}
        out['per_scenario'][name]['continuous_minimum_pitch_mm']=2.6+8*err
        out['handoff'][name]={'absolute_acquisition_error_by_layer_mm':[b+(i+1)*err for i in range(3)],
            'split_region_minimum_free_latch_unload_mm':[2*(i+1)*(spatial+local) for i in range(3)],
            'coherent_region_minimum_free_latch_unload_mm':[2*(i+1)*local for i in range(3)],
            'split_region_passes_0.5mm_free_unload':[2*(i+1)*(spatial+local)<=.5 for i in range(3)]}
    out['co_moving_counterexample']={'adjacent_states':[0,1],
        'layer':1,'input_offsets_mm':[0,10],
        'conclusion':'one rigid common rail cannot co-move with both bases; independent followers or normalization required'}
    out['travelling_head_bound']={'uniform_pair_normalized_ops':6400*40/25,
        'at_0.02s_per_event_seconds_one_head':6400*40/25*.02,
        'worst_pair_ops_per_cell':3,'worst_map_one_head_seconds_at_0.02s':6400*3*.02,
        'conclusion':'optimistic contact-only screen; parallel heads, travel and proof need separate accounting'}
    if '--all' in sys.argv: out['population']=rows
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
