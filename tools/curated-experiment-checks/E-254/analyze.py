#!/usr/bin/env python3
"""Hand-annotated workload counts and conditional full-service schedules; stdlib.
No observed play, calibrated manufacturing priors, or hardware qualification.
stdout JSON is disposable. --write-maps explicitly refreshes requested data.
"""
import argparse
from collections import Counter, deque
import importlib.util
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('e253', HERE.parent/'E-253/screen.py')
crank = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crank)
N = 80


def inside(x, y, poly):
    hit = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:]+poly[:1]):
        if (ay > y) != (by > y) and x < (bx-ax)*(y-ay)/(by-ay)+ax:
            hit = not hit
    return hit


def raster(m, shift=0):
    x0, y0, w, h = m['crop']
    rows, labels = [], []
    for y in range(N):
        row, lab = [], []
        for x in range(N):
            sx, sy = x0+(x+.5)*w/N+shift, y0+(y+.5)*h/N
            value, label = m['base']*10, 'base'
            for name, level, poly in m['features']:
                if inside(sx, sy, poly):
                    value, label = 10*level, name
            row.append(value); lab.append(label)
        rows.append(row); labels.append(lab)
    return rows, labels


def components(mask):
    todo = {(x,y) for y in range(N) for x in range(N) if mask[y][x]}
    sizes = []
    while todo:
        seed = todo.pop(); q = deque([seed]); size = 1
        while q:
            x,y = q.popleft()
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if p in todo:
                    todo.remove(p); q.append(p); size += 1
        sizes.append(size)
    return sorted(sizes, reverse=True)


def occupied(mask):
    return [y for y in range(N) if any(mask[y])]


def banks(rows, b=3):
    width = math.ceil(N/b)
    return [[y-i*width for y in rows if i*width <= y < min(N,(i+1)*width)] for i in range(b)]


def transpose(m):
    return [list(r) for r in zip(*m)]


def footprint(m):
    mask = [[h>0 for h in row] for row in m]
    cc = components(mask); count = sum(map(sum,mask))
    perimeter = sum(1 for y in range(N) for x in range(N) if mask[y][x]
                    for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                    if not (0<=xx<N and 0<=yy<N) or not mask[yy][xx])
    # Explicit one-pin boundary ambiguity; outside-board cells are ignored.
    bounds = []; boundary_rows = []
    for dilate in (False,True):
        expanded = [[(any if dilate else all)(mask[yy][xx]
            for yy in range(max(0,y-1),min(N,y+2))
            for xx in range(max(0,x-1),min(N,x+2))) for x in range(N)] for y in range(N)]
        bounds.append(sum(map(sum,expanded))/6400)
        boundary_rows.append(list(map(len,banks(occupied(expanded)))))
    return dict(raised=count, fraction=count/6400, levels=dict(Counter(itertools.chain.from_iterable(m))),
                rows=len(occupied(mask)), columns=len(occupied(transpose(mask))),
                bank_rows=list(map(len,banks(occupied(mask)))), components=len(cc), largest_component=cc[0] if cc else 0,
                boundary_edges=perimeter, one_pin_footprint_bounds=bounds, one_pin_bank_row_bounds=boundary_rows)


def move(d):
    # E-050 central translation; no jerk bound.
    return 2*math.sqrt(d/5000) if d<=200**2/5000 else d/200+200/5000


def spin(turns, rpm=3000, accel_rpm_s=60000):
    # New labelled ramp allowance; identical trapezoidal law in revolutions.
    v, a = rpm/60, accel_rpm_s/60
    return 2*math.sqrt(turns/a) if turns<=v*v/a else turns/v+v/a


def screw_row(delta, b=3, lead=.4):
    # 80 independently reversible spindles/head; change-only docking assumed.
    # This avoids hidden two-sign serialization of a single common shaft.
    rows = occupied(delta); schedules = []; max_dwell = 0
    for br in banks(rows,b):
        i = len(schedules); start=i*math.ceil(N/b); last=0; seek=0; service=0
        for r in br:
            seek += max(.05,move(abs(r-last)*5.08))
            dwell=.08+.02+spin(max(delta[start+r])/lead)
            max_dwell=max(max_dwell,dwell); service+=dwell; last=r
        if br: seek+=move(last*5.08)
        schedules.append((seek,service))
    if not rows: return dict(seconds=0,seek=0,service=0,retry=0,heads=80*b)
    # Conservative one full row retry after latest finishing bank, .5-s remote
    # diagnosis allowance remains in fixed 4 s. Immediate retained station retry.
    s=max(schedules,key=sum)
    return dict(seconds=4+sum(s)+max_dwell,seek=s[0],service=s[1],retry=max_dwell,heads=80*b)


def screw_serial(delta, lead=.4, matrix=False):
    # One screwdriver serpentine traversal; alternatively grant free stationary
    # matrix routing but charge .05 s address/AND selection each site.
    points=[(x,y) for y in range(N) for x in (range(N) if y%2==0 else range(N-1,-1,-1)) if delta[y][x]]
    seek=service=0; prev=(0,0); longest=0
    for x,y in points:
        seek += .05 if matrix else move(5.08*max(abs(x-prev[0]),abs(y-prev[1])))
        dwell=.08+.02+spin(delta[y][x]/lead)
        service+=dwell; longest=max(longest,dwell);prev=(x,y)
    if points and not matrix: seek+=move(5.08*max(prev))
    return dict(seconds=4+seek+service+longest if points else 0,seek=seek,service=service,retry=longest)


def transition(old,new):
    delta=[[abs(b-a) for a,b in zip(ra,rb)] for ra,rb in zip(old,new)]
    rows=occupied(delta); count=sum(d>0 for r in delta for d in r)
    unchanged=6400-count
    changed_rows_u=sum(delta[y][x]==0 for y in rows for x in range(N))
    raised_u=sum(a>0 and a==b for ra,rb in zip(old,new) for a,b in zip(ra,rb))
    signed=Counter(b-a for ra,rb in zip(old,new) for a,b in zip(ra,rb))
    crank_time=crank.sparse(crank.geometry(60),banks(rows))
    n=max(map(len,banks(rows)),default=0)
    return dict(changed=count,fraction=count/6400,rows=len(rows),bank_rows=list(map(len,banks(rows))),
        unchanged=unchanged,unchanged_raised=raised_u,unchanged_in_serviced_rows=changed_rows_u,
        delta_mm=dict(sorted(signed.items())),total_travel_mm=sum(map(sum,delta)),
        turns_at_lead_04=sum(map(sum,delta))/.4, row_max_travel_mm=sum(max(r) for r in delta),
        e253_seconds=crank_time,e253_physical_decisions=640*len(rows),
        e253_program_rounds=n,e253_retry_decisions=640 if count else 0,
        row_slot_inflation=80*len(rows)/count if count else 0,
        screw_rows={f'B{b}_lead{lead}':screw_row(delta,b,lead) for b in (1,2,3) for lead in (.15,.4,1.,3.)},
        screw_serial=screw_serial(delta),screw_matrix_serial=screw_serial(delta,matrix=True),
        changed_docks=count, row_orientation90_e253_seconds=crank.sparse(crank.geometry(60),banks(occupied(transpose(delta)))))


def checks():
    assert inside(.5,.5,[[0,0],[1,0],[1,1],[0,1]])
    assert not inside(2,.5,[[0,0],[1,0],[1,1],[0,1]])
    assert abs(spin(100)-2.05)<1e-10
    assert abs(move(5.08)-2*math.sqrt(5.08/5000))<1e-12
    assert [len(x) for x in banks(list(range(80)))]==[27,27,26]
    flat=[[0]*80 for _ in range(80)]; dense=[[40]*80 for _ in range(80)]
    t=transition(flat,dense)
    assert t['changed']==6400 and t['turns_at_lead_04']==640000
    assert abs(t['screw_rows']['B3_lead0.4']['service']-27*2.15)<1e-9
    assert transition(dense,dense)['changed']==0
    assert transition(dense,dense)['unchanged_raised']==6400
    one=[r[:] for r in flat];one[27][5]=20
    assert transition(flat,one)['bank_rows']==[0,1,0]
    assert footprint(one)['components']==1
    return flat,dense


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-maps',action='store_true');args=parser.parse_args()
    flat,dense=checks();data=json.loads((HERE/'sample.json').read_text());maps={};stats={}
    for m in data['maps']:
        height,labels=raster(m);maps[m['id']]=height;stats[m['id']]=footprint(height)
        wall=[[label=='wall' for label in r] for r in labels]
        length=0.; orientations=Counter(); x0,y0,w,h=m['crop']
        for line in m.get('wall_centerlines',[]):
            for (ax,ay),(bx,by) in zip(line,line[1:]):
                # Midpoint quadrature clips the hand trace to the sampled window.
                fraction=sum(x0<=ax+(bx-ax)*(k+.5)/1000<x0+w and y0<=ay+(by-ay)*(k+.5)/1000<y0+h for k in range(1000))/1000
                segment=math.hypot(bx-ax,by-ay)*fraction/(w/16)
                length+=segment
                angle=math.degrees(math.atan2(abs(by-ay),abs(bx-ax)))
                orientations['horizontal_15deg' if angle<=15 else 'vertical_15deg' if angle>=75 else 'other']+=segment
        stats[m['id']]['traced_wall_length_grid_squares']=length
        stats[m['id']]['wall_orientation_lengths_grid_squares']=dict(orientations)
        stats[m['id']]['wall_cells']=sum(map(sum,wall));stats[m['id']]['wall_components']=components(wall)
        stats[m['id']]['crop_x_shift_one_square']=[footprint(raster(m,s)[0])['fraction'] for s in (-35,35)]
    maps['road_flat_water']=[[0 if h==10 else h for h in row] for row in maps['road']]
    stats['road_flat_water']=footprint(maps['road_flat_water'])
    encoded={k:[''.join(str(h//10) for h in r) for r in v] for k,v in maps.items()}
    if args.write_maps:(HERE/'heightmaps.json').write_text(json.dumps(encoded,indent=2)+'\n')
    assert json.loads((HERE/'heightmaps.json').read_text())==encoded, 'Stored maps differ from annotation rasterization'
    out={}
    for name,m in maps.items():
        out['initial_'+name]=transition(flat,m)
        west=[[h if x<40 else 0 for x,h in enumerate(row)] for row in m]
        out['reveal_east_'+name]=transition(west,m)
        local=[[0 if 40<=x<60 and 20<=y<40 else h for x,h in enumerate(row)] for y,row in enumerate(m)]
        out['reveal_4x4_squares_'+name]=transition(local,m)
    for a,b in itertools.permutations(('ruins','road','ravine'),2):
        out[a+'_to_'+b]=transition(maps[a],maps[b])
        assert out[a+'_to_'+b]['changed']==sum(maps[a][y][x]!=maps[b][y][x] for y in range(80) for x in range(80))
    out['dense_stress']=transition(flat,dense)
    # Joint channel/cost discriminator, not a fitted population percentile.
    sample_pairs=[(flat,maps[k]) for k in ('ruins','road','ravine')]
    sample_pairs += [(maps[a],maps[b]) for a,b in itertools.permutations(('ruins','road','ravine'),2)]
    minimum_banks={}
    for lead in (.15,.4,1.,3.):
        for b in range(1,81):
            times=[screw_row([[abs(q-p) for p,q in zip(r,t)] for r,t in zip(x,y)],b,lead)['seconds'] for x,y in sample_pairs]
            if max(times)<30:
                minimum_banks[str(lead)]=dict(banks=b,channels=80*b,maximum_sample_seconds=max(times),
                    channel_allowances={str(c):(c-250-6400*.02)/(80*b) for c in (500,1000,1500)})
                break
    # Square-thread necessary friction thresholds, not finished-thread predictions.
    screw_bounds=[dict(diameter_mm=d,lead_mm=l,mu_threshold=l/(math.pi*d))
                  for d,l in itertools.product((2.8,3.,3.2),(.15,.35,.4,.45,1.,3.))]
    print(json.dumps(dict(evidence='Annotation calculations and conditional schedules; no hardware or play measurements',maps=stats,transitions=out,minimum_screw_banks=minimum_banks,screw_hold_thresholds=screw_bounds),indent=2))

if __name__=='__main__':main()
