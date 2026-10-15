#!/usr/bin/env python3
"""Generate compact DES-008 conditional timing evidence; no measured performance.

Example from repository root:
python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/run_timing.py --output work/des008-timing.json
"""
import argparse,importlib.util,itertools,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

global_pulse=load('timing_global_pulse')
retirement=load('timing_retirement')
pipeline=load('timing_target_pipeline')
workloads=global_pulse.p
reference=global_pulse.tp

def category(pairs,fn=global_pulse.schedule,**kwargs):
    runs={name:fn(*ab,**kwargs) for name,ab in pairs.items()}
    worst=max(runs,key=lambda name:runs[name]['seconds'])
    return dict(case_count=len(runs),worst_case=worst,**runs[worst],
        mean_seconds=sum(r['seconds'] for r in runs.values())/len(runs))

def combine_ledger(*records):
    keys={key for record in records for key in record.get('ledger',{})}
    return {key:sum(record.get('ledger',{}).get(key,0) for record in records) for key in sorted(keys)}

def selected_case(n,stroke,row_write,quantum=5,full_row_scan=False):
    states,pairs,initial,local,extra=workloads.suites(n,stroke)
    kw=dict(banks=2,row_write=row_write,quantum=quantum,full_row_scan=full_row_scan)
    neutral=20 if stroke==40 else 30
    flat=lambda h:[[h]*n for _ in range(n)]
    prep=global_pulse.schedule(flat(0),flat(neutral),**kw)
    first=category({name:(flat(neutral),height) for name,height in states.items()},**kw)
    sustained={}
    for mode in (('40mm',) if stroke==40 else ('shallow','deep')):
        names=[name for name in states if name.startswith(mode+':')]
        legs={a+'>'+b:global_pulse.schedule(states[a],states[b],**kw) for a,b in zip(names,names[1:]+names[:1])}
        sustained[mode]=dict(order=names,legs=legs,total_seconds=sum(v['seconds'] for v in legs.values()),
            mean_seconds=sum(v['seconds'] for v in legs.values())/len(legs),total_ledger=combine_ledger(*legs.values()))
    levels=stroke//quantum+1
    # This creates many distinct signed deltas, separately from a uniform lift.
    old=[[quantum*(x%levels) if x%2 else 0 for x in range(n)] for y in range(n)]
    new=[[0 if x%2 else quantum*(x%levels) for x in range(n)] for y in range(n)]
    dense={k:global_pulse.schedule(*v,**kw) for k,v in extra.items() if k.startswith('dense') and not k.startswith('dense21')}
    dense['all_delta_levels']=global_pulse.schedule(old,new,**kw)
    scene=category(pairs,**kw)
    plans=[global_pulse.schedule(*ab,**kw) for ab in pairs.values()]
    budget=min(v['row_write_budget_30s'] for v in plans if v['seconds'])
    return dict(n=n,pitch_mm=406.4/n,stroke_mm=stroke,height_quantum_mm=quantum,neutral_mm=neutral,
        full_row_scan=full_row_scan,row_write_seconds=row_write,row_write_four_strokes_seconds=global_pulse.row_write_cycle(row_write),
        inventory=dict(data_actuators=2*n,row_decoders=2,platen_drives=2,resident_selection_memories=n*n,
            resident_lifting_dogs=n*n,resident_ground_pawls=n*n),
        scenes=scene,cold_start=category(initial,**kw),neutral_preparation=prep,first_from_neutral=first,
        neutral_then_first=dict(seconds=prep['seconds']+first['seconds'],worst_case=first['worst_case'],ledger=combine_ledger(prep,first)),
        sustained=sustained,local_reveals=category(local,**kw),dense_stresses=dense,
        maximum_row_write_seconds_for_all_scenes_current_plans=budget,
        required_row_write_stage_budget_seconds=budget/4)

def checks():
    baseline=reference.checks()
    cases=0
    for quantum in (2,5):
        for old,new in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
            result=global_pulse.bank_schedule([[quantum*(b-a) for a,b in zip(old,new)]],quantum=quantum)
            assert all(v>=0 for v in result[0].values());cases+=1
    for total in (.05,.08,.12):
        assert math.isclose(sum(global_pulse.row_write_cycle(total).values()),total)
    assert math.isclose(reference.move(6.35,400,4000)*7,.5578082107678234)
    assert math.isclose(2*reference.move(80,80,800),2.2)
    for bad in (0,-1,float('inf')):
        try:global_pulse.row_write_cycle(bad)
        except ValueError:pass
        else:raise AssertionError('invalid cycle time accepted')
    return dict(reference=baseline,signed_two_output_pulse_replays=cases,
        row_write_four_strokes='sum equals total; invalid inputs rejected',
        writer_index_and_80mm_clearance_anchors='passed')

def comparator_cases():
    _,pairs,_,_,_=workloads.suites(64,50)
    _,pairs40,_,_,_=workloads.suites(64,40)
    des={}
    for banks,rewind in ((4,False),(4,True),(8,False)):
        des[f'B{banks}_'+('strip' if rewind else 'loop')]=category(pairs,reference.des.schedule,banks=banks,rpm=850,lead=3,rewind=rewind)
    direct={f'B{b}':category(pairs,reference.row_writer,banks=b,v=80,mode='independent') for b in (2,4)}
    pulse={f'B{b}':category(pairs40,workloads.comb.schedule,banks=b,quantum=5,write=.2,event=.08,event_count=5,microtravel=.3) for b in (8,16)}
    retire={f'B8_W{w}':category(pairs40,retirement.schedule,banks=8,writers=w,dirty_only=True) for w in (8,16,32)}
    target={f'program2s_undock{z}mm':category(pairs40,pipeline.schedule,program=2,undock=z) for z in (0,80)}
    return dict(des007_reproduction=des,independent_row_heads=direct,pulsed_scanning_heads_optimistic_mask=pulse,
        stopped_retirement_scanning_heads=retire,double_buffer_target_register=target)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=dict(evidence='Conditional event and kinematic calculations. No complete hardware performance or mechanical qualification.',
        assumptions=dict(platen_speed_mm_s=80,platen_acceleration_mm_s2=800,support_strokes_and_check_per_pulse=5,
            seconds_per_support_stroke_or_check=.08,unload_mm=.3,seat_mm=.3,microtravel_speed_mm_s=20,
            common_seconds=4,retry='TIME RESERVE ONLY: duration of one complete bank mask and maximum pulse per bank; not qualified recovery when OLD memory state is unknown',
            selection='stationary addressed row; old data, row up, new data, row down; equal assumed timing quarters',
            unresolved=['mechanical AND selection','resident memory fidelity','whole-platen load/stiffness','support handoff geometry','actual actuator cycle times','playable wall geometry','safe recovery after unknown OLD memory state']),
        checks=checks(),selected_cases={})
    for n,stroke,row_write in itertools.product((64,80),(40,50),(.08,.12)):
        result['selected_cases'][f'N{n}_stroke{stroke}_q5_row{int(row_write*1000)}ms']=selected_case(n,stroke,row_write)
    result['fine_height_sensitivity']={f'N64_stroke{stroke}_q2_row80ms':selected_case(64,stroke,.08,quantum=2) for stroke in (40,50)}
    result['row_decoder_full_scan_sensitivity']={}
    for n,stroke,row_write in itertools.product((64,80),(40,50),(.08,.12)):
        _,pairs,_,_,_=workloads.suites(n,stroke)
        result['row_decoder_full_scan_sensitivity'][f'N{n}_stroke{stroke}_row{int(row_write*1000)}ms']=category(
            pairs,banks=2,quantum=5,row_write=row_write,full_row_scan=True)
    result['full_scan_category_ledgers']={
        f'N{n}_stroke{stroke}_q5_row80ms':selected_case(n,stroke,.08,full_row_scan=True)
        for n,stroke in itertools.product((64,80),(40,50))}
    result['decision_comparators']=comparator_cases()
    # Regression anchors reproduce previously reported independent calculations.
    anchors={'N64_stroke40_q5_row80ms':20.817298334620747,'N64_stroke50_q5_row80ms':22.90729833462074}
    for key,expected in anchors.items():
        assert math.isclose(result['selected_cases'][key]['scenes']['seconds'],expected,abs_tol=1e-9),(key,result['selected_cases'][key]['scenes']['seconds'])
    def validate_ledgers(value):
        if isinstance(value,dict):
            if 'seconds' in value and 'ledger' in value:
                assert math.isclose(sum(value['ledger'].values()),value['seconds'],abs_tol=1e-8), value
            for child in value.values():validate_ledgers(child)
        elif isinstance(value,list):
            for child in value:validate_ledgers(child)
    validate_ledgers(result)
    result['checks']['all_reported_category_ledgers']='sum to reported duration'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'Wrote {args.output}: 8 dirty-row cases, 4 full-scan category cases, 2 fine-height sensitivities, failed-screen comparators and checks.')
    for key,value in result['selected_cases'].items():
        print(f"{key}: worst scene {value['scenes']['seconds']:.2f} s; conditional row-write budget {1000*value['maximum_row_write_seconds_for_all_scenes_current_plans']:.1f} ms")
    for key,value in result['full_scan_category_ledgers'].items():
        print(f"Full scan {key}: scene {value['scenes']['seconds']:.2f} s; neutral then first {value['neutral_then_first']['seconds']:.2f} s; all-level dense stress {value['dense_stresses']['all_delta_levels']['seconds']:.2f} s")
    print('Retry durations are time reserves only; recovery from unknown OLD memory is unqualified.')
if __name__=='__main__':main()
