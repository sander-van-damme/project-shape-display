#!/usr/bin/env python3
"""Reuse the E-295 nominal thread and capped pin mesh without rescaling.

Requires trimesh and manifold3d. The source is already exported, checked E-295
geometry: no BOSL version substitution or analytic thread approximation.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'owner-print-tests/2026-10-15-four-pin-screw-demo/four-pin-demo-0175-plate.stl'

def main():
    parts=trimesh.load(SOURCE,force='mesh').split()
    screw=next(p.copy() for p in parts if np.allclose(p.bounds,[[5.8,36.8,0],[10.2,41.2,21.5]],atol=1e-4))
    pin=next(p.copy() for p in parts if np.allclose(p.bounds,[[5.8,49.8,0],[10.2,54.2,18]],atol=1e-4))
    screw.apply_translation([-8,-39,-5.5])
    clip=trimesh.creation.box(extents=[10,10,16])
    clip.apply_translation([0,0,8])
    thread=trimesh.boolean.intersection([screw,clip],engine='manifold')
    pin.apply_translation([-8,-52,0])
    out=HERE/'cad';out.mkdir(exist_ok=True)
    data={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'thread_operation':'source screw centered x8 y39, cropped source z5.5..21.5 then translated z-5.5; exact original triangulated thread phase, no rescale',
          'pin_operation':'source closed-top pin translated x-8 y-52; unchanged geometry',
          'qualification':'E295 closed-top demo pin uses physically successful 0.175 radial thread relief; closed cap itself and guide assembly are not yet physically tested',
          'outputs':{}}
    for name,mesh in [('e295-thread',thread),('e295-pin',pin)]:
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
        path=out/(name+'.stl');mesh.export(path)
        data['outputs'][name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds_mm':mesh.bounds.tolist(),'faces':len(mesh.faces),'volume_mm3':mesh.volume,'watertight':mesh.is_watertight}
    (HERE/'validation/e295-source.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
