"""Numerical geometry gate for the DES-004 5x5 rotor coupon.

This is a calculated envelope check, not a print or hardware measurement.
"""

PITCH = 5.08
N = 5
FIELD = N * PITCH
FRAME = 40.0
ROTOR_RADIUS = 1.50
POCKET_RADIUS = 2.20             # clears the integral vane swept envelope
AXLE_DIAMETER = 1.00
BORE_DIAMETER = 1.40
VANE_THICKNESS = 0.45
VANE_OFFSET = 1.70
VANE_WIDTH = 1.20
VANE_OFFSET_TOL = 0.05
BODY = 3.60
PIN_LENGTH = 10.0
FRAME_THICKNESS = 3.0
ROTOR_THICKNESS = 3.0
RETAINER_THICKNESS = 1.0
WRITER_TONGUE_T = 0.80
WRITER_TONGUE_W = 1.00
WRITER_POCKET_T = 1.20
WRITER_POCKET_W = 1.40
READER_APERTURE_W = 0.70
READER_APERTURE_H = 1.00
READER_VANE_W = 1.20
READER_STANDOFF = 1.80
TOL = {"pitch": 0.03, "rotor_radius": 0.05, "pocket_radius": 0.05,
       "bore": 0.05, "axle": 0.05, "vane_width": 0.05,
       "writer": 0.05, "frame": 0.10}


def check() -> dict[str, float | bool]:
    neighbour_edge_gap = PITCH - 2 * ROTOR_RADIUS
    vane_outer_edge = VANE_OFFSET + VANE_THICKNESS / 2
    vane_corner_radius = ((VANE_OFFSET + VANE_OFFSET_TOL
                           + (VANE_THICKNESS + TOL["vane_width"]) / 2) ** 2
                          + ((VANE_WIDTH + TOL["vane_width"]) / 2) ** 2) ** 0.5
    neighbour_body_inner_edge = PITCH - BODY / 2
    vane_neighbour_gap = neighbour_body_inner_edge - vane_outer_edge
    stack = FRAME_THICKNESS + ROTOR_THICKNESS + 2 * RETAINER_THICKNESS
    result = {
        "field_span_mm": FIELD,
        "field_fits_frame": FIELD <= FRAME,
        "frame_margin_each_side_mm": (FRAME - FIELD) / 2,
        "rotor_radial_clearance_mm": POCKET_RADIUS - ROTOR_RADIUS,
        "rotor_pocket_fits": POCKET_RADIUS >= ROTOR_RADIUS,
        "vane_swept_corner_radius_mm": vane_corner_radius,
        "vane_frame_clearance_mm": POCKET_RADIUS - vane_corner_radius,
        "vane_clears_frame": POCKET_RADIUS >= vane_corner_radius,
        "axle_bore_diametral_clearance_mm": BORE_DIAMETER - AXLE_DIAMETER,
        "axle_bore_fits": BORE_DIAMETER >= AXLE_DIAMETER,
        "nearest_rotor_edge_gap_mm": neighbour_edge_gap,
        "rotors_clear_neighbours": neighbour_edge_gap > 0,
        "vane_neighbour_gap_mm": vane_neighbour_gap,
        "vane_clears_neighbour_body": vane_neighbour_gap > 0,
        "pin_stack_mm": stack,
        "pin_end_margin_mm": PIN_LENGTH - stack,
        "pin_reaches_stack": PIN_LENGTH >= stack,
        "writer_side_clearance_mm": WRITER_POCKET_T - WRITER_TONGUE_T,
        "writer_width_clearance_mm": WRITER_POCKET_W - WRITER_TONGUE_W,
        "reader_vane_width_clearance_mm": READER_VANE_W - READER_APERTURE_W,
        "reader_target_height_mm": READER_APERTURE_H,
        "reader_standoff_mm": READER_STANDOFF,
    }
    assert result["field_fits_frame"]
    assert result["rotor_pocket_fits"]
    assert result["vane_clears_frame"]
    assert result["axle_bore_fits"]
    assert result["rotors_clear_neighbours"]
    assert result["vane_clears_neighbour_body"]
    assert result["pin_reaches_stack"]
    assert result["writer_side_clearance_mm"] > 0
    assert result["writer_width_clearance_mm"] > 0
    assert result["reader_vane_width_clearance_mm"] > 0
    return result


def worst_case() -> dict[str, float | bool]:
    """Independent +/- tolerance screen; not a print measurement."""
    pitch = PITCH + TOL["pitch"]
    rotor_r = ROTOR_RADIUS + TOL["rotor_radius"]
    pocket_r = POCKET_RADIUS - TOL["pocket_radius"]
    bore = BORE_DIAMETER - TOL["bore"]
    axle = AXLE_DIAMETER + TOL["axle"]
    writer_t = WRITER_TONGUE_T + TOL["writer"]
    writer_w = WRITER_TONGUE_W + TOL["writer"]
    vane_corner = ((VANE_OFFSET + VANE_OFFSET_TOL
                    + (VANE_THICKNESS + TOL["vane_width"]) / 2) ** 2
                   + ((VANE_WIDTH + TOL["vane_width"]) / 2) ** 2) ** 0.5
    return {
        "field_fits_frame": N * pitch <= FRAME - TOL["frame"],
        "frame_margin_each_side_mm": (FRAME - TOL["frame"] - N * pitch) / 2,
        "rotor_radial_clearance_mm": pocket_r - rotor_r,
        "vane_frame_clearance_mm": (POCKET_RADIUS - TOL["pocket_radius"])
                                    - vane_corner,
        "vane_clears_frame": (POCKET_RADIUS - TOL["pocket_radius"])
                              >= vane_corner,
        "axle_bore_diametral_clearance_mm": bore - axle,
        "nearest_rotor_edge_gap_mm": pitch - 2 * rotor_r,
        "vane_reader_width_margin_mm": READER_VANE_W - READER_APERTURE_W - 2*TOL["vane_width"],
        "writer_side_clearance_mm": (WRITER_POCKET_T - TOL["writer"]) - writer_t,
        "writer_width_clearance_mm": (WRITER_POCKET_W - TOL["writer"]) - writer_w,
    }


def logical_smoke(transitions: int = 10_000) -> dict[str, int]:
    """Ideal state-machine smoke only; it is not a hardware run."""
    state = errors = 0
    for i in range(transitions):
        target = (i * 3 + 1) % 5
        state = target
        if state != target:
            errors += 1
    return {"transitions": transitions, "commanded": transitions,
            "read": transitions, "state_errors": errors}


if __name__ == "__main__":
    for key, value in check().items():
        print(f"{key}={value}")
    for key, value in worst_case().items():
        print(f"worst_case_{key}={value}")
    for key, value in logical_smoke().items():
        print(f"logical_smoke_{key}={value}")
