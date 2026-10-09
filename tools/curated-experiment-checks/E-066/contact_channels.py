#!/usr/bin/env python3
"""E-066: deterministic command-pad geometry/force bounds; not contact FEA.
SI internally; inputs explicitly suffixed. Requires NumPy. --all emits cases.
No random draws or calibrated yield. Physical assumptions are in E-066.
"""
import itertools as it
import json
import math
import sys
from collections import Counter
import numpy as np

EPS = 8.8541878128e-12
ER = 3.0
N = 6400
SCENARIOS = {
    'tight': dict(film=.10, placement_mm=.05, rough_um=2, tilt_mrad=.5, bow_um=2, mu=.3),
    'middle': dict(film=.20, placement_mm=.15, rough_um=5, tilt_mrad=1, bow_um=5, mu=.2),
    'wide': dict(film=.30, placement_mm=.30, rough_um=20, tilt_mrad=2, bow_um=20, mu=.1),
}


def pad(t_um, s, stroke_mm=.5, cells=128):
    """Actual rectangular overlap: fixed 2x20 mm, translated pad +stroke in y.
    Worst lateral placement reduces x overlap. Gap profile on fixed face is
    roughness pedestal + wedge + parabolic bow; shape is prescribed, not solved.
    Return unit-voltage force integrator, including remaining uniform air gap.
    """
    width = (2-s['placement_mm'])*1e-3
    lo, hi = stroke_mm*1e-3, .020
    dy = (hi-lo)/cells
    y = lo+(np.arange(cells)+.5)*dy
    u = y/.020
    profile = s['tilt_mrad']*1e-3*y + 4*s['bow_um']*1e-6*u*(1-u)
    eff = t_um*1e-6/ER+profile
    def force_unit(gap):
        g = np.asarray(gap)
        return EPS/2*width*dy*np.sum(1/(g[...,None]+eff)**2, axis=-1)
    return force_unit


def flat_pullin(g0, stop, k, film, area):
    # Exact maximum of k*x*(g0-x+d)^2 on [0,g0-stop].
    d=film/ER
    x=min(g0-stop,(g0+d)/3)
    return math.sqrt(2*k*x*(g0-x+d)**2/(EPS*area))


def geometry(t, g0_mm, k_N_mm, s, cells=128, steps=401):
    tmin,tmax=t*(1-s['film']),t*(1+s['film'])
    gmin,gmax=(g0_mm-s['placement_mm'])*1e-3,(g0_mm+s['placement_mm'])*1e-3
    stop=s['rough_um']*1e-6
    if gmin<=stop:
        return None
    kmin,kmax=.8*k_N_mm*1000,1.2*k_N_mm*1000
    unit=pad(tmax,s,cells=cells)
    # Sweep actual normal opening and finite sliding overlap; worst slide is
    # endpoint since the positive integrand loses [0,stroke] as stroke grows.
    x=np.linspace(0,gmax-stop,steps)
    vreq=np.sqrt(kmax*x/unit(gmax-x))
    # Best flat geometry upper-bounds unwanted attraction; use larger full area.
    fmax_unit=EPS/2*40e-6/(tmin*1e-6/ER)**2
    return dict(v_pull_selected=float(max(vreq)),
                v_pull_unwanted=flat_pullin(gmin,0,kmin,tmin*1e-6,40e-6),
                unit_min=float(unit(stop)),unit_max=fmax_unit,
                restore_min=kmin*gmin,restore_max=kmax*(gmax-stop),
                closing_stroke_mm=(gmax-stop)*1000,
                cam_force_two_arrays_N=2*N*kmax*(gmax-stop))


def population(cells=128, steps=401):
    out=[]
    for (name,s),t,g0,k in it.product(SCENARIOS.items(),[10,25,50],[.15,.35,.6],[.02,.1,.5]):
        geo=geometry(t,g0,k,s,cells,steps)
        for v,r,topology,address in it.product([200,265,500],[0,.02,.1,.3],['free','preclosed'],['active','half']):
            row=dict(scenario=name,film_um=t,rest_gap_mm=g0,k_N_mm=k,V=v,
                     residual_fraction=r,topology=topology,address=address)
            reasons=[]
            if geo is None:
                reasons=['open_clearance']
            else:
                # Active 35V off is an explicit conservative circuit scenario;
                # half voltage is a passive cross-point comparator, not A-015.
                unwanted=35 if address=='active' else v/2
                shear=s['mu']*max(0,v*v*geo['unit_min']-geo['restore_max'])
                drag=.6*max(0,unwanted**2*geo['unit_max']-geo['restore_min'])
                if shear<.05: reasons.append('command_force')
                if topology=='free':
                    if v<geo['v_pull_selected']: reasons.append('acquisition')
                    if unwanted>=geo['v_pull_unwanted']: reasons.append('unwanted_acquisition')
                if drag>=.01: reasons.append('unwanted_command')
                # Remove the closing cam before transmitting shear. On reset,
                # spring must start separation at the strongest contact corner.
                release_v = (35 if address=='active' else 0) + r*v
                if release_v**2*geo['unit_max']>=geo['restore_min']:
                    reasons.append('residual_release')
                row.update(selected_shear_N=shear,unwanted_drag_N=drag,
                           residual_release_limit=max(0,math.sqrt(geo['restore_min']/geo['unit_max'])-(35 if address=='active' else 0))/v,
                           **geo)
            row['reasons']=reasons
            out.append(row)
    return out


def support_check():
    """Required logical support guards, not a generated collet/pawl solution.
    Refuse loss of support and preserve unchanged columns across 25 height pairs.
    Failed command/proof freezes before a destructive transfer.
    """
    traces=[]
    for old,new in it.product(range(0,41,10),repeat=2):
        ground,moving=True,False
        trace=['ground']
        if old!=new:
            for _ in range(int(old!=0)+int(new!=0)):
                moving=True;trace.append('ground+moving: grip proved')
                ground=False;trace.append('moving: ground withdrawn')
                ground=True;trace.append('ground+moving: ground seated/proved')
                moving=False;trace.append('ground: collet reset')
                assert ground or moving
        traces.append(dict(old=old,new=new,trace=trace))
    # A stuck command must inhibit shared motion, not unlock the old pawl.
    def allowed(ground,grip_proof,latch_proof,release_ok,action):
        if action=='unlock_ground': return ground and grip_proof and release_ok
        if action=='release_moving': return latch_proof and release_ok
        raise ValueError(action)
    for action in ['unlock_ground','release_moving']:
        assert not allowed(True,True,True,False,action)
    assert not allowed(True,False,True,True,'unlock_ground')
    assert not allowed(False,True,False,True,'release_moving')
    return traces


def ledger():
    channels=2*N
    chips=math.ceil(channels/64)
    # Source snapshots verified 2026-10-09: manufacturer 5k indicative and DigiKey 100+.
    cap=EPS*40e-6/(10e-6/ER)
    motion=.6+8*2*math.sqrt(10/500)+6
    return dict(channels=channels,HV507_packages=chips,
        HV507_chip_only_USD_100_tier=chips*16.0875,
        HV507_chip_only_USD_5k_indicative=chips*14.47,
        HV583_chip_only_USD_5k_80V_counterfactual=100*11.38,
        max_complete_channel_USD_at_250reserve=250/channels,
        max_sites_chip_only_at_250reserve=32*math.floor(250/16.0875),
        max_IC_USD_at_250reserve=250/chips,
        full_chain_shift_s_at_8MHz=channels/8e6,
        nominal_flat_pad_cap_pF=cap*1e12,
        board_charge_C_265V=channels*cap*265,
        capacitor_storage_J_265V=.5*channels*cap*265**2,
        ideal_source_step_J_265V=channels*cap*265**2,
        naive_1mA_each_peak_A=channels*.001,
        HV507_quiescent_max_W_at_300V=chips*.0005*300,
        trace_m_at_10_50mm_per_channel=[channels*x/1000 for x in [10,50]],
        HV507_package_pins=chips*80,
        event_budget_s=(30-motion)/9,
        full_time_s_at_dwell={str(d):motion+9*d for d in [.02,.2,1.4,2.4]},
        false_accept_expected_sites={str(p):N*p for p in [1e-3,1e-4,1e-5]})


def checks():
    flat=dict(film=0,placement_mm=0,rough_um=0,tilt_mrad=0,bow_um=0,mu=.3)
    f=pad(25,flat,stroke_mm=0)
    expected=EPS/2*40e-6/(25e-6/ER)**2
    assert math.isclose(float(f(0)),expected,rel_tol=1e-12)
    assert math.isclose(float(f(1e-3)),EPS/2*40e-6/(1e-3+25e-6/ER)**2,rel_tol=1e-12)
    assert math.isclose(float(pad(25,flat)(0))/expected,19.5/20,rel_tol=1e-12)
    assert math.isclose(flat_pullin(.00035,0,100,0,40e-6),math.sqrt(8*100*.00035**3/(27*EPS*40e-6)))
    # Independent grid maximization of the closed-form flat pull-in barrier.
    x=np.linspace(0,.00035,100001)
    vmax=max(np.sqrt(2*100*x*(.00035-x+25e-6/3)**2/(EPS*40e-6)))
    assert math.isclose(vmax,flat_pullin(.00035,0,100,25e-6,40e-6),rel_tol=1e-8)
    # Independent virtual-work derivative of C validates force units/sign.
    gap=10e-6;h=1e-9;v=265
    c=lambda g:EPS*40e-6/(g+25e-6/ER)
    denergy=.5*v*v*(c(gap-h)-c(gap+h))/(2*h)
    assert math.isclose(denergy,v*v*float(f(gap)),rel_tol=1e-8)
    assert float(f(1))<float(f(.1))<float(f(.001))
    convergence=[]
    for cells,steps in [(64,201),(128,401),(256,801),(512,1601)]:
        q=geometry(10,.35,.1,SCENARIOS['middle'],cells,steps)
        convergence.append(dict(cells=cells,steps=steps,pull_V=q['v_pull_selected'],
                                force_265V=q['unit_min']*265**2))
    assert abs(convergence[-1]['pull_V']/convergence[-2]['pull_V']-1)<1e-4
    assert abs(convergence[-1]['force_265V']/convergence[-2]['force_265V']-1)<1e-4
    support_check()
    return convergence


def main():
    conv=checks(); rows=population()
    summaries=[]
    for topology,address,name in it.product(['free','preclosed'],['active','half'],SCENARIOS):
        subset=[r for r in rows if (r['topology'],r['address'],r['scenario'])==(topology,address,name)]
        summaries.append(dict(topology=topology,address=address,scenario=name,count=len(subset),
                        survivors=sum(not r['reasons'] for r in subset),
                        failures=dict(Counter(x for r in subset for x in r['reasons']))))
    witnesses=[r for r in rows if r['scenario']=='tight' and r['film_um']==10
               and r['rest_gap_mm']==.35 and r['k_N_mm']==.1 and r['V']==265
               and r['residual_fraction']==.02 and r['address']=='active']
    survivors=[r for r in rows if not r['reasons']]
    result=dict(cases=len(rows),summary=summaries,witnesses=witnesses,
                convergence=conv,ledger=ledger(),support_pairs=len(support_check()),
                survivors=survivors)
    if '--check' in sys.argv:
        fine=population(512,1601)
        changes=sum(a['reasons']!=b['reasons'] for a,b in zip(rows,fine))
        assert changes==0
        result['full_grid_refinement_classification_changes']=changes
        conformal=dict(SCENARIOS['tight'],tilt_mrad=0,bow_um=0)
        g=geometry(10,.35,.1,conformal)
        result['conformal_265V_shear_N']=conformal['mu']*(265**2*g['unit_min']-g['restore_max'])
    if '--all' in sys.argv: result['cases_detail']=rows;result['support_traces']=support_check()
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
