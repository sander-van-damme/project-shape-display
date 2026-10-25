#!/usr/bin/env python3
"""Focused plots of actual deposited paths for human inspection."""
from pathlib import Path
import argparse,importlib.util,json,zipfile
import numpy as np
import trimesh as tm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon as Patch
P=Path(__file__).resolve().parents[1];R=P.parents[1]
s=importlib.util.spec_from_file_location('v',R/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
a=argparse.ArgumentParser();a.add_argument('--preview-dir',type=Path);a=a.parse_args()
with zipfile.ZipFile(P/'guided-matrix-clutch.3mf') as z:
 settings=json.loads(z.read('Metadata/project_settings.config'));gcode=z.read('Metadata/plate_1.gcode').decode();bounds,_,_,_=v.project_bounds(z)
m=tm.load(P/'components/plate.stl');shift=bounds[0]-m.bounds[0];off=settings['extruder_offset'][0].split('x');delta=shift[:2]-np.array(list(map(float,off)));paths,_=v.parse(gcode)
layout={e['name']:e for e in json.loads((P/'metadata/layout.json').read_text())};mid=np.array([[(p['x']+p['x1'])/2,(p['y']+p['y1'])/2] for p in paths])
picks=[('follower-1',.12),('follower-1',.72),('rotor-1',7.20),('pin-1',12.48),('pin-1',15.48),('screw-tree-1',3.60),('row-base-1',3.36),('beam-100-1',9.72),('frame-print-1',15.96)]
fig,axs=plt.subplots(3,3,figsize=(14,12))
for ax,(name,z) in zip(axs.flat,picks):
 lo,hi=np.array(layout[name]['bounds_mm']);lo=lo[:2]+delta;hi=hi[:2]+delta
 if name=='screw-tree-1':hi[0]=lo[0]+7.4
 mask=np.all((mid>=lo-.01)&(mid<=hi+.01),axis=1);ps=[paths[i] for i in np.flatnonzero(mask) if abs(paths[i]['z']-z)<.001 and paths[i]['role'].lower() not in ['skirt','brim']];foot=v.footprint(ps);polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
 for poly in polys:
  ax.add_patch(Patch(np.array(poly.exterior.coords),facecolor='#216f94',edgecolor='none'))
  for hole in poly.interiors:ax.add_patch(Patch(np.array(hole.coords),facecolor='white',edgecolor='none'))
 ax.add_collection(LineCollection([[(p['x'],p['y']),(p['x1'],p['y1'])] for p in ps if 'bridge' in p['role'].lower() or 'overhang' in p['role'].lower()],colors='#db5435',linewidths=.6))
 ax.set(xlim=(lo[0]-.3,hi[0]+.3),ylim=(lo[1]-.3,hi[1]+.3),title=f'{name}, Z{z:.2f}');ax.set_aspect('equal')
fig.suptitle('Actual nominal deposited material — red: bridge / overhang centreline\nSlicer evidence; adhesion, physical thread fit and beam strength remain untested',fontsize=12);fig.tight_layout(rect=(0,0,1,.94));fig.savefig(P/'images/critical-toolpaths.svg')
if a.preview_dir:a.preview_dir.mkdir(parents=True,exist_ok=True);fig.savefig(a.preview_dir/'critical-toolpaths.png',dpi=160)
plt.close(fig)
