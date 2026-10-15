#!/usr/bin/env python3
"""Rebuild three alternative complete plates; owners select one, no compilation.
Example from repository root:
  python owner-print-tests/four-pin-screw-demo/generate.py \
    --bosl2 work/compact-screw-fit/BOSL2 --scratch work/four-pin-demo
Requires OpenSCAD, git, and Python trimesh. Then run validate.py.
"""
import argparse, concurrent.futures, os, subprocess
from pathlib import Path
import trimesh

HERE=Path(__file__).resolve().parent
REV='136e6367e65d52196a3ea51d03156f8b622c60fc'

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--scratch',type=Path,required=True)
    a=ap.parse_args()
    library=a.bosl2.resolve()
    assert library.name=='BOSL2', 'OpenSCAD include path requires a BOSL2 directory'
    rev=subprocess.check_output(['git','-C',str(library),'rev-parse','HEAD'],text=True).strip()
    assert rev==REV,(rev,REV)
    assert not subprocess.check_output(['git','-C',str(library),'status','--porcelain'],text=True).strip()
    env=os.environ.copy()
    env['OPENSCADPATH']=str(library.parent)+(os.pathsep+env['OPENSCADPATH'] if env.get('OPENSCADPATH') else '')
    a.scratch.mkdir(parents=True,exist_ok=True)
    def export(item):
        label,relief=item
        path=HERE/f'four-pin-demo-{label}-plate.stl'
        result=subprocess.run(['openscad','-o',str(path),'-D',f'relief={relief}',str(HERE/'demo.scad')],
                              env=env,capture_output=True,text=True)
        log=result.stdout+result.stderr
        (a.scratch/f'demo-{label}-openscad.log').write_text(log)
        assert result.returncode==0 and 'WARNING' not in log and 'ERROR' not in log,log
        mesh=trimesh.load(path)
        assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==12
        mesh.export(path,file_type='stl')
        print(path.name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(export,[('015',.15),('0175',.175),('020',.20)]))

if __name__=='__main__': main()
