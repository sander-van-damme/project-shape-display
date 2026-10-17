#!/usr/bin/env python3
"""Render deposited-path footprints at the final project's critical regions."""
import argparse,collections,importlib.util,json,zipfile
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('v',ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True)
 r=json.loads(a.review.read_text());delta=np.array(r['geometry']['source_to_gcode_translation_xy_mm'])
 with zipfile.ZipFile(a.project) as z:paths,_=v.parse(z.read('Metadata/plate_1.gcode').decode())
 layers=collections.defaultdict(list)
 for p in paths:layers[p['z']].append(p)
 zs=sorted(layers)
 groups={'pin':[.12,.84,1.2,4.56,8.16,16.8],'rotor':[.12,.72,1.2,2.4,6.24,8.4],'column-selector':[.12,1.2,2.16,2.4,3.12,4.56],'screw-tree':[.12,9.12,10.2,14.52,20.4,26.88]}
 for name,wanted in groups.items():
  part=next(p for p in r['part_toolpath_screens'] if p['name']==name);bounds=np.array(part['source_bounds_mm']);lo=bounds[0,:2]+delta-.4;hi=bounds[1,:2]+delta+.4
  fig,axs=plt.subplots(2,3,figsize=(12,8))
  for ax,target in zip(axs.flat,wanted):
   z=min(zs,key=lambda q:abs(q-target));local=[p for p in layers[z] if lo[0]<=(p['x']+p['x1'])/2<=hi[0] and lo[1]<=(p['y']+p['y1'])/2<=hi[1]]
   foot=v.footprint(local);polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
   for poly in polys:
    ax.add_patch(Patch(np.array(poly.exterior.coords),facecolor='#2474a8',edgecolor='none'))
    for hole in poly.interiors:ax.add_patch(Patch(np.array(hole.coords),facecolor='white',edgecolor='none'))
   ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),title=f'{name} · Z {z:.2f} mm');ax.set_aspect('equal');ax.grid(alpha=.15)
  fig.suptitle('Actual saved Bambu paths · nominal LINE_WIDTH footprint; mm',fontsize=12);fig.tight_layout();fig.savefig(a.out/(name+'-toolpaths.png'),dpi=160);plt.close(fig)
if __name__=='__main__':main()
