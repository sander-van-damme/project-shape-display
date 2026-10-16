#!/usr/bin/env python3
"""Independent Bambu archive/settings and actual deposited-path review.

Uses nominal G-code geometry and line-width comments, not printer measurements.
"""
import argparse, collections, hashlib, json, math, re, zipfile, posixpath, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

def project_bounds(archive):
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    cache={};pns='{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}path'
    def read(name):
        if name not in cache:cache[name]=ET.fromstring(archive.read(name))
        return cache[name]
    def matrix(value):
        result=np.eye(4)
        if value:result[:3,:]=np.array([float(v) for v in value.split()]).reshape(4,3).T
        return result
    def resolve(base,path):return posixpath.normpath(path.lstrip('/') if path.startswith('/') else posixpath.join(posixpath.dirname(base),path))
    vertices=[];instances=[];triangles=[]
    def walk(name,oid,transform):
        root=read(name);obj=next(q for q in root.findall('m:resources/m:object',ns) if q.get('id')==oid)
        vv=obj.findall('m:mesh/m:vertices/m:vertex',ns)
        if vv:
            points=np.array([[float(q.get(k)) for k in ['x','y','z']]+[1.] for q in vv])@transform.T
            vertices.append(points[:,:3]);instances.append(dict(model=name,object_id=oid,bounds_mm=[points[:,:3].min(axis=0).tolist(),points[:,:3].max(axis=0).tolist()]))
            face=np.array([[int(q.get(k)) for k in ['v1','v2','v3']] for q in obj.findall('m:mesh/m:triangles/m:triangle',ns)])
            triangles.append(points[face,:3])
        for component in obj.findall('m:components/m:component',ns):
            target=resolve(name,component.get(pns)) if component.get(pns) else name
            walk(target,component.get('objectid'),transform@matrix(component.get('transform')))
    name='3D/3dmodel.model';root=read(name)
    for item in root.findall('m:build/m:item',ns):walk(name,item.get('objectid'),matrix(item.get('transform')))
    points=np.concatenate(vertices)
    return np.array([points.min(axis=0),points.max(axis=0)]),instances,points,np.concatenate(triangles)

def parse(text):
    x=y=z=e=0.; relative=True; role=''; layer_z=None; height=.12; width=.45
    paths=[]; arcs=[]; feed=0.; max_accel=[];current_accel=0.
    for number,line in enumerate(text.splitlines(),1):
        line=line.strip()
        m=re.match(r';\s*(FEATURE|TYPE|Z_HEIGHT|LAYER_HEIGHT|HEIGHT|LINE_WIDTH):\s*(.*)',line)
        if m:
            key,value=m.groups()
            if key in ('FEATURE','TYPE'): role=value.strip()
            elif key=='Z_HEIGHT':layer_z=float(value)
            elif key in ('LAYER_HEIGHT','HEIGHT'):height=float(value)
            elif key=='LINE_WIDTH':width=float(value)
        code=line.split(';')[0].strip()
        if code=='M83': relative=True
        if code=='M82': relative=False
        if code.startswith('G92 '):
            vals={k:float(v) for k,v in re.findall(r'([XYZEF])(-?[\d.]+)',code)}
            e=vals.get('E',e)
        if code.startswith('M204 '):
            max_accel.append(code)
            avals={k:float(v) for k,v in re.findall(r'([SP])(-?[\d.]+)',code)}
            current_accel=avals.get('S',avals.get('P',current_accel))
        if not re.match(r'G[0123] ',code):continue
        vals={k:float(v) for k,v in re.findall(r'([XYZEF])(-?[\d.]+)',code)}
        nx,ny,nz=vals.get('X',x),vals.get('Y',y),vals.get('Z',z)
        amount=vals.get('E',0.) if relative else vals.get('E',e)-e
        feed=vals.get('F',feed)
        length=math.hypot(nx-x,ny-y)
        if amount>0 and length>1e-6 and role and layer_z is not None:
            if code.startswith(('G2 ','G3 ')):arcs.append(number)
            paths.append(dict(x=x,y=y,x1=nx,y1=ny,z=round(layer_z,5),role=role,
                              e=amount,width=width,height=height,length=length,speed=feed/60,accel=current_accel))
        if 'E' in vals:e=e+vals['E'] if relative else vals['E']
        x,y,z=nx,ny,nz
    assert paths,'No model extrusion recognized'
    assert not arcs, f'Arc interpolation is not supported; lines {arcs[:10]}'
    return paths,max_accel

def footprint(ps):
    return unary_union([LineString([(p['x'],p['y']),(p['x1'],p['y1'])]).buffer(p['width']/2,quad_segs=4) for p in ps])

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--project',type=Path,required=True)
    ap.add_argument('--stl',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--layers',default='0.12,0.72,1.2,2.4,3.6,5.4')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.project) as archive:
        names=archive.namelist()
        settings=json.loads(archive.read('Metadata/project_settings.config'))
        gnames=[n for n in names if n.endswith('.gcode')]
        assert len(gnames)==1,gnames
        gbytes=archive.read(gnames[0]);text=gbytes.decode()
        (a.out/'plate.gcode').write_bytes(gbytes)
        meta={n:archive.read(n).decode(errors='replace') for n in names if n.endswith(('slice_info.config','model_settings.config'))}
        built_bounds,instances,built_points,built_triangles=project_bounds(archive)
    paths,accel=parse(text);layers=collections.defaultdict(list)
    for p in paths:layers[p['z']].append(p)
    roles=collections.Counter(p['role'] for p in paths)
    previous=None;orphans=[];spans=[];summaries=[]
    for z,ps in sorted(layers.items()):
        foot=footprint(ps)
        parts=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
        missing=[]
        if previous is not None:
            prev=previous.buffer(.01)
            for poly in parts:
                if poly.area>.005 and poly.intersection(prev).area<.001:
                    missing.append(dict(area_mm2=round(poly.area,5),centroid=list(poly.centroid.coords)[0]))
            for p in ps:
                if 'bridge' not in p['role'].lower() and 'overhang' not in p['role'].lower():continue
                line=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]);free=line.difference(prev)
                pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
                spans.append(dict(z_mm=z,role=p['role'],max_free_centerline_mm=max((q.length for q in pieces),default=0.),
                                  start_distance_mm=Point(p['x'],p['y']).distance(prev),end_distance_mm=Point(p['x1'],p['y1']).distance(prev)))
        if missing:orphans.append(dict(z_mm=z,components=missing))
        summaries.append(dict(z_mm=z,footprint_area_mm2=round(foot.area,4),components=len(parts),orphans=len(missing)))
        previous=foot
    mesh=trimesh.load(a.stl,force='mesh');bodies=mesh.split()
    from scipy.spatial import cKDTree
    translation=built_bounds[0]-mesh.bounds[0]
    source_points=mesh.vertices+translation
    pointset_error=max(cKDTree(built_points).query(source_points)[0].max(),cKDTree(source_points).query(built_points)[0].max())
    def facet_error(first,second):
        candidates=cKDTree(second.mean(axis=1)).query(first.mean(axis=1),k=8)[1]
        nearby=second[candidates]
        # Preserve winding, allowing only cyclic triangle-corner permutations.
        distances=[np.linalg.norm(first[:,None]-np.roll(nearby,shift,axis=2),axis=3).max(axis=2) for shift in range(3)]
        return float(np.min(np.stack(distances),axis=(0,2)).max())
    source_triangles=mesh.triangles+translation
    face_error=max(facet_error(source_triangles,built_triangles),facet_error(built_triangles,source_triangles))
    facets_equal=len(mesh.faces)==len(built_triangles) and face_error<.00003
    keys=['printer_model','printer_variant','printer_settings_id','nozzle_diameter','extruder_offset','filament_settings_id','filament_type',
          'filament_vendor','filament_diameter','filament_density','filament_flow_ratio','nozzle_temperature',
          'nozzle_temperature_initial_layer','curr_bed_type','hot_plate_temp','hot_plate_temp_initial_layer',
          'textured_plate_temp','textured_plate_temp_initial_layer','layer_height','initial_layer_print_height',
          'wall_generator','wall_loops','sparse_infill_density','line_width','initial_layer_line_width',
          'outer_wall_line_width','inner_wall_line_width','top_surface_line_width','internal_solid_infill_line_width',
          'outer_wall_speed','inner_wall_speed','small_perimeter_speed','small_perimeter_threshold',
          'initial_layer_speed','initial_layer_infill_speed','bridge_speed','internal_bridge_speed',
          'default_acceleration','outer_wall_acceleration','inner_wall_acceleration','initial_layer_acceleration',
          'enable_support','brim_type','brim_width','brim_object_gap','raft_layers','print_sequence',
          'xy_contour_compensation','xy_hole_compensation','elefant_foot_compensation','detect_thin_wall',
          'slow_down_for_layer_cooling','slow_down_min_speed','fan_min_speed','fan_max_speed',
          'slow_down_layer_time','fan_cooling_layer_time','overhang_fan_speed','close_fan_the_first_x_layers']
    report=dict(project=a.project.name,project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),
                source_stl=a.stl.name,source_stl_sha256=hashlib.sha256(a.stl.read_bytes()).hexdigest(),
                gcode_sha256=hashlib.sha256(gbytes).hexdigest(),archive_entries=names,
                settings={k:settings.get(k,'MISSING') for k in keys},
                source_geometry=dict(bodies=len(bodies),watertight=bool(mesh.is_watertight),bounds_mm=mesh.bounds.tolist(),
                     bodies_bounds_mm=[b.bounds.tolist() for b in bodies]),
                project_geometry=dict(bounds_mm=built_bounds.tolist(),mesh_instances=instances,
                    extents_equal_source=bool(np.allclose(built_bounds[1]-built_bounds[0],mesh.extents,atol=.0001)),
                    source_rigid_translation_mm=translation.tolist(),max_bidirectional_vertex_distance_after_translation_mm=float(pointset_error),
                    facets_and_winding_match_source_within_00003mm=facets_equal,max_bidirectional_oriented_facet_distance_mm=face_error,
                    source_facet_count=len(mesh.faces),project_facet_count=len(built_triangles)),
                layer_count=len(layers),layer_heights_mm=sorted(set(p['height'] for p in paths)),
                roles=dict(roles),role_max_speeds_mm_s={r:round(max(p['speed'] for p in paths if p['role']==r),4) for r in roles},
                role_max_accelerations_mm_s2={r:round(max(p['accel'] for p in paths if p['role']==r),4) for r in roles},
                actual_line_width_percentiles_mm=np.percentile([p['width'] for p in paths],[0,1,50,99,100]).tolist(),
                unsupported_layer_components=orphans,
                max_bridge_free_centerline_mm=max((q['max_free_centerline_mm'] for q in spans),default=0.),
                max_bridge_anchor_distance_mm=max((max(q['start_distance_mm'],q['end_distance_mm']) for q in spans),default=0.),
                gcode_estimates=[l for l in text.splitlines() if re.match(r'; (?:model printing time|total estimated time|total filament|filament used)',l)],
                caveats=['Nominal deposited footprints use slicer LINE_WIDTH comments, not measured bead flow or motion.',
                         'A connected footprint with previous-layer overlap does not prove bed adhesion, stiffness, bridge quality or physical stability.',
                         'Physical fit, PLA temperature suitability, friction, load capacity and repeatability remain unknown.'])
    startup=text.split('; CHANGE_LAYER',1)[0]
    startup_commands=[l.split(';')[0].strip() for l in startup.splitlines() if re.match(r'^M10[49]\s',l)]
    report['startup_check']=dict(official_x1_04_marker_present=';===== machine: X1-0.4' in startup,
            last_nozzle_temperature_command_before_first_model_layer=startup_commands[-1] if startup_commands else None,
            nozzle_temperature_commands_before_first_model_layer=startup_commands)
    (a.out/'bridge-details.json').write_text(json.dumps(spans,indent=2)+'\n')
    (a.out/'layer-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (a.out/'archive-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    offset=settings.get('extruder_offset',['0x0'])
    offset=offset[0] if isinstance(offset,list) else offset
    nozzle_offset=np.array([float(v) for v in offset.split('x')])
    path_translation=(built_bounds[0]-mesh.bounds[0])[:2]-nozzle_offset
    report['model_to_gcode_translation_xy_mm']=path_translation.tolist()
    part_screens=[]
    dx,dy=path_translation
    first=footprint(layers[min(layers)])
    for i,body in enumerate(bodies,1):
        lo,hi=body.bounds
        region=box(lo[0]+dx-.2,lo[1]+dy-.2,hi[0]+dx+.2,hi[1]+dy+.2)
        counts=[]
        for z,ps in sorted(layers.items()):
            if z>hi[2]+.12:continue
            local=[p for p in ps if region.contains(Point((p['x']+p['x1'])/2,(p['y']+p['y1'])/2))]
            counts.append(dict(z_mm=z,path_segments=len(local)))
        part_screens.append(dict(index=i,source_bounds_mm=body.bounds.tolist(),
               first_layer_contact_area_mm2=first.intersection(region).area,
               layers_with_extrusion=sum(q['path_segments']>0 for q in counts),
               top_layer_with_extrusion_mm=max((q['z_mm'] for q in counts if q['path_segments']),default=0)))
    report['part_toolpath_screens']=part_screens
    plot(paths,a.out,[float(z) for z in a.layers.split(',')])
    (a.out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['archive_entries','source_geometry','settings']},indent=2))

def plot(paths,out,wanted):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    zs=sorted(set(p['z'] for p in paths))
    fig,axs=plt.subplots(3,2,figsize=(13,10))
    colors={'Outer wall':'#045a8d','Inner wall':'#74a9cf','Overhang wall':'red','Bridge':'#f16913','Support':'purple','Support interface':'magenta','Brim':'#00a377'}
    for ax,wanted_z in zip(axs.flat,wanted):
        z=min(zs,key=lambda q:abs(q-wanted_z));ps=[p for p in paths if p['z']==z]
        ax.add_collection(LineCollection([[(p['x'],p['y']),(p['x1'],p['y1'])] for p in ps],colors=[colors.get(p['role'],'#555') for p in ps],linewidths=.6))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Actual Bambu G-code paths Z={z:.2f} mm')
    fig.tight_layout();fig.savefig(out/'toolpaths.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
