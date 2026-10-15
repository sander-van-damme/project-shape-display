#!/usr/bin/env python3
"""Offline CAD checks. Regenerate STLs first using generate.py. No physical pass."""
from pathlib import Path
import hashlib, importlib.metadata, json, math, numpy as np, trimesh
HERE=Path(__file__).resolve().parent

def intersect(a,b):
    q=trimesh.boolean.intersection([a,b],engine='manifold')
    return 0.0 if q.is_empty else abs(float(q.volume))

def placed(mesh,xyz=(0,0,0),angle=0):
    m=mesh.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[0,0,1]))
    m.apply_translation(xyz)
    return m

report={'scope':'CAD meshes and ideal coaxial poses; no physical qualification',
 'packages':{n:importlib.metadata.version(n) for n in ['numpy','trimesh','manifold3d']},
 'variants':{}}
for label in ['015','0175','020']:
    mesh=trimesh.load(HERE/f'four-pin-demo-{label}-plate.stl')
    bodies=list(mesh.split(only_watertight=False))
    assert len(bodies)==12 and all(x.is_watertight and x.volume>0 for x in bodies)
    assert abs(mesh.bounds[0,2])<1e-5
    # Locate invariant bodies by their unique delivered center / dimensions.
    def bodynear(x,y): return min(bodies,key=lambda b:np.linalg.norm(b.bounds.mean(axis=0)[:2]-[x,y]))
    screw=placed(bodynear(8,39),[-8,-39,0]); pin=placed(bodynear(8,52),[-8,-52,0])
    base=placed(bodynear(13,13),[-13,-13,0])
    # Print cage maps original (x,y,z) -> (5.1-z,y,12+x), plus layout offset.
    cage=bodynear(40.85,13).copy()
    T=np.eye(4);T[:3,:3]=np.array([[0,0,1],[0,1,0],[-1,0,0]]);T[:3,3]=[-12,-13,56.1]
    cage.apply_transform(T)
    driver=placed(bodynear(55,48),[-55,-48,0])
    collisions=[]; neighbor=[]; dock=[]
    for dz in np.linspace(0,6,25):
        bottom=7.7+float(dz);phase=240-120*(bottom-10.7)
        for axial in [0,.3]:
            s=placed(screw,[0,0,1.2+axial],phase)
            p=placed(pin,[0,0,bottom+axial])
            collisions.append(intersect(s,p))
            for x in [-2.54,2.54]:
                for y in [-2.54,2.54]:
                    pp=placed(p,[x,y,0]);ss=placed(s,[x,y,0])
                    neighbor.extend([intersect(pp,cage),intersect(ss,cage),intersect(ss,base)])
        # Test a fully inserted, correctly phased manual tool; 0.1mm below roof.
        d=placed(driver,[-2.54,-2.54,-10.5],phase)
        dock.extend([intersect(d,base),intersect(d,cage)])
        for x in [-2.54,2.54]:
            for y in [-2.54,2.54]:
                ss=placed(screw,[x,y,1.2],phase if (x,y)==(-2.54,-2.54) else 0)
                dock.append(intersect(d,ss))
    assert max(collisions+neighbor+dock)<1e-5,(label,max(collisions),max(neighbor),max(dock))
    report['variants'][label]={'bodies':len(bodies),'sha256':hashlib.sha256((HERE/f'four-pin-demo-{label}-plate.stl').read_bytes()).hexdigest(),
      'bounds_mm':mesh.bounds.tolist(),
      'solid_volume_mm3':float(mesh.volume),'coaxial_screw_pin_poses':50,
      'max_thread_intersection_mm3':max(collisions),'max_frame_intersection_mm3':max(neighbor),
      'max_docked_tool_intersection_mm3':max(dock)}
report['analytic_nominal_clearances_mm']={'head_to_neighbor_min_at_opposed_journal_float':5.08-4.4-.3,
 'journal_radial':(3.5-3.2)/2,'head_axial':3.9-3.6,'guide_per_side':(4.6-4.4)/2,
 'guide_web':5.08-4.6,'top_gap_aligned':5.08-4.4,
 'conservative_top_gap_with_guidance_tilt':5.08-4.6-2*7.2*(4.6-4.4)/10.2}
(HERE/'cad-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
