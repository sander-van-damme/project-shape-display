#!/usr/bin/env python3
"""Finite release screen; numpy/trimesh/manifold3d + OpenSCAD + pinned BOSL2.

python release.py --bosl2 PATH --output SCRATCH
All numbers are CAD intersections or explicit scenarios, never measured yield.
"""
import argparse
import json
import math
import os
from pathlib import Path
from importlib.metadata import version
import subprocess
import manifold3d as md
import numpy as np
import trimesh

REV='136e6367e65d52196a3ea51d03156f8b622c60fc'
ROOT=Path(__file__).resolve().parent

def run(cmd, **kwargs):
    p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,**kwargs)
    assert p.returncode==0,(cmd,p.stderr)
    assert not any(x in p.stderr for x in ['WARNING','ERROR']),p.stderr
    return p.stdout

def box(x0,x1,y0,y1,z0,z1):
    return md.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])

def volume(a,b): return abs((a^b).volume())

def load(path):
    m=trimesh.load(path,force='mesh')
    assert m.is_watertight and m.is_winding_consistent
    s=md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
    assert s.status()==md.Error.NoError and len(s.decompose())==1
    return s

def geometry(a):
    assert run(['git','-C',a.bosl2,'rev-parse','HEAD']).strip()==REV
    assert not run(['git','-C',a.bosl2,'status','--porcelain']).strip()
    env=dict(os.environ,OPENSCADPATH=str(a.bosl2.resolve().parent))
    result={}
    for res in [64,128]:
        for angle in [30,90]:
            solids={}
            for part in ['finished','outer']:
                path=a.output/f'{part}-{angle}-{res}.stl'
                run(['openscad','-o',path,'-D',f'part="{part}"','-D',f'angle={angle}',
                     '-D',f'$fn={res}',ROOT/'release.scad'],env=env)
                solids[part]=load(path)
            s,o=solids['finished'],solids['outer']
            assert volume(s,o)>0 and abs((s-o).volume())<1e-6
            # Axial socket pin is removed first: half molds see the filled outer.
            halves=[box(0,6,-6,6,-12,70)-o,box(-6,0,-6,6,-12,70)-o]
            offsets=[0,.02,.1,.5,1,2,4.4]
            split=[[volume(h.translate([sign*t,0,0]),s) for t in offsets]
                   for h,sign in zip(halves,[1,-1])]
            assert max(row[0] for row in split)<1e-5
            assert min(row[2] for row in split)>.001
            assert max(row[-1] for row in split)<1e-5
            # Smooth stepped outer + axial pin: controls isolate helical undercut.
            smooth=(md.Manifold.cylinder(64,1.6,1.6,res)+
                    md.Manifold.cylinder(4,1.4,1.4,res).translate([0,0,-4])+
                    md.Manifold.cylinder(6,2.2,2.2,res).translate([0,0,-10])+
                    md.Manifold.cylinder(4,.7,.7,res).translate([0,0,64]))
            for sign in [1,-1]:
                blank=box(0,6,-6,6,-12,70) if sign==1 else box(-6,0,-6,6,-12,70)
                h=blank-smooth
                assert max(volume(h.translate([sign*t,0,0]),smooth) for t in offsets)<1e-5
            pin=o-s
            assert max(volume(pin.translate([0,0,-t]),s) for t in [0,.1,1,2,3])<1e-5
            pin_lateral=volume(pin.translate([.1,0,0]),s)
            assert pin_lateral>.01
            # Separate open-ended threaded sleeve; lower end mold already removed.
            sleeve=box(-6,6,-6,6,0,68)-o
            # Faceted mesh helical invariance checked at exact angular grid steps.
            ds=sorted(set([3*i/res for i in range(res+1)]+[12,30,60,63,64,65,68]))
            down=[volume(s.rotate([0,0,-360*d/3]).translate([0,0,-d]),sleeve) for d in ds]
            wrong=volume(s.rotate([0,0,360*.375/3]).translate([0,0,-.375]),sleeve)
            up=volume(s.rotate([0,0,360*5/3]).translate([0,0,5]),sleeve)
            # No radial clearance claimed: float/export and end tessellation limits reported.
            result[f'{angle}-{res}']=dict(volume_mm3=s.volume(),split_offsets_mm=offsets,
                split_intersections_mm3=split,socket_lateral_collision_mm3=pin_lateral,
                sleeve_down_cases=len(ds),sleeve_down_max_mm3=max(down),
                sleeve_down_final_mm3=down[-1],wrong_rotation_mm3=wrong,
                collar_up_collision_mm3=up)
            assert wrong>.01 and up>1 and down[-1]<1e-5
            print(f'checked profile={angle}, facets={res}', flush=True)
    return result

def ledger(v):
    # E-279 actual 3-copy slicer totals; no optimized production plate forecast.
    rows=[]
    mold_l=(180*104*30.4-16*v)/1e6 # 13mm cover/edges, 10mm cavity pitch: assumption
    for n in [1024,4096,6400]:
        batches=math.ceil(n/16)
        cn_h=n*(4057+1571)/3/3600
        cn_l=n*(9.41+3.14)/3/1000
        handling=[3*n*t/3600+(math.ceil(n/24)+math.ceil(n/289))*5/60 for t in [10,30]]
        # E-276 installation base scaled; reference, not fine-grid compatible BOM.
        install=[10.94*n/1024,23.69*n/1024]
        cast=[]
        for yield_fraction in [1,.8]:
            b=math.ceil(n/(16*yield_fraction))
            for cure_min in [10,30,60]:
                for life in [25,100,250]:
                    molds=math.ceil(b/life)
                    attempts=16*b
                    # Mix/pour/open/reset 2..5 min/batch; four individual duties:
                    # socket-core withdraw/reset, peel/eject, gate/seam finish, gauge 10..30s each.
                    active=[handling[i]+install[i]+b*bm/60+attempts*4*t/3600+setup
                            for i,(bm,t,setup) in enumerate([(2,10,4),(5,30,12)])]
                    resin_l=attempts*v/1e6*1.5 # assumed 50% runner/mixing waste
                    # Allocation bounds, NOT sourced prices or a quote. Tool fixtures 100..500.
                    usd=[resin_l*1.05*price+molds*mold_l*1.18*silicone+fixture
                         for price,silicone,fixture in [(30,40,100),(80,80,500)]]
                    cast.append(dict(yield_fraction=yield_fraction,cure_min=cure_min,
                        life_cycles=life,batches=b,mold_sets=molds,
                        batch_occupancy_h=[b*(cure_min+bm+32*t/60)/60 for bm,t in [(2,10),(5,30)]],
                        whole_pair_serial_h=[cn_h+b*(cure_min+bm+32*t/60)/60 for bm,t in [(2,10),(5,30)]],
                        active_h=active,resin_l=resin_l,tool_rubber_l=molds*mold_l,
                        screw_process_usd=usd))
        rows.append(dict(cells=n,channel_nut_machine_h=cn_h,channel_nut_l=cn_l,
            bare_upright_pair_h=cn_h+n*640/3/3600,
            finished_screw_net_l=n*v/1e6,channel_nut_handling_h=handling,
            installation_h=install,nominal_16_batches=batches,
            resident_pieces=3*n,column_joins=n,guide_apertures=2*n,
            finished_screw_gauges=5*n, # thread, two journals, collar, socket
            socket_core_cycles=16*batches,
            extra_10s_h=n*10/3600,cast_scenarios=cast))
    # Common dimensional bias is NOT 6400 independent random failures.
    shrink=1-(1-.002)*(1-.01)
    return dict(rows=rows,mold_l_per_set=mold_l,
        sourced_nominal_combined_shrink=shrink,
        uncompensated_64mm_loss=64*shrink,uncompensated_3mm_lead_loss=3*shrink,
        differential_strain_10mm_engagement=[dict(strain=e,mismatch_mm=10*e) for e in [.002,.005,.01,.02]],
        fraction_of_bare_pair_time_due_to_bare_screw=640/(4057+1571+640),
        unscrew_turns=68/3,unscrew_seconds_at_60rpm=68/3,
        service_replacement_1percent=[dict(cells=n,pairs=math.ceil(.01*n),
            minutes_at_2_to_5=[math.ceil(.01*n)*t for t in [2,5]]) for n in [1024,4096,6400]])

def main():
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--bosl2',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    geo=geometry(a)
    report=dict(geometry=geo,ledger=ledger(geo['90-128']['volume_mm3']),bosl2=REV,
        packages={p:version(p) for p in ['numpy','trimesh','manifold3d']})
    (a.output/'summary.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(geometry=geo,ledger={k:v for k,v in report['ledger'].items() if k!='rows'}),indent=2))
if __name__=='__main__': main()
