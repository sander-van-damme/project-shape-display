import importlib.util,zipfile,json
from pathlib import Path
import numpy as np
from shapely.geometry import Point,box
root=Path(__file__).resolve().parents[4];sp=importlib.util.spec_from_file_location('v',root/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
folder=root/'owner-print-tests/2026-10-16-self-aligning-point-matrix';layout=json.loads((folder/'layout.json').read_text());
with zipfile.ZipFile(folder/'point-matrix.3mf') as archive:
 bounds,_,_,_=v.project_bounds(archive);settings=json.loads(archive.read('Metadata/project_settings.config'))
 source_min=np.min([p['bounds_mm'][0] for p in layout],axis=0);offset=np.array([float(v) for v in settings['extruder_offset'][0].split('x')]);dx,dy=bounds[0,:2]-source_min[:2]-offset
with zipfile.ZipFile(folder/'point-matrix.3mf') as z:paths,_=v.parse(z.read('Metadata/plate_1.gcode').decode())
ps=[p for p in paths if p['z']==.12];brim=v.footprint([p for p in ps if p['role']=='Brim']);model=v.footprint([p for p in ps if p['role']!='Brim']);rows=[]
for idx,part in enumerate(layout,1):
 if part['name'].split('#')[0]!='screw':continue
 lo,hi=np.array(part['bounds_mm']);cx,cy=(lo[:2]+hi[:2])/2+[dx,dy];region=box(cx-2.2,cy-2.2,cx+2.2,cy+2.2);m=model.intersection(region);b=brim.intersection(box(cx-5,cy-5,cx+5,cy+5));rows.append(dict(part=idx,model_firstlayer_area_mm2=m.area,brim_gap_from_model_mm=m.distance(b),brim_contact_area_mm2=m.intersection(b).area,firstlayer_model_bounds_mm=list(m.bounds)))
print(json.dumps(rows,indent=2));(folder/'brim-contact.json').write_text(json.dumps(rows,indent=2)+'\n')
