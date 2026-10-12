"""E-246: sealed pressure strip architecture bounds; no hardware validation.
All contact, motion, viscosity, error and cost inputs are scenario assumptions.
Stdlib, stdout only. Uses E-236's existing rest-to-rest motion law.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

s = importlib.util.spec_from_file_location('e236', Path(__file__).resolve().parents[1]/'E-236'/'screen.py')
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)
move = p.move
A = 25.6  # mm2, each of two opposed contact faces
PRESSURE = 1.5/(2*.15*A)  # MPa; 1 N total static weight, factor 1.5


def flow_time(n=80, gap=.44, viscosity=.001, travel=.9, feeds=1, beta=.25):
    """Rigid, wide slit: mu*u''=dp/dx gives Q=w*g^3*gradient/(12mu).
    Uniform distributed sink: integrate Q(x)=Qin*(1-x/L), hence factor 6.
    feeds=2: equal independent feeds from BOTH ends, each half length/volume.
    beta*holding pressure is allowed longitudinal driving pressure difference.
    Constant maximum gap, no fittings, no entrance/inertial/FSI losses granted.
    """
    length = n*5.08/1000/feeds
    face_volume = n*A*travel*1e-9/feeds
    return 6*viscosity*length*face_volume/(.008*(gap/1000)**3*(beta*PRESSURE*1e6))


def schedule(banks, area_per_cell=40., gap=.44, viscosity=.001, feeds=1, beta=.25, error=.35):
    # Largest resident zone has 80 sites (row); column segment <=80 sites.
    travel = .2+2*error
    volume_cell = 2*A*travel  # mm3, two opposed faces
    reservoir_stroke = volume_cell/area_per_cell
    r_close = max(move(reservoir_stroke), flow_time(80,gap,viscosity,travel,feeds,beta))+.003
    # Drawback grants an 80-kPa suction differential, no cavitation/adhesion.
    # Positive fill overpressure does not provide unlimited negative pressure.
    drain_beta = min(beta, .08/PRESSURE)
    r_open = max(move(reservoir_stroke), flow_time(80,gap,viscosity,travel,feeds,drain_beta))+.003
    # Grant identical volumetric stroke/site and pressure margin for head grip;
    # its holding pressure is higher for acceleration, so using static pressure
    # in its flow law is conservative within this fixed-slot model only.
    g_close = max(move(reservoir_stroke), flow_time(1,gap,viscosity,travel,1,beta))+.003
    g_open = max(move(reservoir_stroke), flow_time(1,gap,viscosity,travel,1,drain_beta))+.003
    write = move(2)+.003
    service = .525+5*(r_open+r_close+g_open+g_close+write)+move(5.08)
    visits = math.ceil(80/banks)
    total = 2+.185+(visits+1)*service
    events = [2., .185]
    for _ in range(visits+1):
        for d in (-20,-10,30,-10,10):
            events += [write,g_close,r_open,move(abs(d)),r_close,g_open]
        events += [move(5.08)]
    assert math.isclose(sum(events),total)
    return dict(banks=banks, seconds=total, resident_close_s=r_close, resident_open_s=r_open, grip_close_s=g_close,
                reservoir_stroke_mm=reservoir_stroke,
                row_reservoir_area_mm2=80*area_per_cell,
                row_hold_force_N=80*area_per_cell*PRESSURE,
                allocation_before_pressure_hardware_usd=195+61.6*banks)


def checks():
    # Independent discrete network: evenly-spaced sinks. Infinite uniform result
    # is approached from above; factor n/(n+1) distinguishes continuum optimism.
    n=80; length=n*.00508; gap=.00044; mu=.001; volume=n*A*.9*1e-9
    q=volume  # m3/s at one-second fill
    segment_resistance=12*mu*(length/n)/(.008*gap**3)
    discrete_dp=sum(segment_resistance*q*(n-i)/n for i in range(n))
    continuous_dp=6*mu*length*q/(.008*gap**3)
    assert math.isclose(discrete_dp/continuous_dp,(n+1)/n)
    assert math.isclose(flow_time(feeds=2)*4,flow_time())
    assert math.isclose(flow_time(gap=.22)/flow_time(gap=.44),8)
    assert math.isclose(flow_time(viscosity=.01)/flow_time(),10)
    # Pressure proof and total injected volume cannot locate a blind membrane.
    # Two faces at every pin, target .5 mm; one bridged/recessed site gets no
    # contact, another expands into an extra pocket, same aggregate volume/p.
    uniform=[.5]*80
    hidden=uniform[:];hidden[0]=0;hidden[1]=1
    assert sum(uniform)==sum(hidden)
    capacities=[0]+[2*.15*PRESSURE*A]*79
    assert capacities[0] < 1 and sum(capacities)>80
    # Hydraulic equalization is normal-force equalization, not shear stiffness.
    assert math.isclose(1/(2*10),.05)
    return dict(network_ratio=discrete_dp/continuous_dp,
                blind_contact_cells=1, same_total_volume_mm3=2*A*sum(hidden),
                equal_shear_stiffness_neighbor_shift_mm=.05)


def main():
    c=checks()
    sample=[]
    for feeds,beta,area,mu in [(1,.25,40,.001),(2,.25,40,.001),
                              (2,1,40,.001),(2,1,5,.001),
                              (2,1,40,.01),(2,4,40,.001)]:
        best=next(schedule(b,area,viscosity=mu,feeds=feeds,beta=beta)
                  for b in range(1,81)
                  if schedule(b,area,viscosity=mu,feeds=feeds,beta=beta)['seconds']<30)
        sample.append(dict(feeds=feeds,beta=beta,area_per_cell_mm2=area,viscosity_Pa_s=mu,**best))
    grid=[]
    for e,mu,gap,feeds,beta,area in itertools.product(
            (.15,.35,.70),(.001,.01,.1),(.14,.24,.44),(1,2),(.25,1,4),(5.,20.,40.,80.)):
        v=schedule(4,area,gap,mu,feeds,beta,e)
        if v['seconds']<30:
            grid.append(dict(error=e,viscosity=mu,gap=gap,feeds=feeds,beta=beta,area=area,seconds=v['seconds']))
    # Worst geometric displacement, not p*V electrical-work lower bound.
    zone=80+80*4;head=80*4
    print(json.dumps(dict(checks=c,pressure_MPa=PRESSURE,
        row_face_N=80*A*PRESSURE,row_volume_ml=2*80*A*.9/1000,
        flow_times_s={str(g):flow_time(gap=g) for g in (.14,.24,.34,.44)},
        samples=sample,
        B4_grid=dict(tested=3*3*3*2*3*4,timing_only_survivors=len(grid),survivors=grid),
        ledger_B4=dict(resident_circuits=zone,head_circuits=head,total_circuits=zone+head,
            independent_squeeze_and_keeper_duties=zone+head,
            two_face_strip_length_m=2*80*.4064+2*320*.1016,
            ideal_two_terminal_seals_per_circuit=2*(zone+head),
            fill_and_proof_hours_at_30_90_s=[(zone+head)*t/3600 for t in (30,90)],
            reservoir_projected_area_m2=(12800+320)*40/1e6,
            remaining_budget_usd=500-(195+61.6*4),
            remaining_usd_per_circuit=(500-(195+61.6*4))/(zone+head),
            release_volume_all_resident_ml=12800*2*A*.9/1000),
        fast_flow_diagnostic=dict(
            assumed_density_kg_m3=1000,
            mean_inlet_speed_m_s=(40*A*.9*1e-9)/(.024*.008*.00044),
            slit_Reynolds=(40*A*.9*1e-9)/(.024*.008*.00044)*(.00088)*1000/.001,
            triangular_flow_peak_acceleration_pressure_MPa=
                2*1000*.2032*(40*A*.9*1e-9)/(.008*.00044*.024**2)/1e6),
        gas_isothermal=dict(initial_absolute_MPa=.101,final_absolute_MPa=.101+PRESSURE,
            initial_volume_removal_fraction=1-.101/(.101+PRESSURE))),indent=2))

if __name__=='__main__':
    main()
