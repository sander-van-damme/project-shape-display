#!/usr/bin/env python3
"""Mechanism-specific deposited-bead screens. No physical print claims."""
import argparse, importlib.util, json, zipfile, math
from pathlib import Path
import numpy as np
from shapely.geometry import Point, Polygon, LineString, box
sp=importlib.util.spec_from_file_location('base',Path(__file__).with_name('validate-project.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--dog-root',type=float,default=5.2);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 layout=json.loads(a.layout.read_text());review=json.loads(a.review.read_text());dx,dy=review['model_to_gcode_translation_xy_mm']
 with zipfile.ZipFile(a.project) as z:paths,_=m.parse(z.read('Metadata/plate_1.gcode').decode())
 samples=[];localsets={};footprints={}
 for idx,part in enumerate(layout,1):
  name=part['name'];lo,hi=np.array(part['bounds_mm']);cx,cy=(lo[:2]+hi[:2])/2+[dx,dy]
  region=box(lo[0]+dx-.25,lo[1]+dy-.25,hi[0]+dx+.25,hi[1]+dy+.25)
  local=[p for p in paths if p['role']!='Brim' and lo[0]+dx-.25<(p['x']+p['x1'])/2<hi[0]+dx+.25 and lo[1]+dy-.25<(p['y']+p['y1'])/2<hi[1]+dy+.25]
  byz={z:[p for p in local if p['z']==z] for z in sorted(set(p['z'] for p in local))}; localsets[idx]=byz
  for z,ps in byz.items():
   if not (name.startswith(('rotor','point')) or name.split('#')[0] in ['pin','screw'] or 'comb' in name or 'selector' in name):continue
   foot=m.footprint(ps);polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
   q=dict(part=idx,name=name,z_mm=z,area_mm2=foot.area)
   if name.startswith(('rotor','point')):
    if z<=a.dog_root-.88:q['central_radius_060_free']=foot.intersection(Point(cx,cy).buffer(.6)).area<.001
    if .84<=z<=1.92:
     q['neck_is_closed_wall']=any(Polygon(p.exterior).contains(Point(cx,cy)) and not p.contains(Point(cx,cy)) for p in polys if p.geom_type=='Polygon')
     relief=.12 if 'tight' in name else .20 if 'loose' in name else .15
     skeleton=[]
     for angle in np.linspace(0,2*math.pi,721):
      inner=min(1.1+relief,(.8+relief)/max(abs(math.sin(angle)),1e-9));rr=(inner+1.6)/2
      skeleton.append((cx+rr*math.cos(angle),cy+rr*math.sin(angle)))
     missing=LineString(skeleton).difference(foot)
     gaps=list(missing.geoms) if hasattr(missing,'geoms') else [missing]
     q['neck_nominal_midwall_max_gap_mm']=max((gap.length for gap in gaps),default=0)
    if False: # E-298 apex footprint reviewed independently by point-paths.py
    
     q['two_dog_components']=len([p for p in polys if p.area>.02])==2
     portions=[]
     for phase in [0,math.pi]:
      arc=LineString([(cx+1.375*math.cos(t+phase),cy+1.375*math.sin(t+phase)) for t in np.linspace(-math.radians(24),math.radians(24),65)])
      portions.append(arc.intersection(foot.buffer(.02)).length/arc.length)
     q['dog_midradius_48deg_arc_coverage']=portions
   if name.split('#')[0]=='pin' and z>=1.32:
    q['central_radius_060_free']=foot.intersection(Point(cx,cy).buffer(.6)).area<.001
    q['closed_wall']=any(Polygon(p.exterior).contains(Point(cx,cy)) and not p.contains(Point(cx,cy)) for p in polys if p.geom_type=='Polygon')
    q['pin_zone']='thread' if z>12 else 'plain_tube'
    rr=1.9875
    skeleton=LineString([(cx-rr,cy-rr),(cx+rr,cy-rr),(cx+rr,cy+rr),(cx-rr,cy+rr),(cx-rr,cy-rr)])
    missing=skeleton.difference(foot);gaps=list(missing.geoms) if hasattr(missing,'geoms') else [missing]
    q['pin_nominal_midwall_max_gap_mm']=max((gap.length for gap in gaps),default=0)
   if name.split('#')[0]=='screw' and 10.44<=z<=26.16:
    disk=Point(cx,cy).buffer(.45)
    q['thread_core_radius_045_coverage']=foot.intersection(disk).area/disk.area
    q['thread_connected_components']=len([p for p in polys if p.area>.02])
    q['thread_crest_radius_mm']=max((math.hypot(x-cx,y-cy) for p in polys if p.geom_type=='Polygon' for x,y in p.exterior.coords),default=0)
   samples.append(q)
 summaries={}
 for name in sorted(set(p['name'] for p in layout)):
  ss=[q for q in samples if q['name']==name];fields=['central_radius_060_free','neck_is_closed_wall','two_dog_components','closed_wall']
  sums={f:dict(samples=sum(f in q for q in ss),failed=sum(q.get(f) is False for q in ss)) for f in fields if any(f in q for q in ss)}
  vv=[v for q in ss for v in q.get('dog_midradius_48deg_arc_coverage',[])];
  if vv:sums['dog_arc_min_coverage']=min(vv)
  gaps=[q['neck_nominal_midwall_max_gap_mm'] for q in ss if 'neck_nominal_midwall_max_gap_mm' in q]
  if gaps:sums['neck_nominal_midwall_max_gap_mm']=max(gaps)
  if name.split('#')[0]=='pin':
   for zone in ['thread','plain_tube']:
    zs=[q for q in ss if q.get('pin_zone')==zone]
    sums[zone]=dict(samples=len(zs),wall_not_closed=sum(not q['closed_wall'] for q in zs),nominal_midwall_max_gap_mm=max((q['pin_nominal_midwall_max_gap_mm'] for q in zs),default=0))
  if name.split('#')[0]=='screw':
   ts=[q for q in ss if 'thread_core_radius_045_coverage' in q]
   sums['thread']=dict(samples=len(ts),min_core_coverage=min((q['thread_core_radius_045_coverage'] for q in ts),default=0),min_crest_radius_mm=min((q['thread_crest_radius_mm'] for q in ts),default=0),max_connected_components=max((q['thread_connected_components'] for q in ts),default=0),working_section_min_crest_radius_mm=min((q['thread_crest_radius_mm'] for q in ts if q['z_mm']<25.2),default=0))
  if sums:summaries[name]=sums
 # Keep plots local and legible: representative rotor, selector and pin layers.
 chosen=[]
 for prefix,wanted in [('point',[1.2,a.dog_root-.76,a.dog_root+.32,a.dog_root+2.24]),('comb',[.12,1.44]),('row-selector',[.12,1.44]),('pin',[1.32,12.24,17.76]),('screw',[.12,10.44,23.16])]:
  candidates=[i for i,p in enumerate(layout,1) if p['name'].startswith(prefix)]
  if candidates:
   i=candidates[0];byz=localsets[i]
   for desired in wanted:
    zz=min(byz,key=lambda z:abs(z-desired));chosen.append((i,layout[i-1]['name'],zz,byz[zz]))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.collections import LineCollection
 cols=3;rows=math.ceil(len(chosen)/cols);fig,axs=plt.subplots(rows,cols,figsize=(13,rows*3.5),squeeze=False)
 colors={'Outer wall':'#045a8d','Inner wall':'#74a9cf','Bridge':'#f16913','Overhang wall':'red'}
 for ax,(idx,name,z,ps) in zip(axs.flat,chosen):
  for p in ps:
   b=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]).buffer(p['width']/2,quad_segs=3)
   ax.fill(*b.exterior.xy,color=colors.get(p['role'],'#999'),alpha=.45,linewidth=0)
  ax.autoscale();ax.set_aspect('equal');ax.set_title(f'{idx:02d} {name}; Z={z:.2f} mm',fontsize=9)
 for ax in list(axs.flat)[len(chosen):]:ax.set_visible(False)
 fig.tight_layout();fig.savefig(a.out/'critical-toolpaths.png',dpi=180);plt.close(fig)
 (a.out/'critical-paths.json').write_text(json.dumps(dict(dog_root_mm=a.dog_root,summary=summaries,details=samples,caveats=['Nominal buffered toolpaths, not measured extrusion.','Closed wall and connected layer do not establish stiffness or adhesion.','0.60 mm bore disk is a blockage screen; it does not prove full DD/thread clearance.']),indent=2)+'\n')
 print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
