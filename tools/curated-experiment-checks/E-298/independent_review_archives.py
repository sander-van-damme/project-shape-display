from pathlib import Path
import zipfile,xml.etree.ElementTree as E,numpy as np,trimesh as tm,json,hashlib
for tag,folder,base in [('A','fit','point-fit'),('B','matrix','point-matrix')]:
 p=Path('owner-print-tests/2026-10-16-self-aligning-point-'+folder)
 src=tm.load(p/(base+'.stl'),force='mesh').split(); dst=[]
 with zipfile.ZipFile(p/(base+'.3mf')) as z:
  assert z.testzip() is None, 'ZIP integrity failure'
  settings=json.loads(z.read('Metadata/project_settings.config'))
  settings_checked={k:settings.get(k) for k in ['printer_model','printer_settings_id','nozzle_diameter','layer_height','initial_layer_print_height','wall_generator','wall_loops','filament_type']}
  assert settings_checked['printer_model']=='Bambu Lab X1 Carbon' and settings_checked['nozzle_diameter']==['0.4']
  gcode=z.read('Metadata/plate_1.gcode')
  gcode_md5=hashlib.md5(gcode).hexdigest()
  saved_md5=z.read('Metadata/plate_1.gcode.md5').decode().strip()
  assert gcode_md5==saved_md5.lower()
  assert b'; layer num/total_layer_count' in gcode
  for n in z.namelist():
   if not (n.startswith('3D/Objects/') and n.endswith('.model')):continue
   r=E.fromstring(z.read(n))
   for me in [x for x in r.iter() if x.tag.endswith('}mesh')]:
    vs=next(x for x in me if x.tag.endswith('}vertices'));ts=next(x for x in me if x.tag.endswith('}triangles'))
    v=[[float(x.attrib[k]) for k in ['x','y','z']] for x in vs];f=[[int(x.attrib[k]) for k in ['v1','v2','v3']] for x in ts]
    m=tm.Trimesh(v,f,process=False)
    m.metadata['closed_after_coordinate_merge']=bool(tm.Trimesh(v,f,process=True).is_watertight)
    dst.append(m)
 src.sort(key=lambda m:round(m.volume,3));dst.sort(key=lambda m:round(m.volume,3))
 assert len(src)==len(dst)
 errors=[]
 for a,b in zip(src,dst):errors.append({'volume_difference_mm3':abs(float(a.volume-b.volume)),'max_sorted_extent_difference_mm':float(np.abs(np.sort(a.extents)-np.sort(b.extents)).max()),'source_watertight':bool(a.is_watertight),'project_watertight':bool(b.is_watertight),'project_closed_after_coordinate_merge':b.metadata['closed_after_coordinate_merge'],'facets_equal':len(a.faces)==len(b.faces)})
 r={'saved_settings_checked':settings_checked,'gcode_md5_matches':True,'gcode_bytes':len(gcode),'project_sha256':hashlib.sha256((p/(base+'.3mf')).read_bytes()).hexdigest(),'source_stl_sha256':hashlib.sha256((p/(base+'.stl')).read_bytes()).hexdigest(),'body_count':len(src),'maximum_volume_difference_mm3':max(x['volume_difference_mm3'] for x in errors),'maximum_sorted_extent_difference_mm':max(x['max_sorted_extent_difference_mm'] for x in errors),'all_closed':all(x['source_watertight'] and x['project_watertight'] for x in errors),'all_facet_counts_equal':all(x['facets_equal'] for x in errors),'all_project_meshes_closed_after_coordinate_merge':all(x['project_closed_after_coordinate_merge'] for x in errors),'topology_note':'Project watertightness preserves the 3MF vertex indices. Coordinate welding can merge distinct indexed vertices after decimal export rounding; that diagnostic is recorded separately.','scope':'Independent volume/extents/facet-count check, complements exact transformed vertex comparison in primary slicer validation.'}
 assert r['all_closed'] and r['all_facet_counts_equal'] and r['maximum_sorted_extent_difference_mm']<0.001 and r['maximum_volume_difference_mm3']<0.01, r
 out=Path('tools/curated-experiment-checks/E-298')/('independent-review-archive-geometry-'+tag+'.json');out.write_text(json.dumps(r,indent=2)+'\n');print(tag,r)
