#!/usr/bin/env python3
"""Same-area semantic rerasterization and paid neutral schedules (conditional).

No resampling height arrays, fitted process priors or physical qualifications.
Stdlib JSON and optional SVG figure. Output is reproducible, not repo source.
"""
import argparse
from collections import Counter, deque
import itertools
import json
import math
from pathlib import Path
import importlib.util

DATA = Path(__file__).resolve().parent.parent/'E-254'
_spec = importlib.util.spec_from_file_location('playable_variants', DATA/'playable_variants.py')
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)

WIDTH = 406.4
SUITES = {'relief': ('ruins', 'road', 'ravine'),
          'mixed': ('ruins_walls', 'road_visual', 'ravine'),
          'visual': ('ruins_walls', 'road_visual', 'ravine_visual')}
GROUND = {'ruins': 0, 'ruins_walls': 0, 'road': 10, 'road_visual': 0,
          'ravine': 30, 'ravine_visual': 0, 'road_flat_water': 0}
SOURCE = json.loads((DATA/'sample.json').read_text())['maps']
PROBES = [('thin_wall', 'ruins', (530, 100), (575, 100)),
          ('north_passage', 'ruins', (558, 115), (558, 205)),
          ('south_passage', 'ruins', (420, 382), (510, 382)),
          ('bridge_width', 'ravine', (380, 180), (380, 300)),
          ('ford_width', 'road', (515, 250), (640, 250))]


def flat(n, h=0):
    return [[h]*n for _ in range(n)]


def schedule(d, b=2, shared=False, **kw):
    return v.rotary.schedule(d, b, shared, pitch=WIDTH/len(d), rpm=2000, **kw)


def stats(a, b):
    d = v.rotary.delta(a, b)
    c = Counter(x for row in d for x in row)
    n = len(d)
    rows = [i for i, row in enumerate(d) if any(row)]
    return dict(lower=sum(z for x,z in c.items() if x<0), stay=c[0],
                rise=sum(z for x,z in c.items() if x>0), rows=len(rows),
                columns=sum(any(row[x] for row in d) for x in range(n)),
                bank_rows_b2=[sum(lo<=y<hi for y in rows) for lo,hi in ((0,n//2),(n//2,n))],
                unchanged_in_visited_rows=sum(x==0 for y in rows for x in d[y]),
                turns=sum(abs(x)*z for x,z in c.items())/3,
                independent_b2=schedule(d), mask_b2=schedule(d,shared=True),
                mask_b3=schedule(d,3,True),
                four16=v.rotary.quarters(d,pitch=WIDTH/n,rpm=2000),
                turning_row=min(schedule(d,1)['seconds'],
                    schedule(list(map(list,zip(*d))),1)['seconds']+.5+2*v.rotary.move((n-1)*WIDTH/n))
                    if rows else 0)


def source_label(item, sx, sy):
    label = {'road':'water','ruins':'ground','ravine':'plateau'}[item['id']]
    for name, _, poly in item['features']:
        if v.annotation.inside(sx,sy,poly):
            label = name
    return label


def support(h, item):
    """Same 256 physical square centers at both pitches, including even 4 pins.

    Equal-height tops under whole 25.4-mm square: sufficient geometric footprint,
    not contact, gaps, stability, round-base or load qualification.
    """
    k=len(h)//16
    eligible=level=0
    x0,y0,w,hh=item['crop']
    for y,x in itertools.product(range(16),repeat=2):
        if source_label(item,x0+(x+.5)*w/16,y0+(y+.5)*hh/16) in {'ground','land','plateau','bridge'}:
            eligible+=1
            level+=len({h[yy][xx] for yy in range(y*k,(y+1)*k) for xx in range(x*k,(x+1)*k)})==1
    return dict(eligible=eligible,coplanar=level)


def components(labels, kind):
    todo={(x,y) for y,row in enumerate(labels) for x,c in enumerate(row) if c==kind}
    sizes=[]
    while todo:
        q=deque([todo.pop()]);count=0
        while q:
            x,y=q.popleft();count+=1
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if p in todo: todo.remove(p);q.append(p)
        sizes.append(count)
    return sorted(sizes,reverse=True)


def transect(labs,item,a,b):
    """Exact intersections of axis-aligned probe with raster-cell boundaries."""
    n=len(labs);x0,y0,w,h=item['crop']
    ax,ay=(a[0]-x0)*WIDTH/w,(a[1]-y0)*WIDTH/h
    bx,by=(b[0]-x0)*WIDTH/w,(b[1]-y0)*WIDTH/h
    length=math.hypot(bx-ax,by-ay);cuts={0.,1.}
    for u in range(n+1):
        for start,end in ((ax,bx),(ay,by)):
            if end!=start:
                t=(u*WIDTH/n-start)/(end-start)
                if 0<t<1:cuts.add(t)
    cuts=sorted(cuts);runs=[]
    for lo,hi in zip(cuts,cuts[1:]):
        t=(lo+hi)/2
        x,y=int((ax+t*(bx-ax))*n/WIDTH),int((ay+t*(by-ay))*n/WIDTH)
        label=labs[y][x];size=(hi-lo)*length
        if runs and runs[-1]['label']==label:runs[-1]['mm']+=size
        else:runs.append(dict(label=label,mm=size))
    return runs


def suite_screen(maps,n,names,aligned=False):
    # Aligned physical ground at 30 mm: river floor20, ravine floor0, walls50.
    target={k:[[h+30-GROUND[k] for h in row] for row in maps[k]]
            if aligned else maps[k] for k in names}
    start=flat(n,30 if aligned else 0)
    pairs=[(start,target[k]) for k in names]+[(target[a],target[b]) for a,b in itertools.permutations(names,2)]
    result={}
    for shared in (False,True):
        times={str(b):max(schedule(v.rotary.delta(a,z),b,shared)['seconds'] for a,z in pairs) for b in (1,2,3,4)}
        first=next((b for b in (1,2,3,4) if times[str(b)]<30),None)
        result['mask' if shared else 'independent']=dict(max_s_by_banks=times,first_below30=first,
            allocation=v.rotary.costs(first,shared,n=n) if first else None)
    # Explicit sequence alternatives: direct initial; prepared neutral; and paid
    # flatten-to-neutral between each map. No blanket reset of loaded regions.
    sequences={}
    for order in itertools.permutations(names):
        for neutral in (0,10,20,30) if not aligned else (30,):
            home=flat(n,neutral)
            prep=schedule(v.rotary.delta(flat(n),home))['seconds']
            direct=[schedule(v.rotary.delta(flat(n),target[order[0]]))['seconds']]
            prepared=[schedule(v.rotary.delta(home,target[order[0]]))['seconds']]
            resets=prepared[:]
            for a,z in zip(order,order[1:]):
                t=schedule(v.rotary.delta(target[a],target[z]))['seconds']
                direct.append(t);prepared.append(t)
                resets.extend([schedule(v.rotary.delta(target[a],home))['seconds'],
                               schedule(v.rotary.delta(home,target[z]))['seconds']])
            sequences['>'.join(order)+f':N{neutral}']=dict(prep=prep,direct_sum=sum(direct),
                paid_neutral_sum=prep+sum(prepared),reset_each_sum=prep+sum(resets),
                visible_prepared=prepared)
    result['transitions']={f'{a}>{z}':stats(target[a],target[z]) for a,z in itertools.permutations(names,2)}
    result['sequences']=sequences
    result['physical_range_mm']=[min(h for k in names for row in target[k] for h in row),
                                  max(h for k in names for row in target[k] for h in row)]
    return result


def checks():
    # Legacy calculations stay identical; independently derive the dense B2 time.
    old,_=v.variants()
    raw=json.loads((DATA/'heightmaps.json').read_text())
    for key,rows in raw.items():assert old[key]==[[int(c)*10 for c in row] for row in rows]
    for n in (64,80):
        p=WIDTH/n;d=flat(n,40);m=n//2
        expected=4+m*(.1+v.rotary.spin(40/3,2000))+.05+(m-1)*max(.05,v.rotary.move(p))+v.rotary.move((m-1)*p)+.1+v.rotary.spin(40/3,2000)
        assert abs(schedule(d)['seconds']-expected)<1e-10
        assert schedule(flat(n))['seconds']==0
        witness=flat(n);witness[0][0]=10;witness[n-1][n-1]=-10
        assert schedule(witness)['stations']==2
        assert [len(range(i,min(n,i+math.ceil(n/3)))) for i in range(0,n,math.ceil(n/3))]==([22,22,20] if n==64 else [27,27,26])
        maps,labs=v.variants(n)
        joined,jlabs=connected_walls(maps,labs,n)
        passage=transect(jlabs['ruins'],SOURCE[0],PROBES[2][2],PROBES[2][3])
        assert abs(next(r['mm'] for r in passage if r['label']=='ground')-25.4)<1e-10
        assert joined['road']==maps['road'] and joined['ravine']==maps['ravine']
        for y,x in itertools.product(range(n),repeat=2):
            assert joined['ruins'][y][x]==maps['ruins'][y][x] or jlabs['ruins'][y][x]=='wall'
        for a,b in itertools.combinations(maps,2):
            d=v.rotary.delta(maps[a],maps[b]);r=v.rotary.delta(maps[b],maps[a])
            assert schedule(d)['seconds']==schedule(r)['seconds']
            assert d==v.rotary.delta([[h-20 for h in row] for row in maps[a]],[[h-20 for h in row] for row in maps[b]])
        # Square-aligned one-square passage/bridge retains 25.4 mm at both grids.
        item=dict(id='ruins',crop=[0,0,WIDTH,WIDTH])
        k=n//16;toy=[['wall' if x<k or x>=2*k else 'ground' for x in range(n)] for _ in range(n)]
        assert abs(transect(toy,item,(0,12.7),(76.2,12.7))[1]['mm']-25.4)<1e-10
    assert v.rotary.costs(2,n=80)==v.rotary.costs(2)


def connected_walls(maps, labs, n):
    """Retain polygon fill and join sampled traced wall centerlines, per polyline.

    Four-neighbor stairs; on diagonal steps add x-first bridge cell. This is a
    declared conversion policy, not a repair to source art or proof of playability.
    Separate centerlines never get joined; doors remain explicit probe checks.
    """
    import copy
    maps,labs=copy.deepcopy(maps),copy.deepcopy(labs)
    item=SOURCE[0];x0,y0,w,h=item['crop'];added=set()
    for line in item['wall_centerlines']:
        prior=None
        for a,b in zip(line,line[1:]):
            steps=max(1,math.ceil(max(abs(b[0]-a[0])*n/w,abs(b[1]-a[1])*n/h)*10))
            for i in range(steps+1):
                t=i/steps;x=math.floor((a[0]+t*(b[0]-a[0])-x0)*n/w);y=math.floor((a[1]+t*(b[1]-a[1])-y0)*n/h)
                if not (0<=x<n and 0<=y<n):prior=None;continue
                if prior is not None and x!=prior[0] and y!=prior[1]:added.add((x,prior[1]))
                added.add((x,y));prior=x,y
    for x,y in added:
        for key in ('ruins','ruins_walls'):
            maps[key][y][x]=20;labs[key][y][x]='wall'
    return maps,labs


def run(n):
    maps,labs=v.variants(n);out={};neutral={};probes={}
    connected,clabs=connected_walls(maps,labs,n)
    for key,h in maps.items():
        item=next(m for m in SOURCE if m['id']==key.split('_')[0])
        out[key]=dict(labels=dict(Counter(c for row in labs[key] for c in row)),
            support=support(h,item),initial=stats(flat(n),h))
        for z in (10,20,30):
            s=stats(flat(n,z),h);prep=schedule(flat(n,z))['seconds']
            neutral[f'{key}:N{z}']=dict(moves=s,prep=prep,cold_sum=prep+s['independent_b2']['seconds'])
        # Same physical 4x4-square reveal region at both resolutions.
        old=[[0 if n//2<=x<3*n//4 and n//4<=y<n//2 else h[y][x] for x in range(n)] for y in range(n)]
        out[key]['local']=stats(old,h)
    for name,key,a,b in PROBES:
        probes[name]=transect(labs[key],next(m for m in SOURCE if m['id']==key),a,b)
    # Coherent global x/y registration uncertainty +/-half a coarse cell. Bounds,
    # not measured annotation/process errors or random independent pixel jitter.
    phase={}
    for dx,dy in itertools.product((-.5,0,.5),repeat=2):
        item=json.loads(json.dumps(SOURCE[0]));item['crop'][0]+=dx*item['crop'][2]/64;item['crop'][1]+=dy*item['crop'][3]/64
        _,labels=v.annotation.raster(item,n=n)
        phase[f'{dx},{dy}']=dict(wall_cells=sum(c=='wall' for r in labels for c in r),
            wall_components=len(components(labels,'wall')),
            thin_wall=transect(labels,item,PROBES[0][2],PROBES[0][3]))
    return dict(n=n,pitch=WIDTH/n,maps=out,neutral=neutral,probes=probes,
        wall_components=components(labs['ruins'],'wall'),phase_bounds=phase,
        connected_walls=dict(added_cells=sum(c=='wall' for r in clabs['ruins'] for c in r)-sum(c=='wall' for r in labs['ruins'] for c in r),
            components=components(clabs['ruins'],'wall'),
            probes={name:transect(clabs[key],SOURCE[0],a,b) for name,key,a,b in PROBES if key=='ruins'},
            support=support(connected['ruins'],SOURCE[0]),
            initial=stats(flat(n),connected['ruins']),
            suites={key:suite_screen(connected,n,names) for key,names in SUITES.items()},
            ground_aligned={key:suite_screen(connected,n,names,True) for key,names in SUITES.items()}),
        suites={key:suite_screen(maps,n,names) for key,names in SUITES.items()},
        ground_aligned={key:suite_screen(maps,n,names,True) for key,names in SUITES.items()},
        dense=stats(flat(n),flat(n,40)),dense50=stats(flat(n),flat(n,50)),mixed_dense=stats(
            [[40*((x+y)%2) for x in range(n)] for y in range(n)],
            [[40*(1-(x+y)%2) for x in range(n)] for y in range(n)]),
        inventory=dict(cells=n*n,moving_parts=2*n*n,guide_duties=2*n*n,
            independent_b2_channels=2*n,mask_b3_channels=3*n,
            row_and_column_lines=2*n,and_contacts=2*n*n,
            four16_allocation=250+n*n*.02+4*(55+35)+64*4,
            turning_row_before_yaw=v.rotary.costs(1,n=n)['assumed_total'],
            assembly_two_touches_hours={s:2*n*n*s/3600 for s in (5,10,20)},
            independent_b2=v.rotary.costs(2,n=n),mask_b2=v.rotary.costs(2,True,n=n),
            mask_b3=v.rotary.costs(3,True,n=n)))


def figure(path):
    """Standalone vector artifact; source polygons and digital cells are inspectable."""
    from html import escape
    colors={'ground':'#eee5cb','wall':'#584f47','rubble':'#ac9271','water':'#5aaace',
            'land':'#ddd0a6','rock':'#8a918a','plateau':'#ddd0a6','ravine':'#354351','bridge':'#b78048'}
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="2050" viewBox="0 0 1000 2050">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<style>text{font-family:sans-serif;fill:#222} .title{font-size:16px;font-weight:bold}</style>',
         '<text x="30" y="30" class="title">Same 406.4-mm window: semantic polygons at fifth- and quarter-square pitch</text>']
    for col,n in enumerate((80,64)):
        maps,labs=v.variants(n)
        for row,item in enumerate([SOURCE[0]]+SOURCE):
            key=item['id'];shown=labs if row!=1 else connected_walls(maps,labs,n)[1]
            ox,oy=40+col*490,90+row*475;p=WIDTH/n
            title=item['title']+(' + connected centerlines' if row==1 else '')
            svg.append(f'<text x="{ox}" y="{oy-27}" class="title">{escape(title)}</text>')
            svg.append(f'<text x="{ox}" y="{oy-8}">{n}×{n}; {p:.2f} mm; 25.4-mm game grid</text>')
            svg.append(f'<svg x="{ox}" y="{oy}" width="{WIDTH}" height="{WIDTH}" viewBox="0 0 {WIDTH} {WIDTH}">')
            for y,rr in enumerate(shown[key]):
                start=0
                for end in range(1,n+1):
                    if end==n or rr[end]!=rr[start]:
                        svg.append(f'<rect x="{start*p:.4f}" y="{y*p:.4f}" width="{(end-start)*p:.4f}" height="{p:.4f}" fill="{colors[rr[start]]}"/>');start=end
            x0,y0,w,h=item['crop']
            for _,_,poly in item['features']:
                points=' '.join(f'{(x-x0)*WIDTH/w:.3f},{(y-y0)*WIDTH/h:.3f}' for x,y in poly)
                svg.append(f'<polygon points="{points}" fill="none" stroke="black" stroke-width=".5"/>')
            for i in range(17):
                z=i*25.4
                svg.append(f'<path d="M {z},0 V {WIDTH} M 0,{z} H {WIDTH}" stroke="white" stroke-opacity=".4" stroke-width=".5"/>')
            for name,k,a,b in PROBES:
                if k==key:
                    ax,ay=(a[0]-x0)*WIDTH/w,(a[1]-y0)*WIDTH/h
                    bx,by=(b[0]-x0)*WIDTH/w,(b[1]-y0)*WIDTH/h
                    svg.append(f'<path d="M {ax},{ay} L {bx},{by}" stroke="#f02d9a" stroke-width="1.5"/>')
                    svg.append(f'<text x="{ax}" y="{ay-4}" style="font-size:8px;fill:#a40059">{name}</text>')
            svg.append('</svg>')
    for i,line in enumerate(['Black: original polygons. Pink: numerical probes. Colors label terrain; they do not establish projection.',
        'Wall continuity is a conversion alternative; compare openings and mergers before choosing it.',
        '25.4-mm squares illustrate base footprints. Physical/visual policies retain labels but change heights.',
        'Annotations after Ross McConnell / 2-Minute Tabletop. Schematics; no player or hardware qualification.']):
        svg.append(f'<text x="30" y="{1980+i*19}" font-size="12">{escape(line)}</text>')
    path.write_text('\n'.join(svg+['</svg>']))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--figure',type=Path);args=parser.parse_args()
    checks();results={n:run(n) for n in (80,64)}
    if args.figure:figure(args.figure)
    print(json.dumps(dict(evidence='Calculations and bounded assumptions; no play or hardware qualification',results=results),indent=2))


if __name__=='__main__':main()
