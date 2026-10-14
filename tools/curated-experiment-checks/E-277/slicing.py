#!/usr/bin/env python3
"""E-277 finite solids + actual PrusaSlicer paths; scratch output only.

Requires numpy, trimesh, manifold3d. Supply pinned clean BOSL2, OpenSCAD and
PrusaSlicer 2.7.2. No generated file is a qualified printer program.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess

import manifold3d as md
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent
REV = '136e6367e65d52196a3ea51d03156f8b622c60fc'
SIZES = dict(integral=(136,10.3,10.3), open=(134,10.3,10.3),
             tube=(124,10.3,10.3), nut=(10.3,10.3,10), cap=(10.3,10.3,2))
CASES = {
    'integral_auto': ('integral', []),
    'integral_transverse': ('integral', ['--bridge-angle','90']),
    'integral_longitudinal': ('integral', ['--bridge-angle','180']),
    'integral_support': ('integral', ['--support-material']),
    'integral_bed_support': ('integral', ['--support-material','--support-material-buildplate-only']),
    'open_auto': ('open', []),
    'open_support': ('open', ['--support-material']),
    'tube_auto': ('tube', []),
    'tube_support': ('tube', ['--support-material']),
    'nut_auto': ('nut', []),
    'cap_auto': ('cap', []),
}

def run(cmd, env=None):
    p = subprocess.run(list(map(str,cmd)), env=env, capture_output=True,text=True)
    assert p.returncode == 0, (cmd,p.stdout,p.stderr)
    assert not re.search(r'WARNING|ERROR|repair',p.stderr,re.I),p.stderr
    return p.stdout+p.stderr

def paths(file):
    """Positive relative-E XY segments, with role and layer Z from actual G-code."""
    content=file.read_text()
    assert 'M83' in content and 'use_relative_e_distances = 1' in content
    x=y=z=0.; role=''; result=[]
    for line in content.splitlines():
        if line.startswith(';TYPE:'): role=line[6:]
        if not re.match(r'G[01] ',line): continue
        vals={k:float(v) for k,v in re.findall(r'([XYZEF])(-?[\d.]+)',line.split(';')[0])}
        nx,ny,nz=vals.get('X',x),vals.get('Y',y),vals.get('Z',z)
        if vals.get('E',0)>0 and math.hypot(nx-x,ny-y)>1e-6:
            result.append((x,y,nx,ny,nz,role,vals['E']))
        x,y,z=nx,ny,nz
    assert result
    return result

def inspect(file, part):
    pp=paths(file); result={}
    for role in sorted({p[5] for p in pp}):
        group=[p for p in pp if p[5]==role]
        result[role]={'length_mm':round(sum(math.hypot(p[2]-p[0],p[3]-p[1]) for p in group),3),
            'extruded_mm3':round(sum(p[6] for p in group)*math.pi*1.75**2/4,3)}
    # Bodies centered at x=78; y centers=15.15,28.45,41.75. Length varies.
    x0=78-SIZES[part][0]/2
    cavity_end={'integral':134,'open':134,'tube':124}.get(part)
    cavity_start=0 if part=='tube' else 10
    cavity=[]; thread=[]; support=[]; first=[]
    for p in pp:
        mx=(p[0]+p[2])/2-x0; my=(p[1]+p[3])/2
        cy=min((15.15,28.45,41.75),key=lambda c:abs(c-my))
        if abs(my-cy)>5.15+.01: continue
        if p[4]<.201: first.append(p)
        if cavity_end and cavity_start+.5<mx<cavity_end-.5 and abs(my-cy)<4.35:
            if p[5]=='Bridge infill': cavity.append(p)
            if p[5].startswith('Support') and .8<p[4]<9.5: support.append(p)
        if part in ('integral','open') and 0<mx<10 and abs(my-cy)<1.8 and p[4]<7.2:
            if p[5] in ('Bridge infill','Overhang perimeter'): thread.append(p)
    def spans(group):
        return {'segments':len(group),
                'max_segment_mm':round(max((math.hypot(p[2]-p[0],p[3]-p[1]) for p in group),default=0),3),
                'z_mm':sorted({round(p[4],3) for p in group}),
                'direction_degrees':sorted({round(math.degrees(math.atan2(p[3]-p[1],p[2]-p[0]))%180,1) for p in group})}
    text=file.read_text()
    return dict(roles=result,cavity_bridge=spans(cavity),thread_overhang=spans(thread),
                cavity_support=spans(support),first_layer=spans(first),
                footer=[s for s in text.splitlines() if re.match(r'; (filament used|estimated printing time)',s)])

def plot(folder):
    """Plot actual extrusion paths; view layers, not a cosmetic CAD render."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    panels=[('integral_auto',9.8,'Ceiling: automatic LONG bridge'),
            ('integral_transverse',9.8,'Ceiling: transverse override'),
            ('integral_support',8.92,'Support inside closed cavity, Z=8.92'),
            ('integral_auto',6.2,'Horizontal thread, Z=6.2'),
            ('integral_auto',7.0,'Horizontal thread, Z=7.0'),
            ('nut_auto',6.4,'Separate upright nut, Z=6.4')]
    fig,axs=plt.subplots(3,2,figsize=(14,9))
    colors={'Bridge infill':'#ed8b00','Overhang perimeter':'#db3236',
            'Support material':'#7d3cb5','Support material interface':'#c589e8'}
    for ax,(case,z,title) in zip(axs.flat,panels):
        pp=[p for p in paths(folder/(case+'.gcode')) if abs(p[4]-z)<.01]
        for role in sorted({p[5] for p in pp}):
            group=[p for p in pp if p[5]==role]
            lines=[[(p[0],p[1]),(p[2],p[3])] for p in group]
            ax.add_collection(LineCollection(lines,colors=colors.get(role,'#256087'),linewidths=.65,label=role))
        ax.autoscale(); ax.set_aspect('equal'); ax.set_title(title); ax.set_xlabel('bed X (mm)'); ax.set_ylabel('bed Y (mm)')
        if 'thread' in title: ax.set_xlim(9.5,20.5); ax.set_ylim(12.8,17.5)
        if 'nut' in title: ax.set_xlim(72.5,83.5); ax.set_ylim(9.5,20.8)
    fig.suptitle('E-277 actual PrusaSlicer 2.7.2 extrusion paths — computational comparison only\nBlue: ordinary part; orange: bridge; red: overhang perimeter; purple: removable support')
    fig.tight_layout(); fig.savefig(folder/'paths.png',dpi=180); plt.close(fig)

def check_slices(summary, folder):
    """Decision witnesses, duplicate bodies, and independent filament accounting."""
    assert summary['integral_auto']['cavity_bridge']['max_segment_mm']>120
    assert summary['integral_transverse']['cavity_bridge']['max_segment_mm']<8.3
    assert summary['integral_support']['cavity_support']['segments']>1000
    assert summary['integral_bed_support']['cavity_support']['segments']==0
    assert summary['integral_transverse']['cavity_support']['segments']==0
    for case,(part,_) in CASES.items():
        r=summary[case]
        # Positive extrusion includes unretract moves only when XY also moves;
        # agreement with independent slicer footer checks that parser contract.
        cm3=float(next(s.split('=')[1] for s in r['footer'] if '[cm3]' in s))
        assert abs(sum(v['extruded_mm3'] for v in r['roles'].values())/1000-cm3)<.015
        if part=='integral':
            pp=paths(folder/(case+'.gcode'))
            for cy in (15.15,28.45,41.75):
                assert any(p[5]=='Bridge infill' and 25<(p[0]+p[2])/2<140
                           and abs((p[1]+p[3])/2-cy)<4.35 for p in pp)
    # Each short transverse ceiling span meets the sidewall vicinity; no claim
    # that nominal path proximity proves molten-polymer anchoring or sag control.
    pp=paths(folder/'integral_transverse.gcode')
    spans=[p for p in pp if p[5]=='Bridge infill' and 30<p[0]<140
           and abs(p[0]-p[2])<.002 and abs(p[3]-p[1])>8]
    assert len(spans)>700
    for p in spans:
        cy=min((15.15,28.45,41.75),key=lambda c:abs(c-(p[1]+p[3])/2))
        assert abs(abs(p[1]-cy)-4.125)<.002 and abs(abs(p[3]-cy)-4.125)<.002

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--bosl2',type=Path,required=True)
    ap.add_argument('--slicer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--analyze-only',action='store_true')
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    assert 'PrusaSlicer-2.7.2' in run([a.slicer,'--help'])
    report={}
    if not a.analyze_only:
        assert run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==REV
        assert not run(['git','-C',a.bosl2,'status','--porcelain']).strip()
        env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
        meshes={}
        for part,dim in SIZES.items():
            file=a.output/(part+'.stl')
            log=run(['openscad','-o',file,'-D',f'part="{part}"',ROOT/'slicing.scad'],env)
            (a.output/(part+'-cad.log')).write_text(log)
            mesh=trimesh.load(file,force='mesh')
            assert np.allclose(mesh.extents,dim,atol=2e-5),(part,mesh.extents)
            assert np.allclose(mesh.bounds[0],0,atol=2e-5)
            s=md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
            assert s.status()==md.Error.NoError and len(s.decompose())==1
            mm=s.to_mesh()
            mesh=trimesh.Trimesh(np.asarray(mm.vert_properties)[:,:3],np.asarray(mm.tri_verts),process=True)
            assert mesh.is_watertight and mesh.is_winding_consistent
            meshes[part]=mesh
            if part=='integral':
                gross=136*10.3**2-124*8.7**2
                assert gross-10*math.pi*1.75**2 < mesh.volume < gross-10*math.pi*.85**2
            report[part]={'solid_mm3':round(s.volume(),6),'bounds_mm':mesh.bounds.tolist()}
            copies=[]
            for i in range(3):
                m=mesh.copy(); m.apply_translation([78-dim[0]/2,10+i*13.3,0]); copies.append(m)
            plate=trimesh.util.concatenate(copies)
            ps=md.Manifold(md.Mesh(np.asarray(plate.vertices,dtype=np.float32),np.asarray(plate.faces,dtype=np.uint32)))
            assert ps.status()==md.Error.NoError and len(ps.decompose())==3
            plate.export(a.output/(part+'-three.stl'))
        # Same analytic decomposition; ASCII/float32 mesh roundoff <.01 mm3.
        assert abs(meshes['integral'].volume-meshes['open'].volume-meshes['cap'].volume)<.01
        assert abs(meshes['integral'].volume-sum(meshes[p].volume for p in ('tube','nut','cap')))<.01
        (a.output/'geometry.json').write_text(json.dumps(report,indent=2))
        for case,(part,options) in CASES.items():
            out=a.output/(case+'.gcode')
            log=run([a.slicer,'--load',ROOT/'slicing.ini','--threads','2','--center','78,28.45',
                     '--export-gcode','--output',out,*options,a.output/(part+'-three.stl')])
            (a.output/(case+'.log')).write_text(log)
            print(case,flush=True)
    summary={case:inspect(a.output/(case+'.gcode'),part) for case,(part,_) in CASES.items()}
    check_slices(summary,a.output)
    summary['provenance']={'bosl2':REV,'slicer':run([a.slicer,'--help']).splitlines()[0],
        'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'slicing.scad',ROOT/'slicing.ini',ROOT.parent/'E-263'/'article.scad']}}
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2))
    plot(a.output)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
