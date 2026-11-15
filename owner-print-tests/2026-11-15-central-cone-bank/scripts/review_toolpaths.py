#!/usr/bin/env python3
"""Generic actual-path screen. Geometry, not physical strength/adhesion proof.
Usage: python scripts/review_toolpaths.py PROJECT.3mf OUTPUT.json [--layout layout.json --plate NAME]
Layout is A-style {plate:[{name,source,bounds_mm,center_xy}]} in original STL coords.
"""
from pathlib import Path
import argparse,importlib.util,json,zipfile,collections,re,hashlib
import numpy as np
from shapely.geometry import Point,LineString,Polygon
from shapely.affinity import translate
p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('output',type=Path);p.add_argument('--layout',type=Path);p.add_argument('--plate');p.add_argument('--critical-only',action='store_true');p.add_argument('--plot',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('reader',root/'owner-print-tests/validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
with zipfile.ZipFile(a.project) as z:
 cfg=json.loads(z.read('Metadata/project_settings.config'));gn=[n for n in z.namelist() if n.endswith('.gcode')];assert len(gn)==1,gn
 g=z.read(gn[0]).decode();paths,acc=reader.parse(g);bounds,instances,verts,tris=reader.project_bounds(z)
roles=collections.Counter(q['role'] for q in paths)
report=dict(project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),layer_count=len(set(q['z'] for q in paths)),roles=dict(roles),support_paths=sum(n for role,n in roles.items() if 'support' in role.lower()),brim_paths=roles.get('Brim',0),project_bounds_mm=bounds.tolist(),stats=[s for s in g.splitlines() if re.search(r'(total estimated time|total filament|model printing time)',s)],parts=[],scope='Nominal sliced deposition; not physical fit, stability, strength or adhesion')
if a.layout:
 rows=json.loads(a.layout.read_text());rows=rows[a.plate] if isinstance(rows,dict) else rows
 original=np.array([r['bounds_mm'] for r in rows]);shift=bounds[0]-original[:,0,:].min(axis=0)
 offset=cfg.get('extruder_offset',['0x0']);offset=offset[0] if isinstance(offset,list) else offset;shift[:2]-=np.array([float(v) for v in offset.split('x')])
 for r in rows:
  if a.critical_only and r['source'] not in ['pin','screw-supported','rotor','rotor-tight','rotor-loose','guide','guide-46','guide-47','guide-48']:continue
  lo,hi=np.array(r['bounds_mm'])+shift;center=np.array(r['center_xy'])+shift[:2];groups=collections.defaultdict(list)
  for q in paths:
   if lo[0]-.02<=(q['x']+q['x1'])/2<=hi[0]+.02 and lo[1]-.02<=(q['y']+q['y1'])/2<=hi[1]+.02 and q['role'] not in ['Brim','Skirt'] and 'support' not in q['role'].lower():groups[q['z']].append(q)
  prev=None;orphans=[];cores=[];sections=[];bridges=[]
  for z,qs in sorted(groups.items()):
   fp=reader.footprint(qs);polys=list(fp.geoms) if hasattr(fp,'geoms') else [fp]
   if prev is not None:
    previous_support=prev.buffer(.01)
    for poly in polys:
     if poly.area>.005 and poly.intersection(previous_support).area<.001:orphans.append(dict(z_mm=z,area_mm2=poly.area,bounds_mm=list(poly.bounds)))
   if prev is not None and r['source'] in ['bank','yoke','yoke-long']:
    for q in qs:
     if 'bridge' not in q['role'].lower() and 'overhang' not in q['role'].lower():continue
     line=LineString([(q['x'],q['y']),(q['x1'],q['y1'])]);free=line.difference(previous_support);pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
     bridges.append(dict(z_mm=z,role=q['role'],maximum_free_segment_mm=max((v.length for v in pieces),default=0),endpoint_distances_mm=[Point(line.coords[i]).distance(previous_support) for i in [0,-1]]))
   cores.append(dict(z_mm=z,center_disk_radius_06_deposition_mm2=fp.intersection(Point(*center).buffer(.6)).area))
   local=translate(fp,-center[0],-center[1]);src=r['source']
   checks={}
   # Fixed mid-wall probe loops test actual deposited closure, not just STL closure.
   if src=='pin' and .36<=z<=39.84:
    loop=LineString([(-1.98,-1.98),(1.98,-1.98),(1.98,1.98),(-1.98,1.98),(-1.98,-1.98)])
    checks.update(midwall_uncovered_mm=loop.difference(local.buffer(.04)).length,bore_core_deposition_mm2=local.intersection(Point(0,0).buffer(.55)).area)
   if src.startswith('rotor') and .36<=z<=7.8:
    loop=Point(0,0).buffer(1.82,quad_segs=64).exterior
    checks.update(rotor_wall_uncovered_mm=loop.difference(local.buffer(.04)).length,rotor_key_core_deposition_mm2=local.intersection(Point(0,0).buffer(.8)).area)
   if src=='guide':
    vertical=LineString([(2.54,-2.2),(2.54,7.28)]);horizontal=LineString([(-2.2,2.54),(7.28,2.54)])
    checks.update(vertical_web_uncovered_mm=vertical.difference(local).length,horizontal_web_uncovered_mm=horizontal.difference(local).length,hole_core_deposition_mm2=max(local.intersection(Point(x,y).buffer(.8)).area for x in [0,5.08] for y in [0,5.08]))
   if src in ['guide-46','guide-47','guide-48']:
    vertical=LineString([(2.54,-2.2),(2.54,2.2)])
    checks.update(vertical_web_uncovered_mm=vertical.difference(local).length,hole_core_deposition_mm2=max(local.intersection(Point(x,0).buffer(.8)).area for x in [0,5.08]))
   if src=='screw-supported':
    if .36<=z<=1.32:
     loop=Point(0,0).buffer(2.11,quad_segs=64).exterior
     checks.update(cup_wall_uncovered_mm=loop.difference(local.buffer(.04)).length,cup_core_deposition_mm2=local.intersection(Point(0,0).buffer(.6)).area)
    if 8.52<=z<=34.56:
     checks['screw_core_coverage']=local.intersection(Point(0,0).buffer(.5)).area/Point(0,0).buffer(.5).area
   if checks and any('uncovered' in k for k in checks):
    def closed(shape):
     pp=list(shape.geoms) if hasattr(shape,'geoms') else [shape]
     return any(Polygon(v.exterior).contains(Point(0,0)) and not v.contains(Point(0,0)) for v in pp)
    checks['closed_hoop_raw']=closed(local)
    checks['closed_hoop_buffer04']=closed(local.buffer(.04))
   if checks:sections.append(dict(z_mm=z,**checks))
   prev=fp
  report['parts'].append(dict(name=r['name'],source=r['source'],layers=len(groups),role_counts=dict(collections.Counter(q['role'] for qs in groups.values() for q in qs)),orphan_components=orphans,critical_sections=sections,bridges=bridges,role_max_speed_mm_s={role:max(q['speed'] for qs in groups.values() for q in qs if q['role']==role) for role in set(q['role'] for qs in groups.values() for q in qs)},center_disk_probe=cores))
a.output.write_text(json.dumps(report,indent=2)+'\n');print(a.output,report['stats'],'support_paths',report['support_paths'])

if a.plot and a.layout and any(r['source']=='pin' for r in rows):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 rr=next(r for r in rows if r['source']=='pin');c=np.array(rr['center_xy'])+shift[:2]
 pack=Path(__file__).resolve().parents[1];mesh=reader.trimesh.load(pack/'components/pin.stl');fig,axs=plt.subplots(1,4,figsize=(14,4))
 for ax,z in zip(axs,[.48,.60,1.44,3.48]):
  qs=[q for q in paths if q['z']==z and abs((q['x']+q['x1'])/2-c[0])<2.3 and abs((q['y']+q['y1'])/2-c[1])<2.3 and q['role'] not in ['Brim','Skirt']]
  fp=reader.footprint(qs);polys=list(fp.geoms) if hasattr(fp,'geoms') else [fp]
  for poly in polys:
   x,y=np.array(poly.exterior.coords).T;ax.fill(x-c[0],y-c[1],color='#80c5d4',alpha=.8)
   for ring in poly.interiors:
    x,y=np.array(ring.coords).T;ax.fill(x-c[0],y-c[1],color='white')
  sec=mesh.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
  if sec:
   for entity in sec.entities:
    line=entity.discrete(sec.vertices);ax.plot(line[:,0],line[:,1],'--',lw=.7,color='#8c2644')
  ax.set(xlim=(-2.4,2.4),ylim=(-2.4,2.4),title=f'Z {z:.2f} mm',xlabel='X mm');ax.set_aspect('equal');ax.grid(alpha=.2)
 axs[0].set_ylabel('Y mm');fig.suptitle('Pin: nominal deposited beads (blue) and STL section (dashed).\nLocal gaps are slicer findings; physical strength and fit remain untested.',fontsize=11)
 fig.tight_layout();fig.savefig(pack/'images/critical-pin-paths.svg');plt.close(fig)
 svg=pack/'images/critical-pin-paths.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
