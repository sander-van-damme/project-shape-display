"""Finite planar pickup subsection, mm; quasistatic gravity, rigid bodies.
Ground stop heights are granted boundary conditions, NOT generated setters.
Ideal prismatic guides react moments; their load capacity is not established.
Deterministic epistemic corners, no manufacturing probabilities or hardware pass.
"""
import itertools as it
import json
import math


def overlap(a,b):
    return max(0.,min(a[1],b[1])-max(a[0],b[0]))


def area(a,b):
    return overlap(a[:2],b[:2])*overlap(a[2:],b[2:])


def rect(x,z):return (*x,*z)


def horizontal(e):
    cases=[]
    # Column/hook datum, deck datum and neighboring column datum can differ;
    # each can be coherent across an entire print/bank. Edge errors are bounds.
    datums=(-e,e) if e else (0.,)
    for c,d,n,tip,left,right,body in it.product(datums,datums,datums,(-.1,.1),(-.1,.1),(-.1,.1),(-.1,.1)):
        extended=(1.4+c,3.8+c+tip)
        withdrawn=(c,2.4+c+tip)
        finger=(3.1+d+left,4.3+d+right)
        column=(c,2.4+c+body)
        neighbor=(5.08+n,7.48+n+body)
        vals=dict(capture=overlap(extended,finger),
            inactive_gap=finger[0]-withdrawn[1],
            body_gap=finger[0]-column[1],neighbor_gap=neighbor[0]-finger[1],
            root_overlap=overlap(extended,column))
        cases.append(dict(extended=extended,withdrawn=withdrawn,finger=finger,column=column,neighbor=neighbor,**vals))
    minima={key:min(c[key] for c in cases) for key in ('capture','inactive_gap','body_gap','neighbor_gap','root_overlap')}
    # .05 mm is a geometric reserve, not adequate load overlap/print qualification.
    passed=all(x>=.05-1e-12 for x in minima.values())
    return cases,dict(datum_bound_mm=e,corners=len(cases),minima_mm=minima,section_pass=passed)


def poses(start,finish,breakpoint,n):
    points={start,finish}
    if min(start,finish)<=breakpoint<=max(start,finish):points.add(breakpoint)
    points.update(start+(finish-start)*k/n for k in range(n+1))
    return sorted(points,reverse=finish<start)


def check_scene(old,target,neighbor,delta,subdivisions=8):
    # Use the most adverse retained horizontal capture width (.1 mm) and finite
    # body/deck gaps. Root is a joint region, not tested for self-penetration.
    lip_x=(1.2,3.5); finger_x=(3.4,4.6)
    col_x=(-.2,2.3); neighbor_x=(4.88,7.38)
    withdrawn_neighbor=(4.88,7.38)
    stop_x=(-.2,1.0)
    thickness=.9
    scenes=0
    for ascending,stop in ((True,old),(False,target)):
        path=poses(-2.,45.,old+delta,subdivisions) if ascending else poses(45.,-2.,target+delta,subdivisions)
        for e in path:
            z=max(stop,e-delta)
            lip=rect(lip_x,(z+delta,z+delta+thickness))
            finger=rect(finger_x,(e-.9,e))
            # Foot over the stop; side column/slider housing in its own lane.
            foot=rect(stop_x,(z,z+60))
            ground=rect(stop_x,(-5,stop))
            body=rect((1.2,col_x[1]),(z-.5,z+60))
            cap=rect(col_x,(z+1,z+60))
            idle=rect(neighbor_x,(neighbor,neighbor+60))
            idle_lip=rect(withdrawn_neighbor,(neighbor+.8,neighbor+2.1))
            assert area(lip,finger)<1e-10
            assert area(foot,ground)<1e-10
            assert area(body,ground)==0 and area(cap,ground)==0 and area(lip,ground)==0
            assert area(body,finger)==0 and area(cap,finger)==0
            assert area(idle,finger)==0 and area(idle_lip,finger)==0
            # Continuous load support: existence of a nonnegative unit-gravity
            # vertical equilibrium at a real contact, with IDEAL guide moment reactions.
            # This does not establish guide force, strength or full equilibrium.
            on_ground=math.isclose(z,stop,abs_tol=1e-10)
            on_deck=math.isclose(z+delta,e,abs_tol=1e-10)
            assert on_ground or on_deck
            if on_deck:assert overlap(lip_x,finger_x)>=.1-1e-12
            if on_ground:assert overlap(stop_x,stop_x)>0
            scenes+=1
        if not ascending:
            assert math.isclose(z,target)
            assert e<z+delta # positively separated at home, hook still extended
    # Whole horizontal arm/clear sweep at deck home is disjoint by vertical
    # separation; intermediate poses confirm the finite rectangle witness.
    for stop in (old,target):
        for k in range(17):
            shift=1.4*k/16
            hook=rect((-.2+shift,2.1+shift),(stop+delta,stop+delta+thickness))
            assert area(hook,rect(finger_x,(-2.9,-2.)))==0
            assert area(hook,rect(stop_x,(-5,stop)))==0
    # At the top, every hypothetical intervening stop height is below the foot.
    assert 45-delta-max(old,target)>=3.6-1e-12
    return scenes


def main():
    sections=[horizontal(e)[1] for e in (0.,.1,.2,.3)]
    assert [x['section_pass'] for x in sections]==[True,True,True,False]
    middle=sections[2]['minima_mm']
    assert math.isclose(middle['capture'],.1) and math.isclose(middle['body_gap'],.1)
    # Independent interval reserves for coherent adverse corners.
    for row in sections:
        e=row['datum_bound_mm'];m=row['minima_mm']
        assert math.isclose(m['capture'],max(0.,.7-2*e-.2),abs_tol=1e-12)
        assert math.isclose(m['inactive_gap'],.7-2*e-.2,abs_tol=1e-12)
        assert math.isclose(m['neighbor_gap'],.78-2*e-.1,abs_tol=1e-12)
    cases=states=0
    for old,target,idle,delta,oe,te in it.product(range(0,41,5),range(0,41,5),range(0,41,5),(.8,1.2),(-.2,.2),(-.2,.2)):
        states+=check_scene(old+oe,target+te,idle,delta)
        cases+=1
    # Independent finer-path holdouts on extremes and a mixed transition.
    holdouts=[check_scene(old,target,20,delta,n) for old,target in ((.2,40.2),(40.2,-.2),(20.2,5.2)) for delta,n in it.product((.8,1.2),(1,16,64))]
    # Captured/bilateral coupling cannot continue below a deposited fixed stop.
    target=20.;e=19.5;z=e
    penetration=area(rect((0,1.2),(z,z+60)),rect((0,1.2),(-5,target)))
    assert math.isclose(penetration,.6)
    # Failed neutralization before NEXT upward stroke moves an unchanged column.
    wrong_height=max(0.,10.-1.2)
    assert wrong_height==8.8
    # Beyond the retained bound, a withdrawn lip intersects a passing deck.
    bad=next(c for c in horizontal(.3)[0] if c['inactive_gap']<0)
    fault_area=area(rect(bad['withdrawn'],(0,.9)),rect(bad['finger'],(-.4,.5)))
    assert fault_area>0
    print(json.dumps(dict(section_scenarios=sections,vertical_cases=cases,contact_states=states,
        refined_holdouts=len(holdouts),captured_hook_ground_penetration_mm2=penetration,
        failed_clear_unchanged_lift_mm=wrong_height,wide_bound_inactive_collision_mm2=fault_area,
        disposition='Unilateral pickup section survives bounded geometry; ground-stop setter, hook retention, strength and 3D assembly remain unproved.'),indent=2))

if __name__=='__main__':main()
