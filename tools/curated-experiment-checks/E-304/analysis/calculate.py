#!/usr/bin/env python3
"""Reproducible analytical screening. mm, N, Nmm, MPa; no measured material inputs."""
from pathlib import Path
import math,json,csv,sys,importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flexure import solve
H=Path(__file__).resolve().parent;O=H/'results';O.mkdir(exist_ok=True)
ROOT=H.parents[3]
spec=importlib.util.spec_from_file_location('e303',ROOT/'tools/curated-experiment-checks/E-303/analysis/model.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
pi=math.pi
LIGHT=1000*old.screw_scenario(.05,.01,.15,.005/1000)[0]
MODERATE=1000*old.screw_scenario(.20,.05,.30,.020/1000)[0]

def csvout(name,rows):
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def rect(b,h):return b*h,b*h**3/12,h*b**3/12
sections=[]
def add(name,A,Iy,Iz,J,E=2000,G=740,rho=.00124,EA=None,EIy=None,EIz=None,GJ=None):
 sections.append(dict(name=name,A_mm2=A,EI_vertical_Nmm2=EIy or E*Iy,EI_lateral_Nmm2=EIz or E*Iz,EA_N=EA or E*A,GJ_Nmm2=GJ or G*J,mass_g_406mm=A*406.4*rho))
def rj(a,b):
 a,b=max(a,b),min(a,b);return a*b**3*(1/3-.21*(b/a)*(1-(b/a)**4/12))
A,Iy,Iz=rect(4.6,1.6);add('flat 4.6 x 1.6 PLA',A,Iy,Iz,rj(4.6,1.6))
A,Iy,Iz=rect(4.6,10);add('solid 4.6 x 10 PLA',A,Iy,Iz,rj(4.6,10))
b=4.6;h=10;t=.8;A=b*h-(b-2*t)*(h-2*t);Iy=(b*h**3-(b-2*t)*(h-2*t)**3)/12;Iz=(h*b**3-(h-2*t)*(b-2*t)**3)/12
J=4*((b-t)*(h-t))**2/(2*(b+h-2*t)/t)
add('closed box 4.6 x 10 x .8 PLA',A,Iy,Iz,J)
A_i=2*b*t+(h-2*t)*t;Iy_i=2*(b*t**3/12+b*t*((h-t)/2)**2)+t*(h-2*t)**3/12;Iz_i=2*t*b**3/12+(h-2*t)*t**3/12;J_i=(2*b+(h-2*t))*t**3/3
add('I section 4.6 x 10 x .8 PLA',A_i,Iy_i,Iz_i,J_i)
# T: flange at top, central vertical web. Exact centroidal bending, thin-open torsion approximation.
Af=b*t;Aw=t*(h-t);zc=(Af*(h-t/2)+Aw*(h-t)/2)/(Af+Aw)
Iy_t=b*t**3/12+Af*(h-t/2-zc)**2+t*(h-t)**3/12+Aw*((h-t)/2-zc)**2
add('T section 4.6 x 10 x .8 PLA',Af+Aw,Iy_t,t*b**3/12+(h-t)*t**3/12,(b+h-t)*t**3/3)
# Chord-only axial bending upper bound; diagonal volume included. Joint/shear losses bracketed separately.
tr_A=2*4.6*.8+2*.8*math.sqrt(5.08**2+8.4**2)/5.08
tr_I=2*(4.6*.8**3/12+4.6*.8*4.6**2)
add('Warren truss chord upper bound',tr_A,tr_I,2*.8*4.6**3/12,J_i)
# Two inserted rods. Full composite ideal requires continuous shear transfer; zero-composite bound is separate.
ar=pi;ir=pi/4;z=2.9; Ecf=20000;Gcf=4000
for eta in [0,1]:
 add(f'box + two 2mm CF rods composite {eta}',A,Iy,Iz,J,EA=2000*A+2*28000*ar,EIy=2000*Iy+2*Ecf*(ir+eta*ar*z*z),EIz=2000*Iz+2*Ecf*ir,GJ=740*J+2*Gcf*(pi*2**4/32))
 sections[-1]['mass_g_406mm']=A*406.4*.00124+2*ar*406.4*.0015
for name,d,di,E,G,rho in [('CF rod 2',2,0,20000,4000,.0015),('CF rod 3',3,0,20000,4000,.0015),('CF tube 3/2',3,2,20000,4000,.0015),('glass rod 3',3,0,30000,4000,.002),('steel rod 2',2,0,200000,77000,.00785),('steel rod 3',3,0,200000,77000,.00785),('aluminium tube 3/2.1',3,2.1,69000,26000,.0027)]:
 a=pi*(d*d-di*di)/4;i=pi*(d**4-di**4)/64;add(name,a,i,i,2*i,E,G,rho)
for s in sections:
 for L in [25.4,50.8,101.6,406.4]:
  s[f'distributed_1N_cell_deflection_{L}_mm']=5*(1/5.08)*L**4/(384*s['EI_vertical_Nmm2'])
  s[f'3N_point_deflection_{L}_mm']=3*L**3/(48*s['EI_vertical_Nmm2'])
 s['local_twist_3Nmm_25mm_deg']=3*25.4/s['GJ_Nmm2']*180/pi
 s['unsupported_twist_40Nmm_406mm_deg']=40*406.4/s['GJ_Nmm2']*180/pi
 s['distributed_axial_shortening_100N_mm']=100*406.4/(2*s['EA_N'])
 s['weak_buckling_25mm_N']=pi*pi*s['EI_lateral_Nmm2']/25.4**2
 s['weak_buckling_406mm_N']=pi*pi*s['EI_lateral_Nmm2']/406.4**2
csvout('selector-sections.csv',sections)
flex=[]
for t in [.35,.40,.45]:
 for E in [1200,2000,2800]:
  s=solve(t,E=E)
  for delta in [.4,.6,.8,1.0,1.3,1.4]:flex.append(dict(thickness_mm=t,E_MPa=E,compression_mm=delta,k_N_per_mm=s['k_N_mm'],force_N=s['k_N_mm']*delta,beam_bending_stress_MPa=s['stress_MPa_per_N']*s['k_N_mm']*delta))
csvout('flexure.csv',flex)
tor=[]
for F in [.3,.6,.9,1.2]:
 for muc in [.1,.15,.2,.25,.3,.4]:
  for mut in [.1,.2,.3]:
   for radialloss in [0,.1,.25]:
    # Uniform-wear cone radius1.5. Small lower pad effective radius0.267; output thrust ring wear radius1.17.
    gross=F*muc*1.5/math.sin(pi/6);loss=F*(mut*(1.17+.267)+radialloss)
    tor.append(dict(force_N=F,cone_mu=muc,thrust_mu=mut,lateral_loss_Nmm_per_N=radialloss,gross_Nmm=gross,net_Nmm=gross-loss,light_start_margin_Nmm=gross-loss-LIGHT,moderate_start_margin_Nmm=gross-loss-MODERATE,wedging_screen=math.tan(pi/6)<=muc))
csvout('torque.csv',tor)
forces=[]
for f in [.3,1.102,1.79]:
 for mu in [.1,.2,.35]:
  slope=1.4/(2.54-.6);w=(slope+mu)/(1-mu*slope)
  for count in [1,2,80]:forces.append(dict(cell_N=f,selected_or_blocked_cells=count,mu=mu,cam_slope=slope,cam_force_N=count*f*w,shoe_friction_N=count*f*mu,total_selector_force_N=count*f*(w+mu)))
csvout('selector-forces.csv',forces)
# Independent angular height-envelope screening; no contact dynamics.
nt=1440;theta=np.linspace(0,2*pi,nt,endpoint=False);profiles={}
for name,kind in [('flat dogs','dog'),('triangular teeth','triangle'),('rounded teeth','cos'),('asymmetric ramp teeth','saw')]:
 u=(theta/(2*pi)*3)%1
 if kind=='dog':h=np.where(u<.35,1.,0.)
 elif kind=='triangle':h=1-abs(2*u-1)
 elif kind=='cos':h=.5-.5*np.cos(2*pi*u)
 else:h=np.where(u<.8,u/.8,(1-u)/.2)
 profiles[name]=np.array([np.max(h+np.roll(h[::-1],k+1)) for k in range(nt)])
phrows=[]
for k,deg in enumerate(theta*180/pi):
 row={'angle_deg':float(deg),'axisymmetric_cone_contact_lift_mm':.6}
 for name,d in profiles.items():row[name+'_envelope_mm']=d[k]
 phrows.append(row)
csvout('angular-envelopes.csv',phrows)
fig,ax=plt.subplots(1,2,figsize=(11,4))
for name,d in profiles.items():ax[0].plot(theta*180/pi,d,label=name)
ax[0].set(xlim=(0,120),xlabel='Initial relative angle (degrees)',ylabel='Required face separation (mm)',title='Representative three-tooth profiles; sampled geometry');ax[0].legend(fontsize=7)
for mu in [.15,.25,.35]:
 F=np.linspace(0,1.5,100);ax[1].plot(F,F*(3*mu-.2*(1.17+.267)-.1),label=f'cone μ={mu}')
for T,label in [(LIGHT,'E-303 light start'),(MODERATE,'E-303 moderate start')]:ax[1].axhline(T,ls='--',label=label,color='gray')
ax[1].set(xlabel='Axial clamp force per cell (N)',ylabel='Available output torque (N mm)',title='Assumed thrust μ=.20; lateral loss=.10 Nmm/N');ax[1].legend(fontsize=7)
fig.tight_layout();fig.savefig(O/'engagement-and-torque.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4))
L=np.linspace(10,120,100)
for s in sections:
 if s['name'] in ['flat 4.6 x 1.6 PLA','closed box 4.6 x 10 x .8 PLA','box + two 2mm CF rods composite 1','CF rod 2','steel rod 3']:
  ax.semilogy(L,5*(1/5.08)*L**4/(384*s['EI_vertical_Nmm2'])+3*L**3/(48*s['EI_vertical_Nmm2']),label=s['name'])
ax.axhline(.15,color='gray',ls='--');ax.set(xlabel='Actual transverse support spacing (mm)',ylabel='Deflection (mm)',title='1 N/cell distributed + separate 3 N centre obstruction, conservative sum');ax.legend(fontsize=7);fig.tight_layout();fig.savefig(O/'support-spacing.svg')
summary={'evidence':'analytical assumptions; not measurements','selected_flexure_nominal':solve(.40),'cone_half_angle_deg':30,'self_wedge_threshold_mu':math.tan(pi/6),'source_screw_scenarios':'E-303 unchanged','computed_light_start_Nmm':LIGHT,'computed_moderate_start_Nmm':MODERATE,'local_deformation_allowance_mm':.15,'allowance_reason':'.30-mm cam dwell half width and .8-mm nominal elastic preload; .15 consumes half dwell and changes nominal force by about .207 N','gross_friction_torque_per_N_at_mu025_Nmm':.75,'new_thrust_effective_radius_sum_mm':1.437,'E300_rotating_selector_thrust_radius_mm':1.85,'qualification':'No physical qualification; force/drag/creep and guide rubbing unmeasured.'}
(O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Calculated',len(sections),'sections;',len(tor),'torque cases;',len(phrows),'phases')

# Independent closed-form limit: one fixed-guided horizontal beam.
beam=solve(.4,b=3.6,E=2000,n=1,L=3.2);closed=12*2000*(3.6*.4**3/12)/3.2**3
assert abs(beam['k_N_mm']/closed-1)<1e-10
# Coordinate-grid estimate of actual core, excluding notched cam walls.
x=np.arange(-2.3,2.3,.01)+.005;z=np.arange(0,10.4,.01)+.005;X,Z=np.meshgrid(x,z)
solid=~((abs(X)<1.5)&(Z>.8)&(Z<9.6))
solid |= (abs(X)<.4)&(Z>3.3)&(Z<8.1)
for zz in [2.2,8.1]:solid |= X*X+(Z-zz)**2<1.6**2
for zz in [2.2,8.1]:solid &= X*X+(Z-zz)**2>1.1**2
a=solid.sum()*.0001;zc=(Z*solid).sum()/solid.sum()
core={'area_mm2':float(a),'centroid_z_mm':float(zc),'I_vertical_mm4':float((((Z-zc)**2)*solid).sum()*.0001),'I_lateral_mm4':float((X**2*solid).sum()*.0001),'grid_mm':.01,'one_beam_FE_vs_closed_form_relative_error':abs(beam['k_N_mm']/closed-1)}
(O/'model-checks.json').write_text(json.dumps(core,indent=2)+'\n')
# Warren-web shear and diagonal buckling, independent of chord-only EI upper bound.
a=5.08;h=8.4;l=math.hypot(a,h);Ad=2*.8;Id=2*.8**3/12;E=2000;GA=E*Ad*a*h*h/l**3;L=25.4;q=1/5.08;V=q*L/2+3/2
web={'panel_length_mm':a,'height_mm':h,'diagonal_length_mm':l,'diagonal_area_mm2':Ad,'effective_shear_rigidity_N':GA,'distributed_shear_deflection_mm':q*L*L/(8*GA),'point_shear_deflection_mm':3*L/(4*GA),'maximum_diagonal_force_N':V*l/h,'ideal_pinned_diagonal_buckling_N':math.pi**2*E*Id/l**2,'limits':'Single active diagonal; joint flexibility/print anisotropy and compression damage omitted. Add these deflections to chord bending.'}
(O/'truss-web.json').write_text(json.dumps(web,indent=2)+'\n')
manifest=ROOT/'owner-print-tests/2026-10-25-guided-matrix-clutch/metadata/meshes.json'
if manifest.exists():
 mm=json.loads(manifest.read_text());local=sum(mm[n]['volume_mm3'] for n in ['pin','output-screw','rotor','follower'])
 (O/'counts-and-material.json').write_text(json.dumps({'nominal_cells':6400,'printed_parts_per_cell':4,'local_printed_parts':25600,'purchased_local_parts':0,'local_solid_volume_mm3':local,'local_solid_mass_6400_kg':local*6400*.00124/1000,'shared_long_functional_members':480,'continuous_member_part_count_excluding_guides_and_edge_hardware':26082,'four_segment_part_count_excluding_guides_and_edge_hardware':27522,'carbon_1m_rods':80,'carbon_bulk_eur_ex_tax':80*1.95,'carbon_single_eur_ex_tax':80*3.05,'limits':'CAD solid volume; actual infill, failure rate, fixed guides, joints, drive and actuators not priced as a completed BOM.'},indent=2)+'\n')
