#!/usr/bin/env python3
"""Arrange already oriented rack-coupon parts without changing functional CAD.

Requires numpy and trimesh. Meshes remain separate bodies. This verifies a
nonoverlapping print arrangement, not support paths or physical print success.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
import trimesh


def pack(items, size, gap, strategy):
    free = [(0., 0., size, size)]
    placed = []
    order = sorted(items, key=lambda i: (max(i['xy']), min(i['xy'])) if strategy == 'longest' else (math.prod(i['xy']), max(i['xy'])), reverse=True)
    for item in order:
        candidates = []
        for i, (x,y,w,h) in enumerate(free):
            for angle in (0, 90):
                a,b = item['xy'] if angle == 0 else item['xy'][::-1]
                a += gap; b += gap
                if a <= w+1e-8 and b <= h+1e-8:
                    candidates.append(((min(w-a,h-b),max(w-a,h-b),y,x),i,angle,a,b))
        if not candidates: return None
        _,index,angle,a,b = min(candidates)
        x,y,_,_ = free[index]
        used = (x,y,a,b)
        new = []
        for fx,fy,fw,fh in free:
            if x+a <= fx or x >= fx+fw or y+b <= fy or y >= fy+fh:
                new.append((fx,fy,fw,fh)); continue
            if x > fx: new.append((fx,fy,x-fx,fh))
            if x+a < fx+fw: new.append((x+a,fy,fx+fw-x-a,fh))
            if y > fy: new.append((fx,fy,fw,y-fy))
            if y+b < fy+fh: new.append((fx,y+b,fw,fy+fh-y-b))
        free = []
        for i,r in enumerate(new):
            rx,ry,rw,rh = r
            contained = any(i != j and sx <= rx+1e-8 and sy <= ry+1e-8 and sx+sw >= rx+rw-1e-8 and sy+sh >= ry+rh-1e-8 and (s != r or j < i)
                            for j,s in enumerate(new) for sx,sy,sw,sh in [s])
            if not contained: free.append(r)
        placed.append(dict(item, x=x+gap/2, y=y+gap/2, angle=angle))
    return placed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parts', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--gap', type=float, default=4.)
    args = ap.parse_args()
    manifest = json.loads((args.parts/'manifest.json').read_text())
    meshes = {}; items = []
    for name,info in manifest['parts'].items():
        path = args.parts/(name+'.stl')
        m = trimesh.load_mesh(path)
        assert m.is_volume and len(m.split()) == 1, name
        assert m.bounds[0,2] > -1e-4, (name,m.bounds)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if 'stl_sha256' in info: assert digest == info['stl_sha256'], name
        m.apply_translation(-m.bounds[0]); meshes[name] = m
        for index in range(info['quantity']):
            items.append(dict(name=name,index=index,xy=list(map(float,m.extents[:2]))))
    options = []
    for size in range(100,226,5):
        for strategy in ('longest','area'):
            result = pack(items,size,args.gap,strategy)
            if result is not None: options.append((size,strategy,result))
        if options: break
    if not options: raise RuntimeError('Parts do not fit a 225 mm plate; revise deliberately')
    size,strategy,placed = min(options, key=lambda r:(r[0],r[1]))
    result = []; records = []
    for item in placed:
        m = meshes[item['name']].copy()
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(item['angle']),[0,0,1]))
        m.apply_translation(-m.bounds[0]+[item['x'],item['y'],0])
        result.append(m)
        records.append({k:v for k,v in item.items() if k!='xy'} | {'bounds_mm':m.bounds.tolist()})
    for a,b in itertools.combinations(result,2):
        assert np.any(np.minimum(a.bounds[1,:2],b.bounds[1,:2])-np.maximum(a.bounds[0,:2],b.bounds[0,:2]) <= -args.gap+1e-5)
    plate = trimesh.util.concatenate(result)
    assert plate.is_volume and len(plate.split()) == len(items)
    assert abs(plate.volume-sum(m.volume for m in result)) < .01
    args.output.mkdir(parents=True,exist_ok=True)
    target = args.output/'four-pin-handoff-plate.stl'; plate.export(target)
    record = dict(source_sha256=manifest['source_sha256'],stl_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  bodies=len(items),watertight=bool(plate.is_watertight),bounds_mm=plate.bounds.tolist(),
                  solid_PLA_g_at_1_24=float(plate.volume*.00124),minimum_box_gap_mm=args.gap,
                  square_bin_mm=size,packing_strategy=strategy,parts=records,
                  scope='Nominal meshes/print arrangement only; actual slicing, fit, assembly and load qualification remain separate.')
    (args.output/'plate-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='parts'},indent=2))


if __name__ == '__main__': main()
