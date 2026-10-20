"""Actual Bambu toolpaths, layer connectivity and critical feature checks.
Usage: review_slice.py PROJECT OUT.json. Does not establish physical fit.
"""
import sys,json,zipfile,hashlib,importlib.util,collections,math,re
from pathlib import Path
import numpy as np
from shapely.geometry import Point,Polygon,LineString
from shapely.affinity import translate
from scipy.spatial import cKDTree
from paths import *
spec=importlib.util.spec_from_file_location('reader',TEST_DIR.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
project=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(project)as archive:
 cfg=json.loads(archive.read('Metadata/project_settings.config'));gcode=archive.read('Metadata/plate_1.gcode').decode();paths,_=reader.parse(gcode);bounds,instances,vertices,triangles=reader.project_bounds(archive)
layout=json.loads((METADATA/'layout.json').read_text());source_lo=np.min([p['bounds_mm'][0]for p in layout],axis=0)
shift=bounds[0,:2]-source_lo[:2]-np.array([float(x)for x in cfg['extruder_offset'][0].split('x')])
import trimesh
mesh=trimesh.load(COMPONENTS/'microstepper-frame-v3.stl',force='mesh');shift3=bounds[0]-mesh.bounds[0];points=mesh.vertices+shift3
error=max(cKDTree(vertices).query(points)[0].max(),cKDTree(points).query(vertices)[0].max());assert error<.00003,error
assert not any('support' in p['role'].lower()for p in paths)
report=dict(scope='Nominal deposited paths; no physical reliability claim',project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),max_mesh_vertex_error_mm=float(error),parts=[],stats=[s for s in gcode.splitlines()if re.search(r'(total estimated time|total filament|model printing time)',s)])
plot=[]
for part in layout:
 lo,hi=np.array(part['bounds_mm']);lo[:2]+=shift;hi[:2]+=shift;cx,cy=np.array(part['center_xy'])+shift
 layers=collections.defaultdict(list)
 for p in paths:
  if lo[0]-.05<=(p['x']+p['x1'])/2<=hi[0]+.05 and lo[1]-.05<=(p['y']+p['y1'])/2<=hi[1]+.05 and p['role']!='Skirt':layers[p['z']].append(p)
 previous=None;orphans=[];bridges=[];features=[];tip_r=[];core_coverage=[];annulus_coverage=[];local={}
 for z,ps in sorted(layers.items()):
  fp=translate(reader.footprint(ps),-cx,-cy);local[z]=fp;polys=list(fp.geoms)if hasattr(fp,'geoms')else[fp]
  if previous is not None:
   for poly in polys:
    if poly.area>.005 and poly.intersection(previous.buffer(.01)).area<.001:orphans.append(dict(z=z,area=poly.area,bounds_mm=list(poly.bounds)))
   for p in ps:
    if 'bridge' in p['role'].lower():
     line=LineString([(p['x']-cx,p['y']-cy),(p['x1']-cx,p['y1']-cy)]);free=line.difference(previous.buffer(.01))
     bridges.append(dict(z=z,free_span_mm=max((q.length for q in (list(free.geoms)if hasattr(free,'geoms')else[free])),default=0),ends_mm=[Point(line.coords[i]).distance(previous.buffer(.01))for i in[0,-1]]))
  if part['source']=='rotor':
   if .36<=z<=5.88:
    def radius(a):
     a=math.radians(a);hit=fp.intersection(LineString([(0,0),(2*math.cos(a),2*math.sin(a))]));return Point(0,0).distance(hit)if not hit.is_empty else 2
    tips=[radius(a)for a in[0,120,240]];valleys=[radius(a)for a in[60,180,300]]
    features.append(dict(z=z,core_open=fp.intersection(Point(0,0).buffer(.8)).area<.001,contrast=min(valleys)-max(tips),tips=tips))
   if 12.12<=z<=27.36:
    core_coverage.append(fp.intersection(Point(0,0).buffer(.5)).area/Point(0,0).buffer(.5).area)
    annulus=Point(0,0).buffer(.68).difference(Point(0,0).buffer(.58))
    annulus_coverage.append(fp.intersection(annulus).area/annulus.area)
    assert len([poly for poly in polys if poly.area>.02])==1,('disconnected thread contour',z)
    assert fp.area>1.5,('missing thread body',z,fp.area)
    coords=np.concatenate([np.asarray(p.exterior.coords)for p in polys if p.geom_type=='Polygon']);tip_r.append([z,float(np.linalg.norm(coords,axis=1).max())])
  if part['source']=='pin':
   assert fp.intersection(Point(0,0).buffer(.6)).area<.001,('pin bore',z)
   if z>6.12:assert any(p.geom_type=='Polygon' and Polygon(p.exterior).contains(Point(0,0))for p in polys),('upper pin closed',z)
  previous=fp
 summary=dict(name=part['name'],layers=len(layers),top_z_mm=max(layers),bed_contact_mm2=local[min(local)].area,unsupported_islands=orphans,bridges=bridges)
 assert not orphans,(part['name'],orphans)
 assert all(max(b['ends_mm'])<.02 and b['free_span_mm']<3 for b in bridges),('unanchored or long bridge',part['name'])
 if part['source']=='rotor':
  assert len(features)>=46 and all(r['core_open']and r['contrast']>.12 for r in features),features
  assert len(tip_r)>120
  turns=[]
  for i in range(5):
   vals=[r for z,r in tip_r if 12+i*3<z<=15+i*3];turns.append(max(vals));assert max(vals)>1.45
  summary.update(lobe_layers=len(features),minimum_lobe_contrast_mm=min(r['contrast']for r in features),lobe_tip_radius_range_mm=[min(min(r['tips'])for r in features),max(max(r['tips'])for r in features)],thread_connected_body_layers=len(tip_r),minimum_core_r050_coverage=min(core_coverage),minimum_annulus_r058_068_coverage=min(annulus_coverage),thread_turn_max_radii_mm=turns)
  for z,title in[(3,'C ribben / open holte'),(6.12,'Dak tandwielholte'),(15,'Korte schroefdraad')]:plot.append((title,part,min(local,key=lambda x:abs(x-z)),layers,cx,cy))
 if part['source'] in ['front','back']:
  fp=local[min(local,key=lambda z:abs(z-5.4))]
  assert fp.intersection(Polygon([(-2.2,33),(2.2,33),(2.2,72.5),(-2.2,72.5)])).area<.001, 'Guide channel obstructed'
  for y in np.arange(41,72,.5):
   for x in [-3.2,3.2]:
    assert fp.intersection(Point(x,y).buffer(.4)).area>.1, ('Missing guide wall',part['source'],x,y)
  summary['guide_channel_and_walls_checked_mm']=[33,72.5]
 if part['source']=='back':
  fp=local[min(local,key=lambda z:abs(z-5.4))]
  for x,y in[(11.5,6),(-11.5,29.7)]:assert fp.intersection(Point(x,y).buffer(1.3)).area<.001
  summary['alignment_holes_r130_open_at_z540']=True
  plot.append(('Rond + langwerpig pasgat',part,5.4,layers,cx,cy))
 if part['source']=='front':
  for z,fp in local.items():
   if 6.6<=z<=8.76:
    for x,y in[(-11.5,6),(11.5,29.7)]:assert fp.intersection(Point(x,y).buffer(1.1)).area/Point(x,y).buffer(1.1).area>.95,('peg',z)
  summary['both_peg_cores_continuous']=True
 if part['source'].startswith('spacer'):
  t=int(part['source'].split('-')[1])/100
  summary['full_body_layers']=sum(z<=t+.001 for z in layers)
  assert summary['full_body_layers']==round(t/.12)
 report['parts'].append(summary)
(METADATA/'saved-settings.json').write_text(json.dumps(cfg,indent=2)+'\n')
out.write_text(json.dumps(report,indent=2)+'\n')
if not out.stem.endswith('reopened'):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(2,2,figsize=(10,9))
 for ax,(title,part,z,layers,cx,cy)in zip(axes.flat,plot):
  ps=layers[min(layers,key=lambda v:abs(v-z))]
  for p in ps:ax.plot([p['x']-cx,p['x1']-cx],[p['y']-cy,p['y1']-cy],lw=max(.5,p['width']*5),color='#cc6335'if 'bridge'in p['role'].lower()else'#216e83')
  ax.set_aspect('equal');ax.set_title(f'{title} — laag Z{z:g}');ax.set_xlabel('mm');ax.grid(alpha=.2)
  if part['source']=='rotor':
   lim=1.8 if z<6 or z>12 else 4;ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim)
 fig.tight_layout();fig.savefig(IMAGES/'toolpaths.png',dpi=160)
print(json.dumps({**report,'parts':[{k:v for k,v in p.items()if k!='bridges'}for p in report['parts']]},indent=2))
