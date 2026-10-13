#!/usr/bin/env python3
"""Verify actual STL solids, signed mating, stops and optional-land clearance.
Requires numpy, trimesh, manifold3d. --pack writes a verified binary plate STL.
No physical fit, friction, stiffness, speed or print-yield claim.
"""
import argparse, json, pathlib
import numpy as np
import trimesh
import manifold3d as md

EXPECTED = {'pin':(28,28,86),'screw':(24,24,80),
 'frame_front':(70,116.2,25),'frame_back':(70,116.2,25),
 'land_front':(44,10,2),'land_back':(44,10,2),'key':(3.2,4,3.2)}

def solid(mesh):
    out=md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),
                           np.asarray(mesh.faces,dtype=np.uint32)))
    assert out.status()==md.Error.NoError, out.status()
    assert out.volume()>0
    return out

def as_mesh(s):
    a=s.to_mesh()
    return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)

def overlap(a,b):return abs((a^b).volume())

def check(folder,pack):
    solids={}; report={}
    for name,dim in EXPECTED.items():
        m=trimesh.load(folder/(name+'.stl'),force='mesh')
        assert np.allclose(m.extents,dim,atol=2e-5),(name,m.extents)
        assert abs(m.bounds[0,2])<2e-5
        s=solid(m)
        # CGAL ASCII vertices can differ in the last exported decimal. Convert
        # through float32 manifold topology, then REQUIRE watertight positive
        # winding. No hole filling, smoothing, or slicer repair is accepted.
        normalized=as_mesh(s)
        assert normalized.is_watertight and normalized.is_winding_consistent,name
        assert len(s.decompose())==1,name
        assert np.allclose(m.bounds,normalized.bounds,atol=2e-5)
        assert abs(m.volume-normalized.volume)<.001,name
        solids[name]=s
        report[name]={'mm':list(dim),'solid_mm3':round(s.volume(),3),
                      'raw_watertight':bool(m.is_watertight)}
    pin=solids['pin'].translate([0,0,-86]).rotate([180,0,0])
    screw=solids['screw'].translate([0,0,-26])
    front=solids['frame_front'].translate([-35,-86,0]).rotate([-90,0,0])
    back=solids['frame_back'].translate([-35,-30.2,0]).rotate([90,0,0])
    frame=front+back
    lands=(solids['land_front'].translate([-22,0,-18])+
           solids['land_back'].translate([-22,-10,-18]))
    key=solids['key'].translate([-1.6,-2,-1.6])
    for x,z in [(-24,10),(24,70)]:
        assert overlap(key.translate([x,0,z]),frame)<1e-5
    assert overlap(front,back)<1e-5
    assert overlap(lands,frame)<1e-5
    assert overlap(lands,screw)<1e-5
    assert overlap(screw,frame)<1e-5
    worst=0; states=0
    # Half-mm states plus incommensurate phases; off-grid endfloat changes
    # screw/nut relative phase too, rather than silently forcing coaxial fit.
    positions=sorted(set(np.linspace(2,42,81).tolist()+[2.137,21.891,41.863]))
    for q in positions:
        for float_z in [-.19999,0,.17999]:
            male=screw.rotate([0,0,-360*(q-float_z)/3]).translate([0,0,float_z])
            nut=pin.translate([0,0,q])
            v=overlap(nut,male);worst=max(worst,v)
            assert v<1e-4,(q,float_z,'thread collision',v)
            assert overlap(nut,frame)<1e-4,(q,'frame collision')
            assert overlap(male,frame)<1e-4,(q,float_z,'seat collision')
            assert q-float_z>=1.8-1e-9 and 54-(q+10-float_z)>=1.8-1e-9
            states+=1
    # Wrong rotation really collides; stops physically intercept beyond range.
    wrong=overlap(pin.translate([0,0,22.25]),screw.rotate([0,0,360*22.25/3]))
    low=overlap(pin.translate([0,0,1.9]),frame)
    high=overlap(pin.translate([0,0,42.1]),frame)
    assert wrong>1 and low>1 and high>1,(wrong,low,high)
    for f in [-.3,.3]:assert overlap(screw.translate([0,0,f]),frame)>1
    # Deliberate transverse error is a failure witness, not an FDM distribution.
    misalignment=overlap(pin.translate([.2,0,22]),screw.rotate([0,0,-360*22/3]))
    assert misalignment>0
    report['checks']={'sampled_states':states,'max_thread_overlap_mm3':worst,
        'wrong_direction_overlap_mm3':wrong,'lower_stop_overlap_mm3':low,
        'upper_stop_overlap_mm3':high,'offset_0.2_overlap_mm3':misalignment,
        'axial_float_interval_mm':[-.2,.18],'minimum_thread_margin_mm':1.8,'minimum_cap_clearance_mm':31.8}
    if pack:
        # All objects are in supplied print orientation, with generous XY gaps.
        # Pin tray is bed-down. External stop-flange supports remain necessary.
        placements=[('frame_front',(5,5,0)),('frame_back',(85,5,0)),
            ('screw',(175,20,0)),('pin',(215,20,0)),
            ('land_front',(163,55,0)),('land_back',(163,75,0)),
            ('key',(173,95,0)),('key',(183,95,0))]
        placed=[solids[n].translate(t) for n,t in placements]
        for i,a in enumerate(placed):
            for b in placed[i+1:]:assert overlap(a,b)<1e-6
        plate=md.Manifold.compose(placed)
        assert len(plate.decompose())==8
        mesh=as_mesh(plate)
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert np.all(mesh.bounds[0]>=-1e-5) and np.all(mesh.bounds[1]<256)
        mesh.export(pack,file_type='stl')
        reread=trimesh.load(pack,force='mesh')
        assert reread.is_watertight and reread.is_winding_consistent
        assert len(solid(reread).decompose())==8
        report['plate']={'bounds_mm':mesh.bounds.tolist(),'parts':8,
            'solid_mm3':plate.volume(),'file':str(pack)}
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=pathlib.Path)
    p.add_argument('--pack',type=pathlib.Path);a=p.parse_args();check(a.folder,a.pack)
