"""E-241: polarized reusable commands; bounded architecture screen, not hardware.
Stdlib, stdout only. Supplier observations and assumptions in canonical result.
"""
import importlib.util
import itertools as it
import json
import math
from functools import lru_cache
from pathlib import Path

spec = importlib.util.spec_from_file_location('e240', Path(__file__).resolve().parents[1]/'E-240'/'screen.py')
e240 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e240)
prior = e240.prior
MU = 4e-7*math.pi
A = math.pi/4  # +/-45 degrees; 90-degree total rotor travel
J = .0002*.002**2  # assumed complete rotor mass and radius of gyration
VOLUME = math.pi*(.003175/2)**2*.0015875
MOMENT = 1.2*VOLUME/MU  # 1.2 T is an assumed working Br, not vendor minimum


def write_time(banks, pulse, group):
    # Local H bridges write either sign concurrently; no global polarity phase.
    # Current extinction per group; physical pattern proof once after all groups.
    return math.ceil(80/group)*(pulse+.001)+.003+160*banks/1e6


@lru_cache(None)
def costs(banks, turns):
    n=80*banks
    bridges=min(max(150,5*math.ceil(n/5))*.1684,max(500,5*math.ceil(n/5))*.1428)
    # Pack-size pricing: 50 packs = 500 magnets, NOT 50 magnets.
    magnets=min(math.ceil(n/10)*1.32,max(50,math.ceil(n/10))*1.20)
    shifts=max(50,math.ceil(2*n/8))*.0906
    wire=e240.wire_buy(n*turns*.030*1.15)[0]
    sourced=dict(bridges=bridges,magnets=magnets,shift_registers=shifts,wire=wire)
    # Retain inherited reserve conservatively, including $20 common writer drives.
    extra=dict(pcbs=25,pulse_power_extra=20,steel_targets_pivots=.05*n,
               harness=10,passives=5,winding_fixture=5)
    reserve=sum(prior.reserve(banks).values())
    base=reserve+sum(sourced.values())
    return dict(reserve=reserve,sourced=sourced,extras_assumed=extra,
                extras_ceiling_at_500=500-base,total=base+sum(extra.values()))


def field(ni, radius=.005, length=.010, axial_error=0):
    # Thin finite solenoid, on-axis field; actual dipole is extended/off-axis.
    z=axial_error
    f=lambda x:x/math.sqrt(radius*radius+x*x)
    return MU*ni/(2*length)*(f(z+length/2)-f(z-length/2))


def barrier_window(turns,current,pulse,reader=.01,error=.00035,k=.5,
                   moment_factor=.85,barrier_spread=.3,friction=6e-6,impulse=2e-6):
    # U=E*cos(pi*theta/(2a))^2. E(1-spread) must exceed work to saddle.
    # Reader acts adversely at 3 mm. Impulse is a bounded energy disturbance.
    # Pulse torque floor pays max restoring torque + triangular-profile inertia.
    read_torque=reader*.003
    low=(read_torque*A+impulse)/(1-barrier_spread)
    b=k*field(turns*current*.85,radius=.005+error,length=.010+2*error,
              axial_error=error)
    torque=MOMENT*moment_factor*b*math.cos(A)
    inertia=4*J*(2*A)/pulse**2
    high=(torque-friction-inertia)*(2*A/math.pi)/(1+barrier_spread)
    return dict(barrier_low_uJ=low*1e6,barrier_high_uJ=high*1e6,
        feasible=high>low,drive_floor_uNm=torque*1e6,inertia_uNm=inertia*1e6,
        field_mT=b*1000,midpoint_input_uJ=MOMENT*moment_factor*b*math.sin(A)*1e6,
        midpoint_kinetic_uJ=.5*J*(4*A/pulse)**2*1e6,maximum_reader_N=max(0,((high*(1-barrier_spread)-impulse)/A)/.003))


def power(banks,turns,current,pulse,group):
    n=banks*group
    r=1.72e-8*turns*.030/(math.pi*.000160**2/4)
    # Constant-current demand: PWM/current-control implementation is unqualified.
    return dict(coil_R=r,simultaneous=n,coil_sum_A=n*current,
        peak_copper_W=n*current*current*r,
        peak_5V_bus_W_bound=5*n*current,
        map_copper_J=(math.ceil(80/banks)+1)*5*80*banks*current*current*r*pulse,
        coil_voltage=current*r,bridge_voltage_typ=current*.280)


def overwrite(old,target,group=2):
    bits=list(old); observations=0
    for start in range(0,len(bits),group):
        for i in range(start,min(start+group,len(bits))): bits[i]=target[i]
        # Ideal bistable state survives current removal. Support remains resident.
        assert tuple(bits[:start+group])==target[:start+group]
        observations+=1
    return tuple(bits),observations


def checks():
    overwrites=observations=0
    for old,target in it.product(it.product((0,1),repeat=4),repeat=2):
        for group in (1,2,4):
            end,count=overwrite(old,target,group)
            assert end==target
            observations+=count; overwrites+=1
    # Independent sum of ring fields integrates the finite-solenoid expression.
    errs=[]
    for steps in (32,128,512):
        dz=.010/steps
        num=sum(MU*80/.010*.005**2/(2*(.005**2+(-.005+(i+.5)*dz)**2)**1.5)*dz for i in range(steps))
        errs.append(abs(num/field(80)-1))
    assert errs[2]<errs[1]<errs[0] and errs[2]<1e-6
    # Energy derivative, signed PM torque and soft-pole contrast.
    u=lambda t,e:e*math.cos(math.pi*t/(2*A))**2
    for t in (-.6,-.3,0,.3,.6):
        e=1e-5; dt=1e-6
        derivative=(u(t+dt,e)-u(t-dt,e))/(2*dt)
        exact=-e*math.pi/(2*A)*math.sin(math.pi*t/A)
        assert abs(derivative-exact)<1e-13
        assert math.cos(t)>0  # opposite field signs reverse torque throughout
    # Midpoint work by independent quadrature, and kinetic-energy demand.
    case=barrier_window(100,1.2,.005)
    b=case['field_mT']/1000
    steps=1000
    work=sum(MOMENT*.85*b*math.cos(-A+(i+.5)*A/steps)*A/steps for i in range(steps))
    assert abs(work/(case['midpoint_input_uJ']*1e-6)-1)<1e-7
    assert case['midpoint_input_uJ']<case['midpoint_kinetic_uJ']
    assert abs(field(160)-2*field(80))<1e-12
    assert abs(field(80,axial_error=.0005)-field(80,axial_error=-.0005))<1e-12
    sched=0
    for banks,p,g in it.product((4,5,6),(.005,.01,.02),(20,80)):
        w=write_time(banks,p,g)
        direct=2+prior.move(30)+.010+(math.ceil(80/banks)+1)*(.525+5*(4*(prior.move(2)+.003)+w)+prior.move(5.08))
        assert abs(prior.schedule(banks,writer=w)-direct)<1e-10
        sched+=1
    # Gate isolation: command loss during write cannot drop resident support;
    # during pickup, reject any rewrite or unproved retention.
    states=0
    for resident,pickup,proved,retained,rewrite in it.product((False,True),repeat=5):
        allowed=(resident or pickup) and (not pickup or (proved and retained and not rewrite)) and (not rewrite or resident)
        if allowed:
            assert not (pickup and rewrite)
            states+=1
    return dict(overwrites=overwrites,retained_group_observations=observations,
                solenoid_quadrature_relative_errors=errs,schedule_checks=sched,support_logic_states=states)


def parasitic_bound(pitch=.02032, columns=20, rows=4, ni=160):
    # Far-field dipole norm bound, not resolved fields or a universal lower bound.
    # Sum all sites in a rectangular 80-site head; coherent alignment is allowed.
    moment_max=1.32*(math.pi*((.003175+.0001)/2)**2*(.0015875+.0001))/MU
    coil_moment=ni*math.pi*.005**2
    worst=0
    for x,y in it.product(range(columns),range(rows)):
        inverse_r3=sum(1/(pitch*math.hypot(x-i,y-j))**3
            for i,j in it.product(range(columns),range(rows)) if (i,j)!=(x,y))
        worst=max(worst,inverse_r3)
    return dict(pitch_mm=pitch*1000,columns=columns,rows=rows,
        pm_field_bound_mT=1000*MU*moment_max*worst/(2*math.pi),
        neighbor_coil_bound_mT=1000*MU*coil_moment*worst/(2*math.pi),
        minimum_center_span_mm=[(columns-1)*pitch*1000,(rows-1)*pitch*1000])


def main():
    cases=[]
    for p,g,turns,current in it.product((.005,.010,.020,.040),(10,20,40,80),(50,100,200,400),(.2,.4,.8,1.2)):
        banks=next(b for b in range(4,21) if prior.schedule(b,writer=write_time(b,p,g))<30)
        window=barrier_window(turns,current,p)
        pw=power(banks,turns,current,p,g)
        # 5-V rail headroom is a necessary screen, not current regulation proof.
        voltage_ok=pw['coil_voltage']+pw['bridge_voltage_typ']<5
        cases.append(dict(pulse_ms=1000*p,group=g,banks=banks,turns=turns,current=current,
            seconds=prior.schedule(banks,writer=write_time(banks,p,g)),
            cost=costs(banks,turns)['total'],window=window,power=pw,voltage_ok=voltage_ok))
    eligible=[c for c in cases if c['window']['feasible'] and c['voltage_ok']]
    cheapest=min(eligible,key=lambda c:c['cost']) if eligible else None
    summary=dict(checks=checks(),case_count=len(cases),
        coupled_under_500=[c for c in eligible if c['cost']<500],
        cheapest_eligible=cheapest,cheapest_economic=min(cases,key=lambda c:c['cost']),
        cross_talk_bounds=[parasitic_bound(p,c,r) for p,c,r in ((.01016,40,2),(.02032,20,4),(.04064,10,8))],
        timing=[dict(banks=b,pulse_ms=p*1000,group=g,seconds=prior.schedule(b,writer=write_time(b,p,g)))
                for b,p,g in it.product((4,5),(.005,.01,.02),(20,80))],
        cost_examples=[dict(banks=b,turns=t,**costs(b,t)) for b,t in it.product((4,5),(50,100,200))],
        read_sensitivity=[dict(reader_N=f,error_mm=e*1000,factor=k,
            **barrier_window(200,.8,.020,reader=f,error=e,k=k))
            for f,e,k in it.product((0,.005,.01,.05,.2),(.00015,.00035,.00070),(.25,.5,1))],
        grouped_power=[dict(group=g,**power(5,200,.8,.02,g)) for g in (10,20,40,80)],
        pulse_limit_B4_ms=1000*((30-prior.schedule(4,writer=0))/(21*5)-.004-640/1e6),
        scenarios=cases)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
