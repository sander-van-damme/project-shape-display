#!/usr/bin/env python3
"""Independent comparison of every pre-existing tracked file against owner-feedback commit."""
import subprocess,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE='46a4117d5bbed2c5fc0669be62e27b7c1233a7e2'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
files=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
records=[]
for name in files:
    expected=hashlib.sha256(git('show',f'{BASE}:{name}')).hexdigest()
    p=ROOT/name
    actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    records.append({'path':name,'baseline_sha256':expected,'actual_sha256':actual,'unchanged':expected==actual})
out={'baseline_commit':BASE,'tracked_files_checked':len(records),'changed':[x for x in records if not x['unchanged']],'git_status':git('status','--short').decode(),'files':records}
Path(__file__).with_name('history-integrity.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['baseline_commit','tracked_files_checked','changed','git_status']},indent=2))
assert not out['changed']
