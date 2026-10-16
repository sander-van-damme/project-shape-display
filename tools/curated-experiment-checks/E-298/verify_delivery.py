"""Check saved deliverables, provenance and preservation; no physical qualification."""
from pathlib import Path
import ast, hashlib, json, re, subprocess, sys, zipfile
from urllib.parse import unquote, urlsplit
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
BASE='f7721f3abbf2cc35fb59dd5440c5d0b1c42d1315'
TESTS=[ROOT/('owner-print-tests/2026-10-16-self-aligning-point-'+x) for x in ['fit','matrix']]
errors=[];checks=0

def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

for p in HERE.rglob('*.py'):ast.parse(p.read_text(),filename=str(p));checks+=1
for rec in read(HERE/'mesh-contact-envelope.json')['variants']:
 check(sha(HERE/'cad/parts'/(rec['name']+'.stl'))==rec['source_sha256'],'stale contact mesh '+rec['name'])
g=read(HERE/'cad/validation.json');check(g['pass_nominal'] and not g['unexpected_intersections'],'CAD collisions')
for name,value in g['unchanged_E297_source_sha256'].items():
 check(sha(HERE/'cad/parts'/name)==value,'Changed inherited CAD '+name)
 check(sha(HERE.parent/'E-297/cad/parts'/name)==value,'Changed original CAD '+name)
for rec in read(HERE/'print-and-assembly.sources.json')['sources']:
 check(sha(ROOT/rec['path'])==rec['sha256'],'stale PDF '+rec['path'])
mp=read(HERE/'cad/mixed-phase-path.json')
check(mp['pass_nominal'] and not mp['unexpected_intersections'],'mixed phase geometry')
check(sha(HERE/'mesh-contact-envelope.json')==mp['source_envelope_sha256'],'stale mixed phase envelope')
projects=[]
for test in TESTS:
 stem='point-fit' if test.name.endswith('fit') else 'point-matrix'
 project=test/(stem+'.3mf');build=read(test/(stem+'-build.json'))
 check(sha(project)==build['final_project_sha256'],'stale build '+stem)
 rt=build['roundtrip'];check(rt['reopened_without_external_profiles'] and rt['return_code']==0,'reopen failed '+stem)
 check(not rt['settings_differences'],'reopen changed settings '+stem)
 with zipfile.ZipFile(project) as z:
  check(z.testzip() is None,'corrupt project '+stem)
  s=json.loads(z.read('Metadata/project_settings.config'));gc=z.read('Metadata/plate_1.gcode')
  check(s['printer_model']=='Bambu Lab X1 Carbon','printer '+stem)
  check(s['nozzle_diameter']==['0.4'],'nozzle '+stem)
  check(s['enable_support']=='0','supports '+stem)
  check(s['min_bead_width']=='75%' and s['min_feature_size']=='10%','Arachne settings '+stem)
  check(s['filament_type']==['PLA'],'filament '+stem)
  check(s['layer_height']=='0.08','layers '+stem)
  check(s['initial_layer_print_height']=='0.12','first layer '+stem)
  check(len(gc)>10000,'missing real Gcode '+stem)
 projects.append({'file':str(project.relative_to(ROOT)),'sha256':sha(project),'embedded_gcode_sha256':hashlib.sha256(gc).hexdigest(),'reopen_verified':True})
 sv=read(test/'slicer-review.json')
 check(sv['project_sha256']==sha(project),'stale toolpath review '+stem)
 check(sv['gcode_sha256']==hashlib.sha256(gc).hexdigest(),'stale toolpath Gcode '+stem)
 check(not sv['unsupported_layer_components'],'floating extrusion layers '+stem)
 pp=read(test/'point-paths.json')
 check(len(pp['samples'])==(12 if stem=='point-fit' else 8),'missing point specimens '+stem)
 for sample in pp['samples']:
  check(sample['top_extrusion_mm']>=8.35,'missing taper '+sample['name'])
 rc=read(test/'reopened-critical-paths.json')
 check(bool(rc['summary']),'missing reopened critical checks '+stem)
 if stem=='point-fit':
  rp=read(test/'reopened-point-paths.json')
  check([x['top_extrusion_mm'] for x in rp['samples']]==[x['top_extrusion_mm'] for x in pp['samples']],'reopened tip heights changed')
 tag='A' if test.name.endswith('fit') else 'B'
 ar=read(HERE/f'independent-review-archive-geometry-{tag}.json')
 check(ar['project_sha256']==sha(project),'stale independent archive '+tag)
 check(ar['all_closed'] and ar['all_facet_counts_equal'],'archive geometry '+tag)

# Preservation is checked against the fixed starting commit, not a moving branch.
oldpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'owner-print-tests','tools/curated-experiment-checks/E-297','06-experiments'],cwd=ROOT,text=True).splitlines()
preserved=[]
for name in oldpaths:
 if name.startswith('06-experiments/') and '/E-297-' not in name:continue
 original=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
 check((ROOT/name).read_bytes()==original,'Changed preserved file '+name)
 preserved.append(name)
docs=list(HERE.rglob('*.md'))+[p for t in TESTS for p in t.glob('*.md')]+[ROOT/'06-experiments/E-298-self-aligning-point-clutch.md']
for p in docs:
 for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  u=urlsplit(target.strip('<>'))
  if not u.scheme and u.path:
   linked=(p.parent/unquote(u.path)).resolve()
   check(linked.exists() or linked==HERE/'validation/delivery-integrity.json',f'Broken link {p.relative_to(ROOT)}: {target}')
if (HERE/'provenance.json').exists():
 for item in read(HERE/'provenance.json')['files']:
  check(sha(ROOT/item['path'])==item['sha256'],'stale package file '+item['path'])
result={'scope':'Saved package integrity and existing-file preservation; not physical validation','base_commit':BASE,'checks':checks,'errors':errors,'preserved_old_file_count':len(preserved),'preserved_all_checked':not any('preserved' in e for e in errors),'projects':projects}
(HERE/'validation/delivery-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
