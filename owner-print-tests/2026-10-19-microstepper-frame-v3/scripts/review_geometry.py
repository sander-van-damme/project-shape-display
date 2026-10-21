"""Audit corrected v3 meshes against measured motor; exit 2 means not releasable.
Unknown appendages are NOT replaced by invented solids or marked collision-free.
"""
import hashlib
import json
import sys
import numpy as np
import trimesh
import manifold3d as md
from paths import COMPONENTS, METADATA, TEST_DIR


def load(n):
    return trimesh.load(COMPONENTS / (n + '.stl'), force='mesh')


def solid(m):
    return md.Manifold(md.Mesh(np.asarray(m.vertices, dtype=np.float32),
                              np.asarray(m.faces, dtype=np.uint32)))


def rot(m, a, axis=(0, 0, 1)):
    m = m.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(a), axis))
    return m


def move(m, v):
    m = m.copy()
    m.apply_translation(v)
    return m


basis = json.loads((METADATA / 'motor-interface.json').read_text())
assert basis['body_height_mm'] == 9.2
assert basis['motor_base_z_mm'] == 2
front = rot(move(load('front'), [0, 0, -6.5]), 90, [1, 0, 0])
back = rot(move(load('back'), [0, 0, -6.5]), 90, [1, 0, 0])
# Proper rigid transforms only: a printed part cannot be reflected.
back = rot(back, 180)
assembly_rotation = (trimesh.transformations.rotation_matrix(np.pi,[0,0,1]) @
                     trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
assert abs(np.linalg.det(assembly_rotation[:3,:3])-1)<1e-12
f, b = solid(front), solid(back)
frame = f + b
rotor_z = basis["rotor_z_mm"]
shift = basis["upper_shift_mm"]
rotor = move(load('rotor'), [0, 0, rotor_z])
washer = (md.Manifold.cylinder(.5, 3.5, 3.5, 256) -
          md.Manifold.cylinder(.5, 1.6, 1.6, 256)).translate([0, 0, basis["ring_bottom_z_mm"]])
checks = []
for diameter in [basis['body_diameter_nominal_mm'], basis['drawing_max_diameter_mm']]:
    body = md.Manifold.cylinder(basis['body_height_mm'], diameter/2, diameter/2, 256).translate([0, 0, 2])
    checks.append(dict(diameter_mm=diameter, height_mm=9.2, bottom_z_mm=2, top_z_mm=11.2,
                       front_collision_mm3=(body ^ f).volume(), back_collision_mm3=(body ^ b).volume(),
                       rotor_collision_mm3=(body ^ solid(rotor)).volume(),
                       ring_collision_mm3=(body ^ washer).volume()))
# Exact lip and wire shapes remain unknown; expanded envelopes are checked below.
body = md.Manifold.cylinder(9.2, 4, 4, 256).translate([0, 0, 2])
long_pin_mesh = load('pin-50')
long_rotor = move(load('rotor-long'), [0, 0, rotor_z])
assert abs(long_pin_mesh.bounds[1,2]-50)<1e-4
# This solid sweep bounds all square pin upper sections from 18 through 50 mm
# over the whole 3 mm stroke plus 0.3 mm lift (continuous frame clearance).
guide_sweep = md.Manifold.cube([4.4,4.4,81.2-33.9]).translate([-2.2,-2.2,33.9])
assert abs((guide_sweep ^ frame).volume())<1e-4
# Demonstrate the old unmirrored printed back cannot assemble by rotation.
legacy_back=trimesh.load(COMPONENTS/'archive/2026-10-20-before-handedness-fix/back.stl',force='mesh')
legacy_back=rot(rot(move(legacy_back,[0,0,-6.5]),90,[1,0,0]),180)
old_hand_error=(solid(legacy_back)^f).volume()
assert old_hand_error>1, old_hand_error
assert abs((f^b).volume())<1e-4
rows = []
for lift in [0, .3]:
    for angle in range(361):
        r = solid(move(rot(rotor, -angle), [0, 0, lift]))
        lr = solid(move(rot(long_rotor, -angle), [0, 0, lift]))
        p = solid(move(load('pin'), [0, 0, 27.2 + shift + 3*angle/360 + lift]))
        long_p = solid(move(long_pin_mesh, [0,0,27.2+shift+3*angle/360+lift]))
        rows.append(dict(angle_deg=angle, lift_mm=lift,
                         long_rotor_frame_mm3=(lr ^ frame).volume(),
                         long_rotor_long_pin_mm3=(lr ^ long_p).volume(),
                         long_pin_frame_mm3=(long_p ^ frame).volume(),
                         long_pin_rotor_mm3=(long_p ^ r).volume(),
                         rotor_frame_mm3=(r ^ frame).volume(),
                         pin_frame_mm3=(p ^ frame).volume(), rotor_pin_mm3=(r ^ p).volume()))
maxima = {k: max(row[k] for row in rows) for k in rows[0] if k.endswith('mm3')}
spacers = []
for t, n in [(.60, 'spacer-060'), (.72, 'spacer-072'), (.84, 'spacer-084')]:
    shim = solid(move(rot(load(n), 90, [0, 1, 0]), [4.7-t, -1, 3]))
    spacers.append(dict(name=n, frame_collision_mm3=(shim ^ frame).volume(),
                        body_interference_mm3=(shim ^ body).volume(), tangent_width_mm=8.8-t))
old = trimesh.load(TEST_DIR.parent / '2026-10-18-microstepper-frame-v2/components/screw.stl', force='mesh')
clip = md.Manifold.cube([10, 10, 16.001]).translate([-5, -5, 24.20001+shift])
a = solid(move(old, [0, 0, 21.8+shift])) ^ clip
c = solid(rotor) ^ clip
long_old = trimesh.load(TEST_DIR.parent/'2026-10-18-microstepper-frame-v2/components/screw-long.stl',force='mesh')
long_clip = md.Manifold.cube([10,10,48.001]).translate([-5,-5,24.90001])
long_a = solid(move(long_old,[0,0,22.5])) ^ long_clip
long_c = solid(long_rotor) ^ long_clip
long_thread_difference = (long_a-long_c).volume()+(long_c-long_a).volume()
assert long_thread_difference < 1e-4
# Same coupling and load-bearing body for both lengths.
base_clip = md.Manifold.cube([20,20,11.999]).translate([-10,-10,rotor_z])
short_base, long_base = solid(rotor)^base_clip, solid(long_rotor)^base_clip
base_difference = (short_base-long_base).volume()+(long_base-short_base).volume()
assert base_difference < 1e-4
pcb = md.Manifold.cube([3.5, 7, 4]).translate([-6, -3.5, 4])
# Expanded glue/wire/flange envelopes are design allowances, not measured maxima.
glue = md.Manifold.cube([3.5, 7.8, 2]).translate([-6, -3.9, 2])
wire_z = basis['pcb_solder_wire_envelope_mm']['wire_z']
wire = md.Manifold.cube([2.6, 8, wire_z[1]-wire_z[0]]).translate([-7, -4, wire_z[0]])
flange = md.Manifold.cylinder(1.2, 5.1, 5.1, 256).translate([0, 0, 10])
boss = md.Manifold.cylinder(.25, 1.5, 1.5, 128).translate([0, 0, 11.2])
shaft = md.Manifold.cylinder(3.35, .4, .4, 96).translate([0, 0, 11.2])
gear = md.Manifold.cylinder(1.25, 1.1, 1.1, 128).translate([0, 0, 13.2])
complete = body + flange + boss + shaft + gear + pcb + glue + wire
appendages = {name: {'frame_mm3': (m ^ frame).volume(),
                    'ring_mm3': (m ^ washer).volume(),
                    'rotor_mm3': (m ^ solid(rotor)).volume()}
              for name, m in [('pcb',pcb),('glue_allowance',glue),('wire_allowance',wire),
                              ('flange_allowance',flange),('boss',boss),('shaft',shaft),('gear_outer_envelope',gear)]}
# Only gear cylinder penetration into C-ribs is intentional: tooth profile unknown.
assert all(max(abs(v) for k,v in vals.items() if not (name=='gear_outer_envelope' and k=='rotor_mm3')) < 1e-4
           for name, vals in appendages.items()), appendages
assert max(maxima.values()) < 1e-4, maxima
assert all(max(abs(c['front_collision_mm3']),abs(c['back_collision_mm3'])) < 1e-4 for c in checks), checks
# Small penetrations test that surfaces actually meet, unlike zero-volume tangency.
report = dict(status=basis['status'], scope='Corrected L design: measured body/boss/shaft, PCB and expanded glue/wire/lip envelopes; approximate gear outer cylinder' ,
              assembly_rotation_determinant=float(np.linalg.det(assembly_rotation[:3,:3])), legacy_back_rigid_assembly_collision_mm3=old_hand_error, pin_lengths_checked_mm=[18,50], screw_lengths_mm=[28,60], long_screw_only_with_pin_mm=50, long_thread_symmetric_difference_mm3=long_thread_difference, coupling_body_symmetric_difference_mm3=base_difference, guide_sweep_collision_mm3=(guide_sweep^frame).volume(), guide_z_mm=[32.7,72.7], long_pin_tip_z_mm=[77.9,80.9], motor=checks, appendage_checks=appendages, complete_motor_frame_collision_mm3=(complete ^ frame).volume(), unknown_motor_fields=[k for k, v in basis.items() if v is None and k.endswith('_mm')],
              measured_pcb_envelope_collision_mm3=(pcb ^ frame).volume(),
              sampled_poses=rows, max_collision_mm3=maxima, spacers=spacers,
              frame_half_collision_mm3=(f ^ b).volume(),
              thread_symmetric_difference_mm3=(a-c).volume()+(c-a).volume(),
              ring_frame_collision_mm3=(washer ^ frame).volume(),
              ring_rotor_collision_mm3=(washer ^ solid(rotor)).volume(),
              ring_lower_contact_probe_mm3=(washer.translate([0, 0, -.001]) ^ frame).volume(),
              ring_upper_contact_probe_mm3=(washer ^ solid(move(rotor, [0, 0, -.001]))).volume(),
              upward_stop_at_030_mm3=(solid(move(rotor, [0, 0, .3])) ^ frame).volume(),
              upward_stop_probe_031_mm3=(solid(move(rotor, [0, 0, .31])) ^ frame).volume(),
              gear_boss_shaft_clearance='Nominal boss and shaft clear; gear outer cylinder intentionally overlaps fitted ribs. No true tooth mesh or physical axial-load proof',
              source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [COMPONENTS/'front.stl', COMPONENTS/'back.stl', COMPONENTS/'rotor.stl', COMPONENTS/'pin.stl', COMPONENTS/'pin-50.stl', COMPONENTS/'rotor-long.stl', METADATA/'motor-interface.json']})
(METADATA / 'motor-interface-review.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: v for k, v in report.items() if k != 'sampled_poses'}, indent=2))
sys.exit(0 if basis["status"] == "READY" else 2)
