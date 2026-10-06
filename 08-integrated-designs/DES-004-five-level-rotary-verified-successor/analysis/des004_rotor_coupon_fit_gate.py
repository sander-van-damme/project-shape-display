"""Numerical geometry gate for the DES-004 5x5 rotor coupon.

This is a calculated envelope check, not a print or hardware measurement.
"""

PITCH = 5.08
N = 5
FIELD = N * PITCH
FRAME = 40.0
ROTOR_RADIUS = 1.50
POCKET_RADIUS = 1.70
AXLE_DIAMETER = 1.00
BORE_DIAMETER = 1.40
VANE_THICKNESS = 0.45
VANE_OFFSET = 1.70
VANE_WIDTH = 1.20
BODY = 3.60
PIN_LENGTH = 10.0
FRAME_THICKNESS = 3.0
ROTOR_THICKNESS = 3.0
RETAINER_THICKNESS = 1.0


def check() -> dict[str, float | bool]:
    neighbour_edge_gap = PITCH - 2 * ROTOR_RADIUS
    vane_outer_edge = VANE_OFFSET + VANE_THICKNESS / 2
    neighbour_body_inner_edge = PITCH - BODY / 2
    vane_neighbour_gap = neighbour_body_inner_edge - vane_outer_edge
    stack = FRAME_THICKNESS + ROTOR_THICKNESS + 2 * RETAINER_THICKNESS
    result = {
        "field_span_mm": FIELD,
        "field_fits_frame": FIELD <= FRAME,
        "frame_margin_each_side_mm": (FRAME - FIELD) / 2,
        "rotor_radial_clearance_mm": POCKET_RADIUS - ROTOR_RADIUS,
        "rotor_pocket_fits": POCKET_RADIUS >= ROTOR_RADIUS,
        "axle_bore_diametral_clearance_mm": BORE_DIAMETER - AXLE_DIAMETER,
        "axle_bore_fits": BORE_DIAMETER >= AXLE_DIAMETER,
        "nearest_rotor_edge_gap_mm": neighbour_edge_gap,
        "rotors_clear_neighbours": neighbour_edge_gap > 0,
        "vane_neighbour_gap_mm": vane_neighbour_gap,
        "vane_clears_neighbour_body": vane_neighbour_gap > 0,
        "pin_stack_mm": stack,
        "pin_end_margin_mm": PIN_LENGTH - stack,
        "pin_reaches_stack": PIN_LENGTH >= stack,
    }
    assert result["field_fits_frame"]
    assert result["rotor_pocket_fits"]
    assert result["axle_bore_fits"]
    assert result["rotors_clear_neighbours"]
    assert result["vane_clears_neighbour_body"]
    assert result["pin_reaches_stack"]
    return result


if __name__ == "__main__":
    for key, value in check().items():
        print(f"{key}={value}")
