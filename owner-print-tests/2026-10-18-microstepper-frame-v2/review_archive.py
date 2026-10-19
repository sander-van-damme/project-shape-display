"""Verify delivered meshes/settings and bind every path review to its project hash."""
from pathlib import Path
import importlib.util,json,zipfile,hashlib
import numpy as np,trimesh
from scipy.spatial import cKDTree
h=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',h.parent/'validate-bambu-project.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
p=h/'microstepper-frame-v2.3mf'
with zipfile.ZipFile(p) as z:
 b,objects,points,_=r.project_bounds(z);settings=json.loads(z.read('Metadata/project_settings.config'))
m=trimesh.load(h/'microstepper-frame-v2.stl',force='mesh');v=m.vertices+(b[0]-m.bounds[0]);error=max(cKDTree(points).query(v)[0].max(),cKDTree(v).query(points)[0].max())
assert error<.0001 and len(objects)==8
assert settings['printer_model']=='Bambu Lab X1 Carbon' and settings['nozzle_diameter']==['0.4'] and settings['enable_support']=='0'
spec2=importlib.util.spec_from_file_location('builder',h/'build_project.py');builder=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(builder)
with zipfile.ZipFile(p) as z: local=builder.object_settings(z)
assert len(local)==8 and all(v.get('enable_support')=='0' for v in local.values())
assert next(v for k,v in local.items() if k.endswith('screw-50-supported'))['brim_width']=='3'
sha=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['lobe-review-original.json','support-review.json','pin-review.json','long-screw-review.json']:
 assert json.loads((h/n).read_text())['project_sha256']==sha,n
(h/'archive-validation.json').write_text(json.dumps(dict(objects=len(objects),bidirectional_vertex_error_mm=error,printer=settings['printer_model'],nozzle=settings['nozzle_diameter'],reports_match_project_sha256=True,project_sha256=sha),indent=2)+'\n')
print('Final geometry/archive match passed',error)
