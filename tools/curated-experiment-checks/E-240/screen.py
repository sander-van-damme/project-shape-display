"""E-240: electrical mask writing, retention and complete-machine bounds.
Stdlib; stdout only. No FDM priors, qualified actuator or physical validation.
Supplier observations and scenario meanings are in the canonical result.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e239', Path(__file__).resolve().parents[1]/'E-239'/'screen.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
MU = 4e-7*math.pi
# Sourced spool lengths/prices; use a whole-spool procurement, not consumed grams.
SPOOLS = ((4043*.3048,22.37),(8086*.3048,41.76),(20215*.3048,85.82))


def wire_buy(length):
    # Sufficient bounded enumeration for the <=6-bank comparison (up to 6 km).
    return min((sum(n*p for n,(_,p) in zip(ns,SPOOLS)),ns)
               for ns in it.product(range(7),repeat=3)
               if sum(n*l for n,(l,_) in zip(ns,SPOOLS))>=length)


def inventory(banks,kind='direct',q=20):
    sites=80*banks
    dual=kind=='matrix_bistable'
    windings=sites*(2 if dual else 1)
    if kind=='direct': sinks,rows,keepers=sites,0,banks
    else:
        rows=banks*math.ceil(80/q)*(2 if dual else 1)
        sinks=banks*q
        keepers=0 if dual else banks*math.ceil(80/q)
    return dict(sites=sites,windings=windings,sinks=sinks,row_sources=rows,
        keepers=keepers,local_bistable_sites=sites if dual else 0,
        series_diodes=windings if kind!='direct' else 0,
        flyback_diodes=windings,shift_packages=banks*math.ceil((sinks//banks)/8))


def write_time(banks,kind='direct',q=20,throw=2,pulse=.010,decay=.001,proof=.003):
    # Safe, nonoverlapped transaction at a stationary supported datum.
    # Open/unlock and restore OFF; energize; close positive keeper; deenergize;
    # wait decay and read physical mask. Motion=assumed shared v/a from E-239.
    groups=math.ceil(80/q)
    bits=80*banks*(2 if kind=='matrix_bistable' else 1)
    serial=bits/1e6  # allocated shared 1-MHz chain; electrical timing unqualified
    if kind=='direct': return 2*(prior.move(throw)+proof)+pulse+decay+proof+serial
    if kind=='matrix_keeper':
        # Grant simultaneous release of all groups, sequential lock per group.
        return prior.move(throw)+proof+groups*(pulse+prior.move(throw)+proof+decay)+proof+serial
    return 2*groups*(pulse+decay)+proof+serial


def costs(banks,kind='direct',q=20,turns=100):
    inv=inventory(banks,kind,q)
    # 30-mm mean turn, 15% lead/scrap overhead. Unknown actual winding geometry.
    wire=wire_buy(inv['windings']*turns*.030*1.15)
    sinks=inv['sinks']
    # Published tiers with pack rounding; choose cheaper eligible order.
    fet=min(max(150,math.ceil(sinks/5)*5)*.0634,max(500,math.ceil(sinks/5)*5)*.056)
    shifts=max(50,inv['shift_packages'])*.0906
    diodes=inv['flyback_diodes']+inv['series_diodes']
    diode=min(max(50,math.ceil(diodes/50)*50)*.019,
              max(500,math.ceil(diodes/50)*50)*.0152,
              max(1500,math.ceil(diodes/50)*50)*.0134)
    sourced=dict(wire=wire[0],sink_fets=fet,shift_registers=shifts,diodes=diode)
    reserve=sum(prior.reserve(banks).values())
    # ALL remaining inputs are allocations, not quotations or a routed BOM.
    extra=dict(selector_pcbs=25,regulated_pulse_supply_extra=20,
               pole_armature_stock=.10*inv['sites'],returns_or_detents=.02*inv['sites'],
               keeper_hardware=2*inv['keepers'],harness_extra=10,
               passives_suppression_extra=5,winding_fixture=5,
               row_source_channels=.30*inv['row_sources'])
    base=reserve+sum(sourced.values())
    return dict(reserve=reserve,sourced=sourced,spools=wire[1],extras_assumed=extra,
                unpriced_remaining_at_500=500-base,total_allocation=base+sum(extra.values()))


def force(ni,gap_mm,area_mm2=25,force_factor=1):
    # Ideal one-gap Maxwell stress with a labelled force derating factor.
    return force_factor*MU*area_mm2*1e-6*ni**2/(2*(gap_mm*.001)**2)


def required_ni(gap_mm,load=.010,area_mm2=25,force_factor=.5,current_factor=.85):
    return gap_mm*.001*math.sqrt(2*load/(force_factor*MU*area_mm2*1e-6))/current_factor


def overwrite(old,target,kind,q=2):
    """Discrete command retention only: resident support is granted throughout.
    Matrix monostable without group retention has a constructive failure.
    """
    bits=list(old); n=len(bits); locked=[True]*n
    if kind=='direct':
        locked=[False]*n; bits=[0]*n
        bits=list(target)  # powered
        locked=[True]*n   # common keeper before removing power
    else:
        # Bistable bits are overwritten in place with explicit set/reset phases;
        # no bulk erase or loss of unaddressed state is granted.
        if kind!='matrix_bistable': bits=[0]*n; locked=[False]*n
        for start in range(0,n,q):
            for i in range(start,min(start+q,n)): bits[i]=target[i]
            if kind=='matrix_keeper':
                for i in range(start,min(start+q,n)): locked[i]=True
            elif kind=='matrix_bistable': locked=[True]*n
            # Turn current OFF before addressing next group.
            bits=[b if held else 0 for b,held in zip(bits,locked)]
    return tuple(bits)


def checks():
    count=0
    for old,target in it.product(it.product((0,1),repeat=4),repeat=2):
        for kind in ('direct','matrix_keeper','matrix_bistable'):
            assert overwrite(old,target,kind)==target
            count+=1
    assert overwrite((0,0,0,0),(1,0,0,0),'matrix_unretained')!=(1,0,0,0)
    # Force formula cross-check against B^2 A/(2 mu0), scaling and zero current.
    b=MU*40/.0015
    assert abs(force(40,1.5)-b*b*25e-6/(2*MU))<1e-12
    assert force(0,1)==0 and abs(force(80,1)-4*force(40,1))<1e-12
    for k in (.25,.5,1):
        ni=required_ni(1.85,force_factor=k)
        assert abs(force(ni*.85,1.85,force_factor=k)-.010)<1e-12
    # Bounded retained/power-loss states: no command-dependent output enabled
    # until lock+physical proof, no unlock while pickup bears load.
    allowed=0
    for resident,pickup,locked,proved,unlock in it.product((False,True),repeat=5):
        admissible=(resident or pickup) and (not pickup or (locked and proved and not unlock)) and (not unlock or resident)
        if admissible:
            assert not (pickup and unlock)
            assert resident or (locked and proved)
            allowed+=1
    for banks in (4,5,6):
        for w in (0,.01,.05,.1):
            independent=2+prior.move(30)+.010+(math.ceil(80/banks)+1)*(
                .525+5*(4*(prior.move(2)+.003)+w)+prior.move(5.08))
            assert abs(prior.schedule(banks,writer=w)-independent)<1e-9
    return dict(overwrites=count,unretained_counterexamples=1,admissible_support_states=allowed,
                scheduler_cross_checks=12)


def dynamic_demand(pulse, mass=.0002, stroke=.001, drag=.002):
    # Rest-to-rest triangular speed over full mechanical pulse time; optimistic
    # because current rise is included in the available time, not added to it.
    # Comparing initial-gap force to this demand tests this prescribed profile,
    # not a universal lower bound for variable-acceleration pull-in.
    return drag+4*mass*stroke/pulse**2


def main():
    cases=[]
    for kind,q,throw,pulse in it.product(('direct','matrix_keeper','matrix_bistable'),(10,20,40,80),(1,2,4),(.005,.010,.020)):
        if kind=='direct' and q!=80: continue
        if kind=='matrix_bistable' and throw!=2: continue
        banks=next(b for b in range(4,21) if prior.schedule(b,writer=write_time(b,kind,q,throw,pulse))<30)
        cases.append(dict(kind=kind,q=q,throw_mm=throw,pulse_ms=pulse*1000,banks=banks,
            seconds=prior.schedule(banks,writer=write_time(banks,kind,q,throw,pulse)),
            write_ms=1000*write_time(banks,kind,q,throw,pulse),inventory=inventory(banks,kind,q),
            costs=costs(banks,kind,q)))
    # Two isolated winding alternatives; no measured steel permeability/damping.
    coils=[]
    for turns,current,gap,e,k in it.product((100,200),(.2,.4),(1.5,2.5),(.15,.35,.70),(.25,.5,1)):
        length=turns*.030; resistance=1.72e-8*length/(math.pi*.000160**2/4)
        coils.append(dict(turns=turns,current_A=current,gap_mm=gap,error_mm=e,force_factor=k,
            adverse_force_N=force(turns*current*.85,gap+e,force_factor=k),
            resistance_ohm=resistance,all_400_peak_copper_W=400*current**2*resistance,
            installed_400_wire_m=400*length,wire_cost_with_15pct_extra=wire_buy(400*length*1.15)[0]))
    coupled=[]
    for case in cases:
        for turns,current in it.product((100,200),(.2,.4)):
            available=force(turns*current*.85,1.85,force_factor=.5)
            required=dynamic_demand(case['pulse_ms']/1000)
            cost=costs(case['banks'],case['kind'],case['q'],turns)['total_allocation']
            coupled.append(dict(kind=case['kind'],banks=case['banks'],q=case['q'],
                throw_mm=case['throw_mm'],pulse_ms=case['pulse_ms'],turns=turns,
                current_A=current,available_N=available,required_N=required,
                force_necessary_pass=available>=required,cost=cost,seconds=case['seconds']))
    power=[]
    for turns,current in it.product((100,200),(.2,.4)):
        r=1.72e-8*(turns*.03)/(math.pi*.000160**2/4)
        hold=.010+prior.move(1)+.003
        power.append(dict(turns=turns,current=current,coil_R=r,
            all_400_peak_A=400*current,copper_peak_W=400*current**2*r,
            five_V_bus_peak_W=5*400*current,
            # Favorable constant-current capacitor top-up, 5 V bus, 15% droop.
            capacitor_F_if_40A_supply=max(0,400*current-40)*hold/.75,
            powered_seconds_per_29s_map=85*hold,
            copper_energy_per_map_J=85*hold*400*current**2*r))
    out=dict(checks=checks(),scenarios=cases,coil_bounds=coils,power=power,
        coupled_case_count=len(coupled),coupled_under_500_and_force=[c for c in coupled
            if c['force_necessary_pass'] and c['cost']<500],
        least_allocated_force_survivor=min((c for c in coupled if c['force_necessary_pass']),
                                         key=lambda c:c['cost']),
        nominal_direct_B5=costs(5),nominal_direct_B6=costs(6),
        direct_B5_keeper_sweep=[dict(throw_mm=t,write_ms=1000*write_time(5,throw=t),
            seconds=prior.schedule(5,writer=write_time(5,throw=t))) for t in (1,2,4)],
        force_required_ampere_turns=[dict(error_mm=e,factor=k,NI=required_ni(1.5+e,force_factor=k))
            for e,k in it.product((.15,.35,.70),(.25,.5,1))],
        coincidence_bounds=[dict(field_error=e,threshold_error=d,max_parasitic=(1-3*e-3*d+e*d)/2)
            for e,d in ((.05,.05),(.15,.15),(.25,.30))])
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
