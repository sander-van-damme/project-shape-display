#!/usr/bin/env python3
"""Unqualified global-platen drive envelope. SI units internally; JSON stdout.
No generated files. See D-final-drive.md for assumptions and catalog provenance.
"""
import json
from math import pi, sqrt
N=2048
G=9.81
V=.080
A=.800
SF=1.5

def column_bank_mass(length_mm=80,cavity=(3.8,.9)):
    # Same conservative two-sided-rack envelope as D-followup-cost.py.
    # 5.4x3.8 stem, 6x6x1.2 cap; do not subtract open rack grooves.
    volume=5.4*3.8*length_mm+(36-5.4*3.8)*1.2-cavity[0]*cavity[1]*(length_mm-1.2)
    return volume*N*1.24/1e6

scenarios={
 'light_hollow_80':dict(columns=column_bank_mass(),moving_frame=1.5,terrain=1.),
 'root_2kg_frame':dict(columns=column_bank_mass(),moving_frame=2.,terrain=5.),
 'nominal_3kg_frame':dict(columns=column_bank_mass(),moving_frame=3.,terrain=5.),
 'heavy_solid_100':dict(columns=column_bank_mass(100,(0,0)),moving_frame=5.,terrain=5.),
}
# Transmission efficiency assumptions, not vendor-verified properties.
# effective_lead is vertical travel per MOTOR revolution.
drives={
 'TR8x8_direct':dict(effective_lead=.008,efficiency=.30),
 '1605_ball_direct':dict(effective_lead=.005,efficiency=.90),
 '1610_ball_direct':dict(effective_lead=.010,efficiency=.90),
 'belt_3mm_20T_4p8reduction':dict(effective_lead=.003*20/4.8,efficiency=.90),
}

def travel_time(d):
    return 2*sqrt(d/A) if d<=V*V/A else 2*V/A+(d-V*V/A)/V

result=dict(inputs=dict(sites=N,g_m_s2=G,v_m_s=V,a_m_s2=A,force_service_factor=SF),mass_scenarios=scenarios,transmissions=drives,cases=[])
for name,masses in scenarios.items():
    mass=sum(masses.values())
    for drag in [.01,.03,.10,.50]:
        steady=mass*G+N*drag
        peak=mass*(G+A)+N*drag
        row=dict(scenario=name,moving_mass_kg=mass,drag_N_site=drag,up_steady_N=steady,up_peak_N=peak,design_force_N=SF*peak,steady_power_W=steady*V,down_steady_drive_N=N*drag-mass*G,four_corner_design_force_N=SF*peak/4,drive={})
        for dname,d in drives.items():
            lead=d['effective_lead']
            row['drive'][dname]=dict(rpm=60*V/lead,torque_Nm_excluding_rotation=SF*peak*lead/(2*pi*d['efficiency']))
        result['cases'].append(row)
# Four 16mm x200mm steel cylinders are conservative rotating screw envelopes;
# actual thread root/end machining reduce inertia; rotating pulleys must be added.
screw_radius=.008
screw_length=.2
screw_mass=7850*pi*screw_radius**2*screw_length
screw_inertia=.5*screw_mass*screw_radius**2
# Old 23HS30 datasheet rotor inertia is 280g cm²; use as labelled sensitivity only.
rotor_inertia=280e-7
result['1605_rotation_sensitivity']=dict(screws=4,steel_screw_mass_each_kg=screw_mass,screw_inertia_each_kg_m2=screw_inertia,assumed_rotor_inertia_kg_m2=rotor_inertia,angular_acceleration_rad_s2=2*pi*A/.005,additional_torque_Nm_without_service_factor=(4*screw_inertia+rotor_inertia)*2*pi*A/.005,additional_torque_Nm_with_service_factor=SF*(4*screw_inertia+rotor_inertia)*2*pi*A/.005)
result['travel_time_seconds']={str(int(mm)):travel_time(mm/1000) for mm in [5,40,50]}
# End-supported gate bending estimate: deflection PL^3/(48EI); force1N.
result['memory_gate_deflection_mm_per_N']={str(span):span**3/(48*3000*(4.2*.8**3/12)) for span in [10,15,20,84]}
# Price anchors plus separately named unquoted procurement allowances, per bank.
# $42.95 is displayed ball-screw family price, exact 200mm selected SKU unconfirmed.
price_rows=[
 ('NEMA23 motor',1,18.26,18.26,'catalog current 23HS30-2804S'),
 ('DM542T driver',1,19.65,19.65,'catalog'),
 ('36V ~200W supply',1,19.96,35.,'catalog low; preorder, no qualified SKU'),
 ('1605 screw with ballnut',4,42.95,55.,'family displayed price low; exact short SKU/options unconfirmed'),
 ('BF12/BK12 support pairs',4,16.80,22.,'catalog low; currently out of stock'),
 ('Ballnut mounting blocks',4,9.95,14.,'catalog low; custom plate alternative not free'),
 ('Synchronization belts/pulleys/idlers',1,35.,70.,'unquoted provision'),
 ('Independent anti-rack guide sets',1,30.,70.,'unquoted provision'),
 ('Brake/positive catch and release',1,20.,60.,'unquoted, essential unpowered support'),
 ('Mounting/leveling/fastener stock',1,20.,50.,'unquoted provision'),
 ('Axis wiring/limit/fusing provision',1,10.,25.,'unquoted provision'),
]
result['drive_cost_per_bank_rows']=[dict(item=k,qty=n,unit_low=l,unit_high=h,basis=b) for k,n,l,h,b in price_rows]
result['drive_cost_per_bank']={bound:sum(n*(l if bound=='low' else h) for _,n,l,h,_ in price_rows) for bound in ['low','high']}
result['drive_cost_two_banks']={k:2*v for k,v in result['drive_cost_per_bank'].items()}
assert abs(travel_time(.005)-.158113883)<1e-8
assert result['cases'][8]['scenario']=='nominal_3kg_frame'
print(json.dumps(result,indent=2))
