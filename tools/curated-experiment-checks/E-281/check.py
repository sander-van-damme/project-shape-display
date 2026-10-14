#!/usr/bin/env python3
"""Export/check optional E-281 STLs; scratch geometry and G-code never drive a printer.
Requires numpy, trimesh, manifold3d, matplotlib; OpenSCAD, pinned BOSL2, Prusa2.7.2.
"""
import argparse, hashlib, json, os, sys
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'E-277'))
import slicing as base
from split import solid, overlap, analyze

def main():
    ap=argparse.ArgumentParser(__doc__)
    for key in ['bosl2','slicer','output','deliverables']:
        ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--reuse-cad',action='store_true',help='Use existing scratch exports from this unchanged SCAD')
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    a.deliverables.mkdir(parents=True,exist_ok=True)
    assert base.run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==base.REV
    assert not base.run(['git','-C',a.bosl2,'status','--porcelain']).strip()
    assert 'PrusaSlicer-2.7.2' in base.run([a.slicer,'--help'])
    env=dict(os.environ,OPENSCADPATH=str(a.bosl2.parent))
    pieces=[]; records=[]; solids={}
    for i,relief in enumerate([.15,.15,.15,.10,.20],1):
        for part,y in [('screw',12),('nut',32)]:
            f=a.output/f'{part}-{i}.stl'
            if not a.reuse_cad: base.run(['openscad','-o',f,'-D',f'part="{part}"','-D',f'label={i}',
                      '-D',f'relief={relief}',ROOT/'coupon.scad'],env)
            m=trimesh.load(f,force='mesh')
            assert m.is_watertight and m.is_winding_consistent and m.volume>0
            assert np.allclose(m.extents,[14,14,19] if part=='screw' else [10.3,10.3,10.4],atol=2e-5)
            assert abs(m.bounds[0,2])<1e-6
            solids[part,i]=solid(m)
            records.append(dict(part=part,label=i,relief_mm=relief,volume_mm3=m.volume))
            m.apply_translation([12+(i-1)*20,y,0]);pieces.append(m)
    plate=trimesh.util.concatenate(pieces)
    target=a.deliverables/'five-short-thread-pairs.stl'
    plate.export(target)
    loaded=trimesh.load(target,force='mesh')
    # STL float32 at plate coordinates can collapse zero-width CAD slivers.
    # Drop only geometrically degenerate facets, never fill holes or alter fits.
    keep=loaded.nondegenerate_faces()
    removed=int((~keep).sum())
    loaded.update_faces(keep); loaded.remove_unreferenced_vertices()
    loaded.export(target)
    loaded=trimesh.load(target,force='mesh')
    assert loaded.is_watertight and len(loaded.split())==10
    assert abs(loaded.volume-sum(r['volume_mm3'] for r in records))<.01
    assert np.allclose(loaded.extents,[94,32.15,19],atol=1e-4)
    # Thread-local axial origins differ by 3mm = one full lead.
    # Test the actual labeled geometry from entry down to the grip, not just
    # an infinite helical pair. Coaxial rigid samples do not prove physical fit.
    cases=[]
    for i in range(1,6):
        screw=solids['screw',i]
        for q in np.linspace(3.5,19.25,85):
            v=overlap(solids['nut',i].translate([0,0,float(q)]),
                      screw.rotate([0,0,-360*float(q)/3]))
            assert v<.001,(i,q,v)
            cases.append(v)
    wrong=overlap(solids['nut',1].translate([0,0,4.375]),
                  solids['screw',1].rotate([0,0,360*4.375/3]))
    assert wrong>.01,wrong
    slices={}
    for support in [False,True]:
        name='support-on' if support else 'support-off'
        f=a.output/(name+'.gcode')
        base.run([a.slicer,'--load',ROOT.parent/'E-277'/'slicing.ini',
                  '--threads','2','--export-gcode','--output',f,
                  *(['--support-material'] if support else []),target])
        r=analyze(f)
        assert not any(k.startswith('Support') or k in ['Overhang perimeter','Bridge infill'] for k in r['roles']),r
        # Confirm all 30 identification dots survive actual slicing.
        pp=base.paths(f)
        shift=np.array([128,128])-loaded.bounds[:,:2].mean(axis=0)
        for i in range(1,6):
            for y,z in [(12,3.4),(32,10.4)]:
                for j in range(i):
                    dot=np.array([12+(i-1)*20-3+j*1.5,y+4])+shift
                    assert any(abs(p[4]-z)<.01 and np.linalg.norm(
                        np.array([(p[0]+p[2])/2,(p[1]+p[3])/2])-dot)<.5
                        for p in pp), (name,i,y,j)
        slices[name]=r
    summary=dict(degenerate_export_facets_removed=removed,parts=records,plate_mm=loaded.extents.tolist(),
                 sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                 mating_samples=len(cases),max_overlap_mm3=max(cases),
                 wrong_sign_mm3=wrong,slices=slices)
    (a.output/'result.json').write_text(json.dumps(summary,indent=2))
    plot(pieces,a.output)
    print(json.dumps({k:v for k,v in summary.items() if k!='slices'},indent=2))
    for name,r in slices.items():print(name,r['footer'])
def plot(pieces,output):
    # Visual inspection sheet: actual mesh and actual deposited layer.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.collections import LineCollection
    fig=plt.figure(figsize=(13,8)); ax=fig.add_subplot(211,projection='3d')
    for j,m in enumerate(pieces):
        ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=['#64a8cf','#f5bb5e'][j%2],shade=True,linewidth=0))
    ax.set(xlim=(0,105),ylim=(0,43),zlim=(0,22));ax.set_box_aspect((105,43,22));ax.view_init(55,-65)
    ax.set_title('Exact STL: five screws + five nuts; raised dot counts 1–5')
    ax=fig.add_subplot(212)
    pp=[p for p in base.paths(output/'support-off.gcode') if abs(p[4]-5)<.01]
    ax.add_collection(LineCollection([[(p[0],p[1]),(p[2],p[3])] for p in pp],linewidths=.5))
    ax.autoscale();ax.set_aspect('equal');ax.set_title('Actual deposition paths at Z=5 mm; no supports')
    fig.tight_layout();fig.savefig(output/'inspection.png',dpi=160)

if __name__=='__main__':main()
