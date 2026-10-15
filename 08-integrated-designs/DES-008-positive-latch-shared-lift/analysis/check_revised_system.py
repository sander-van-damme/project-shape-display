#!/usr/bin/env python3
"""Independent stdlib audit of resident-cell mass, bank drive, and handoff timing.
Uses the canonical repository workload generator only; motion/scheduling and
rectilinear volume accounting below are independently implemented.
"""
import argparse,hashlib,importlib.util,itertools,json,math
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CAD=ROOT/'08-integrated-designs/DES-008-positive-latch-shared-lift/cad/resident_cell.scad'
ANALYSIS=ROOT/'08-integrated-designs/DES-008-positive-latch-shared-lift/analysis'
workloads=None

def source_key(p):
 try:return str(p.relative_to(ROOT))
 except ValueError:return str(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def travel(d,v=80.,acc=800.):
 d=abs(d)
 return 2*math.sqrt(d/acc) if d<=v*v/acc else d/v+v/acc

def micro(d):return travel(d,20,800)
def motion(d,sign,revised):
 if not revised:return 2*travel(d)+2*micro(.3)
 return 2*travel(d)+micro(.4)+micro(.7)+micro(.3)

@lru_cache(None)
def sequence_options(targets):
 if not targets:return [()]
 for count in range(max(1,math.ceil(max(targets)/20)),10):
  good=[]
  for seq in itertools.combinations_with_replacement((5,10,20),count):
   reach={0}
   for d in seq:reach|={x+d for x in reach}
   if set(targets)<=reach:good.append(seq)
  if good:return good
 raise AssertionError(targets)
@lru_cache(None)
def bits_for(target,seq):
 for bits in itertools.product((0,1),repeat=len(seq)):
  if sum(b*d for b,d in zip(bits,seq))==target:return bits
 raise AssertionError((target,seq))

def bank(delta,row_time,full_scan,revised):
 nr=len(delta);n=len(delta[0]);old=tuple(tuple(0 for _ in range(n)) for _ in range(nr))
 row_writes=0;total_motion=0;up=[];down=[];support=0
 for sign in (1,-1):
  targets=tuple(sorted({sign*x for row in delta for x in row if sign*x>0}))
  if not targets:continue
  options=[]
  for seq in sequence_options(targets):
   rep={v:bits_for(v,seq) for v in targets}
   masks=[tuple(tuple(int(sign*x>0 and rep[sign*x][i]) for x in row) for row in delta) for i in range(len(seq))]
   prev=old;writes=0
   for mask in masks:
    writes+=nr if full_scan else sum(a!=b for a,b in zip(prev,mask));prev=mask
   cost=writes*row_time+sum(.4+motion(d,sign,revised) for d in seq)
   options.append((cost,seq,masks,writes))
  cost,seq,masks,writes=min(options,key=lambda v:v[0])
  row_writes+=writes;total_motion+=sum(motion(d,sign,revised) for d in seq);support+=.4*len(seq)
  (up if sign==1 else down).extend(seq);old=masks[-1]
  for r in range(nr):
   for c in range(n):
    assert sum(d for d,m in zip(seq,masks) if m[r][c])==max(0,sign*delta[r][c])
 pulses=len(up)+len(down)
 if not pulses:return dict(seconds=0,writes=0,up=[],down=[],budget=1e6)
 row_writes+=nr if full_scan else sum(any(row) for row in old)
 retry_fixed=.4+max(motion(20,s,revised) for s in (1,-1))
 ledger=dict(program=row_writes*row_time,support=support,motion=total_motion,retry=nr*row_time+retry_fixed)
 budget=(30-4-support-total_motion-retry_fixed)/(row_writes+nr)
 return dict(seconds=sum(ledger.values()),ledger=ledger,writes=row_writes,up=up,down=down,budget=budget)

def schedule(a,b,row_time=.08,full_scan=False,revised=True):
 n=len(a);delta=tuple(tuple(v-u for u,v in zip(ra,rb)) for ra,rb in zip(a,b))
 if not any(any(r) for r in delta):return dict(seconds=0,critical_bank=None,banks=[],budget=1e6)
 banks=[bank(delta[n*k//2:n*(k+1)//2],row_time,full_scan,revised) for k in range(2)]
 i=max(range(2),key=lambda k:banks[k]['seconds'])
 return dict(seconds=4+banks[i]['seconds'],critical_bank=i,banks=banks,budget=min(b['budget'] for b in banks))

def critical_ledger(record):
 return dict(common=4,**record['banks'][record['critical_bank']]['ledger']) if record['banks'] else {}
def sum_ledgers(*records):
 keys={k for r in records for k in r}
 return {k:sum(r.get(k,0) for r in records) for k in sorted(keys)}

def category(pairs,row_time=.08,full_scan=False):
 base={k:schedule(a,b,row_time,full_scan,False) for k,(a,b) in pairs.items()}
 new={k:schedule(a,b,row_time,full_scan,True) for k,(a,b) in pairs.items()}
 bk=max(base,key=lambda k:base[k]['seconds']);nk=max(new,key=lambda k:new[k]['seconds'])
 return dict(cases=len(pairs),baseline_ledger=critical_ledger(base[bk]),revised_ledger=critical_ledger(new[nk]),baseline_seconds=base[bk]['seconds'],revised_seconds=new[nk]['seconds'],increment_of_worst_seconds=new[nk]['seconds']-base[bk]['seconds'],baseline_worst_case=bk,revised_worst_case=nk,revised_critical=new[nk],revised_row_time_limit=min(v['budget'] for v in new.values()),largest_single_case_increment=max(new[k]['seconds']-base[k]['seconds'] for k in base))

# Exact volume of an axis-aligned union minus an axis-aligned union. Midpoints
# partition all faces, so this is exact rectilinear integration, not a voxel mesh.
def volume(positive,negative=()):
 edges=[sorted({box[side][axis] for box in positive+list(negative) for side in (0,1)}) for axis in range(3)]
 def inside(point,boxes):return any(all(lo[j]<=point[j]<=hi[j] for j in range(3)) for lo,hi in boxes)
 result=0.
 for ix,iy,iz in itertools.product(*(range(len(e)-1) for e in edges)):
  idx=(ix,iy,iz);lo=[edges[j][idx[j]] for j in range(3)];hi=[edges[j][idx[j]+1] for j in range(3)];p=[(a+b)/2 for a,b in zip(lo,hi)]
  if inside(p,positive) and not inside(p,negative):result+=math.prod(b-a for a,b in zip(lo,hi))
 return result

def box(x,y,z,dx,dy,dz):return ((x,y,z),(x+dx,y+dy,z+dz))
def calculate_mass():
 source=CAD.read_text()
 for token in ('cube([2.8,2.4,130])','cube([4.8,4.8,90])','cube([4.8,4.8,1.2])','cube([1.0,.66,3.2])'):
  assert token in source, 'CAD dimensions changed: re-audit volume before running '+token
 pin=volume([box(-1.4,-1.2,-85,2.8,2.4,130),box(-2.4,-2.4,45,4.8,4.8,90),box(-2.4,-2.4,135,4.8,4.8,1.2)], [box(.3,-1.21,z-2,1,.66,3.2) for z in range(-80,1,5)])
 # C-profile backbone and separate additions. The lug and feet refill portions
 # of the channel, so do NOT subtract its void after unioning the additions.
 core=volume([box(2.2,-1.2,-104,1.6,2.4,136)],[box(2.5,-.85,-104.1,1,1.7,136.2),box(2.1,-.5,-104.1,.5,1,136.2)])
 additions=[box(3.8,.1,-101,.8,.4,.6),box(4.2,.1,-100.4,.4,.4,2),box(2.2,-1.2,-104,1.6,2.4,.5),box(2.2,-1.2,31.5,1.6,2.4,.5),box(2.65,-.4,-105.2,.7,.8,1.3),box(3.8,-.4,30,.65,.8,.8),box(3.95,-.4,28.8,.5,.8,1.3),box(1.9,-1.2,-101,2.2,2.4,.6),box(2.8,.1,31.9,.4,.4,2.1)]
 # Shoulder and two end bridges overlap the original core section.
 channel=core+volume(additions)-1.84*(.6+.5+.5)
 dog=volume([box(1.65,-.4,-1.3,.35,4,2.6),box(.4,-.2,-1.3,1,.4,2.6),box(1.4,-.4,-1.3,1.25,.8,2.6),box(.4,-.2,-1.3,.8,1.7,2.6),box(2.75,-.75,-1.3,.5,1.5,2.6),box(2.6,-.4,-1.3,.2,.8,2.6)])
 dog_guide=.65*.5*3.1-.45*.5*2.8
 a_rail_each=.4*(31*6.35+12)*20.45
 steel=7.85;pla=1.24
 out=dict(pin_volume_mm3=pin,pin_PLA_g=pin*pla/1000,pins_full_4096_kg=pin*pla*4096/1e6,pins_bank_2048_kg=pin*pla*2048/1e6,channel_volume_mm3=channel,channel_steel_g=channel*steel/1000,channels_full_4096_kg=channel*steel*4096/1e6,A_dog_volume_mm3=dog,A_dogs_bank_kg=dog*steel*2048/1e6,A_dog_guides_bank_kg=dog_guide*steel*2048/1e6,A_Z_rails_bank_kg=a_rail_each*steel*64/1e6)
 out['paired_writer_added_bars_full']=128
 out['paired_writer_added_channel_lugs_full']=4096
 out['paired_writer_reference_link_count_full']=256
 writer_length=31*6.35+20
 writer_positive=[box(2.5,-10,34.4,1,writer_length,3),box(4,-10,-98,.8,writer_length,3)]+[box(2.5,y-1.75,-96,2.5,3.5,133.4) for y in (-8,31*6.35+8)]
 writer_negative=[box(x,j*6.35-.3,z,.6,.6,2.2) for x,z in ((2.7,34.3),(4.1,-98.1)) for j in range(32)]
 out['paired_writer_volume_mm3']=volume(writer_positive,writer_negative)
 out['paired_writer_steel_g']=out['paired_writer_volume_mm3']*7.85/1000
 out['paired_writers_full_128_kg']=out['paired_writer_steel_g']*128/1000
 out['writer_acceleration_for_1p6mm_in20ms_m_s2']=4*.0016/.02**2
 out['writer_and_one_channel_inertial_force_N']=(out['paired_writer_steel_g']+out['channel_steel_g'])/1000*out['writer_acceleration_for_1p6mm_in20ms_m_s2']
 out['paired_writer_reference_steel_links_full_kg']=2.5*3.5*133.4*7.85*256/1e6
 out['known_A_Z_parts_bank_kg']=out['A_dogs_bank_kg']+out['A_dog_guides_bank_kg']+out['A_Z_rails_bank_kg']
 out['note']='C-channels are stationary in terrain Z during the pulse; they move with common A in Y and selected-row programming Z. Excluded from main Z moving mass, not massless. 3 kg frame allowance INCLUDES the enumerated A Z parts; do not add them twice. PAWL/ground root, B rail and memory drive are not in main Z force calculation.'
 return out

def drive(mass):
 old_column=(5.4*3.8*80+(36-5.4*3.8)*1.2-3.8*.9*(80-1.2))*2048*1.24/1e6
 screw_mass=7850*math.pi*.008**2*.2
 inertia=4*.5*screw_mass*.008**2+280e-7
 rotating=1.5*inertia*2*math.pi*.8/.005
 cases=[]
 for frame,terrain,label in [(1.5,1,'light'),(2,5,'2kg_frame'),(3,5,'nominal'),(5,5,'5kg_frame')]:
  m=mass['pins_bank_2048_kg']+frame+terrain
  old=old_column+frame+terrain
  for drag in (.01,.03,.1,.5):
   peak=m*(9.81+.8)+2048*drag;steady=m*9.81+2048*drag
   cases.append(dict(case=label,moving_mass_kg=m,frame_includes_local_A_parts_kg=frame,terrain_kg=terrain,drag_N_site=drag,up_peak_N=peak,design_force_N=1.5*peak,ideal_equal_corner_design_N=1.5*peak/4,steady_mechanical_power_W=steady*.08,down_steady_drive_N=2048*drag-m*9.81,torque_1605_at960rpm_Nm=1.5*peak*.005/(2*math.pi*.9)+rotating,prior_torque_same_case_Nm=1.5*(old*(9.81+.8)+2048*drag)*.005/(2*math.pi*.9)+rotating,descent_40mm_gravity_J=m*9.81*.04))
 return dict(prior_columns_bank_kg=old_column,revised_minus_prior_columns_bank_kg=mass['pins_bank_2048_kg']-old_column,rotational_allowance_Nm=rotating,cases=cases,note='Same unqualified 36V motor comparison and 90% ball-screw efficiency as D. No new motor qualification. Holding torque is not torque at960rpm. Price reference is unchanged; heavier columns increase material and handling cost.')

def main():
 global ROOT,CAD,ANALYSIS,workloads
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('work/des008-revised-system.json'));ap.add_argument('--repo-root',type=Path,default=ROOT);ap.add_argument('--cad',type=Path)
 args=ap.parse_args();ROOT=args.repo_root.resolve();CAD=(args.cad.resolve() if args.cad else ROOT/'08-integrated-designs/DES-008-positive-latch-shared-lift/cad/resident_cell.scad');ANALYSIS=ROOT/'08-integrated-designs/DES-008-positive-latch-shared-lift/analysis'
 spec=importlib.util.spec_from_file_location('workload_source',ANALYSIS/'workload_variants.py');workloads=importlib.util.module_from_spec(spec);spec.loader.exec_module(workloads)
 mass=calculate_mass()
 result=dict(evidence='Independent conditional calculation; no physical validation',source_hashes={source_key(CAD):sha(CAD),str((ANALYSIS/'bank_drive.py').relative_to(ROOT)):sha(ANALYSIS/'bank_drive.py'),str((ANALYSIS/'timing_global_pulse.py').relative_to(ROOT)):sha(ANALYSIS/'timing_global_pulse.py')},mass=mass,drive=drive(mass),micro_times_seconds={str(d):micro(d) for d in (.1,.3,.4,.7)},pulse_corrections={str(d):{str(sign):motion(d,sign,True)-motion(d,sign,False) for sign in (1,-1)} for d in (5,10,20)},scene_cases={},category_cases={})
 for n,stroke,row_time,scan in itertools.product((64,80),(40,50),(.08,.12),(False,True)):
  states,pairs,initial,local,extra=workloads.suites(n,stroke)
  key=f'N{n}_stroke{stroke}_row{int(row_time*1000)}_'+('full_scan' if scan else 'dirty_rows')
  result['scene_cases'][key]=category(pairs,row_time,scan)
  if row_time==.08 and scan:
   flat=lambda h:[[h]*n for _ in range(n)]
   neutral=20 if stroke==40 else 30
   cat=dict(cold_start=category(initial,row_time,scan),first_from_neutral=category({k:(flat(neutral),v) for k,v in states.items()},row_time,scan),local_reveal=category(local,row_time,scan),neutral_preparation=category({'prep':(flat(0),flat(neutral))},row_time,scan))
   levels=stroke//5+1
   old=[[5*(x%levels) if x%2 else 0 for x in range(n)] for y in range(n)]
   new=[[0 if x%2 else 5*(x%levels) for x in range(n)] for y in range(n)]
   cat['dense_all_levels']=category({'dense':(old,new)},row_time,scan)
   cat['neutral_then_first']={field:cat['neutral_preparation'][field]+cat['first_from_neutral'][field] for field in ('baseline_seconds','revised_seconds')}
   for field in ('baseline_ledger','revised_ledger'):cat['neutral_then_first'][field]=sum_ledgers(cat['neutral_preparation'][field],cat['first_from_neutral'][field])
   cat['sustained']={}
   for mode in (('40mm',) if stroke==40 else ('shallow','deep')):
    names=[name for name in states if name.startswith(mode+':')]
    legs={a+'>'+b:category({a+'>'+b:(states[a],states[b])},row_time,scan) for a,b in zip(names,names[1:]+names[:1])}
    cat['sustained'][mode]=dict(order=names,legs=legs)
    for field in ('baseline_seconds','revised_seconds'):
     cat['sustained'][mode]['total_'+field]=sum(v[field] for v in legs.values());cat['sustained'][mode]['mean_'+field]=cat['sustained'][mode]['total_'+field]/len(legs)
    for field in ('baseline_ledger','revised_ledger'):cat['sustained'][mode]['total_'+field]=sum_ledgers(*(v[field] for v in legs.values()))
   result['category_cases'][key]=cat
 # Independently reproduce published baseline anchors before trusting differences.
 assert math.isclose(result['scene_cases']['N64_stroke40_row80_dirty_rows']['baseline_seconds'],20.817298334620747,abs_tol=1e-9)
 assert math.isclose(result['scene_cases']['N64_stroke50_row80_dirty_rows']['baseline_seconds'],22.90729833462074,abs_tol=1e-9)
 assert math.isclose(mass['pin_volume_mm3'],2939.488,abs_tol=1e-8)
 assert math.isclose(mass['channel_volume_mm3'],256.632,abs_tol=1e-8)
 assert math.isclose(mass['paired_writer_volume_mm3'],3430.506,abs_tol=1e-8)
 assert math.isclose(travel(5),.15811388300841897,abs_tol=1e-12)
 # A shared dog center constrains every pin to the same interval, independent
 # of whether gravity holds it on the upper flank or friction on the lower.
 pin_before=(.4-.3,.4+.3)
 pin_after_seat=(-.3-.3,-.3+.3)
 ground_interval=(0.,2.)  # 3.2 groove, 1.2 grounded pawl, target phase aligned.
 final_interval=(max(ground_interval[0],pin_after_seat[0]),min(ground_interval[1],pin_after_seat[1]))
 assert final_interval==(0.,0.) and pin_before[0]>=0 and pin_before[1]<=2
 result['handoff_interval_check']=dict(dog_minus_groove_centre_allowed_mm=[-.3,.3],pin_after_main_down_d_mm=pin_before,ground_pawl_insertion_height_window_mm=ground_interval,pin_after_extra_down_point7_without_ground_mm=pin_after_seat,intersection_with_ground_support_mm=final_interval,rejected_precompensated_d_plus_point6_pin_range_mm=[-.5,.1],rejected_up_seat_point4_sticky_pin_residual_mm=.1,finding='Ground must be restored BEFORE the extra0.7downward seating stroke; use this seating stroke after BOTH signs. The earlier UP0.4 centering stroke alone does not force a sticky pin onto its grounded support. Precompensating0.6 in the main stroke can drive gravity-following pins below target before grounding. Bounds are ideal rigid geometry; physical phase and force limits remain unqualified.')
 result['cost_update']=dict(axes_assigned=6,axes_reserved=2,reference_coil_and_board_cost=722.24,generic_motor_driver_pair=20.95,previous_column_polymer_dollars=2*result['drive']['prior_columns_bank_kg']*20,revised_column_polymer_dollars=mass['pins_full_4096_kg']*20,conventional_two_bank_drives_low=903.34,other_common_low_allocations=dict(frame=80,controller=30,coil_power=100,wiring=50))
 cost=result['cost_update'];cost['low_allocation_eight_axes']=722.24+6*20.95+903.34+cost['revised_column_polymer_dollars']+260;cost['low_allocation_six_assigned_axes']=cost['low_allocation_eight_axes']-2*20.95
 cost['illustrative_column_print_hours_at_g_per_hour']={str(flow):mass['pins_full_4096_kg']*1000/flow for flow in (5,15)}
 cost['qualification']='Incomplete allowance, not a quote or complete BOM. Two of six assigned axes use the conventional drive provision; four assigned generic axes and two optional reserved generic axes remain. $100 coil-power allowance is unqualified against704W reference; lift-drive supplies are already inside903.34. No custom resident-channel/dog/pawl fabrication or full frame design included.'
 def check_ledgers(obj):
  if isinstance(obj,dict):
   for prefix in ('baseline','revised'):
    if prefix+'_seconds' in obj and prefix+'_ledger' in obj:assert math.isclose(obj[prefix+'_seconds'],sum(obj[prefix+'_ledger'].values()),abs_tol=1e-8)
   for value in obj.values():check_ledgers(value)
  elif isinstance(obj,list):
   for value in obj:check_ledgers(value)
 check_ledgers(result)
 result['checks']='All category ledgers sum; two published worst-scene baseline anchors, exact pin-volume anchor, triangular motion anchor, and every pulse replay passed.'
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(args.output)
 for k,r in result['scene_cases'].items():print(k,round(r['baseline_seconds'],6),round(r['revised_seconds'],6),round(r['revised_row_time_limit']*1000,3))
if __name__=='__main__':main()
