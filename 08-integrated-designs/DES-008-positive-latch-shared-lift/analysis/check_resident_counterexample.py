#!/usr/bin/env python3
"""A deterministic admitted-clearance counterexample, independent of A's checks.

The counterexample uses perfect nominal solids with rigid play inside the given
guide clearances. It does not assume a printing error, force, wear or deformation.
"""
import argparse,hashlib,json,subprocess,warnings
from pathlib import Path
import numpy as np
import trimesh

parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'cad/resident_cell.scad')
parser.add_argument('--output',type=Path,default=Path('work/des008-resident-counterexample'))
args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
expected='780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157'
digest=hashlib.sha256(args.source.read_bytes()).hexdigest()
assert digest==expected, 'Counterexample source changed; review it before reusing conclusions.'

def load(part):
    target=args.output/(part+'.stl')
    subprocess.run(['openscad','-o',str(target),'-D',f'part="{part}"',str(args.source)],capture_output=True,check=True)
    return trimesh.load(target,force='mesh')
meshes={name:load(name) for name in ['dog','channel','dog_guide','pin','writer_pair']}
def intersection(a,b):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        return trimesh.boolean.intersection([a,b],engine='manifold')
def intersection_volume(a,b):
    m=intersection(a,b)
    return 0.0 if m.is_empty else float(abs(m.volume))

angle_deg=-4.0
origin=np.array([3.,-2.2,-30.4])
translation=np.array([-.08175086979335999,.04879836891098147,0.])
theta=np.deg2rad(angle_deg)
rotation=np.array([[np.cos(theta),-np.sin(theta),0],
                   [np.sin(theta),np.cos(theta),0],[0,0,1]])
played=meshes['dog'].copy()
played.vertices=(played.vertices-origin)@rotation.T+origin+translation
collision=intersection(played,meshes['pin'])
actual={name:intersection_volume(played,meshes[name]) for name in ['channel','dog_guide','pin']}
nominal={name:intersection_volume(meshes['dog'],meshes[name]) for name in ['channel','dog_guide','pin']}
assert max(nominal.values())<1e-6
assert actual['channel']<1e-6 and actual['dog_guide']<1e-6
assert actual['pin']>.05
played.export(args.output/'admitted-yaw-dog.stl')
collision.export(args.output/'rack-intersection.stl')

# This is an independent packaging warning for two abutting, unmirrored banks.
# A two-row representative's next-bank first pin is atY=2*pitch. The far end
# of its paired link occupies the next bank; the mirrored/relocated alternative
# is not supplied as a completed design and is not disproved by this example.
next_pin=meshes['pin'].copy();next_pin.apply_translation([6.35,12.7,0])
bank_collision=intersection_volume(meshes['writer_pair'],next_pin)

result={
 'source_sha256':digest,
 'claim':'The current dog-guide embodiment fails clearance-based engagement isolation.',
 'rotation_degrees_about_Z':angle_deg,'rotation_origin_mm':origin.tolist(),
 'translation_mm':translation.tolist(),
 'nominal_intersection_mm3':nominal,'admitted_play_intersection_mm3':actual,
 'toe_max_Y_mm':float(played.vertices[played.vertices[:,0]<1.4,1].max()),
 'groove_back_Y_mm':-.55,
 'abutting_unmirrored_bank_next_pin_intersection_mm3':bank_collision,
 'limits':'No claim of physical testing or universal topology failure. Self-alignment, preload, longer guides, changed slots or mirrored banks require their own design and qualification.'
}
(args.output/'counterexample.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,2,figsize=(11,5))
def draw_section(ax,mesh,colour,width=1,label=None):
    sec=mesh.section(plane_origin=[0,0,-30.4],plane_normal=[0,0,1])
    if sec is None:return
    for i,entity in enumerate(sec.entities):
        line=sec.vertices[entity.points]
        ax.plot(line[:,0],line[:,1],color=colour,lw=width,label=label if i==0 else None)
for ax in axes:
    draw_section(ax,meshes['pin'],'#536171',1.7,'Terrain rack')
    draw_section(ax,meshes['channel'],'#cc8c22',1.5,'C-channel')
    draw_section(ax,meshes['dog_guide'],'#267d97',1.5,'Dog guide')
    draw_section(ax,meshes['dog'],'#9b9fa5',1,'Centred dog')
    draw_section(ax,played,'#bf2637',1.7,'Admitted yaw')
    draw_section(ax,collision,'#d00000',3,'Rack overlap')
    ax.set_aspect('equal');ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.grid(alpha=.2)
axes[0].set_xlim(-1.6,4.0);axes[0].set_ylim(-3.6,1.4)
axes[0].set_title('Perfect solids, permitted guide play')
axes[1].set_xlim(.1,1.5);axes[1].set_ylim(-1.4,-.35)
axes[1].set_title('Rack collision: 0.10135 mm³')
axes[0].legend(loc='upper right',fontsize=8)
fig.suptitle('DES-008 engagement-clearance counterexample: −4° yaw, no guide/channel overlap',fontsize=12)
fig.tight_layout()
fig.savefig(args.output/'admitted-yaw-counterexample.png',dpi=180)
fig.savefig(args.output/'admitted-yaw-counterexample.pdf')
