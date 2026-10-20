"""Verify actual brim/support paths in saved and reopened projects.
Usage: review_brim.py saved.3mf reopened.3mf
"""
import importlib.util,json,zipfile,hashlib,sys
import numpy as np
from pathlib import Path
from paths import TEST_DIR,METADATA
spec=importlib.util.spec_from_file_location('reader',TEST_DIR.parent/'validate-bambu-project.py')
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
layout=json.loads((METADATA/'layout.json').read_text())
lo=np.min([p['bounds_mm'][0] for p in layout],axis=0)
rotor=next(p for p in layout if p['source']=='rotor')
rows=[]
for name in sys.argv[1:]:
 p=Path(name)
 with zipfile.ZipFile(p) as z:
  paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode())
  bounds,*_=reader.project_bounds(z);cfg=json.loads(z.read('Metadata/project_settings.config'))
  shift=bounds[0,:2]-lo[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')])
  center=np.array(rotor['center_xy'])+shift
  brim=[q for q in paths if q['role']=='Brim'];assert brim
  radii=[float(np.linalg.norm(np.array([q[x],q[y]])-center)) for q in brim for x,y in [('x','y'),('x1','y1')]]
  assert min(radii)>3.5 and max(radii)<6 and all(q['z']==.12 for q in brim)
  assert not any('support' in q['role'].lower() for q in paths)
  rows.append(dict(project_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),brim_segments=len(brim),radius_mm=[min(radii),max(radii)],only_around_rotor=True,only_first_layer=True,support_segments=0))
assert len(rows)==2
(METADATA/'brim-review.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
