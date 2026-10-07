"""E-018 definition checks; no measurements are created or implied."""
import argparse
from math import isclose

PITCH=5.08; N=5; APERTURE=3.0; FRAME=40.0; FID_OFFSET=15.0
PLANE_Y=34.0; PLANE_T=0.8; PLANE_GAP=1.2; FRAME_T=3.0
PORT_T=1.0; WRITER_INSERTION=1.0; WRITER_PARK_CLEARANCE=0.2
READER_STANDOFF=2.0; READER_BODY_T=4.0; READER_WINDOW_X=0.0; READER_WINDOW_Y=0.0
CASES=("all_zero","all_four","checkerboard","single_corner","single_centre",
       "plane_complements","cross_neighbour","walking_one")
REQUIRED={"cycle_id","map_case","plane","commanded_25bit","readback_25bit",
"pulse_start_ns","pulse_width_ns","actual_ack","fault_code","fiducial_error_x_mm",
"fiducial_error_y_mm","reader_class","reader_confidence","reseat_event",
"neighbour_displacement_mm","wear_code","retry_count","operator_id","environment_id"}

def check():
    field_span=N*PITCH
    assert round(field_span,2)==25.4 and round(PITCH-APERTURE,2)==2.08
    assert round(FRAME-field_span,2)==14.6 and FID_OFFSET>field_span/2
    tab_outer=-PLANE_Y/2-PORT_T
    tab_inner=-PLANE_Y/2
    tongue_outer=-PLANE_Y/2-PORT_T
    tongue_inner=tongue_outer+PORT_T
    writer_overlap=min(tab_inner,tongue_inner)-max(tab_outer,tongue_outer)
    assert isclose(writer_overlap, PORT_T, abs_tol=1e-9)
    assert writer_overlap >= WRITER_INSERTION > 0
    parked_outer=-FRAME/2-PORT_T-WRITER_PARK_CLEARANCE
    parked_inner=-FRAME/2-WRITER_PARK_CLEARANCE
    assert parked_inner < -FRAME/2 and parked_outer < parked_inner
    upper_top=FRAME_T+3*(PLANE_T+PLANE_GAP)+PLANE_T
    reader_bottom=upper_top+READER_STANDOFF
    assert reader_bottom > upper_top
    assert READER_BODY_T > 0 and READER_STANDOFF > 0
    assert isclose(READER_WINDOW_X, 0.0, abs_tol=1e-9)
    assert isclose(READER_WINDOW_Y, 0.0, abs_tol=1e-9)
    assert READER_WINDOW_X-APERTURE/2 <= 0 <= READER_WINDOW_X+APERTURE/2
    assert READER_WINDOW_Y-APERTURE/2 <= 0 <= READER_WINDOW_Y+APERTURE/2
    assert len(CASES)==8 and 20*len(CASES)<=1000 and len(REQUIRED)==19
    print("E-018 analytical checks passed")
    print(f"field_span_mm={field_span:.2f} aperture_web_mm={PITCH-APERTURE:.2f}")
    print(f"writer_overlap_mm={writer_overlap:.2f} parked_clearance_mm={-FRAME/2-parked_inner:.2f} reader_clearance_mm={reader_bottom-upper_top:.2f}")
    print(f"adversarial_cases={len(CASES)} minimum_cycles=1000 required_fields={len(REQUIRED)}")

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
    if not args.check: parser.error("use --check")
    check()
