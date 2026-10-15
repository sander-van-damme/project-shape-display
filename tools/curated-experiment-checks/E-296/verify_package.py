#!/usr/bin/env python3
"""Verify retained evidence and local links without recomputing CAD contacts."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    provenance = json.loads((HERE / 'provenance.json').read_text())
    failures = []
    for relative, expected in provenance['sha256'].items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f'Missing: {relative}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f'Changed since evidence was recorded: {relative}')

    docs = list(HERE.glob('*.md')) + [
        ROOT / '06-experiments/E-296-compact-matrix-clutch-selection.md']
    links = 0
    for document in docs:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            path = target.split('#', 1)[0]
            links += 1
            if not (document.parent / path).exists():
                failures.append(f'Broken link in {document.name}: {target}')

    cad = json.loads((HERE / 'validation.json').read_text())
    if not cad['pass']:
        failures.append('Retained CAD validation did not pass')
    for state in cad['brep_states']:
        if state['unexpected_intersections'] or state['invalid_parts']:
            failures.append(f'Invalid retained BREP result: {state["state"]}')
    print(json.dumps(dict(
        pass_package=not failures,
        hashed_files=len(provenance['sha256']),
        local_links=links,
        brep_states=len(cad['brep_states']),
        rigid_boolean_pairs=sum(s['boolean_pairs_checked_after_aabb'] for s in cad['brep_states']),
        axial_float_probes=len(cad['axial_float_to_selector_probes']),
        failures=failures,
        evidence='File integrity and retained analytical/CAD results; no physical qualification'
    ), indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
