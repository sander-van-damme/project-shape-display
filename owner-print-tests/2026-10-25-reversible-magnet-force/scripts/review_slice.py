"""Inspect real deposited footprints, bores and layer support in saved Bambu projects."""
from pathlib import Path
import sys,json,zipfile,importlib.util,collections,re,hashlib
import numpy as np,trimesh
from scipy.spatial import cKDTree
from shapely.geometry import Point
from shapely.affinity import translate
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader',HERE.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
p=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 cfg=json.loads(z.read('Metadata/project_settings.config'));g=z.read('Metadata/plate_1.gcode').decode();bounds,instances,vertices,triangles=reader.project_bounds(z)
assert cfg['printer_settings_id']=='Bambu Lab X1 Carbon 0.4 nozzle'
assert cfg['layer_height']=='0.12' and cfg['initial_layer_print_height']=='0.2'
assert cfg['enable_support']=='0' and cfg['brim_type']=='no_brim'
assert ';===== machine: X1-0.4' in g and 'M190 S55' in g
paths,_=reader.parse(g);assert not any('support' in p['role'].lower() for p in paths)
mesh=trimesh.load(HERE/'components/reversible-magnet-force.stl',force='mesh');delta=bounds[0]-mesh.bounds[0]
err=max(cKDTree(vertices).query(mesh.vertices+delta)[0].max(),cKDTree(mesh.vertices+delta).query(vertices)[0].max());assert err<.00003
shift=delta[:2]-np.array([float(x)for x in cfg['extruder_offset'][0].split('x')])
layout=json.loads((HERE/'metadata/layout.json').read_text());assert len(instances)==len(layout)==6
reports=[];fig,axs=plt.subplots(2,3,figsize=(11,7))
for part,ax in zip(layout,axs.flat):
 name=part['name'];lo,hi=np.array(part['bounds_mm']);lo[:2]+=shift;hi[:2]+=shift;cx,cy=np.array(part['position_mm'])+shift
 layers=collections.defaultdict(list)
 for q in paths:
  if lo[0]-.1<=(q['x']+q['x1'])/2<=hi[0]+.1 and lo[1]-.1<=(q['y']+q['y1'])/2<=hi[1]+.1:layers[q['z']].append(q)
 assert layers;prev=None;orphans=[];maxfill=0;coverage=[]
 for zz,qs in sorted(layers.items()):
  fp=translate(reader.footprint(qs),-cx,-cy)
  if prev is not None:
   for poly in (fp.geoms if hasattr(fp,'geoms') else [fp]):
    if poly.area>.005 and poly.intersection(prev.buffer(.01)).area<.001:orphans.append([zz,poly.area])
  prev=fp
  check=None
  if name=='bobbin':
   check=Point(0,0).buffer(1.8)
   if zz>1:band=Point(0,0).buffer(2.3).difference(Point(0,0).buffer(2.1));coverage.append(fp.intersection(band).area/band.area)
  if name=='top-flange':check=Point(0,0).buffer(2.2)
  if name=='core-sleeve':check=Point(0,0).buffer(1.4)
  if name=='coil-bracket':check=Point(0,0).buffer(3.5)
  if name=='scale-foot' and zz>2.15:check=Point(0,0).buffer(3)
  if name=='magnet-arm' and zz>2.15:
   check=Point(10,0).buffer(3)
   if zz<4.9:assert fp.intersection(Point(-10,0).buffer(1.1)).area>3.5
  if check is not None:maxfill=max(maxfill,fp.intersection(check).area)
 assert maxfill<.001,(name,'closed bore',maxfill)
 assert not orphans,(name,'unsupported',orphans)
 if coverage:assert min(coverage)>.95,(name,min(coverage))
 pick=min(layers,key=lambda z:abs(z-(3.8 if hi[2]>4 else .56)))
 for q in layers[pick]:ax.plot([q['x']-cx,q['x1']-cx],[q['y']-cy,q['y1']-cy],lw=max(.3,q['width']*2.5))
 ax.set_aspect('equal');ax.set_title(f'{name} / z {pick:.2f} mm');ax.grid(alpha=.2)
 reports.append(dict(name=name,layers=len(layers),top_z_mm=max(layers),critical_bore_deposition_mm2=maxfill,unsupported_islands=orphans,minimum_barrel_band_coverage=min(coverage)if coverage else None))
fig.tight_layout()
if '--plot' in sys.argv:fig.savefig(HERE/'images/toolpaths.svg')
report=dict(project_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),parts=reports,max_mesh_error_mm=float(err),settings='X1C/0.4mm/PLA 210C/55C 0.12mm; no supports or brim',scope='Nominal actual slicer paths, NOT physical print evidence',estimates=[l for l in g.splitlines()if re.match(r'; (model printing time|total filament)',l)],zip_crc_valid=True)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if "--plot" in sys.argv:
 svg=HERE/"images/toolpaths.svg"
 svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines())+"\n")
