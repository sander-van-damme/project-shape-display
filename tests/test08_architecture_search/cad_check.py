"""Export real CSG/STLs and run scoped interference queries using installed OpenSCAD.

No collision-free claim about omitted bearings, detents, head or structural frame.
Empty intersection is expected to return OpenSCAD status 1; other errors fail.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import analysis


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--render',action='store_true')
    args=ap.parse_args()
    exe=shutil.which('openscad.com') or shutil.which('openscad')
    if not exe: raise SystemExit('OpenSCAD not installed; analytical results remain usable')
    analysis.main()
    root=analysis.HERE; out=root/'results'; source=root/'coupon.scad'
    records=[]
    def run(name, defs, empty=False, render=False):
        target=out/name
        if target.exists(): target.unlink()  # Only this exact regenerated artifact.
        command=[exe,'-o',str(target)]
        for d in defs: command += ['-D',d]
        if render: command += ['--imgsize=1400,1000','--viewall','--autocenter','--projection=o']
        command += [str(source)]
        proc=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=120)
        log=proc.stdout+proc.stderr
        if empty:
            ok='Current top level object is empty.' in log and not target.exists() and 'ERROR:' not in log and 'WARNING:' not in log
        else:
            ok=proc.returncode==0 and target.exists() and target.stat().st_size>0 and 'ERROR:' not in log and 'WARNING:' not in log
        records.append(dict(artifact=name,definitions=defs,passed=ok,log=log))
        if not ok:
            (out/'cad_checks.json').write_text(json.dumps(records,indent=2))
            raise RuntimeError(f'{name}: {log}')
        print(f'CAD verified: {name}',flush=True)
    for part in ['rotor','follower','follower_guide','body_guide','lift_plate']:
        run(part+'.stl',[f'part="{part}"'])
    run('assembly.csg',['part="assembly"'])
    for level in range(5):
        run(f'interference_level_{level}.stl',['part="collision"',f'level={level}'],empty=True)
    # Full rotational sweep is analytically bounded by radius; these sampled solids
    # independently catch wrong axes/datum errors in the actual SCAD construction.
    for angle in range(0,360,18):
        run(f'interference_raised_{angle}.stl',['part="collision"','raised=true',f'rotation={angle}'],empty=True)
    if args.render:
        run('section.png',['part="section"'],render=True)
        run('rotor.png',['part="rotor"'],render=True)
        run('assembly.png',['part="assembly"'],render=True)
    (out/'cad_checks.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'{len(records)} CAD exports/interference checks passed (scoped coupon only).')


if __name__=='__main__': main()
