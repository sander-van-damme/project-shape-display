import sys,json,zipfile,hashlib,importlib.util,collections,math
from pathlib import Path
import numpy as np
from shapely.geometry import LineString,Point
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('reader',root/'owner-print-tests/validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
here=root/'owner-print-tests/2026-10-18-microstepper-frame-v2'
project=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(project) as z:
 cfg=json.loads(z.read('Metadata/project_settings.config'));paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode());bounds,*_=reader.project_bounds(z)
layout=json.loads((here/'layout.json').read_text());source_lo=np.min([p['bounds_mm'][0] for p in layout],axis=0)
shift=bounds[0,:2]-source_lo[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')])
report={'scope':'Independent deposited-path footprint review; nominal line widths are not physical measurements.','parts':[]};plots=[]
for part in layout:
 if not part['source'].startswith('coupling'):continue
 cx,cy=np.array(part['center_xy'])+shift
 layers=collections.defaultdict(list)
 for p in paths:
  if abs((p['x']+p['x1'])/2-cx)<6.6 and abs((p['y']+p['y1'])/2-cy)<6.6 and 9.48<=p['z']<=15.00:layers[p['z']].append(p)
 rows=[]
 for z,ps in sorted(layers.items()):
  fp=reader.footprint(ps);center=Point(cx,cy)
  def radius(a):
   rad=math.radians(a);hit=LineString([(cx,cy),(cx+2*math.cos(rad),cy+2*math.sin(rad))]).intersection(fp)
   return center.distance(hit) if not hit.is_empty else 2
  tips=[radius(a) for a in (0,120,240)];valleys=[radius(a) for a in (60,180,300)]
  rows.append({'z':z,'tip_radii':tips,'valley_radii':valleys,'min_contrast':min(valleys)-max(tips),'core_r080_open':fp.intersection(center.buffer(.8)).area<.001})
  if abs(z-12)<.01:plots.append((part['name'],ps,cx,cy))
 report['parts'].append({'name':part['name'],'layers':len(rows),'min_contrast_mm':min(r['min_contrast'] for r in rows),'tip_radius_range_mm':[min(min(r['tip_radii']) for r in rows),max(max(r['tip_radii']) for r in rows)],'valley_radius_range_mm':[min(min(r['valley_radii']) for r in rows),max(max(r['valley_radii']) for r in rows)],'all_core_r080_open':all(r['core_r080_open'] for r in rows),'layer_details':rows})
report['project_sha256']=hashlib.sha256(project.read_bytes()).hexdigest()
assert all(p['layers']==47 and p['min_contrast_mm']>.14 and p['all_core_r080_open'] for p in report['parts'])
out.write_text(json.dumps(report,indent=2)+'\n')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,2,figsize=(8,3.5))
for ax,(name,ps,cx,cy) in zip(axes,plots):
 for p in ps:ax.plot([p['x']-cx,p['x1']-cx],[p['y']-cy,p['y1']-cy],linewidth=max(.5,p['width']*7),color='#286d8c',solid_capstyle='round')
 ax.set_aspect('equal');ax.set_xlim(-1.7,1.7);ax.set_ylim(-1.7,1.7);ax.set_title(name+' at Z=12 mm');ax.set_xlabel('mm');ax.grid(alpha=.15)
fig.tight_layout();fig.savefig(out.with_suffix('.png'),dpi=180)
print(json.dumps([{k:v for k,v in p.items() if k!='layer_details'} for p in report['parts']],indent=2))
