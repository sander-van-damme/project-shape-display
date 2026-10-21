"""Verify actual local brims and absence of automatic supports after reopening.
Usage: review_brim.py saved.3mf reopened.3mf
"""
import importlib.util,json,zipfile,hashlib,sys
import numpy as np
from pathlib import Path
from shapely.geometry import Point,box
from shapely.ops import unary_union
from paths import TEST_DIR,METADATA
spec=importlib.util.spec_from_file_location('reader',TEST_DIR.parent/'validate-bambu-project.py')
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
layout=json.loads((METADATA/'layout.json').read_text())
lo=np.min([p['bounds_mm'][0] for p in layout],axis=0)
rows=[]
for name in sys.argv[1:]:
 p=Path(name)
 with zipfile.ZipFile(p) as z:
  paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode())
  bounds,*_=reader.project_bounds(z);cfg=json.loads(z.read('Metadata/project_settings.config'))
 shift=bounds[0,:2]-lo[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')])
 brim=[q for q in paths if q['role']=='Brim'];assert brim
 assigned=set();objects=[]
 for source,width in [('rotor',2),('rotor-long-supported',3)]:
  part=next(p for p in layout if p['source']==source)
  cx,cy=np.array(part['center_xy'])+shift
  footprint=Point(cx,cy).buffer(3.5,resolution=128)
  if source=='rotor-long-supported':
   footprint=unary_union([footprint,*[box(cx+x-2,cy-4,cx+x+2,cy+4) for x in [-7.5,7.5]]])
  indices=[i for i,q in enumerate(brim) if footprint.distance(Point((q['x']+q['x1'])/2,(q['y']+q['y1'])/2))<width+.6]
  assert indices and not assigned.intersection(indices)
  distances=[footprint.distance(Point(q[x],q[y])) for i in indices for q in [brim[i]] for x,y in [('x','y'),('x1','y1')]]
  assert min(distances)>.05 and max(distances)<width+.6,distances
  assert all(brim[i]['z']==.12 for i in indices)
  assigned.update(indices)
  objects.append(dict(source=source,configured_width_mm=width,brim_segments=len(indices),path_distance_to_footprint_mm=[min(distances),max(distances)]))
 assert len(assigned)==len(brim),'Brim outside the two screw objects'
 assert not any('support' in q['role'].lower() for q in paths)
 rows.append(dict(project_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),brim_segments=len(brim),objects=objects,only_first_layer=True,pin_brim_segments=0,automatic_support_segments=0,modeled_supports='Eight necks / two towers on long screw; see long-screw-review'))
assert len(rows)==2
(METADATA/'brim-review.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
