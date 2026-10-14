#!/usr/bin/env python3
"""Integral upright body comparison. Pinned dependencies/profile from slicing.py.

Requires numpy, trimesh, manifold3d; generated outputs are scratch only.
Four actual slices distinguish roof bridges from internal-thread supports.
No physical print stability, fit or load qualification.
"""
import argparse
import json
import math
import os
from pathlib import Path
import re

import numpy as np
import trimesh
import slicing as base
from split import solid, mesh
from open_channel import section

ROOT = Path(__file__).resolve().parent


def check(report):
    assert abs(report['closed']['solid_mm3']-report['open']['solid_mm3']-124*6.96)<.02
    for shape in ['closed','open']:
        r=report[shape]['slices']['False']
        assert r['thread_nonordinary_segments']==0
        assert r['roles']['Bridge infill']['z_min']==134.2
        assert r['roles']['Bridge infill']['max_segment_mm']<9
        if shape=='closed':
            assert 'Overhang perimeter' not in r['roles']
        else:
            assert r['roles']['Overhang perimeter']['z_min']==134.2
        assert report[shape]['slices']['True']['roles']['Support material']['segments']>10000


def inspect(path):
    pp = base.paths(path)
    roles = {}
    for role in sorted({p[5] for p in pp}):
        group = [p for p in pp if p[5] == role]
        roles[role] = dict(segments=len(group),
            z_min=min(p[4] for p in group), z_max=max(p[4] for p in group),
            max_segment_mm=max(math.hypot(p[2]-p[0],p[3]-p[1]) for p in group))
    footer = [s for s in path.read_text().splitlines()
              if re.match(r'; (filament used|estimated printing time)',s)]
    times = next(s for s in footer if 'estimated printing time (normal mode)' in s)
    seconds = sum(float(v)*{'d':86400,'h':3600,'m':60,'s':1}[u]
                  for v,u in re.findall(r'(\d+(?:\.\d+)?)\s*([dhms])',times))
    cm3 = float(next(s.split('=')[1] for s in footer if '[cm3]' in s))
    assert abs(sum(p[6] for p in pp)*math.pi*1.75**2/4000-cm3)<.02
    # Three known body centres: check actual extrusion at both bottom and roof.
    for cy in [15,30,45]:
        for z in [.2,136]:
            assert any(abs(p[4]-z)<.001 and abs((p[1]+p[3])/2-cy)<5.2
                       and not p[5].startswith('Support') for p in pp)
    return dict(roles=roles,seconds=seconds,filament_cm3=cm3,
        repeated_1024_hours=seconds*1024/3/3600,
        repeated_1024_litres=cm3*1024/3/1000,
        thread_nonordinary_segments=sum(p[4]<10 and p[5] in
            ['Bridge infill','Overhang perimeter','Support material','Support material interface']
            for p in pp),footer=footer)


def main():
    ap=argparse.ArgumentParser(__doc__)
    for key in ['bosl2','slicer','output']:
        ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    if a.analyze_only:
        report=json.loads((a.output/'result.json').read_text())
        for shape in ['closed','open']:
            for support in [False,True]:
                assert report[shape]['slices'][str(support)]==inspect(
                    a.output/(shape+'-s'+str(int(support))+'.gcode'))
        check(report)
        print('Four slices, extrusion accounting and decision witnesses checked.')
        return
    assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==base.REV
    assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
    report={}
    for shape in ['closed','open']:
        path=a.output/(shape+'.stl')
        base.run(['openscad','-o',path,'-D','angle=90','-D',f'open_side={str(shape=="open").lower()}',
                  ROOT/'upright.scad'],env)
        s=solid(trimesh.load(path,force='mesh')); m=mesh(s)
        assert np.allclose(m.extents,[10.3,10.3,136],atol=2e-5)
        # Independent sum of the previously checked 90-degree nut and prismatic body.
        expected=1003.949+124*(23.44 if shape=='open' else 30.4)+2*10.3**2
        assert abs(s.volume()-expected)<.01,(shape,s.volume(),expected)
        copies=[]
        for cy in [15,30,45]:
            c=m.copy(); c.apply_translation([15,cy,0]); copies.append(c)
        plate=a.output/(shape+'-three.stl')
        trimesh.util.concatenate(copies).export(plate)
        report[shape]=dict(solid_mm3=s.volume(),slices={})
        for support in [False,True]:
            name=shape+'-s'+str(int(support)); gcode=a.output/(name+'.gcode')
            base.run([a.slicer,'--load',ROOT/'slicing.ini','--threads','2','--dont-arrange',
                      '--export-gcode','--output',gcode,
                      *(['--support-material'] if support else []),plate])
            report[shape]['slices'][str(support)]=inspect(gcode)
            print(name,json.dumps(report[shape]['slices'][str(support)]),flush=True)
    check(report)
    # Equal-E ideal cantilever comparison, no assumed nozzle load or modulus.
    # Nominal full screw diameter is an upper stiffness bound for threaded shank.
    ix=(10.3**4-8.7**4)/12
    shank_i=math.pi*3.2**4/64
    report['ideal_tip_stiffness_relative_to_64mm_solid_3point2_shank']={
        'closed':ix/shank_i*(64/136)**3,
        'open_weak_axis':min(section()['Ix_mm4'],section()['Iy_mm4'])/shank_i*(64/136)**3}
    # No per-body joining. Assumed 289-up packing, not an actual batch slice.
    report['handling_scenarios']={str(n):dict(plates=math.ceil(n/289),
        body_removal_and_gauge_h=[2*n*t/3600+math.ceil(n/289)*5/60 for t in [10,30]],
        removed_joins=n, resident_parts=2*n) for n in [1024,4096,6400]}
    report['provenance']=dict(bosl2=base.REV,slicer=base.run([a.slicer,'--help']).splitlines()[0])
    (a.output/'result.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['closed','open']},indent=2))


if __name__=='__main__': main()
