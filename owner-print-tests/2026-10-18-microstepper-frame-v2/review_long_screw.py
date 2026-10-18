#!/usr/bin/env python3
"""Check real horizontal screw/support paths; PROJECT OUTPUT.json [OUTPUT.png].

Nominal G-code footprints are a computational screen, never physical qualification.
"""
from pathlib import Path
import collections, hashlib, importlib.util, json, sys, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from shapely.geometry import box
from shapely.affinity import translate
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reader', HERE.parent / 'validate-bambu-project.py')
reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)
project, out = Path(sys.argv[1]), Path(sys.argv[2])
with zipfile.ZipFile(project) as archive:
    settings = json.loads(archive.read('Metadata/project_settings.config'))
    gcode = archive.read('Metadata/plate_1.gcode').decode()
    paths, _ = reader.parse(gcode)
    bounds, *_ = reader.project_bounds(archive)
    config = ET.fromstring(archive.read('Metadata/model_settings.config'))
objects = {}
for obj in config.findall('object'):
    values = {m.get('key'): m.get('value') for m in obj.findall('metadata') if m.get('key')}
    name = values.pop('name'); values.pop('extruder', None); objects[name] = values
assert settings['enable_support'] == '0'
assert sum(v['enable_support'] == '1' for v in objects.values()) == 1
saved = next(v for k, v in objects.items() if k.endswith('-screw-50-supported'))
assert saved['enable_support'] == '1' and saved['support_type'] == 'normal(auto)'
assert saved['support_on_build_plate_only'] == '1' and saved['support_top_z_distance'] == '0.24'
layout = json.loads((HERE / 'layout.json').read_text())
source_lo = np.min([p['bounds_mm'][0] for p in layout], axis=0)
shift = bounds[0, :2] - source_lo[:2] - np.array([float(v) for v in settings['extruder_offset'][0].split('x')])
part = next(p for p in layout if p['name'] == 'screw-50-supported')
cx, cy = np.array(part['center_xy']) + shift
local = [p for p in paths if -3.6 < (p['x'] + p['x1']) / 2 - cx < 54 and abs((p['y'] + p['y1']) / 2 - cy) < 8.6]
support = [p for p in local if 'support' in p['role'].lower()]
interface = [p for p in support if 'interface' in p['role'].lower()]
model = [p for p in local if 'support' not in p['role'].lower() and p['role'] != 'Brim']
assert support and interface and model
assert len(support) == sum('support' in p['role'].lower() for p in paths), 'Support outside the long screw region'
def footprint(ps):
    return translate(reader.footprint(ps), -cx, -cy)
def layers(ps):
    result = collections.defaultdict(list)
    for p in ps: result[p['z']].append(p)
    return {z: footprint(qs) for z, qs in sorted(result.items())}
support_layers, model_layers = layers(support), layers(model)
interface_fp = footprint(interface)
samples = np.arange(2.45, 50.4, .1)
covered = [interface_fp.intersection(box(x - .05, -1.75, x + .05, 1.75)).area > .00001 for x in samples]
max_gap = run = 0
for hit in covered:
    run = 0 if hit else run + 1
    max_gap = max(max_gap, run)
# Newly appearing model islands are acceptable only above a real support footprint
# with the saved release gap (+ one layer for quantized inclined thread surfaces).
previous = None; starts = []; unbacked = []
for z, fp in model_layers.items():
    polys = list(fp.geoms) if hasattr(fp, 'geoms') else [fp]
    for poly in polys:
        if poly.area <= .005 or z <= .121: continue
        if previous is not None and poly.intersection(previous.buffer(.01)).area >= .001: continue
        candidates = [(zs, s) for zs, s in support_layers.items() if -.001 <= z - .12 - zs <= .361]
        contacts = [(zs, poly.intersection(s).area) for zs, s in candidates if poly.intersection(s).area >= .001]
        row = dict(z_mm=z, area_mm2=poly.area, centroid_xy_mm=list(poly.centroid.coords)[0],
                   support_z_mm=max((zs for zs, area in contacts), default=None))
        if contacts: row['nominal_vertical_gap_mm'] = z - .12 - row['support_z_mm']
        else: unbacked.append(row)
        starts.append(row)
    previous = fp
support_first = support_layers[min(support_layers)]
report = dict(scope='Nominal G-code footprint check, not measured adhesion, rigidity, support removal or thread fit.',
    project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),
    object_settings=objects, supported_object=part['name'],
    model_height_mm=max(model_layers), screw_thread_length_mm=48,
    support_path_count=len(support), support_interface_path_count=len(interface),
    all_support_paths_confined_to_long_screw=True,
    support_z_range_mm=[min(support_layers), max(support_layers)],
    interface_z_range_mm=[min(p['z'] for p in interface), max(p['z'] for p in interface)],
    interface_projection_bounds_local_mm=list(interface_fp.bounds),
    support_bed_area_mm2=support_first.area,
    support_bed_bounds_local_mm=list(support_first.bounds),
    thread_axis_local_x_mm=[2.4, 50.4], thread_axis_source_plate_x_mm=[cx-shift[0]+2.4,cx-shift[0]+50.4],
    thread_axis_y_mm=0, thread_axis_z_mm=5,
    longitudinal_coverage_step_mm=.1, longitudinal_covered_bins=sum(covered), longitudinal_total_bins=len(covered),
    longitudinal_coverage_fraction=sum(covered)/len(covered), largest_uncovered_longitudinal_bin_run_mm=max_gap*.1,
    new_model_islands_backed_by_support=starts, new_model_islands_without_support=unbacked,
    no_unbacked_islands=not unbacked,
    support_max_speed_mm_s=max(p['speed'] for p in support),
    model_max_speed_mm_s=max(p['speed'] for p in model),
    model_max_acceleration_mm_s2=max(p['accel'] for p in model),
    estimates=[line for line in gcode.splitlines() if line.startswith(('; total estimated time','; total filament','; filament used','; model printing time'))],
    limits=['The screw is horizontal: 10 mm overall printing height and a 5 mm shaft axis; it is not a 50 mm unsupported upright column.',
            'Support is distributed beneath the thread, with a nominal 0.24 mm removable PLA interface gap. The upper thread layers build on the screw body.',
            'The underside of the external thread contacts removable support; inspect for scars and hand-test through the pin before motor use.',
            'The 50 mm female pin remains upright on its original foot, without support inside its bore. Its physical stability remains untested.'])
out.write_text(json.dumps(report, indent=2) + '\n')
assert sum(covered)/len(covered) > .95 and max_gap*.1 <= .5, 'Insufficient distributed support coverage'
assert not unbacked, f'{len(unbacked)} new model islands lack support'
assert max(model_layers) <= 10.13 and min(support_layers) == .12
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
fig, axes = plt.subplots(2, 1, figsize=(11, 6), gridspec_kw={'height_ratios':[1,1]})
for ax, view in zip(axes, ['side','plan']):
    for ps, color, label, lw in [(model,'#306886','schroef',.45),(support,'#d39a52','support',.6),(interface,'#bc3e2c','supportinterface',.85)]:
        if view == 'side':
            lines = [[(p['x']-cx,p['z']),(p['x1']-cx,p['z'])] for p in ps]
        else: lines = [[(p['x']-cx,p['y']-cy),(p['x1']-cx,p['y1']-cy)] for p in ps]
        ax.add_collection(LineCollection(lines, colors=color, linewidths=lw, label=label, alpha=.55))
    ax.set_xlim(-4,54); ax.set_ylim((-.5,10.8) if view=='side' else (-8.5,8.5)); ax.set_aspect('equal')
    ax.set_ylabel('Z mm' if view=='side' else 'Y mm'); ax.set_xlabel('Lengte-as X mm')
    ax.grid(alpha=.15)
axes[0].set_title('Werkelijke G-code: horizontale lange schroef boven verwijderbare supports')
axes[0].legend(loc='upper right', ncol=3)
axes[1].set_title('Bovenaanzicht: supportinterface verdeeld over 48 mm schroefdraad')
fig.tight_layout(); fig.savefig(Path(sys.argv[3]) if len(sys.argv)>3 else out.with_suffix('.png'), dpi=180)
print(json.dumps({k:v for k,v in report.items() if k not in ('object_settings','new_model_islands_backed_by_support')}, indent=2))
