#!/usr/bin/env python3
"""Final package audit, including current generated STLs versus saved Bambu projects."""
from pathlib import Path
import argparse,ast,hashlib,json,re,zipfile,importlib.util,subprocess
import numpy as np,trimesh
from scipy.spatial import cKDTree
P=Path(__file__).resolve().parents[1];R=P.parents[1];M=P/'metadata'
a=argparse.ArgumentParser();a.add_argument('--baseline-check',type=Path,required=True);opts=a.parse_args()
for f in (P/'scripts').glob('*.py'):ast.parse(f.read_text(),filename=str(f))
links=[]
for f in P.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if ':' in target or target.startswith('#'):continue
  assert (f.parent/target.split('#')[0]).exists(),(f.name,target)
  links.append([f.name,target])
spec=importlib.util.spec_from_file_location('reader',P.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
project_checks={}
for short,name in [('A','A-first'),('BC','BC-comparisons')]:
 project=P/(name+'.3mf');build=json.loads((M/(name+'-build.json')).read_text());digest=hashlib.sha256(project.read_bytes()).hexdigest();assert digest==build['project_sha256']
 with zipfile.ZipFile(project) as z:bounds,instances,verts,tris=reader.project_bounds(z);settings=json.loads(z.read('Metadata/project_settings.config'))
 assert settings['printer_settings_id']=='Bambu Lab X1 Carbon 0.4 nozzle'
 mesh=trimesh.load(P/'components'/(name+'.stl'),force='mesh');shift=bounds[0]-mesh.bounds[0]
 err=max(cKDTree(verts).query(mesh.vertices+shift)[0].max(),cKDTree(mesh.vertices+shift).query(verts)[0].max());assert err<.00004,err
 for suffix in ['', '-reopened']:
  rev=json.loads((M/(short+'-slice-review'+suffix+'.json')).read_text())
  expected=digest if not suffix else build['reopened_project_sha256'];assert rev['project_sha256']==expected
  assert rev['support_paths']==0
  assert all(not row['orphan_components'] for row in rev['parts'])
 project_checks[name]=dict(current_mesh_max_vertex_error_mm=float(err),objects=len(instances),archive_sha256=digest,saved_and_reopened_reviews_match_hashes=True)
geometry=json.loads((M/'geometry-review.json').read_text());assert len(geometry['sampled_motion_states'])==122 and len(geometry['pin40_endpoint_checks'])==4 and len(geometry['fixture_checks'])==4
r=subprocess.run([str(R/'repo'),'check'],capture_output=True,text=True,cwd=R);repo_output=r.stdout+r.stderr;baseline=opts.baseline_check.read_text();assert repo_output==baseline,(repo_output,baseline)
diff=subprocess.run(['git','diff','HEAD','--check'],capture_output=True,text=True,cwd=R);assert diff.returncode==0,diff.stdout+diff.stderr
manifest={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.rglob('*')) if f.is_file() and f.name!='delivery-checks.json' and '__pycache__' not in f.parts}
report=dict(status='READY_FOR_BOUNDED_PHYSICAL_TESTS_NOT_PHYSICALLY_VALIDATED',date='2026-10-25',source_main='1071f695b93951246a2865038e7fb9de9bdf2a05',projects=project_checks,geometry_samples=122,pin40_endpoint_checks=4,fixture_conditions=4,local_markdown_links_verified=len(links),python_sources_parse=True,git_diff_check='PASS',repository_check=dict(return_code=r.returncode,output=repo_output,identical_to_clean_main=True),physical_test_performed=False,manifest_sha256=manifest)
(M/'delivery-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='manifest_sha256'},indent=2))
