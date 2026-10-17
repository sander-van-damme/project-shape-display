#!/usr/bin/env python3
"""Engineering reproduction only; the owner opens the supplied .3mf directly.

python generate.py --bosl2 /path/BOSL2 --scratch /tmp/microstepper-cad
Requires openscad, numpy, trimesh, manifold3d, matplotlib.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import numpy as np
import trimesh
import manifold3d as md

HERE = Path(__file__).resolve().parent

def solid(m):
    s = md.Manifold(md.Mesh(np.asarray(m.vertices, dtype=np.float32),
                           np.asarray(m.faces, dtype=np.uint32)))
    assert s.status() == md.Error.NoError
    return s

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--scratch',type=Path,required=True)
    a=ap.parse_args(); a.scratch.mkdir(parents=True,exist_ok=True)
    rev=subprocess.check_output(['git','-C',str(a.bosl2),'rev-parse','HEAD'],text=True).strip()
    assert rev=='136e6367e65d52196a3ea51d03156f8b622c60fc'
    env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
    meshes={}
    for name in ('half','cup','screw','pin'):
        p=subprocess.run(['openscad','-o',str(a.scratch/f'{name}.stl'),'-D',f'part="{name}"',str(HERE/'rig.scad')],env=env,capture_output=True,text=True)
        (a.scratch/f'{name}.log').write_text(p.stdout+p.stderr)
        assert p.returncode==0 and 'ERROR' not in p.stderr and 'WARNING' not in p.stderr,p.stderr
        m=trimesh.load(a.scratch/f'{name}.stl',force='mesh')
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
        assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
        meshes[name]=m
        m.export(HERE/f'{name}.stl')
    layout=[]; pieces=[]
    for name,xy in [('half',(20,24)),('half',(64,24)),('cup',(99,10)),('screw',(99,29)),('pin',(99,47))]:
        m=meshes[name].copy(); m.apply_translation([xy[0],xy[1],0]); pieces.append(m)
        layout.append(dict(name=name,bounds_mm=m.bounds.tolist()))
    plate=trimesh.util.concatenate(pieces); plate.export(HERE/'microstepper-rig.stl')
    (HERE/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    # Restore operating coordinate system from print orientation.
    f=meshes['half'].copy(); f.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0]))
    b=f.copy(); b.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[0,0,1]))
    c=meshes['cup'].copy(); c.apply_translation([0,0,-28.8]); c.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    s=meshes['screw'].copy(); s.apply_translation([0,0,26.2])
    parts={'front':solid(f),'back':solid(b),'cup':solid(c),'screw':solid(s)}
    fixed=parts['front']+parts['back']
    collisions=[]; assembly=[f,b,c,s]
    for q in np.linspace(3,6,41):
        pin=solid(meshes['pin']).translate([0,0,float(28.6+q)])
        angle=float(-360*q/3)
        screw=parts['screw'].rotate([0,0,angle]); cup=parts['cup'].rotate([0,0,angle])
        row=dict(q_mm=float(q),pin_frame=(pin^fixed).volume(),screw_frame=(screw^fixed).volume(),cup_frame=(cup^fixed).volume(),pin_screw=(pin^screw).volume(),pin_cup=(pin^cup).volume())
        assert max(v for k,v in row.items() if k!='q_mm')<.001,row
        collisions.append(row)
    pin=meshes['pin'].copy(); pin.apply_translation([0,0,33.1]); assembly.append(pin)
    report=dict(bosl2=rev,print_body_count=5,plate_bounds_mm=plate.bounds.tolist(),parts=[dict(name=n,volume_mm3=m.volume,bounds_mm=m.bounds.tolist(),watertight=m.is_watertight) for n,m in meshes.items()],mating_positions=len(collisions),max_overlap_mm3=max(max(v for k,v in r.items() if k!='q_mm') for r in collisions),stroke_mm=3,washer=dict(ID_mm=3.2,OD_mm=7,thickness_mm=.5,Z_bottom_mm=23.7),journal_radial_clearance_mm=.25,cup_radial_socket_clearance_mm=.2,motor_radial_cradle_clearance_mm=.25,guide_side_clearance_mm=.2,axial_keeper_clearance_mm=.3,scope='Nominal CAD only. No measured torque, fit, wear or load result.',stl_sha256=hashlib.sha256((HERE/'microstepper-rig.stl').read_bytes()).hexdigest())
    (HERE/'geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    render(pieces,HERE/'plate.png',False); render(assembly,HERE/'assembly.png',True)
    print(json.dumps(report,indent=2))

def render(meshes,path,assembled):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig=plt.figure(figsize=(9,7));ax=fig.add_subplot(111,projection='3d')
    for i,m in enumerate(meshes):
        ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=['#8295a5','#aab9c5','#e8a340','#4d9d7b','#c76d57'][i],linewidth=0,alpha=.65 if assembled and i<2 else 1))
    points=np.vstack([m.vertices for m in meshes]); lo=points.min(axis=0);hi=points.max(axis=0)
    ax.set(xlim=(lo[0]-2,hi[0]+2),ylim=(lo[1]-2,hi[1]+2),zlim=(0,hi[2]+2),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
    ax.set_box_aspect(hi-lo+2);ax.view_init(25,-65)
    ax.set_title('Assembly: motor, silicone tube and washer omitted' if assembled else 'Five printable pieces; retain supplied orientation')
    fig.tight_layout();fig.savefig(path,dpi=150);plt.close(fig)

if __name__=='__main__': main()
