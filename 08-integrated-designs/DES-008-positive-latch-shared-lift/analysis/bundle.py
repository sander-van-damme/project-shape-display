#!/usr/bin/env python3
"""Export reviewed source and owner articles, with unchanged timing dependencies.

This is a portable subset, not a replacement repository or a physical pass.
Only explicit deliverable directories are included; scratch/G-code are excluded.
"""
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

DESIGN = Path(__file__).resolve().parents[1]
REPO = DESIGN.parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    files = set()
    directories = [DESIGN,
                   REPO/'owner-print-tests/positive-pocket-memory',
                   REPO/'owner-print-tests/positive-rack-handoff']
    for directory in directories:
        if not directory.is_dir():
            raise RuntimeError(f'Missing release directory: {directory}')
        for path in directory.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.gcode'):
                files.add(path.relative_to(REPO))
    for name in json.loads((DESIGN/'analysis/dependency-files.json').read_text()):
        files.add(Path(name))
    for name in ['AGENTS.md', '01-project-description/shape-display-mission.md',
                 '02-design-criteria/current-prototype-priorities.md',
                 'owner-print-tests/AGENTS.md',
                 'owner-print-tests/short-thread-fit/test.md',
                 'owner-print-tests/trial5-short-replica/test.md',
                 'owner-print-tests/radial-pinch-four-pin/test.md']:
        files.add(Path(name))
    for path in files:
        if path.is_absolute() or '..' in path.parts or not (REPO/path).is_file():
            raise RuntimeError(f'Invalid or missing dependency: {path}')
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
        status = subprocess.check_output(['git', 'status', '--porcelain', '--',
                    str(DESIGN.relative_to(REPO)), 'owner-print-tests'], cwd=REPO, text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        commit, status = 'not exported from a Git checkout', 'unknown'
    manifest = {'commit': commit, 'release_paths_clean': not bool(status),
                'branch': 'codex/des008-multiplexed-lift',
                'baseline': 'b23ed12; 20ebaa1 main has identical net tree',
                'physical_validation': False,
                'files': {str(path): hashlib.sha256((REPO/path).read_bytes()).hexdigest()
                          for path in sorted(files)}}
    intro = '''SHAPE DISPLAY — DES-008 engineering decision package

Recommendation: test the support-transfer article; do not build a full display.
No complete architecture in this investigation is physically qualified or shown
to meet the full cost/playability requirements. Read the main design document
and final-disposition review before interpreting the timing estimates.

Source: https://github.com/sander-van-damme/project-shape-display
Branch: codex/des008-multiplexed-lift
Exact commit and file hashes: RELEASE-MANIFEST.json

Open owner-print-tests/positive-rack-handoff/test.md for the support-transfer
article. The positive-pocket-memory folder is a DEFERRED principle study.
Both retain ready-to-slice STL files, drawings and blank physical result forms.
No owner CAD export is needed. No G-code or purchased hardware is included.

The engineering package is in
08-integrated-designs/DES-008-positive-latch-shared-lift/.
Start with DES-008-positive-latch-shared-lift.md, then verification.md.
Run commands from this archive's top directory. Timing/cost use standard Python.
CAD checks additionally need OpenSCAD and analysis/requirements.txt packages.

This archive contains unchanged historical calculation dependencies, not the
entire historical repository. Other historical documents remain in the source
repository. Slicer estimates and nominal geometry are not physical test results.
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prefix = 'shape-display-des008/'
    with zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            archive.write(REPO/path, prefix+path.as_posix())
        archive.writestr(prefix+'RELEASE-MANIFEST.json', json.dumps(manifest, indent=2)+'\n')
        archive.writestr(prefix+'START-HERE.txt', intro)
    print(f'{args.output}: {len(files)} source/artifact files; release paths clean={not bool(status)}')


if __name__ == '__main__':
    main()
