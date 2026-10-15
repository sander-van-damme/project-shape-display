#!/usr/bin/env python3
"""Independent mixed free/sticky descent audit, using exported nominal meshes.

Every pin can be unselected, free-following or sticky (3**4=81 combinations).
Main downward head stroke is 5 mm, without blind reversal precompensation.
All selected ground pawls restore before the final 1.15-mm nominal seating.
This uses exact nominal backlash; individual manual dog retirement remains
necessary when real fits/compliance cause different final seating points.
"""
import argparse,hashlib,itertools,json,re
from pathlib import Path
import numpy as np
import trimesh
C={'pin':8,'ground_comb':2,'drive_key':4,'carriage_base':1,'carriage_lid':1,'root_clamp':2,'lower_guide':1,'upper_guide':1,'ground_seat':1,'frame_foot':4,'bottom_guide':1,'spacer':12,'dog_keeper':4,'ground_keeper':4,'bolt':10,'nut':10}
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'cad'/'rack_handoff.scad');ap.add_argument('--meshes',type=Path,default=Path('work/des008-handoff-review/components'));ap.add_argument('--nominal-results',type=Path,default=Path('work/des008-handoff-review/poses.json'));ap.add_argument('--output',type=Path,default=Path('work/des008-handoff-review/mixed-descent.json'));a=ap.parse_args()
s=a.source.read_bytes();sha=hashlib.sha256(s).hexdigest();src=s.decode();nom=json.loads(a.nominal_results.read_text());assert nom['source_sha256']==sha
def val(name):return float(re.search(r'^'+name+r'=([.0-9-]+);',src,re.M).group(1))
slot=val('key_slot_play');gap=val('groove_h')-val('drive_tip_h');unload=val('unload');preload=unload+val('dog_initial_gap');release=val('release');total_seat=unload+gap+slot
assert abs(total_seat-1.15)<1e-8
baseold=json.loads(re.search(r'^active_h=(\[[^;]+\]);',src,re.M).group(1));old=[5,5,10,10]
names=[f'{c}-{i}' for c,n in C.items() for i in range(n)]+['active-comb-'+''.join(map(str,k)) for k in itertools.product((0,1),repeat=4)]
m={n:trimesh.load_mesh(a.meshes/(n+'.stl')) for n in names};cache={};hits={};cases=0

def overlap(an,ao,bn,bo):
 rel=tuple(round(float(y-x),7) for x,y in zip(ao,bo));key=(an,bn,rel)
 if key in cache:return cache[key]
 am=m[an];bm=m[bn];bounds=bm.bounds+np.asarray(rel)
 if np.any(np.minimum(am.bounds[1],bounds[1])-np.maximum(am.bounds[0],bounds[0])<=1e-5):cache[key]=0.;return 0.
 bm=bm.copy();bm.apply_translation(rel);v=float(abs(trimesh.boolean.intersection([am,bm],engine='manifold').volume))
 if not np.isfinite(v):raise RuntimeError('Non-finite intersection volume')
 cache[key]=v;return v

stages=[('main_move',0,True,False,False,False),('all_pawls_restored',0,False,False,False,False),('seat_0.30',.3,False,False,False,False),('free_dogs_centered',.6,False,False,False,False),('free_dogs_retired',.6,False,True,False,False),('sticky_pins_seated',total_seat,False,True,False,False),('sticky_dogs_centered',.6,False,True,False,True),('all_dogs_retired',.6,False,True,True,True)]
for modes in itertools.product((0,1,2),repeat=4):
 mask=[int(k!=0) for k in modes]
 for stage,t,free,retire_free,retire_all,center_sticky in stages:
  dz=preload-5-t
  parts={n:(n,(0.,0.,0.)) for n in names if not n.startswith(('active-comb','ground_keeper','ground_comb-0'))}
  parts['ground_comb-0']=('active-comb-'+''.join(map(str,mask)) if free else 'ground_comb-0',(0.,0.,0.))
  for i,mode in enumerate(modes):
   offset=max(0.,(unload if mode==1 else total_seat)-t)
   if mode==2 and center_sticky:offset=0.
   on=bool(mode) and not retire_all and not (mode==1 and retire_free)
   pinz=old[i]-baseold[i]+(-5+offset if mode else 0)
   keylift=slot if mode==2 and not center_sticky else max(0.,t-unload-gap) if mode==1 else 0.
   if not on:keylift=0.
   parts[f'pin-{i}']=(f'pin-{i}',(0.,0.,pinz))
   parts[f'drive_key-{i}']=(f'drive_key-{i}',(0.,-release if on else 0.,dz+keylift))
   parts[f'dog_keeper-{i}']=(f'dog_keeper-{i}',(0.,2.45 if on else 0.,dz))
   if mode and free:parts[f'ground_keeper-{i}']=(f'ground_keeper-{i}',(0.,0.,0.))
  for n in ('carriage_base-0','carriage_lid-0','bolt-8','bolt-9','nut-8','nut-9'):parts[n]=(n,(0.,0.,dz))
  for (la,(an,ao)),(lb,(bn,bo)) in itertools.combinations(parts.items(),2):
   v=overlap(an,ao,bn,bo)
   if v>1e-4:
    key=(la,lb)
    if key not in hits:hits[key]={'a':la,'b':lb,'max_mm3':v,'first_modes':modes,'first_stage':stage,'cases':0}
    hits[key]['max_mm3']=max(hits[key]['max_mm3'],v);hits[key]['cases']+=1
  cases+=1
result={'source_sha256':sha,'cases':cases,'drag_combinations':81,'modes':{'0':'unselected','1':'free following','2':'resists descent'},'stages':[k[0] for k in stages],'main_downward_head_stroke_mm':5,'height_above_target_when_ground_restored_mm':{'free':unload,'sticky':total_seat},'ground_insertion_window_mm':[0,val('groove_h')-val('ground_tip_h')],'nominal_final_seating_head_travel_mm':total_seat,'retirement_sequence':'Free-following dogs are centered and withdrawn after0.60mm seating. Remaining sticky pins seat after1.15mm total; head then rises0.55mm to center their dogs before withdrawal. These nominal distances do not replace observed manual fit/support checks.','unique_intersections':len(cache),'collisions':list(hits.values()),'limits':'Exact nominal backlash/slot dimensions and rigid parts. Restoring ground support before final seating is essential. Does not qualify friction, force, print variation, manually observed individual dog retirement or blind automatic overtravel.'}
if hashlib.sha256(a.source.read_bytes()).hexdigest()!=sha:raise RuntimeError('CAD changed during verification')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(hits))
