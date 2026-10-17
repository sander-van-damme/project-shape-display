#!/usr/bin/env python3
"""Quantify original/reopened Bambu extrusion geometry differences."""
import argparse,importlib.util,json,zipfile,hashlib,collections
from pathlib import Path
sp=importlib.util.spec_from_file_location('v',Path(__file__).resolve().parents[2]/'E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project',type=Path,required=True);ap.add_argument('--reopened',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 project=a.project;reopen=a.reopened;target=a.out;label=project.stem
 with zipfile.ZipFile(project) as z: original=z.read('Metadata/plate_1.gcode').decode()
 with zipfile.ZipFile(reopen) as z: repeated=z.read('Metadata/plate_1.gcode').decode()
 pa,_=v.parse(original);pb,_=v.parse(repeated)
 key=lambda p:(p['z'],p['role'],p['x'],p['y'],p['x1'],p['y1'],p['width'])
 ca=collections.Counter(key(p) for p in pa);cb=collections.Counter(key(p) for p in pb)
 changes=sorted(set(p[0] for p in list(ca-cb)+list(cb-ca)))
 print(label,'paths',len(pa),len(pb),'unmatched',sum((ca-cb).values()),sum((cb-ca).values()),'changedlayers',len(changes),flush=True)
 report=dict(original_gcode_sha256=hashlib.sha256(original.encode()).hexdigest(),reopened_gcode_sha256=hashlib.sha256(repeated.encode()).hexdigest(),original_extrusion_segments=len(pa),reopened_extrusion_segments=len(pb),original_unmatched_extrusion_segments=sum((ca-cb).values()),reopened_unmatched_extrusion_segments=sum((cb-ca).values()),layers_with_changed_segment_geometry=changes,original_model_extruded_filament_mm=sum(p['e'] for p in pa),reopened_model_extruded_filament_mm=sum(p['e'] for p in pb),roles_original=dict(collections.Counter(p['role'] for p in pa)),roles_reopened=dict(collections.Counter(p['role'] for p in pb)),changed_layer_footprints=[])
 for z in changes:
  a=v.footprint([p for p in pa if p['z']==z]);b=v.footprint([p for p in pb if p['z']==z]);diff=a.symmetric_difference(b)
  report['changed_layer_footprints'].append(dict(z_mm=z,original_area_mm2=a.area,reopened_area_mm2=b.area,symmetric_difference_area_mm2=diff.area,percent_of_original=100*diff.area/a.area))
 report['max_layer_footprint_change_percent']=max((p['percent_of_original'] for p in report['changed_layer_footprints']),default=0)
 report['caveat']='Comparison uses nominal LINE_WIDTH footprints, not measured printing. Shapely Hausdorff is boundary-sensitive: opening/closing a tiny interior hole may give a large boundary distance despite a small material-area difference. Ordering/flow changes can still differ physically.'
 target.write_text(json.dumps(report,indent=2)+'\n')
 print(label,report['max_layer_footprint_change_percent'],flush=True)

if __name__=='__main__':main()
