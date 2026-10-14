#!/usr/bin/env python3
"""Inspect comparison G-code only; never transmit to a printer.
Assumes build.py's exact plate order and PrusaSlicer's default centering at128,128.
Checks support toolpath midpoints within the threaded-cylinder envelope, not
physical support removal or complete nozzle collision. Plot includes real paths.
"""
import argparse,json,re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def paths(path):
 state=dict(X=0.,Y=0.,Z=0.,E=0.);kind='';relative=False
 for line in path.read_text().splitlines():
  if line.startswith(';TYPE:'):kind=line[6:]
  if line.startswith('M83'):relative=True
  if line.startswith('M82'):relative=False
  if line.startswith('G92'):
   for k,v in re.findall(r'([XYZE])(-?[\d.]+)',line):state[k]=float(v)
  if not line.startswith(('G0 ','G1 ')):continue
  v={k:float(x) for k,x in re.findall(r'([XYZE])(-?[\d.]+)',line)}
  old=state.copy();state.update(v)
  de=v.get('E',0) if relative else state['E']-old['E']
  if de>1e-8 and ('X' in v or 'Y' in v):
   yield old['X'],old['Y'],state['X'],state['Y'],state['Z'],kind

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pla',type=Path,required=True);ap.add_argument('--tpu',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 rows=list(paths(a.pla));tp=list(paths(a.tpu))
 ox=(256-215)/2;oy=(256-162.4500006)/2;cy=139.4500006+6
 centers=[(x+ox,y+cy+oy,z) for x,y,z in [(88,3,24),(109,3,24),(130,3,24),(151,3,24),(172,3,30),(193,3,30),(8,14,30),(29,14,30)]]
 violations=[]
 for x,y,xx,yy,z,k in rows:
  if not k.startswith('Support'):continue
  mid=((x+xx)/2,(y+yy)/2)
  for cx,cy,zt in centers:
   if z>=zt and np.hypot(mid[0]-cx,mid[1]-cy)<2.05:violations.append([mid[0],mid[1],z])
 assert not violations,violations[:10]
 assert set(round(r[4],3) for r in tp)=={.2}
 summary={'evidence':'PrusaSlicer comparison toolpaths, not physical validation',
 'pla_positive_xy_extrusion_segments':len(rows),'support_midpoints_inside_thread_envelopes':len(violations),
 'tpu_layers_mm':sorted(set(round(r[4],3) for r in tp)),
 'statistics':{}}
 for name,p in [('pla',a.pla),('tpu',a.tpu)]:summary['statistics'][name]=[s[2:] for s in p.read_text().splitlines() if s.startswith(('; filament used [','; estimated printing time'))]
 fig,axs=plt.subplots(2,2,figsize=(12,9))
 for ax,z in zip(axs.flat,[.2,22.1,24.05,30.05]):
  zs=sorted(set(r[4] for r in rows));actual=min(zs,key=lambda v:abs(v-z))
  selected=[r for r in rows if abs(r[4]-actual)<1e-6]
  segs=[[(r[0],r[1]),(r[2],r[3])] for r in selected]
  colors=['#de662d' if r[5].startswith('Support') else '#27698a' for r in selected]
  ax.add_collection(LineCollection(segs,colors=colors,linewidths=.35));ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Actual toolpaths Z={actual:g} mm (orange=support)')
 fig.tight_layout();fig.savefig(a.output/'slice-layers.png',dpi=160);plt.close(fig)
 (a.output/'slice-results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
