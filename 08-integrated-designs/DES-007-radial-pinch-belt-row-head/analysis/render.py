#!/usr/bin/env python3
"""Render actual exported meshes, simplified ONLY for visualization."""
import argparse,math
from pathlib import Path
import trimesh,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from check_geometry import moved

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();b=args.build;out=args.output;out.mkdir(parents=True,exist_ok=True)
 def raw(n):return trimesh.load_mesh(b/(n+'-raw.stl'))
 parts=[]
 for z in (0,15):
  for r in range(3):parts.append((moved(raw(f'upper_{r}'),(0,0,z)),'#b9c8cf'))
 for name,z in [('foot',-30),('keeper',20.2),('guide',34),('guide',44),('roof',53.2),('head',-25),('head_cover',-20.8)]:parts.append((moved(raw(name),(0,0,z)),'#8eb6a0' if 'head' in name else '#cbd3d7'))
 posts=[(-9,-7),(-9,17),(-9,3.175),(28.05,-7),(28.05,17),(28.05,3.175)]
 for x,y in posts:
  for z,h in [(-27,27),(3,12),(18,2.2),(21.8,12.2),(36,8),(46,7.2)]:parts.append((moved(raw(f'spacer_{h:g}'),(x,y,z)),'#cbd3d7'))
 for row in (0,1):
  screw=trimesh.load_mesh(b/f'bare_screw_{row}.stl')
  for x in np.arange(4)*6.35:
   parts.append((moved(screw,(x,row*6.35,0),angle=-240),'#d29a4b'))
   parts.append((moved(raw('pin'),(x,row*6.35,25)),'#78b7cc'))
 tip=raw('shoe_tip');tip.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
 for x in np.arange(4)*6.35:
  parts.append((moved(raw('shoe_base'),(x,-4.4,-24)),'#ab94c1'));parts.append((moved(tip,(x,-4.4,-24)),'#ab94c1'))
  stem=trimesh.creation.cylinder(radius=.4,height=18.8);stem.apply_translation([x+3.175,-4.4,-13.6]);parts.append((stem,'#616d78'))
 for x in np.arange(5)*6.35-3.175:
  wire=trimesh.creation.cylinder(radius=.5,height=23.8);wire.apply_translation([x,-2.3,-12.9]);parts.append((wire,'#616d78'))
 for azim,label in [(-70,'front'),(-130,'side')]:
  fig=plt.figure(figsize=(9,10));ax=fig.add_subplot(projection='3d')
  for m,c in parts:
   if len(m.faces)>1200:m=m.simplify_quadric_decimation(face_count=1200)
   coll=Poly3DCollection(m.triangles,facecolor=c,edgecolor='none',alpha=1);ax.add_collection3d(coll)
  ax.set(xlim=(-16,35),ylim=(-24,24),zlim=(-32,58),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((51,48,90));ax.view_init(elev=18,azim=azim)
  ax.set_title('DES-007 nominal bench assembly\nActual CAD meshes; steel links shown; tape and bolts omitted for visibility')
  fig.savefig(out/f'cad-{label}.png',dpi=150);plt.close(fig)
 print('Rendered actual meshes; no physical hardware photographed.')
if __name__=='__main__':main()
