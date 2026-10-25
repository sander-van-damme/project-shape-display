#!/usr/bin/env python3
"""Reproduce 90/180/270-degree roll screening; final saved duplicates are checked separately.
Run build_projects.py for BC first; --profiles points to its scratch directory.
This writes scratch evidence only, never overwrites a delivered project.
"""
from pathlib import Path
import argparse,subprocess,zipfile,importlib.util,collections,json
import trimesh,numpy as np
from shapely.affinity import translate
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(__doc__);ap.add_argument('--bambu',type=Path,required=True);ap.add_argument('--profiles',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);a=ap.parse_args();w=a.scratch.resolve();w.mkdir(parents=True,exist_ok=True);profiles=a.profiles.resolve();meshes=[]
for i,angle in enumerate([90,180,270]):
 m=trimesh.load(P/'components/C-pin-18-upright.stl');m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(angle),[0,0,1]));m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));m.apply_translation([80+i*12,98,2.2]);meshes.append(m)
plate=trimesh.util.concatenate(meshes);plate.export(w/'trial.stl')
cmd=[str(a.bambu.resolve()),'--datadir',str(w/'studio-data'),'--load-settings',str(profiles/'printer.json')+';'+str(profiles/'process.json'),'--load-filaments',str(profiles/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf','trial.3mf','--outputdir',str(w),str(w/'trial.stl')]
result=subprocess.run(cmd,capture_output=True,text=True,cwd=w);(w/'slice.log').write_text(result.stdout+result.stderr);assert result.returncode==0
spec=importlib.util.spec_from_file_location('reader',P.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
with zipfile.ZipFile(w/'trial.3mf') as z:bounds,_,_,_=reader.project_bounds(z);paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode())
shift=bounds[0]-plate.bounds[0];results=[]
for i,angle in enumerate([90,180,270]):
 cx,cy=shift[:2]+np.array([80+i*12,80]);layers=collections.defaultdict(list)
 for p in paths:
  if abs((p['x']+p['x1'])/2-cx)<2.3 and -.1<(p['y']+p['y1'])/2-cy<18.1 and p['role']!='Skirt':layers[p['z']].append(p)
 previous=None;orphans=[]
 for z,ps in sorted(layers.items()):
  fp=translate(reader.footprint(ps),-cx,-cy)
  if previous is not None:
   for poly in list(fp.geoms) if hasattr(fp,'geoms') else [fp]:
    if poly.area>.005 and poly.intersection(previous.buffer(.01)).area<.001:orphans.append(dict(z_mm=z,area_mm2=poly.area,bounds_mm=list(poly.bounds)))
  previous=fp
 results.append(dict(roll_degrees=angle,orphans=orphans))
(w/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
