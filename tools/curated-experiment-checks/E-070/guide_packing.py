#!/usr/bin/env python3
"""E-070: constructive 3-D box packing, exact one-axis sweeps, units mm.
Single guided stage, not a stacked machine; deterministic epistemic bounds.
"""
from dataclasses import dataclass
from itertools import product
from collections import Counter
import json
import math
import sys

EPS = 1e-9
PITCH = 5.08

@dataclass(frozen=True)
class Solid:
    name: str
    lo: tuple
    hi: tuple

    def move(self, axis, distance):
        lo, hi = list(self.lo), list(self.hi)
        lo[axis] += distance
        hi[axis] += distance
        return Solid(self.name, tuple(lo), tuple(hi))

    def sweep(self, axis, distance):
        b = self.move(axis, distance)
        return Solid(self.name, tuple(min(a, c) for a, c in zip(self.lo, b.lo)),
                     tuple(max(a, c) for a, c in zip(self.hi, b.hi)))

    def inflate(self, e):
        return Solid(self.name, tuple(x-e for x in self.lo), tuple(x+e for x in self.hi))

    def hits(self, other):
        return all(min(b, d) > max(a, c)+EPS for a,b,c,d in
                   zip(self.lo, self.hi, other.lo, other.hi))

    def connected(self, other):
        lengths = [min(b,d)-max(a,c) for a,b,c,d in zip(self.lo,self.hi,other.lo,other.hi)]
        # Volume overlap or finite face contact; edge/point contact is not a join.
        return min(lengths) >= -EPS and sum(x > EPS for x in lengths) >= 2


def box(name, x0, x1, y0, y1, z0, z1):
    assert x1 > x0 and y1 > y0 and z1 > z0, (name, x0,x1,y0,y1,z0,z1)
    return Solid(name, (x0,y0,z0), (x1,y1,z1))


def connected(parts):
    reached = {0}
    while True:
        more = {j for j,b in enumerate(parts) if any(parts[i].connected(b) for i in reached)}
        if more <= reached:
            return len(reached) == len(parts)
        reached |= more


def geometry(profile, e, bearing, wall, length, layer=2, extra=.0):
    """Construct the minimum dog core and guide under named design allocations.
    Positive extra enlarges ONLY the backstop running gap, an off-grid holdout.
    e is total relative fit erosion, never an iid per-solid draw.
    """
    stroke = (10.,20.,40.)[layer]
    spine, margin, tip, dog_h, dog_y = .8, .05, .1, 1.2, 2.
    gap = margin+e
    root = overlap = .4+e
    core = spine+root+gap+overlap+e+margin+extra
    right = core+gap+overlap+e+tip+wall
    wing = bearing+gap+e if profile == 'captured_t' else 0.
    left = -wing-gap-wall
    guide_right = spine+wing+gap+wall
    # Keep E-069 tight split-region contact/failed-proof bounds. Wider-error
    # cases below are packaging counterfactuals only, not contact survivors.
    delta = .2*(layer+1)
    failed_drop = delta+.05
    unload = delta+.05+.15
    guide_z = (2.,2.+length)
    dog_z = guide_z[1]+gap+wall+failed_drop+gap
    dog_y0 = gap+wall
    rear = dog_y0+dog_y+gap+wall
    z0, z1 = -stroke-unload-1.6, dog_z+dog_h+gap+wall
    moving = [box('neck',0,spine,1.2,2.,z0,z1)]
    if wing:
        # Relieve the flange above the guide; an untrimmed flange blocks the dog bore.
        moving.append(box('flange',-wing,spine+wing,1.6,2.,z0,dog_z-gap-wall))
    for k in (0.,-stroke):
        moving += [box('seat_upper',0,spine,0,1.2,k,k+.8),
                   box('seat_lower',0,spine,0,1.2,k-unload-1.6,k-unload-.8)]
    # Finite dog bore: floor, roof, two sides and blind backstop, open at x=core.
    moving += [box('bore_floor',0,core,0,rear,dog_z-gap-wall,dog_z-gap),
               box('bore_roof',0,core,0,rear,dog_z+dog_h+gap,dog_z+dog_h+gap+wall),
               box('bore_front',0,core,0,wall,dog_z-gap,dog_z+dog_h+gap),
               box('bore_back',0,core,rear-wall,rear,dog_z-gap,dog_z+dog_h+gap),
               box('bore_stop',0,spine,0,rear,dog_z-gap,dog_z+dog_h+gap)]
    front = (1.6 if wing else 1.2)-gap-wall
    fixed = [box('guide_left',left,left+wall,front,2.+gap+wall,*guide_z),
             box('guide_right',guide_right-wall,guide_right,front,2.+gap+wall,*guide_z),
             box('guide_back',left,guide_right,2.+gap,2.+gap+wall,*guide_z)]
    if profile == 'sleeve':
        fixed.append(box('guide_front',left,guide_right,front,front+wall,*guide_z))
    elif profile == 'captured_t':
        fixed += [box('lip_left',left,-gap,front,front+wall,*guide_z),
                  box('lip_right',spine+gap,guide_right,front,front+wall,*guide_z)]
    # Tongue guide is open at both y ends; actuators/stroke stops not invented.
    fixed += [box('tongue_left',-gap-wall,-gap,-1.6,-.2,-.8-gap-wall,gap+wall),
              box('tongue_right',spine+gap,spine+gap+wall,-1.6,-.2,-.8-gap-wall,gap+wall),
              box('tongue_floor',-gap-wall,spine+gap+wall,-1.6,-.2,-.8-gap-wall,-.8-gap),
              box('tongue_roof',-gap-wall,spine+gap+wall,-1.6,-.2,gap,gap+wall),
              box('mount_backplate',left,left+wall,-1.6,2.+gap+wall,-.8-gap-wall,guide_z[1]),
              box('mount_bridge',left,spine+gap+wall,-1.6,-.2,-.8-gap-wall,-.8-gap)]
    tongue = box('tongue',0,spine,-.8,.6,-.8,0)
    dog = box('dog',core-root,core+gap+overlap,dog_y0,dog_y0+dog_y,dog_z,dog_z+dog_h)
    a = (.225,.35,.5)[layer]
    rail = [box('fork_lower',core+gap,right,-1.6,rear,dog_z-a-.8,dog_z-a),
            box('fork_upper',core+gap,right,-1.6,rear,dog_z+dog_h+a,dog_z+dog_h+a+.8),
            box('fork_web',right-wall,right,-1.6,rear,dog_z-a-.8,dog_z+dog_h+a+.8)]
    return dict(moving=moving,fixed=fixed,tongue=tongue,dog=dog,rail=rail,
                stroke=stroke,failed_drop=failed_drop,unload=unload,dog_z=dog_z,
                core=core,right=right,left=left,rear=rear,gap=gap,root=root,
                wing=wing,spine=spine,guide_right=guide_right,
                width=right-left+e,depth=rear+1.6+e,
                guide_overlap=wing-gap-e if wing else 0.)


def collisions(moving, fixed, axis, start, end, erosion=0.):
    hits=[]
    for a,b in product(moving,fixed):
        swept=a.move(axis,start).sweep(axis,end-start)
        if swept.inflate(erosion/2).hits(b.inflate(erosion/2)):
            hits.append([a.name,b.name])
    return sorted(set(tuple(x) for x in hits))


def screen(profile,e,bearing,wall,length):
    reasons=set()
    all_hits=set()
    layers=[]
    for layer in range(3):
        g=geometry(profile,e,bearing,wall,length,layer)
        if not connected(g['moving']): reasons.add('disconnected_carriage')
        if not connected(g['fixed']): reasons.add('disconnected_mount')
        # Entire envelope includes failed proof below zero and unloaded travel.
        hits=collisions(g['moving'],g['fixed'],2,-g['failed_drop'],g['stroke']+g['unload'],e)
        all_hits.update(hits)
        if hits: reasons.add('guide_blocks_carriage')
        # Latch contact paths in the connected assembly, both stroke directions.
        # Intended seat contact is exact; E-069 separately erodes free overtravel.
        lift = .2*(layer+1)+.05
        for start,end in [(0.,g['stroke']),(g['stroke'],0.)]:
            if collisions(g['moving'],[g['tongue']],2,start,start+lift):
                reasons.add('loaded_acquisition_collision')
            moved=[s.move(2,start+lift) for s in g['moving']]
            if collisions([g['tongue']],moved,1,-.8,0):
                reasons.add('latch_release_collision')
            moved=[s.move(2,end+lift) for s in g['moving']]
            if collisions([g['tongue']],moved,1,-.8,0):
                reasons.add('latch_insertion_collision')
            if collisions(g['moving'],[g['tongue']],2,end,end+lift):
                reasons.add('loaded_deposition_collision')
        # Dog translates in an actual finite bore. Touch not treated as overlap.
        hits=collisions([g['dog']],g['moving'],0,-(g['gap']+.4+e),0,e)
        if hits: reasons.add('dog_bore_collision')
        all_hits.update(hits)
        hits=collisions([g['tongue']],g['fixed'],1,-.8,0,e)
        if hits: reasons.add('tongue_guide_collision')
        all_hits.update(hits)
        # Parked tongue bypass: inherited .2-mm y gap has only tight-bound use.
        if collisions(g['moving'],[g['tongue'].move(1,-.8)],2,-g['failed_drop'],g['stroke']+g['unload'],e):
            reasons.add('parked_tongue_bypass_collision')
        # Continuous rail; every parked body/dog position is separated in x.
        park=g['dog'].move(0,-(g['gap']+.4+e))
        if any(a.inflate(e/2).hits(b.inflate(e/2)) for a,b in product(
                [x.sweep(2,g['stroke']) for x in g['rail']],
                [x.move(2,-g['failed_drop']).sweep(2,70+g['unload']+g['failed_drop'])
                 for x in g['moving']+[park]])):
            reasons.add('rail_bypass_collision')
        if collisions(g['rail'],g['fixed'],2,0,g['stroke'],e):
            reasons.add('rail_mount_collision')
        deployed_sweep=g['dog'].sweep(0,-(g['gap']+.4+e))
        if collisions([deployed_sweep],g['fixed'],2,-g['failed_drop'],g['stroke']+g['unload'],e):
            reasons.add('dog_mount_collision')
        # No rail in fixed geometry because it intentionally supports the dog;
        # E-069 retains contact/load sequence, error and proof obligations.
        if g['width'] > PITCH+EPS: reasons.add('x_pitch')
        if g['depth'] > PITCH+EPS: reasons.add('y_pitch')
        if profile=='open_c': reasons.add('guide_has_free_negative_y_escape')
        if profile=='captured_t' and g['guide_overlap'] < bearing-EPS:
            reasons.add('insufficient_lip_overlap')
        layers.append(dict(stroke=g['stroke'],dog_z=g['dog_z'],
                           solid_count=len(g['moving'])+len(g['fixed'])+5,
                           moving_connected=connected(g['moving']),mount_connected=connected(g['fixed'])))
    return dict(profile=profile,error=e,bearing=bearing,wall=wall,length=length,
                width=g['width'],depth=g['depth'],guide_overlap=g['guide_overlap'],
                reasons=sorted(reasons),collision_pairs=sorted(all_hits),layers=layers)


def guide_play_counterexample(length):
    g=geometry('captured_t',.15,.2,.4,length)
    # 0.19-mm FREE guide displacement, not a second manufacturing error.
    # Only the common rail datum is biased -0.15 mm; all other parts nominal.
    moved=[s.move(0,.19) for s in g['moving']]
    biased=[s.move(0,-.15) for s in g['rail']]
    return dict(guide_length=length,carriage_shift=.19,common_rail_shift=-.15,
                shifted_carriage_mount_collisions=collisions(moved,g['fixed'],2,0,0),
                centered_carriage_rail_collisions=collisions(g['moving'],biased,2,0,0),
                shifted_carriage_rail_collisions=collisions(moved,biased,2,0,0),
                minimum_x_with_nominal_guide_play=g['width']+2*g['gap'],
                maximum_play_from_pitch_alone=(PITCH-g['width'])/2)


def checks():
    a=box('a',0,1,0,1,0,1)
    assert not a.hits(a.move(0,1)) and a.hits(a.move(0,.999))
    assert a.sweep(2,10).hits(a.move(2,7))
    assert a.connected(a.move(0,1)) and not a.connected(a.move(0,1).move(1,1))
    # Reject an actual shelf/sleeve collision and a genuinely unretained C guide.
    assert 'guide_blocks_carriage' in screen('sleeve',.15,.2,.4,1.6)['reasons']
    assert 'guide_has_free_negative_y_escape' in screen('open_c',.15,.2,.4,1.6)['reasons']
    good=screen('captured_t',.15,.2,.4,1.6)
    assert not good['reasons'], good
    assert math.isclose(good['width'],5.) and math.isclose(good['depth'],4.95)
    assert 'x_pitch' in screen('captured_t',.15,.4,.4,1.6)['reasons']
    for length in [1.6,4.,11.137]:
        bad=guide_play_counterexample(length)
        assert not bad['shifted_carriage_mount_collisions']
        assert not bad['centered_carriage_rail_collisions']
        assert bad['shifted_carriage_rail_collisions']
    # Independent continuous packing expression cross-checks generated extrema.
    for e,b,w in product([.15,.35,.6],[.2,.4],[.4,.8]):
        g=geometry('captured_t',e,b,w,1.6)
        assert math.isclose(g['width'],2.35+b+2*w+11*e)
        assert math.isclose(g['depth'],3.7+3*e+2*w)
    # Off-grid clearance increase: independent holdout, not another topology.
    g=geometry('captured_t',.15,.2,.4,2.173,extra=.031)
    assert not collisions(g['moving'],g['fixed'],2,-g['failed_drop'],g['stroke']+g['unload'],.15)
    assert math.isclose(g['width'],5.031)
    # Preserve the rejected unrelieved flange: it intrudes into the bore.
    untrimmed=[Solid(s.name,s.lo,(s.hi[0],s.hi[1],g['dog_z']+1.2))
               if s.name=='flange' else s for s in g['moving']]
    assert collisions([g['dog']],untrimmed,0,-(g['gap']+.55),0,.15)
    # Deliberately remove failed-proof housing clearance: witness MUST collide.
    lowered=[s.move(2,-.7) if s.name.startswith('bore_') else s for s in g['moving']]
    assert collisions(lowered,g['fixed'],2,-g['failed_drop'],0,.15)
    # A failed datum-error assumption is visible, rather than hidden in sampling.
    assert collisions(g['moving'],g['fixed'],2,0,g['stroke'],.25)
    # Open C throat permits a finite negative-y escape of the isolated backbone.
    c=geometry('open_c',.15,.2,.4,1.6)
    neck=[s for s in c['moving'] if s.name=='neck']
    guides=[s for s in c['fixed'] if s.name.startswith('guide_')]
    assert not collisions(neck,guides,1,-5,0,.15)
    # Neighbor envelope proof includes all motions within a stage's own cell:
    # bounds leave ≥e between adjacent extrema in x/y at the accepted witness.
    assert good['width'] <= PITCH and good['depth'] <= PITCH


def main():
    checks()
    rows=[screen(*v) for v in product(['sleeve','open_c','captured_t'],[.15,.35,.60],
                                     [.2,.4],[.4,.8],[1.6,4.])]
    out={'evidence':'connected finite single-stage geometry and exact sweeps; not stacked CAD or hardware',
         'generated':len(rows),'prescribed_translation_passed':sum(not r['reasons'] for r in rows),
         'guide_play_counterexamples':[guide_play_counterexample(L) for L in [1.6,4.]],
         'survivors_after_guide_play_bound':sum(not r['reasons'] and r['width']+2*(.05+r['error'])<=PITCH+EPS for r in rows),
         'failure_counts_nonexclusive':dict(Counter(x for r in rows for x in r['reasons'])),
         'prescribed_translation_survivors':[r for r in rows if not r['reasons']],
         'continuous_captured_t_minimum_pitch':[
             {'error':e,'bearing':b,'wall':.4,'minimum_x':2.35+b+2*.4+11*e,
              'minimum_y':3.7+3*e+2*.4}
             for e,b in product([.15,.35,.60],[.2,.4])],
         'omitted':['stacked connectors','drive/flag stroke stops','latch faults except absent seat',
                    'reader and brake','strength, friction, creep, wear, guide rotation and dynamics']}
    if '--all' in sys.argv: out['population']=rows
    if '--geometry' in sys.argv:
        g=geometry('captured_t',.15,.2,.4,1.6)
        out['witness_solids']={k:[s.__dict__ for s in g[k]] for k in ['moving','fixed','rail']}
        out['witness_solids'].update({k:g[k].__dict__ for k in ['dog','tongue']})
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
