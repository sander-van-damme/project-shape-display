#!/usr/bin/env python3
"""Transparent mechanical bounds, not material ratings or physical measurements."""
import argparse, json, math
from pathlib import Path

def leaf(E, width, thickness, length, displacement):
    # N/mm^2, mm -> N and MPa. Small-deflection cantilever, no notch factor.
    return dict(force_N=E*width*thickness**3*displacement/(4*length**3),
                stress_MPa=1.5*E*thickness*displacement/length**2)

def cantilever(E, width, thickness, length, force):
    inertia=width*thickness**3/12
    return dict(I_mm4=inertia,deflection_mm=force*length**3/(3*E*inertia))

def compute():
    rows=[]
    for grid,wall,base in [(25.4,5.08,25),(25.4,6.35,25),(25.4,.8,25),
                           (25.4,.8,25.4),(25.4,.8,24),(26.7,.8,25.4),
                           (25.4,.2,25)]:
        clear=grid-wall
        rows.append(dict(grid_mm=grid,wall_mm=wall,base_mm=base,clear_mm=clear,
                         allowance_each_side_mm=(clear-base)/2,
                         nominal_overlap=base>clear))
    # Acquisition budget for the reference section, before print/guide errors.
    transfer=dict(groove_mm=3.2,dog_mm=2.6,ground_pawl_mm=1.2,takeup_mm=.1)
    transfer['dog_backlash_mm']=transfer['groove_mm']-transfer['dog_mm']
    transfer['ground_insertion_window_mm']=transfer['groove_mm']-transfer['ground_pawl_mm']
    transfer['nominal_remaining_budget_mm']=transfer['ground_insertion_window_mm']-transfer['dog_backlash_mm']-transfer['takeup_mm']
    # Motor requirement envelope only. Gravity and drag assumptions stated.
    forces=[]
    for drag in [.01,.03,.1,.25,.5]:
        count=2048; pin_mass=0.00175; platen_mass=2; terrain_mass=5
        mass=count*pin_mass+platen_mass+terrain_mass
        f=mass*9.81+count*drag+mass*.8
        forces.append(dict(drag_N_per_site=drag,sites=count,pin_mass_kg=pin_mass,
                           platen_mass_kg=platen_mass,terrain_mass_kg=terrain_mass,
                           acceleration_m_s2=.8,lift_force_N=f,
                           belt_drum_radius_mm=8,transmission_efficiency=.8,
                           drum_torque_Nm=f*.008/.8,
                           mechanical_power_W_at_80mm_s=f*.08,
                           drum_rpm_at_80mm_s=80/(2*math.pi*8)*60))
    return dict(evidence='Assumption-based equations; no hardware qualification',
        wall_geometry=rows,reference_transfer=transfer,
        PLA_bias_leaf_3p8_by_p6_by20_at_p8=leaf(2000,3.8,.6,20,.8),
        steel_bias_leaf_3_by_p15_by10_at_p65=leaf(200000,3,.15,10,.65),
        narrowed_column_40mm_1N=cantilever(2000,5.6,2.4,40,1),
        global_force_sensitivity=forces,
        note='Force sensitivity differs from the BOM static screen by explicitly including 2 kg platen mass and acceleration. Neither is a measured force or selected motor.')

def drawings(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Circle
    cases=[(25.4,.8,25.4,'Required grid / common base\nFAIL: base intersects walls'),
           (25.4,.8,24,'Smaller-base alternative\nUnapproved product trade-off'),
           (26.7,.8,25.4,'Wider-grid alternative\nUnapproved product trade-off')]
    fig,axs=plt.subplots(1,3,figsize=(12,4.7))
    for ax,(g,t,d,title) in zip(axs,cases):
        ax.add_patch(Rectangle((-t/2,-3),t,32,color='#707d87'))
        ax.add_patch(Rectangle((g-t/2,-3),t,32,color='#707d87'))
        ax.add_patch(Circle((g/2,13),d/2,fc='#d1e5ef',ec='#1b5676',lw=1.5,alpha=.8))
        for x in [0,g]:ax.axvline(x,ls=':',c='black',lw=.7)
        ax.annotate('',(t/2,-1),(g-t/2,-1),arrowprops={'arrowstyle':'<->'})
        ax.text(g/2,-2.7,f'clear {g-t:.2f} mm',ha='center',fontsize=10)
        ax.text(g/2,13,f'base Ø{d:g}',ha='center',fontsize=10)
        ax.text(g/2,27.5,f'grid {g:g}; wall {t:g} mm',ha='center',fontsize=10)
        ax.set_title(title,fontsize=11);ax.set_aspect('equal');ax.set_xlim(-2,29);ax.set_ylim(-4,30);ax.axis('off')
    fig.suptitle('One-square corridor: pin pitch cannot change the wall-face clearance',fontsize=14)
    fig.text(.5,.02,'Nominal dimensions only. Actual base size, wall position, wall deflection and placement allowance remain necessary.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.93]);fig.savefig(output/'wall-clearance.pdf');fig.savefig(output/'wall-clearance.png',dpi=160);plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('work/des008-mechanics'));a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    result=compute()
    assert all(r['clear_mm']<r['base_mm'] for r in result['wall_geometry'][:4])
    assert abs(result['narrowed_column_40mm_1N']['deflection_mm']-1.6534391534391535)<1e-10
    (a.output/'mechanics.json').write_text(json.dumps(result,indent=2)+'\n');drawings(a.output)
    print('Wall equations, leaf/beam bounds and explicit bank-force sensitivity written; no physical pass.')
