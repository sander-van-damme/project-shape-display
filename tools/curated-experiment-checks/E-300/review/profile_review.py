#!/usr/bin/env python3
"""Compare actual triangulated vertical-bending sections at each rotor notch.

Second moment is geometric only: layer bond, anisotropy, torsion, notch stress
and long selector supports are not qualified by this calculation.
"""
from pathlib import Path
import json,numpy as np,trimesh as tm,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
def profile(path,x):
    m=tm.load(path,force='mesh');section=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
    adjacency={}
    for e in section.entities:
        for a,b in zip(e.points[:-1],e.points[1:]):
            adjacency.setdefault(int(a),[]).append(int(b));adjacency.setdefault(int(b),[]).append(int(a))
    assert all(len(n)==2 for n in adjacency.values())
    first=next(iter(adjacency));order=[first];previous=None;current=first
    while True:
        following=next(n for n in adjacency[current] if n!=previous)
        if following==first:break
        order.append(following);previous,current=current,following
    assert len(order)==len(adjacency),'section must have one loop'
    loops=[section.vertices[order]]
    y,z=loops[0][:,[1,2]].T;yn,zn=np.roll(y,-1),np.roll(z,-1)
    cross=y*zn-yn*z;area=.5*cross.sum();cz=((z+zn)*cross).sum()/(6*area);cy=((y+yn)*cross).sum()/(6*area)
    i0=((z*z+z*zn+zn*zn)*cross).sum()/12
    j0=((y*y+y*yn+yn*yn)*cross).sum()/12
    k0=((2*y*z+y*zn+yn*z+2*yn*zn)*cross).sum()/24
    if area<0:area=-area;i0=-i0;j0=-j0;k0=-k0
    return dict(area_mm2=float(area),centroid_z_mm=float(cz),centroid_y_mm=float(cy),
                I_vertical_bending_mm4=float(i0-area*cz*cz),
                I_lateral_bending_mm4=float(j0-area*cy*cy),
                product_inertia_yz_mm4=float(k0-area*cy*cz),
                loop_vertices=len(y),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
old=profile(BASE/'E-299/cad/parts/row-selector.stl',2.5401)
new=profile(BASE/'E-300/cad/parts/row-selector-core.stl',2.5401)
record=dict(evidence='Section properties calculated from exported mesh; not measured stiffness.',
            section_x_mm=2.5401,section_note='0.0001 mm off rotor axis avoids coplanar triangulation degeneracy.',
            E299=old,E300=new,ratio_E300_to_E299=new['I_vertical_bending_mm4']/old['I_vertical_bending_mm4'],
            limitations='E299 and E300 exact rotor-notch sections only. E300 external hand paddle excluded. No FEA, orthotropic material model, creep, torsional stiffness, support-span or strength qualification.')
(HERE/'profile-review.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
