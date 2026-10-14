#!/usr/bin/env python3
"""Actual three-screw deposition comparison; no physical process qualification.

Reuses E-277's pinned paired thread and slicer comparison profile. All exports
and G-code go to --output, never the owner-print queue. No fit/angle sweep.
"""
import argparse
import json
import math
import os
from pathlib import Path
import re
import sys

import manifold3d as md
import numpy as np
import trimesh
ROOT = Path(__file__).resolve().parent.parent / "E-277"
sys.path.insert(0,str(ROOT))
import slicing as base
from split import solid, mesh, analyze
from open_channel import ledger as column_ledger

CASES = [(angle, pose, support) for angle in [30,90]
         for pose in ['horizontal','upright'] for support in [False,True]] + [(90,'horizontal','raft')]

def case_name(angle,pose,support):
    return f'a{angle}-{pose}-'+('raft' if support=='raft' else f's{int(support)}')


def seconds(footer):
    text = next(s for s in footer if 'estimated printing time (normal mode)' in s)
    return sum(float(v)*{'d':86400,'h':3600,'m':60,'s':1}[u]
               for v,u in re.findall(r'(\d+(?:\.\d+)?)\s*([dhms])',text))


def metrics(path,pose):
    r=analyze(path)
    pp=base.paths(path)
    # --dont-arrange preserves specified bed coordinates. Horizontal axes are X;
    # each identical screw is 10..74 mm long, with Y=15,25,35. Upright X=15,25,35.
    part_paths=[p for p in pp if not p[5].startswith('Support')]
    assert min(min(p[0],p[2]) for p in part_paths)>9
    assert max(max(p[0],p[2]) for p in part_paths)<75
    if pose=='horizontal':
        # Role segments are NOT physical support contacts. Report deposited
        # interface footprint in 1-mm axial bins underneath the thread envelope.
        region=[p for p in pp if p[5]=='Support material interface'
                and 10 <= (p[0]+p[2])/2 <=74
                and min(abs((p[1]+p[3])/2-c) for c in [15,25,35])<=1.8
                ]
        bins=sorted({min(63,max(0,int((p[0]+p[2])/2-10))) for p in region})
        r['interface_under_screw'] = dict(segments=len(region),axial_1mm_bins=bins)
        r['interface_under_each_screw'] = []
        for center in [15,25,35]:
            local=[p for p in region if abs((p[1]+p[3])/2-center)<=1.8]
            r['interface_under_each_screw'].append(dict(
                center_y_mm=center, segments=len(local),
                axial_1mm_bins=sorted({min(63,max(0,int((p[0]+p[2])/2-10)))
                                      for p in local})))
        assert sum(p['segments'] for p in r['interface_under_each_screw'])==len(region)
    first=[p for p in pp if abs(p[4]-.2)<1e-5 and not p[5].startswith('Support')]
    r['first_layer_part_path_length_mm']=sum(math.hypot(p[2]-p[0],p[3]-p[1]) for p in first)
    r['first_layer_support_gap_crossings']=sum(
        1 for p in pp if p[5].startswith('Support') and abs(p[4]-.2)<1e-5
        and min(p[1],p[3])<=16.6 and max(p[1],p[3])>=23.4)
    r['seconds']=seconds(r['footer'])
    r['filament_cm3']=float(next(s.split('=')[1] for s in r['footer'] if '[cm3]' in s))
    return r


def plot(folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    fig,axes=plt.subplots(2,2,figsize=(12,7))
    for ax,(pose,support,z) in zip(axes.flat,[('horizontal',False,.2),
            ('horizontal',True,.8),('horizontal','raft',.2),('upright',True,32)]):
        pp=[p for p in base.paths(folder/(case_name(90,pose,support)+'.gcode'))
            if abs(p[4]-z)<.025]
        for role in sorted({p[5] for p in pp}):
            group=[p for p in pp if p[5]==role]
            color={'Support material interface':'#9643a3',
                   'Support material':'#c68bdd','Overhang perimeter':'#de3838',
                   'Bridge infill':'#e89a20'}.get(role,'#256087')
            ax.add_collection(LineCollection([[(p[0],p[1]),(p[2],p[3])] for p in group],
                colors=color,linewidths=1,label=role))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(f'{pose}, support {support}, Z={z} mm')
        ax.set_xlabel('Bed X, mm');ax.set_ylabel('Bed Y, mm')
        if support=='raft':ax.set(xlim=(0,84),ylim=(5,45))
        elif pose=='horizontal':ax.set(xlim=(9,75),ylim=(12.5,17.5))
        else:ax.set(xlim=(12.5,17.5),ylim=(12.5,17.5))
        ax.legend(fontsize=7)
    fig.suptitle('E-279: actual 90° screw paths; raft panel shows all three copies\n'
                 'Computational comparison only; support labels do not qualify print or removal')
    fig.tight_layout();fig.savefig(folder/'screw-paths.png',dpi=160);plt.close(fig)


def ledger(slices):
    # Channel and 90-degree nut: existing actual three-component E-277 slices.
    pair_without_screw_s=4057+1571
    pair_without_screw_cm3=9.41+3.14
    columns=column_ledger()
    return {name:{str(n):dict(
        screw_hours=r['seconds']*n/3/3600,
        whole_pair_hours=(pair_without_screw_s+r['seconds'])*n/3/3600,
        whole_pair_liters=(pair_without_screw_cm3+r['filament_cm3'])*n/3/1000,
        column_components_and_handling=columns[str(n)],
        # Deposition proxy, not adhesion points or physical release operations.
        support_interface_segments_three_copy_repetition=
            r['roles'].get('Support material interface',{}).get('segments',0)*n/3,
        screws_exposed_to_thread_support=n if
            r.get('interface_under_screw',{}).get('segments',0)>0 else 0,
        individual_screw_release_inspection_duties=n,
        assumed_16_screw_groups=math.ceil(n/16),
        additional_cleanup_hours=[n*s/3600 for s in [10,30,60]],
        group_release_hours_at_30s_per_16=math.ceil(n/16)*30/3600)
        for n in [1024,4096,6400]}
        for name,r in slices.items() if name.startswith('a90')}


def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--slicer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    if not a.analyze_only:
        assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==base.REV
        assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
        env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
        geo={}
        for angle in [30,90]:
            p=a.output/f'male-{angle}.stl'
            base.run(['openscad','-o',p,'-D','part="male"','-D',f'angle={angle}',
                      ROOT/'thread_profile.scad'],env)
            m=mesh(solid(trimesh.load(p,force='mesh')))
            assert np.allclose(m.extents,[3.2,3.2,64],atol=2e-5)
            geo[str(angle)]=dict(volume_mm3=float(m.volume),extent_mm=m.extents.tolist())
            for pose in ['horizontal','upright']:
                parts=[]
                for i in range(3):
                    copy=m.copy()
                    if pose=='horizontal':
                        copy.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
                        copy.apply_translation([10,15+10*i,1.6])
                    else:copy.apply_translation([15+10*i,15,0])
                    assert abs(copy.bounds[0,2])<2e-5
                    parts.append(copy)
                plate=trimesh.util.concatenate(parts)
                compound=md.Manifold(md.Mesh(np.asarray(plate.vertices,dtype=np.float32),
                                            np.asarray(plate.faces,dtype=np.uint32)))
                assert len(compound.decompose())==3 and plate.is_watertight
                assert abs(plate.volume-3*m.volume)<.001
                plate.export(a.output/f'{angle}-{pose}.stl')
        (a.output/'geometry.json').write_text(json.dumps(geo,indent=2))
        for angle,pose,support in CASES:
            name=case_name(angle,pose,support)
            base.run([a.slicer,'--load',ROOT/'slicing.ini','--threads','2',
                      '--dont-arrange','--export-gcode','--output',a.output/f'{name}.gcode',
                      *(['--support-material'] if support else []),
                      *(['--raft-layers','3','--raft-expansion','4'] if support=='raft' else []),
                      a.output/f'{angle}-{pose}.stl'])
            print(name,flush=True)
    slices={case_name(angle,pose,support):metrics(
        a.output/(case_name(angle,pose,support)+'.gcode'),pose)
        for angle,pose,support in CASES}
    # Discriminating witnesses; extrusion accounting is independently checked
    # against slicer footer by analyze(), geometry by manifold + dimensions.
    for name in ['a90-upright-s0','a90-upright-s1']:
        assert not {'Overhang perimeter','Bridge infill','Support material',
                    'Support material interface'} & slices[name]['roles'].keys()
    # No support paths is the witness, not identical travel/time estimates:
    # repeated slicing gave 640..650 s while all deposited roles stayed equal.
    assert slices['a90-upright-s0']['filament_cm3']==slices['a90-upright-s1']['filament_cm3']
    assert slices['a30-upright-s1']['roles']['Support material interface']['segments']>0
    for angle in [30,90]:
        r=slices[f'a{angle}-horizontal-s1']
        assert len(r['interface_under_screw']['axial_1mm_bins'])==64
        assert all(len(p['axial_1mm_bins'])==64 for p in r['interface_under_each_screw'])
    assert slices['a90-horizontal-raft']['first_layer_support_gap_crossings']>0
    assert slices['a90-horizontal-s1']['first_layer_support_gap_crossings']==0
    assert slices['a90-horizontal-raft']['seconds']>slices['a90-horizontal-s1']['seconds']
    # Assembly-free end bracing cannot stabilize earlier deposited layers:
    # the top tie only joins after the full slender span has already been built.
    # Euler cantilever is only a comparative stiffness bound, not nozzle force.
    Icore=math.pi*1.4**4/64
    Iouter=math.pi*3.2**4/64
    compliance={str(E):[64**3/(3*E*I) for I in [Iouter,Icore]] for E in [1000,3000]}
    assert Iouter>Icore>0
    result=dict(geometry=json.loads((a.output/'geometry.json').read_text()),
                slices=slices,ledger=ledger(slices),
                upright_tip_compliance_mm_per_N_bounded_by_solid_cylinders= compliance)
    (a.output/'result.json').write_text(json.dumps(result,indent=2))
    for name,r in slices.items():
        print(name,json.dumps({k:v for k,v in r.items() if k!='roles'}))
        print('roles', {k:v['segments'] for k,v in r['roles'].items()})
    print('ledger',json.dumps(result['ledger']))
    print('compliance',compliance)
    plot(a.output)

if __name__=='__main__':main()
