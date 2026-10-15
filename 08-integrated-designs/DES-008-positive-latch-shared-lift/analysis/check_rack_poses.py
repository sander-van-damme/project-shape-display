#!/usr/bin/env python3
"""Independent nominal signed-mask pose audit for the DES-008 hand rig.

Rebuilds geometry, then transforms independently rather than calling B's pose
checker. 16 masks x two allowed signed pulses x five phases, with separate
forced-lowering, seating and return poses. Includes spacers,
fasteners, both support combs and both families of keepers. No elastic/tolerance,
contact-pressure, slicer, load, or physical qualification follows.
"""
import argparse, concurrent.futures, hashlib, itertools, json, re, subprocess
from pathlib import Path
import numpy as np
import trimesh
COUNTS={'pin':8,'ground_comb':2,'drive_key':4,'carriage_base':1,
 'carriage_lid':1,'root_clamp':2,'lower_guide':1,'upper_guide':1,'ground_seat':1,
 'frame_foot':4,'bottom_guide':1,'spacer':12,
 'dog_keeper':4,'ground_keeper':4,'bolt':10,'nut':10}
PHASES=('park','capture','unloaded','move','restored')
PULSES=(-5,5)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--prototype',type=Path);ap.add_argument('--output',type=Path,default=Path('work/des008-handoff-review/poses.json'));ap.add_argument('--scratch',type=Path,default=Path('work/des008-handoff-review/components'));a=ap.parse_args()
 scad=a.source or (a.prototype/'rack_handoff.scad' if a.prototype else Path(__file__).resolve().parents[1]/'cad'/'rack_handoff.scad');source=scad.read_bytes();sha=hashlib.sha256(source).hexdigest();src=source.decode();a.scratch.mkdir(parents=True,exist_ok=True)
 def val(name):return float(re.search(r'^'+re.escape(name)+r'=([.0-9-]+);',src,re.M).group(1))
 release=val('release');unload=val('unload');preload=unload+val('dog_initial_gap')
 slot=val('key_slot_play');backlash=val('groove_h')-val('drive_tip_h')
 # Keeper addresses are explicit physical positions, independent of key travel.
 assert 'on?-5.55:-8' in src,'Update independent keeper-position model after CAD change'
 def render(job):
  name,c,i,mask=job;path=a.scratch/(name+'.stl');defs={'part':'component','component':c,'index':i,'phase':'unloaded' if mask is not None else 'park','selected':mask or [0,0,0,0],'pulse':0}
  cmd=['openscad','-q','-o',str(path)]
  for k,v in defs.items():cmd+=['-D',f'{k}={json.dumps(v,separators=(",",":"))}']
  p=subprocess.run(cmd+[str(scad)],capture_output=True,text=True)
  if p.returncode:raise RuntimeError(p.stderr)
  return name,trimesh.load_mesh(path)
 jobs=[(f'{c}-{i}',c,i,None) for c,n in COUNTS.items() for i in range(n)]
 jobs += [('active-comb-'+''.join(map(str,m)),'ground_comb',0,list(m)) for m in itertools.product((0,1),repeat=4)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:raw=dict(pool.map(render,jobs))
 invalid=[n for n,m in raw.items() if not m.is_volume or len(m.split())!=1]
 if invalid:raise RuntimeError('Invalid component solids: '+str(invalid))
 cache={};hits={};cases=0
 def overlap(an,ao,bn,bo):
  # Common world translation cannot change intersection.
  rel=tuple(round(float(x-y),7) for x,y in zip(bo,ao));key=(an,bn,rel)
  if key in cache:return cache[key]
  am=raw[an];bm=raw[bn];bb=bm.bounds+np.asarray(rel)
  if np.any(np.minimum(am.bounds[1],bb[1])-np.maximum(am.bounds[0],bb[0])<=1e-5):cache[key]=0.;return 0.
  moved=bm.copy();moved.apply_translation(rel);inter=trimesh.boolean.intersection([am,moved],engine='manifold');v=float(abs(inter.volume))
  if not np.isfinite(v):raise RuntimeError('Non-finite Boolean volume: '+str(key))
  cache[key]=v;return v
 baseold=json.loads(re.search(r'^active_h=(\[[^;]+\]);',src,re.M).group(1))
 by_phase={}
 for mask,pulse in itertools.product(itertools.product((0,1),repeat=4),PULSES):
  old=[5,5,10,10] if pulse<0 else [0,0,5,5]
  phases=PHASES+(('forced_lower','forced_restored','seated_lower','returned') if pulse<0 else ('returned',))
  for phase in phases:
   pre=phase in ('unloaded','move','restored');shift=phase in ('move','restored');capt=phase!='park';free=phase in ('unloaded','move');dz=(preload if pre else 0)+(pulse if shift else 0)
   forced=phase in ('forced_lower','forced_restored','seated_lower')
   if forced:
    pre=phase!='seated_lower';shift=True;capt=True;free=phase=='forced_lower'
    dz=preload+pulse-backlash-slot-(unload if phase=='seated_lower' else 0)
   if phase=='returned':pre=False;shift=True;capt=False;free=False;dz=0.
   parts={k:(k,(0.,0.,0.)) for k in raw if not k.startswith(('active-comb','ground_keeper','ground_comb-0'))}
   parts['ground_comb-0']=('active-comb-'+''.join(map(str,mask)) if free else 'ground_comb-0',(0.,0.,0.))
   for i in range(4):
    parts[f'pin-{i}']=(f'pin-{i}',(0.,0.,old[i]-baseold[i]+(unload if pre and mask[i] else 0)+(pulse if shift and mask[i] else 0)))
    parts[f'drive_key-{i}']=(f'drive_key-{i}',(0.,-release if capt and mask[i] else 0.,dz+(slot if forced and mask[i] else 0)))
    parts[f'dog_keeper-{i}']=(f'dog_keeper-{i}',(0.,2.45 if capt and mask[i] else 0.,dz))
    if free and mask[i]:parts[f'ground_keeper-{i}']=(f'ground_keeper-{i}',(0.,0.,0.))
   for k in ('carriage_base-0','carriage_lid-0','bolt-8','bolt-9','nut-8','nut-9'):parts[k]=(k,(0.,0.,dz))
   for (labela,(an,ao)),(labelb,(bn,bo)) in itertools.combinations(parts.items(),2):
    v=overlap(an,ao,bn,bo)
    if v>1e-4:
     k=(labela,labelb)
     if k not in hits:hits[k]={'a':labela,'b':labelb,'max_mm3':v,'first':{'mask':mask,'pulse':pulse,'phase':phase},'cases':0}
     hits[k]['max_mm3']=max(hits[k]['max_mm3'],v);hits[k]['cases']+=1
   cases+=1
   by_phase[phase]=by_phase.get(phase,0)+1
 if hashlib.sha256(scad.read_bytes()).hexdigest()!=sha:raise RuntimeError('CAD changed during verification; rerun on frozen source')
 result={'source_sha256':sha,'evidence':'nominal rigid CAD poses only; ideal elastic-leaf visualization','cases':cases,'masks':16,'pulses':PULSES,'phases':by_phase,'forced_down_model':{'groove_reversal_mm':backlash,'key_slot_reversal_mm':slot,'seat_mm':unload,'description':'Selected key at upper slot bearing; lower tooth flank pulls resisted pin. Return state is a separate collision endpoint, not a demonstrated continuous transition.'},'unique_intersection_queries':len(cache),'invalid':invalid,'collisions':list(hits.values()),'excluded':'Continuous motion, nonideal deformation/tolerances, key pitch under load, forces, print fit, instructions and physical tests remain separate'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(hits))
if __name__=='__main__':main()
