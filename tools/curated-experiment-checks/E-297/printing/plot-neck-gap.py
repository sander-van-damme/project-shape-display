import sys,importlib.util,json,zipfile
from pathlib import Path
import numpy as np
from shapely.geometry import Point,LineString,box
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[4];folder=root/'owner-print-tests/2026-10-16-two-half-clutch-fit'
spec=importlib.util.spec_from_file_location('v',root/'tools/curated-experiment-checks/E-297/printing/validate-project.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
report=json.loads((folder/'validation.json').read_text());dx,dy=report['model_to_gcode_translation_xy_mm'];layout=json.loads((folder/'layout.json').read_text())
with zipfile.ZipFile(folder/'clutch-fit.3mf') as z:paths,_=v.parse(z.read('Metadata/plate_1.gcode').decode())
fig,axs=plt.subplots(1,2,figsize=(10,5))
for ax,(idx,zz) in zip(axs,[(1,1.8),(2,1.92)]):
 lo,hi=np.array(layout[idx-1]['bounds_mm']);cx,cy=(lo[:2]+hi[:2])/2+[dx,dy]
 ps=[p for p in paths if p['z']==zz and abs((p['x']+p['x1'])/2-cx)<2.2 and abs((p['y']+p['y1'])/2-cy)<2.2]
 foot=v.footprint(ps)
 for poly in list(foot.geoms) if hasattr(foot,'geoms') else [foot]:
  ax.fill(*poly.exterior.xy,color='#74a9cf')
  for hole in poly.interiors:ax.fill(*hole.xy,color='white')
 skeleton=[]
 for t in np.linspace(0,np.pi*2,721):
  inner=min(1.22,.92/max(abs(np.sin(t)),1e-9));r=(inner+1.6)/2;skeleton.append([cx+r*np.cos(t),cy+r*np.sin(t)])
 missing=LineString(skeleton).difference(foot)
 for gap in list(missing.geoms) if hasattr(missing,'geoms') else [missing]:
  ax.plot(*gap.xy,color='red',linewidth=4)
 ax.set_aspect('equal');ax.set_title(f'Krappe rotor {idx}; Z={zz:.2f} mm\nRood: nominale middellijn buiten bead-footprint')
fig.tight_layout();fig.savefig(folder/'tight-neck-gaps.png',dpi=180)
