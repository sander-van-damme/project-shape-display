"""Export actual coupon STLs; check compiler, dimensions and frozen Test08 contacts.

OpenSCAD 2021.01; no third-party Python packages. --render adds PNGs.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import analyze as a


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--render',action='store_true')
    ap.add_argument('--coupons-only',action='store_true',help='recheck changed Test09 coupons without repeating unchanged historical contacts')
    args=ap.parse_args()
    exe=shutil.which('openscad.com') or shutil.which('openscad')
    if not exe:raise SystemExit('OpenSCAD required for CAD checks; physical status remains unverified')
    a.OUT.mkdir(exist_ok=True)
    a.cad_parameters(json.loads((a.HERE/'params.json').read_text()))
    old=a.HERE.parent/'test08_architecture_search'
    p=json.loads((old/'params.json').read_text())
    # Local generated snapshot; historical files and historical results untouched.
    (a.OUT/'parameters.scad').write_text('\n'.join(f'{k} = {json.dumps(v)};' for group in ['grid','terrain','cam'] for k,v in p[group].items() if type(v) in [int,float])+'\n')
    source=(old/'coupon.scad').read_text().replace('include <results/parameters.scad>','include <parameters.scad>')
    (a.OUT/'baseline.scad').write_text(source)
    records=[]
    def run(name, source, definitions, empty=False):
        dest=a.OUT/name
        if dest.exists():dest.unlink()
        cmd=[exe,'-o',str(dest)]
        for d in definitions:cmd.extend(['-D',d])
        if dest.suffix=='.png':cmd.extend(['--imgsize=1200,900','--viewall','--autocenter','--projection=o'])
        cmd.append(str(source))
        proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        log=proc.stdout+proc.stderr
        clean='WARNING:' not in log and 'ERROR:' not in log
        ok=clean and ((proc.returncode in (0,1) and 'Current top level object is empty.' in log and not dest.exists()) if empty else (proc.returncode==0 and dest.exists() and dest.stat().st_size>0))
        record={'artifact':name,'definitions':definitions,'passed':ok,'log':log}
        if ok and not empty and dest.suffix=='.stl':
            # OpenSCAD 2021 default ASCII STL: inspect all vertex bounds.
            vertices=[tuple(map(float,m)) for m in re.findall(r'vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)',dest.read_text())]
            if not vertices:raise RuntimeError('ASCII STL expected')
            dims=[max(v[i] for v in vertices)-min(v[i] for v in vertices) for i in range(3)]
            record['bbox_mm']=dims
            record['within_256mm_build_box']=max(dims)<=256
            ok=ok and max(dims)<=256;record['passed']=ok
        records.append(record)
        a.save('cad_coupons.json' if args.coupons_only else 'cad_checks.json',{'openscad_version':subprocess.run([exe,'--version'],capture_output=True,text=True).stderr.strip(),
                                 'historical_source_sha256':hashlib.sha256((old/'coupon.scad').read_bytes()).hexdigest(),'checks':records,
                                 'coupon_source_sha256':hashlib.sha256((a.HERE/'coupons.scad').read_bytes()).hexdigest(),
                                 'limits':'No complete integrated head/detent/frame collision or printability certification'})
        if not ok:raise RuntimeError(name+'\n'+log)
        print(name,flush=True)
    src=a.HERE/'coupons.scad'
    for clear in [.05,.1,.15]:
        run(f'fit_tile_{clear:g}.stl',src,['part="fit_tile"',f'clearance={clear}'])
    # Width reduction buys a 0.4 mm web at same pitch, but changes fill/mass.
    run('fit_tile_narrow.stl',src,['part="fit_tile"','body=4.48'])
    run('slider_narrow.stl',src,['part="slider"','body=4.48'])
    for part in ['slider','walls','bushings','shaft','leaf','bench_base','journal_half','collar_half','coupler','beam_half','splice','home_wheel','motor_cradle','home_stop','bearing_half']:
        run(part+'.stl',src,[f'part="{part}"'])
    for k in [4,5,6]:run(f'wheel_{k}.stl',src,['part="wheel"',f'levels={k}'])
    if not args.coupons_only:
        baseline=a.OUT/'baseline.scad'
        for part in ['rotor','follower','follower_guide','body_guide','lift_plate']:
            run('passive_'+part+'.stl',baseline,[f'part="{part}"'])
        run('passive_hollow_follower.stl',baseline,['part="follower"','body_hollow=1'])
        for level in range(5):run(f'contact_{level}.stl',baseline,['part="collision"',f'level={level}'],True)
        for deg in range(0,360,18):run(f'raised_{deg}.stl',baseline,['part="collision"','raised=true',f'rotation={deg}'],True)
    if args.render:
        for part in ['fit_tile','detent_scene','beam_half']:run(part+'.png',src,[f'part="{part}"'])
    print(f'{len(records)} scoped CAD checks complete; mechanical behavior unverified')


if __name__=='__main__':main()
