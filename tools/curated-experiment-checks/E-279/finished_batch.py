#!/usr/bin/env python3
"""Slice E-280's existing finished screw; no geometry tuning or print handoff.

Same pinned dependencies/profile as screw_batch.py. Outputs are scratch only.
"""
import argparse
import json
import math
import os
from pathlib import Path

import manifold3d as md
import numpy as np
import trimesh
import screw_batch as bare

base = bare.base
HERE = Path(__file__).resolve().parent
CASES = [(pose, support) for pose in ('upright', 'horizontal')
         for support in (False, True)]


def inspect(path, pose):
    r = bare.analyze(path)
    pp = base.paths(path)
    r['seconds'] = bare.seconds(r['footer'])
    r['filament_cm3'] = float(next(s.split('=')[1] for s in r['footer'] if '[cm3]' in s))
    # Horizontal screw axis: local z = bed x - 20. Upright: local z = bed z - 10.
    # Midpoint regions are deposition witnesses, NOT adhesion or contact counts.
    regions = {'socket_axial_envelope': (-10, -8), 'driver_collar': (-10, -4),
               'lower_journal': (-4, 0), 'thread': (0, 64), 'upper_journal': (64, 68)}
    r['feature_roles'] = {}
    for name, (lo, hi) in regions.items():
        group = [p for p in pp if lo <= ((p[0]+p[2])/2-20 if pose == 'horizontal'
                                       else p[4]-10) < hi]
        r['feature_roles'][name] = {role: sum(p[5] == role for p in group)
                                   for role in sorted({p[5] for p in group})}
    first = [p for p in pp if p[4] < .201 and not p[5].startswith('Support')]
    r['first_layer_part_x_range_mm'] = [min(min(p[0], p[2]) for p in first),
                                          max(max(p[0], p[2]) for p in first)]
    if pose == 'horizontal':
        r['thread_interface_1mm_bins_per_screw'] = []
        for y in (15, 25, 35):
            bins = {int((p[0]+p[2])/2-20) for p in pp
                    if p[5] == 'Support material interface'
                    and 20 <= (p[0]+p[2])/2 < 84
                    and abs((p[1]+p[3])/2-y) <= 1.8}
            r['thread_interface_1mm_bins_per_screw'].append(sorted(bins))
        r['interface_under_screw'] = dict(segments=sum(
            p[5] == 'Support material interface' and 20 <= (p[0]+p[2])/2 < 84
            and min(abs((p[1]+p[3])/2-y) for y in (15,25,35)) <= 1.8 for p in pp))
    return r


def plot(folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, (pose, z) in zip(axes, [('upright', 1.6), ('upright', 2.2), ('horizontal', .8)]):
        pp = [p for p in base.paths(folder/f'{pose}-s1.gcode') if abs(p[4]-z)<.01]
        for role in sorted({p[5] for p in pp}):
            group = [p for p in pp if p[5] == role]
            ax.add_collection(LineCollection([[(p[0],p[1]),(p[2],p[3])] for p in group],
                colors={'Support material interface':'purple','Support material':'pink',
                        'Bridge infill':'orange','Overhang perimeter':'red'}.get(role,'steelblue'),
                linewidths=1, label=role))
        ax.autoscale(); ax.set_aspect('equal'); ax.set_title(f'{pose}, Z={z} mm')
        ax.legend(fontsize=6)
    fig.suptitle('E-279 finished screw: actual paths, support enabled; no physical qualification')
    fig.tight_layout(); fig.savefig(folder/'finished-paths.png',dpi=150); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--slicer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a = ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    if not a.analyze_only:
        assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip() == base.REV
        assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
        env = dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
        model = a.output/'finished.stl'
        base.run(['openscad','-o',model,'-D','angle=90','-D','$fn=128',
                  HERE.parent/'E-280/release.scad'],env)
        m = bare.mesh(bare.solid(trimesh.load(model,force='mesh')))
        assert np.allclose(m.extents,[4.4,4.4,78],atol=2e-5)
        assert abs(m.volume-405.703)<.01
        (a.output/'geometry.json').write_text(json.dumps(dict(volume_mm3=m.volume,
            extents_mm=m.extents.tolist(),bounds_mm=m.bounds.tolist()),indent=2))
        for pose in ('upright','horizontal'):
            parts = []
            for i in range(3):
                cp = m.copy()
                if pose == 'horizontal':
                    cp.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
                    cp.apply_translation([20,15+10*i,2.2])
                else:
                    cp.apply_translation([15+10*i,15,10])
                assert abs(cp.bounds[0,2])<2e-5
                parts.append(cp)
            plate = trimesh.util.concatenate(parts)
            s = md.Manifold(md.Mesh(np.asarray(plate.vertices,dtype=np.float32),
                                    np.asarray(plate.faces,dtype=np.uint32)))
            assert s.status()==md.Error.NoError and len(s.decompose())==3
            assert plate.is_watertight and abs(plate.volume-3*m.volume)<.001
            plate.export(a.output/f'{pose}.stl')
        for pose, support in CASES:
            name = f'{pose}-s{int(support)}'
            base.run([a.slicer,'--load',bare.ROOT/'slicing.ini','--threads','2','--dont-arrange',
                '--export-gcode','--output',a.output/f'{name}.gcode',
                *(['--support-material'] if support else []),a.output/f'{pose}.stl'])
            print(name,flush=True)
    slices = {f'{pose}-s{int(support)}':inspect(a.output/f'{pose}-s{int(support)}.gcode',pose)
              for pose,support in CASES}
    # Physical distinctions the bare-shank comparison cannot represent.
    for pose in ('upright','horizontal'):
        assert not any(role.startswith('Support') for role in slices[f'{pose}-s0']['roles'])
        assert slices[f'{pose}-s1']['filament_cm3'] > slices[f'{pose}-s0']['filament_cm3']
    for support in (0,1):
        upright = slices[f'upright-s{support}']
        assert upright['roles']['Bridge infill']['z_mm'] == [2.2]  # socket roof
        assert not any(role.startswith('Support') for role in upright['feature_roles']['thread'])
    assert slices['upright-s1']['feature_roles']['socket_axial_envelope']['Support material interface'] > 0
    assert slices['upright-s1']['feature_roles']['lower_journal']['Support material interface'] > 0
    assert all(len(bins)==64 for bins in slices['horizontal-s1']['thread_interface_1mm_bins_per_screw'])
    assert slices['horizontal-s0']['first_layer_part_x_range_mm'][1] < 16  # head only
    ledger = bare.ledger({'a90-'+k:v for k,v in slices.items()})
    result = dict(geometry=json.loads((a.output/'geometry.json').read_text()),
                  slices=slices,ledger=ledger)
    (a.output/'result.json').write_text(json.dumps(result,indent=2))
    for name,r in slices.items():
        print(name,json.dumps({k:v for k,v in r.items() if k not in ('roles','footer')}))
        print('roles', {k:v['segments'] for k,v in r['roles'].items()})
    plot(a.output)


if __name__=='__main__':
    main()
