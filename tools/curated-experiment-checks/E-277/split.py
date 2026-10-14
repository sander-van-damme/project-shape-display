#!/usr/bin/env python3
"""Split-column finite geometry, assembly sensitivity and actual slicing.

Same dependencies/profile/pinned BOSL2 as slicing.py. All outputs in --output.
No measured fit, bond strength, print yield or machine-ready G-code.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re

import manifold3d as md
import numpy as np
import trimesh
import slicing as baseline

ROOT = Path(__file__).resolve().parent


def solid(mesh):
    s = md.Manifold(md.Mesh(np.asarray(mesh.vertices, dtype=np.float32),
                           np.asarray(mesh.faces, dtype=np.uint32)))
    assert s.status() == md.Error.NoError and len(s.decompose()) == 1
    return s


def mesh(s):
    m = s.to_mesh()
    out = trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3],
                          np.asarray(m.tri_verts), process=True)
    assert out.is_watertight and out.is_winding_consistent
    return out


def overlap(a, b):
    return abs((a ^ b).volume())


def core_draw(a):
    # Isolate nine interior mm: no roof/end-wall obstruction in this test.
    box = md.Manifold.cube([5.15, 10.3, 9]).translate([0, -5.15, .5])
    core = box - a
    round_core = md.Manifold.cylinder(9, 1.75, 1.75, 64).translate([0, 0, .5]) ^ box
    smooth = box - round_core
    result = {str(t):overlap(core.translate([-t, 0, 0]), a)
              for t in [0, .02, .1, .5, 1, 2]}
    for t in [0, .02, .1, .5, 1, 2]:
        assert overlap(round_core.translate([-t, 0, 0]), smooth) < 1e-6
    assert result['0'] < 1e-6 and result['0.1'] > .1 and result['2'] < 1e-6
    return result


def assembly(solids):
    a = solids['positive'].translate([0, -5.15, -5.15]).rotate([0, -90, 0])
    b = solids['negative'].translate([0, -5.15, -5.15]).rotate([0, -90, 0]).rotate([0, 0, -180])
    reference = solids['integral'].translate([0, -5.15, -5.15]).rotate([0, -90, 0])
    # Allow sub-micrometre exported split-plane mismatch, not physical clearance.
    assert overlap(a, b) < 1e-4
    assert abs(a.volume() + b.volume() - reference.volume()) < .01
    assert (reference - (a + b)).volume() < .01
    assert ((a + b) - reference).volume() < .01
    male = solids['male'].translate([0, 0, -6])  # two full leads, interior engagement
    assert overlap(a + b, male) < 1e-5
    assert overlap((a+b).translate([0, 0, .2]), male.translate([0, 0, .2])) < 1e-5
    result = {}
    for delta in [0, .05, .08, .10, .20, .40]:
        shifted = a.translate([0, 0, delta / 2]) + b.translate([0, 0, -delta / 2])
        # One full lead at .05 mm plus .01 mm near alignment. Translation is
        # equivalent to screw phase here; end faces remain outside the nut.
        # A sampled search, not proof over continuous phase or deformation.
        samples = sorted({round(float(s), 8) for s in
                          np.r_[np.linspace(-1.5, 1.5, 61), np.linspace(-.3, .3, 61)]})
        trials = [(float(s), overlap(shifted, male.translate([0, 0, float(s)])))
                  for s in samples]
        best = min(trials, key=lambda pair: pair[1])
        result[str(delta)] = dict(best_axial_phase_mm=best[0], min_overlap_mm3=best[1],
                                 sampled_phases=len(samples))
    assert result['0']['min_overlap_mm3'] < 1e-5
    assert result['0.2']['min_overlap_mm3'] > 1e-4
    return dict(axial_phase_sensitivity=result, rigid_core_draw_overlap_mm3=core_draw(a))


def analyze(file):
    pp = baseline.paths(file)
    roles = {}
    for role in sorted({p[5] for p in pp}):
        group = [p for p in pp if p[5] == role]
        roles[role] = dict(segments=len(group),
            max_segment_mm=max(math.hypot(p[2]-p[0], p[3]-p[1]) for p in group),
            volume_cm3=sum(p[6] for p in group)*math.pi*1.75**2/4/1000,
            z_mm=sorted({round(p[4], 3) for p in group}))
    # All bodies start at X=10. Thread block X=10..20, cavity X=20..144.
    cavity_bridges = [p for p in pp if p[5] == 'Bridge infill'
                      and 21 < (p[0]+p[2])/2 < 143]
    text = file.read_text()
    footer = [s for s in text.splitlines()
              if re.match(r'; (filament used|estimated printing time)', s)]
    cm3 = float(next(s.split('=')[1] for s in footer if '[cm3]' in s))
    assert abs(sum(v['volume_cm3'] for v in roles.values())-cm3) < .015
    return dict(roles=roles, cavity_bridge_segments=len(cavity_bridges), footer=footer)


def ledger():
    # Labels: allocations, no measured joining/inspection cycle times.
    return {str(n): dict(shells=2*n, screws=n, joining_operations=n,
        longitudinal_seam_lines=2*n, paired_thread_registrations=n,
        plates_at_24_halves=math.ceil(2*n/24),
        join_hours=[n*t/3600 for t in [10, 30, 60]],
        additional_half_handling_hours=[n*t/3600 for t in [10, 30]],
        total_handling_join_plate_hours=[3*n*t/3600+math.ceil(2*n/24)*5/60 for t in [10, 30]],
        bond_liters_at_0_05mm_198_4mm2=n*.05*198.4/1e6)
        for n in [1024, 4096, 6400]}


def plot(folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))
    panels = [('split_auto', 4.8, (9, 21), (9, 34), 'Two complementary half-threads, Z4.8'),
              ('split_auto', 5.2, (9, 21), (9, 34), 'Open split faces, Z5.2'),
              ('integral_transverse', 9.8, (9, 146), (9, 34), 'Integral transverse roof, Z9.8')]
    for ax, (case, z, xb, yb, title) in zip(axes, panels):
        pp = [p for p in baseline.paths(folder/(case+'.gcode')) if abs(p[4]-z)<.01]
        for role in sorted({p[5] for p in pp}):
            selected = [p for p in pp if p[5] == role]
            lines = [[(p[0], p[1]), (p[2], p[3])] for p in selected]
            color = '#e38800' if role == 'Bridge infill' else '#246b87'
            ax.add_collection(LineCollection(lines, colors=color, linewidths=.6))
        ax.set(xlim=xb, ylim=yb, xlabel='Bed X, mm', ylabel='Bed Y, mm', title=title)
        ax.set_aspect('equal')
    fig.suptitle('E-277 actual slicer paths: blue ordinary extrusion; orange bridge\nComputational comparison, not a print-quality or fit qualification')
    fig.tight_layout(); fig.savefig(folder/'split-paths.png', dpi=160); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2', type=Path, required=True)
    ap.add_argument('--slicer', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--analyze-only', action='store_true')
    args = ap.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    run = baseline.run
    assert 'PrusaSlicer-2.7.2' in run([args.slicer, '--help'])
    if not args.analyze_only:
        assert run(['git', '-C', args.bosl2, 'rev-parse', 'HEAD']).strip() == baseline.REV
        assert not run(['git', '-C', args.bosl2, 'status', '--porcelain']).strip()
        env = dict(os.environ, OPENSCADPATH=str(args.bosl2.resolve().parent))
        solids = {}
        for name in ['positive', 'negative', 'male', 'integral']:
            file = args.output / (name + '.stl')
            source = ROOT / ('slicing.scad' if name == 'integral' else 'split.scad')
            log = run(['openscad', '-o', file, '-D', f'part="{name}"', source], env)
            (args.output / (name + '-cad.log')).write_text(log)
            solids[name] = solid(trimesh.load(file, force='mesh'))
        for name in ['positive', 'negative']:
            assert np.allclose(mesh(solids[name]).extents, [136, 10.3, 5.15], atol=2e-5)
        phases = assembly(solids)
        (args.output / 'geometry.json').write_text(json.dumps(dict(
            volumes_mm3={n:s.volume() for n,s in solids.items()},
            phase_sensitivity=phases), indent=2))
        # Three identical matched pairs; halves are complementary, not interchangeable.
        for name in ['split', 'integral']:
            names = ['positive', 'negative']*3 if name == 'split' else ['integral']*3
            copies = []
            for i, component in enumerate(names):
                m = mesh(solids[component]); m.apply_translation([10, 10+13.3*i, 0]); copies.append(m)
            plate = trimesh.util.concatenate(copies)
            packed = md.Manifold(md.Mesh(np.asarray(plate.vertices, dtype=np.float32),
                                        np.asarray(plate.faces, dtype=np.uint32)))
            assert packed.status() == md.Error.NoError
            assert len(packed.decompose()) == len(names)
            assert np.all(plate.bounds[0] >= -1e-5) and np.all(plate.bounds[1] < 256)
            plate.export(args.output / (name+'-three.stl'))
        for name, part, flags in [('split_auto','split',[]),
                ('split_support','split',['--support-material']),
                ('integral_transverse','integral',['--bridge-angle','90'])]:
            cy = 48.4 if part == 'split' else 28.45
            log = run([args.slicer, '--load', ROOT/'slicing.ini', '--threads','2',
                '--center', f'78,{cy}', '--export-gcode','--output',args.output/(name+'.gcode'),
                *flags,args.output/(part+'-three.stl')])
            (args.output/(name+'.log')).write_text(log)
            print(name, flush=True)
    else:
        solids = {n:solid(trimesh.load(args.output/(n+'.stl'), force='mesh'))
                  for n in ['positive', 'negative', 'male', 'integral']}
        (args.output/'geometry.json').write_text(json.dumps(dict(
            volumes_mm3={n:s.volume() for n,s in solids.items()},
            phase_sensitivity=assembly(solids)), indent=2))
    result = {name:analyze(args.output/(name+'.gcode')) for name in
              ['split_auto','split_support','integral_transverse']}
    assert result['split_auto']['cavity_bridge_segments'] == 0
    assert result['integral_transverse']['cavity_bridge_segments'] > 100
    for case in ['split_auto', 'split_support']:
        assert not set(result[case]['roles']) & {'Bridge infill', 'Overhang perimeter',
                                                'Support material', 'Support material interface'}
    result['geometry'] = json.loads((args.output/'geometry.json').read_text())
    result['ledger'] = ledger()
    result['planar_flank_axial_relief_mm'] = .15*math.tan(math.radians(15))
    result['provenance'] = dict(bosl2=baseline.REV,
        slicer=run([args.slicer, '--help']).splitlines()[0], computational_only=True)
    result['source_sha256'] = {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
                             for n in ['split.py','split.scad','slicing.scad','slicing.ini']}
    (args.output/'split-summary.json').write_text(json.dumps(result, indent=2))
    plot(args.output)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
