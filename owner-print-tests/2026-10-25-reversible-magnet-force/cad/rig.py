"""E-305 force rig; mm. CadQuery, no downloaded geometry or external CAD.
The scale, two independent wooden supports and wiring are purchased/reused items.
"""
from pathlib import Path
import cadquery as cq
import trimesh,numpy as np,json,hashlib
HERE=Path(__file__).resolve().parents[1]
def cyl(d,h,z=0,x=0):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,0,z))
def ring(od,idd,h,z=0):return cyl(od,h,z).cut(cyl(idd,h+.2,z-.1))
parts={}
# Top flange slips over barrel, glued with its underside at z=4.4.
parts['bobbin']=ring(8.4,4, .8).union(ring(4.8,4,4.4,.8))
parts['top-flange']=ring(8.4,4.9,.8)
# Large bed contact at both ends; no bridges, supports, hidden threaded parts.
parts['scale-foot']=cyl(24,2).union(cyl(10,9,2)).cut(cyl(6.4,9.1,2))
arm=cq.Workplane('XY').box(30,10,2,centered=(True,True,False))
arm=arm.union(cyl(10,8,2,10)).cut(cyl(6.4,8.1,2,10))
arm=arm.union(cyl(3,3,2,-10))
parts['magnet-arm']=arm # invert for assembly; magnet bonds to Ø3 post end
holder=cq.Workplane('XY').box(32,12,.8,centered=(False,True,False)).translate((-6,0,0))
holder=holder.union(cyl(12,1.6)).cut(cyl(7.6,2,-.1)).cut(cyl(8.6,.9,.8))
for x in [16,23]:holder=holder.cut(cq.Workplane('XY').box(2,8,2,centered=(True,True,False)).translate((x,0,-.1)))
parts['coil-bracket']=holder
parts['core-sleeve']=ring(5.8,3.2,.8).union(ring(3.9,3.2,8,.8))
layout=[];meshes=[]
positions=[(0,0),(13,0),(0,24),(32,24),(30,0),(19,45)]
for (name,part),pos in zip(parts.items(),positions):
 out=HERE/'components'/(name+'.stl');cq.exporters.export(part,str(out),tolerance=.01,angularTolerance=.1)
 mesh=trimesh.load(out,force='mesh');assert mesh.is_watertight and mesh.volume>0,name
 assert len(mesh.split())==1,name
 moved=mesh.copy();moved.apply_translation([*pos,0]);meshes.append(moved)
 layout.append(dict(name=name,position_mm=pos,bounds_mm=moved.bounds.tolist(),volume_mm3=mesh.volume,
                    sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
plate=trimesh.util.concatenate(meshes);plate.export(HERE/'components/reversible-magnet-force.stl')
(HERE/'metadata/layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(HERE/'metadata/geometry.json').write_text(json.dumps(dict(parts=len(parts),bounds_mm=plate.bounds.tolist(),
 volume_mm3=plate.volume,solid_PLA_mass_g=plate.volume*1.24/1000,all_watertight=True,
 assembly='Scale arm is inverted after printing. No force results.',
 bobbin=dict(bore=4,barrel_od=4.8,winding_length=3.6,flange_od=8.4,barrel_height=5.2),
 purchased_supports='Ø6 mm wooden dowel, nominal 80 mm; independent bench stand/wood arm'),indent=2)+'\n')
print(json.dumps(dict(parts=len(parts),bounds=plate.bounds.tolist(),solid_mass_g=plate.volume*1.24/1000)))
