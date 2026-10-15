#!/usr/bin/env python3
"""Independent mechanical bounds; assumptions explicit, not hardware qualification."""
import json, math
from pathlib import Path

def stop_index_time(pitch, slots, acceleration, writer_dwell):
    return 2*(slots-1)*math.sqrt(pitch/acceleration)+slots*writer_dwell

def beam_deflection(total_load, length, modulus, width, height, wall):
    inertia=(width*height**3-(width-2*wall)*(height-2*wall)**3)/12
    return {'I_mm4':inertia,'deflection_mm':5*total_load*length**3/(384*modulus*inertia)}

def finger(modulus,width,thickness,length,lateral_load):
    inertia=width*thickness**3/12
    return {'cantilever_Euler_N':math.pi**2*modulus*inertia/(4*length**2),
            'cantilever_lateral_deflection_mm':lateral_load*length**3/(3*modulus*inertia)}

out={
 'writer_assumptions':{'pitch_mm':6.35,'slots':8,'one_way_travel_mm':44.45,'return_travel_included':False},
 'stop_index_writer_times':[
  {'acceleration_mm_s2':a,'dwell_s_per_slot':d,'seconds':stop_index_time(6.35,8,a,d)}
  for a in [1000,3000,10000] for d in [0,.02,.04]],
 'Z_beam_assumptions':{'span_mm':406.4,'uniform_total_load_N':64,'modulus_MPa':69000,'simply_supported':True},
 'Z_beams':[
  {'section_mm':[b,h,t],**beam_deflection(64,406.4,69000,b,h,t)}
  for b,h,t in [(10,10,1),(20,20,2),(30,20,2)]],
 'finger_assumptions':{'length_mm':80,'lateral_load_N':.3,'cantilever':True,'no_upper_guidance':True},
 'finger_bounds':[
  {'modulus_MPa':E,'section_mm':[b,t],**finger(E,b,t,80,.3)}
  for E in [2000,69000,200000] for b,t in [(3,1),(4,2),(4,3)]],
 'retained_head_counts':[
  {'heads':h,'writers':8*h,'flags':64*h,'binary_output_keys_AB':128*h,'compliant_readers_AB':128*h,
   'keeper_combs_AB':2*h,'bilateral_dog_channels':64*h,'ground_release_tongues':64*h}
  for h in [4,8]],
 'reliability_independent_bound':[
  {'transactions':N,'per_transaction_failure_rate':p,'probability_all_succeed':(1-p)**N}
  for N in [4096,8192] for p in [1e-3,1e-4,1e-5]]
}
Path(__file__).with_name('bounds-audit-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
