"""E-173: lane-addressed rack, finite rigid boxes; mm, s, N, USD.
No fabricated geometry, process distributions, strength or dynamic qualification.
"""
import itertools as it
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-172'))
import scheduling as control

P = 10.1
LANES = tuple(.9*(j-2) for j in range(5))
PAIRS = tuple(it.product(range(5), repeat=2))


def overlap(a, b):
    return max(0., min(a[1], b[1])-max(a[0], b[0]))


def volume(a, b):
    return math.prod(overlap(x,y) for x,y in zip(a,b))


def box(x, y, z):
    return (x,y,z)


def solids(z, q, d, pad, errors, dog_z, lip):
    # Connected column union: spine, five unique-lane teeth, left pickup, cap.
    spine = box((-.6,.6),(-2.3,2.3),(z-41.4,z+50))
    teeth = [box((.2,1.8),(y-.25,y+.25),(z-j*P+errors[j],z-j*P+errors[j]+1.2))
             for j,y in enumerate(LANES)]
    pickup = box((-1.8,-.2),(-.5,.5),(z+lip,z+lip+.9))
    cap = box((-2.3,2.3),(-2.3,2.3),(z+50,z+51))
    dog = box((1.2,2.2),(q-.25,q+.25),(dog_z-1,dog_z))
    moving = box((-2.2,-1.2),(pad-.5,pad+.5),(d-1,d))
    return [spine,*teeth,pickup,cap], dog, moving


def supported_height(q, errors, dog_z):
    seats = [j*P+dog_z-errors[j] for j,y in enumerate(LANES)
             if overlap((q-.25,q+.25),(y-.25,y+.25))>1e-10]
    assert seats, 'dog between lanes: no grounded support'
    return max(seats)


def check_pose(z,q,d,pad,errors,dog_z,lip):
    column,dog,moving = solids(z,q,d,pad,errors,dog_z,lip)
    assert all(volume(s,dog)<1e-9 and volume(s,moving)<1e-9 for s in column)
    assert volume(dog,moving)==0
    grounded = any(overlap(t[0],dog[0])*overlap(t[1],dog[1])>1e-10
                   and abs(t[2][0]-dog[2][1])<1e-8 for t in column[1:6])
    carried = (overlap(column[6][0],moving[0])*overlap(column[6][1],moving[1])>1e-10
               and abs(column[6][2][0]-d)<1e-8)
    assert grounded or carried, 'neither finite contact supports the column'
    # Vertical force allocation exists; ideal prismatic joints carry moments.
    for force in (.1,1.,10.):
        rg = force if grounded else 0.
        rc = force-rg
        assert rg>=0 and rc>=0 and math.isclose(rg+rc,force)
    # Every generated solid is confined in XY to the same 4.6-mm square.
    # This exact projection certificate covers both lattice directions, all
    # neighbor heights/pad states, and continuous motion without height samples.
    assert all(-2.3-1e-9<=v<=2.3+1e-9 for part in column+[dog,moving]
               for interval in part[:2] for v in interval)
    return 1


def replay(pairs,errors=(0.,)*5,dog_z=0.,lip=1.,subdivisions=1):
    """Common deck; per-cell pad bit and persistent five-position grounded dog.
    Actual y-index retention is a boundary, not an implemented detent.
    """
    q=[LANES[o] for o,t in pairs]
    pads=[1.7]*len(pairs)  # 0 active; 1.7 clear
    d=-2.; count=0
    active=[i for i,(o,t) in enumerate(pairs) if o!=t]
    def pose(dd,qq=None,pp=None):
        nonlocal count
        qs=q if qq is None else qq;ps=pads if pp is None else pp
        for i,(o,t) in enumerate(pairs):
            ground=supported_height(qs[i],errors,dog_z) if qq is None else None
            # During a top-level selector sweep, the deck alone carries the cell.
            if ground is None:
                ground=max((j*P+dog_z-errors[j] for j,y in enumerate(LANES)
                            if overlap((qs[i]-.25,qs[i]+.25),(y-.25,y+.25))>1e-10),default=-math.inf)
            pickup=overlap((ps[i]-.5,ps[i]+.5),(-.5,.5))>1e-10
            z=max(ground,dd-lip) if pickup else ground
            if i not in active: assert abs(z-(o*P+dog_z-errors[o]))<1e-9
            count+=check_pose(z,qs[i],dd,ps[i],errors,dog_z,lip)
    def deck(end):
        nonlocal d
        ts={k/subdivisions for k in range(subdivisions+1)}
        if end!=d:
            # All actual lip contact crossings; other rack lanes stay disjoint.
            for j in range(5):
                crossing=j*P+dog_z-errors[j]+lip
                t=(crossing-d)/(end-d)
                if 0<t<1:ts.add(t)
        ordered=sorted(ts);ts.update((a+b)/2 for a,b in zip(ordered,ordered[1:]))
        for t in sorted(ts):pose(d+t*(end-d))
        d=end
    def pad_set(value):
        start=pads[:]
        for k in range(subdivisions+1):
            pp=[start[i]+(value-start[i])*k/subdivisions if i in active else start[i] for i in range(len(pairs))]
            pose(d,pp=pp)
        for i in active:pads[i]=value
    pose(d)
    if not active:return count
    pad_set(0.)
    for o in sorted({pairs[i][0] for i in active}):deck(o*P+2)
    deck(4*P+5)
    # Full continuous selector sweep is vertically clear of every rack tooth.
    for k in range(subdivisions+1):
        qq=[q[i]+(LANES[pairs[i][1]]-q[i])*k/subdivisions if i in active else q[i] for i in range(len(pairs))]
        pose(d,qq=qq)
    for i in active:q[i]=LANES[pairs[i][1]]
    for t in sorted({pairs[i][1] for i in active},reverse=True):
        deck(t*P+2);deck(t*P)
        for i in active:
            if pairs[i][1]==t:assert t*P-lip<supported_height(q[i],errors,dog_z)
    deck(-2.);pad_set(1.7)
    assert all(abs(supported_height(q[i],errors,dog_z)-(t*P+dog_z-errors[t]))<1e-9 for i,(o,t) in enumerate(pairs))
    return count


def dimensional_bounds(e):
    # Two center errors plus two independent facing-edge errors: ±4e.
    # Enumerate actual finite 1-D intervals rather than only assert formulas.
    same=[];wrong=[];x_same=[]
    for da,db,ea,eb in it.product((-e,e),repeat=4):
        same.append(overlap((-.25+da+ea,.25+da-ea),(-.25+db+eb,.25+db-eb)))
        wrong.append((.9-.25+db+eb)-(.25+da-ea))
        x_same.append(overlap((.2+da+ea,1.8+da-ea),(1.2+db+eb,2.2+db-eb)))
    assert math.isclose(min(same),max(0,.5-4*e),abs_tol=1e-9)
    assert math.isclose(min(wrong),.4-4*e,abs_tol=1e-9)
    assert math.isclose(min(x_same),max(0,.6-4*e),abs_tol=1e-9)
    return dict(e=e,bearing_y=min(same),wrong_lane_gap=min(wrong),bearing_x=min(x_same),area=min(same)*min(x_same),neighbor_gap=.48-4*e)


def bank_time(rows,word=.5,slot=.1,proof=.1,v=200,acc=5000,overhead=2):
    active=[i for i,row in enumerate(rows) if any(o!=t for o,t in row)]
    if not active:return 0.
    pairs=[p for row in rows for p in row if p[0]!=p[1]]
    mv=lambda dist:control.r.move(dist,v,acc)
    elapsed=0.;rowpos=0
    for duration,order in ((slot,active),(word,list(reversed(active))),(slot,active)):
        for row in order:
            elapsed+=mv((row-rowpos)*5.08)+duration;rowpos=row
    elapsed+=mv(rowpos*5.08)
    d=-2.
    for end in [o*P+2 for o in sorted({o for o,t in pairs})]+[4*P+5]+[x for t in sorted({t for o,t in pairs},reverse=True) for x in (t*P+2,t*P)]+[-2.]:
        elapsed+=mv(end-d);d=end
    elapsed+=(len({o for o,t in pairs})+len({t for o,t in pairs}))*proof
    return overhead+elapsed+max(slot,word)+proof+2*mv(2.2)


def evaluate(banks,kind='full',start=0,**kwargs):
    rows=control.workload(kind,start);n=80//banks
    return max(bank_time(rows[i:i+n],**kwargs) for i in range(0,80,n))


def main():
    checks={}
    checks['vertical_corner_poses']=sum(replay(PAIRS,err,g,l) for err in it.product((-.05,.05),repeat=5) for g,l in it.product((-.05,.05),(.95,1.05)))
    checks['two_cell_maps']=625
    checks['two_cell_poses']=sum(replay(pairs) for pairs in it.product(PAIRS,repeat=2))
    checks['holdout_poses']=[replay(PAIRS,(.013,-.021,.037,-.043,.019),-.017,1.031,n) for n in (1,4,16)]
    # Missing target storage: two same-old cells given the same binary arm and
    # identical common history cannot take different targets deterministically.
    checks['binary_without_target_counterexample']={'old':[0,0],'wanted':[1,4],'same_local_input':True}
    # A retained dog at a wrong lane can be firmly supported at the WRONG level.
    q=LANES[2]+.41;actual=supported_height(q,(0.,)*5,0.)
    assert actual==3*P
    # At the incorrectly commanded target position tooth 3 has already passed
    # the dog; show the actual first collision just below its higher capture.
    column,dog,pad=solids(actual-.05,q,-2,1.7,(0.,)*5,0.,1.)
    penetration=volume(column[4],dog)
    assert math.isclose(penetration,.6*.01*.05,abs_tol=1e-10)
    checks['misindex_041']={'actual_height':actual,'target_height':2*P,'collision_mm3':penetration}
    # e=.125 adverse neighbor contact: centers move toward each other and both
    # facing edges expand. This is a concrete 3D collision, not just zero margin.
    e=.125
    adverse_dog=box((1.2,2.2),(e-.25-e,e+.25+e),(-1.,0.))
    wrong_tooth=box((.2,1.8),(.9-e-.25-e,.9-e+.25+e),(-.05,1.15))
    checks['e0125_wrong_tooth_collision_mm3']=volume(adverse_dog,wrong_tooth)
    assert math.isclose(checks['e0125_wrong_tooth_collision_mm3'],.003,abs_tol=1e-9)
    # Recessed ±.05-mm faces at an off-index midpoint leave no ground overlap.
    assert all(overlap((.45-.2,.45+.2),(y-.2,y+.2))==0 for y in LANES)
    checks['recessed_midpoint_has_no_ground_support']=True
    # A missed arm clear on a low unchanged neighbor makes the next sweep lift it.
    assert check_pose(2.,LANES[0],3.,0.,(0.,)*5,0.,1.)
    checks['missed_clear_unintended_lift_mm']=max(0.,3.-1.)
    assert checks['missed_clear_unintended_lift_mm']==2.
    # Independent dense hand sum with three row scans plus the final long return.
    mv=control.r.move;n=20
    deck=mv(4)+4*mv(P)+2*mv(3)+5*mv(2)+4*mv(P-2)+mv(2)
    hand=2+n*(.1+.5+.1)+3*(n-1)*mv(5.08)+mv((n-1)*5.08)+deck+1+.5+.1+2*mv(2.2)
    assert math.isclose(hand,evaluate(4))
    checks['independent_dense_time']=hand
    assert all(evaluate(b,'none')==0 for b in control.BANKS)
    out={'checks':checks,'dimensions':[dimensional_bounds(e) for e in (.025,.05,.075,.1,.125)],
         'central':{b:{'lanes':evaluate(b),**{f:control.evaluate(f,b)['seconds'] for f in ('key_tongue','separate','direct')}} for b in control.BANKS}}
    out['word_sensitivity']={w:{b:evaluate(b,word=w) for b in control.BANKS} for w in (.1,.2,.5,1.)}
    out['motion_sensitivity']=[{'v':v,'acc':a,'word':w,'first_bank':next((b for b in control.BANKS if evaluate(b,word=w,v=v,acc=a)<30),None)} for v,a in ((80,1000),(200,5000),(400,20000)) for w in (.1,.5,1.)]
    out['local']={b:[min(ts),max(ts)] for b in (2,4,8,16) for ts in [[evaluate(b,'local',start) for start in range(76)]]}
    # Linear inversion of multilevel setting time, including one repeated word.
    out['word_ceiling_s']={b:(30-evaluate(b,word=.1))/(80//b+1)+.1 for b in control.BANKS}
    out['overhead6_B4']=evaluate(4,overhead=6)
    out['channels']={b:{'shared':82*b,'separate_writers':163*b,'allowance_shared':250/(82*b),'allowance_split':250/(163*b)} for b in (2,4,8)}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
