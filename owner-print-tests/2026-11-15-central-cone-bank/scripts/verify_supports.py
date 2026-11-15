#!/usr/bin/env python3
"""Locate actual bank-only supports and supported bridge spans; no physical claim."""
from pathlib import Path
import argparse,json,zipfile,importlib.util,hashlib
import numpy as np
from shapely.geometry import LineString
from shapely.ops import unary_union
p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('output',type=Path);a=p.parse_args();P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader',P.parents[1]/'owner-print-tests/validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
with zipfile.ZipFile(a.project) as z:
 paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode());bounds,*_=reader.project_bounds(z);cfg=json.loads(z.read('Metadata/project_settings.config'))
rows=json.loads((P/'metadata/layout.json').read_text())['mechanical'];original=np.array([r['bounds_mm'] for r in rows]);shift=bounds[0]-original[:,0,:].min(axis=0)
offset=cfg.get('extruder_offset',['0x0']);offset=offset[0] if isinstance(offset,list) else offset;shift[:2]-=np.array([float(v) for v in offset.split('x')]);r=next(r for r in rows if r['source']=='bank');lo,hi=np.array(r['bounds_mm'])+shift
inside=lambda q,l,h,margin=.5:l[0]-margin<=(q['x']+q['x1'])/2<=h[0]+margin and l[1]-margin<=(q['y']+q['y1'])/2<=h[1]+margin
supports=[q for q in paths if 'support' in q['role'].lower()]
assert supports,'Bank roof requires actual supports'
assert all(inside(q,lo,hi,5) for q in supports),'Support outside bank footprint'
for r in rows:
 if r['source']=='bank':continue
 l,h=np.array(r['bounds_mm'])+shift
 assert not any(inside(q,l,h) for q in supports),r['name']
bankpaths=[q for q in paths if inside(q,lo,hi) and q['role'] not in ['Brim','Skirt']]
levels=sorted(set(q['z'] for q in bankpaths));bridges=[];cache={}
for q in bankpaths:
 if 'bridge' not in q['role'].lower():continue
 z=q['z']
 key=(z,q['height'])
 if key not in cache:
  under=[v for v in bankpaths if .05<z-v['z']<q['height']+.15];cache[key]=reader.footprint(under).buffer(.01)
 free=LineString([(q['x'],q['y']),(q['x1'],q['y1'])]).difference(cache[key]);pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
 bridges.append(dict(z_mm=z,max_free_segment_with_model_or_support_below_bead_height_plus015_mm=max((v.length for v in pieces),default=0)))
report=dict(project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),support_paths=len(supports),supports_exclusively_bank=True,bank_support_foundation_allowance_mm=5,support_z_mm=sorted(set(q['z'] for q in supports)),maximum_bridge_free_segment_with_support_mm=max((r['max_free_segment_with_model_or_support_below_bead_height_plus015_mm'] for r in bridges),default=0),bridges=bridges,scope='Deposited support below roof within deposited bead height plus0.15mm support gap; does not prove bridge adhesion, removal or strength.')
a.output.write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['bridges','support_z_mm']})
