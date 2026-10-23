#!/usr/bin/env python3
"""Regenerate E-303 small analytical tables and plots; run from any directory."""
import csv
import itertools
import json
from pathlib import Path
from math import pi, cos, sqrt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from model import *

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
P = json.loads((HERE / "inputs.json").read_text())
plt.rcParams.update({"svg.hashsalt": "E303", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})


def save_csv(name, rows):
    with (OUT / (name + ".csv")).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def table(rows, cols):
    def fmt(v):
        if isinstance(v, float):
            return f"{v:.4g}"
        return str(v)
    keys, titles = zip(*cols)
    return ("| " + " | ".join(titles) + " |\n| " + " | ".join("---" for _ in keys) + " |\n"
        + "\n".join("| " + " | ".join(fmt(row[k]) for k in keys) + " |" for row in rows))


def figsave(name):
    plt.tight_layout()
    plt.savefig(OUT / (name + ".svg"), metadata={"Date": None})
    plt.close()


screw = []
scenarios = [
    ("light terrain", .05, .01, .10, .15, .005),
    ("moderate terrain", .2, .05, .20, .30, .020),
    ("loaded / imperfect guide", 1., .20, .30, .45, .080),
    ("5 N obstruction scenario", 5., .50, .30, .45, .100),
    ("20 N obstruction scenario", 20., 1., .30, .45, .100),
]
for name, f, guide, mu, mustart, drag_nmm in scenarios:
    up, down = screw_scenario(f, guide, mu, drag_nmm / 1000)
    startup, _ = screw_scenario(f, guide, mustart, drag_nmm / 1000)
    screw.append(dict(scenario=name, weight_N=f, guide_N=guide,
        mu_running=mu, mu_starting=mustart, parasitic_Nmm=drag_nmm,
        raising_running_Nmm=up*1000, raising_starting_Nmm=startup*1000,
        lowering_applied_Nmm=down*1000))
save_csv("screw-scenarios", screw)

eff = [dict(load_N=f, efficiency=eta,
            torque_Nmm=efficiency_torque(f, P["lead_m"], eta)*1000)
       for f in [.05, .2, 1., 5.] for eta in [.1,.25,.5,.75]]
save_csv("screw-efficiency", eff)
sensitivity = [dict(mean_diameter_mm=d, mu=mu,
    raising_1N_Nmm=thread_torque(1, .003, d/1000, mu)*1000,
    lowering_1N_Nmm=thread_torque(1, .003, d/1000, mu, direction="lower")*1000,
    efficiency=efficiency_torque(1, .003, 1)/thread_torque(1, .003,d/1000,mu),
    self_lock_mu_threshold=.003/(pi*d/1000)*cos(pi/4))
    for d in [2.,2.3,2.8] for mu in [.10,.20,.30,.45]]
save_csv("screw-thread-sensitivity", sensitivity)
plt.figure(figsize=(7.4,4.3))
mus = np.linspace(.05,.5,100)
for d in [2,2.3,2.8]:
    plt.plot(mus,[thread_torque(1,.003,d/1000,m)*1000 for m in mus],label=f"Raise, dm={d} mm")
    plt.plot(mus,[thread_torque(1,.003,d/1000,m,direction='lower')*1000 for m in mus],ls="--",label=f"Lower, dm={d} mm")
plt.axhline(0,color="black",lw=.8)
plt.xlabel("Assumed thread friction coefficient")
plt.ylabel("Thread-only torque at 1 N (N mm)")
plt.title("3 mm lead, 90° thread; negative lower torque = overhauling")
plt.legend(ncol=2,fontsize=8)
figsave("screw-friction-sensitivity")

geometry=[]
for d in P["diameters_mm"][:-1]:
    geometry.append(dict(diameter_mm=d, one_height_edge_gap_mm=5.08-d,
        two_height_same_level_gap_mm=nearest_same_tier(.00508,2)*1000-d,
        four_height_same_level_gap_mm=nearest_same_tier(.00508,4)*1000-d,
        nearest_3p2mm_shaft_edge_gap_mm=5.08-d/2-1.6))
save_csv("stagger-clearance", geometry)

friction=[]
for d in P["diameters_mm"]:
    area,rp,rw=annulus(d/2000,P["annulus_inner_radius_m"])
    required_force=.0001/(.3*rp)
    # Two hypothetical 1 mm² poles at every diameter: field demand only. This
    # deliberately does not imply that both poles/coils fit inside the diameter.
    required_B=sqrt(2*MU0*required_force/2e-6)
    friction.append(dict(diameter_mm=d, area_mm2=area*1e6,
        uniform_pressure_radius_mm=rp*1000, uniform_wear_radius_mm=rw*1000,
        force_for_0p1Nmm_N=required_force, force_for_0p5Nmm_N=.0005/(.3*rp),
        required_B_two_1mm2_poles_T=required_B,
        gap_only_AT_two_0p1mm_gaps=required_B*.0002/MU0,
        kinetic_torque_at_0p1N_Nmm=.3*.1*rp*1000,
        static_torque_at_0p1N_Nmm=.4*.1*rp*1000))
save_csv("friction-size",friction)
_, r47, _=annulus(.0047/2,.0011)
drag=[dict(preload_N=n, dynamic_mu=mu, off_drag_Nmm=friction_torque(n,mu,r47)*1000)
      for n in [.001,.005,.02,.05,.1] for mu in [.1,.3,.5]]
save_csv("off-drag",drag)

# Concrete A reference from mechanical concept: two M2 poles/series coils.
# 80 turns each, copper diameter0.10 mm, ID2.4/OD3.8 mm, height4 mm.
refcoil=dict(turns=160, wire_length_m=160*pi*.0031,
    resistance_ohm=RHO_CU*160*pi*.0031/(pi*.0001**2/4),
    copper_mass_kg=8960*160*pi*.0031*pi*.0001**2/4,
    copper_area_m2=pi*.0001**2/4)
_,rA,_=annulus(.0045,.0040)
mag=[]
for gap_um in [50,100,200]:
    for contact_um in [0,50,100]:
        for at in [8,16,32,48,64]:
            # Add fixed contact equivalent reluctance to steel branch; force only
            # from the TWO intended armature gaps, never from fixed contacts.
            steel=[(.025,1.7e-6,300)]
            if contact_um:
                steel.append((contact_um*1e-6,1.7e-6,1))
            m=magnetic_circuit(at,[(gap_um*1e-6,1.7e-6)]*2,steel,
                               bottleneck_m2=4.64e-6)
            op=coil_operating_point(refcoil,at)
            mag.append(dict(gap_each_um=gap_um, equivalent_fixed_contact_gap_um=contact_um,
                ampere_turns=at, current_A=op["current_a"], coil_power_W=op["power_w"],
                linear_pole_B_T=m["gap_flux_t"][0],
                ideal_gap_force_N=m["linear_force_n"],
                ideal_interface_torque_Nmm=.3*rA*m["linear_force_n"]*1000,
                below_assumed_core_limit=m["below_core_limit"],
                initial_copper_only_heating_K_per_s=op["initial_adiabatic_k_per_s"]))
save_csv("magnetic-reference",mag)
winding_rows=[]
for name, args in [("compact envelope only",(.0024,.0046,.003)),
                   ("larger envelope only",(.003,.008,.004))]:
    coil=winding(*args)
    for at in [10,30,60]:
        op=coil_operating_point(coil,at)
        winding_rows.append(dict(case=name, ID_mm=args[0]*1000,OD_mm=args[1]*1000,
            height_mm=args[2]*1000,turns=coil["turns"],resistance_ohm=coil["resistance_ohm"],
            ampere_turns=at,current_A=op["current_a"],power_W=op["power_w"],
            current_density_A_mm2=op["current_density_a_per_mm2"]))
save_csv("winding-envelope",winding_rows)
plt.figure(figsize=(7.4,4.3))
for gap in [50,100,200]:
    rows=[r for r in mag if r['gap_each_um']==gap and r['equivalent_fixed_contact_gap_um']==50]
    plt.plot([r['coil_power_W'] for r in rows], [r['ideal_interface_torque_Nmm'] for r in rows],marker="o",label=f"{gap} µm each armature gap")
plt.xlabel("Two 80-turn coils: calculated DC copper power (W)")
plt.ylabel("Ideal friction torque, μ=0.3 (N mm)")
plt.title("A: 9 mm armature reference, two 1.7 mm² poles\nNo leakage; μr=300; additional contact equivalent gap 50 µm")
plt.legend(fontsize=8)
figsave("magnetic-gap-power")

es=[]
for d in P['diameters_mm']:
    a,r,_=annulus(d/2000,.0011)
    for gap in [0,5,20]:
        for split in [False,True]:
            e=electrostatic(.8*a,r,300,12e-6,3.25,gap*1e-6,split=split)
            es.append(dict(diameter_mm=d, gap_um=gap, type="B2 floating" if split else "B1 connected",
                total_dielectric_um=12, terminal_V=300, active_area_mm2=.8*a*1e6,
                gap_pressure_Pa=e['gap_pressure_pa'],torque_gap_Nmm=e['torque_gap_nm']*1000,
                torque_bulk_Nmm=e['torque_bulk_nm']*1000,
                capacitance_pF=e['capacitance_f']*1e12, stored_energy_uJ=e['stored_energy_j']*1e6,
                cycle_energy_uJ=e['resistive_cycle_energy_j']*1e6,
                dielectric_field_MV_m=e['dielectric_field_v_per_m']/1e6))
save_csv("electrostatic-size",es)
esstack=[]
a,r,_=annulus(.0047/2,.0011)
for t in [6,12,25,50]:
    for v in [100,300,500]:
        for gap in [0,5,20]:
            e=electrostatic(.8*a,r,v,t*1e-6,3.25,gap*1e-6,split=True)
            esstack.append(dict(total_dielectric_um=t,terminal_V=v,gap_um=gap,
                torque_gap_Nmm=e['torque_gap_nm']*1000,capacitance_pF=e['capacitance_f']*1e12,
                dielectric_field_MV_m=e['dielectric_field_v_per_m']/1e6))
save_csv("electrostatic-film-voltage",esstack)
# Mechanical B concept active annulus, separate from constant-ID size sweep.
a,r,_=annulus(.0045,.0018)
bconcept=[]
for gap in [0,5,20]:
    e=electrostatic(a,r,300,12e-6,3.25,gap*1e-6,split=True)
    bconcept.append(dict(gap_um=gap,active_area_mm2=a*1e6,
        effective_radius_mm=r*1000,terminal_V=300,torque_gap_Nmm=e['torque_gap_nm']*1000,
        torque_bulk_Nmm=e['torque_bulk_nm']*1000,capacitance_pF=e['capacitance_f']*1e12,
        stored_energy_uJ=e['stored_energy_j']*1e6))
save_csv("electrostatic-B-concept",bconcept)
plt.figure(figsize=(7.4,4.4))
for gap in [0,5,20]:
    rows=[r for r in es if r['gap_um']==gap and r['type']=='B2 floating']
    plt.semilogy([r['diameter_mm'] for r in rows],[r['torque_gap_Nmm'] for r in rows],marker="o",label=f"{gap} µm assumed uniform air gap")
plt.axvline(5.08,color="gray",ls=":",label="5.08 mm pitch (not usable diameter)")
plt.xlabel("Outer active envelope diameter (mm); fixed 2.2 mm centre hole")
plt.ylabel("Ideal gap-closing friction torque (N mm)")
plt.title("B2: floating equal halves, 300 V terminal, 12 µm PET\nεr=3.25, μ=0.3, 80% electrode coverage; analytical bounds")
plt.legend(fontsize=8)
figsave("electrostatic-gap-size")

scaling=[]
for d in P['diameters_mm']:
    factor=(d/20)**3
    scaling.append(dict(diameter_mm=d,cubic_factor=factor,
        counterfactual_on_Nmm=83.4*factor,counterfactual_off_Nmm=1.1*factor,
        status="NOT a PET forecast; assumes same pressure, friction and scaled radial geometry"))
save_csv("published-cubic-counterfactual",scaling)

power=[dict(active_count=n,unit_coil_W=p,total_coil_W=n*p)
       for n in P['active_counts'] for p in P['coil_power_w_scenarios']]
save_csv("coil-array-power",power)
slip=[dict(torque_Nmm=t,relative_rpm=rpm,one_clutch_heat_W=slip_heat(t/1000,rpm),
           all6400_heat_W=6400*slip_heat(t/1000,rpm))
      for t in [.01,.1,.5,1.] for rpm in [60,300,600]]
save_csv("slip-heat",slip)
es_power=[]
ep=electrostatic(.8*annulus(.0047/2,.0011)[0],r47,300,12e-6,3.25,split=True)
for n in P['active_counts']:
    es_power.append(dict(count=n,capacitance_per_cell_pF=ep['capacitance_f']*1e12,
        all_charge_energy_J=n*ep['resistive_cycle_energy_j'],
        cycle_10Hz_power_W=n*ep['resistive_cycle_energy_j']*10,
        continuously_connected_100Mohm_bleed_W=n*300**2/1e8,
        continuously_connected_10Gohm_leak_W=n*300**2/1e10,
        driver_and_converter_losses="excluded; unknown"))
save_csv("electrostatic-array-power",es_power)

states=[]
for bits in itertools.product([0,1],repeat=4):
    rows,cols=bits[:2],bits[2:]
    v=matrix_voltages(rows,cols)
    unsigned=matrix_on(rows,cols)
    diode=matrix_on(rows,cols,mode="diode")
    states.append(dict(row1=rows[0],row2=rows[1],col1=cols[0],col2=cols[1],
        signed_voltages="/".join(",".join(map(str,row)) for row in v),
        unsigned_on_mask="/".join("".join(str(int(x)) for x in row) for row in unsigned),
        diode_on_mask="/".join("".join(str(int(x)) for x in row) for row in diode)))
save_csv("matrix-two-rail-states",states)
plt.figure(figsize=(7.4,4.0))
for p in [.01,.1,.5]:
    plt.loglog(P['active_counts'],[n*p for n in P['active_counts']],marker="o",label=f"{p:g} W per coil")
plt.xlabel("Simultaneously energized coils")
plt.ylabel("DC copper power (W)")
plt.title("Scale penalty; no heat-removal capacity assumed")
plt.legend()
figsave("array-coil-power")

md = """# E-303 generated analytical tables

Regenerate with `python analysis/generate.py` from the E-303 directory.
Inputs are **assumptions**, except explicit repository geometry and the separately
labeled published 20 mm reference. CSVs retain additional scenarios and precision.
All table torques are N mm; 1 N mm = 1 mN m = 0.001 N m.

## Screw scenarios

Guide resistance, friction and parasitic torque are illustrative; no owner torque
measurement exists. Lowering negative values mean braking is needed in this model.

"""
md+=table(screw,[("scenario","Scenario"),("weight_N","Weight N"),("guide_N","Guide N"),("raising_running_Nmm","Raise/run N mm"),("raising_starting_Nmm","Raise/start N mm"),("lowering_applied_Nmm","Lower applied N mm")])
md+="\n\n## Friction size comparison\n\nInner radius 1.1 mm; uniform pressure, μk=0.3, μs=0.4. No thrust-brake deduction.\n\n"
md+=table(friction,[("diameter_mm","OD mm"),("uniform_pressure_radius_mm","r effective mm"),("force_for_0p1Nmm_N","N for 0.1 N mm"),("force_for_0p5Nmm_N","N for 0.5 N mm"),("kinetic_torque_at_0p1N_Nmm","Kinetic at 0.1 N, N mm")])
md+="\n\nMagnetic field demand for the same 0.1 N mm using **two hypothetical 1 mm² poles**, with 0.1 mm gap each, zero steel reluctance and no leakage. These are field-demand bounds, not a fitting coil layout:\n\n"
md+=table(friction,[("diameter_mm","OD mm"),("required_B_two_1mm2_poles_T","Required gap B T"),("gap_only_AT_two_0p1mm_gaps","Gap-only NI A turns")])
md+="\n\n## Magnetic A reference\n\nTwo M2 poles, effective root area 1.7 mm² each; gap 0.10 mm each, extra fixed contact equivalent gap 0.05 mm, steel path 25 mm, μr=300. Two 80-turn series coils, calculated 3.42 Ω. Friction annulus 4.0–4.5 mm radius, μk=0.3. Values exclude leakage, bearing torque and temperature rise.\n\n"
base=[r for r in mag if r['gap_each_um']==100 and r['equivalent_fixed_contact_gap_um']==50]
md+=table(base,[("ampere_turns","NI A turns"),("current_A","I A"),("coil_power_W","P W"),("linear_pole_B_T","B T"),("ideal_gap_force_N","Force N"),("ideal_interface_torque_Nmm","Torque ceiling N mm")])
md+="\n\n## Electrostatic B2 size and air-gap sensitivity\n\n300 V terminal, equal floating halves, 12 µm total PET, εr3.25, μ0.3, 80% active annulus. Gap-closing model; not demonstrated real contact force.\n\n"
md+=table([r for r in es if r['type']=='B2 floating' and r['diameter_mm'] in [4.7,7,10]],[("diameter_mm","OD mm"),("gap_um","Gap µm"),("torque_gap_Nmm","Torque N mm"),("capacitance_pF","C terminal pF"),("stored_energy_uJ","Stored µJ")])
md+="\n\n## B concept annulus, separately dimensioned\n\nRo4.5/Ri1.8 mm on Ø10 mm carrier; 100% of this annulus before insulating seam allowance, otherwise as B2 above.\n\n"
md+=table(bconcept,[("gap_um","Gap µm"),("torque_gap_Nmm","Gap-closing N mm"),("torque_bulk_Nmm","Bulk-stress N mm"),("capacitance_pF","C pF")])
md+="\n\n## Stagger clearance\n\nSame-height circular envelopes only; negative clearance means collision. Last column checks a 3.2 mm shaft crossing the neighboring tier. A design allowance of 0.30 mm total envelope-to-envelope clearance is an assumption, not proven FDM tolerance.\n\n"
md+=table(geometry,[("diameter_mm","D mm"),("one_height_edge_gap_mm","1 height gap mm"),("two_height_same_level_gap_mm","2 heights gap mm"),("four_height_same_level_gap_mm","4 heights gap mm"),("nearest_3p2mm_shaft_edge_gap_mm","Neighbor shaft gap mm")])
md+="\n\n## Continuous coil power\n\n"
pr=[dict(count=n,**{str(p):n*p for p in P['coil_power_w_scenarios']}) for n in P['active_counts']]
md+=table(pr,[("count","Active")]+[(str(p),f"{p:g} W/cell → W") for p in P['coil_power_w_scenarios']])
md+="\n\n## Electrostatic electrical power\n\n4.7 mm envelope at ideal zero air gap. Full resistive charge/discharge cycles; fixed bleeders and leakage are examples, not verified parts. Converter quiescent power and switch leakage are excluded.\n\n"
md+=table(es_power,[("count","Cells"),("cycle_10Hz_power_W","10 Hz switching W"),("continuously_connected_100Mohm_bleed_W","100 MΩ bleeders W"),("continuously_connected_10Gohm_leak_W","10 GΩ leakage W")])
md+="\n\n## Useful plots and full data\n\n- [Screw friction](screw-friction-sensitivity.svg)\n- [A magnetic gap versus power](magnetic-gap-power.svg)\n- [B floating electrostatic gap versus size](electrostatic-gap-size.svg)\n- [Coil power at array scale](array-coil-power.svg)\n- [All 16 two-rail matrix states](matrix-two-rail-states.csv)\n- [Counterfactual scaling of published specialized 20 mm clutch](published-cubic-counterfactual.csv)\n- [Slip heat](slip-heat.csv)\n- [Film/voltage sweep](electrostatic-film-voltage.csv)\n- [Thread-diameter/friction sensitivity](screw-thread-sensitivity.csv)\n- [OFF preload sweep](off-drag.csv)\n- [Winding envelopes, not complete clutches](winding-envelope.csv)\n"
(OUT / "tables.md").write_text(md)
print(f"Generated {len(list(OUT.iterdir()))} tables/plots in {OUT.name}/")
