"""E-089: deterministic support-state synthesis; NOT a contact/hardware model.
Coordinates are level indices; reporting scales 0..H-1 to 40 mm. Command
notch screening is a separate one-dimensional, bounded-error model in mm.
"""
import argparse
import itertools
import json
from collections import Counter


def replay(old, target, family='displacement', fault=None, trace=False, return_policy='global_inhibit'):
    assert len(old) == len(target) and all(len(a) == len(b) for a,b in zip(old,target))
    sites = [(r,c) for r,row in enumerate(old) for c in range(len(row))]
    initial = {x:old[x[0]][x[1]] for x in sites}
    goal = {x:target[x[0]][x[1]] for x in sites}
    changed = {x for x in sites if initial[x] != goal[x]}
    height = initial.copy()
    stop = initial.copy()
    ground = set(sites)
    grips = {}
    armed = set()
    done = set()  # proof bookkeeping; physical latch only in local_done variant
    word = {x:0 for x in sites}
    e = 0
    paths = [0]
    history = []
    counts = Counter()
    written = []

    def check(event):
        counts[event] += 1
        assert all(x in ground or x in grips for x in sites), 'unsupported cell'
        assert all(height[x] == e+d for x,d in grips.items()), 'rigid offset changed'
        assert all(height[x] == stop[x] for x in ground), 'ground support not seated'
        assert all(height[x] >= 0 for x in sites), 'below zero'
        assert all(height[x] == initial[x] and x in ground and x not in grips
                   for x in sites if x not in changed), 'unchanged region moved'
        if family == 'displacement':
            assert all(min(initial[x],goal[x]) <= height[x] <= max(initial[x],goal[x])
                       for x in sites), 'overshoot'
        if trace:
            history.append(dict(event=event,e=e,height=[height[x] for x in sites],
                ground=sorted(ground),grip=sorted(grips),armed=sorted(armed),verified_done=sorted(done)))

    def write(values, event):
        dirty = {x[0] for x in sites if word[x] != values[x]}
        written.append(dict(event=event,rows=sorted(dirty)))
        word.update(values)
        check(event)

    def acquire(group):
        if not group:return
        assert all(x in ground and x not in grips for x in group)
        for x in group:grips[x] = height[x]-e
        check('grip_proof')
        counts['grip_observations'] += len(group)
        ground.difference_update(group)
        check('ground_release')

    def deposit(group):
        if not group:return
        assert all(x in grips for x in group), 'trip without grip'
        if fault != 'missing_ground':
            for x in group:
                if family == 'stepped_deck':assert height[x] == stop[x], 'wrong rotor support'
                else:stop[x] = height[x]
            ground.update(group)
        check('ground_proof')
        counts['ground_observations'] += len(group)
        for x in group:del grips[x]
        if fault != 'missing_done':done.update(group)
        check('grip_release')

    def move(z):
        nonlocal e
        if z == e:return
        assert not ground.intersection(grips), 'moving with two rigid supports'
        e = z; paths.append(z)
        for x,d in grips.items():height[x]=e+d
        check('move')

    check('initial')
    if changed:
        if family == 'displacement':
            # Physical hypothesis: a retained notch at signed coordinate q and
            # reader coupled to e. Sign cam selects one side of neutral; done
            # latch OR global RETURN cam inhibits empty-return trips. Abstract trip,
            # not an ideal comparator being credited as a completed mechanism.
            write({x:goal[x]-initial[x] for x in sites},'program_displacement')
            if fault == 'stale_command':
                x=next(x for x in sites if x not in changed);word[x]=1
            armed={x for x in sites if word[x] != 0}
            eligible=lambda x:return_policy != 'local_done' or x not in done
            for sign in (-1,1):
                group={x for x in armed if sign*word[x]>0 and eligible(x)}
                acquire(group)
                for q in sorted({word[x] for x in group},key=abs):
                    move(q)
                    hit={x for x in armed if word[x]==e and eligible(x)}
                    deposit(hit)
                # Crossings are logical checkpoints, not required return dwells.
                # No local done latch is needed when a common RETURN phase
                # positively inhibits probes and output cams.
                check('return_inhibit')
                for q in sorted({word[x] for x in group},key=abs,reverse=True):
                    move(q)
                    hit={x for x in armed if word[x]==e and eligible(x)} if (return_policy == 'local_done' or fault == 'missing_return_inhibit') else set()
                    deposit(hit)
                move(0)
            assert done == changed, 'unfinished command'
            write({x:0 for x in sites},'exact_clear')
            armed.clear();done.clear();check('reset_done')
        elif family == 'stepped_deck':
            # Arm retractable pickup hooks while columns rest on their old stops.
            # Pick up at each old height; all acquired hooks share zero offset.
            write({x:int(x in changed) for x in sites},'program_hooks')
            armed=set(changed)
            for h in sorted({initial[x] for x in changed}):
                move(h);acquire({x for x in changed if initial[x]==h})
            # One level of positive clearance, rescaled in physical accounting.
            # Rotate only after every selected old stop is unloaded.
            top=max(max(initial[x],goal[x]) for x in changed)+1
            move(top)
            assert all(height[x] > stop[x] for x in changed)
            counts['rotor_row_programs']=len({r for r,c in changed})
            for x in changed:stop[x]=goal[x]
            check('program_unloaded_rotors')
            for h in sorted({goal[x] for x in changed},reverse=True):
                move(h);deposit({x for x in changed if goal[x]==h})
            move(0)
            assert done == changed
            write({x:0 for x in sites},'exact_clear_hooks')
            armed.clear();done.clear();check('reset_done')
        elif family == 'direct_writer':
            # One independent coordinate per active head. Replay a single site at
            # a time here; reporting credits row concurrency only conditionally.
            for x in sorted(changed):
                move(initial[x]);acquire({x});move(goal[x]);deposit({x});move(0)
            counts['direct_row_visits']=len({r for r,c in changed})
            done.clear()
        else:raise ValueError(family)
    assert not grips and not armed and not done and not any(word.values())
    assert ground == set(sites) and height == goal
    return dict(family=family,return_policy=return_policy,changed=len(changed),counts=dict(counts),
                memory_row_transactions=sum(len(w['rows']) for w in written),
                row_programs=written,path=paths,travel=sum(abs(a-b) for a,b in zip(paths,paths[1:])),
                support_observations=counts['grip_observations']+counts['ground_observations'],
                trace=history if trace else None)


def workload(levels, kind, n=80):
    pairs=[(h,0) for h in range(1,levels)]+[(0,h) for h in range(1,levels)]
    if kind=='cyclic':pairs=[((h+1)%levels,h) for h in range(levels)]
    if kind=='uniform':pairs=[(0,levels-1)]
    old=[[pairs[c%len(pairs)][0] for c in range(n)] for _ in range(n)]
    new=[[pairs[c%len(pairs)][1] for c in range(n)] for _ in range(n)]
    if kind in ('local','unchanged'):
        old=[[0]*n for _ in range(n)];new=[[0]*n for _ in range(n)]
        if kind=='local':
            for r in range(5):
                for c in range(5):new[r][c]=1+c%(levels-1)
    return old,new


def synthesize_coordinates():
    """Enumerate linear memories against two physically different references.
    Fix unit reader gain to remove arbitrary scaling/sign duplicates. Every
    rejected encoding retains a concrete old/target counterexample.
    """
    candidates=[]
    for reader,(c,d) in (('elevator',(0,1)),('column_tail',(1,1))):
        for a,b in itertools.product((-1,0,1),repeat=2):
            witness=next(((old,target) for old,target in itertools.product(range(3),repeat=2)
                          if a*old+b*target != c*old+d*(target-old)),None)
            candidates.append(dict(reader=reader,memory_coefficients=[a,b],
                passes_coordinate_identity=witness is None,rejection_witness=witness,
                family='retained_coordinate_trip'))
    return candidates


def notch_screen(levels, scale, common, spatial, local):
    """Full insertion of a .4-mm rectangular reader into ONE translated slot.
    No periodic-land constraint: there is one slot, not a repeated aperture comb.
    Error bounds add coherently, never RSS. They are hypotheses, not measured
    distributions. Half-window p/2 balances target/adjacent-state margins.
    """
    pitch=40*scale/(levels-1)
    error=common+spatial+local
    reader=.4;half=pitch/2
    return dict(levels=levels,scale=scale,signed_travel_mm=80*scale,
        pitch_mm=pitch,error_mm=error,half_window_mm=half,slot_width_mm=reader+2*half,
        intended_capture_margin_mm=half-error,
        neighbor_rejection_margin_mm=pitch-error-half,
        feasible_1d=half>=error and pitch-error>half,
        note='One translated slot only; no memory detent, guide, latch, force or 3D proof')


def checks():
    total=0
    for old,new in itertools.product(itertools.product(range(3),repeat=3),repeat=2):
        delta=[b-a for a,b in zip(old,new)]
        for family in ('displacement','stepped_deck','direct_writer'):
            out=replay([old],[new],family)
            assert out['support_observations']==2*sum(a!=b for a,b in zip(old,new))
            if family=='displacement':
                assert out['travel']==2*(max(delta+[0])-min(delta+[0]))
                assert out['memory_row_transactions']==(2 if any(delta) else 0)
            if family=='stepped_deck' and any(delta):
                top=max(max(a,b) for a,b in zip(old,new) if a!=b)+1
                assert out['travel']==2*top
        retained=replay([old],[new],return_policy='local_done')
        assert retained['travel']==2*(max(delta+[0])-min(delta+[0]))
        total+=1
    failures={}
    for fault in ('missing_ground','missing_done','stale_command','missing_return_inhibit'):
        try:replay([[2,0,1]],[[0,2,1]],fault=fault,return_policy='local_done' if fault=='missing_done' else 'global_inhibit')
        except AssertionError as ex:failures[fault]=str(ex)
        else:raise AssertionError('fault not detected')
    # Independent kinematic obstruction for comparing absolute target with e.
    old,target=2,1
    naive_e=target
    assert old+naive_e!=target
    # Reader full containment checked by endpoints, not matching integer labels.
    for H in (5,9,21):
        for scale in (.25,.5,1.):
            for common,spatial,local in ((.05,.025,.025),(.10,.05,.05),(.20,.10,.10)):
                n=notch_screen(H,scale,common,spatial,local)
                half=n['half_window_mm']; E=n['error_mm'];p=n['pitch_mm']
                w=.4+2*half
                for error in (-E,E):
                    inside=(-w/2 <= error-.2 and error+.2 <= w/2)
                    if n['feasible_1d']:assert inside
                    neighbor_inside=(-w/2 <= p+error-.2 and p+error+.2 <= w/2)
                    if n['feasible_1d']:assert not neighbor_inside
    return dict(exhaustive_three_cell_maps=total,controller_replays=4*total,
                fault_witnesses=failures,absolute_target_elevator_counterexample=dict(old=old,target=target,result=old+naive_e))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--trace',action='store_true');args=parser.parse_args()
    out={'checks':checks(),'coordinate_synthesis':synthesize_coordinates()}
    assert sum(c['passes_coordinate_identity'] for c in out['coordinate_synthesis']) == 2
    if args.trace:
        out['mixed_trace']=replay([[2,0,1]],[[0,2,1]],trace=True)
    else:
        cases=[]
        for H,kind in itertools.product((5,9,21),('cyclic','all_deltas','uniform','local','unchanged')):
            old,new=workload(H,kind)
            row={'levels':H,'workload':kind,'binary_adverse_row_transactions':80*(2*H+1) if kind=='all_deltas' else None}
            for family in ('displacement','stepped_deck'):
                result=replay(old,new,family)
                # Drop reproducible verbose traces/paths. Deck's top guard is one
                # level here, an explicit clearance hypothesis rather than zero.
                row[family]={k:result[k] for k in ('changed','memory_row_transactions','support_observations')}
                row[family]['rotor_row_programs']=result['counts'].get('rotor_row_programs',0)
                row[family]['travel_mm']=result['travel']*40/(H-1)
                row[family]['decoded_deposit_groups']=result['counts'].get('ground_proof',0)
            row['direct_writer_row_visits']=len({r for r in range(80) if old[r]!=new[r]})
            cases.append(row)
        out['workloads']=cases
        out['notch_scenarios']=[notch_screen(H,s,*errors) for H,s,errors in itertools.product(
            (5,9,21),(.25,.5,1.),((.05,.025,.025),(.10,.05,.05),(.20,.10,.10)))]
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
