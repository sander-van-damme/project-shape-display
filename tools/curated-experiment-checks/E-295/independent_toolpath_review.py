#!/usr/bin/env python3
"""Independent STL + deposited-path audit. Comparison G-code is scratch only.

Requires numpy, trimesh, shapely, matplotlib. No printer is controlled.
All-layer overlap is a geometric support screen, not a stability/adhesion proof.
"""
import argparse, collections, hashlib, json, math, re
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import LineString, Point
from shapely.ops import unary_union


def parse_paths(path):
    txt=path.read_text()
    assert 'M83' in txt and 'use_relative_e_distances = 1' in txt
    x=y=z=0.; role=''; height=.12; paths=[]
    for line in txt.splitlines():
        if line.startswith(';TYPE:'): role=line[6:]
        if line.startswith(';HEIGHT:'): height=float(line[8:])
        if not re.match(r'G[01] ',line): continue
        vals={k:float(v) for k,v in re.findall(r'([XYZEF])(-?[\d.]+)',line.split(';')[0])}
        nx,ny,nz=vals.get('X',x),vals.get('Y',y),vals.get('Z',z)
        length=math.hypot(nx-x,ny-y)
        if vals.get('E',0)>0 and length>1e-6:
            # Stadium cross-section used by FFF extrusion planners.
            w=vals['E']*math.pi*1.75**2/4/(height*length)+height*(1-math.pi/4)
            paths.append(dict(x=x,y=y,x1=nx,y1=ny,z=round(nz,5),role=role,e=vals['E'],width=w,length=length))
        x,y,z=nx,ny,nz
    return paths,txt


def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--stl',type=Path,required=True)
    ap.add_argument('--gcode',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    mesh=trimesh.load(args.stl,force='mesh')
    parts=mesh.split(only_watertight=False)
    paths,txt=parse_paths(args.gcode)
    role_counts=collections.Counter(p['role'] for p in paths)
    layers=collections.defaultdict(list)
    for p in paths: layers[p['z']].append(p)
    summaries=[]; previous=None; prev_z=0; orphan=[]
    for z,ps in sorted(layers.items()):
        footprints=[LineString([(p['x'],p['y']),(p['x1'],p['y1'])]).buffer(max(.05,min(1.,p['width']))/2,quad_segs=3) for p in ps]
        swept=unary_union(footprints)
        components=list(swept.geoms) if hasattr(swept,'geoms') else [swept]
        positive=[g for g in components if g.area>.005]
        missing=[]
        if previous is not None:
            previous_tolerant=previous.buffer(.01)
            for i,c in enumerate(positive):
                if c.intersection(previous_tolerant).area<.001: missing.append(dict(index=i,area_mm2=c.area,xy=list(c.centroid.coords)[0]))
            # Line midpoint beyond previous deposit: diagnostic for bridges,
            # not a guarantee that every filament is supported all along.
            d=max((Point((p['x']+p['x1'])/2,(p['y']+p['y1'])/2).distance(previous_tolerant) for p in ps),default=0.)
            newly_exposed=swept.difference(previous_tolerant).area
        else: d=0.;newly_exposed=0.
        if missing: orphan.append(dict(z_mm=z,components=missing))
        summaries.append(dict(z_mm=z,components_over_005mm2=len(positive),deposited_area_mm2=round(swept.area,4),newly_exposed_area_mm2=round(newly_exposed,4),max_midpoint_outside_previous_mm=round(d,4),orphan_components=len(missing)))
        previous=swept;prev_z=z
    result=dict(stl_sha256=hashlib.sha256(args.stl.read_bytes()).hexdigest(),gcode_sha256=hashlib.sha256(args.gcode.read_bytes()).hexdigest(),stl_file=args.stl.name,gcode_file=args.gcode.name,
        watertight=bool(mesh.is_watertight),winding_consistent=bool(mesh.is_winding_consistent),body_count=len(parts),bounds_mm=mesh.bounds.tolist(),volume_mm3=float(mesh.volume),
        bodies=[dict(extents_mm=m.extents.tolist(),bounds_mm=m.bounds.tolist(),volume_mm3=float(m.volume),watertight=bool(m.is_watertight),winding_consistent=bool(m.is_winding_consistent)) for m in parts],
        layer_count=len(layers),roles=dict(role_counts),footer=[s for s in txt.splitlines() if re.match(r'; (filament used|estimated printing time)',s)],
        extrusion_width_range_mm=[float(np.percentile([p['width'] for p in paths if p['length']>.05],q)) for q in [0,1,50,99,100]],
        unsupported_layer_components=orphan,layers=summaries,
        caveats=['Swept deposition is reconstructed from nominal E and XY, not printer motion or flow measurements.','A connected overlap with the previous layer does not prove adequate bed adhesion, stiffness or physical print stability.','No finite-mesh CAD or toolpath result proves thread fit, friction, load capacity or repeatability.'])
    (args.output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
    plot(paths,args.output)
    print(json.dumps({k:v for k,v in result.items() if k not in ['bodies','layers']},indent=2))


def plot(paths,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    zs=sorted({p['z'] for p in paths})
    wanted=[zs[0],1.2,3.,5.88,6.12,12.]
    fig,axs=plt.subplots(3,2,figsize=(13,10))
    colors={'External perimeter':'#045a8d','Perimeter':'#74a9cf','Overhang perimeter':'red','Bridge infill':'#f16913','Support material':'purple','Support material interface':'magenta'}
    for ax,z0 in zip(axs.flat,wanted):
        z=min(zs,key=lambda x:abs(x-z0));ps=[p for p in paths if p['z']==z]
        ax.add_collection(LineCollection([[(p['x'],p['y']),(p['x1'],p['y1'])] for p in ps],colors=[colors.get(p['role'],'#555555') for p in ps],linewidths=.5))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Actual deposition paths: Z={z:.2f} mm')
    fig.suptitle('Independent toolpath inspection — computational comparison only')
    fig.tight_layout();fig.savefig(output/'layers.png',dpi=170);plt.close(fig)

if __name__=='__main__': main()
