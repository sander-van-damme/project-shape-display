#!/usr/bin/env python3
"""E-254 representation sensitivity; assumptions, not owner-approved workloads.

Stdlib calculations. Optional --figure PATH uses matplotlib for an explanatory
figure, not a CAD/hardware rendering. Original annotations/arrays stay unchanged.
"""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


annotation = load('annotation', HERE/'analyze.py')
rotary = load('rotary', HERE.parent/'E-255/screen.py')
N = 80
FLAT = [[0]*N for _ in range(N)]


def variants():
    maps, semantics = {}, {}
    for item in json.loads((HERE/'sample.json').read_text())['maps']:
        height, labels = annotation.raster(item)
        key = item['id']
        maps[key] = height
        # Base means water for road, plateau for ravine, ground for ruins.
        base = {'road': 'water', 'ravine': 'plateau', 'ruins': 'ground'}[key]
        semantics[key] = [[base if c == 'base' else c for c in row] for row in labels]
    # Preserve local rock height above neighboring ground (10 mm), rather than
    # inheriting absolute 20/40-mm tops when the ground datum is flattened.
    for key in ('road', 'ravine'):
        maps[key+'_visual'] = [[10 if c == 'rock' else 0 for c in row]
                               for row in semantics[key]]
        semantics[key+'_visual'] = semantics[key]
    maps['ruins_walls'] = [[20 if c == 'wall' else 0 for c in row]
                           for row in semantics['ruins']]
    semantics['ruins_walls'] = semantics['ruins']
    # Legacy flattened-water control keeps its original, taller 20-mm rocks.
    maps['road_flat_water'] = [[0 if h == 10 else h for h in row] for row in maps['road']]
    semantics['road_flat_water'] = semantics['road']
    return maps, semantics


def services(old, new):
    d = rotary.delta(old, new)
    counts = annotation.transition(old, new)
    horizontal = rotary.schedule(d, 1)['seconds']
    vertical = rotary.schedule(annotation.transpose(d), 1)['seconds']
    return dict(changed=counts['changed'], rows=counts['rows'],
                columns=len(annotation.occupied(annotation.transpose(d))),
                bank_rows_b3=counts['bank_rows'],
                unchanged_raised=counts['unchanged_raised'],
                unchanged_in_serviced_rows=counts['unchanged_in_serviced_rows'],
                turns_lead3=sum(abs(v) for row in d for v in row)/3,
                independent_b2_2000=rotary.schedule(d, 2, rpm=2000)['seconds'],
                independent_b2_3000=rotary.schedule(d, 2)['seconds'],
                mask_b3_3000=rotary.schedule(d, 3, True)['seconds'],
                four_16_3000=rotary.quarters(d),
                turning_80_3000=min(horizontal, vertical+.5+2*rotary.move(79*5.08))
                    if counts['changed'] else 0,
                e253_b3=counts['e253_seconds'])


def footprint_support(height, labels):
    """Conservative equal-height 5x5-pin squares, not a base stability test.

    Count squares centered on walkable ground/deck; exclude obstacle/water/chasm
    centers. Full square contact is sufficient geometrically, not necessary.
    """
    allowed = {'ground', 'land', 'plateau', 'bridge'}
    eligible = level = 0
    for y in range(0, N, 5):
        for x in range(0, N, 5):
            if labels[y+2][x+2] in allowed:
                eligible += 1
                level += len({height[yy][xx] for yy in range(y, y+5)
                              for xx in range(x, x+5)}) == 1
    return dict(ground_centered_squares=eligible, equal_height_5x5_squares=level)


def benchmark(maps, names):
    pairs = [(FLAT, maps[k]) for k in names]
    pairs += [(maps[a], maps[b]) for a, b in itertools.permutations(names, 2)]
    out = {}
    for shared, rpm in itertools.product((False, True), (2000, 3000)):
        for banks in range(1, 17):
            maximum = max(rotary.schedule(rotary.delta(a, b), banks, shared, rpm=rpm)['seconds']
                          for a, b in pairs)
            if maximum < 30:
                out[f'{"mask" if shared else "independent"}_{rpm}'] = dict(
                    banks=banks, channels=80*banks, max_seconds=maximum,
                    cost_allocation=rotary.costs(banks, shared))
                break
    return out


def neutral_screen(maps):
    """Same physical target heights; a paid uniform starting surface, no free zero.

    Range stays 0..40 mm. These are actual commanded screw positions; holding,
    guidance and signed loaded motion remain unqualified. Map pairs are unchanged.
    """
    out = {}
    for neutral in (10, 20, 30):
        start = [[neutral]*N for _ in range(N)]
        prep = rotary.schedule(rotary.delta(FLAT, start), rpm=2000)['seconds']
        for key in ('ruins', 'road', 'ravine'):
            delta = rotary.delta(start, maps[key])
            signed = [v for row in delta for v in row]
            service = services(start, maps[key])
            out[f'{key}_from_{neutral}'] = dict(
                lowered=sum(v < 0 for v in signed), unchanged=signed.count(0),
                raised=sum(v > 0 for v in signed), service=service,
                cold_neutral_prep_b2_2000=prep,
                two_paid_updates_b2_2000=prep+service['independent_b2_2000'])
    assert (out['road_from_10']['lowered'],out['road_from_10']['unchanged'],
            out['road_from_10']['raised']) == (1951,4272,177)
    # Re-labeling both endpoints with the same datum cannot change signed travel.
    for a,b in itertools.permutations(('ruins','road','ravine'),2):
        assert rotary.delta([[v-20 for v in row] for row in maps[a]],
                            [[v-20 for v in row] for row in maps[b]]) == rotary.delta(maps[a],maps[b])
    return out


def checks(maps, labels):
    old = json.loads((HERE/'heightmaps.json').read_text())
    for k, rows in old.items():
        assert maps[k] == [[int(c)*10 for c in row] for row in rows]
    assert sum(c == 'rock' for r in labels['road'] for c in r) == 177
    assert sum(c == 'rock' for r in labels['ravine'] for c in r) == 167
    assert sum(v > 0 for r in maps['ruins_walls'] for v in r) == 572
    for k in ('road', 'ravine'):
        assert {v for r in maps[k+'_visual'] for v in r} == {0, 10}
        assert all(v == (10 if c == 'rock' else 0)
                   for row, lab in zip(maps[k+'_visual'], labels[k]) for v, c in zip(row, lab))
    assert services(FLAT, FLAT)['independent_b2_2000'] == 0
    # Reverse signed changes preserve independent timing, not force or mask time.
    for a, b in itertools.combinations(maps, 2):
        f, r = rotary.delta(maps[a], maps[b]), rotary.delta(maps[b], maps[a])
        assert rotary.schedule(f, rpm=2000)['seconds'] == rotary.schedule(r, rpm=2000)['seconds']
    # Exact row occupancy is decisive; two cells at opposite bank limits stay two
    # stations, not a mandatory full-board pass. Both unchanged regions are kept.
    witness = [r[:] for r in FLAT]
    witness[0][0], witness[79][79] = 10, 10
    assert rotary.schedule(witness)['stations'] == 2


def figure(maps, labels, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import math
    colors = {'water': '#6ab6d5', 'ravine': '#4b5968', 'land': '#ddd0a6',
              'plateau': '#ddd0a6', 'bridge': '#b78048', 'rock': '#8a918a'}
    cases = [('road_visual', 'River A: flat water + 10-mm rock masses',
              'Easy placement; water rules need a visual marker. No bank drop.'),
             ('road', 'River B: 10-mm land + 20-mm rock tops',
              'Visible banks; edge-straddling bases can rock. Ford is solid.'),
             ('ravine', 'Ravine A: 30-mm plateaux + 40-mm rock tops',
              'Physical drop; pin-built bridge is solid underneath.'),
             ('ravine_visual', 'Ravine B: visual drop + 10-mm rock masses',
              'Flat support; dark region is a marked hazard, not walkable ground.')]
    fig = plt.figure(figsize=(16, 12), facecolor='white')
    for i, (key, title, note) in enumerate(cases, 1):
        h, labs = maps[key], labels[key]
        faces, shades = [], []
        for y in range(N):
            for x in range(N):
                z = h[y][x]
                # mm geometry at true 5.08-mm pitch; no vertical exaggeration.
                a, b, c, d = x*5.08, (x+1)*5.08, y*5.08, (y+1)*5.08
                faces.append([(a,c,z),(b,c,z),(b,d,z),(a,d,z)])
                shades.append(colors[labs[y][x]])
                # Every unequal-height interface and exterior raised face once.
                for yy, xx, edge in ((y, x-1, [(a,c),(a,d)]),
                                     (y, x+1, [(b,c),(b,d)]),
                                     (y-1, x, [(a,c),(b,c)]),
                                     (y+1, x, [(a,d),(b,d)])):
                    other = h[yy][xx] if 0 <= yy < N and 0 <= xx < N else 0
                    if z > other:
                        p, q = edge
                        faces.append([(*p,other),(*q,other),(*q,z),(*p,z)])
                        shades.append('#9b8d71')
        ax = fig.add_subplot(2, 2, i, projection='3d')
        # Same two base locations in each map pair; choose flat interior land
        # in the relief version. Disks are illustrative 25.4-mm bases, no load model.
        reference = maps['road' if key.startswith('road') else 'ravine']
        for band in ((10,30), (50,70)):
            candidates = [(x,y) for y in range(band[0],band[1],5) for x in range(10,70,5)
                          if labs[y+2][x+2] in {'land','plateau','bridge'}
                          and len({reference[yy][xx] for yy in range(y,y+5)
                                   for xx in range(x,x+5)}) == 1]
            if candidates:
                x,y = min(candidates, key=lambda p: abs(p[0]-40))
                cx,cy,z = (x+2.5)*5.08,(y+2.5)*5.08,h[y+2][x+2]+1
                ring=[(cx+12.7*math.cos(t*math.pi/24),cy+12.7*math.sin(t*math.pi/24),z)
                      for t in range(48)]
                faces.append(ring)
                shades.append('#dc568d')
                for t in range(12):
                    a,b=t*math.pi/6,(t+1)*math.pi/6
                    p,q=(cx+2*math.cos(a),cy+2*math.sin(a)),(cx+2*math.cos(b),cy+2*math.sin(b))
                    faces.append([(*p,z),(*q,z),(*q,z+24),(*p,z+24)])
                    shades.append('#762844')
        ax.add_collection3d(Poly3DCollection(faces, facecolors=shades, edgecolors='none'))
        ax.set(xlim=(0,406.4),ylim=(406.4,0),zlim=(0,65))
        ax.set_box_aspect((406.4,406.4,65))
        ax.view_init(elev=27, azim=-62)
        ax.set_axis_off()
        ax.set_title(title,fontsize=13,pad=0,fontweight='bold')
        fp=annotation.footprint(h)
        ax.text2D(.03,.05,f"{fp['raised']}/6400 raised ({100*fp['fraction']:.2f}%) | {fp['rows']} rows\n{note}",
                  transform=ax.transAxes,fontsize=10)
    fig.suptitle('Which physical battlefield helps play?  |  Same 406.4-mm board and camera',
                 fontsize=17,y=.97,fontweight='bold')
    fig.text(.5,.015,'Semantic colors explain water, ground, bridge and rocks; no working overlay is assumed.\n'
             'Pink tokens: illustrative 25.4-mm bases. Schematics omit pin gaps, texture, trees and small props.\n'
             'Terrain annotations after Ross McConnell / 2-Minute Tabletop; heights and representation policies are hypotheses.',
             ha='center',fontsize=10)
    fig.subplots_adjust(top=.90,bottom=.10,wspace=0,hspace=.12)
    fig.savefig(path,dpi=150)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--figure', type=Path)
    args=parser.parse_args()
    maps, labels=variants()
    checks(maps, labels)
    stats={}; updates={}
    for key, h in maps.items():
        stats[key]=dict(occupancy=annotation.footprint(h),
                       support=footprint_support(h,labels[key]))
        updates['initial_'+key]=services(FLAT,h)
        for name, visible in [('east',lambda x,y: x<40),
                              ('local',lambda x,y: not (40<=x<60 and 20<=y<40))]:
            old=[[v if visible(x,y) else 0 for x,v in enumerate(row)] for y,row in enumerate(h)]
            updates[name+'_'+key]=services(old,h)
        # Visual-only reveal of already deployed physical geometry moves no pins.
        updates['visual_reveal_'+key]=services(h,h)
    suites={'legacy_relief':('ruins','road','ravine'),
            'flat_river_deep_ravine':('ruins_walls','road_visual','ravine'),
            'visual_depressions':('ruins_walls','road_visual','ravine_visual')}
    for names in suites.values():
        for a,b in itertools.permutations(names,2):
            updates[a+'_to_'+b]=services(maps[a],maps[b])
    updates['dense_stress']=services(FLAT,[[40]*N for _ in range(N)])
    if args.figure:
        figure(maps,labels,args.figure)
    print(json.dumps(dict(evidence='Assumed encodings and conditional schedules; no player or hardware qualification',
        maps=stats,updates=updates,neutral=neutral_screen(maps),
        suites={k:benchmark(maps,names) for k,names in suites.items()}),indent=2))


if __name__=='__main__':
    main()
