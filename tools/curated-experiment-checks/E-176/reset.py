"""E-176: state synthesis, finite reset comb and schedule bounds. mm, N, s.
Standard library, no process distribution or hardware qualification.
"""
import itertools as it
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-173'))
import lanes as lane


def synthesize(clock=False):
    # Deterministic Moore automata. A=arm, L=loaded, U=unloaded, H=home.
    # Idle load exposure is ignored; a false physical arm is outside this contract.
    symbols='ALUH' if clock else 'ALU'
    traces={'':0,'U':0,'L':0,'A':1,'AU':1,'AUU':1,'AL':1,
            'ALL':1,'ALU':0,'ALUU':0,'ALUA':1,'ALUALU':0}
    if clock:
        # Clocked reset need not distinguish load history: clear only at home.
        traces={'':0,'U':0,'L':0,'A':1,'AU':1,'AL':1,'ALU':1,
                'AH':0,'ALUH':0,'ALUHA':1,'H':0,'HH':0}
    reference=((1,0,0,0),(1,1,1,0)) if clock else ((1,0,0),(1,2,1),(2,2,0))
    reference_out=(0,1) if clock else (0,1,1)
    def equivalent(out,tr):
        pending=[(0,0)];seen=set()
        while pending:
            q,r=pending.pop()
            if (q,r) in seen:continue
            seen.add((q,r))
            if out[q]!=reference_out[r]:return False
            pending.extend((tr[q*len(symbols)+j],reference[r][j]) for j in range(len(symbols)))
        return True  # finite product-automaton check covers arbitrary input words
    counts=[];witness=None
    for n in range(1,4):
        count=0
        for tail in it.product((0,1),repeat=n-1):
            out=(0,)+tail
            for tr in it.product(range(n),repeat=n*len(symbols)):
                def run(word):
                    q=0
                    for s in word:q=tr[q*len(symbols)+symbols.index(s)]
                    return out[q]
                if all(run(word)==val for word,val in traces.items()) and equivalent(out,tr):
                    count+=1
                    if witness is None:witness=dict(outputs=out,transition=tr,symbols=symbols)
        counts.append(count)
        if count:break
    return dict(counts=counts,witness=witness)


def shift(box,dx,dy):
    return tuple((a+d,b+d) for (a,b),d in zip(box,(dx,dy,0)))


def comb(face):
    # One repeating tooth, its grounded-at-home post and a longitudinal rail.
    # Separate x rails connect outside the bank; external bridge/guides unbuilt.
    return [lane.box((-2.8,-1.3),(face-.4,face),(-2.8,-2.2)),
            lane.box((-2.8,-2.5),(face-.4,face),(-3.5,-2.2)),
            lane.box((-2.8,-2.5),(-8.,8.),(-4.,-3.5))]


def reset_geometry(subdivisions):
    count=0
    for level,initial in it.product(range(5),(0.,1.7)):
        for phase in range(subdivisions+1):
            face=-.9+2.1*phase/subdivisions
            pad=max(initial,face+.5)
            col,dog,moving=lane.solids(level*lane.P,lane.LANES[level],-2.,pad,(0.,)*5,0.,1.)
            parts=comb(face)
            assert all(lane.volume(a,b)<1e-10 for a in parts for b in col+[dog,moving])
            # An active pad becomes contacted at face=-.5; then unilateral push.
            if face>=initial-.5:
                assert math.isclose(moving[1][0],face,abs_tol=1e-10)
                area=lane.overlap(parts[0][0],moving[0])*lane.overlap(parts[0][2],moving[2])
                assert math.isclose(area,.54)
            # All neighbor heights and both pad states, at home; non-contacting
            # parts of the comb must not collide with other cell solids.
            for dx,dy in it.product((-5.08,0,5.08),repeat=2):
                if dx==dy==0:continue
                for h,p in it.product(range(5),(0.,1.7)):
                    nc,nd,np=lane.solids(h*lane.P,lane.LANES[h],-2.,max(p,face+.5),(0.,)*5,0.,1.)
                    # Rail repeats along Y; it is a shared solid, not separate bodies.
                    assert all(lane.volume(a,shift(b,dx,dy))<1e-10 for a in parts for b in nc+[nd,np])
            count+=1
        assert math.isclose(pad,1.7)
    # Retracted comb while deck moves: x separates posts/rails; y separates teeth.
    for level,pad,d in it.product(range(5),(0.,1.7),(-2.,0.,20.,45.4)):
        h=max(level*lane.P,d-1.) if pad==0 else level*lane.P
        col,dog,moving=lane.solids(h,lane.LANES[level],d,pad,(0.,)*5,0.,1.)
        assert all(lane.volume(a,b)<1e-10 for a in comb(-.9) for b in col+[dog,moving])
    return count


def rigid_mismatch(e):
    # Two resident end stops; keeper captures within .03 of each actual stop.
    # Errors are explicit bounds, not measured. First stop limits rigid travel.
    stops=(1.7-e,1.7+e);face_first=stops[0]-.5
    shortfall=stops[1]-(face_first+.5)
    tooth=comb(stops[1]-.5)[0]
    _,_,early=lane.solids(0,lane.LANES[0],-2.,stops[0],(0.,)*5,0.,1.)
    collision=lane.volume(tooth,early)
    assert math.isclose(shortfall,2*e,abs_tol=1e-9)
    assert math.isclose(collision,.54*2*e,abs_tol=1e-9)
    return dict(e=e,late_shortfall=shortfall,early_penetration_mm3=collision,
                capture_window=.03,both_captured=shortfall<=.03+1e-9)


def schedule(rows,read=.02,reset=.1,word=.5,slot=.1,proof=.1,v=200,acc=5000,audit_all=True):
    active=[i for i,row in enumerate(rows) if any(o!=t for o,t in row)]
    if not active:return 0.
    # Keep all inherited deck motion, preparation, support proofs and retry.
    old=lane.bank_time(rows,word=word,slot=slot,proof=proof,v=v,acc=acc)
    mv=lambda d:lane.control.r.move(d,v,acc)
    # Prior final pass started at smallest active row, ended at largest, home.
    # New mechanism returns from smallest directly home before broadcast reset.
    # Conservative protocol exposes all pads and scans all bank rows.
    old_clear=len(active)*slot+sum(mv((b-a)*5.08) for a,b in zip(active,active[1:]))+mv(max(active)*5.08)
    new=mv(min(active)*5.08)+2*mv(1.75)+reset
    if not audit_all and read is not None:
        # Conditional monotone reset: known-clear unchanged pads cannot arm.
        # Writer withdraws in place, resets, and scans only changed rows.
        # Actual shared writer/reset access remains unbuilt.
        return old+2*mv(1.75)+reset-len(active)*(slot-read)
    if read is not None:
        n=len(rows)
        new+=n*read+(n-1)*mv(5.08)+mv((n-1)*5.08)
    # read=None grants independent parallel pad sensing already in reset slot.
    return old-old_clear+new


def evaluate(banks,kind='full',start=0,**kwargs):
    rows=lane.control.workload(kind,start);n=80//banks
    return max(schedule(rows[i:i+n],**kwargs) for i in range(0,80,n))


def main():
    states=synthesize();clock=synthesize(True)
    assert states['counts'][:2]==[0,0] and states['counts'][2]>0
    assert clock['counts'][0]==0 and clock['counts'][1]>0
    poses=[reset_geometry(n) for n in (1,4,16)]
    # At every scan pose mechanics is affine, with contact at face=-.5.
    # Include this breakpoint explicitly independently of uniform refinement.
    assert lane.volume(comb(-.5)[0],lane.solids(0,lane.LANES[0],-2.,0.,(0.,)*5,0.,1.)[2])==0
    central={b:dict(explicit=lane.evaluate(b),broadcast_scan=evaluate(b),
                    broadcast_parallel=evaluate(b,read=None),
                    direct=lane.control.evaluate('direct',b)['seconds'],
                    channels=83*b,allowance_250=250/(83*b)) for b in (2,4,8,16)}
    # Dense case, same serpentine path: savings must equal n(slot-read),
    # less the added reset stroke/dwell. This is an independent hand sum.
    for b in (2,4,8,16):
        delta=(80//b)*(.1-.02)-.1-2*lane.control.r.move(1.75)
        assert math.isclose(central[b]['explicit']-central[b]['broadcast_scan'],delta)
    assert evaluate(4,'none')==0
    load=[]
    for bank,f,k,e in it.product((4,8),(.01,.1,1.),(.2,1.,5.),(.025,.05,.1)):
        # Per-finger spring overdrive beyond latest stop gives force f there;
        # earliest stop compresses 2e further. Full bank can share that error.
        travel=f/k+2*e
        load.append(dict(banks=bank,breakout=f,stiffness=k,e=e,
                         extra_travel=travel,bank_force=(6400//bank)*(f+2*k*e)))
    windows=[]
    for e,bias in it.product((.025,.05,.1,.2,.25,.3),(.0,.05,.1)):
        # Self-completing keeper threshold 1.0±e, terminal stop 1.7±e.
        low=1.+e+bias;high=1.7-e-bias
        # Product of endpoint errors includes coherent and opposed bias.
        feasible=low<high
        if feasible:
            cmd=(low+high)/2
            assert all(c<cmd+db<s for c,s,db in it.product((1.-e,1.+e),(1.7-e,1.7+e),(-bias,bias)))
        windows.append(dict(e=e,drive_bias=bias,command_low=low,command_high=high,positive_window=feasible))
    out=dict(reset_windows=windows,state_synthesis=states,clocked_synthesis=clock,geometry_poses=poses,
             rigid_mismatch=[rigid_mismatch(e) for e in (.01,.025,.05,.1)],central=central,
             read_sensitivity={str(r):{b:evaluate(b,read=r) for b in (2,4,8)} for r in (None,0.,.02,.05,.1)},
             local={b:{'explicit':[min(a),max(a)],'broadcast_scan':[min(c),max(c)],'changed_only':[min(z),max(z)]}
                    for b in (4,8) for a,c,z in [([lane.evaluate(b,'local',s) for s in range(76)],
                    [evaluate(b,'local',s) for s in range(76)],
                    [evaluate(b,'local',s,audit_all=False) for s in range(76)])]},
             compliant_bounds=load)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
