#!/usr/bin/env python3
"""E-158: SI-unit stationary-yield/flow and loss-volume necessary bounds.
All grids are epistemic scenarios, not fitted material/process distributions.
No B-H field solution, particle/contact simulation, CFD or hardware validation.
Stdlib only; --all emits disposable detailed scenario output.
"""
import json
import math
import sys
from itertools import product

A = math.pi * .002**2 / 4
H = .040
N = 6400
BIAS = .30
DRAG = .05


def q_slit(dp, g, length, width, mu, tau):
    """Exact infinite-width, no-slip, homogeneous Bingham slit law.
    Finite-width entrance/sidewall losses omitted: optimistic release flow.
    Cannot model carrier filtration or wall slip below yield.
    """
    if dp == 0:
        return 0.
    b = 2 * tau * length / (g * abs(dp))
    if b >= 1:
        return 0.
    factor = (1-b)**2 * (1+b/2)  # stable near b=1
    return width*g**3*dp/(12*mu*length)*factor


def q_integrated(dp, g, length, width, mu, tau, n):
    """Independent shear-rate integration, Fubini: Q=2w int_0^a s*gamma(s)ds."""
    a = g/2
    ds = a/n
    return 2*width*sum(((i+.5)*ds)*max(0., abs(dp)/length*((i+.5)*ds)-tau)
                       /mu*ds for i in range(n))*math.copysign(1, dp)


def close(x, y, rel=1e-9, absolute=1e-20):
    assert abs(x-y) <= max(absolute, rel*max(abs(x), abs(y))), (x, y)


def schedule(flow, heads, closure=.020):
    # Conditional two full strokes/group, not measured arbitrary-map performance.
    # 6 s: preparation/indexing/final proof/settle/one bounded retry allocation.
    # .05 s/group: local acquisition/reset/proof; 2 closures/group.
    if flow <= 0:
        return None
    # Generous 16-L/min board source, with perfect fair allocation granted.
    # Real shared-pump starvation needs E-108-style checking; this is a relaxation.
    flow = min(flow, (16e-3/60)/heads)
    return 6 + math.ceil(N/heads)*(2*(A*H/flow+closure)+.05)


def grid():
    # Gaps do NOT denote printable/qualified internal geometries.
    geometries = list(product([.00015,.00030,.00060], [.002,.005,.010],
                              [.05,.10,.30], [5e3,20e3,50e3]))
    summaries = []
    details = []
    for force, exponent, error, neighbor in product([1.,10.], [1.,2.],
                                                   [.02,.10,.25], [.05,.20,.50]):
        held = released = timed = 0
        fastest = None
        for g, length, mu, tau in geometries:
            # |Btarget|/Bnom <= error; |Bneighbor|/Bnom >= 1-error-neighbor.
            # tau(B)/tau_nom=(|B|/Bnom)^exponent: competing unsourced laws.
            p_hold = 2*tau*max(0.,1-error-neighbor)**exponent*length/g
            hold = p_hold > (force+BIAS)/A  # do not credit uncertain seal friction
            dp_up = .5e6-(BIAS+.10+DRAG)/A
            dp_down = (BIAS-DRAG)/A  # zero payload; explicit return bias
            q = min(q_slit(dp_up,g,length,.003,mu,tau*error**exponent),
                    q_slit(dp_down,g,length,.003,mu,tau*error**exponent))
            t = schedule(q,160)
            held += hold
            released += hold and q > 0
            timed += hold and t is not None and t < 30
            record = dict(gap_mm=g*1000,length_mm=length*1000,mu_Pas=mu,
                          tau_kPa=tau/1000,hold_kPa=p_hold/1000,
                          release_mL_s=q*1e6,time_160_s=t)
            if hold and q > 0 and (fastest is None or t < fastest['time_160_s']):
                fastest=record
            if '--all' in sys.argv:
                details.append(dict(force_N=force,exponent=exponent,error=error,
                                    neighbor=neighbor,hold=hold,**record))
        summaries.append(dict(force_N=force,exponent=exponent,error=error,
                              neighbor=neighbor,cases=len(geometries),hold=held,
                              hold_and_release=released,conditional_time=timed,
                              fastest=fastest))
    return summaries, details


def main():
    checks = {}
    g,L,w,mu,tau = .00030,.005,.003,.10,20e3
    py = 2*tau*L/g
    close(q_slit(1e5,g,L,w,mu,0),w*g**3*1e5/(12*mu*L))
    assert q_slit(0,g,L,w,mu,tau) == 0
    assert q_slit(py,g,L,w,mu,tau) == 0
    assert q_slit(py*.999,g,L,w,mu,tau) == 0
    assert q_slit(py*1.001,g,L,w,mu,tau) > 0
    for dp in [1e5,1e6,1e7]:
        close(q_slit(-dp,g,L,w,mu,tau),-q_slit(dp,g,L,w,mu,tau))
        assert 0 <= q_slit(dp,g,L,w,mu,tau) <= q_slit(dp,g,L,w,mu,0)
    exact = q_slit(1e6,g,L,w,mu,tau)
    errors = [abs(q_integrated(1e6,g,L,w,mu,tau,n)/exact-1)
              for n in [64,256,1024]]
    assert errors[-1] < errors[0]/100
    checks['quadrature_relative_errors_64_256_1024']=errors
    # Independent integral of wall stress times both walls = dp * section area.
    close((py*g/(2*L))*2*w*L,py*w*g)

    nominal=[]
    for g,L,tau in [(.00030,.005,20e3),(.00015,.010,50e3)]:
        for frac,exp in product([0.,.02,.10,.25,.50],[1.,2.]):
            q=q_slit((BIAS-DRAG)/A,g,L,w,mu,tau*frac**exp)
            nominal.append(dict(gap_mm=g*1e3,length_mm=L*1e3,tau_kPa=tau/1e3,
                                field_fraction=frac,exponent=exp,
                                hold_N=2*tau*L/g*A-BIAS,
                                down_mL_s=q*1e6,time_80_s=schedule(q,80),
                                time_160_s=schedule(q,160)))

    # Gap/length/viscosity bounds, coherent corners, no distribution.
    sensitivity=[]
    for dg,dL,dmu in product([-.00005,.00005],[-.0001,.0001],[-.03,.03]):
        gg,ll,mm=.00030+dg,.005+dL,.10+dmu
        sensitivity.append(dict(gap_mm=gg*1e3,length_mm=ll*1e3,mu_Pas=mm,
                                hold_kPa=2*20e3*ll/gg/1000,
                                ideal_down_mL_s=q_slit((BIAS-DRAG)/A,gg,ll,w,mm,0)*1e6))

    # Source dumps to ambient, cancellation coil cuts. Favorable instantaneous
    # piston force balance and constant conductance until field closes; no inertia.
    losses=[]
    for f,tclose in product([0.,.02,1.,10.],[.002,.020,1.]):
        dp=(f+BIAS-DRAG)/A
        q=q_slit(dp,.00030,.005,w,mu,0)
        loss=q*tclose/A
        losses.append(dict(payload_N=f,closure_s=tclose,unclipped_loss_mm=loss*1e3,
                           stroke_limited_loss_mm=min(H,loss)*1e3))
    # EPM retains last state: open on power loss remains conducting (counterexample).
    epm_open_empty_time=A*H/q_slit((BIAS-DRAG)/A,.00030,.005,w,mu,0)
    assert epm_open_empty_time > 0
    # A closed ideal yield plug has no translated solid coordinate, but bulk sag remains.
    compliance=[dict(K_MPa=k/1e6,sag_10N_mm=10*H/(k*A)*1000)
                for k in [10e6,100e6,1000e6]]

    # Darcy law is an alternative material model, not a perturbation of exact yield.
    # Channel wall supports grains while carrier crosses; k deliberately uncalibrated.
    seepage=[]
    for k,mu_carrier in product([1e-20,1e-18,1e-16,1e-14],[.01,.10]):
        q=k*1e-6*105e3/(mu_carrier*.001)
        seepage.append(dict(k_m2=k,mu_carrier_Pas=mu_carrier,
                            four_hour_loss_mm=q*14400/A*1000))
    kcrit=A*.0001*.01*.001/(1e-6*105e3*14400)
    # Published mass loss does not specify effluent density or uniform leak history.
    published=[]
    for rho in [.8,1.,4.]: # g/mL, explicit conversion bounds, NOT fluid-density priors
        volume_m3=.020/rho*1e-6
        published.append(dict(density_g_mL=rho,loss_24h_mm=volume_m3/A*1e3,
                              mean_nL_s=volume_m3/86400*1e12))
    # Constant-flow before closure: allowed integral, not 100-us electric pulse time.
    t_allowed=[dict(flow_mL_s=q,max_close_s=A*.0001/(q*1e-6)) for q in [.1,1.]]
    # Diagnostic proof cannot see slow drift in its short observation window.
    qlimit=A*.0001/14400
    proof_seconds=A*.00005/qlimit
    contrast=(H/.0001)*(14400/.1)*(105e3/200e3)
    half_select=[dict(exponent=m,remaining_field_fraction=.5,
                       holding_payload_N=2*20e3*.5**m*.005/.0003*A-BIAS)
                 for m in [1,2]]
    reset=[dict(packet_mm3=v*1e9,pressure_change_kPa=dp/1000,
                height_change_mm=v*dp/100e6/A*1000)
           for v,dp in product([1e-9,10e-9],[0.,.5e6])]
    # Source loss and later recovery must not be conflated with a powered stop.
    return_limits=dict(no_bias_no_payload_no_suction_flow=0.,
                       suction_minus_035N_drag_N=101325*A-.35)
    totals=dict(board_swept_L=N*A*H*1e3,minimum_L_min_at_30s=N*A*H*1e3*2,
                spring_stored_J=N*BIAS*H,PM_magnets=N,EPM_magnets=2*N,
                separate_flux_caps=2*N,resident_coils=N,coil_terminations=2*N,
                published_EPM_material_cost_2020_USD=N*7.32,
                published_cost_minus_free_EDM_caps_USD=N*(7.32-6.30),
                EPM_two_pulses_board_energy_J=2*N*.010,
                max_all_cell_purchases_at_250_shared_USD=(500-250)/N,
                ambient_suction_force_N=101325*A)
    assert totals['published_cost_minus_free_EDM_caps_USD'] > 500
    # Mass/volume conservation for every witness, independent conversion identity.
    for r in published:
        close(r['mean_nL_s']*86400*1e-12,A*r['loss_24h_mm']*.001)
    assert all(r["height_change_mm"] == 0 for r in reset
               if r["pressure_change_kPa"] == 0)
    summaries,details=grid()
    assert sum(r["cases"] for r in summaries) == 2916
    result=dict(evidence='analytical and bounded scenarios; no hardware or yield claim',
                checks=checks,nominal=nominal,manufacturing_corners=sensitivity,
                grid_count=sum(s['cases'] for s in summaries),grid=summaries,
                cut_losses=losses,EPM_open_cut_empty_time_s=epm_open_empty_time,
                compliance=compliance,Darcy=seepage,kcrit_m2=kcrit,
                published_leak_conversion=published,closure_volume_budget=t_allowed,
                diagnostic_q_limit_nL_s=qlimit*1e12,proof_at_50um_seconds=proof_seconds,
                required_conductance_ratio=contrast,half_select=half_select,
                reset_packet=reset,return_limits=return_limits,totals=totals)
    if details:result['all_cases']=details
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__ == '__main__':
    main()
