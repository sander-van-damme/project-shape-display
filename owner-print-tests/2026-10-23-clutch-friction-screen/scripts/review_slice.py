#!/usr/bin/env python3
"""Independent source mesh and deposited-footprint checks on each saved archive.
Usage: review_slice.py project.3mf report.json [--plot]
"""
from pathlib import Path
import collections,hashlib,importlib.util,json,re,sys,zipfile
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from shapely.geometry import Point,Polygon
from shapely.affinity import translate
HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader',HERE.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
project=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(project) as z:
 assert z.testzip() is None
 cfg=json.loads(z.read('Metadata/project_settings.config'));gcode=z.read('Metadata/plate_1.gcode').decode();bounds,instances,vertices,triangles=reader.project_bounds(z)
startup=gcode.split('; CHANGE_LAYER',1)[0]
assert ';===== machine: X1-0.4' in startup
assert re.findall(r'^M10[49].*',startup,re.M)[-1].startswith('M109 S210')
assert 'M190 S55' in startup
paths,_=reader.parse(gcode);layout=json.loads((HERE/'metadata/layout.json').read_text());mesh=trimesh.load(HERE/'components/clutch-friction-screen.stl',force='mesh')
translation=bounds[0]-mesh.bounds[0];offset=np.array([float(x)for x in cfg['extruder_offset'][0].split('x')]);shift=translation[:2]-offset
err=max(cKDTree(vertices).query(mesh.vertices+translation)[0].max(),cKDTree(mesh.vertices+translation).query(vertices)[0].max())
assert err<.00003,err
assert len(instances)==7
assert cfg['printer_settings_id']=='Bambu Lab X1 Carbon 0.4 nozzle'
assert cfg['enable_support']=='0';assert not any('support' in p['role'].lower() for p in paths)
report=dict(scope='CAD and nominal deposited toolpaths, NOT physical print or torque evidence',project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),max_mesh_vertex_error_mm=float(err),support_paths=0,zip_crc_valid=True,official_x1c_start_gcode=True,nozzle_before_first_layer_C=210,bed_wait_C=55,parts=[],gcode_estimates=[s for s in gcode.splitlines()if re.match(r'; (model printing time|total filament)',s)])
plot=[]
for part in layout:
 lo,hi=np.array(part['bounds_mm']);lo[:2]+=shift;hi[:2]+=shift;cx,cy=np.array(part['position_mm'])+shift
 layers=collections.defaultdict(list)
 for p in paths:
  if lo[0]-.1 <= (p['x']+p['x1'])/2<=hi[0]+.1 and lo[1]-.1 <= (p['y']+p['y1'])/2<=hi[1]+.1:
   layers[p['z']].append(p)
 assert layers,part['name'];previous=None;orphans=[];local={};ring_coverage=[];cup=[];bore=[]
 for zz,ps in sorted(layers.items()):
  fp=translate(reader.footprint(ps),-cx,-cy);local[zz]=fp
  polys=list(fp.geoms)if hasattr(fp,'geoms') else[fp]
  if previous is not None:
   for poly in polys:
    if poly.area>.005 and poly.intersection(previous.buffer(.01)).area<.001:orphans.append(dict(z_mm=zz,area_mm2=poly.area))
  previous=fp
  # Common 1.0mm radial core must stay open through every layer.
  area=fp.intersection(Point(0,0).buffer(1.0)).area;assert area<.001,(part['name'],zz,area);bore.append(area)
  if part['name'].startswith('input') and zz>2.12:
   od,idd=(4.7,2.4)if part['name']=='input-47' else(10,5.4)
   check=Point(0,0).buffer(od/2-.20).difference(Point(0,0).buffer(idd/2+.20))
   cover=fp.intersection(check).area/check.area;assert cover>.9,(part['name'],zz,cover);ring_coverage.append(cover)
  if part['name'].startswith('follower'):
   if zz<=1.48:
    for x in [-20,20]:assert fp.intersection(Point(x,0).buffer(.63)).area<.001,('eyelet closed',part['name'],zz)
   if zz>1.65:
    assert fp.intersection(Point(0,0).buffer(6.4)).area<.001,('cup filled',part['name'],zz)
    band=Point(0,0).buffer(7.8).difference(Point(0,0).buffer(7.0));coverage=fp.intersection(band).area/band.area;assert coverage>.85;cup.append(coverage)
 assert not orphans,(part['name'],orphans)
 report['parts'].append(dict(name=part['name'],layers=len(layers),top_z_mm=max(layers),bed_contact_mm2=local[min(local)].area,unsupported_islands=orphans,central_r1mm_open_all_layers=True,minimum_ring_inner_band_coverage=min(ring_coverage)if ring_coverage else None,minimum_cup_wall_band_coverage=min(cup)if cup else None))
 if part['name']in['base','input-47','input-100','follower-nominal-1']:
  target=3.72 if part['name'].startswith('input') else(.84 if part['name']=='base' else 2.92)
  chosen=min(local,key=lambda q:abs(q-target));plot.append((part['name'],chosen,layers[chosen],cx,cy))
out.write_text(json.dumps(report,indent=2)+'\n')
if '--plot' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axs=plt.subplots(2,2,figsize=(9,7))
 for ax,(name,z,ps,cx,cy)in zip(axs.flat,plot):
  for p in ps:ax.plot([p['x']-cx,p['x1']-cx],[p['y']-cy,p['y1']-cy],linewidth=max(.3,p['width']*3),color='#207c85')
  ax.set_aspect('equal');ax.set_title(f'{name} · Z{z:.2f} mm');ax.set_xlabel('mm');ax.set_ylabel('mm');ax.grid(alpha=.2)
 fig.tight_layout();fig.savefig(HERE/'images/toolpaths.svg');plt.close(fig)
print(json.dumps(dict(archive=project.name,parts=len(report['parts']),max_mesh_error_mm=err,all_checks_pass=True,gcode_estimates=report['gcode_estimates']),indent=2))
