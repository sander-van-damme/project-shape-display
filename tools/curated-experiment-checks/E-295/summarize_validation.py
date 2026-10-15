#!/usr/bin/env python3
"""Retain auditable check summaries and worst bridge cases, not raw scratch rows.
Usage: python summarize_validation.py input.json output.json
Full records are reproducible with independent_toolpath_review.py/bridge_review.py.
"""
import json
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[1:])
result = json.loads(source.read_text())
if isinstance(result, list):
    groups = {}
    for index, row in enumerate(result):
        groups.setdefault((row['z'], row['role']), []).append(index)
    selected = set()
    for indices in groups.values():
        for metric in ['length', 'max_free_centerline_mm', 'start_distance_mm', 'end_distance_mm']:
            selected.add(max(indices, key=lambda i: result[i][metric]))
    result = {
        'record_scope': 'Worst cases per layer/role; complete segment records remain reproducible scratch.',
        'segments_audited': len(result),
        'max_free_centerline_mm': max(row['max_free_centerline_mm'] for row in result),
        'max_anchor_distance_mm': max(max(row['start_distance_mm'], row['end_distance_mm']) for row in result),
        'retained_worst_cases': [result[i] for i in sorted(selected)],
    }
elif 'layers' in result:
    layers = result.pop('layers')
    result['record_scope'] = 'Summary of every audited layer; full layer records remain reproducible scratch.'
    result['layer_audit_summary'] = {
        'layers_audited': len(layers),
        'orphan_components_total': sum(row['orphan_components'] for row in layers),
        'max_midpoint_outside_previous_mm': max(row['max_midpoint_outside_previous_mm'] for row in layers),
    }
destination.write_text(json.dumps(result, indent=2) + '\n')
