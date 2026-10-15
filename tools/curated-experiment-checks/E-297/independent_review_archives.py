from pathlib import Path
import zipfile,xml.etree.ElementTree as E,numpy as np,trimesh as tm,json,hashlib
for tag,folder,base in [('A','fit','clutch-fit'),('B','matrix','clutch-matrix')]:
 p=Path('owner-print-tests/2026-10-16-two-half-clutch-'+folder)
 src=tm.load(p/(base+'.stl'),force='mesh').split(); dst=[]
 with zipfile.ZipFile(p/(base+'.3mf')) as z:
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
 r={'project_sha256':hashlib.sha256((p/(base+'.3mf')).read_bytes()).hexdigest(),'source_stl_sha256':hashlib.sha256((p/(base+'.stl')).read_bytes()).hexdigest(),'body_count':len(src),'maximum_volume_difference_mm3':max(x['volume_difference_mm3'] for x in errors),'maximum_sorted_extent_difference_mm':max(x['max_sorted_extent_difference_mm'] for x in errors),'all_closed':all(x['source_watertight'] and x['project_watertight'] for x in errors),'all_facet_counts_equal':all(x['facets_equal'] for x in errors),'all_project_meshes_closed_after_coordinate_merge':all(x['project_closed_after_coordinate_merge'] for x in errors),'topology_note':'Project watertightness preserves the 3MF vertex indices. Coordinate welding can merge distinct indexed vertices after decimal export rounding; that diagnostic is recorded separately.','scope':'Independent volume/extents/facet-count check, complements exact transformed vertex comparison in primary slicer validation.'}
 out=Path('tools/curated-experiment-checks/E-297/validation')/('independent-review-archive-geometry-'+tag+'.json');out.write_text(json.dumps(r,indent=2)+'\n');print(tag,r)
