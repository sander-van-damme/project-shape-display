import json, math
from pathlib import Path
ri,ro,alpha=1.4,1.9,math.radians(45)
r=(2/3)*(ro**3-ri**3)/(ro**2-ri**2)
k=r/math.sin(alpha)
I_old=2.21*4.16**3/12
I_new=.46*7.1**3/12
out={'evidence':'Analytical sensitivity, assumed friction and modulus; no physical measurement','cone':{'r_inner_mm':ri,'r_outer_mm':ro,'half_angle_deg':45,'uniform_pressure_R_mm':r,'uniform_wear_R_mm':(ri+ro)/2,'torque_multiplier_mm':k,'area_mm2':math.pi*(ro+ri)*(ro-ri)/math.sin(alpha),'non_self_locking_condition':'mu_axial < tan(alpha) = 1'},'assumed_effective_upper_thrust_radius_mm':1.85,'assumed_lower_thrust_radius_mm':1.8,'force_sensitivity':[],'section_ratios':{'same_width_lower_fork_EI':(2.4/1.6)**3,'notch_actual_mesh_EI_ratio':36.17283/17.85192,'spine_EI':I_new/I_old},'beam_assumptions':{'E_MPa':1500,'spine_min_width_mm':.46,'spine_height_mm':8,'spine_relieved_kernel_I_mm4':I_new,'force_per_pitch_N':.5,'pitch_mm':5.08},'simply_supported_uniform_beam_deflection_mm':{},'equalizer':{'tilt_deg':3,'geometric_height_difference_mm':5.08*math.tan(math.radians(3)),'flange_projected_height_at_tilt_mm':.72*math.cos(math.radians(3))+4.3*math.sin(math.radians(3))}}
for t in [.1,.25,.5]:
 for mu in [.15,.25,.4]:out['force_sensitivity'].append({'screw_torque_each_Nmm':t,'assumed_equal_mu':mu,'row_force_N':2*t/(mu*(k-1.85))})
for L in [25,50,100]:out['simply_supported_uniform_beam_deflection_mm'][str(L)]=5*(.5/5.08)*L**4/(384*1500*I_new)
out['adverse_friction_coefficient_Nmm_per_N']=k*.15-1.85*.4
p=Path('tools/curated-experiment-checks/E-300/analysis');p.mkdir(exist_ok=True);(p/'force-and-section.json').write_text(json.dumps(out,indent=2)+'\n')
