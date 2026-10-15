#!/usr/bin/env python3
"""Reproduce E-295 compact coupon STL and nominal mesh mating checks.

Requires OpenSCAD, pinned BOSL2, Python numpy/trimesh/manifold3d/matplotlib.
Example (from repository root):
  python owner-print-tests/2026-10-15-compact-screw-fit/generate.py \
    --bosl2 work/compact-screw-fit/BOSL2 --scratch work/compact-screw-fit
No printer G-code is generated. The supplied STL can be imported directly.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess

import manifold3d as md
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
REV = '136e6367e65d52196a3ea51d03156f8b622c60fc'
RELIEFS = [.175, .175, .175, .15, .20]


def solid(mesh):
    out = md.Manifold(md.Mesh(np.asarray(mesh.vertices, dtype=np.float32),
                              np.asarray(mesh.faces, dtype=np.uint32)))
    assert out.status() == md.Error.NoError
    return out


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--reuse', action='store_true')
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    rev = subprocess.check_output(['git', '-C', a.bosl2, 'rev-parse', 'HEAD'], text=True).strip()
    assert rev == REV
    assert not subprocess.check_output(['git', '-C', a.bosl2, 'status', '--porcelain'], text=True).strip()
    env = dict(os.environ, OPENSCADPATH=str(a.bosl2.resolve().parent))

    def export(item):
        i, part = item
        out = a.scratch / f'{part}-{i}.stl'
        if not a.reuse:
            cmd = ['openscad', '-o', str(out), '-D', f'part="{part}"',
                   '-D', f'label={i}', '-D', f'relief={RELIEFS[i-1]}', str(HERE / 'coupon.scad')]
            p = subprocess.run(cmd, env=env, capture_output=True, text=True)
            (a.scratch / f'{part}-{i}.log').write_text(p.stdout + p.stderr)
            assert p.returncode == 0 and 'WARNING' not in p.stderr and 'ERROR' not in p.stderr, p.stderr
        m = trimesh.load(out, force='mesh')
        assert m.is_watertight and m.is_winding_consistent and len(m.split()) == 1
        assert np.allclose(m.extents, [10, 10, 18.4] if part == 'screw' else [12, 12, 18], atol=1e-4)
        assert abs(m.bounds[0, 2]) < 1e-6
        return i, part, m

    jobs = [(i, p) for i in range(1, 6) for p in ('screw', 'pin')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        meshes = {(p, i): m for i, p, m in executor.map(export, jobs)}
    pieces = []
    records = []
    for i, part in jobs:
        m = meshes[part, i].copy()
        pos = [7 + (i-1)*15, 7 if part == 'screw' else 23, 0]
        m.apply_translation(pos)
        pieces.append(m)
        records.append(dict(part=part, label=i, radial_relief_mm=RELIEFS[i-1],
                            center_xy_mm=pos[:2], solid_mm3=float(meshes[part, i].volume)))
    plate = trimesh.util.concatenate(pieces)
    target = HERE / 'compact-five-pairs.stl'
    plate.export(target)
    reloaded = trimesh.load(target, force='mesh')
    # Float32 STL export can collapse zero-width CSG slivers. Remove only
    # geometrically degenerate facets; never fill holes or change the fit.
    keep = reloaded.nondegenerate_faces()
    removed = int((~keep).sum())
    reloaded.update_faces(keep); reloaded.remove_unreferenced_vertices()
    reloaded.export(target)
    reloaded = trimesh.load(target, force='mesh')
    assert reloaded.is_watertight and reloaded.is_winding_consistent
    assert len(reloaded.split()) == 10
    assert np.allclose(reloaded.extents, [72, 27, 18.4], atol=1e-4), reloaded.extents
    assert abs(reloaded.volume - sum(r['solid_mm3'] for r in records)) < .01
    solids = {key: solid(m) for key, m in meshes.items()}
    overlap = []
    for i in range(1, 6):
        for dz in np.linspace(.6, 9.5, 61):
            # Screw axis retained. Holding pin angle zero requires a negative
            # (clockwise seen from above) screw angle as the pin rises.
            # These are geometric pose checks; operation direction is reviewed
            # independently and is described from the underside in test.md.
            moving_pin = solids['pin', i].translate([0, 0, float(2.4 + dz)])
            rotated_screw = solids['screw', i].rotate([0, 0, float(-360*dz/3)])
            volume = (moving_pin ^ rotated_screw).volume()
            assert volume < .001, (i, dz, volume)
            overlap.append(volume)
    q = 1.125
    wrong = (solids['pin', 1].translate([0, 0, 2.4+q]) ^
             solids['screw', 1].rotate([0, 0, 360*q/3])).volume()
    assert wrong > .01, wrong
    # Existing optional owner parts really are compatible in nominal CAD:
    # retained E-281 pair 5, same screw profile and 0.20 mm radial relief.
    old_file = HERE.parent / 'short-thread-fit' / 'five-short-thread-pairs.stl'
    old = trimesh.load(old_file, force='mesh').split()
    old_screw = next(m.copy() for m in old if np.allclose(m.bounds.mean(axis=0), [92, 12, 9.5], atol=.01))
    old_nut = next(m.copy() for m in old if np.allclose(m.bounds.mean(axis=0), [92, 32, 5.2], atol=.01))
    old_screw.apply_translation([-92, -12, 0]); old_nut.apply_translation([-92, -32, 0])
    old_screw = solid(old_screw); old_nut = solid(old_nut)
    cross = []
    for dz in (6., 7.5, 9.):
        cross += [(solids['pin', 5].translate([0, 0, 3+dz]) ^ old_screw.rotate([0, 0, -360*dz/3])).volume(),
                  (old_nut.translate([0, 0, 2.4+dz]) ^ solids['screw', 5].rotate([0, 0, -360*dz/3])).volume()]
    assert max(cross) < .001, cross
    result = dict(bosl2=rev, openscad=subprocess.check_output(['openscad', '--version'],
                  stderr=subprocess.STDOUT, text=True).strip(),
                  python_packages={name: importlib.metadata.version(name) for name in ('numpy', 'trimesh', 'manifold3d')},
                  plate_mm=reloaded.extents.tolist(), part_count=10, watertight=True,
                  degenerate_float32_export_facets_removed=removed,
                  total_solid_mm3=float(reloaded.volume),
                  pla_mass_at_1_24_g_cm3=float(reloaded.volume*1.24/1000),
                  parts=records, mating_pose_count=len(overlap),
                  max_mating_overlap_mm3=float(max(overlap)),
                  wrong_phase_overlap_mm3=float(wrong),
                  retained_broad_pair5_cross_pose_count=len(cross),
                  retained_broad_pair5_max_overlap_mm3=float(max(cross)),
                  sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  scope='CAD only; no print, load, wear or production-yield result')
    (HERE / 'geometry-validation.json').write_text(json.dumps(result, indent=2)+'\n')
    render(pieces, HERE / 'plate-preview.png')
    print(json.dumps(result, indent=2))


def render(pieces, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    for j, m in enumerate(pieces):
        ax.add_collection3d(Poly3DCollection(m.triangles,
            facecolors=['#4597b9', '#eab260'][j % 2], linewidth=0, shade=True))
    for i in range(5):
        ax.text(7+i*15, 23, 20, f'{i+1}: {RELIEFS[i]:.3f}')
    ax.set(xlim=(0, 76), ylim=(0, 32), zlim=(0, 22), xlabel='mm', ylabel='mm')
    ax.set_box_aspect((76, 32, 22)); ax.view_init(36, -66)
    ax.set_title('Exact printable mesh: 5 screws + 5 compact sleeves\n'
                 '12 mm external two-layer sleeve feet; bore has no support geometry')
    fig.tight_layout(); fig.savefig(output, dpi=160); plt.close(fig)


if __name__ == '__main__':
    main()
