from pathlib import Path
import csv,json
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import *
OUT=Path(__file__).parent/'results';OUT.mkdir(exist_ok=True)
def save(name,rows):
 with (OUT/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
props=winding_properties();props.update(source='CALCULATION, no physical measurements',current_max_test_A=.5,
 power_03A_W=.3**2*props['resistance_20C_ohm'],power_05A_W=.5**2*props['resistance_20C_ohm'],
 stroke_mm=.6,off_lower_face_mm=-1.,on_lower_face_mm=-.4)
(OUT/'winding.json').write_text(json.dumps(props,indent=2)+'\n')
rows=[]
for g in np.linspace(-3,6,91):
 for i in [-.5,-.3,-.1,0,.1,.3,.5]:
  rows.append(dict(gap_mm=round(g,5),current_A=i,force_N=force(g/1000,i)))
save('force-position',rows)
fig,ax=plt.subplots(figsize=(8,4.7))
for i in [-.5,-.3,0,.3,.5]:
 rr=[r for r in rows if r['current_A']==i];ax.plot([r['gap_mm'] for r in rr],[1000*r['force_N'] for r in rr],label=f'{i:+g} A')
ax.axvspan(-1,-.4,alpha=.12,color='green',label='concept stroke')
ax.set(xlabel='Lower magnet face relative to winding top (mm)',ylabel='Upward force (mN)',title='Finite winding + finite Ø3 × 2 mm N48 magnet · calculation')
ax.legend(ncol=3);ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'force-position.svg');plt.close(fig)
rows=[]
for d in [2,3,4,6]:
 for t in [1,2,3]:
  # For 4/6 mm magnet enlarge bore to preserve 0.9mm radial allowance to winding.
  winding=turns(inner=max(.0024,d/2000+.0009))
  for g in [-1,-.4,.3,1,2]:
   rows.append(dict(diameter_mm=d,thickness_mm=t,gap_mm=g,current_A=-.3,
    winding_inner_diameter_mm=2*min(winding[0])*1000-.18,
    force_N=force(g/1000,-.3,d/1000,t/1000,winding=winding),**winding_properties(winding)))
save('magnet-size',rows)
save('magnet-field',[dict(distance_mm=g,axis_B_T=magnet_axis(g/1000))for g in [0,.1,.3,.5,1,2,3,5,10]])
rows=[]
for g in [.3,.9,2,3]:
 for nd in [.1,.15,.3]:
  for i in [-.5,-.3,0,.3,.5]:
   rows.append(dict(gap_mm=g,demag_factor=nd,current_A=i,**core_surrogate(g/1000,i,nd)))
save('core-sensitivity-NOT-validated',rows)
rows=[]
for p in [5.08,7.1842,10.16,15,20]:
 for dz in [0,.3,.6,1,2,5]:
  rows.append(dict(pitch_mm=p,offset_z_mm=dz,**finite_neighbor(p/1000,dz/1000)))
save('finite-neighbors',rows)
rows=[]
for i in [.1,.2,.3,.4,.5]:
 for mu in [.15,.25,.4]:
  f=min(force(-.001,-i),force(-.0004,-i))
  rows.append(dict(current_A=i,mu=mu,magnetic_force_N=f,available_torque_Nmm=1000*cone_torque(f,mu),
    power_W=i*i*props['resistance_20C_ohm']))
save('cone-torque',rows)
rows=[]
for mu in [.15,.25,.4]:
 for t in [.0596654963,.3429438473,2.1963162635]:
  unit=cone_torque(1+.0004*9.80665,mu)
  required=t/1000/unit+.0004*9.80665
  ia=required/force(-.0004,-1)
  rows.append(dict(mu=mu,required_torque_Nmm=t,required_magnetic_force_N=required,
    predicted_current_A=ia,copper_power_W=ia*ia*props['resistance_20C_ohm']))
save('required-force',rows)
theta=np.linspace(0,360,36001);rad=np.deg2rad(theta)
fig,axs=plt.subplots(2,1,figsize=(8,6),sharex=True)
for k in ['triangular','rounded','flat']:
 h=face_envelope(theta,k);t=-.03*np.gradient(h,rad)*1000
 axs[0].plot(theta,h*1000,label=k);axs[1].plot(theta,t,label=k)
 save('phase-'+k,[dict(phase_deg=float(a),separation_mm=float(b*1000),ideal_aligning_torque_Nmm=float(c))for a,b,c in zip(theta[::10],h[::10],t[::10])])
axs[0].set(ylabel='Separation (mm)',title='Six-period ideal contact envelopes; 0.03 N axial force')
axs[1].axhline(.059665,color='red',ls='--',label='E-303 light starting torque')
axs[1].axhline(-.059665,color='red',ls='--');axs[1].set(xlabel='Relative angle (degrees)',ylabel='Ideal aligning torque (N mm)')
for ax in axs:ax.grid(alpha=.2);ax.legend(loc='upper right')
fig.tight_layout();fig.savefig(OUT/'phase-envelopes.svg');plt.close(fig)
rows=[]
for active in [1,16,80,800,6400]:
 for current in [.3,.5]:
  p=active*current**2*props['resistance_20C_ohm']
  rows.append(dict(active=active,current_A=current,total_coil_current_A=active*current,
    copper_W=p,ideal_5V_input_A=p/5,pulse_energy_100ms_J=p*.1))
save('array-power',rows)
print(json.dumps(props,indent=2))

for svg in OUT.glob("*.svg"):
 svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines())+"\n")
