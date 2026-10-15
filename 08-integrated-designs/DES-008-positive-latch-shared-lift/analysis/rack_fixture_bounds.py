#!/usr/bin/env python3
"""Simple beam/leaf screens for the manual article, not a finite-element or physical pass."""
import argparse,json
from pathlib import Path

def beam(load,span,width,thickness,young):
 inertia=width*thickness**3/12
 return load*span**3/(48*young*inertia)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('work/des008-rack/fixture-bounds.json'));a=ap.parse_args()
 span=64.05;loads=[.05,.1,.5];out={}
 for name,width,thick in [('old_single_rail',2.45,1.2),('new_floor_net_section',12.75,3.6),('new_lid_rail',2.45,6),('new_ground_seat_net_section',10.55,4)]:
  out[name]={'width_mm':width,'thickness_mm':thick,'inertia_mm4':width*thick**3/12,'central_point_load_deflection_mm':{str(E):{str(F):beam(F,span,width,thick,E) for F in loads} for E in [1000,2000,3000]}}
 E=2000;width=4.4;t=.6;length=20;d=1.05;I=width*t**3/12
 result={'scope':'Simply supported rectangular-beam screens; cutouts, bolted joints, layer anisotropy, torsion, actual loads and support compliance are not qualified.',
 'span_mm':span,'young_modulus_MPa_sensitivity':[1000,2000,3000], 'beam_screens':out,
 'leaf_screen':{'tip_shift_mm':d,'force_N_at_E2GPa':3*E*I*d/length**3,'root_surface_strain':1.5*t*d/length**2,'root_stress_MPa_at_E2GPa':E*1.5*t*d/length**2,'deflection_at_first_4mm':d*(3*.2**2-.2**3)/2,'caveat':'Prescribed ideal cantilever shape; head rotation, keeper moment, ledge contact, root fit, creep and fatigue remain physical tests.'},
 'nominal_clearance':{'sleeve_OD_mm':5.5,'carriage_bore_mm':5.9,'bearing_length_mm':18.4,'pitch_slope_screen':.4/18.4,'dog_nose_offset_from_axis_mm':6.95,'dog_phase_screen_mm':6.95*.4/18.4,'keeper_combined_Y_play_mm':.4,'ground_release_min_before_other_errors_mm':1.05-.4,'ground_tip_clearance_after_keeper_play_mm':1.05-.4-.45,'ground_tip_clearance_after_keeper_play_and_pin_Y_mm':1.05-.4-.45-.1},
 'root_clamp':{'non_root_underside_relief_mm':.3,'root_pad_area_mm2':3.21,'backbone_section_mm':[.85,3.7],'approx_force_N_to_deflect_one_13_55mm_anchor_span_by_relief_at_E2GPa':3*2000*(.85*3.7**3/12)*.3/13.55**3,'caveat':'Cantilever estimate only; no tightening torque specified. Confirm actual root preload before non-root faces bottom.'},
 'hardware':{'frame_bolt_mm':80,'frame_stack_mm':76,'nut_mm':2.4,'frame_thread_protrusion_mm':1.6,'carrier_bolt_mm':16,'carrier_stack_mm':12.45,'carrier_thread_protrusion_mm':1.15}}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
