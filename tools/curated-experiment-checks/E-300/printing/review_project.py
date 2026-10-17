#!/usr/bin/env python3
"""Review actual saved Bambu configuration, geometry and selected deposited paths.

Reuses the historical G-code parser read-only. Results are slicer observations,
never evidence of successful physical printing. See --help for invocation.
"""
import argparse, collections, hashlib, importlib.util, json, re, zipfile, math
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from shapely.geometry import box, LineString, Point, Polygon

ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('e298_review', ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py')
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--project',type=Path,required=True)
    ap.add_argument('--stl',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--layers',default='.12,1.2,2.4,4.8,7.2,10.8')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.project) as z:
        settings=json.loads(z.read('Metadata/project_settings.config'))
        gnames=[n for n in z.namelist() if n.endswith('.gcode')]
        assert len(gnames)==1
        gbytes=z.read(gnames[0]);gcode=gbytes.decode()
        bounds,instances,points,triangles=v.project_bounds(z)
        archive_meta={n:z.read(n).decode() for n in z.namelist() if n.endswith('slice_info.config')}
    mesh=trimesh.load(a.stl,force='mesh');bodies=mesh.split()
    assert mesh.is_watertight,'Nonwatertight input geometry'
    translation=bounds[0]-mesh.bounds[0]
    source_points=mesh.vertices+translation
    vertex_error=max(cKDTree(points).query(source_points)[0].max(),cKDTree(source_points).query(points)[0].max())
    assert vertex_error<.00003 and len(triangles)==len(mesh.faces)
    assert np.allclose(bounds[1]-bounds[0],mesh.extents,atol=.0001)
    paths,_=v.parse(gcode);layers=collections.defaultdict(list)
    for p in paths:layers[p['z']].append(p)
    layer_zs=sorted(layers);first_z=min(layer_zs);roles=collections.Counter(p['role'] for p in paths)
    assert not any('support' in r.lower() for r in roles),'Unexpected slicer support inside geometry'
    assert settings['printer_model']=='Bambu Lab X1 Carbon'
    assert [float(x) for x in settings['nozzle_diameter']]==[.4]
    assert float(settings['layer_height'])==.12
    assert settings['wall_generator']=='arachne'
    assert settings['enable_support']=='0' and settings['brim_type']=='no_brim'
    assert ';===== machine: X1-0.4' in gcode
    offset=settings.get('extruder_offset',['0x0']);offset=offset[0] if isinstance(offset,list) else offset
    nozzle_offset=np.array([float(x) for x in offset.split('x')])
    delta=translation[:2]-nozzle_offset
    first=v.footprint(layers[first_z])
    layout_path=a.stl.parent/'layout.json'
    layout=json.loads(layout_path.read_text()) if layout_path.exists() else []
    screens=[]
    for body in bodies:
        low,high=body.bounds;lo=low[:2]+delta-.05;hi=high[:2]+delta+.05
        name='unnamed'
        if layout:
            match=min(layout,key=lambda p:np.linalg.norm(np.array(p['bounds_mm'])-body.bounds))
            if np.max(np.abs(np.array(match['bounds_mm'])-body.bounds))<.001:name=match['name']
        counts=[];widths=[];local_layers={}
        for z,ps in sorted(layers.items()):
            if z>high[2]+.12:continue
            local=[p for p in ps if lo[0]<=(p['x']+p['x1'])/2<=hi[0] and lo[1]<=(p['y']+p['y1'])/2<=hi[1]]
            counts.append((z,len(local)))
            local_layers[z]=local
            widths.extend(p['width'] for p in local)
        contact=first.intersection(box(*lo,*hi)).area
        missing=[z for z,n in counts if not n and z<=high[2]-.12]
        all_layer_orphans=[];bridge_segments=[];previous=None;bore_screens=[]
        for z,local in local_layers.items():
            if not local:continue
            need_foot=(name=='pin' or name.endswith('-rotor') or name.endswith('-selector')) or any('bridge' in p['role'].lower() or 'overhang' in p['role'].lower() for p in local)
            if (name=='pin' or name.endswith('-rotor') or name.endswith('-selector')):
                foot=v.footprint(local)
                polygons=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
                if previous is not None:
                    all_layer_orphans.extend(dict(z_mm=z,area_mm2=poly.area,centroid_xy_mm=list(poly.centroid.coords)[0]) for poly in polygons if poly.area>.005 and poly.intersection(previous.buffer(.01)).area<.001)
                previous=foot
                if (name=='pin' and z>=1.2) or (name.endswith('-rotor') and .84<=z<=5.48):
                    center=Point(*(body.bounds.mean(axis=0)[:2]+delta))
                    enclosed=any(Polygon(hole).contains(center) for poly in polygons for hole in poly.interiors)
                    cx,cy=center.x,center.y
                    if name=='pin':
                        rr=1.9875;skeleton=LineString([(cx-rr,cy-rr),(cx+rr,cy-rr),(cx+rr,cy+rr),(cx-rr,cy+rr),(cx-rr,cy-rr)])
                    else:
                        skeleton=[]
                        for angle in np.linspace(0,2*math.pi,721):
                            inner=min(1.25,.95/max(abs(math.sin(angle)),1e-9));rr=(inner+1.6)/2
                            skeleton.append((cx+rr*math.cos(angle),cy+rr*math.sin(angle)))
                        skeleton=LineString(skeleton)
                    skeleton_missing=skeleton.difference(foot);gaps=list(skeleton_missing.geoms) if hasattr(skeleton_missing,'geoms') else [skeleton_missing]
                    softened=foot.buffer(.005);softpolys=list(softened.geoms) if hasattr(softened,'geoms') else [softened]
                    closed_with_005=any(Polygon(hole).contains(center) for poly in softpolys for hole in poly.interiors)
                    bore_screens.append(dict(z_mm=z,axis_in_enclosed_hole=enclosed,axis_to_deposited_material_mm=center.distance(foot),nominal_midwall_max_gap_mm=max((gap.length for gap in gaps),default=0.),closed_with_0005mm_radius_buffer=closed_with_005))
            if need_foot:
                prior_zs=[zz for zz in local_layers if zz<z]
                if not prior_zs:continue
                prior=v.footprint(local_layers[max(prior_zs)]).buffer(.01)
                for p in local:
                    if not ('bridge' in p['role'].lower() or 'overhang' in p['role'].lower()):continue
                    line=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]);free=line.difference(prior)
                    pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
                    bridge_segments.append(dict(z_mm=z,role=p['role'],free_centerline_mm=max((q.length for q in pieces),default=0.),start_anchor_distance_mm=Point(p['x'],p['y']).distance(prior),end_anchor_distance_mm=Point(p['x1'],p['y1']).distance(prior)))
        screens.append(dict(name=name,source_bounds_mm=body.bounds.tolist(),bed_contact_nominal_area_mm2=round(contact,3),
            layers_with_extrusion=sum(n>0 for z,n in counts),empty_interior_layers_mm=missing,
            top_extrusion_z_mm=max((z for z,n in counts if n),default=0),
            line_width_range_mm=[min(widths),max(widths)] if widths else [],
            line_width_percentiles_mm=np.percentile(widths,[0,1,50,99,100]).tolist() if widths else [],
            all_layers_unsupported_components=all_layer_orphans if (name=='pin' or name.endswith('-rotor') or name.endswith('-selector')) else 'not screened for this part',
            rotor_neck_screen=dict(examined_layers=len(bore_screens),layers_without_closed_wall_loop_mm=[p['z_mm'] for p in bore_screens if not p['axis_in_enclosed_hole']],minimum_axis_clearance_mm=min((p['axis_to_deposited_material_mm'] for p in bore_screens),default=None),nominal_midwall_max_gap_mm=max((p['nominal_midwall_max_gap_mm'] for p in bore_screens),default=0.),layers_unclosed_after_0005mm_buffer=[p['z_mm'] for p in bore_screens if not p['closed_with_0005mm_radius_buffer']]) if name.endswith('-rotor') else None,
            pin_open_bore_screen=dict(examined_layers=len(bore_screens),layers_without_enclosed_open_bore_mm=[p['z_mm'] for p in bore_screens if not p['axis_in_enclosed_hole']],minimum_axis_clearance_mm=min((p['axis_to_deposited_material_mm'] for p in bore_screens),default=None),nominal_midwall_max_gap_mm=max((p['nominal_midwall_max_gap_mm'] for p in bore_screens),default=0.),layers_unclosed_after_0005mm_buffer=[p['z_mm'] for p in bore_screens if not p['closed_with_0005mm_radius_buffer']]) if name=='pin' else None,
            bridge_overhang_segment_count=len(bridge_segments),
            max_free_bridge_overhang_centerline_mm=max((p['free_centerline_mm'] for p in bridge_segments),default=0.),
            longest_bridge_overhang_segments=sorted(bridge_segments,key=lambda p:p['free_centerline_mm'],reverse=True)[:8]))
    selected=sorted(set(min(layer_zs,key=lambda z:abs(z-float(t))) for t in a.layers.split(',')))
    layer_reports=[]
    for z in selected:
        current=v.footprint(layers[z]);idx=layer_zs.index(z)
        prev=v.footprint(layers[layer_zs[idx-1]]).buffer(.01) if idx else None
        polygons=list(current.geoms) if hasattr(current,'geoms') else [current]
        unsupported=[dict(area_mm2=round(p.area,5),centroid_xy_mm=list(p.centroid.coords)[0]) for p in polygons if prev is not None and p.area>.005 and p.intersection(prev).area<.001]
        layer_reports.append(dict(z_mm=z,nominal_deposited_area_mm2=current.area,components=len(polygons),unsupported_components=unsupported))
    keys=['printer_model','printer_variant','printer_settings_id','nozzle_diameter','filament_settings_id','filament_type','filament_diameter','filament_density','filament_flow_ratio','nozzle_temperature','nozzle_temperature_initial_layer','curr_bed_type','textured_plate_temp','textured_plate_temp_initial_layer','layer_height','initial_layer_print_height','wall_generator','min_bead_width','min_feature_size','wall_loops','sparse_infill_density','sparse_infill_pattern','line_width','initial_layer_line_width','outer_wall_line_width','inner_wall_line_width','top_surface_line_width','sparse_infill_line_width','internal_solid_infill_line_width','support_line_width','outer_wall_speed','inner_wall_speed','small_perimeter_speed','small_perimeter_threshold','initial_layer_speed','initial_layer_infill_speed','bridge_speed','default_acceleration','outer_wall_acceleration','inner_wall_acceleration','initial_layer_acceleration','enable_support','brim_type','brim_width','brim_object_gap','raft_layers','print_sequence','xy_contour_compensation','xy_hole_compensation','elefant_foot_compensation','fan_min_speed','fan_max_speed','slow_down_min_speed','slow_down_for_layer_cooling','close_fan_the_first_x_layers','additional_cooling_fan_speed']
    report=dict(project=a.project.name,project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),source_stl_sha256=hashlib.sha256(a.stl.read_bytes()).hexdigest(),gcode_sha256=hashlib.sha256(gbytes).hexdigest(),settings={k:settings.get(k,'MISSING') for k in keys},
        geometry=dict(body_count=len(bodies),watertight=True,bounds_mm=bounds.tolist(),source_to_project_translation_mm=translation.tolist(),source_to_gcode_translation_xy_mm=delta.tolist(),max_bidirectional_vertex_error_mm=float(vertex_error),source_facet_count=len(mesh.faces),archive_facet_count=len(triangles)),
        layer_count=len(layers),actual_layer_heights_mm=sorted(set(p['height'] for p in paths)),roles=dict(roles),role_max_speeds_mm_s={r:max(p['speed'] for p in paths if p['role']==r) for r in roles},role_max_acceleration_mm_s2={r:max(p['accel'] for p in paths if p['role']==r) for r in roles},part_toolpath_screens=screens,selected_layer_contact_screens=layer_reports,
        gcode_estimates=[l for l in gcode.splitlines() if re.match(r'; (?:model printing time|total estimated time|total filament|filament used)',l)],
        caveats=['Nominal slicer geometry; actual bed adhesion, scaffold strength, print quality, fit and operation remain untested.','Selected-layer footprint overlap and all-layer per-object extrusion continuity screens do not constitute a full overhang/stability proof.'])
    (a.out/'slicer-review.json').write_text(json.dumps(report,indent=2)+'\n')
    (a.out/'archive-metadata.json').write_text(json.dumps(archive_meta,indent=2)+'\n')
    v.plot(paths,a.out,[float(t) for t in a.layers.split(',')])
    plot_details(paths,screens,delta,a.out,selected)
    print(json.dumps(dict(project=a.project.name,layers=len(layers),roles=dict(roles),geometry_vertex_error_mm=float(vertex_error),estimates=report['gcode_estimates'],parts=screens),indent=2))

def plot_details(paths,screens,delta,out,selected):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    cols=3;rows=(len(screens)+cols-1)//cols
    fig,axs=plt.subplots(rows,cols,figsize=(15,4*rows),squeeze=False)
    for ax,part in zip(axs.flat,screens):
        bounds=np.array(part['source_bounds_mm']);lo=bounds[0,:2]+delta-.5;hi=bounds[1,:2]+delta+.5
        ps=[p for p in paths if p['z']==selected[min(len(selected)-1,2)] and lo[0]<=(p['x']+p['x1'])/2<=hi[0] and lo[1]<=(p['y']+p['y1'])/2<=hi[1]]
        ax.add_collection(LineCollection([[(p['x'],p['y']),(p['x1'],p['y1'])] for p in ps],colors=['red' if 'overhang' in p['role'].lower() else '#045a8d' for p in ps],linewidths=.7))
        ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),title=part['name']);ax.set_aspect('equal')
    for ax in list(axs.flat)[len(screens):]:ax.axis('off')
    fig.tight_layout();fig.savefig(out/'part-paths.png',dpi=140);plt.close(fig)

if __name__=='__main__':main()
