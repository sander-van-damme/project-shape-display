#!/usr/bin/env python3
"""Compare actual saved/reopened Bambu triangle geometry to delivered plate meshes."""
from pathlib import Path
import argparse,importlib.util,zipfile,json,hashlib
import numpy as np,trimesh
from scipy.spatial import cKDTree
p=argparse.ArgumentParser();p.add_argument('--reopened-mechanical',type=Path,required=True);p.add_argument('--reopened-actuator',type=Path,required=True);a=p.parse_args();P=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('reader',P.parents[1]/'owner-print-tests/validate-bambu-project.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def face_error(first,second):
 candidates=cKDTree(second.mean(axis=1)).query(first.mean(axis=1),k=8)[1];nearby=second[candidates]
 distances=[np.linalg.norm(first[:,None]-np.roll(nearby,shift,axis=2),axis=3).max(axis=2) for shift in range(3)]
 return float(np.min(np.stack(distances),axis=(0,2)).max())
rows=[]
for name,reopen in [('mechanical',a.reopened_mechanical),('actuator',a.reopened_actuator)]:
 mesh=trimesh.load(P/'components'/(name+'.stl'),force='mesh')
 for project in [P/(name+'.3mf'),reopen]:
  with zipfile.ZipFile(project) as z:bounds,_,vv,ff=r.project_bounds(z)
  shift=bounds[0]-mesh.bounds[0];sv=mesh.vertices+shift;sf=mesh.triangles+shift
  ve=max(cKDTree(vv).query(sv)[0].max(),cKDTree(sv).query(vv)[0].max());fe=max(face_error(ff,sf),face_error(sf,ff))
  assert len(ff)==len(mesh.faces) and ve<.00003 and fe<.00003,(project,ve,fe)
  rows.append(dict(project=project.name,reopened=project==reopen,sha256=hashlib.sha256(project.read_bytes()).hexdigest(),source_mesh_facets=len(mesh.faces),archive_facets=len(ff),maximum_vertex_error_mm=float(ve),maximum_winding_preserving_triangle_error_mm=fe))
(P/'metadata/archive-geometry-review.json').write_text(json.dumps(dict(scope='Actual archive meshes vs delivered source; no physical claim',projects=rows),indent=2)+'\n');print('PASS',len(rows),'archive comparisons')
