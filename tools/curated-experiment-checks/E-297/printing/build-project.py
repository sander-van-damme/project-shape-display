#!/usr/bin/env python3
"""Create configured X1C/0.4 PLA coupling projects and reopen/reslice them.

Requires numpy/trimesh, official Bambu Studio 02.08.02.61 executable/resources.
Call --help for paths. Runtime binaries and temporary logs belong in work/.
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

ROOT = Path(__file__).resolve().parents[4]
HERE = ROOT / 'owner-print-tests'
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
    ET.SubElement(model, f'{{{NS}}}metadata', name='Application').text = 'Two-half coupling print project builder'
    resources = ET.SubElement(model, f'{{{NS}}}resources')
    build = ET.SubElement(model, f'{{{NS}}}build')
    layout_path = stl.parent / 'layout.json'
    layout = json.loads(layout_path.read_text()) if layout_path.exists() else []
    for i, part in enumerate(parts, 1):
        x, y, _ = part.bounds.mean(axis=0)
        name = f'{stl.stem}-part-{i:02d}'
        if layout:
            idx, match = min(enumerate(layout),key=lambda pair: np.linalg.norm(np.array(pair[1]['bounds_mm'])-part.bounds))
            assert np.max(np.abs(np.array(match['bounds_mm'])-part.bounds)) < .001
            name = f'{idx+1:02d}-{match["name"]}'
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
    return {'stl': str(stl.relative_to(ROOT)), 'stl_sha256': hashlib.sha256(stl.read_bytes()).hexdigest(),
            'body_count': len(parts), 'translation_mm': offset.tolist(),
            'source_bounds_mm': mesh.bounds.tolist()}


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--bambu', type=Path, required=True)
    ap.add_argument('--resources', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--stl', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--name', default='Two-half coupling 0.12 X1C PLA')
    ap.add_argument('--brim', type=float, default=0)
    ap.add_argument('--brim-gap', type=float, default=0.12)
    a = ap.parse_args()
    scratch = a.scratch.resolve(); scratch.mkdir(parents=True, exist_ok=True)
    target = a.out.resolve(); target.parent.mkdir(parents=True, exist_ok=True)
    help_result = subprocess.run([str(a.bambu.resolve()), '--help'], capture_output=True, text=True, cwd=scratch)
    assert help_result.returncode == 0 and VERSION in help_result.stdout, 'Use pinned Bambu Studio version'
    printer, printer_sources = resolve(a.resources, 'machine', 'Bambu Lab X1 Carbon 0.4 nozzle')
    filament, filament_sources = resolve(a.resources, 'filament', 'Generic PLA')
    process, process_sources = resolve(a.resources, 'process', '0.12mm Fine @BBL X1C')
    assert ';===== machine: X1-0.4' in printer['machine_start_gcode']
    # Reuse settings actually printed unchanged in the completed E-295 compact fit.
    baseline = HERE / '2026-10-15-compact-screw-fit' / 'compact-five-pairs.3mf'
    with zipfile.ZipFile(baseline) as archive:
        baseline_settings = json.loads(archive.read('Metadata/project_settings.config'))
    metadata_keys = {'from','type','version','name','instantiation','setting_id','inherits','compatible_printers','include'}
    keys = (set(process) | {'curr_bed_type', 'enable_arc_fitting'}) - metadata_keys
    for key in keys:
        if key in baseline_settings: process[key] = baseline_settings[key]
    for key in set(filament) - metadata_keys:
        if key in baseline_settings: filament[key] = baseline_settings[key]
    printer['printer_settings_id'] = 'Bambu Lab X1 Carbon 0.4 nozzle'
    process.update(name=a.name, print_settings_id=a.name,
                   brim_type='outer_only' if a.brim else 'no_brim',
                   brim_width=str(a.brim), brim_object_gap=str(a.brim_gap))
    # Baseline preserves exact support-off, cooling, temperatures, 0.12-mm layers,
    # Arachne 0.45 widths, two walls, 100% infill and conservative speeds.
    for name, config in [('printer', printer), ('filament', filament), ('process', process)]:
        (scratch / (name + '.json')).write_text(json.dumps(config, indent=2) + '\n')
    provenance = input_project(a.stl.resolve(), scratch / 'input.3mf')
    cmd = [str(a.bambu.resolve()), '--datadir', str(scratch / 'studio-data'),
           '--load-settings', str(scratch / 'printer.json') + ';' + str(scratch / 'process.json'),
           '--load-filaments', str(scratch / 'filament.json'), '--arrange', '0', '--orient', '0',
           '--slice', '0', '--export-3mf', target.name,
           '--export-settings', str(scratch / 'effective-settings.json'),
           '--outputdir', str(scratch), str(scratch / 'input.3mf')]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=scratch)
    (scratch / 'studio.log').write_text(result.stdout + result.stderr)
    if result.returncode: raise RuntimeError((result.stdout + result.stderr)[-10000:])
    shutil.copy2(scratch / target.name, target)
    reopen = scratch / 'reopen'; reopen.mkdir(exist_ok=True)
    cmd2 = [str(a.bambu.resolve()), '--datadir', str(reopen / 'studio-data'),
            '--arrange', '0', '--orient', '0', '--slice', '0', '--export-3mf', target.name,
            '--export-settings', str(reopen / 'effective-settings.json'),
            '--outputdir', str(reopen), str(target)]
    result2 = subprocess.run(cmd2, capture_output=True, text=True, cwd=scratch)
    (reopen / 'studio.log').write_text(result2.stdout + result2.stderr)
    if result2.returncode: raise RuntimeError((result2.stdout + result2.stderr)[-10000:])
    with zipfile.ZipFile(target) as first, zipfile.ZipFile(reopen / target.name) as second:
        settings1 = json.loads(first.read('Metadata/project_settings.config'))
        settings2 = json.loads(second.read('Metadata/project_settings.config'))
        different = {k: [settings1.get(k), settings2.get(k)] for k in set(settings1)|set(settings2) if settings1.get(k)!=settings2.get(k)}
        paths1 = first.read('Metadata/plate_1.gcode').decode()
        paths2 = second.read('Metadata/plate_1.gcode').decode()
        normalize = lambda s: '\n'.join(q for q in s.splitlines() if not q.startswith('; generated by'))
        roundtrip = dict(reopened_without_external_profiles=True, return_code=result2.returncode,
                         settings_differences=different, gcode_equal_except_generated_header=normalize(paths1)==normalize(paths2))
    provenance.update(bambu_studio=VERSION, printer_sources=printer_sources,
                      filament_sources=filament_sources, process_sources=process_sources,
                      baseline_project=str(baseline.relative_to(ROOT)), baseline_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
                      final_project_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                      roundtrip=roundtrip)
    (target.parent / (target.stem + '-build.json')).write_text(json.dumps(provenance, indent=2)+'\n')
    print(json.dumps(roundtrip, indent=2), flush=True)

if __name__ == '__main__': main()
