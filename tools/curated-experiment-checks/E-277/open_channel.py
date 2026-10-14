#!/usr/bin/env python3
"""E-277 open-channel/intact-nut discriminator; computation, not hardware proof.

Same dependencies, pinned BOSL2 and comparison slicer profile as slicing.py.
All generated geometry/toolpaths/results go in the supplied scratch directory.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
import trimesh
import manifold3d as md
import slicing as base
from split import solid, mesh, analyze

ROOT = Path(__file__).resolve().parent


def section():
    # Disjoint rectangles (xmin,xmax,ymin,ymax), world coordinates.
    rectangles = [(4.35, 5.15, -5.15, 5.15),
                  (-5.15, 4.35, -5.15, -4.35),
                  (-5.15, 4.35, 4.35, 5.15)]
    areas = [(b-a)*(d-c) for a,b,c,d in rectangles]
    centers = [((a+b)/2, (c+d)/2) for a,b,c,d in rectangles]
    area = sum(areas)
    cx = sum(a*c[0] for a,c in zip(areas,centers))/area
    ix = sum(a*((d-c)**2/12+y*y) for a,(_,y),(_,_,c,d)
             in zip(areas,centers,rectangles))
    iy = sum(a*((b-c)**2/12+(x-cx)**2) for a,(x,_),(c,b,_,_)
             in zip(areas,centers,rectangles))
    assert abs(area-23.44)<1e-10
    assert abs(cx-6.96*4.75/area)<1e-10
    # Independent 2x2 Gauss area quadrature recovers force and moment exactly
    # for this affine stress field; avoids midpoint discretization error.
    quad=[]
    for a,b,c,d in rectangles:
        nodes=np.array([-1,1])/math.sqrt(3)
        xx,yy=np.meshgrid((a+b)/2+nodes*(b-a)/2,
                         (c+d)/2+nodes*(d-c)/2)
        quad.append((xx.ravel(), yy.ravel(), (b-a)*(d-c)/4))
    extrema={}
    for ex,ey in [(0,0),(-5.15,0),(5.15,0),(0,5.15)]:
        f=.2
        def pressure(x,y):
            return f/area+f*(ex-cx)*(x-cx)/iy+f*ey*y/ix
        values=[pressure(x,y) for a,b,c,d in rectangles for x in [a,b] for y in [c,d]]
        integrated=sum(float(np.sum(pressure(x,y)))*da for x,y,da in quad)
        mx=sum(float(np.sum(pressure(x,y)*x))*da for x,y,da in quad)
        my=sum(float(np.sum(pressure(x,y)*y))*da for x,y,da in quad)
        assert abs(integrated-f)<1e-8
        assert abs(mx-f*ex)<1e-10 and abs(my-f*ey)<1e-10
        extrema[f'{ex},{ey}']=[min(values),max(values)]
    # Thin-wall Saint-Venant surrogates, free warping, not FDM/contact properties.
    # J_open = sum(b*t^3)/3; closed square Bredt J = t*(w-t)^3.
    # Source: https://mechanics.ju.se/SolidMechanics/Torsion.html
    jo=(10.3+2*9.5)*.8**3/3
    jc=.8*9.5**3
    # Loaded torque .1/1/5 Nmm; effective shear modulus 200/1000 MPa;
    # torque span 4/54 mm are labelled scenarios, not measured distributions.
    twist=[dict(torque_Nmm=t,span_mm=l,G_MPa=g,
                open_deg=math.degrees(t*l/g/jo),
                closed_deg=math.degrees(t*l/g/jc))
           for t in [.1,1,5] for l in [4,54] for g in [200,1000]]
    return dict(area_mm2=area,centroid_x_mm=cx,Ix_mm4=ix,Iy_mm4=iy,
                joint_pressure_MPa_at_point2N=extrema,
                J_open_mm4=jo,J_closed_mm4=jc,stiffness_ratio=jc/jo,
                twist_scenarios=twist)


def ledger():
    return {str(n):dict(channel_bodies=n,intact_nuts=n,screws=n,
                       column_joins=n,paired_thread_joins=0,guide_apertures=2*n,
                       # Conservative separated packing, not an optimized plate.
                       channel_plates_24_up=math.ceil(n/24),
                       nut_plates_289_up=math.ceil(n/289),
                       handling_join_plate_hours=[3*n*t/3600+
                           (math.ceil(n/24)+math.ceil(n/289))*5/60
                           for t in [10,30]],
                       extra_minute_per_join_hours=n/60,
                       total_with_E276_base_hours=([3*n*t/3600+
                           (math.ceil(n/24)+math.ceil(n/289))*5/60+b
                           for t,b in [(10,10.94),(30,23.69)]] if n==1024 else None))
            for n in [1024,4096,6400]}


def core_draw(folder):
    # Undo horizontal print placement to original column coordinates.
    channel=solid(trimesh.load(folder/'channel.stl',force='mesh'))
    channel=channel.translate([10,-5.15,-5.15]).rotate([0,-90,0])
    core=md.Manifold.cube([9.5,8.7,124]).translate([-5.15,-4.35,10])
    overlaps={str(x):abs((core.translate([-x,0,0]) ^ channel).volume())
              for x in [0,.1,1,5,9.5,10]}
    assert max(overlaps.values())<.001
    return overlaps


def plot(folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    fig,axes=plt.subplots(1,3,figsize=(14,5))
    nut=base.paths(folder/'nut_support.gcode')
    levels=sorted({p[4] for p in nut if p[5]=='Support material interface'})
    z=max(levels,key=lambda z:sum(p[4]==z and p[5]=='Support material interface'
                                for p in nut))
    for ax,(case,level,title) in zip(axes,[
            ('channel_auto',5.2,'Open channel: mid-height slice'),
            ('nut_auto',z,'Intact nut: support disabled'),
            ('nut_support',z,'Same nut: support enabled')]):
        paths=[p for p in base.paths(folder/(case+'.gcode')) if abs(p[4]-level)<1e-5]
        for role in sorted({p[5] for p in paths}):
            group=[p for p in paths if p[5]==role]
            color=('#9342b5' if role.startswith('Support') else
                   '#d33d35' if role=='Overhang perimeter' else '#236782')
            ax.add_collection(LineCollection([[(p[0],p[1]),(p[2],p[3])] for p in group],
                                             colors=color,linewidths=.7,label=role))
        ax.autoscale(); ax.set_aspect('equal')
        ax.set_title(f'{title}\nZ={level:g} mm'); ax.set_xlabel('Bed X, mm')
        ax.set_ylabel('Bed Y, mm')
    fig.suptitle('E-277: actual PrusaSlicer 2.7.2 paths for three identical components\n'
                 'Blue: ordinary extrusion; red: overhang; purple: bore support. No physical print proof.')
    fig.tight_layout(); fig.savefig(folder/'open-channel-paths.png',dpi=170); plt.close(fig)


def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--slicer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    cases=[('channel_auto','channel',[]),
           ('channel_support','channel',['--support-material']),
           ('nut_auto','nut',[]),('nut_support','nut',['--support-material'])]
    if not a.analyze_only:
        assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==base.REV
        assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
        env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
        solids={}
        for part,dims in [('channel',[126,10.3,10.3]),('nut',[10.3,10.3,10])]:
            file=a.output/(part+'.stl')
            base.run(['openscad','-o',file,'-D',f'part="{part}"',ROOT/'open_channel.scad'],env)
            s=solid(trimesh.load(file,force='mesh')); m=mesh(s)
            assert np.allclose(m.extents,dims,atol=2e-5)
            assert np.allclose(m.bounds[0],0,atol=2e-5)
            solids[part]=s
            if part=='channel':
                assert abs(s.volume()-(124*23.44+2*10.3**2))<.01
                # Every corner remains in the section convex hull, preserving
                # the rigid square's support function (not elastic stiffness).
                points=np.asarray([[-5.15,-5.15],[5.15,-5.15],
                                   [5.15,5.15],[-5.15,5.15]])
                for angle in np.linspace(0,2*math.pi,361):
                    u=np.array([math.cos(angle),math.sin(angle)])
                    assert abs(max(points@u)-5.15*sum(abs(u)))<1e-10
            copies=[]
            for i in range(3):
                c=m.copy(); c.apply_translation([10,10+13.3*i,0]); copies.append(c)
            plate=trimesh.util.concatenate(copies)
            # Individual meshes already checked; concat should have 3 shells.
            packed=md.Manifold(md.Mesh(np.asarray(plate.vertices,dtype=np.float32),
                                       np.asarray(plate.faces,dtype=np.uint32)))
            assert packed.status()==md.Error.NoError and len(packed.decompose())==3
            plate.export(a.output/(part+'-three.stl'))
        geometry={p:s.volume() for p,s in solids.items()}
        assert abs(sum(geometry.values())-(4983.871-124*6.96))<.01
        (a.output/'geometry.json').write_text(json.dumps(geometry,indent=2))
        for case,part,flags in cases:
            base.run([a.slicer,'--load',ROOT/'slicing.ini','--threads','2',
                      '--export-gcode','--output',a.output/(case+'.gcode'),
                      *flags,a.output/(part+'-three.stl')])
            print(case,flush=True)
    results={name:analyze(a.output/(name+'.gcode')) for name,_,_ in cases}
    # Main decision: channel needs no bridge, overhang or support, even enabled.
    for name in ['channel_auto','channel_support']:
        assert not any(r in results[name]['roles']
                       for r in ['Bridge infill','Overhang perimeter',
                                 'Support material','Support material interface'])
    report=dict(geometry_mm3=json.loads((a.output/'geometry.json').read_text()),
                section=section(),ledger=ledger(),slices=results,
                side_core_draw_overlap_mm3=core_draw(a.output),
                provenance=dict(bosl2=base.REV,slicer=base.run([a.slicer,'--help']).splitlines()[0],
                    sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in [ROOT/'open_channel.py',ROOT/'open_channel.scad',
                                      ROOT/'slicing.scad',ROOT/'slicing.ini',
                                      ROOT.parent/'E-263'/'article.scad']}))
    (a.output/'summary.json').write_text(json.dumps(report,indent=2))
    plot(a.output)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
