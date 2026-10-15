#!/usr/bin/env python3
"""Export oriented rig parts, with mesh/bounds/hash ledger. No slicer or fit claim."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, subprocess
import trimesh
HERE=Path(__file__).resolve().parent
COUNTS={'pin':8,'ground_comb':2,'drive_key':4,'carriage_base':1,'carriage_lid':1,
 'root_clamp_active':1,'root_clamp_witness':1,'lower_guide':1,'upper_guide':1,
 'ground_seat':1,'bottom_guide':1,'frame_foot':4,'spacer_long':4,'spacer_bottom':4,'spacer_short':4,'dog_keeper':4,'ground_keeper':4}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'cad/rack_handoff.scad');ap.add_argument('--output',type=Path,default=Path('work/des008-rack/parts'));a=ap.parse_args()
 source=a.source.read_bytes();sha=hashlib.sha256(source).hexdigest();a.output.mkdir(parents=True,exist_ok=True)
 def export(item):
  name,quantity=item;path=a.output/(name+'.stl')
  run=subprocess.run(['openscad','-q','-o',str(path),'-D',f'part="{name}"',str(a.source)],capture_output=True,text=True)
  if run.returncode:raise RuntimeError(name+': '+run.stderr)
  mesh=trimesh.load_mesh(path);body_count=len(mesh.split());minimum_z=float(mesh.bounds[0,2])
  assert mesh.is_volume and body_count==1,(name,'invalid mesh')
  assert abs(minimum_z)<0.002,(name,'not placed on bed',minimum_z)
  return name,{'quantity':quantity,'body_count':body_count,'watertight':bool(mesh.is_watertight),
   'bounds_mm':mesh.bounds.tolist(),'volume_mm3':float(mesh.volume),'stl_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:parts=dict(pool.map(export,COUNTS.items()))
 assert hashlib.sha256(a.source.read_bytes()).hexdigest()==sha,'Source changed during export'
 total=sum(x['quantity']*x['volume_mm3'] for x in parts.values())
 result={'source_sha256':sha,'evidence':'Nominal connected oriented mesh geometry only; no assembly, slicer or physical qualification',
  'part_count':sum(COUNTS.values()),'material_solid_volume_mm3':total,'solid_PLA_g_at_1_24':total*.00124,'parts':parts}
 (a.output/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='parts'},indent=2))
if __name__=='__main__':main()
