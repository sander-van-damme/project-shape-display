#!/usr/bin/env python3
"""Fixed witness camera: ideal pinhole construction, not hardware accuracy.

Finite coverage/occlusion, local pose rank, and exact frontoparallel error
witnesses. All dimensions, pixel bounds and rigid attachments are assumptions.
"""
import itertools
import json
import numpy as np

H, HEAD_Z, SIDE, BOARD_HALF = 800., 300., 90., 203.2
REF_HALF, PATCH_HALF = 230., 5.
F = 4096 * 500 / 600
CORNERS = np.array(list(itertools.product((-SIDE/2, SIDE/2), repeat=2)))
REFS = np.array([(x, y) for x, y in itertools.product((-REF_HALF, 0., REF_HALF), repeat=2)
                 if x or y])


def project(points, f=F, H=H):
    return f * points[:, :2] / (H-points[:, 2, None])


def head_points(x=0., y=0., z=HEAD_Z):
    return np.column_stack((CORNERS + (x, y), np.full(4, z)))


def jacobian(points):
    # Small rigid translations and rotations about the target center.
    origin = points.mean(axis=0)
    J = []
    for k in range(6):
        if k < 3:
            delta = np.zeros_like(points)
            delta[:, k] = 1
        else:
            axis = np.eye(3)[k-3]
            delta = np.cross(axis, points-origin)
        step = 1e-5
        J.append(((project(points+step*delta)-project(points-step*delta))/(2*step)).ravel())
    return np.array(J).T


def main():
    counts=[]; maximum_image=0.; ranks=[]
    # Finite point projections plus finite reference patches, not a full housing.
    for x,y in itertools.product(np.linspace(-BOARD_HALF, BOARD_HALF, 17), repeat=2):
        head=head_points(x,y)
        maximum_image=max(maximum_image,float(np.max(abs(project(head)))))
        ranks.append(int(np.linalg.matrix_rank(jacobian(head))))
        # At head plane, a ray to a board point has XY=(1-z/H)*boardXY.
        factor=1-HEAD_Z/H
        rays=REFS*factor
        patch=PATCH_HALF*factor
        blocked=np.all(abs(rays-(x,y)) <= SIDE/2+patch, axis=1)
        counts.append(int(sum(blocked)))
        # At least one complete diametric side-midpoint pair survives.
        sidepairs=[((0,-REF_HALF),(0,REF_HALF)),((-REF_HALF,0),(REF_HALF,0))]
        assert any(all(not blocked[np.where(np.all(REFS==r,axis=1))[0][0]]
                           for r in pair) for pair in sidepairs)
    assert set(ranks)=={6}
    assert max(counts)==1  # Also continuous: nearest projected centers 143.75 > 96.25.
    assert REF_HALF*(1-HEAD_Z/H) > SIDE+2*PATCH_HALF*(1-HEAD_Z/H)
    assert maximum_image < 4096/2
    board_corners=np.array([(x,y,0.) for x,y in itertools.product((-235.,235.),repeat=2)])
    assert np.max(abs(project(board_corners))) < 4096/2
    # Exterior board-reference paths stay outside terrain even at maximum height.
    outside_at_50=(REF_HALF-PATCH_HALF)*(1-50/H)
    assert outside_at_50 > BOARD_HALF
    # Corners-only station can lose one of its four points to the moving housing.
    assert np.all(abs(np.array([REF_HALF,REF_HALF])*.625-(150,150))<SIDE/2)
    rows=[]
    for pixels in (1024,4096):
        f=F*pixels/4096
        board_span=f*(2*REF_HALF)/H
        head_span=f*SIDE/(H-HEAD_Z)
        eps=.25  # allocated endpoint error, no earned subpixel measurement
        errors=[]
        for eb,eh in itertools.product((-2*eps,2*eps),repeat=2):
            z=f*(2*REF_HALF/(board_span+eb)-SIDE/(head_span+eh))
            errors.append(z-HEAD_Z)
        rows.append(dict(pixels=pixels,head_span_px=head_span,board_span_px=board_span,
                         exact_height_error_interval_mm=[min(errors),max(errors)]))
    # Exact frontoparallel aliases: no residual can identify unknown marker scale.
    span=F*SIDE/(H-HEAD_Z)
    inferred_with_wrong_size=H-F*(SIDE+.1)/span
    assert abs(inferred_with_wrong_size-HEAD_Z+.1*(H-HEAD_Z)/SIDE)<1e-10
    # Fixed camera translation cancels only with same-time board observations.
    moved=H+.5
    sh=F*SIDE/(moved-HEAD_Z); sb=F*(2*REF_HALF)/moved
    recovered=F*((2*REF_HALF)/sb-SIDE/sh)
    assert abs(recovered-HEAD_Z)<1e-10
    stale=H-F*SIDE/sh
    assert abs(stale-HEAD_Z+.5)<1e-10
    # Common marker + optics displacement is visible; marker-to-optics flex is not.
    before=project(head_points())
    after=project(head_points(z=HEAD_Z+.5))
    assert np.max(abs(after-before))>0
    print(json.dumps(dict(assumptions=dict(camera_height_mm=H,head_marker_height_mm=HEAD_Z,
          marker_side_mm=SIDE,board_reference_centers_mm=REF_HALF,
          board_reference_patch_side_mm=2*PATCH_HALF,field_at_head_mm=600,
          pixel_endpoint_bound=.25),positions_checked=len(counts),
          max_occluded_of_eight_references=max(counts),min_pose_jacobian_rank=min(ranks),
          max_head_pixel_coordinate=maximum_image,reference_ray_min_coordinate_at_z50=outside_at_50,
          error_scenarios=rows,head_size_error_point1_mm=inferred_with_wrong_size-HEAD_Z,
          focal_point1_percent_height_error_mm=HEAD_Z*.001,
          stale_camera_datum_error_mm=stale-HEAD_Z,
          corrected_camera_motion_error_mm=recovered-HEAD_Z,
          fixed_camera_detects_half_mm_head_motion_max_pixel_change=float(np.max(abs(after-before))),
          extra_witness_seconds={str(n):n/4*.1 for n in (1024,4096,6400)}),indent=2))


if __name__=='__main__':
    main()
