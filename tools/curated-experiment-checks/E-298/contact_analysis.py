#!/usr/bin/env python3
"""Independent ideal ruled-crown contact envelope, not an FDM/friction solver.
Same halves face one another: D(phi)=max_r,theta(h(r,theta)+h(r,phi-theta)).
At crown mean radius every angular height is maximized, eliminating r exactly
for this ideal angular/radial linear-loft model. STEP facets differ slightly.
"""
from pathlib import Path
import json, math
import numpy as np
HERE=Path(__file__).resolve().parent
VARIANTS=[('A',.48,0),('B',.60,0),('C',.60,12)]
R=1.2; HALF_ROOT=38.; HALF_TIP=math.degrees(.30/R)/2; H=2.4

def height(theta,taper,skew):
    a=(np.asarray(theta)+90)%180-90
    # Angular boundaries move linearly with height through a radial pyramid.
    q=np.minimum((HALF_ROOT-a)/(HALF_ROOT-HALF_TIP-skew),
                 (HALF_ROOT+a)/(HALF_ROOT-HALF_TIP+skew))
    return np.where(np.abs(a)<=HALF_ROOT,H-taper+taper*np.clip(q,0,1),0)

def main():
    theta=np.arange(-90,90,.025)
    phis=np.arange(0,180,.25)
    out={'model':'Ideal angular/radial ruled crown; not exact STEP or printed contact',
         'theta_step_deg':.025,'phase_step_deg':.25,'crown_width_deg':2*HALF_TIP,
         'crown_radial_width_mm':.30,'radius_mm':R,'root_width_deg':76,
         'engaged_root_distance_mm':3.36,'variants':[]}
    for name,t,sk in VARIANTS:
        hs=height(theta,t,sk)
        D=np.array([np.max(hs+height(p-theta,t,sk)) for p in phis])
        # Brute local descent outside maximum flat and fully insertable region.
        prev=np.roll(D,1);nxt=np.roll(D,-1)
        blocked=(D>3.36+1e-8)&(prev>=D-1e-8)&(nxt>=D-1e-8)
        plateau=np.abs(D-4.8)<1e-8
        residual=blocked&~plateau
        assert not residual.any(), (name,phis[residual].tolist())
        assert abs(D.min()-2.4)<1e-7
        # Flank slopes at r=1.2 and simple one-contact Coulomb screen.
        ramps=[]
        for denom in [HALF_ROOT-HALF_TIP-sk,HALF_ROOT-HALF_TIP+sk]:
            slope=t/(R*math.radians(denom))
            ramps.append({'ramp_angle_deg':math.degrees(math.atan(slope)),
                'ideal_torque_per_axial_N_Nmm':R*slope,
                'friction_screen_torque_per_axial_N_Nmm':{
                    str(mu):R*(slope-mu)/(1+mu*slope) for mu in [.1,.2,.3,.4,.5]}})
        out['variants'].append({'variant':name,'taper_mm':t,'skew_deg':sk,
            'straight_flank_overlap_nominal_mm':1.44-2*t,
            'straight_overlap_at_old_minus_072_budget_mm':1.44-2*t-.72,
            'ideal_top_dead_center_deg':2*sk,
            'ideal_top_dead_half_width_deg':2*HALF_TIP,
            'sampled_blocked_phase_count':int(blocked.sum()),
            'sampled_additional_nonmaximum_traps':int(residual.sum()),
            'envelope_min_max_mm':[float(D.min()),float(D.max())],
            'half_selected_min_tip_gap_mm':.96,
            'full_fit_window_deg':[76,104],
            'max_nearest_window_rotation_deg':76,
            'max_nearest_window_pin_shift_at_lead3_mm':76/360*3,
            'max_biased_path_before_window_deg':min(180,76+2*sk),
            'max_biased_path_pin_shift_at_lead3_mm':(76+2*sk)/360*3,
            'one_contact_ramps':ramps,
            'phase_deg':phis.tolist(),'separation_envelope_mm':D.round(7).tolist()})
    (HERE/'contact-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
    try:
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(8.5,4.2))
        for v in out['variants']:ax.plot(v['phase_deg'],v['separation_envelope_mm'],label=f"{v['variant']}: crown {v['taper_mm']:.2f} mm, skew {v['skew_deg']}°")
        ax.axhline(3.36,c='black',ls='--',label='Both ON: root distance 3.36 mm')
        ax.set(xlabel='Relative face phase φ (degrees; upper face reflected)',ylabel='Required root separation D (mm)',xlim=(0,180),ylim=(2.2,5.0))
        ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout()
        fig.savefig(HERE/'contact-envelope.svg');fig.savefig(HERE/'contact-envelope.png',dpi=160)
    except ImportError:pass
    print(json.dumps({'variants':[{'name':v['variant'],'nominal_straight_overlap_mm':v['straight_flank_overlap_nominal_mm'],'extra_traps':v['sampled_additional_nonmaximum_traps']} for v in out['variants']]},indent=2))
if __name__=='__main__': main()
