#!/usr/bin/env python3
"""Independent rigid geometry replay of frozen DES-008 resident-cell study.

Uses source meshes but not the author's check functions or equations. No force,
tolerance distribution, manufacture, powered timing or physical pass is implied.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('work/des008-resident-independent'));args=parser.parse_args()
DIR=args.output;DIR.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT.parent/'cad/resident_cell.scad'
EXPECTED='780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
OUT=DIR/'meshes';OUT.mkdir(exist_ok=True)

def mesh(part,**kw):
    dest=OUT/(part+''.join(f'_{k}_{v}' for k,v in sorted(kw.items()))+'.stl')
    cmd=['openscad','-o',str(dest),'-D',f'part="{part}"']
    for k,v in kw.items():cmd += ['-D',f'{k}={v}']
    if not dest.exists():subprocess.run(cmd+[str(SOURCE)],capture_output=True,check=True)
    return trimesh.load(dest,force='mesh')

names=['pin','channel','dog','dog_guide','rail','b_dog','b_rail','pawl','ground_seat','channel_top','pockets','cassette','codebar','lower_codebar','writer_pair']
with ThreadPoolExecutor(4) as ex:
    base=dict(zip(names,ex.map(mesh,names)))
record=[]
def shift(m,x=0,y=0,z=0):
    a=m.copy();a.apply_translation([x,y,z]);return a
def test(name,a,b,expected=False):
    if np.any(a.bounds[1]<b.bounds[0]) or np.any(b.bounds[1]<a.bounds[0]):v=0.0
    else:v=float(abs(trimesh.boolean.intersection([a,b],engine='manifold').volume))
    good=(v>1e-5) if expected else (v<1e-6)
    record.append(dict(name=name,intersection_mm3=v,expected_obstruction=expected,pass_check=good))

# Arbitrary OLD-to-NEW states, checking both end registers and disabled row.
for old in [0,1]:
    dy=-.85-1.6*(1-old)
    for r in np.linspace(0,2,9):
        ch=shift(base['channel'],y=dy,z=r)
        for other in ['channel_top','pockets']:
            test(f'row_acquire_{old}_{r}_{other}',ch,shift(base[other],y=-.85))
        for bar in ['codebar','lower_codebar','writer_pair']:
            test(f'OLD_{bar}_{old}_{r}',ch,shift(base[bar],y=dy))
        for name in ['dog','b_dog']:
            test(f'row_acquire_{old}_{r}_{name}',ch,shift(base[name],y=dy))
    for new in np.linspace(0,1,17):
        dy_new=-.85-1.6*(1-new)
        ch=shift(base['channel'],y=dy_new,z=2)
        cb=shift(base['writer_pair'],y=dy_new)
        test(f'NEW_raised_bar_{old}_{new}',ch,cb)
        for other in ['channel_top','pockets']:
            test(f'NEW_raised_{old}_{new}_{other}',ch,shift(base[other],y=-.85))
        for neighbor in [0,1]:
            locked=shift(base['channel'],y=6.35-.85-1.6*(1-neighbor))
            test(f'disabled_neighbor_{old}_{new}_{neighbor}',locked,cb)
    test(f'wrongOLD_{old}',shift(base['channel'],y=dy,z=2),
         shift(base['writer_pair'],y=-.85-1.6*old),expected=True)

# Common A actuation, fixed-ground support and neighboring terrain clearance.
for bit in [0,1]:
 for a in np.linspace(0,.85,18):
    dy=a-.85-1.6*(1-bit)
    ch=shift(base['channel'],y=dy)
    for name in ['dog','b_dog']:
        mover=shift(base[name],y=dy)
        test(f'A_{bit}_{a}_{name}_channel',mover,ch)
        guide=shift(base['dog_guide'],z=35.4 if name=='b_dog' else 0)
        test(f'A_{bit}_{a}_{name}_guide',mover,guide)
        test(f'A_{bit}_{a}_{name}_previous_pin',mover,shift(base['pin'],y=-6.35))
    test(f'A_{bit}_{a}_ground_pawl_channel',base['pawl'],ch)

# B ramp is exact-source geometry, independently sampled beyond endpoint poses.
for bit in [0,1]:
 for b in np.linspace(0,1,21):
    paw=mesh('pawl',bit=bit,B=float(b))
    mover=shift(base['b_dog'],y=-1.6*(1-bit),z=-1.2*b)
    test(f'B_{bit}_{b}_ramp',mover,paw)
    test(f'B_{bit}_{b}_pin',paw,shift(base['pin'],z=.1*bit))

# A downward main stroke must NOT blindly add reversal clearance. A freely
# descending pin follows the upper flank, while a sticky pin lags until the
# lower flank catches. Restore ground support before the final backlash takeup.
for old in range(0,51,5):
 for delta in [-20,-10,-5,5,10,20]:
    if not 0<=old+delta<=50:continue
    down=delta<0
    for progress in np.linspace(0,1,11):
        if down:
            travel=(-delta)*progress
            z_dog=.4-travel
            h_sticky=old+.1-max(0,travel-.6)
            h_gravity=old+.1-travel
        else:
            z_dog=.4+delta*progress;h_sticky=old+.1+delta*progress
        mover=shift(base['dog'],z=z_dog)
        test(f'loaded_{old}_{delta}_{progress}',mover,shift(base['pin'],z=h_sticky))
        if down:test(f'gravity_{old}_{delta}_{progress}',mover,shift(base['pin'],z=h_gravity))
        test(f'loaded_channel_{old}_{delta}_{progress}',mover,base['channel'])
    target=old+delta
    for excess in ([.1,.7] if down else [.1]):
        test(f'restore_{old}_{delta}_{excess}',base['pawl'],shift(base['pin'],z=target+excess))
    # Last0.7 DOWN movement positively seats a sticky pin; the restored pawl
    # prevents overshoot of a gravity-following pin during that same movement.
    z_end=delta+.4
    for progress in np.linspace(0,1,6):
        travel=.7*progress
        z_seat=z_end-travel
        for excess in ([.1,.7] if down else [.1]):
            h=target+max(0,excess-travel)
            test(f'seat_{old}_{delta}_{progress}_{excess}',shift(base['dog'],z=z_seat),
                 shift(base['pin'],z=h))
            test(f'grounded_seat_{old}_{delta}_{progress}_{excess}',base['pawl'],shift(base['pin'],z=h))
    # Both signs positively seat through the lower flank, then rise .3 to clear.
    start=delta-.3
    for progress in np.linspace(0,1,6):
        z=start+.3*progress
        test(f'centre_{old}_{delta}_{progress}',shift(base['dog'],z=z),shift(base['pin'],z=target))

out={
 'source_sha256':EXPECTED,
 'scope':'Nominal rigid geometry only; no assembly, force or tolerance qualification',
 'parts':{name:{'watertight':m.is_watertight,'bodies':len(m.split()),'volume_mm3':float(m.volume)} for name,m in base.items()},
 'check_count':len(record),'failures':[r for r in record if not r['pass_check']],
 'checks':record,
}
(DIR/'independent-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))

assert not out['failures'], 'Nominal resident replay failed'
