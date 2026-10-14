#!/usr/bin/env python3
"""Half-square terrain/direct spindle comparison; geometry and conditional models only."""
import argparse
import functools
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('direct', Path(__file__).resolve().parents[1]/'E-272/direct.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
s = d.h.a.c.v.s
# Proposed protected opening, source coordinates. A 25.4-mm-wide clear rectangle
# through the known southern doorway, not a new claim about player practice.
CORRIDOR = (449., 350., 484., 415.)


def clipped_area(poly, box):
    """Sutherland-Hodgman clipping; positive area means semantic obstruction."""
    points = list(poly)
    for axis, edge, sign in ((0,box[0],1),(0,box[2],-1),(1,box[1],1),(1,box[3],-1)):
        out = []
        for a,b in zip(points, points[1:]+points[:1]):
            ia,ib = sign*(a[axis]-edge)>=0, sign*(b[axis]-edge)>=0
            if ia: out.append(a)
            if ia != ib:
                t=(edge-a[axis])/(b[axis]-a[axis])
                out.append(tuple(a[j]+t*(b[j]-a[j]) for j in (0,1)))
        points=out
    return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points,points[1:]+points[:1])))/2


@functools.lru_cache(None)
def terrain(n, protected=False):
    maps,labs=s.v.variants(n)
    maps,labs=s.connected_walls(maps,labs,n)
    changed=[]
    if protected:
        x0,y0,w,h=s.SOURCE[0]['crop']
        for y,x in itertools.product(range(n),repeat=2):
            box=(x0+x*w/n,y0+y*h/n,x0+(x+1)*w/n,y0+(y+1)*h/n)
            if min(box[2],CORRIDOR[2])>max(box[0],CORRIDOR[0]) and min(box[3],CORRIDOR[3])>max(box[1],CORRIDOR[1]):
                if maps['ruins'][y][x]: changed.append((x,y))
                for key in ('ruins','ruins_walls'):
                    maps[key][y][x]=0;labs[key][y][x]='ground'
    return maps,labs,changed


def intended_ground_support(maps,item,n):
    k=n//16; x0,y0,w,h=item['crop'];key=item['id']
    eligible=preserved=0
    for y,x in itertools.product(range(16),repeat=2):
        if s.source_label(item,x0+(x+.5)*w/16,y0+(y+.5)*h/16) in {'ground','land','plateau','bridge'}:
            eligible+=1
            preserved+=all(maps[key][yy][xx]==s.GROUND[key] for yy in range(y*k,(y+1)*k) for xx in range(x*k,(x+1)*k))
    return dict(eligible=eligible,whole_square_at_intended_ground=preserved)


def geometry(n, protected=False):
    raw,raw_labs=s.v.variants(n)
    maps,labs,changed=terrain(n,protected)
    probes={name:s.transect(labs[key],next(i for i in s.SOURCE if i['id']==key),a,b)
            for name,key,a,b in s.PROBES if name!='north_passage'}
    p=s.WIDTH/n; cap=p-.4; yaw=math.radians(3)
    # Exact square-polygon SAT for two adjacent caps at opposite allowed yaw.
    def square(cx,angle,width):
        return [(cx+x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle))
                for x,y in ((-width/2,-width/2),(width/2,-width/2),(width/2,width/2),(-width/2,width/2))]
    left,right=square(0,yaw,cap),square(p,-yaw,cap)
    gaps=[]
    for angle in (yaw,-yaw,yaw+math.pi/2,-yaw+math.pi/2):
        axis=math.cos(angle),math.sin(angle)
        a=[x*axis[0]+y*axis[1] for x,y in left];b=[x*axis[0]+y*axis[1] for x,y in right]
        gaps.append(max(min(b)-max(a),min(a)-max(b)))
    # A fixed 4.4-mm square stem rotates in a nominal 4.64-mm square guide.
    guide_width=4.4*(math.cos(yaw)+math.sin(yaw))
    return dict(n=n,pitch=p,protected=protected,wall_cells=sum(c=='wall' for row in labs['ruins'] for c in row),
                raw_components=len(s.components(raw_labs['ruins'],'wall')),
                wall_components=len(s.components(labs['ruins'],'wall')),cleared_cells=changed,
                probes=probes,support={item['id']:intended_ground_support(maps,item,n) for item in s.SOURCE},
                cap_width_mm=cap,cap_area_per_board_mm2=n*n*cap*cap,
                bare_4p4_top_area_fraction=(4.4/p)**2,cap_overhang_mm=(cap-4.4)/2,
                three_degree_guide_envelope_mm=guide_width,guide_fits_nominal=guide_width<=4.64,
                opposite_yaw_max_separating_gap_mm=max(gaps),caps_overlap=max(gaps)<0,
                max_opposite_yaw_deg=math.degrees(math.asin(p/(math.sqrt(2)*cap)))-45,
                pairs=n*n,guide_apertures=2*n*n,shared_ribs_two_layers=2*(n-1),
                base32_min_grid_width_mm=math.ceil(32/p)*p,
                cap_edge_moment_0p1N_Nmm=.1*cap/2)


@functools.lru_cache(None)
def workloads(n,stroke,protected):
    maps,_,_=terrain(n,protected)
    ground=stroke-20
    # Same aligned physical relief semantics as E-258; S50 retains both depth presets.
    states={}
    for depth in ((20,) if stroke==40 else (20,30)):
        targets=d.h.a.c.v.aligned(maps,ground,depth)
        states.update({f'{depth}:{key}':targets[key] for key in s.SUITES['relief']})
    start=s.flat(n,ground)
    scene={f'ground>{key}':d.h.a.r.delta(start,h) for key,h in states.items()}
    scene.update({a+'>'+b:d.h.a.r.delta(states[a],states[b]) for a,b in itertools.permutations(states,2)})
    local={};w=n//4;step=n//8
    for name,h in states.items():
        delta=d.h.a.r.delta(start,h)
        for y0,x0 in itertools.product(range(0,n-w+1,step),repeat=2):
            local[f'{name}:{x0},{y0}']=[[v if x0<=x<x0+w and y0<=y<y0+w else 0 for x,v in enumerate(row)] for y,row in enumerate(delta)]
    return scene,local,states,start


def case(n,k,stroke,protected=False,rpm=850,lead=3):
    scene,local,states,start=workloads(n,stroke,protected)
    kw=dict(rpm=rpm,lead=lead)
    prep=d.schedule(start,k,stroke,**kw)['seconds']
    initial={name:d.h.a.r.delta(start,h) for name,h in states.items()}
    return dict(n=n,k=k,stroke=stroke,protected=protected,rpm=rpm,lead=lead,
                local=d.summary(local,k,stroke,**kw),scene=d.summary(scene,k,stroke,**kw),
                neutral_s=prep,minimum_rest_first_s=d.summary(states,k,stroke,**kw)['max_s'],
                paid_neutral_first_s=prep+d.summary(initial,k,stroke,**kw)['max_s'],
                dense_s=d.schedule(s.flat(n,stroke),k,stroke,**kw)['seconds'])


def checks():
    assert clipped_area([(0,0),(2,0),(2,2),(0,2)],(1,1,3,3))==1
    assert clipped_area([(0,0),(2,0),(2,2),(0,2)],(2,0,3,2))==0
    assert all(clipped_area(poly,CORRIDOR)==0 for _,_,poly in s.SOURCE[0]['features'])
    assert math.isclose((CORRIDOR[2]-CORRIDOR[0])*s.WIDTH/560,25.4)
    for n in (32,64,80):
        g=geometry(n); gp=geometry(n,True)
        assert g['guide_fits_nominal']
        assert g['caps_overlap']==(n==32)
        assert math.isclose(g['opposite_yaw_max_separating_gap_mm'],
                            s.WIDTH/n*math.cos(math.radians(3))-(s.WIDTH/n-.4)/2*(1+math.cos(math.radians(6))+math.sin(math.radians(6))))
        assert d.envelope(n,4)['conflicts']==0
        maps,labs,_=terrain(n);fixed,flabs,changed=terrain(n,True)
        assert maps['road']==fixed['road'] and maps['ravine']==fixed['ravine']
        # Only ground clearing; never count a deleted obstruction as a preserved wall.
        assert all(fixed['ruins'][y][x]==0 for x,y in changed)
        scene,local,states,start=workloads(n,50,False)
        for delta in (s.flat(n),s.flat(n,50),next(iter(scene.values()))):
            seen={}
            for _,_,items in d.stations(delta,4):
                for x,y,v in items:
                    assert (x,y) not in seen;seen[x,y]=v
            assert seen=={(x,y):v for y,row in enumerate(delta) for x,v in enumerate(row) if v}
        # Dense station/work closed form; does not reproduce routing implementation.
        dense=d.schedule(s.flat(n,50),4,50)
        assert dense['stations']==n*n/4
        assert math.isclose(dense['spin_s'],n*n/4*d.h.a.r.spin(50/3,850))
        assert dense['seconds']>=dense['transaction_lower_s']
        if n in (64,80):
            assert scene==d.h.a.workloads(n) or sorted(map(str,scene.values()))==sorted(map(str,d.h.a.workloads(n).values()))
    return {'checks':'polygon clipping, source-clear corridor, finite opposite-yaw SAT and independent identity, unchanged relief, exact cell replay, dense counts/work, inherited scene equivalence'}


def figure(path):
    # Static export, geometry only; not a physical rendering or user preference test.
    colors={'ground':'#eee5cb','wall':'#584f47','rubble':'#ac9271'}
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1330" height="1070" viewBox="0 0 1330 1070">',
         '<rect width="100%" height="100%" fill="white"/>','<style>text{font-family:sans-serif;fill:#222}</style>',
         '<text x="20" y="25" font-size="20">Same ruin: finer walls versus fewer threaded columns</text>']
    for col,n in enumerate((80,64,32)):
        for row,protect in enumerate((False,True)):
            _,labs,_=terrain(n,protect);ox,oy=20+col*440,90+row*470;p=s.WIDTH/n
            svg.append(f'<text x="{ox}" y="{oy-35}" font-size="18">{n} × {n} / {p:g} mm / {n*n} columns</text>')
            svg.append(f'<text x="{ox}" y="{oy-13}" font-size="14">'+('Protected 25.4-mm corridor' if protect else 'Inherited connected wall conversion')+'</text>')
            clip=f'crop-{col}-{row}'
            svg.append(f'<defs><clipPath id="{clip}"><rect x="{ox}" y="{oy}" width="406.4" height="406.4"/></clipPath></defs><g clip-path="url(#{clip})">')
            for y,rr in enumerate(labs['ruins']):
                for x,c in enumerate(rr):
                    svg.append(f'<rect x="{ox+x*p:.3f}" y="{oy+y*p:.3f}" width="{p:.3f}" height="{p:.3f}" fill="{colors[c]}"/>')
            x0,y0,w,h=s.SOURCE[0]['crop']
            for _,_,poly in s.SOURCE[0]['features']:
                pts=' '.join(f'{ox+(x-x0)*s.WIDTH/w:.3f},{oy+(y-y0)*s.WIDTH/h:.3f}' for x,y in poly)
                svg.append(f'<polygon points="{pts}" fill="none" stroke="#222" stroke-width=".5"/>')
            for i in range(17):
                z=i*25.4
                svg.append(f'<path d="M{ox+z},{oy} v406.4 M{ox},{oy+z} h406.4" stroke="white" opacity=".5" stroke-width=".6"/>')
            a,b,c,e=CORRIDOR
            svg.append(f'<rect x="{ox+(a-x0)*s.WIDTH/w}" y="{oy+(b-y0)*s.WIDTH/h}" width="{(c-a)*s.WIDTH/w}" height="{(e-b)*s.WIDTH/h}" fill="none" stroke="#f02d9a" stroke-width="2"/>')
            svg.append('</g>')
    for i,line in enumerate(['Black outlines: retained source annotations after Ross McConnell / 2-Minute Tabletop. White grid: 25.4-mm game squares.',
        'Pink: proposed clear swept corridor through the known southern opening. Lower row clears every intersected cell.',
        'Coarse walls merge and openings broaden or close. Protecting this one passage does not validate all routes or gameplay.',
        'Geometry only. No measured miniature stability, hardware qualification, print job or selected pitch.']):
        svg.append(f'<text x="20" y="{1000+i*18}" font-size="13">{line}</text>')
    path.write_text('\n'.join(svg+['</svg>']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--figure',type=Path);args=p.parse_args()
    check=checks()
    if args.figure:figure(args.figure)
    if args.check:print(json.dumps(check))
    else:
        print(json.dumps(dict(verification=check,geometry=[geometry(n,protect) for n,protect in itertools.product((32,64,80),(False,True))],
            rows=[case(n,k,stroke) for n,k,stroke in itertools.product((32,64,80),(1,4,8),(40,50))],
            protected=[case(32,k,stroke,True) for k,stroke in itertools.product((4,8),(40,50))],
            sensitivity=[case(32,4,50,True,rpm,lead) for rpm,lead in ((400,3),(850,2))],
            costs=[dict(n=n,k=k,**d.cost(n,k)) for n,k in itertools.product((32,64,80),(1,4,8))]),indent=2))
