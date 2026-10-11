"""E-175 bounded selectors: mm, N, s, MPa; no physical qualification.
V-seat sections and static reactions, finite stacked-stop contact, schedules.
"""
import itertools as it
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-173'))
import lanes
c = lanes.control
mv = c.r.move
P = 10.1


def key_section(q0, left, right):
    # Each flank's normal error is converted to a vertical plane offset.
    # Male triangular section vertices (q,z),(q-.3,z+.3),(q+.3,z+.3).
    # Female opening slopes +/-1, mouth half-width .4, depth .4.
    a, b = math.sqrt(2)*left, math.sqrt(2)*right
    q, z = q0+(a-b)/2, (a+b)/2
    vertices = ((q,z),(q-.3,z+.3),(q+.3,z+.3))
    gaps = [(zz-(yy-q0)-b, zz+(yy-q0)-a) for yy,zz in vertices]
    assert min(v for pair in gaps for v in pair)>-1e-10
    assert abs(gaps[1][1])<1e-10 and abs(gaps[2][0])<1e-10
    return q,z


def keyed():
    out=[]
    # Front and rear sections; extrapolate nose transverse displacement along
    # a straight rigid centerline. This is affine small-attitude analysis,
    # not a generated assembled rotated solid/contact trajectory.
    xf,xr,xn=2.2,3.5,1.2
    factor=1+2*(xf-xn)/(xr-xf)
    for e in (.025,.05,.075,.1):
        losses=[]
        for signs in it.product((-e,e),repeat=4):
            qf,zf=key_section(0,*signs[:2]);qr,zr=key_section(0,*signs[2:])
            qn=qf+(qf-qr)*(xf-xn)/(xr-xf)
            losses.append(qn)
        assert math.isclose(max(losses),math.sqrt(2)*e*factor)
        out.append(dict(e=e,nose_error=max(losses),wrong_gap=.4-4*e-max(losses),
                        section_assemblies=len(losses)))
    # Proposed ground-attached compression-spring roof, spanning all Y states.
    # No spring/link is credited beyond this failed finite packaging attempt.
    roof=lanes.box((3.,4.1),(-2.3,2.3),(-2.5,-2.))
    neighbor_pads=[lanes.box((5.08-2.2,5.08-1.2),(q-.5,q+.5),(-3.,-2.)) for q in (0,1.7)]
    roof_hits=[lanes.volume(roof,pad) for pad in neighbor_pads]
    assert all(math.isclose(x,.44,abs_tol=1e-9) for x in roof_hits)
    forces=[]
    for F,xload,Pkeep in it.product((.1,1,10),(1.2,1.5,1.8),(.15,.8,1.5)):
        front=F*(xr-xload)/(xr-xf)
        rear=Pkeep-F*(xf-xload)/(xr-xf)
        assert abs(front+rear-F-Pkeep)<1e-10
        assert abs(front*xf+rear*xr-F*xload-Pkeep*xr)<1e-10
        forces.append(dict(F=F,xload=xload,keeper=Pkeep,front=front,rear=rear,
                           unilateral=rear>=0))
    # Round-wire steel spring hypothesis: torsion formula, G explicit bounds.
    springs=[]
    for G,d,compression in it.product((60000,80000),(.15,.2),(.2,.4)):
        D=.8;n=6; k=G*d**4/(8*D**3*n);lift=.8
        springs.append(dict(G=G,wire=d,compression=compression,k=k,
                            preload=k*compression,release_force=k*(compression+lift),
                            minimum_installed_length=n*d+lift,
                            nominal_cavity_coil_bind=1.6-lift<n*d,
                            release_work_mJ=k*(compression*lift+lift*lift/2)))
    # Normal-force resolution: under lateral load H, unilateral seat persists
    # only if |H|<=R for 45-degree flanks. Friction not needed for this bound.
    # With H=.1N applied at the same overhanging nose as F=1N, each station
    # must carry its share of both force and moment. One flank then unloads.
    F,H,Pkeep=1.,.1,.8
    Rf=F*(xr-xn)/(xr-xf);Rr=Pkeep-F*(xf-xn)/(xr-xf)
    Hf=H*(xr-xn)/(xr-xf);Hr=-H*(xf-xn)/(xr-xf)
    normals=[(R+sign*hh)/math.sqrt(2) for R,hh in ((Rf,Hf),(Rr,Hr)) for sign in (-1,1)]
    assert min(normals)<0
    return dict(error=out,reactions=forces,springs=springs,roof_collision_mm3=roof_hits,
                lateral_load_witness=dict(front=Rf,rear=Rr,Hfront=Hf,Hrear=Hr,normals=normals),
                retention_reserve_threshold_e=(.4-.05)/(4+math.sqrt(2)*factor),
                zero_gap_threshold_e=.4/(4+math.sqrt(2)*factor))


def stacked_solids(h,states,heights):
    # One broad lip, five independently grounded binary stops. Guides/keepers
    # explicitly outside this finite contact model, not silently qualified.
    spine=lanes.box((-.6,.6),(-2.3,2.3),(h-2,h+50))
    foot=lanes.box((.2,1.8),(-.8,.8),(h,h+1.2))
    dogs=[lanes.box((1.2,3.2) if on else (2.2,4.2),(-.8,.8),(z-1,z))
          for on,z in zip(states,heights)]
    return spine,foot,dogs


def stacked_replay(old,target,errors,sub=1):
    heights=[j*P+e for j,e in enumerate(errors)]
    state=[j==old for j in range(5)]
    h=heights[old];count=0
    def pose(z,carried):
        nonlocal count
        spine,foot,dogs=stacked_solids(z,state,heights)
        assert all(lanes.volume(s,d)<1e-8 for s in (spine,foot) for d in dogs)
        supported=any(on and abs(z-hh)<1e-9 for on,hh in zip(state,heights))
        pickup=lanes.box((-1.8,-.2),(-.5,.5),(z+1,z+1.9))
        deck_z=z+1 if carried else -2
        pad=lanes.box((-2.2,-1.2),(-.5,.5) if carried else (1.2,2.2),(deck_z-1,deck_z))
        assert all(lanes.volume(part,pad)<1e-9 for part in (spine,foot,pickup))
        assert all(lanes.volume(pickup,dog)<1e-9 for dog in dogs)
        pad_contact=(carried and abs(pickup[2][0]-pad[2][1])<1e-9
                     and lanes.overlap(pickup[0],pad[0])*lanes.overlap(pickup[1],pad[1])>0)
        assert supported or pad_contact
        assert all(-2.3<=v<=4.2 for obj in [spine,foot,*dogs] for v in obj[0])
        count+=1
    pose(h,False)
    if old==target:return count
    top=44.4
    for k in range(sub+1):pose(h+(top-h)*k/sub,True)
    # At top all stops lie below the foot; entire 1-mm X sweeps are clear.
    assert top-min(heights)>0 and top-max(heights)-1.2>0
    # Single pass per level clears previous and sets target; when target is
    # lower than old, two active stops coexist briefly, harmless above both.
    for j in range(5):
        state[j]=(j==target)
        pose(top,True)
    for k in range(sub+1):pose(top+(heights[target]-top)*k/sub,True)
    pose(heights[target],False)
    return count


def stack_time(banks,slot=.1,v=200,acc=5000,kind='full',start=0):
    rows=c.workload(kind,start);n=80//banks
    move=lambda d:c.r.move(d,v,acc)
    def bank(rr):
        active=[i for i,row in enumerate(rr) if any(o!=t for o,t in row)]
        if not active:return 0.
        pairs=[(o,t) for row in rr for o,t in row if o!=t]
        # One 80-channel head with row and access-Z axes, plus shared deck.
        # Seven whole scans: pad-on, five stop planes, pad-off.
        # Plane 0 is at access z=0; pad interface is favorable same datum.
        rp=0;zp=0;elapsed=0
        for scan,z in enumerate([0,0,P,2*P,3*P,4*P,0]):
            elapsed+=move(z-zp);zp=z
            for r in sorted(active,reverse=bool(scan%2)):
                elapsed+=move((r-rp)*5.08)+slot;rp=r
        elapsed+=move(rp*5.08)
        d=-2
        for end in [o*P+2 for o in sorted({o for o,t in pairs})]+[4*P+5]+[x for t in sorted({t for o,t in pairs},reverse=True) for x in (t*P+2,t*P)]+[-2]:
            elapsed+=move(end-d);d=end
        # Preparation/registration/settle, pickup and final support proofs,
        # one repeated bit write and one short supported reseat/proof.
        return 2+elapsed+.1*(len({o for o,t in pairs})+len({t for o,t in pairs}))+slot+.1+2*move(2.2)
    return max(bank(rows[i:i+n]) for i in range(0,80,n))


def main():
    key=keyed()
    count=sum(stacked_replay(o,t,e) for o,t in it.product(range(5),repeat=2)
              for e in it.product((-.05,.05),repeat=5))
    refinement=[sum(stacked_replay(o,t,(.013,-.021,.037,-.043,.019),n)
                    for o,t in it.product(range(5),repeat=2)) for n in (1,4,16)]
    # Concrete wrong-state failure: target stop 2 plus stale stop 4.
    states=[False,False,True,False,True]
    heights=[j*P for j in range(5)];bad=max(h for h,s in zip(heights,states) if s)
    _,foot,dogs=stacked_solids(bad-.05,states,heights)
    penetration=lanes.volume(foot,dogs[4]);assert penetration>0
    # Adjoining cell crosses the parked high stop during ordinary ascent.
    _,_,parked=stacked_solids(0,[True,False,False,False,False],heights)
    neighbor_pickup=lanes.box((5.08-1.8,5.08-.2),(-.5,.5),(40.,40.9))
    neighbor_collision=lanes.volume(parked[4],neighbor_pickup)
    assert math.isclose(neighbor_collision,.368,abs_tol=1e-9)
    # Independently hand-count seven row scans and five vertical transfers.
    expected=lanes.evaluate(4)+4*19*mv(5.08)-.4+4*mv(P)+mv(4*P)
    assert math.isclose(expected,stack_time(4))
    assert stack_time(4,kind='none')==0
    times={b:dict(stack=stack_time(b),keyed_lower_bound=lanes.evaluate(b),
                   separate=c.evaluate('separate',b)['seconds'],direct=c.evaluate('direct',b)['seconds'])
           for b in (1,2,4,8,16)}
    screw=[]
    # Square-thread friction cone, using kinetic lower bound for moving arrest.
    # Favorable unloaded support adjustment; self-locking support still needs
    # finite thrust/anti-rotation/drive docking, not included here.
    for mu,d in it.product((.02,.05,.1),(3,12)):
        lead=math.pi*d*mu*.8
        turns=40.4/lead
        screw.append(dict(mu=mu,diameter=d,lead=lead,turns=turns,rpm_at_half_second=120*turns))
    out=dict(key=key,stack=dict(corner_poses=count,refinement=refinement,
             stale_stop=dict(actual=bad,wanted=2*P,penetration=penetration),neighbor_collision_mm3=neighbor_collision),times=times,
             stack_slots={s:{b:stack_time(b,slot=s) for b in (2,4,8)} for s in (.05,.1,.2)},
             stack_motion={str((v,a)):{b:stack_time(b,v=v,acc=a) for b in (2,4,8)}
                           for v,a in ((80,1000),(200,5000),(400,20000))},
             local_stack=[min(ts),max(ts)] if (ts:=[stack_time(4,kind='local',start=s) for s in range(76)]) else [],
             screw=screw)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
