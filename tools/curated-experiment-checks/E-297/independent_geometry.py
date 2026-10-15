#!/usr/bin/env python3
"""Independent acceptance checks for E-297; no physical qualification.

The kinematic equations below do not import the CAD generator. Optional B-rep
checks import only its shapes, then apply separate placement/contact tests.
Run from the repository root: python tools/curated-experiment-checks/E-297/independent_geometry.py
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Review values: intentionally independent of the generator's internal equations.
PITCH = 5.08
PIN_WIDTH = 4.4
HALF_DIAMETER = 4.3
STROKE = 2.40
OFF_TIP_GAP = 3.36
DOG_HEIGHT = 2.40
DOG_SECTOR_DEG = 76.0
CAPTURE_GAP = .96
FLANGE_THICKNESS = .72
LEAD = 3.0


def gap(row: float, column: float) -> float:
    return OFF_TIP_GAP - STROKE * (row + column)


def matrix_contact(mask):
    r0, r1, c0, c1 = mask
    return [gap(r, c) < -1e-9 for r in (r0, r1) for c in (c0, c1)]


def kinematics():
    masks = list(itertools.product((0, 1), repeat=4))
    states = []
    for mask in masks:
        expected = [bool(r and c) for r in mask[:2] for c in mask[2:]]
        contact = matrix_contact(mask)
        assert contact == expected
        states.append(dict(mask=list(mask), engaged_cells=contact,
                           cell_tip_gaps_mm=[gap(r, c) for r in mask[:2] for c in mask[2:]]))
    samples = [i / 100 for i in range(101)]
    single_gaps = [gap(t, 0) for t in samples] + [gap(0, t) for t in samples]
    assert min(single_gaps) > 0
    # Each transition is conservative: stop rotation; release every previously
    # selected axis, then select the destination axes. Geometry cannot itself
    # enforce this operator sequence. Every emitted intermediate position is
    # evaluated, including all four cells.
    transitions = []
    for source, target in itertools.product(masks, repeat=2):
        current = list(source)
        incidental = []
        path_samples = 0
        old_cells = matrix_contact(source)
        new_cells = matrix_contact(target)
        for axis in range(4):
            if current[axis]:
                for t in samples:
                    pose = current.copy()
                    pose[axis] = 1 - t
                    assert all(not hit or old_cells[i] for i, hit in enumerate(matrix_contact(pose)))
                    path_samples += 1
                current[axis] = 0
        assert not any(matrix_contact(current))
        for axis in range(4):
            if target[axis]:
                for t in samples:
                    pose = current.copy()
                    pose[axis] = t
                    assert all(not hit or new_cells[i] for i, hit in enumerate(matrix_contact(pose)))
                    path_samples += 1
                current[axis] = 1
        assert tuple(current) == target
        transitions.append(dict(source=list(source), target=list(target), samples=path_samples))
    per_cell = [dict(row=r, column=c, tip_gap_mm=gap(r,c),
                     nominal_interdigitation_mm=max(0, -gap(r,c)),
                     nominal_straight_flank_overlap_mm=max(0,-gap(r,c)-.48))
                for r,c in itertools.product((0,1), repeat=2)]
    # Any axial manufacturing/stop/capture errors are bounded by their SUM,
    # not by assuming independent statistical cancellation.
    float_each = CAPTURE_GAP - FLANGE_THICKNESS
    # Deliberately use the full capture play from either loaded direction,
    # rather than claiming a centered +/- half-play without a preload.
    float_stack = 2 * float_each
    single_after_float = gap(1,0) - float_stack
    overlap_after_float = -gap(1,1) - float_stack
    assert single_after_float > 0 and overlap_after_float > 0
    return dict(
        evidence="Analytical geometry, not manufacturing or friction qualification",
        four_states=per_cell,
        all_16_selector_masks=states,
        one_sided_sweep=dict(samples=len(single_gaps), minimum_gap_mm=min(single_gaps)),
        break_before_make=dict(transition_count=len(transitions),
             sample_count=sum(t['samples'] for t in transitions),
             all_intermediate_contacts_subset_of_source_or_destination=True,
             all_routes_pass_through_fully_open=True,
             instruction="Stop input rotation and unload torque before changing selectors; release old selection completely before making the new one."),
        contact_boundary=dict(sum_normalized_strokes=OFF_TIP_GAP/STROKE,
             final_axis_travel_before_contact_mm=OFF_TIP_GAP-STROKE,
             interpretation="Two partly moved selectors CAN touch once their combined closure reaches 3.36 mm. One selector alone cannot. This is a geometric AND for hard-stop states, not a position-independent digital latch."),
        capture_play_budget=dict(axial_play_each_mm=float_each,
             centered_axial_error_each_mm=float_each/2,
             centered_two_half_error_stack_mm=float_each,
             worst_full_play_stack_mm=float_stack,
             single_clearance_after_full_play_stack_mm=single_after_float,
             full_interdigitation_after_full_play_stack_mm=overlap_after_float,
             note="These are residual budgets, before stop error, tip error, deflection and assembly error; no X1C tolerance distribution is assumed."),
        bounded_axial_error=dict(total_adverse_stack_mm=.72,
             single_selection_gap_after_stack_mm=gap(1,0)-.72,
             straight_flank_overlap_after_stack_mm=-gap(1,1)-.48-.72,
             tip_to_opposite_hub_root_gap_after_stack_mm=DOG_HEIGHT+gap(1,1)-.72,
             interpretation="The .72 mm bound is an acceptance budget, not a measured printer capability. It includes capture play, stop error, printed tip error and deflection. All three residuals must remain positive."),
        envelope=dict(pin_to_pin_face_gap_mm=PITCH-PIN_WIDTH,
             rotating_half_to_half_gap_mm=PITCH-HALF_DIAMETER))


def phase_geometry():
    # Two equal dog sectors every 180 degrees; centered complement is 90 deg.
    free_angle = 180 - 2 * DOG_SECTOR_DEG
    half_window = free_angle / 2
    assert free_angle > 0
    return dict(dog_count_each_half=2,
          dog_sector_deg=DOG_SECTOR_DEG,
          centered_complement_phase_deg=90,
          straight_flank_fit_phase_interval_deg=[90-half_window,90+half_window],
          unloaded_reversal_lash_deg=free_angle,
          screw_height_equivalent_at_3mm_lead_mm=LEAD*free_angle/360,
          caveat="This is straight-flank angular geometry. Lead-in chamfers permit a wider initial capture but do not guarantee autonomous seating from every phase. Tooth-on-tooth alignment is a blocked state; gently rock the input while applying light selector force, never force the selector home.")


def dd_profile():
    male_diameter, male_af = 2.2, 1.6
    profile_results = []
    for relief in (.12, .15, .20):
        bore_diameter = male_diameter + 2 * relief
        bore_af = male_af + 2 * relief
        radius, male_half_flat, bore_half_flat = male_diameter/2, male_af/2, bore_af/2
        # The largest projection on the bore flat normal is reached on the
        # circle/flat corner before the full circle radius becomes available.
        half_lash = math.degrees(math.asin(bore_half_flat/radius) - math.asin(male_half_flat/radius))
        capture_margin = male_diameter - bore_af
        assert capture_margin > 0
        corners = []
        for error in (.025, .05, .10):
            # Independent *full feature size* errors, not per-side errors.
            # Male diameter small and female AF large are the adverse corner.
            margin = (male_diameter-error) - (bore_af+error)
            aligned_flat_clearance = (bore_af-error) - (male_af+error)
            corners.append(dict(independent_diameter_or_AF_error_mm=error,
                 worst_torque_capture_diameter_margin_mm=margin,
                 worst_aligned_total_flat_clearance_mm=aligned_flat_clearance,
                 robust_positive_capture=margin > 1e-9,
                 guaranteed_positive_aligned_clearance=aligned_flat_clearance > 1e-9))
        profile_results.append(dict(radial_and_per_flat_relief_mm=relief,
            bore_diameter_mm=bore_diameter, bore_af_mm=bore_af,
            positive_capture_diameter_margin_mm=capture_margin,
            unloaded_profile_reversal_lash_deg=2*half_lash,
            feature_error_corners=corners))
    return dict(male_diameter_mm=male_diameter, male_af_mm=male_af,
        minimum_permanent_axial_overlap_mm=4.92-STROKE,
        nominal_two_DD_plus_dog_reversal_lash_deg=2*profile_results[1]['unloaded_profile_reversal_lash_deg']+28,
        nominal_total_screw_height_equivalent_mm=(2*profile_results[1]['unloaded_profile_reversal_lash_deg']+28)*LEAD/360,
        including_removable_hand_key_reversal_lash_deg=3*profile_results[1]['unloaded_profile_reversal_lash_deg']+28,
        including_hand_key_height_equivalent_mm=(3*profile_results[1]['unloaded_profile_reversal_lash_deg']+28)*LEAD/360,
        variants=profile_results,
        interpretation="DD is a positive bidirectional torsion connection in ideal geometry for all three variants. The .20 variant loses guaranteed positive capture at adverse +/-0.10 mm independent feature-size errors. Clearance does not establish friction, strength, coaxiality or FDM repeatability.")


def mesh_checks():
    """Check exported meshes with independent poses and manifold intersections.

    No generator code or precomputed generator collision results are imported.
    Tangential contact is allowed; positive intersection >1e-5 mm³ is rejected.
    """
    import numpy as np
    import trimesh as tm
    import manifold3d as md
    cad = ROOT/'cad'
    partsdir = cad/'parts'
    names = ('frame-left','frame-center','frame-right','row-selector',
             'input-shaft','rotor','screw','pin','stop-spacer')
    bases, hashes = {}, {}
    for name in names:
        path = partsdir/(name+'.stl')
        mesh = tm.load(path, force='mesh')
        assert mesh.is_watertight, name
        item = md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),
                                  np.asarray(mesh.faces,dtype=np.uint32)))
        assert item.status() == md.Error.NoError, name
        bases[name] = item
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    params = json.loads((cad/'parameters.json').read_text())
    for k,v in dict(pitch=5.08,stroke=2.4,tip_gap=3.36,tooth_height=2.4,
                    lower_base=7,upper_base=27.56,socket_depth=5.48).items():
        assert abs(params[k]-v)<1e-8, (k,params[k],v)
    cache, failures = {}, []
    counts = dict(poses=0,pair_candidates=0,intersection_evaluations=0)
    def part(name, xyz=(0,0,0), rz=0, flip=False):
        shape=bases[name]
        if flip: shape=shape.rotate((180,0,0))
        if rz: shape=shape.rotate((0,0,rz))
        if any(xyz):shape=shape.translate(xyz)
        signature=(name,tuple(round(x,7) for x in xyz),round(rz,7),flip)
        return shape,signature,shape.bounding_box()
    def pose(mask=(0,0,0,0),angles=(0,0,0,0),travels=None,
             input_float=0,output_float=0,lower_float=0,upper_float=0):
        if travels is None:travels=tuple(-3*a/360 for a in angles)
        pp={n:part(n) for n in names if n.startswith('frame')}
        for i,y in enumerate((-2.54,2.54)):
            pp[f'row-{i}']=part('row-selector',(0,y,7+2.4*mask[i]))
        for j,x in enumerate((-2.54,2.54)):
            pp[f'column-{j}']=part('row-selector',(x,0,27.56-2.4*mask[2+j]),90,True)
        for i,y in enumerate((-2.54,2.54)):
            for j,x in enumerate((-2.54,2.54)):
                k=2*i+j;a=angles[k]
                pp[f'input-{k}']=part('input-shaft',(x,y,1.2+input_float),a)
                pp[f'lower-{k}']=part('rotor',(x,y,7+2.4*mask[i]+lower_float),a)
                pp[f'upper-{k}']=part('rotor',(x,y,27.56-2.4*mask[2+j]+upper_float),90+a,True)
                pp[f'screw-{k}']=part('screw',(x,y,22.64+output_float),90+a)
                pp[f'pin-{k}']=part('pin',(x,y,38.21+travels[k]+output_float))
        # Actual shared stop shims belong to the hard-stop state, not to
        # intermediate motion; remove them before moving their selector.
        for i,y in enumerate((-2.54,2.54)):
            if abs(mask[i]-1)<1e-9:
                pp[f'row-shim-{i}-left']=part('stop-spacer',(-13,y-.65,5.8))
                pp[f'row-shim-{i}-right']=part('stop-spacer',(13,y-.65,5.8),180)
        for j,x in enumerate((-2.54,2.54)):
            if abs(mask[2+j])<1e-9:
                pp[f'column-shim-{j}-front']=part('stop-spacer',(x-.65,-13,23.24),90)
                pp[f'column-shim-{j}-back']=part('stop-spacer',(x-.65,13,23.24),-90)
        return pp
    def check(pp, label):
        counts['poses']+=1
        for (na,(a,sa,ba)),(nb,(b,sb,bb)) in itertools.combinations(pp.items(),2):
            if any(min(ba[i+3],bb[i+3])-max(ba[i],bb[i])<=1e-6 for i in range(3)):
                continue
            counts['pair_candidates']+=1
            key=(sa,sb)
            if key not in cache:
                cache[key]=(a^b).volume();counts['intersection_evaluations']+=1
            vol=cache[key]
            if vol>1e-5:failures.append(dict(pose=label,part_a=na,part_b=nb,volume_mm3=vol))
    masks=list(itertools.product((0,1),repeat=4))
    # All hard-stop states; a second non-cardinal angle probes actual rotating
    # sector/comb/spine envelopes, not just a circular diameter assertion.
    for mask in masks:
        for a in (0,45):check(pose(mask,angles=(a,)*4),f'mask{mask}/angle{a}')
    # All 32 undirected selector-cube edges, including transitions while the
    # perpendicular selectors are fully engaged. Endpoint tests above plus
    # three interior points on each edge. Analytic monotonic gap checks cover
    # the whole trajectory; mesh sampling checks the surrounding physical parts.
    for mask in masks:
        for axis in range(4):
            if mask[axis]:continue
            for t in (.25,.5,.75):
                mm=list(mask);mm[axis]=t
                check(pose(mm),f'edge{mask}/axis{axis}/t{t}')
    # One full turn each direction => +/-3 mm real thread/pin travel. The
    # unselected cells are also rotated here to test isolation mechanically.
    max_thread_collision=0
    for a in range(-360,361,15):
        for mask in ((0,0,0,0),(1,0,1,0),(1,1,1,1)):
            check(pose(mask,angles=(a,)*4),f'helical{mask}/angle{a}')
    # All captured-flange float corners plus the two shaft thrust positions.
    # Output float carries its threaded pin axially; otherwise one would be
    # testing an impossible locked-pin/translated-screw configuration.
    for mask in masks:
        for lower_float,upper_float in itertools.product((-.12,.12),repeat=2):
            for shaft_float in (0,.24):
                check(pose(mask,input_float=shaft_float,output_float=shaft_float,
                           lower_float=lower_float,upper_float=upper_float),
                      f'float{mask}/{lower_float}/{upper_float}/{shaft_float}')
    # Assembly is checked as actual continuous-direction insertion paths,
    # sampled every .25 mm. The frame splits through both columns' axes.
    # Lower row forks are attached far row first, before the next row is fitted;
    # otherwise an intact fork cannot slide through another already fitted row.
    target=pose((0,0,0,0))
    fixed={'frame-center':target['frame-center']}
    assembly_steps=[
       ('far-left-lower',['input-2','lower-2'],(-8,0,0)),
       ('far-right-lower',['input-3','lower-3'],(8,0,0)),
       ('far-row-fork-stage',['row-1'],(-40,-6,0),(0,-6,0)),
       ('far-row-fork',['row-1'],(0,-6,0)),
       ('near-left-lower',['input-0','lower-0'],(-8,0,0)),
       ('near-right-lower',['input-1','lower-1'],(8,0,0)),
       ('near-row-fork-stage',['row-0'],(-40,-6,0),(0,-6,0)),
       ('near-row-fork',['row-0'],(0,-6,0)),
       ('left-upper-column',['column-0','upper-0','upper-2','screw-0','screw-2','pin-0','pin-2'],(-8,0,0)),
       ('right-upper-column',['column-1','upper-1','upper-3','screw-1','screw-3','pin-1','pin-3'],(8,0,0)),
       ('left-frame-close',['frame-left'],(-12,0,0)),
       ('right-frame-close',['frame-right'],(12,0,0))]
    assembly_sample_count=0
    for step in assembly_steps:
        label,moving,start=step[:3]
        end=step[3] if len(step)>3 else (0,0,0)
        intervals=int(max(abs(start[i]-end[i]) for i in range(3))/.25)
        for index in range(intervals+1):
            delta=tuple(start[i]+(end[i]-start[i])*index/intervals for i in range(3))
            pp=dict(fixed)
            for name in moving:
                sig=target[name][1]
                xyz=tuple(sig[1][i]+delta[i] for i in range(3))
                pp[name]=part(sig[0],xyz,sig[2],sig[3])
            check(pp,'assembly/'+label+'/'+str(index));assembly_sample_count+=1
        fixed.update({name:pp[name] for name in moving})
    # Two deliberately impossible configurations validate that intersection
    # checks detect blocked geometry rather than merely reporting zero.
    negative=pose((1,1,1,1))
    wrong_upper=part('rotor',(-2.54,-2.54,27.56-2.4),0,True)[0]
    wrong_phase_volume=(negative['lower-0'][0]^wrong_upper).volume()
    assert wrong_phase_volume>1,wrong_phase_volume
    wrong_thread=pose((1,1,1,1),angles=(90,)*4,travels=(.75,)*4)
    wrong_thread_volume=(wrong_thread['screw-0'][0]^wrong_thread['pin-0'][0]).volume()
    assert wrong_thread_volume>1,wrong_thread_volume
    # Test A shapes: each rotor is retained by both blades over a full turn;
    # probe all variants, including both axial contact extremes.
    coupon_results=[]
    for label,relief,play in [('tight',.12,.18),('nominal',.15,.24),('loose',.20,.30)]:
        for prefix in ('rotor-','comb-'):
            n=prefix+label;mp=partsdir/(n+'.stl');m=tm.load(mp,force='mesh')
            bases[n]=md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
            hashes[n]=hashlib.sha256(mp.read_bytes()).hexdigest()
        largest=0
        for angle in range(0,360,15):
            for dz in (-play/2,0,play/2):
                rotor=bases['rotor-'+label].rotate((0,0,angle)).translate((0,0,dz))
                largest=max(largest,(rotor^bases['comb-'+label]).volume())
        assert largest<1e-5,(label,largest)
        coupon_results.append(dict(variant=label,samples=72,max_intersection_mm3=largest))
    return dict(source_mesh_sha256=hashes,intersection_tolerance_mm3=1e-5,
          checks=counts,unexpected_intersections=failures,
          all_nominal_and_sampled_states_clear=not failures,
          negative_controls=dict(tooth_on_tooth_forced_closure_mm3=wrong_phase_volume,
              wrong_thread_travel_sign_mm3=wrong_thread_volume),
          coupon_full_rotation_and_axial_capture=coupon_results,
          assembly=dict(steps=[x[0] for x in assembly_steps],samples=assembly_sample_count,maximum_translation_step_mm=.25),
          scope="Actual exported tessellated meshes, independently placed. Finite intermediate mesh sampling plus continuous analytical axial-gap bounds; not a friction, load, physical print or automatic engagement proof.")


def support_and_tilt():
    # Nominal CAD dimensions, separately derived from the exported assembly.
    pin_base, pin_length, travel = 38.21,18,3
    lower=(42,43.2);upper=(51.2,52.4)
    pin_low=(pin_base-travel,pin_base-travel+pin_length)
    pin_high=(pin_base+travel,pin_base+travel+pin_length)
    guide_overlaps=[]
    for pin in (pin_low,pin_high):
        for guide in (lower,upper):
            overlap=max(0,min(pin[1],guide[1])-max(pin[0],guide[0]))
            assert overlap>=1.2-1e-7
            guide_overlaps.append(overlap)
    closest_plane_separation=upper[0]-lower[1]
    max_tip_overhang=pin_high[1]+.24-upper[1]  # include output thrust float
    half_envelope=2.3+.2*max_tip_overhang/closest_plane_separation
    neighbor_reserve=PITCH-2*half_envelope
    assert neighbor_reserve>0
    return dict(
        lower_guide_z_mm=lower,upper_guide_z_mm=upper,
        pin_bottom_range_mm=[pin_low[0],pin_high[0]],
        pin_top_range_mm=[pin_low[1],pin_high[1]],
        minimum_pin_guide_axial_overlap_mm=min(guide_overlaps),
        conservative_pin_tilt=dict(guide_hole_width_mm=4.6,pin_width_mm=4.4,
            closest_guide_face_separation_mm=closest_plane_separation,
            maximum_tip_overhang_including_output_float_mm=max_tip_overhang,
            maximum_per_pin_face_half_envelope_mm=half_envelope,
            nominal_pair_neighbor_reserve_mm=neighbor_reserve,
            note="Ideal rigid guides only. Hole enlargement, frame-half misalignment, bending and print error consume this small reserve. Square yaw uses some of the same guide clearance and does not increase this bound; no physical neighbor-isolation qualification."),
        shaft_support=dict(input_collar_z_mm=[1.2,3.0],input_keeper_z_mm=3.24,
            input_journal_z_mm=[3.24,5.6],output_cone_seat_z_mm=30.22,
            output_flange_top_z_mm=31.97,output_keeper_z_mm=32.21,
            axial_thrust_float_mm=.24,
            socket_tip_clearance_off_mm=.56,
            worst_input_roof_clearance_after_shaft_and_capture_float_mm=.56-.24-.12,
            input_roof_clearance_with_additional_point12_selector_stop_error_mm=.56-.24-.12-.12,
            worst_output_roof_clearance_after_capture_float_mm=.56-.12,
            nominal_minimum_DD_overlap_mm=2.52,
            worst_minimum_DD_overlap_after_output_and_capture_float_mm=2.52-.24-.12,
            minimum_DD_overlap_with_additional_point12_selector_stop_error_mm=2.52-.24-.12-.12,
            note="Axial shaft float can cause a pin-height transient; it is not automatically part of the dog-gap stack while DD heads remain clear of blind socket roofs."))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-mesh', action='store_true', help='Analytical checks only; not complete validation')
    parser.add_argument('--output', type=Path, default=ROOT/'independent-geometry.json')
    args = parser.parse_args()
    result = dict(kinematics=kinematics(), phase=phase_geometry(), dd=dd_profile(), support=support_and_tilt(),
                  calculated_only=True,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if not args.skip_mesh:result['actual_meshes']=mesh_checks()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if result.get('actual_meshes',{}).get('unexpected_intersections'):
        raise AssertionError("Unexpected mesh intersections; see output JSON")
    print(json.dumps(dict(output=str(args.output), masks=16,
          transitions=result['kinematics']['break_before_make']['transition_count'],
          physical_fit='unknown'),indent=2))

if __name__ == '__main__':
    main()
