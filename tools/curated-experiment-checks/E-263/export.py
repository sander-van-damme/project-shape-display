#!/usr/bin/env python3
"""Export one fixed article; BOSL2 checkout is an explicit, verified input.
Python stdlib; OpenSCAD. Output is reproducible, not physical qualification.
"""
import argparse, os, pathlib, subprocess
REV = '136e6367e65d52196a3ea51d03156f8b622c60fc'
PARTS = ('pin', 'screw', 'frame_front', 'frame_back', 'land_front', 'land_back', 'key')
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bosl2', required=True, type=pathlib.Path)
    p.add_argument('--output', required=True, type=pathlib.Path)
    a = p.parse_args()
    rev = subprocess.check_output(['git','-C',str(a.bosl2),'rev-parse','HEAD'],text=True).strip()
    assert rev == REV, (rev, REV)
    assert not subprocess.check_output(['git','-C',str(a.bosl2),'status','--porcelain'],text=True).strip()
    assert a.bosl2.name == 'BOSL2'
    a.output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OPENSCADPATH=str(a.bosl2.resolve().parent))
    for part in PARTS:
        out = a.output / (part+'.stl')
        run = subprocess.run(['openscad','-o',str(out),'-D',f'part="{part}"',
            str(pathlib.Path(__file__).with_name('article.scad'))],env=env,capture_output=True,text=True)
        assert run.returncode == 0 and 'WARNING' not in run.stderr and 'ERROR' not in run.stderr, run.stderr
        assert out.stat().st_size > 84
        print(part, out.stat().st_size, flush=True)
