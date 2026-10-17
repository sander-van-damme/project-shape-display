#!/usr/bin/env python3
"""Aggregate this one E-300 handoff; preserves all baseline tracked files."""
from pathlib import Path
import hashlib, json, subprocess, zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
TEST=ROOT/'owner-print-tests/2026-10-17-cone-friction-selector'
BASE='c341244ede59ce92ab63f8edd5bcb14907a87f6c'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    project=TEST/'cone-friction-selector.3mf'
    geom=json.loads((HERE/'review/geometry-review.json').read_text())
    array=json.loads((HERE/'review/array-review.json').read_text())
    assert not geom['unexpected_intersections']
    # The reviewer records a separate compact array report; inspect its explicit
    # failure field regardless of the total number of sampled neighbours.
    failkeys=[k for k in array if 'fail' in k or 'unexpected' in k]
    assert failkeys and all(not array[k] for k in failkeys),failkeys
    for n in ['screw','pin','screw-tree']:
        assert sha(HERE/'cad/parts'/(n+'.stl'))==sha(ROOT/'tools/curated-experiment-checks/E-299/cad/parts'/(n+'.stl'))
    layout=json.loads((TEST/'layout.json').read_text());assert len(layout)==17
    for row in layout:
        assert (ROOT/row['source']).exists()
    with zipfile.ZipFile(project) as z:
        config=json.loads(z.read('Metadata/project_settings.config'))
        assert config['printer_model']=='Bambu Lab X1 Carbon'
        assert config['nozzle_diameter']==['0.4']
        assert config['wall_generator']=='arachne'
        assert config['enable_support']=='0' and config['brim_type']=='no_brim'
        assert float(config['layer_height'])==.12
        assert len([n for n in z.namelist() if n.endswith('.gcode')])==1
    roundtrip=json.loads((TEST/'cone-friction-selector-build.json').read_text())['roundtrip']
    assert roundtrip['reopened_without_external_profiles']
    assert roundtrip['settings_differences']=={}
    # Git content hashes cover the complete source baseline without dumping it.
    entries=subprocess.check_output(['git','ls-tree','-r','-z',BASE],cwd=ROOT).split(b'\0')
    changed=[];count=0
    for entry in entries:
        if not entry:continue
        header,name=entry.split(b'\t');mode,kind,blob=header.split()
        if kind!=b'blob':continue
        p=ROOT/name.decode();count+=1
        actual=subprocess.check_output(['git','hash-object','--',str(p)],cwd=ROOT).strip() if p.exists() else b'MISSING'
        if actual!=blob:changed.append(name.decode())
    assert not changed,changed
    files={str(p.relative_to(ROOT)):sha(p) for folder in [HERE,TEST] for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='delivery-integrity.json'}
    record=dict(evidence='CAD, stored project, Bambu reopen and source integrity; no physical measurement',baseline_commit=BASE,baseline_tracked_files_checked=count,baseline_files_changed=changed,print_objects=len(layout),mechanical_parts_after_cleanup=18,project_sha256=sha(project),geometry_checks=geom['checks'],roundtrip=roundtrip,sha256=files)
    (HERE/'review/delivery-integrity.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['baseline_tracked_files_checked','baseline_files_changed','print_objects','project_sha256','geometry_checks']},indent=2))

if __name__=='__main__':main()
