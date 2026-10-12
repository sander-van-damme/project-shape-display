"""E-247: shared signed-displacement rails. Stdlib, stdout only.
Ideal support/state graph and labelled scenario bounds; no physical validation.
"""
import itertools as it
import json
import math

LEVELS = range(0, 41, 10)
Q = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)


def move(d, a=8000., v=200.):
    d = abs(d)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def replay(old, target, fault=None):
    """Rack shoe selects one rail d; all rails obey z_d=lambda*d.
    Four real contact stages, with proved contacts GRANTED, before/after stroke.
    """
    code = tuple(b-a for a,b in zip(old,target))
    assert all(d in range(-40, 41, 10) for d in code)
    row, shoes = True, False
    checks = 0
    def check(h):
        nonlocal checks
        assert row or shoes, 'unsupported'
        assert all(0 <= x <= 40 for x in h), 'travel'
        assert all(a!=b or a==x for a,b,x in zip(old,target,h)), 'unchanged'
        checks += len(h)
    check(old)
    shoes = fault != 'missed_takeover'; check(old)
    if fault == 'program_rewrite': code = (40,)*len(code)
    row = False; check(old)
    for k in range(41):
        h = tuple(a+k*d/40 for a,d in zip(old,code))
        if fault == 'arrest_loss': shoes = False
        check(h)
    assert h == target
    row = fault != 'missed_reseat'; check(h)
    shoes = False; check(h)
    return checks


def writer(q, p, kind):
    d = 8*p; n = 80//q; j = move(2)+.003
    # Both start with unlocked, empty program and include reset, clamp and read.
    # Unary sweep: preset, eight selective releases, clear, then empty return.
    group = 8*move(p)+10*j+move(d) if kind=='sweep' else 2*move(d)+.010
    return 2*move(d)+2*j+.010+n*group+(n-1)*move(5.08)+move((n-1)*5.08)


def cycle(q, p, kind):
    j = move(2)+.003
    # Shoe approach, row out/in, shoe clear, loaded stroke and empty reset.
    return writer(q,p,kind)+4*j+2*move(40)+move(5.08)+.020


def timing(b,q,p,kind):
    # One full causal row retry. Only discrete stable faults qualify for retry.
    # Extra full empty reset/read conservatively charged, not prefetched.
    return 2+(math.ceil(80/b)+1)*cycle(q,p,kind)+move(40)+.010


def allocation(b,q):
    # Inherited category ALLOCATIONS; no quoted nine-lane/cam implementation.
    # 195 common +20/head +.50/writer channel +.02/selector keeper
    # + nine rail guide/backing/arrest duties at assumed $2 each/head.
    return 195+20*b+.50*b*q+.02*80*b+18*b


def main():
    maps = observations = 0
    for a,b in it.product(it.product(LEVELS,repeat=3),repeat=2):
        observations += replay(a,b); maps += 1
    faults = 0
    for f in ('missed_takeover','program_rewrite','arrest_loss','missed_reseat'):
        try: replay((0,40,20),(40,0,20),f)
        except AssertionError: faults += 1
        else: raise AssertionError(f)
    # Wrong but range-safe rail: finish at actual stable height, reseat, rewrite.
    retries=0
    for old,target,actual in it.product(LEVELS,repeat=3):
        replay((old,),(actual,)); replay((actual,),(target,)); retries+=1
    # Stable on-grid partial stops only: no claim of reseating at fractional height.
    partial=0
    for old,target in it.product(LEVELS,repeat=2):
        for h in LEVELS:
            if min(old,target)<=h<=max(old,target):
                replay((h,),(target,)); partial+=1
    # Nine necessary outputs: each retained channel has one net displacement.
    assert len({b-a for a,b in it.product(LEVELS,repeat=2)}) == 9
    # Common comb withdrawal changes support path of every unchanged cell.
    assert sum(a==b for a,b in zip([20]*80,[30]+[20]*79))==79
    # Independent continuous argument: convex interpolation cannot leave endpoints.
    # Rail envelope is exact: +40 rail can be 80 above a selected -40 rail.
    relative=max(a-b for a,b in it.product(range(-40,41,10),repeat=2))
    assert relative==80
    results=[]
    for kind,p in it.product(('sweep','absolute_oracle'),(3,4,6,8)):
        cap=math.floor(406.4/(16*p+4))
        for planar in (False,True):
            cases=[]
            for b,q in it.product(range(1,(cap if planar else 80)+1),Q):
                t=timing(b,q,p,kind)
                if t<30: cases.append(dict(b=b,q=q,channels=b*q,seconds=t,cost=allocation(b,q)))
            best=min(cases,key=lambda x:(x['cost'],x['seconds'])) if cases else None
            results.append(dict(kind=kind,pitch=p,planar=planar,bank_cap=cap,best=best))
    # Expanded no-overlap timeline matches closed form, including first programming.
    for b,q,p in ((4,80,6),(5,40,4),(8,20,6)):
        steps=[2.,move(40),.010]
        for _ in range(math.ceil(80/b)+1):
            steps.extend([writer(q,p,'sweep'),4*(move(2)+.003),move(40),move(40),move(5.08),.020])
        assert abs(sum(steps)-timing(b,q,p,'sweep'))<1e-9
    # Load allocation: worst row concentrated at far rail; no load averaging.
    # Cantilever rectangular section stress/deflection, E labelled 1..3 GPa.
    beam=[]
    for f,e in it.product((.1,1,10),(1000,3000)):
        length,width,height=48.,3.4,6.
        inertia=width*height**3/12
        beam.append(dict(load_N=f,E_MPa=e,stress_MPa=6*f*length/(width*height**2),deflection_mm=f*length**3/(3*e*inertia)))
    print(json.dumps(dict(maps=maps,observations=observations,faults=faults,
        stable_wrong_retries=retries,stable_partial_retries=partial,
        rail_relative_envelope_mm=relative,results=results,beam=beam,
        broad_planar_sweep_s=timing(4,80,6,'sweep'),
        broad_planar_absolute_s=timing(4,80,6,'absolute_oracle')),
        indent=2))


if __name__=='__main__': main()
