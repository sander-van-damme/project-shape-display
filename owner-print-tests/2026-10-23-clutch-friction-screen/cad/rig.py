#!/usr/bin/env python3
"""E-303 normal-force screen. Units mm; CQ2.7. Run directly from any cwd.
No screw geometry re-created: this coupon isolates interface friction.
"""
from pathlib import Path
import json
import cadquery as cq
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'components';META=ROOT/'metadata'


def cylinder(d,h): return cq.Workplane('XY').circle(d/2).extrude(h)

def base():
    b=cq.Workplane('XY').rect(28,28).extrude(2).edges('|Z').fillet(2)
    return b.union(cylinder(6,5)).cut(cylinder(2.2,6))

def input_disc(od,id):
    b=cylinder(22,2)
    ring=cq.Workplane('XY').workplane(offset=2).circle(od/2).circle(id/2).extrude(2)
    b=b.union(ring).cut(cylinder(2.4,5))
    # Four broad notches identify rotating input and aid fingers; not torque calibrated.
    for x,y in [(11,0),(-11,0),(0,11),(0,-11)]:
        b=b.cut(cq.Workplane('XY').center(x,y).circle(1).extrude(2))
    return b

def follower(bore,n):
    # Functional face at bed z=0; raised central mass cup at z=1.5..4.5.
    b=cylinder(22,1.5).union(cq.Workplane('XY').box(40,5,1.5,centered=(True,True,False)))
    for x in [-20,20]:
        b=b.union(cq.Workplane('XY').center(x,0).circle(2.5).extrude(1.5))
        b=b.cut(cq.Workplane('XY').center(x,0).circle(.8).extrude(2))
    b=b.union(cq.Workplane('XY').workplane(offset=1.5).circle(8).circle(6.8).extrude(3))
    b=b.cut(cylinder(bore,6))
    # Raised tally pips off functional face; count1=tight,2=nominal,3=loose.
    for j in range(n):
        b=b.union(cq.Workplane('XY').workplane(offset=1.5).center(-2*(n-1)/2+j*2,9.3).circle(.5).extrude(.6))
    return b

def main():
    parts=[('base',base(),(0,0)),('input-47',input_disc(4.7,2.4),(30,-1)),('input-100',input_disc(10,5.4),(55,-1)),
    ('follower-tight',follower(2.2,1),(9,27)),('follower-nominal-1',follower(2.3,2),(57,27)),
    ('follower-nominal-2',follower(2.3,2),(9,53)),('follower-loose',follower(2.4,3),(57,53))]
    meshes=[];manifest=[]
    for name,part,xy in parts:
        out=OUT/(name+'.stl');cq.exporters.export(part,str(out),tolerance=.03,angularTolerance=.1)
        m=trimesh.load(out,force='mesh');assert m.is_watertight,name
        m.apply_translation([*xy,0]);meshes.append(m)
        manifest.append(dict(name=name,position_mm=list(xy),bounds_mm=m.bounds.tolist(),volume_mm3=float(m.volume),watertight=True))
    plate=trimesh.util.concatenate(meshes);plate.export(OUT/'clutch-friction-screen.stl')
    (META/'layout.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (META/'geometry.json').write_text(json.dumps(dict(units='mm',part_count=len(parts),bounds_mm=plate.bounds.tolist(),volume_mm3=float(plate.volume),estimated_solid_PLA_g=float(plate.volume*.00124),contact_rings_mm=[[4.7,2.4],[10,5.4]],force_eyelet_radius_mm=20,guide_nominal_mm=2,followers_bore_mm=[2.2,2.3,2.3,2.4],physical_status='UNTESTED'),indent=2)+'\n')
    print(json.dumps(dict(part_count=len(parts),bounds_mm=plate.bounds.tolist(),solid_PLA_g=plate.volume*.00124)))
if __name__=='__main__':main()
