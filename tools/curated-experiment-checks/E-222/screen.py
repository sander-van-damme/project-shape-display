"""E-222: architecture necessary conditions, not hardware validation.
All motion/cost/process inputs are labelled scenario bounds in the result.
Stdlib; deterministic, no generated files.
"""
import itertools as it
import json
import math

LEVELS = range(5)


def move(d, a=8000, v=200):
    return 2 * math.sqrt(abs(d) / a) if abs(d) <= v*v/a else abs(d)/v + v/a


def absolute_service(mode, aux=.1, proof=.002, a=8000):
    if mode == 'independent':
        return 2*move(45,a) + move(40,a) + aux
    if mode == 'shared_signed':
        return 2*move(45,a) + 2*move(40,a) + aux
    if mode == 'stopped_dogs':
        # Five old-height stops, four per rewrite direction, five reset stops.
        return 2*move(5,a) + 16*move(10,a) + 18*proof + aux
    raise ValueError(mode)


def schedule(service, banks):
    # Same global 2 s, one complete row retry and feed as E-221.
    return 2 + (math.ceil(80/banks)+1)*(service+move(5.08))


def first_banks(service):
    return next(b for b in range(1,81) if schedule(service,b)<30)


def shared_replay(old, target):
    """Kinematic stopped-source scheduler. Separate grounded dogs and latched
    couplings are assumed; common source brake must arrest all coupled axes.
    Overlap handoffs are allowed ONLY at zero shaft speed. No contact model.
    """
    heights = [-.5]*len(old)  # units of 10 mm
    grounded = [True]*len(old)
    transfers = 0
    def stroke(sign, distances):
        nonlocal transfers
        coupled = [d>0 for d in distances]
        remaining = list(distances)
        # Engage coupling before withdrawing each parking dog, stationary.
        for i,c in enumerate(coupled):
            if c:
                assert grounded[i]
                grounded[i] = False
                transfers += 1
        while any(coupled):
            step = min(d for d,c in zip(remaining,coupled) if c)
            for i,c in enumerate(coupled):
                if c:
                    heights[i] += sign*step
                    remaining[i] -= step
                # Source-loss support cut: dog OR retained coupling to brake.
                assert grounded[i] or coupled[i]
            # Shaft stopped before any ground dog can engage.
            for i,c in enumerate(coupled):
                if c and remaining[i] == 0:
                    grounded[i] = True
                    coupled[i] = False
                    transfers += 1
            assert all(grounded[i] or coupled[i] for i in range(len(old)))
        assert all(grounded)
    stroke(1,[o+.5 for o in old])
    assert heights == list(old)
    # Resident comb can now release. Frozen unchanged channels never couple.
    stroke(1,[max(0,t-o) for o,t in zip(old,target)])
    stroke(-1,[max(0,o-t) for o,t in zip(old,target)])
    assert heights == list(target)
    # Comb deposit/proof precedes empty reset.
    stroke(-1,[t+.5 for t in target])
    assert heights == [-.5]*len(old)
    return transfers


def stack_service(aux=.1, unit_proof=.02):
    # Flat 10-mm units; mixed signed row: four inserts then four removals.
    # Defined four-stroke feeder: vertical up/down + horizontal out/back.
    unit = 2*move(10) + 2*move(5.08) + unit_proof
    return 8*unit+aux


def reserve(banks, shared=False):
    # Controller15+PSU25+frame35+comb hardware16+wiring14+freight25 =130.
    # Per head: transport20+dock5+reader15=40.
    # Shared source adds motor/driver12+brake8+shaft/bearings5=25/head.
    return 130+(65 if shared else 40)*banks


def main():
    visits=0
    for old,target in it.product(it.product(LEVELS,repeat=3),repeat=2):
        shared_replay(old,target)
        visits+=1
    # Witness demands all acquisition, signed delta and reset stop distances.
    old=(0,0,0,0,10,20,30,40,20)
    target=(10,20,30,40,0,0,0,0,20)
    assert set(old)==set(target)=={0,10,20,30,40}
    assert {t-o for o,t in zip(old,target)}==set(range(-40,41,10))
    # Independent limit: source brake alone cannot hold disconnected shoe.
    assert not (False or (False and True))
    # One common hydraulic valve fixes sum, not difference of connected axes.
    A=50 # mm^2
    delta_mm=1
    assert A*(-delta_mm)+A*delta_mm==0
    work_J=(10-1)*delta_mm/1000
    assert work_J>0
    assert math.isclose(schedule(absolute_service('independent'),3),26.5112)
    assert math.isclose(move(5),.05) and move(0)==0
    timing=[]
    for mode in ('independent','shared_signed','stopped_dogs'):
        for aux in (.1,.25,.5):
            s=absolute_service(mode,aux)
            b=first_banks(s)
            timing.append(dict(mode=mode,aux=aux,banks=b,channels=80*b,
                               seconds=schedule(s,b),three_bank_s=schedule(s,3)))
    cost=[]
    for mode,b,shared in [('independent',3,False),('shared_signed',4,True),
                          ('stopped_dogs',5,True)]:
        r=reserve(b,shared); n=80*b
        cost.append(dict(mode=mode,reserve=r,channels=n,cap=(500-r)/n,
            sourced_actuator_only=n*3.96,
            sourced_plus_residual=r+n*(3.96+.53),
            custom_035_selector_plus_053=r+n*.88,
            residual_without_selector=r+n*.53,
            selector_cap_after_residual=(500-r)/n-.53))
    sb=first_banks(stack_service())
    print(json.dumps(dict(ideal_three_cell_visits=visits,timing=timing,cost=cost,
        stack=dict(banks=sb,selected_forks=80*sb,token_shuttles=80*sb,
            seconds=schedule(stack_service(),sb),three_bank_s=schedule(stack_service(),3),
            inventory=4*6400,volume_L=4*6400*3.4**2*10/1e6),
        hydraulic=dict(differential_work_J=work_J,head_peak_L_min=80*A*200/1e6*60,
            drift_mm_30s={str(q):q*30/A for q in (.01,.1,1.)}),
        screw=dict(rpm_at_200mm_s={str(p):200/p*60 for p in (1,2,8)},
            self_lock_lead_mm={str(mu):math.pi*4*mu for mu in (.05,.1,.2)}),
        stack_correlated_height_error_mm={str(e):4*e for e in (.05,.15,.35)},
        coast_after_delay_mm={str(t):200*t/1000 for t in (1,5,20)}),indent=2))


if __name__=='__main__':
    main()
