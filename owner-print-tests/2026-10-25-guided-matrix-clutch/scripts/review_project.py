#!/usr/bin/env python3
"""Inspect actual saved X1C project, named objects, deposited paths and open pin bores."""
from pathlib import Path
import argparse,importlib.util,json,zipfile,hashlib,collections,re
import numpy as np
import trimesh as tm
from scipy.spatial import cKDTree
from shapely.geometry import Point,Polygon,LineString
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
P=Path(__file__).resolve().parents[1];R=P.parents[1]
s=importlib.util.spec_from_file_location('v',R/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
a=argparse.ArgumentParser();a.add_argument('--project',type=Path,required=True);a.add_argument('--report',type=Path,required=True);a.add_argument('--atlas',type=Path);a=a.parse_args()
with zipfile.ZipFile(a.project) as z:
 settings=json.loads(z.read('Metadata/project_settings.config'));gcode=z.read('Metadata/plate_1.gcode').decode();bounds,instances,points,triangles=v.project_bounds(z)
m=tm.load(P/'components/plate.stl');shift=bounds[0]-m.bounds[0];err=max(cKDTree(points).query(m.vertices+shift)[0].max(),cKDTree(m.vertices+shift).query(points)[0].max())
assert err<.00004 and len(triangles)==len(m.faces)
assert settings['printer_model']=='Bambu Lab X1 Carbon' and settings['nozzle_diameter']==['0.4']
assert settings['enable_support']=='0' and float(settings['layer_height'])==.12 and settings['wall_generator']=='arachne'
paths,_=v.parse(gcode);off=settings.get('extruder_offset',['0x0']);off=off[0] if isinstance(off,list) else off;delta=shift[:2]-np.array([float(x) for x in off.split('x')])
paths=[p for p in paths if p['role'].lower() not in ['skirt','brim','custom']]
roles=collections.Counter(p['role'] for p in paths);assert not any('support' in r.lower() for r in roles)
mid=np.array([[(p['x']+p['x1'])/2,(p['y']+p['y1'])/2] for p in paths]);layout=json.loads((P/'metadata/layout.json').read_text());screens=[];plots=[]
seen=set()
for e in layout:
 lo,hi=np.array(e['bounds_mm']);mask=np.all((mid>=lo[:2]+delta-.01)&(mid<=hi[:2]+delta+.01),axis=1);local=[paths[i] for i in np.flatnonzero(mask)];layers=collections.defaultdict(list)
 for p in local:layers[p['z']].append(p)
 zz=sorted(layers);empty=[]
 if zz:empty=[round(float(z),2) for z in np.arange(.12,hi[2]-.06,.12) if not any(abs(z-q)<.001 for q in zz)]
 name=e['name'];kind=name.rsplit('-',1)[0];orphans=[];bores=[];long=[];areas=[]
 # One of each exact mesh: all layers. Duplicates get continuity checks, not duplicate diagrams.
 detailed=kind not in seen
 if detailed:
  seen.add(kind);prev=None
  for z,ps in sorted(layers.items()):
   foot=v.footprint(ps);polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot];areas.append((z,foot.area))
   if prev is not None:
    for poly in polys:
     if poly.area>.005 and poly.intersection(prev.buffer(.02)).area<.001:orphans.append({'z_mm':z,'area_mm2':poly.area,'centroid':list(poly.centroid.coords)[0]})
    for p in ps:
     if 'bridge' in p['role'].lower() or 'overhang' in p['role'].lower():
      line=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]);free=line.difference(prev.buffer(.02));pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
      length=max((q.length for q in pieces),default=0)
      if length>1:long.append({'z_mm':z,'role':p['role'],'free_centerline_mm':length})
   if kind=='pin' and z>=1.32:
    center=Point(*((lo[:2]+hi[:2])/2+delta));rr=1.9875;cx,cy=center.x,center.y;sk=LineString([(cx-rr,cy-rr),(cx+rr,cy-rr),(cx+rr,cy+rr),(cx-rr,cy+rr),(cx-rr,cy-rr)]);gap=sk.difference(foot);maxgap=max((q.length for q in (list(gap.geoms) if hasattr(gap,'geoms') else [gap])),default=0);bores.append({'z_mm':z,'axis_clearance_mm':center.distance(foot),'outer_midwall_max_gap_mm':maxgap,'enclosed':any(Polygon(h).contains(center) for poly in polys for h in poly.interiors),'enclosed_after_005mm_buffer':any(Polygon(h).contains(center) for poly in ([foot.buffer(.005)] if foot.buffer(.005).geom_type=='Polygon' else foot.buffer(.005).geoms) for h in poly.interiors),'closed_buffer_needed_mm':next((d for d in [0,.005,.01,.02,.04,.08] if any(Polygon(h).contains(center) for poly in ([foot.buffer(d)] if foot.buffer(d).geom_type=='Polygon' else foot.buffer(d).geoms) for h in poly.interiors)),None)})
   prev=foot
  # Three heights capture bottom, working section, and upper structure.
  picks=[min(zz,key=lambda z:abs(z-t)) for t in [.12, min(hi[2]*.48,2.4),hi[2]-.36]]
  for z in dict.fromkeys(picks):plots.append((name,z,layers[z],lo[:2]+delta,hi[:2]+delta))
 screens.append({'name':name,'layers':len(zz),'empty_interior_layers_mm':empty,'max_extrusion_z_mm':max(zz,default=0),'minimum_model_bead_width_mm':min((p['width'] for p in local),default=0),'all_layer_unsupported_islands':orphans if detailed else 'same mesh as earlier nominal','long_bridge_or_overhang_segments':sorted(long,key=lambda x:x['free_centerline_mm'],reverse=True)[:10],'open_pin_bore':bores,'first_layer_model_area_mm2':areas[0][1] if areas else None})
 print(name,len(zz),'empty',len(empty),'islands',len(orphans),flush=True)
keys=['printer_model','printer_settings_id','nozzle_diameter','filament_settings_id','filament_type','filament_density','filament_flow_ratio','nozzle_temperature','nozzle_temperature_initial_layer','curr_bed_type','textured_plate_temp','textured_plate_temp_initial_layer','layer_height','initial_layer_print_height','wall_generator','min_bead_width','min_feature_size','wall_loops','sparse_infill_density','sparse_infill_pattern','line_width','initial_layer_line_width','outer_wall_line_width','inner_wall_line_width','top_surface_line_width','sparse_infill_line_width','internal_solid_infill_line_width','outer_wall_speed','inner_wall_speed','initial_layer_speed','initial_layer_infill_speed','bridge_speed','bridge_angle','seam_gap','default_acceleration','outer_wall_acceleration','inner_wall_acceleration','initial_layer_acceleration','enable_support','brim_type','brim_width','brim_object_gap','raft_layers','print_sequence','xy_contour_compensation','xy_hole_compensation','elefant_foot_compensation','fan_min_speed','fan_max_speed','slow_down_min_speed','slow_down_for_layer_cooling','close_fan_the_first_x_layers','additional_cooling_fan_speed']
report={'project_sha256':hashlib.sha256(a.project.read_bytes()).hexdigest(),'gcode_sha256':hashlib.sha256(gcode.encode()).hexdigest(),'geometry_max_vertex_error_mm':float(err),'source_facets':len(m.faces),'archive_facets':len(triangles),'named_objects':len(layout),'saved_settings':{k:settings.get(k) for k in keys},'roles':dict(roles),'layer_heights_mm':sorted(set(p['height'] for p in paths)),'estimates':[l for l in gcode.splitlines() if re.match(r'; (?:model printing time|total estimated time|total filament|filament used)',l)],'parts':screens,'limits':['Slicer paths are not physical print/fit or operation evidence.','Orphan screen tests whole deposited components against previous layer, not every unsupported bead.','Bridge/cantilever details require inspection; no automatic physical qualification.']}
a.report.write_text(json.dumps(report,indent=2)+'\n')
if a.atlas:
 rows=(len(plots)+2)//3;fig,axs=plt.subplots(rows,3,figsize=(15,rows*3.3),squeeze=False)
 for ax,(name,z,ps,lo,hi) in zip(axs.flat,plots):
  ax.add_collection(LineCollection([[(p['x'],p['y']),(p['x1'],p['y1'])] for p in ps],colors=['#d84425' if 'bridge' in p['role'].lower() or 'overhang' in p['role'].lower() else '#175a82' for p in ps],linewidths=.6));ax.set(xlim=(lo[0]-.5,hi[0]+.5),ylim=(lo[1]-.5,hi[1]+.5),title=f'{name}: Z{z:.2f} mm');ax.set_aspect('equal')
 for ax in list(axs.flat)[len(plots):]:ax.axis('off')
 fig.tight_layout();fig.savefig(a.atlas);plt.close(fig)
print(report['estimates'],flush=True)
