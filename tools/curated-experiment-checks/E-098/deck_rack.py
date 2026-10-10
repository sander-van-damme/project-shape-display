"""E-098. Rigid finite contact sections and serialized group-writer ledger.
mm, s; deterministic bounds, not process priors. Ideal guides/retainers and
writer access are explicit grants. No force, sensor or hardware qualification.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('budget', Path(__file__).resolve().parents[1]/'E-094/system_budget.py')
budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget)
move = budget.move


def overlap(a,b):
    return max(0.,min(a[1],b[1])-max(a[0],b[0]))


def volume(a,b):
    return math.prod(overlap(x,y) for x,y in zip(a,b))


def prism(x,y,z): return (x,y,z)


def horizontal(e):
    """Finite bounds on active/retracted pad and dog. Same X cross-section,
    different Y lanes. Edge bounds independent; datums may be bank-coherent.
    """
    out=[]
    for c,p,n in it.product(sorted({-e,e}),repeat=3):
        for ce,le,re,be,ne in it.product((-.1,.1),repeat=5):
            lip=(c-.1,2.5+c+ce)
            active=(1.85+p+le,2.85+p+re)
            idle=(3.15+p+le,4.15+p+re)
            body=(-.1+c,1.2+c+be)
            neighbor=(5.08+n+ne,6.28+n+.1)
            out.append(dict(capture=overlap(lip,active),body_gap=active[0]-body[1],
                inactive_gap=idle[0]-lip[1],neighbor_gap=neighbor[0]-idle[1]))
    return dict(e_mm=e,corners=len(out),minima_mm={k:min(x[k] for x in out) for k in out[0]})


def generated_sections():
    """One translational topology; synthesize contiguous intervals with reserves.
    Body widths, member widths and datum bounds are explicit search dimensions.
    This inexpensive packing test does not generate guides or retention.
    """
    rows=[]
    for body,width,e in it.product((1.2,1.6,2.),(.8,1.,1.2),(.1,.2,.3)):
        required=2*e+.2+.05
        left=body+required
        lip=left+required
        off=lip+required
        envelope=off+width+required
        # minimum pad width after two adverse edge shifts must cover reserve
        rows.append(dict(body=body,width=width,e=e,envelope=envelope,
            survives=envelope<=5.08 and width-.2>=.05))
    return rows


PICKUP_Y=(0.,1.4)
RACK_Y=(2.2,3.6)
# Adverse retained capture .05 mm with broad moving members; X/Y separation
# bounds checked independently. This is a contact-section replay, not assembly.
LIP_X=(-.2,2.2)
PAD_X=(2.15,3.15)
OFF_X=(3.45,4.45)
BODY_X=(-.2,1.1)


def scene(z,deck,delta,errors,dog_top,engaged,selected):
    lip=prism(LIP_X,PICKUP_Y,(z+delta,z+delta+1.0))
    pad=prism(PAD_X if selected else OFF_X,PICKUP_Y,(deck-1.,deck))
    dog=prism(PAD_X if engaged else OFF_X,RACK_Y,(dog_top-1.,dog_top))
    teeth=[prism(LIP_X,RACK_Y,(z-5*j+err,z-5*j+err+1.3)) for j,err in enumerate(errors)]
    spine=prism(BODY_X,(0.,3.6),(z-41,z+60))
    # Nominal 4.4-mm square top; envelope includes +/- .2 datum and .1 edges.
    cap=prism((-.3,4.7),(-.3,4.7),(z+59.9,z+61.1))
    assert volume(lip,pad)<1e-10
    assert volume(spine,pad)==volume(spine,dog)==0
    assert volume(pad,dog)==volume(lip,dog)==0
    assert volume(cap,pad)==volume(cap,dog)==0
    assert all(volume(t,dog)<1e-10 and volume(t,pad)==0 for t in teeth)
    on_pad=selected and math.isclose(z+delta,deck,abs_tol=1e-9)
    on_dog=engaged and any(math.isclose(t[2][0],dog_top,abs_tol=1e-9) for t in teeth)
    assert on_pad or on_dog
    return 1


def samples(a,b,breaks,n):
    return sorted({a,b,*[a+(b-a)*i/n for i in range(n+1)],
        *[q for q in breaks if min(a,b)<=q<=max(a,b)]},reverse=b<a)


def transition(old,new,delta,errors,dog_top,n=4):
    old_z=5*old+dog_top-errors[old]
    new_z=5*new+dog_top-errors[new]
    release=5*old+2.
    insert=5*new+2.
    count=0
    # Home setting changes only X, while the lowest lip is well above the pad.
    for z in (old_z,new_z):
        for i in range(n+1):
            shift=1.3*i/n
            pad=prism((PAD_X[0]+shift,PAD_X[1]+shift),PICKUP_Y,(-3.,-2.))
            assert volume(pad,prism(LIP_X,PICKUP_Y,(z+delta,z+delta+1.)))==0
            assert volume(pad,prism(BODY_X,(0.,3.6),(z-41,z+60)))==0
    # Acquire, prove lifted at old+2, then withdraw the old dog unloaded.
    for d in samples(-2.,release,(old_z+delta,),n):
        z=max(old_z,d-delta)
        count+=scene(z,d,delta,errors,dog_top,True,True)
    for i in range(n+1):
        x=1.3*i/n
        dog=prism((PAD_X[0]+x,PAD_X[1]+x),RACK_Y,(dog_top-1.,dog_top))
        assert all(volume(dog,prism(LIP_X,RACK_Y,(z-5*j+err,z-5*j+err+1.3)))<1e-10 for j,err in enumerate(errors))
    for d in samples(release,45.,(),n)+samples(45.,insert,(),n):
        count+=scene(d-delta,d,delta,errors,dog_top,False,True)
    # Target dog enters below the lifted target tooth. Entire translation is
    # between teeth, so endpoint Z separation proves its continuous X sweep.
    z=insert-delta
    for i in range(n+1):
        x=1.3*i/n
        dog=prism((PAD_X[0]+x,PAD_X[1]+x),RACK_Y,(dog_top-1.,dog_top))
        assert all(volume(dog,prism(LIP_X,RACK_Y,(z-5*j+err,z-5*j+err+1.3)))<1e-10 for j,err in enumerate(errors))
    for d in samples(insert,-2.,(new_z+delta,5*new),n):
        count+=scene(max(new_z,d-delta),d,delta,errors,dog_top,True,True)
    assert 5*new < new_z+delta # proof waypoint below every lip seating contact
    # Unchanged cell, including nine neighbor heights in a separate enumeration.
    return count


def geometry():
    hs=[horizontal(e) for e in (0.,.1,.2,.3)]
    for h in hs:
        e=h['e_mm'];m=h['minima_mm']
        for k in ('capture','body_gap','inactive_gap'):
            assert math.isclose(m[k],max(0.,.45-2*e) if k=='capture' else .45-2*e,abs_tol=1e-10)
        assert math.isclose(m['neighbor_gap'],.73-2*e,abs_tol=1e-10)
    assert min(hs[2]['minima_mm'].values())>=.05-1e-10
    assert hs[3]['minima_mm']['inactive_gap']<0
    # One retained dog datum is common to both endpoints and cancels in travel.
    spans=[(40+g-e8)-(g-e0) for g,e0,e8 in it.product((-.2,.2),repeat=3)]
    assert math.isclose(min(spans),39.6)
    # Independent interval packing equation for this translation topology.
    generated=generated_sections()
    assert sum(r['survives'] for r in generated)>0
    assert all(math.isclose(r['envelope'],r['body']+r['width']+4*(2*r['e']+.25)) for r in generated)
    patterns=[[-.2]*9,[.2]*9,[(-1)**j*.2 for j in range(9)],[(-1)**(j+1)*.2 for j in range(9)]]
    cases=states=0
    for old,new,delta,dg,errs in it.product(range(9),range(9),(.8,1.2),(-.2,.2),patterns):
        states+=transition(old,new,delta,errs,dg);cases+=1
    # All 512 tooth-error sign patterns at every release/insertion state check
    # tooth-to-dog corners omitted by the cheaper full-route patterns.
    corner_states=0
    for errs,level,delta,dg in it.product(it.product((-.2,.2),repeat=9),range(9),(.8,1.2),(-.2,.2)):
        d=5*level+2
        scene(d-delta,d,delta,errs,dg,True,True);corner_states+=1
    idle_states=0
    for level,delta,dg,errs in it.product(range(9),(.8,1.2),(-.2,.2),patterns):
        z=5*level+dg-errs[level]
        for d in samples(-2,45,(),32):
            scene(z,d,delta,errs,dg,True,False);idle_states+=1
    holdouts=[transition(a,b,d,patterns[i],g,n) for a,b in ((0,8),(8,0),(4,1))
              for d,g,i,n in it.product((.8,1.2),(-.2,.2),(0,3),(1,16,64))]
    # Failure to release: next lower tooth hits underside of grounded dog.
    dog=prism((1.85,2.85),RACK_Y,(-.9,0.))
    tooth=prism((0,2.5),RACK_Y,(-1.,.2))
    # old tooth0 at z=0; next lower tooth1 at z-5. z=4 -> [-1,.2].
    collision=volume(dog,tooth)
    assert math.isclose(collision,.819)
    # Missed clear lifts an unchanged column despite its engaged ground dog,
    # then jams the next tooth; the first fault motion is already unacceptable.
    failed_clear_lift=2.-1.
    assert failed_clear_lift==1.
    # A missing target dog leaves selected column deck-supported on return;
    # clearing the pad then leaves no grounded contact. Do not call this safe.
    return dict(horizontal=hs,section_search=generated,route_cases=cases,
        route_states=states,all_tooth_corner_states=corner_states,idle_states=idle_states,
        refined_holdouts=len(holdouts),failed_release_collision_mm3=collision,
        y_lane_clearance_bound_mm=.8-2*.2-.2,vertical_insertion_gap_min_mm=.4,
        surface_cap_gap_bound_mm=5.08-4.4-2*.2-.2,
        lower_tooth_clearance_min_mm=5-1.3-1.-1.-.6,
        maximum_seat_error_mm=.4,failed_clear_lift_mm=failed_clear_lift,
        minimum_endpoint_span_mm=min(spans),
        settled_axial_envelope_mm=41+40+61,
        nominal_swept_axial_envelope_mm=41+(45-1)+61,
        bounded_swept_axial_envelope_mm=41+.4+(45-.8)+61.1)


def workload(kind,start=0):
    if kind=='full':
        # Cycle all 72 nonidentity pairs into 80 cells per row; every old and
        # every target is present. Repeated pairs do not change group counts.
        pairs=[(a,b) for a,b in it.product(range(9),repeat=2) if a!=b]
        return [[pairs[c%72][0] for c in range(80)] for _ in range(80)], [[pairs[c%72][1] for c in range(80)] for _ in range(80)]
    old=[[0]*80 for _ in range(80)];new=[[0]*80 for _ in range(80)]
    if kind=='local':
        for r in range(start,start+5):
            for c in range(5):new[r][c]=c+1
    return old,new


def ledger(old,new,banks,v=200.,a=5000.,hook=.1,dog=.1,proof=.1,overhead=2.,retries=1):
    """Bank-independent, serial row writer; all banks simultaneous. Program
    selection at home, then release by old groups, insert by target groups,
    then clear at home. Serpentine station visits, exact final home return.
    No overlap of deck motion/setting/readback; no free mask or hidden visits.
    One shared writer is a FAVORABLE GRANT across deck-home and ground planes.
    """
    n=80//banks;reports=[]
    for b in range(banks):
        rows=list(range(b*n,(b+1)*n))
        changed={r:[(x,y) for x,y in zip(old[r],new[r]) if x!=y] for r in rows}
        active=[r for r in rows if changed[r]]
        if not active:reports.append(dict(seconds=0.,dog_visits=0,hook_visits=0,writer_motion_s=0.,deck_motion_s=0.,groups=0));continue
        olds=sorted({x for r in active for x,y in changed[r]})
        targets=sorted({y for r in active for x,y in changed[r]},reverse=True)
        visits=[active]+[[r for r in active if any(x==h for x,y in changed[r])] for h in olds]+[[r for r in active if any(y==h for x,y in changed[r])] for h in targets]+[active]
        pos=0;travel=0.
        for index,rr in enumerate(visits):
            for r in sorted(rr,reverse=bool(index%2)):
                p=r-b*n
                travel+=move((p-pos)*5.08,v,a);pos=p
        travel+=move(pos*5.08,v,a)
        # Lift .4 mm or more before release at old+2. Insert at target+2;
        # seat/prove at target+0 before moving to the next target group.
        path=[-2.]+[5*h+2. for h in olds]+[45.]
        for h in targets:path.extend((5*h+2.,5*h))
        path.append(-2.)
        dm=sum(move(y-x,v,a) for x,y in zip(path,path[1:]))
        dv=sum(map(len,visits[1:-1]));hv=2*len(active);groups=len(olds)+len(targets)
        recovery=retries*(dog+proof+2*move(2.2,v,a))
        base=overhead+travel+dm+hv*hook+groups*proof+recovery
        reports.append(dict(seconds=base+dv*dog,dog_visits=dv,hook_visits=hv,
            writer_motion_s=travel,deck_motion_s=dm,deck_mm=sum(abs(y-x) for x,y in zip(path,path[1:])),
            groups=groups,dog_ceiling_s=(30-overhead-travel-dm-hv*hook-groups*proof-retries*(proof+2*move(2.2,v,a)))/(dv+retries)))
    worst=max(reports,key=lambda x:x['seconds'])
    return dict(banks=banks,**worst,channels_shared=82*banks,
        channel_ceiling_usd=250/(82*banks),channels_separate=163*banks,
        separate_channel_ceiling_usd=250/(163*banks))


def checks():
    old,new=workload('full')
    rows=[]
    for b in (1,2,4,8,16):
        r=ledger(old,new,b);n=80//b
        assert r['dog_visits']==18*n and r['hook_visits']==2*n
        assert math.isclose(r['writer_motion_s'],20*(n-1)*move(5.08))
        # Independent stopped deck-leg sum for the full nine-group workload.
        dm=move(4)+8*move(5)+move(3)+move(3)+9*move(2)+8*move(3)+move(2)
        assert math.isclose(r['deck_motion_s'],dm)
        assert r['deck_mm']==94
        cap=r['dog_ceiling_s']
        assert math.isclose(ledger(old,new,b,dog=cap)['seconds'],30)
        assert ledger(old,new,b,dog=cap+1e-6)['seconds']>30
        assert ledger(old,new,b,dog=cap-1e-6)['seconds']<30
        direct=budget.evaluate(budget.ledger('full',b))['direct']
        rows.append(dict(rack=r,direct_seconds=direct['seconds']))
    assert ledger(*workload('none'),4)['seconds']==0
    local=[]
    for b in (1,2,4,8,16):
        rr=[ledger(*workload('local',s),b) for s in range(76)]
        local.append(dict(banks=b,seconds=[min(r['seconds'] for r in rr),max(r['seconds'] for r in rr)]))
    sensitivity=[]
    for (v,a),slot in it.product(((80,1000),(200,5000),(400,20000)),(.02,.05,.1,.2,.5)):
        rr=[ledger(old,new,b,v=v,a=a,dog=slot) for b in (1,2,4,8,16)]
        sensitivity.append(dict(v=v,a=a,dog_slot_s=slot,min_tested_banks=next((r['banks'] for r in rr if r['seconds']<30),None)))
    return dict(full=rows,local=local,sensitivity=sensitivity)


if __name__=='__main__':
    print(json.dumps(dict(geometry=geometry(),system=checks()),indent=2))
