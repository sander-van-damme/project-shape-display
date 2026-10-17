#!/usr/bin/env python3
"""Reproduce E300 loaded-selector-face radii from current exported STL meshes.

Run from the repository root with work/slicer-runtime/cad-python, which provides
numpy, trimesh and shapely. No networkx is needed. Results assume level rigid
parts and uniform contact pressure; they are geometry calculations, not friction
or pressure measurements. Flange creep, tilted-edge contact and print variation
are deliberately not inferred from this model.
"""
from pathlib import Path
import hashlib
import json
import math

import numpy as np
import trimesh
from shapely import contains_xy
from shapely.geometry import LineString, Point
from shapely.ops import polygonize, unary_union

HERE = Path(__file__).resolve().parent
CAD = HERE.parent / 'cad' / 'parts'
FACE_Z = -0.24
SECTION_Z = FACE_Z - 0.00001  # inside the lower blade, immediately below its top
FLANGE_R = 2.15
GRID = 0.0025


def evaluate(name, centers):
    path = CAD / (name + '.stl')
    model = trimesh.load(path, force='mesh')
    section = model.section(plane_normal=[0, 0, 1],
                            plane_origin=[0, 0, SECTION_Z])
    if section is None:
        raise RuntimeError(f'{name}: no section at loaded-face z')
    lines = [LineString(section.vertices[e.points][:, :2])
             for e in section.entities]
    # The open U notches form one outer contour rather than closed bore holes.
    # polygonize avoids trimesh.discrete's optional networkx dependency.
    profile = unary_union(list(polygonize(unary_union(lines))))
    entries = []
    axis = np.arange(-FLANGE_R, FLANGE_R + GRID * 0.1, GRID)
    for center_x in centers:
        circle = Point(center_x, 0).buffer(FLANGE_R, quad_segs=1024)
        contact = profile.intersection(circle)
        xx, yy = np.meshgrid(axis + center_x, axis)
        mask = contains_xy(contact, xx, yy)
        radii = np.hypot(xx[mask] - center_x, yy[mask])
        if not len(radii):
            raise RuntimeError(f'{name}: empty flange/contact intersection')
        entries.append(dict(center_x_mm=center_x,
                            contact_area_mm2=float(contact.area),
                            uniform_pressure_effective_radius_mm=float(radii.mean()),
                            integration_points=int(len(radii))))
    return dict(mesh=str(path.relative_to(HERE.parents[3])),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                local_bearing_face_z_mm=FACE_Z,
                local_section_z_mm=SECTION_Z,
                flange_radius_mm=FLANGE_R,
                entries=entries)


def analytic_u():
    """Exact ideal U face: rear half-annulus plus both front outer tips."""
    ri, ro = 1.4, FLANGE_R
    theta = math.acos(ri / ro)
    sec, tan = 1 / math.cos(theta), math.tan(theta)
    area_back = math.pi / 2 * (ro**2 - ri**2)
    area_front = ro**2 * theta - ri**2 * tan
    radial_back = math.pi / 3 * (ro**3 - ri**3)
    radial_front = 2 / 3 * (ro**3 * theta - ri**3 / 2 *
                          (sec * tan + math.log(sec + tan)))
    return dict(inner_radius_mm=ri, outer_radius_mm=ro,
                contact_area_mm2=area_back + area_front,
                uniform_pressure_effective_radius_mm=(radial_back + radial_front) /
                                                     (area_back + area_front),
                rear_half_annulus_only_radius_mm=radial_back / area_back)


def main():
    results = dict(
        evidence='CAD geometry and uniform-pressure numerical integration; not physical measurements',
        load_path=('Row pushes male rotor upward. Inverted column pushes female rotor downward. '
                   'Both reactions act through local lower-blade top face z=-0.24 mm. '
                   'The upper D3.7 fork is not the normal clamping load face.'),
        grid_spacing_mm=GRID,
        nominal_model_radius_mm=1.85,
        adverse_model_radii_mm=[2.0, 2.15],
        analytic_ideal_u=analytic_u(),
        actual_meshes=[evaluate('row-selector', [-2.54, 2.54]),
                       evaluate('column-selector', [0.0])])
    target = HERE / 'thrust-face.json'
    target.write_text(json.dumps(results, indent=2) + '\n')
    print(f'{target.name}: row radii ' + ', '.join(
        f'{v["uniform_pressure_effective_radius_mm"]:.8f}'
        for v in results['actual_meshes'][0]['entries']) +
        f'; column {results["actual_meshes"][1]["entries"][0]["uniform_pressure_effective_radius_mm"]:.8f} mm')


if __name__ == '__main__':
    main()
