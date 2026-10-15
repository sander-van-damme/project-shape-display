#!/usr/bin/env python3
"""Build the four owner projects from unchanged PR #155 STLs in Bambu Studio.

Requires Python trimesh/numpy and the official Bambu Studio 02.08.02.61 resources.
Example: python owner-print-tests/build-bambu-projects.py --bambu /path/bambu-studio
  --resources /path/resources --scratch work/bambu-projects
No printer connection, CAD regeneration, auto arrangement or auto orientation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
VERSION = '02.08.02.61'
NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)


def resolve(resources, kind, name):
    """Bambu presets also inherit an ordered list of machine G-code templates."""
    source = resources / 'profiles' / 'BBL' / kind / (name + '.json')
    data = json.loads(source.read_text())
    result, sources = {}, []
    parents = data.get('inherits', [])
    if isinstance(parents, str):
        parents = [parents] if parents else []
    for parent in parents:
        config, provenance = resolve(resources, kind, parent)
        result.update(config)
        sources.extend(provenance)
    for template in data.get('include', []):
        config, provenance = resolve(resources, kind, template)
        result.update(config)
        sources.extend(provenance)
    result.update({k: v for k, v in data.items() if k not in ('inherits', 'include')})
    sources.append({'path': str(source.relative_to(resources)),
                    'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    return result, sources


def input_project(stl, output):
    """Split into named objects, translate the complete plate rigidly to bed centre."""
    mesh = trimesh.load(stl, force='mesh')
    parts = sorted(mesh.split(), key=lambda m: (round(m.bounds.mean(axis=0)[1], 2),
                                               round(m.bounds.mean(axis=0)[0], 2)))
    offset = np.array([128., 128., 0.])
    offset[:2] -= mesh.bounds.mean(axis=0)[:2]
    model = ET.Element(f'{{{NS}}}model', unit='millimeter')
    ET.SubElement(model, f'{{{NS}}}metadata', name='Application').text = 'PR155 owner print project builder'
    resources = ET.SubElement(model, f'{{{NS}}}resources')
    build = ET.SubElement(model, f'{{{NS}}}build')
    for i, part in enumerate(parts, 1):
        x, y, _ = part.bounds.mean(axis=0)
        if stl.stem == 'compact-five-pairs':
            label = round((x - 7) / 15) + 1
            relief = ['0.175', '0.175', '0.175', '0.150', '0.200'][label - 1]
            name = f'{"screw" if y < 15 else "pin"}-{label}-relief-{relief}mm'
        elif y < 25:
            name = 'base' if x < 25 else 'guide-cage-side-down'
        elif abs(y - 39) < 1:
            name = f'screw-{round((x - 8) / 10) + 1}'
        elif abs(y - 52) < 1:
            name = f'pin-{round((x - 8) / 10) + 1}'
        else:
            name = 'manual-driver' if y < 55 else 'neutral-gauge-3.3mm'
        obj = ET.SubElement(resources, f'{{{NS}}}object', id=str(i), type='model',
                            name=name)
        geom = ET.SubElement(obj, f'{{{NS}}}mesh')
        vertices = ET.SubElement(geom, f'{{{NS}}}vertices')
        for x, y, z in part.vertices + offset:
            ET.SubElement(vertices, f'{{{NS}}}vertex', x=f'{x:.9g}', y=f'{y:.9g}', z=f'{z:.9g}')
        triangles = ET.SubElement(geom, f'{{{NS}}}triangles')
        for a, b, c in part.faces:
            ET.SubElement(triangles, f'{{{NS}}}triangle', v1=str(a), v2=str(b), v3=str(c))
        ET.SubElement(build, f'{{{NS}}}item', objectid=str(i))
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('3D/3dmodel.model', ET.tostring(model, encoding='utf-8', xml_declaration=True))
        archive.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        archive.writestr('_rels/.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    return {'stl': str(stl.relative_to(HERE)), 'stl_sha256': hashlib.sha256(stl.read_bytes()).hexdigest(),
            'body_count': len(parts), 'translation_mm': offset.tolist(),
            'source_bounds_mm': mesh.bounds.tolist()}


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--bambu', type=Path, required=True)
    ap.add_argument('--resources', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    a = ap.parse_args()
    scratch = a.scratch.resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    help_result = subprocess.run([str(a.bambu.resolve()), '--help'], capture_output=True, text=True, cwd=scratch)
    assert help_result.returncode == 0 and VERSION in help_result.stdout, 'Use pinned Bambu Studio version'
    printer, printer_sources = resolve(a.resources, 'machine', 'Bambu Lab X1 Carbon 0.4 nozzle')
    assert ';===== machine: X1-0.4' in printer['machine_start_gcode'], 'Missing X1C template includes'
    filament, filament_sources = resolve(a.resources, 'filament', 'Generic PLA')
    process, process_sources = resolve(a.resources, 'process', '0.12mm Fine @BBL X1C')
    # All extrusion categories deliberately slow, including thin-wall gap fill.
    for key in ['outer_wall_speed', 'inner_wall_speed', 'small_perimeter_speed',
                'sparse_infill_speed', 'internal_solid_infill_speed', 'top_surface_speed',
                'gap_infill_speed', 'support_speed', 'support_interface_speed']:
        process[key] = ['30', '30']
    for key in ['initial_layer_speed', 'initial_layer_infill_speed', 'bridge_speed']:
        process[key] = ['20', '20']
    for key in ['default_acceleration', 'outer_wall_acceleration', 'inner_wall_acceleration',
                'top_surface_acceleration', 'sparse_infill_acceleration', 'travel_acceleration',
                'initial_layer_travel_acceleration']:
        process[key] = ['1000', '1000']
    process.update({
        'name': 'Owner screw tests 0.12 X1C PLA', 'print_settings_id': 'Owner screw tests 0.12 X1C PLA',
        'layer_height': '0.12', 'initial_layer_print_height': '0.12',
        'wall_generator': 'arachne', 'wall_loops': '2', 'sparse_infill_density': '100%',
        'sparse_infill_pattern': 'zig-zag', 'wall_transition_length': '100%',
        'wall_transition_filter_deviation': '25%', 'wall_transition_angle': '10',
        'wall_distribution_count': '1', 'min_feature_size': '25%', 'min_bead_width': '85%',
        'small_perimeter_threshold': ['20', '20'], 'initial_layer_acceleration': ['500', '500'],
        'travel_speed': ['150', '150'], 'enable_arc_fitting': '0',
        'enable_support': '0', 'raft_layers': '0', 'skirt_loops': '0',
        'enable_prime_tower': '0', 'print_sequence': 'by layer',
        'xy_contour_compensation': '0', 'xy_hole_compensation': '0',
        'elefant_foot_compensation': '0', 'enable_circle_compensation': '0',
        'curr_bed_type': 'Textured PEI Plate',
        'overhang_1_4_speed': ['30', '30'], 'overhang_2_4_speed': ['20', '20'],
        'overhang_3_4_speed': ['10', '10'], 'overhang_4_4_speed': ['10', '10'],
    })
    for key in ['line_width', 'initial_layer_line_width', 'outer_wall_line_width',
                'inner_wall_line_width', 'top_surface_line_width', 'sparse_infill_line_width',
                'internal_solid_infill_line_width', 'support_line_width']:
        process[key] = '0.45'
    filament.update({'additional_cooling_fan_speed': ['0'], 'slow_down_min_speed': ['10'],
                     'filament_settings_id': ['Generic PLA - owner X1C 220C'],
                     'name': 'Generic PLA - owner X1C 220C'})
    printer['printer_settings_id'] = 'Bambu Lab X1 Carbon 0.4 nozzle'
    jobs = [('2026-10-15-compact-screw-fit', 'compact-five-pairs')]
    jobs += [('2026-10-15-four-pin-screw-demo', f'four-pin-demo-{label}-plate') for label in ['015', '0175', '020']]
    for folder, stem in jobs:
        target = HERE / folder
        target.mkdir(exist_ok=True)
        job = scratch / stem
        job.mkdir(exist_ok=True)
        p = dict(process, brim_type='no_brim' if folder == '2026-10-15-compact-screw-fit' else 'outer_only',
                 brim_width='0' if folder == '2026-10-15-compact-screw-fit' else '3', brim_object_gap='0')
        for name, config in [('printer', printer), ('filament', filament), ('process', p)]:
            (job / (name + '.json')).write_text(json.dumps(config, indent=2) + '\n')
        provenance = input_project(HERE / folder / (stem + '.stl'), job / 'input.3mf')
        cmd = [str(a.bambu.resolve()), '--datadir', str(scratch / 'studio-data'),
               '--load-settings', str(job / 'printer.json') + ';' + str(job / 'process.json'),
               '--load-filaments', str(job / 'filament.json'), '--arrange', '0', '--orient', '0',
               '--slice', '0', '--export-3mf', stem + '.3mf',
               '--export-settings', str(job / 'effective-settings.json'),
               '--outputdir', str(job), str(job / 'input.3mf')]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=scratch)
        (job / 'studio.log').write_text(result.stdout + result.stderr)
        print(stem, result.returncode, flush=True)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-10000:])
        shutil.move(job / (stem + '.3mf'), target / (stem + '.3mf'))
        provenance.update({'bambu_studio': VERSION,
                           'printer_sources': printer_sources, 'filament_sources': filament_sources,
                           'process_sources': process_sources})
        (job / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')


if __name__ == '__main__':
    main()
