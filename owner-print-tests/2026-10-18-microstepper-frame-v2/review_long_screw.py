#!/usr/bin/env python3
"""Check upright thread and eight modeled breakaway contacts in actual G-code.
Usage: review_long_screw.py PROJECT OUTPUT.json. Nominal paths, not physical proof.
"""
from pathlib import Path
import collections, hashlib, importlib.util, json, sys, zipfile
import numpy as np
from shapely.geometry import Point, Polygon, box
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
assert settings['enable_support'] == '0'
assert not any('support' in p['role'].lower() for p in paths), 'Unexpected automatic supports'
layout = json.loads((HERE / 'layout.json').read_text())
source_lo = np.min([p['bounds_mm'][0] for p in layout], axis=0)
shift = bounds[0, :2] - source_lo[:2] - np.array([float(v) for v in settings['extruder_offset'][0].split('x')])
part = next(p for p in layout if p['name'] == 'screw-50-supported')
cx, cy = np.array(part['center_xy']) + shift
local = [p for p in paths if abs((p['x'] + p['x1']) / 2 - cx) < 13 and abs((p['y'] + p['y1']) / 2 - cy) < 8.5]
model = [p for p in local if p['role'] != 'Brim']
layers = collections.defaultdict(list)
for p in model: layers[p['z']].append(p)
fps = {z:translate(reader.footprint(ps),-cx,-cy) for z,ps in sorted(layers.items())}
contacts = []; unexpected = []; previous = None; islands = []
def encloses(poly,x):
    return poly.geom_type=='Polygon' and Polygon(poly.exterior).covers(Point(x,0))
for z,fp in fps.items():
    polys = list(fp.geoms) if hasattr(fp,'geoms') else [fp]
    assert any(encloses(p,0) for p in polys), ('Broken thread core',z)
    if z <= 47.52:
        assert all(any(encloses(p,x) for p in polys) for x in (-7.5,7.5)), ('Missing side tower',z)
    if previous is not None:
        islands.extend(dict(z_mm=z,area_mm2=p.area) for p in polys if p.area>.005 and p.intersection(previous.buffer(.01)).area<.001)
    previous = fp
    if z <= 2.4: continue
    for side in (-1,1):
        connected = any(encloses(p,0) and encloses(p,side*2.2) for p in polys)
        expected = [(11.4 if side==1 else 9.96)+12*i for i in range(4)]
        # Slicer rounds the CAD planes to the nearest layer; allow half a layer.
        if connected and not any(abs(z-c)<=.19 for c in expected): unexpected.append(dict(z_mm=z,side=side))
for side in (-1,1):
    for i in range(4):
        centre = (11.4 if side==1 else 9.96)+12*i
        connected = []; neck_areas=[]
        for z,fp in fps.items():
            if abs(z-centre)>.19: continue
            polys = list(fp.geoms) if hasattr(fp,'geoms') else [fp]
            if any(encloses(p,0) and encloses(p,side*2.2) for p in polys):
                connected.append(z)
                neck_areas.append(fp.intersection(box(min(side*1.7,side*2),-.4,max(side*1.7,side*2),.4)).area)
        assert len(connected)>=2 and min(neck_areas)>.08, ('Neck lost in slicing',side,centre,connected)
        # Arms slope down to the tower: connectivity is across layers, not
        # a horizontal bridge all the way to the tower on the contact layer.
        for contact_z in connected:
            clip=box(min(side*1.95,side*9.2),-.9,max(side*1.95,side*9.2),.9)
            trace=Point(side*2.2,0).buffer(.1)
            history=[(z,fp) for z,fp in fps.items() if contact_z-4.92<=z<=contact_z]
            for z,fp in reversed(history):
                region=fp.intersection(clip)
                pieces=list(region.geoms) if hasattr(region,'geoms') else [region]
                trace=unary_union([poly for poly in pieces if poly.intersection(trace.buffer(.01)).area>.001])
                assert not trace.is_empty, ('Disconnected sloping arm',side,contact_z,z)
            assert trace.distance(Point(side*7.5,0))<.1, ('Arm not anchored to tower',side,contact_z)
        contacts.append(dict(side_x=side,nominal_centre_z_mm=centre,connected_layers_z_mm=connected,minimum_neck_footprint_area_mm2=min(neck_areas),sloping_arm_traced_to_tower=True))
assert not islands and not unexpected, (islands,unexpected)
assert abs(max(fps)-50.4)<.13 and min(fps)==.12
# Each of the 16 pitches retains a broad crest as well as a continuous core.
crest=[]
for i in range(16):
    section = unary_union([fp.intersection(box(-1.8,-1.8,1.8,1.8)) for z,fp in fps.items() if 2.4+3*i < z <= 5.4+3*i])
    reach = max(abs(v) for v in section.bounds)
    assert reach>1.45,(i,reach)
    crest.append(dict(pitch=i+1,maximum_crest_extent_mm=reach))
first=fps[min(fps)]
assert all(first.intersection(box(x-2,-4,x+2,4)).area>25 for x in (-7.5,7.5))
report = dict(scope='Nominal G-code widths and connectivity; not measured stiffness, removal force or printed thread fit.',
    project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),
    orientation='upright',model_height_mm=max(fps),layer_count=len(fps),automatic_support_path_count=0,
    modeled_tower_count=2,neck_dimensions_mm=[.85,.45,.24],contacts=contacts,
    side_contact_pitch_mm=12,maximum_same_side_unbraced_height_mm=12,
    shaft_core_continuous_all_layers=True,thread_crests=crest,
    bed_footprint_area_excluding_brim_mm2=first.area,no_unbacked_islands=not islands,
    no_unintended_tower_thread_connections=True,
    model_max_speed_mm_s=max(p['speed'] for p in model),
    model_max_acceleration_mm_s2=max(p['accel'] for p in model),
    estimates=[line for line in gcode.splitlines() if line.startswith(('; total estimated time','; total filament','; filament used','; model printing time'))],
    limits=['Eight solid necks touch small thread-crest regions; cut them locally, do not bend the whole tower away.',
            'No release gap at these modeled necks. Removal and scars require a physical hand-fit test.',
            'Tower pad/brim and 12 mm contact pitch reduce free length; physical stability remains untested.',
            'Layer connectivity and nominal line widths do not measure adhesion, material strength or printer accuracy.'])
out.write_text(json.dumps(report,indent=2)+'\n')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
fig,(ax,bx)=plt.subplots(1,2,figsize=(9,8),gridspec_kw={'width_ratios':[1,1]})
for color,ps,label in [('#306886',[p for p in model if max(abs(p['x']-cx),abs(p['x1']-cx))<1.85 and p['z']>2.4],'schroefdraad'),('#d39a52',[p for p in model if max(abs(p['x']-cx),abs(p['x1']-cx))>=1.85 or p['z']<=2.4],'voet / zijsteunen')]:
    ax.add_collection(LineCollection([[(p['x']-cx,p['z']),(p['x1']-cx,p['z'])] for p in ps],colors=color,linewidths=.5,alpha=.6,label=label))
ax.set(xlim=(-13,13),ylim=(0,52),xlabel='X mm',ylabel='Z mm',title='Rechtop: werkelijke printbanen');ax.set_aspect('equal');ax.legend(fontsize=8)
z=contacts[4]['connected_layers_z_mm'][0]
for p in layers[z]:bx.plot([p['x']-cx,p['x1']-cx],[p['y']-cy,p['y1']-cy],lw=max(.5,p['width']*5),color='#306886')
bx.set(xlim=(-2,9.5),ylim=(-3,3),xlabel='X mm',ylabel='Y mm',title=f'Afbreekverbinding op Z {z:.2f} mm');bx.set_aspect('equal');bx.grid(alpha=.2)
fig.tight_layout();fig.savefig(out.with_suffix('.png'),dpi=180)
print(json.dumps({k:v for k,v in report.items() if k not in ('thread_crests','limits')},indent=2))
