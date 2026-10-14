#!/usr/bin/env python3
"""One manufacturing-oriented thread against E-277's retained control.

Same pinned dependencies/profile as slicing.py. Generated data are scratch only.
No print, load, friction, fit-yield or speed qualification.
"""
import argparse
import json
import math
import os
from pathlib import Path

import numpy as np
import trimesh
import slicing as base
from split import solid, mesh, analyze, overlap

ROOT = Path(__file__).resolve().parent


def mechanics():
    # Derived from the exact trapezoidal profile in pinned BOSL2.
    # V-thread surrogate including helix-angle correction from Douglas Wright's
    # DANotes (Cambridge mirror), threads/mechanics/mechanics.html. Nominal mean
    # diameter, rigid flank contact; no collar, preload, FDM roughness or creep.
    result = {}
    for angle in [30, 90]:
        a = math.radians(angle/2)
        depth, lead, mean_d = .9, 3., 2.3
        flat = lead/2-depth*math.tan(a)
        assert flat > 0
        tan_lam = lead/(math.pi*mean_d)
        lam = math.atan(tan_lam)
        wedge = math.sqrt(1+(math.cos(lam)*math.tan(a))**2)
        result[str(angle)] = dict(
            half_angle_deg=angle/2, male_core_d_mm=1.4,
            female_minor_d_mm=1.7, crest_and_root_flat_mm=flat,
            radial_step_per_point2_layer_mm=.2/math.tan(a),
            axial_gap_per_flank_from_point15_relief_mm=.15*math.tan(a),
            helix_angle_deg=math.degrees(math.atan(tan_lam)),
            small_lead_self_lock_mu_threshold=tan_lam*math.cos(a),
            helix_corrected_self_lock_mu_threshold=tan_lam/wedge,
            axial_section_radial_to_axial_normal_force_ratio=math.tan(a),
            effective_friction_multiplier=wedge,
            raising_torque_Nmm_at_point2N={str(mu):
                .2*mean_d/2*(tan_lam+mu*wedge)/
                (1-mu*wedge*tan_lam) for mu in [.1,.3,.5]})
    # Independent half-angle limits of the elementary force triangle.
    assert math.isclose(result['90']['axial_section_radial_to_axial_normal_force_ratio'],1)
    for r in result.values():
        lam=math.radians(r['helix_angle_deg'])
        for mu,torque in r['raising_torque_Nmm_at_point2N'].items():
            direct=.2*1.15*math.tan(lam+math.atan(
                float(mu)*r['effective_friction_multiplier']))
            assert abs(torque-direct)<1e-14
        assert abs(math.tan(lam)-r['helix_corrected_self_lock_mu_threshold']*
                   r['effective_friction_multiplier'])<1e-14
    return result


def finite_mating(nut, male):
    # Opposite rotation of resident screw permits positive nut translation.
    # 0..3 mm samples span one turn; large endpoints also test S50 reach.
    qs = sorted(set([2+i/16 for i in range(49)]+[12.125,27.375,51.875,52]))
    results = {}
    for offset in [0,.2]:
        values = [overlap(nut.translate([offset,0,q]),
                          male.rotate([0,0,-360*q/3])) for q in qs]
        results[str(offset)] = dict(cases=len(values),minimum_mm3=min(values),
                                   maximum_mm3=max(values))
    assert results['0']['maximum_mm3'] < .001
    # Wrong helical sign is a negative control, not an acceptable assembly.
    wrong = overlap(nut.translate([0,0,2.375]),male.rotate([0,0,360*2.375/3]))
    assert wrong > .01
    return dict(offsets=results,wrong_sign_overlap_mm3=wrong)


def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--slicer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    cases=[(angle,layer,support) for angle in [30,90]
           for layer in [.2,.1] for support in [False,True]]
    if not a.analyze_only:
        assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==base.REV
        assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
        env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
        geo={}
        for angle in [30,90]:
            solids={}
            for part in ['nut','male']:
                path=a.output/f'{part}-{angle}.stl'
                base.run(['openscad','-o',path,'-D',f'part="{part}"',
                          '-D',f'angle={angle}',ROOT/'thread_profile.scad'],env)
                solids[part]=solid(trimesh.load(path,force='mesh'))
            nut_mesh=mesh(solids['nut'])
            assert np.allclose(nut_mesh.extents,[10.3,10.3,10],atol=2e-5)
            if angle==30:
                assert abs(solids['nut'].volume()-1002.0892853)<.001
            assert np.allclose(mesh(solids['male']).extents,[3.2,3.2,64],atol=2e-5)
            copies=[]
            for i in range(3):
                m=nut_mesh.copy(); m.apply_translation([15.15,15.15+i*13.3,0])
                copies.append(m)
            trimesh.util.concatenate(copies).export(a.output/f'three-{angle}.stl')
            geo[str(angle)]=dict(nut_mm3=solids['nut'].volume(),
                male_mm3=solids['male'].volume(),
                mating=finite_mating(solids['nut'],solids['male']))
            print('geometry',angle,flush=True)
        (a.output/'geometry.json').write_text(json.dumps(geo,indent=2))
        for angle,layer,support in cases:
            name=f'a{angle}-l{layer}-s{int(support)}'
            base.run([a.slicer,'--load',ROOT/'slicing.ini','--threads','2',
                      '--layer-height',layer,'--first-layer-height',layer,
                      '--export-gcode','--output',a.output/f'{name}.gcode',
                      *(['--support-material'] if support else []),
                      a.output/f'three-{angle}.stl'])
            print(name,flush=True)
    slices={f'a{angle}-l{layer}-s{int(support)}':
            analyze(a.output/f'a{angle}-l{layer}-s{int(support)}.gcode')
            for angle,layer,support in cases}
    result=dict(geometry=json.loads((a.output/'geometry.json').read_text()),
                mechanics=mechanics(),slices=slices,
                cleanup_hours_if_avoided={str(n):[n*t/3600 for t in [10,30,60]]
                                         for n in [1024,4096,6400]})
    (a.output/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
