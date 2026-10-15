#!/usr/bin/env python3
"""Rigid nominal checks for the resident integration study, not physical proof."""
import argparse,concurrent.futures,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,default=ROOT.parent/'cad/resident_cell.scad')
parser.add_argument('--output',type=Path,default=Path('work/des008-resident'))
args=parser.parse_args()
RESULT_ROOT=args.output.resolve();RESULT_ROOT.mkdir(parents=True,exist_ok=True)
OUT=RESULT_ROOT/'checks';OUT.mkdir(exist_ok=True)
SOURCE=args.source.resolve()
source_sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()

def mesh(part, **kw):
    key=part+'_'+ '_'.join(f'{k}{v}' for k,v in sorted(kw.items()))
    out=OUT/(key+'.stl')
    cmd=['openscad','-o',str(out),'-D',f'part="{part}"']
    for k,v in kw.items():cmd+=['-D',f'{k}={v}']
    subprocess.run(cmd+[str(SOURCE)],capture_output=True,check=True)
    return trimesh.load(out,force='mesh')

parts=['pin','channel','dog','dog_guide','rail','b_dog','b_rail','ground_seat','channel_top','pockets','cassette','codebar','lower_codebar','writer_pair']
with concurrent.futures.ThreadPoolExecutor(4) as ex:
    mm=dict(zip(parts,ex.map(mesh,parts)))

def shift(m,x=0,y=0,z=0):
    n=m.copy();n.apply_translation([x,y,z]);return n
def volume(a,b):
    if np.any(a.bounds[1]<b.bounds[0]) or np.any(b.bounds[1]<a.bounds[0]):return 0.
    return float(abs(trimesh.boolean.intersection([a,b],engine='manifold').volume))

results=[]
def check(name,a,b):
    v=volume(a,b);results.append(dict(name=name,intersection_mm3=v,nominal_clear=v<1e-6))

for bit in (0,1):
 for a in (0,.85):
  dy=-1.6*(1-bit)+a-.85
  chan=shift(mm['channel'],y=dy)
  dog=shift(mm['dog'],y=dy)
  bd=shift(mm['b_dog'],y=dy)
  check(f'dog_channel_b{bit}_A{a}',dog,chan)
  check(f'B_channel_b{bit}_A{a}',bd,chan)
  check(f'dog_guide_b{bit}_A{a}',dog,mm['dog_guide'])
  check(f'B_guide_b{bit}_A{a}',bd,shift(mm['dog_guide'],z=35.4))
  check(f'channel_pin_b{bit}_A{a}',chan,mm['pin'])
  check(f'far_dog_neighbor_b{bit}_A{a}',dog,shift(mm['pin'],y=-6.35))
  check(f'far_B_neighbor_b{bit}_A{a}',bd,shift(mm['pin'],y=-6.35))
  check(f'upper_register_b{bit}_A{a}',chan,shift(mm['channel_top'],y=a-.85))
  check(f'lower_register_b{bit}_A{a}',chan,shift(mm['pockets'],y=a-.85))
  if a==0:
   check(f'raised_channel_dog_b{bit}',shift(chan,z=2),dog)
   check(f'raised_channel_B_b{bit}',shift(chan,z=2),bd)
   check(f'raised_channel_register_b{bit}',shift(chan,z=2),shift(mm['channel_top'],y=-.85))
 for h in range(0,51,5):
  check(f'acquire_b{bit}_h{h}',shift(mm['dog'],y=-1.6*(1-bit)),shift(mm['pin'],z=h))

for h0 in range(0,51,5):
 for d in (-20,-10,-5,5,10,20):
  if not 0<=h0+d<=50:continue
  # 0.3 backlash closes, another0.1 unloads, then signed motion.
  dog=shift(mm['dog'],z=.4+d)
  pin=shift(mm['pin'],z=h0+.1+d)
  check(f'loaded_h{h0}_d{d}',dog,pin)
  check(f'loaded_channel_h{h0}_d{d}',dog,mm['channel'])
  if d<0:
   check(f'sticky_down_h{h0}_d{d}',dog,shift(mm['pin'],z=h0+.7+d))
  check(f'final_seat_h{h0}_d{d}',shift(dog,z=-.7),shift(mm['pin'],z=h0+d))

for b in (0,1):
 cb=mesh('writer_pair',bit=b,A=0)
 for current in (0,1):
  ch=mesh('channel',bit=current,A=0,row_lift=0)
  check(f'disabled_row_data{b}_stored{current}',ch,cb)
  if current==b:check(f'OLD_acquisition{b}',shift(ch,z=2),cb)
  else:
   results.append(dict(name=f'wrong_OLD{b}_{current}',intersection_mm3=volume(shift(ch,z=2),cb),expected='must obstruct'))

for b in (0,1):
 for B in (0,.2,.5,1):
  paw=mesh('pawl',bit=b,B=B)
  bd=mesh('b_dog',bit=b,B=B)
  check(f'B_ramp_b{b}_stroke{B}',bd,paw)
  check(f'pawl_pin_b{b}_stroke{B}',paw,mm['pin'])

I=(1.6*2.4**3-1*1.7**3-.3*1**3)/12
area=1.6*2.4-1*1.7-.3*1
span=134
mechanics=dict(channel_I_yload_mm4=I,channel_solid_area_mm2=area,
 channel_steel_mass_g=area*136*.00785,all4096_channel_kg=area*136*.00785*4096/1000,
 channel_deflection_mm_per_N={str(E):span**3/(48*E*I) for E in (3000,200000)},
 channel_complete_steel_mass_g=float(mm['channel'].volume)*.00785,channel_complete_all4096_kg=float(mm['channel'].volume)*.00785*4096/1000,
 pin_volume_mm3=float(mm['pin'].volume),pin_PLA_mass_g=float(mm['pin'].volume)*.00124,
 rail_deflection_mm_at_1N_each=5*32*203.2**3/(384*200000*(.4*20.45**3/12)),
 pawl_leaf_force_N_at_085=3*200000*(1.2*.4**3/12)/40**3*.85,
 geometry=dict(pitch=6.35,height_range=50,A_home=-30.4,A_take_up=.4,A_up_seat=.7,A_up_center=.3,A_down_backlash_compensation=0,A_down_seat=.7,A_down_center=.3,
 A_pulse_max=20,B_stroke=1.2,B_approach=.35,pawl_release=.85,common_A=.85,data_motion=1.6,row_lift=2,
 pin_low_cap_top=136.2,pin_high_cap_top=186.2,memory_bottom=-107,total_envelope=293.2,
 ground_rack_interval=[-50.4,-.4],A_acquisition_rack_interval=[-80.4,-30.4],same_face_union=[-80.4,-.4]))
out=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),scope='Nominal rigid geometry; no tolerance/yield, contact-force, or full handoff proof',
 results=results,failures=[r for r in results if r.get('nominal_clear') is False],mechanics=mechanics,
 mesh_parts={k:dict(watertight=v.is_watertight,bodies=len(v.split()),volume=float(v.volume)) for k,v in mm.items()})
(RESULT_ROOT/'checks.json').write_text(json.dumps(out,indent=2)+'\n')
assert all(v['watertight'] and v['bodies']==1 for v in out['mesh_parts'].values()), 'disconnected or nonmanifold intended part'
assert not out['failures'], 'nominal collision detected'
assert all(r['intersection_mm3']>1e-4 for r in results if r.get('expected')), 'wrong OLD did not obstruct'
print(json.dumps(dict(checks=len(results),failures=out['failures'],mechanics=mechanics),indent=2))

assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_sha, 'Source changed during verification'
