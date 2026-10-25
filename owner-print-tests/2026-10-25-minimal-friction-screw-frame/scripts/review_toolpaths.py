#!/usr/bin/env python3
"""Actual Bambu paths: shape fidelity, connected deposition, bores, orientation.
Nominal bead footprints cannot prove adhesion, friction, bridging or physical strength.
"""
from pathlib import Path
import argparse,importlib.util,collections,json,zipfile,math,hashlib,re
import numpy as np,trimesh
from shapely.geometry import Point,LineString,Polygon,box
from shapely.affinity import translate
from scipy.spatial import cKDTree
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader',P.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
def orientation(ps,axis='y'):
 total=parallel=transverse=0
 for q in ps:
  l=q['length'];cos=abs(q['y1']-q['y'])/l if axis=='y' else 0
  total+=l;parallel+=l*(cos>.95);transverse+=l*(cos<.05)
 return dict(path_length_mm=total,parallel_percent=100*parallel/total if total else None,transverse_percent=100*transverse/total if total else None)
def review(project,plate,out,plot=False,baseline=False):
 with zipfile.ZipFile(project) as z:
  cfg=json.loads(z.read('Metadata/project_settings.config'));g=z.read('Metadata/plate_1.gcode').decode();paths,_=reader.parse(g);bounds,instances,verts,tris=reader.project_bounds(z)
 if baseline:
  pack=P.parent/'2026-10-19-microstepper-frame-v3';rows=json.loads((pack/'metadata/layout.json').read_text());stl=pack/'components/microstepper-frame-v3.stl'
 else:rows=json.loads((P/'metadata/layout.json').read_text())[plate];stl=P/'components'/(plate+'.stl')
 m=trimesh.load(stl,force='mesh');shift=bounds[0]-m.bounds[0];error=max(cKDTree(verts).query(m.vertices+shift)[0].max(),cKDTree(m.vertices+shift).query(verts)[0].max());assert error<.00004,error
 offset=shift[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')]);summaries=[];plots=[]
 assert not any('support' in q['role'].lower() for q in paths)
 for part in rows:
  lo,hi=np.array(part['bounds_mm']);lo[:2]+=offset;hi[:2]+=offset;center=np.array(part['center_xy'])+offset
  grouped=collections.defaultdict(list)
  for q in paths:
   x=(q['x']+q['x1'])/2;y=(q['y']+q['y1'])/2
   if lo[0]-.02<=x<=hi[0]+.02 and lo[1]-.02<=y<=hi[1]+.02 and q['role'] not in ['Skirt','Brim']:
    grouped[q['z']].append(q)
  if baseline and part['source'] not in ['front','pin-50']:continue
  footprints={};orphans=[];bridges=[];previous=None;lobes=[];core=[];core_overlap=[];previous_core=None;thread_tips=[];bores=[];seams=[]
  for z,qs in sorted(grouped.items()):
   fp=translate(reader.footprint(qs),-center[0],-center[1]);footprints[z]=fp
   polys=list(fp.geoms) if hasattr(fp,'geoms') else [fp]
   if previous is not None:
    for poly in polys:
     if poly.area>.005 and poly.intersection(previous.buffer(.01)).area<.001:orphans.append(dict(z_mm=z,area_mm2=poly.area,bounds_mm=list(poly.bounds)))
    for q in qs:
     if 'bridge' in q['role'].lower():
      line=LineString([(q['x']-center[0],q['y']-center[1]),(q['x1']-center[0],q['y1']-center[1])]);free=line.difference(previous.buffer(.01));pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
      bridges.append(dict(z_mm=z,span_mm=max((v.length for v in pieces),default=0),endpoint_distances_mm=[Point(line.coords[i]).distance(previous.buffer(.01)) for i in [0,-1]]))
   src=part['source']
   if src=='A-screw-supported':
    if .36<=z<=2.28:
     def rad(a):
      a=math.radians(a);hit=fp.intersection(LineString([(0,0),(2*math.cos(a),2*math.sin(a))]));return Point(0,0).distance(hit) if not hit.is_empty else 2
     tips=[rad(a) for a in [0,120,240]];valleys=[rad(a) for a in [60,180,300]]
     lobes.append(dict(z_mm=z,open_core=fp.intersection(Point(0,0).buffer(.8)).area<.001,contrast_mm=min(valleys)-max(tips),tip_radii_mm=tips))
    if 3.84<z<30:
     fp_core=fp.intersection(Point(0,0).buffer(.5));core.append(fp_core.area/Point(0,0).buffer(.5).area)
     if previous_core is not None:core_overlap.append(fp_core.intersection(previous_core).area)
     previous_core=fp_core
     if all(abs(z-h)>.4 for h in [11.16,12.6,23.16,24.6]):
      main=[poly for poly in polys if poly.intersection(Point(0,0).buffer(.5)).area>.1]
      coords=np.concatenate([np.asarray(poly.exterior.coords) for poly in main]);thread_tips.append([z,float(np.linalg.norm(coords,axis=1).max())])
   if src in ['C-pin-18-upright','pin-50']:
    bores.append(dict(z_mm=z,core_clear=fp.intersection(Point(0,0).buffer(.6)).area<.001))
    outer=[q for q in qs if q['role']=='Outer wall' and max(abs(q['x']-center[0]),abs(q['y']-center[1]))>1.8]
    if outer:seams.append([z,outer[0]['x']-center[0],outer[0]['y']-center[1]])
   previous=fp
  allqs=[q for qs in grouped.values() for q in qs];src=part['source']
  row=dict(name=part['name'],source=src,layers=len(grouped),bed_contact_footprint_mm2=footprints[min(footprints)].area,orphan_components=orphans,bridges=bridges,outer_wall_direction=orientation([q for q in allqs if q['role']=='Outer wall'],axis='z' if src in ['C-pin-18-upright','pin-50','B-pin'] else 'y'))
  if src in ['front','A-front','A-back']:
   stations=[(32.7,72.7)] if src=='front' else [(36,38),(56,58)]
   def inside_station(q):return any(a+.05<((q['y']+q['y1'])/2-center[1])<b-.05 for a,b in stations)
   side=[q for q in allqs if inside_station(q) and q['z']>4.2 and q['z']<6.4 and 2.3<abs((q['x']+q['x1'])/2-center[0])<2.9 and 'wall' in q['role'].lower()]
   floor=[q for q in allqs if inside_station(q) and 3.95<q['z']<4.12 and abs((q['x']+q['x1'])/2-center[0])<2.2]
   row.update(guide_side_wall_direction=orientation(side),guide_floor_direction=orientation(floor),guide_floor_roles=dict(collections.Counter(q['role'] for q in floor)))
   if not baseline:plots.append((part,4.08,'A guide floor and walls',(-5,6,34,40),grouped,center))
  if lobes:
   row.update(C_lobe_layers=lobes,minimum_lobe_contrast_mm=min(q['contrast_mm'] for q in lobes),minimum_thread_core_coverage=min(core))
   assert all(q['open_core'] and q['contrast_mm']>.1 for q in lobes),lobes
   assert min(core)>.75,min(core) # baseline short screw is ~0.83 with these inherited bead settings
   row['minimum_adjacent_core_overlap_mm2']=min(core_overlap);assert min(core_overlap)>.4
   row['thread_turn_max_radii_mm']=[max(radius for z,radius in thread_tips if 3.6+3*i<z<=6.6+3*i) for i in range(9)]
   assert all(1.4<radius<1.9 for radius in row['thread_turn_max_radii_mm'])
   row['core_coverage_note']='Partial central bead coverage also occurs in v3; connected deposition is checked separately, this is not a strength prediction.'
   for z,title in [(1.8,'A preserved C socket'),(2.52,'A cavity roof'),(9,'A screw thread')]:plots.append((part,z,title,(-2.3,2.3,-2.3,2.3),grouped,center))
  if bores:
   row['upright_bore_core_clear_all_layers']=all(v['core_clear'] for v in bores);assert row['upright_bore_core_clear_all_layers']
   row['first_outer_path_points_by_layer_mm']=seams
   if not baseline:plots.append((part,1.8,'C upright internal thread',(-2.5,2.5,-2.5,2.5),grouped,center))
  if src=='C-pin-18-horizontal':
   plots.append((part,2.28,'C horizontal thread / tube',(-2.6,2.6,-.5,18.5),grouped,center))
   plots.append((part,4.08,'C horizontal roof bridges',(-2.6,2.6,-.5,18.5),grouped,center))
   sides=[q for q in allqs if q['z']>.36 and q['z']<4.08 and 1.8<abs((q['x']+q['x1'])/2-center[0])<2.4 and q['role']=='Outer wall']
   row['long_side_perimeter_direction']=orientation(sides)
   row['horizontal_lumen_midplane_clear_mm2']=footprints[min(footprints,key=lambda z:abs(z-2.2))].intersection(box(-.55,6.3,.55,17.5)).area
  if plate=='A-first':assert not orphans,(part['name'],orphans)
  summaries.append(row)
 report=dict(project_sha256=hashlib.sha256(Path(project).read_bytes()).hexdigest(),scope='Nominal extruded bead geometry; no physical friction/strength/adhesion claim',mesh_vertex_error_mm=float(error),support_paths=0,parts=summaries,stats=[s for s in g.splitlines() if re.search(r'(total estimated time|total filament|model printing time)',s)])
 Path(out).write_text(json.dumps(report,indent=2)+'\n')
 if plot and plots:
  import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
  selected=plots[:4] if plate=='A-first' else [next(p for p in plots if p[2].startswith('C upright')),next(p for p in plots if p[2].startswith('C horizontal thread')),next(p for p in plots if p[2].startswith('C horizontal roof'))]
  fig,axes=plt.subplots(1,len(selected),figsize=(4*len(selected),5));axes=np.atleast_1d(axes)
  for ax,(part,z,title,lims,groups,center) in zip(axes,selected):
   zz=min(groups,key=lambda v:abs(v-z))
   for q in groups[zz]:ax.plot([q['x']-center[0],q['x1']-center[0]],[q['y']-center[1],q['y1']-center[1]],lw=max(.5,q['width']*6),color='#d55e00' if 'bridge' in q['role'].lower() else '#187b8c')
   ax.set(xlim=lims[:2],ylim=lims[2:],title=f'{title}\nlayer Z={zz:g} mm',xlabel='X mm',ylabel='Y mm');ax.set_aspect('equal');ax.grid(alpha=.2)
  fig.tight_layout();fig.savefig(P/'images'/(plate+'-toolpaths.png'),dpi=160);plt.close(fig)
 print(Path(out).name,[(r['name'],len(r['orphan_components']),len(r['bridges'])) for r in summaries])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('project',type=Path);ap.add_argument('plate');ap.add_argument('out',type=Path);ap.add_argument('--plot',action='store_true');ap.add_argument('--baseline',action='store_true');a=ap.parse_args();review(a.project,a.plate,a.out,a.plot,a.baseline)
