#!/usr/bin/env python3
"""E-144: deterministic state/flow screen; SI; no hardware or yield claim.
Dry air, well-mixed chamber, quasi-static spring piston; emit disposable JSON.
Nozzle law: NASA GUNNS wiki Standard_Flow_Equation, Orifice Flows.
"""
import itertools
import json
import math

PA, P0, T0, R, GAMMA = 101325., 601325., 293.15, 287.05, 1.4
CRIT = (2/(GAMMA+1))**(GAMMA/(GAMMA-1))
AREA, GAP, K, N, SHUNT, MU = .0024, .0004, 200000., 640., 40., .02
P_SEAT = PA + (N-SHUNT)/AREA
P_START = P_SEAT + K*GAP/AREA
P_PROOF = PA + (N-SHUNT-11/MU)/AREA  # 11 N capacity, not stopping proof


def flow(p, temp, diameter, cd=.7):
    if p <= PA or diameter <= 0:
        return 0.
    ratio = max(PA/p, CRIT)
    factor = 2*GAMMA/(GAMMA-1)*(ratio**(2/GAMMA)-ratio**((GAMMA+1)/GAMMA))
    return cd*math.pi*diameter**2/4*p/math.sqrt(R*temp)*math.sqrt(factor)


def chamber(p, dead, compliance, piston=True):
    q = min(GAP, max(0., (AREA*(p-PA)+SHUNT-N)/K)) if piston else 0.
    dq = AREA/K if piston and P_SEAT < p < P_START else 0.
    return dead+AREA*q+compliance*(p-PA), AREA*dq+compliance


def rate_time(p, diameter, cd, dead, compliance, exponent, piston=True):
    temp = T0*(p/P0)**((exponent-1)/exponent)
    volume, derivative = chamber(p, dead, compliance, piston)
    return (volume/exponent+p*derivative)/(R*temp*flow(p,temp,diameter,cd))


def midpoint(f, a, b, steps):
    dx = (b-a)/steps
    return sum(f(a+(i+.5)*dx) for i in range(steps))*dx


def drain(diameter=.0005, cd=.7, dead=2e-6, compliance=0., exponent=1.,
          target=P_PROOF, steps=256, piston=True):
    if diameter <= 0:
        return math.inf
    # Partition at contact, open stop and sonic transition, avoiding derivative jumps.
    cuts = sorted({target,P0,*[p for p in (P_SEAT,P_START,PA/CRIT) if target<p<P0]})
    f = lambda p: rate_time(p,diameter,cd,dead,compliance,exponent,piston)
    return sum(midpoint(f,a,b,steps) for a,b in zip(cuts,cuts[1:]))


def min_heads(cycle):
    return next((h for h in range(1,6401) if 6+math.ceil(6400/h)*cycle<30), None)


def runoff(u, length=.01):
    # Reduced support constraint: 2-mm rise, finite flat pickup, abrupt run-off.
    # Grant ideal disengagement/closure after edge; no finite-contact claim.
    if u < 0 or u >= .002+length:
        return 0.
    return min(u/.002,1.)


def fault_components(n, edges, bleeds, fed=()):
    """Eventual depressurization only; perfect edge conductance, no closure dynamics."""
    unseen, returned = set(range(n)), set()
    while unseen:
        todo, component = [next(iter(unseen))], set()
        while todo:
            i = todo.pop()
            if i in component:
                continue
            component.add(i)
            for a,b in edges:
                if a == i: todo.append(b)
                if b == i: todo.append(a)
        unseen -= component
        if component.intersection(bleeds) and not component.intersection(fed):
            returned |= component
    return sorted(returned)


def main():
    report = {}
    assert P_PROOF > PA and P_SEAT < P_START < P0
    assert AREA*(P0-PA) > 960+K*GAP+SHUNT
    assert math.isclose(MU*(N-SHUNT-AREA*(P_PROOF-PA)),11.)
    # Independent sonic expression, continuity, no-flow limit and diameter scaling.
    sonic = .7*math.pi*.0005**2/4*P0/math.sqrt(T0)*math.sqrt(GAMMA/R)*(2/(GAMMA+1))**((GAMMA+1)/(2*(GAMMA-1)))
    assert math.isclose(flow(P0,T0,.0005),sonic)
    assert flow(PA,T0,.0005) == flow(P0,T0,0) == 0
    assert math.isclose(flow(P0,T0,.001),4*flow(P0,T0,.0005))
    assert abs(flow(PA/CRIT*(1-1e-7),T0,.0005)/flow(PA/CRIT*(1+1e-7),T0,.0005)-1)<3e-7
    # Independent fixed-volume isothermal choked exponential.
    target = 300000.
    b = R*T0*sonic/P0/2e-6
    exact = math.log(P0/target)/b
    numeric = drain(target=target,piston=False,steps=1024)
    assert abs(numeric/exact-1)<1e-7
    report['checks'] = dict(fixed_volume_exact_s=exact,numeric_s=numeric,
        convergence_s=[drain(steps=s) for s in (64,128,256,512)])
    assert abs(drain(steps=256)-drain(steps=512))<1e-6
    # Mass balance derivative check including chamber return and wall compliance.
    for p in (150000.,365000.,500000.):
        for exponent in (1.,GAMMA):
            def mass(x):
                temp=T0*(x/P0)**((exponent-1)/exponent)
                return x*chamber(x,2e-6,2e-12)[0]/(R*temp)
            dm_dp=(mass(p+.1)-mass(p-.1))/.2
            temp=T0*(p/P0)**((exponent-1)/exponent)
            v,dv=chamber(p,2e-6,2e-12)
            assert math.isclose(dm_dp,(v/exponent+p*dv)/(R*temp),rel_tol=1e-8)
    report['release'] = []
    for d in (.0001,.00025,.0005,.001):
        massflow=flow(P0,T0,d)
        # Reversible isothermal compression floor; selected source pressure held.
        power=massflow*R*T0*math.log(P0/PA)
        report['release'].append(dict(d_mm=d*1000,contact_ms=1000*drain(d,target=P_SEAT),
            capacity11N_ms=1000*drain(d),ambient_lpm=massflow*R*T0/PA*60000,
            ideal_compressor_W_per_head=power,ideal_W_121=121*power,
            heads_with_sequential_vent=min_heads(.45+drain(d))))
    report['friction_resizing'] = []
    # Linearity of dt/dp in volume/compliance permits exact geometric rescaling.
    # Scale N, K, SHUNT, AREA together, preserving all pressure thresholds.
    # mu=.1/.3 then gives the same 11-N capacity at P_PROOF.
    base = drain()
    dead_only = drain(piston=False)
    for mu in (.02,.1,.3):
        scale = .02/mu
        fixed_line = dead_only + scale*(base-dead_only)
        all_scaled = scale*base
        for label, time in (('all_volume_scales',all_scaled),('fixed_2ml_line',fixed_line)):
            # d^2 scaling to reach the 10-ms pressure-capacity target.
            diam = .0005*math.sqrt(time/.01)
            watts = flow(P0,T0,diam)*R*T0*math.log(P0/PA)
            report['friction_resizing'].append(dict(mu=mu,volume_model=label,
                at_half_mm_ms=time*1000,d_for_10ms_mm=diam*1000,
                ideal_W_per_head_at_10ms=watts))
    mass_charge = (P0*(2e-6+AREA*GAP)-PA*2e-6)/(R*T0)
    report['recharge'] = dict(mg_from_ambient=mass_charge*1e6,
        constant_2x_steady_flow_ideal_time_bounds_ms=[
            1000*mass_charge/(2*flow(P0,T0,.0005)),
            1000*mass_charge/flow(P0,T0,.0005)],
        ideal_open_work_adverse_J=(960+SHUNT)*GAP+.5*K*GAP**2,
        swept_ml=AREA*GAP*1e6)
    report['thermal_volume'] = [dict(dead_ml=v*1e6,exponent=n,
        wall_expansion_fraction=beta,capacity11N_ms=1000*drain(dead=v,compliance=beta*v/500000,exponent=n))
        for v,n,beta in itertools.product((.25e-6,2e-6,14e-6),(1.,1.4),(0.,.2,1.))]
    # 16 coherent adversarial corners, not random cell draws: d=.5 +/-.05mm,
    # Cd=.4/.9, connected dead/tube volume=1.5/2.5ml, expansion=0/20%.
    cases=[drain(diameter=d,cd=cd,dead=v,compliance=beta*v/500000)
           for d,cd,v,beta in itertools.product((.00045,.00055),(.4,.9),(1.5e-6,2.5e-6),(0.,.2))]
    report['coherent_box'] = dict(cases=len(cases),min_ms=min(cases)*1000,max_ms=max(cases)*1000,
        pump_coast_ms=[0,10,50,200],worst_total_ms=[max(cases)*1000+t for t in (0,10,50,200)])
    # Aggregate restriction area must be shared over the connected volume.
    edges=[(i,i+1) for i in range(7)]
    faults=dict(sole_exhaust_blocked=fault_components(8,edges,[]),
        local_bleeds_common_exhaust_blocked=fault_components(8,edges,range(8)),
        one_bleed_blocked_connected=fault_components(8,edges,range(7)),
        one_bleed_blocked_and_branch_isolated=fault_components(8,edges[:-1],range(7)),
        sustained_source=fault_components(8,edges,range(8),fed=[0]),
        bank_split_all_local_bleeds=fault_components(8,edges[:3]+edges[4:],range(8)),
        coherent_all_bleeds_blocked=fault_components(8,edges,[]))
    assert [len(x) for x in faults.values()] == [0,8,8,7,0,8,0]
    report['eventual_vent_counts']={k:len(v) for k,v in faults.items()}
    report['one_bleed_blocked_connected_time_factor']=8/7
    report['runoff']=dict(flat_length_mm=10,at_20mm_s_dwell_s=.01/.02,
        minimum_40mm_travel_at_100mm_s=.04/.1,
        stall_during_flat_open=bool(runoff(.007)),after_runoff_open=bool(runoff(.013)),
        shortest_finite_flat_for_450ms_at20mm_s_mm=.45*.02*1000)
    assert runoff(.007)==1 and runoff(.013)==0
    report['schedule']=[dict(vent_and_rearm_allocation_s=t,heads=min_heads(.45+t)) for t in (0,.01,.05,.1,.2)]
    report['budget']=[dict(heads=h,remaining_after_250_shared_and_1_56_motors=250-1.56*h) for h in (121,134,137,149,169,178)]
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
