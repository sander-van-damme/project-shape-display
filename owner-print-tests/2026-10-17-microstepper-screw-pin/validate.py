#!/usr/bin/env python3
"""Inspect supplied Bambu project AND a separately reopened/resliced copy.

python validate.py --resliced /tmp/motor-slice-final/reopen/microstepper-rig.3mf
Requires numpy, trimesh, manifold3d, scipy, shapely, matplotlib.
Uses the repository's independent Bambu G-code reader; no printer is required.
"""
import argparse, collections, hashlib, importlib.util, json, math, zipfile
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point, box, LineString
from scipy.spatial import cKDTree
import manifold3d as md

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('bambu_review',HERE.parent/'validate-bambu-project.py')
review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)

def solid(m):
    return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))

def analyze(path):
    with zipfile.ZipFile(path) as archive:
        settings=json.loads(archive.read('Metadata/project_settings.config'))
        g=archive.read('Metadata/plate_1.gcode').decode()
        bounds,objects,points,triangles=review.project_bounds(archive)
    mesh=trimesh.load(HERE/'microstepper-rig.stl',force='mesh')
    translation=bounds[0]-mesh.bounds[0]
    source=mesh.vertices+translation
    error=max(cKDTree(points).query(source)[0].max(),cKDTree(source).query(points)[0].max())
    assert error<.0001 and len(objects)==5
    assert settings['printer_model']=='Bambu Lab X1 Carbon'
    assert settings['enable_support']=='0'
    assert settings['nozzle_diameter']==['0.4']
    paths,_=review.parse(g)
    assert not any('support' in p['role'].lower() for p in paths)
    offset=np.array([float(x) for x in settings['extruder_offset'][0].split('x')])
    shift=translation[:2]-offset
    layout=json.loads((HERE/'layout.json').read_text())
    all_parts=[]; shapes={}; critical=[]
    for index,part in enumerate(layout):
        lo,hi=np.array(part['bounds_mm']);lo[:2]+=shift;hi[:2]+=shift
        selected=[p for p in paths if lo[0]-.1<=(p['x']+p['x1'])/2<=hi[0]+.1 and lo[1]-.1<=(p['y']+p['y1'])/2<=hi[1]+.1]
        layers=collections.defaultdict(list)
        for p in selected: layers[p['z']].append(p)
        assert layers and min(layers)==.12
        previous=None; orphans=[];bore=[]; bridges=[]
        for z,ps in sorted(layers.items()):
            shape=review.footprint(ps);shapes[index,z]=shape
            polygons=list(shape.geoms) if hasattr(shape,'geoms') else [shape]
            if previous is not None:
                unsupported=[dict(area_mm2=p.area,center=list(p.centroid.coords)[0]) for p in polygons if p.area>.005 and p.intersection(previous.buffer(.01)).area<.001]
                if unsupported:orphans.append(dict(z_mm=z,components=unsupported))
                for p in ps:
                    if 'bridge' in p['role'].lower() or 'overhang' in p['role'].lower():
                        free=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]).difference(previous.buffer(.01))
                        seg=list(free.geoms) if hasattr(free,'geoms') else [free]
                        bridges.append(dict(z_mm=z,role=p['role'],free_centerline_mm=max((q.length for q in seg),default=0)))
            previous=shape
            cx,cy=(lo[:2]+hi[:2])/2
            if part['name']=='pin':
                bore.append(dict(z_mm=z,center_radius_060_free=shape.intersection(Point(cx,cy).buffer(.6)).area<.001,
                    ring_closed=any(p.geom_type=='Polygon' and p.exterior and p.contains(Point(cx,cy))==False and
                        __import__('shapely').geometry.Polygon(p.exterior).contains(Point(cx,cy)) for p in polygons)))
            if part['name']=='cup' and z<2.52:
                assert shape.intersection(box(cx-4.8,cy-4.8,cx+4.8,cy+4.8)).area<.001
            if part['name']=='half' and z<=2.16:
                # The 4.4 mm square pin must fit the open half-guide at bed side.
                x=lo[0]+18;y0=hi[1]
                assert shape.intersection(box(x-2.2,y0-43.8,x+2.2,y0-36.2)).area<.001
            if part['name']=='half' and z<3.96:
                # 8 mm motor envelope inside 8.5 mm cavity, through body midsection.
                x=lo[0]+18;y0=hi[1];radius=math.sqrt(4**2-z*z)
                assert shape.intersection(box(x-radius,y0-9.8,x+radius,y0-2.3)).area<.001
        assert not orphans,(part['name'],orphans)
        if bore: assert all(x['center_radius_060_free'] for x in bore)
        all_parts.append(dict(index=index+1,name=part['name'],layers=len(layers),first_layer_nominal_area_mm2=shapes[index,.12].area,
             unsupported_components=orphans,max_free_bridge_or_overhang_centerline_mm=max((p['free_centerline_mm'] for p in bridges),default=0),
             thread_layers_with_nominal_wall_breaks=sum(not p['ring_closed'] for p in bore if .24<p['z_mm']<=6.12) if bore else None,
             upper_pin_all_layers_closed=all(p['ring_closed'] for p in bore if p['z_mm']>6.12) if bore else None,
             bore_radius_060_free=all(p['center_radius_060_free'] for p in bore) if bore else None,
             motor_and_guide_clearance_screens_passed=True if part['name']=='half' else None,
             socket_core_open_to_252mm=True if part['name']=='cup' else None))
        critical.append((part,lo,hi,layers))
    return dict(project_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),geometry_vertex_error_mm=error,body_count=len(objects),parts=all_parts,
                gcode_estimates=[l for l in g.splitlines() if l.startswith(('; model printing time','; total filament'))],settings=settings),shapes,critical

def main():
    ap=argparse.ArgumentParser(__doc__);ap.add_argument('--resliced',type=Path,required=True);a=ap.parse_args()
    first,shapes,critical=analyze(HERE/'microstepper-rig.3mf'); second,other,_=analyze(a.resliced)
    assert first['settings']==second['settings']
    assert shapes.keys()==other.keys()
    changes=[shapes[k].symmetric_difference(other[k]).area/max(shapes[k].area,.001) for k in shapes]
    # Independently compare functional volumes to the owner's original coupon plate.
    old=trimesh.load(HERE.parent/'2026-10-15-compact-screw-fit/compact-five-pairs.stl',force='mesh').split()
    comparisons=[]
    for name,center,zcut in [('screw',(7,7),2.41),('pin',(7,23),.75)]:
        m=min(old,key=lambda m:np.linalg.norm(m.bounds.mean(axis=0)[:2]-np.array(center))).copy()
        m.apply_translation([-center[0],-center[1],0])
        region=md.Manifold.cube([20,20,30]).translate([-10,-10,zcut])
        # Original dots stand above the square foot, outside the thread radius.
        if name=='screw': region=md.Manifold.cylinder(30,1.65,1.65,64).translate([0,0,zcut])
        orig=solid(m)^region;new=solid(trimesh.load(HERE/f'{name}.stl',force='mesh'))^region
        difference=(orig-new).volume()+(new-orig).volume()
        assert difference<.001,(name,difference)
        comparisons.append(dict(part=name,comparison_above_z_mm=zcut,functional_volume_symmetric_difference_mm3=difference))
    settings=first.pop('settings');second.pop('settings')
    report=dict(bambu_version='02.08.02.61',original=first,resliced=second,settings_equal=True,max_per_part_layer_footprint_symmetric_difference_fraction=max(changes),functional_geometry_vs_original_coupon=comparisons,
                limits=['Nominal G-code footprints are not measured extrusion.', 'CLI project reopening/reslicing; no interactive GUI inspection.', 'Physical motor fit, tube grip, friction, torque, heating and speed are unmeasured.'])
    (HERE/'slicer-review.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'saved-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    plot(critical,shapes)
    print(json.dumps(report,indent=2))

def plot(critical,shapes):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(13,8))
    for ax,(i,target,title) in zip(axes.flat,[(0,3.6,'Frame: motor cavity'),(0,2.16,'Frame: square guide'),(2,2.52,'Cup: open socket'),(2,2.76,'Cup: roof bridge'),(3,9.12,'Preserved screw thread'),(4,3.12,'Pin: thin internal thread')]):
        part,lo,hi,layers=critical[i];z=min(layers,key=lambda z:abs(z-target));ps=layers[z]
        for p in ps:ax.plot([p['x'],p['x1']],[p['y'],p['y1']],color='#276b85',linewidth=max(.3,p['width']*1.5))
        if i==0:
            cx=lo[0]+18; cy=hi[1]-(6 if target>3 else 40)
            ax.set_xlim(cx-7,cx+7);ax.set_ylim(cy-7,cy+7)
        else:
            ax.set_xlim(lo[0]-1,hi[0]+1);ax.set_ylim(lo[1]-1,hi[1]+1)
        ax.set_aspect('equal');ax.set_title(f'{title}\nZ = {z:.2f} mm');ax.set_xlabel('bed X mm');ax.set_ylabel('bed Y mm')
    fig.tight_layout();fig.savefig(HERE/'toolpaths.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
