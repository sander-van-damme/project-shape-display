#!/usr/bin/env python3
"""Gameplay-scale relief choices; exact stepped views and conditional schedules.

Stdlib calculations; --figures DIR also needs matplotlib. Outputs are disposable.
Reuses E-257's semantic raster and scheduler, never rewrites historical evidence.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

import importlib.util

_spec=importlib.util.spec_from_file_location('quarter_screen',
    Path(__file__).resolve().parent.parent/'E-257'/'screen.py')
s=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(s)


def metrics(a, b):
    result=s.stats(a,b)
    d=s.v.rotary.delta(a,b);n=len(d);half=n//2
    result.update(changed=result['lower']+result['rise'],
        row_changed_counts=[sum(x!=0 for x in row) for row in d],
        column_changed_counts=[sum(d[y][x]!=0 for y in range(n)) for x in range(n)],
        quadrant_changed_counts=[sum(d[y][x]!=0 for y in range(y0,y0+half)
            for x in range(x0,x0+half)) for y0,x0 in itertools.product((0,half),repeat=2)])
    assert sum(result['row_changed_counts'])==sum(result['column_changed_counts'])==sum(result['quadrant_changed_counts'])==result['changed']
    return result


def aligned(maps, neutral, depth):
    """Walls remain +20, rocks +10; only ravine depth is deliberately changed."""
    result = {}
    for key, h in maps.items():
        if key == 'road_flat_water':
            continue  # legacy control is not a proposed local-height policy
        result[key] = [[neutral + value - s.GROUND[key] for value in row] for row in h]
        if key == 'ravine':
            result[key] = [[neutral-depth if value == 0 else neutral+value-30
                            for value in row] for row in h]
    return result


def comparison(n, neutral, depth):
    maps, labs = s.v.variants(n)
    maps, labs = s.connected_walls(maps, labs, n)
    targets = aligned(maps, neutral, depth)
    start = s.flat(n, neutral)
    prep = metrics(s.flat(n), start)
    initial = {key: metrics(start, targets[key]) for key in targets}
    suites = {}
    for name, keys in s.SUITES.items():
        transitions = {a+'>'+b: metrics(targets[a], targets[b])
                       for a, b in itertools.permutations(keys, 2)}
        cases = list(transitions.values())+[initial[k] for k in keys]
        suites[name] = dict(transitions=transitions,
            maximum={layout: max(c[layout]['seconds'] for c in cases)
                     for layout in ('independent_b2', 'mask_b2', 'mask_b3')},
            maximum_four16=max(c['four16'] for c in cases),
            maximum_turning_row=max(c['turning_row'] for c in cases))
        pairs=[(start,targets[k]) for k in keys]+[(targets[a],targets[b])
            for a,b in itertools.permutations(keys,2)]
        suites[name]['one_bus_oracles']={kind:max(bus_oracle(s.v.rotary.delta(a,b),kind)
            for a,b in pairs) for kind in ('serial_intersection','parallel_row_mask')}
        if name in ('mixed', 'relief'):
            # Coherent machine-wide bounds, not independent random cell priors.
            suites[name]['rate_bounds']={label:{kind:max(s.v.rotary.schedule(
                s.v.rotary.delta(a,b),2,kind=='mask',pitch=s.WIDTH/n,**kw)['seconds']
                for a,b in pairs) for kind in ('independent','mask')}
                for label,kw in {'rpm1500':dict(rpm=1500),
                    'accel200':dict(rpm=2000,accel=200),
                    'proof100ms':dict(rpm=2000,proof=.1),
                    'write50ms':dict(rpm=2000,write=.05)}.items()}
    # An explicit sequence, not observed session behavior. Reset-free map changes.
    order = s.SUITES['mixed']
    later = sum(s.stats(targets[a], targets[b])['independent_b2']['seconds']
                for a, b in zip(order, order[1:]))
    return dict(n=n, neutral=neutral, depth=depth,
        range_mm=[min(x for h in targets.values() for row in h for x in row),
                  max(x for h in targets.values() for row in h for x in row)],
        prep=prep, initial=initial, suites=suites,
        mixed_sequence=dict(order=order,
            cold_direct=s.stats(s.flat(n),targets[order[0]])['independent_b2']['seconds']+later,
            paid_neutral=prep['independent_b2']['seconds']+initial[order[0]]['independent_b2']['seconds']+later),
        # Preserve the full declared height arrays for exact replay/inspection.
        heightmaps_mm=targets)


def configurable_depth(n):
    """Two software depth presets on ONE granted 50-mm-travel machine.

    Ground stays at 30 mm; only the physical ravine bottom changes. This is a
    command/schedule comparison, not implemented controller or qualified travel.
    """
    maps, labs = s.v.variants(n)
    maps, labs = s.connected_walls(maps, labs, n)
    fast = aligned(maps, 30, 20)
    deep = aligned(maps, 30, 30)
    compact = aligned(maps, 20, 20)
    for key in fast:
        assert all(f == c+10 for fr, cr in zip(fast[key], compact[key])
                   for f, c in zip(fr, cr))
        assert all(0 <= h <= 50 for row in deep[key] for h in row)
        assert all(0 <= h <= 50 for row in fast[key] for h in row)
        assert s.v.rotary.delta(fast[key], deep[key]) == [
            [-10 if key == 'ravine' and h == 0 else 0 for h in row]
            for row in maps[key]]
    switches = {key: dict(to_deep=metrics(fast[key], deep[key]),
                          to_fast=metrics(deep[key], fast[key]),
                          moving_neutral_to_deep=metrics(compact[key], deep[key]))
                for key in s.SUITES['relief']}
    # Every cross-scene/preset transition, including same-scene mode changes.
    states = {f'{mode}:{key}': targets[key]
              for mode, targets in (('fast',fast),('deep',deep))
              for key in s.SUITES['relief']}
    cases = {a+'>'+b:metrics(states[a],states[b])
             for a,b in itertools.permutations(states,2)}
    for a,b in itertools.permutations(s.SUITES['relief'],2):
        assert s.v.rotary.delta(fast[a],fast[b]) == s.v.rotary.delta(compact[a],compact[b])
    return dict(neutral_mm=30, mechanical_range_mm=[0,50],
                presets_ravine_depth_mm=dict(fast=20,deep=30),
                switches=switches, cross_preset_transitions=cases,
                maximum={layout:max(c[layout]['seconds'] for c in cases.values())
                         for layout in ('independent_b2','mask_b2')})


def bus_oracle(delta, kind):
    """One fixed power bus; no travel or row-selection delay, hence favorable.

    Serial case: one intersection at a time. Row-mask case: arbitrary column
    subset in one selected row, signed threshold groups at rest. Actual n*n
    resident AND paths are GRANTED, not solved by the row/column bit count.
    Both pay E-255 dwell/proof, one longest-event retry and common four seconds.
    """
    jobs=[[x] for row in delta for x in row if x] if kind=='serial_intersection' else [row for row in delta if any(row)]
    times=[s.v.rotary.dwell(row,shared=kind=='parallel_row_mask',rpm=2000) for row in jobs]
    return 4+sum(times)+max(times) if times else 0


def corridor(n, extra_cell=False):
    """Synthetic 4-square-long passage. Never claimed to be a sourced map.

    Protect one game-square interior, then place walls OUTSIDE that footprint.
    One extra clear column gives lateral room for base/registration uncertainty.
    """
    k=n//16
    width=k+int(extra_cell)
    h=s.flat(n)
    for y in range(6*k,10*k):
        for x in (7*k-1,7*k+width):
            h[y][x]=20
    return h, width*s.WIDTH/n


def checks():
    s.checks()
    for n in (80,64):
        maps,labs=s.v.variants(n)
        a=aligned(maps,30,30);b=aligned(maps,20,20)
        assert (min(x for h in b.values() for row in h for x in row),
                max(x for h in b.values() for row in h for x in row)) == (0,40)
        # Only ravine bottoms differ after removing the 10-mm common offset.
        for key in b:
            for y,x in itertools.product(range(n),repeat=2):
                assert b[key][y][x] == a[key][y][x]-10 + (10 if key=='ravine' and maps[key][y][x]==0 else 0)
        # The equal-width passage has zero diametral margin, even at fine pitch.
        for extra in (False,True):
            _,width=corridor(n,extra)
            assert abs(width-(25.4+extra*s.WIDTH/n))<1e-10
        # Real initial flat, not just changing the labels on the same delta.
        road=s.stats(s.flat(n,10),maps['road'])
        assert road['stay']+road['lower']+road['rise']==n*n
        if n==80: assert (road['lower'],road['stay'],road['rise'])==(1951,4272,177)
    # Independent necessary arithmetic for the fixed bus, with no travel credited.
    assert bus_oracle([[0,0],[0,0]],'serial_intersection')==0
    assert abs(bus_oracle([[10,0],[0,0]],'serial_intersection') -
               (4+2*(.1+s.v.rotary.spin(10/3,2000))))<1e-10
    assert bus_oracle([[10,-20],[0,0]],'parallel_row_mask') == bus_oracle([[-10,20],[0,0]],'parallel_row_mask')


COLORS={'ground':'#e8dcc1','wall':'#827363','rubble':'#bda078',
        'water':'#6aa9c4','land':'#e2d0a2','rock':'#91978f',
        'plateau':'#d8cba7','ravine':'#536473','bridge':'#ba8957'}


def surface(ax,h,labs,reference=None,neutral=None,limits=None):
    """True-scale polygon tops and every exposed riser; no smooth interpolation."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    n=len(h);p=s.WIDTH/n;faces=[];colors=[]
    for y,x in itertools.product(range(n),repeat=2):
        z=h[y][x];a,b,c,d=x*p,(x+1)*p,y*p,(y+1)*p
        faces.append([(a,c,z),(b,c,z),(b,d,z),(a,d,z)])
        colors.append(COLORS[labs[y][x]])
        for yy,xx,edge in ((y,x-1,((a,c),(a,d))),(y,x+1,((b,c),(b,d))),
                            (y-1,x,((a,c),(b,c))),(y+1,x,((a,d),(b,d)))):
            other=h[yy][xx] if 0<=yy<n and 0<=xx<n else -5
            if z>other:
                q,r=edge
                faces.append([(*q,other),(*r,other),(*r,z),(*q,z)])
                colors.append('#a49478')
    # Same coplanar game-square bases between representations and pitches.
    reference=reference if reference is not None else h
    k=n//16
    for low,high in ((3,6),(10,13)):
        candidates=[(x,y) for y in range(low,high) for x in range(3,13)
                    if labs[y*k][x*k] in {'ground','land','plateau','bridge'}
                    and len({reference[yy][xx] for yy in range(y*k,(y+1)*k)
                             for xx in range(x*k,(x+1)*k)})==1]
        if not candidates:continue
        x,y=min(candidates,key=lambda xy:abs(xy[0]-8))
        cx,cy,z=(x+.5)*25.4,(y+.5)*25.4,h[y*k][x*k]+.4
        circle=[(cx+12.7*math.cos(i*math.pi/24),cy+12.7*math.sin(i*math.pi/24),z) for i in range(48)]
        faces.append(circle);colors.append('#d35780')
        for i in range(12):
            t,u=i*math.pi/6,(i+1)*math.pi/6
            q,r=(cx+2*math.cos(t),cy+2*math.sin(t)),(cx+2*math.cos(u),cy+2*math.sin(u))
            faces.append([(*q,z),(*r,z),(*r,z+25),(*q,z+25)]);colors.append('#67354a')
    ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolors='none'))
    # Dashed frame marks the prepared start height, NOT a physical support plate.
    if neutral is not None:
        ax.plot([0,s.WIDTH,s.WIDTH,0,0],[0,0,s.WIDTH,s.WIDTH,0],
                [neutral]*5,color='#bd456b',linestyle='--',linewidth=1)
    if limits is None:limits=(0,s.WIDTH,0,s.WIDTH)
    x0,x1,y0,y1=limits
    ax.set(xlim=(x0,x1),ylim=(y1,y0),zlim=(-5,70))
    ax.set_box_aspect((x1-x0,y1-y0,75))
    ax.view_init(elev=30,azim=-62)
    ax.set_axis_off()


def figures(folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    folder.mkdir(parents=True,exist_ok=True)
    with PdfPages(folder/'terrain-choices.pdf') as pdf:
        for key,name,ground in [('road','Riverside Road',10),('ravine','Mountain Ravine',30)]:
            fig=plt.figure(figsize=(16,10),facecolor='white')
            for row,n in enumerate((80,64)):
                maps,labs=s.v.variants(n)
                cases=[('A  Minimum start',maps[key],0),
                       ('B  Prepared ground',maps[key],ground),
                       ('C  Visual depression',maps[key+'_visual'],0)]
                for col,(label,h,start) in enumerate(cases):
                    ax=fig.add_subplot(2,3,row*3+col+1,projection='3d')
                    surface(ax,h,labs[key],maps[key],start)
                    m=s.stats(s.flat(n,start),h);prep=s.schedule(s.flat(n,start))['seconds']
                    ax.set_title(f'{label} | {s.WIDTH/n:.2f} mm',fontsize=12,fontweight='bold')
                    ax.text2D(.02,.02,f"Down {m['lower']} / still {m['stay']} / up {m['rise']}\n"
                        f"{m['rows']} rows, {m['columns']} columns | B2 {m['independent_b2']['seconds']:.2f} s\n"
                        f"Cold neutral preparation +{prep:.2f} s; homing additional",
                        transform=ax.transAxes,fontsize=10)
            fig.suptitle(name+' — A and B finish in exactly the same shape',fontsize=19,fontweight='bold',y=.97)
            fig.text(.5,.915,'A moves from minimum; B starts from an already retained elevated plane; C loses physical depth.',ha='center',fontsize=12)
            fig.text(.5,.025,'True-scale stepped surfaces; dashed perimeter = starting plane, not a support plate. Pink = illustrative 25.4-mm bases.\n'
                     'Colors explain semantics; no functioning projection. Pin gaps and miniature stability unqualified.\n'
                     'B2 times: assumed lead 3 mm, 2000 loaded rpm; props, visual setup and extra proof time are additional.\n'
                     'Terrain annotations after Ross McConnell / 2-Minute Tabletop. No measured play or hardware performance.',ha='center',fontsize=10)
            fig.subplots_adjust(top=.88,bottom=.12,wspace=0,hspace=.12)
            pdf.savefig(fig);fig.savefig(folder/(key+'-choices.png'),dpi=140);plt.close(fig)
        fig=plt.figure(figsize=(15,10),facecolor='white')
        for row,n in enumerate((80,64)):
            maps,labs=s.v.variants(n);maps,labs=s.connected_walls(maps,labs,n)
            for col,(neutral,depth,key,title) in enumerate([(30,30,'ravine','50-mm range / 30-mm drop'),
                    (20,20,'ravine','40-mm range / 20-mm drop'),(20,20,'ruins_walls','40-mm range / +20-mm walls')]):
                h=aligned(maps,neutral,depth)[key]
                ax=fig.add_subplot(2,3,row*3+col+1,projection='3d')
                surface(ax,h,labs[key],neutral=neutral)
                m=s.stats(s.flat(n,neutral),h)
                ax.set_title(f'{title}\n{s.WIDTH/n:.2f}-mm pitch; neutral {neutral} mm',fontsize=12,fontweight='bold')
                ax.text2D(.02,.02,f"Down {m['lower']} / still {m['stay']} / up {m['rise']}\n"
                          f"{m['rows']} rows | B2 {m['independent_b2']['seconds']:.2f} s",
                          transform=ax.transAxes,fontsize=10)
        fig.suptitle('Keep real depth; challenge the amount of depth',fontsize=19,fontweight='bold',y=.97)
        fig.text(.5,.92,'The narrower range deliberately reduces ravine relief. Its narrative depth remains a DM rule.',ha='center',fontsize=12)
        fig.text(.5,.03,'Same camera and physical scale. The pin-built bridge has no usable underside in either case.\n'
                 'Wall traces are the E-257 connected alternative: gaps and mergers still need semantic adjudication.\n'
                 'Prepared neutral and homing are extra; no final architecture, print or purchase is selected.',ha='center',fontsize=11)
        fig.subplots_adjust(top=.87,bottom=.13,wspace=0,hspace=.14)
        pdf.savefig(fig);fig.savefig(folder/'depth-and-walls.png',dpi=140);plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('--figures',type=Path);args=p.parse_args()
    checks()
    out={f'{n}:N{neutral}:D{depth}':comparison(n,neutral,depth)
         for n in (80,64) for neutral,depth in ((30,30),(20,20),(30,20))}
    out['configurable_depth']={str(n):configurable_depth(n) for n in (80,64)}
    out['abc']={}
    for n in (80,64):
        maps,_=s.v.variants(n)
        for scene,ground in (('road',10),('ravine',30)):
            for variant,target,start in (('A',maps[scene],0),('B',maps[scene],ground),
                    ('C',maps[scene+'_visual'],0)):
                out['abc'][f'{n}:{scene}:{variant}']=dict(
                    motion=metrics(s.flat(n,start),target),
                    preparation=s.schedule(s.flat(n,start))['seconds'],
                    heightmap_mm=target)
    # Quantized clearance is a geometry diagnostic, not a fit distribution.
    out['passage_controls']={str(n):{
        'clear_width_mm':corridor(n)[1],
        'width_with_one_extra_clear_cell_mm':corridor(n,True)[1],
        'diametral_margin_for_25_4_base_mm':corridor(n)[1]-25.4,
        'nominal_32mm_base_fits_extra_cell':corridor(n,True)[1]>=32}
        for n in (80,64)}
    if args.figures:figures(args.figures)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
