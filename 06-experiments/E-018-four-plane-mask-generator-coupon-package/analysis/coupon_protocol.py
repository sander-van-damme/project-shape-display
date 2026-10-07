"""E-018 definition checks; no measurements are created or implied."""
import argparse

PITCH=5.08; N=5; APERTURE=3.0; FRAME=40.0; FID_OFFSET=15.0
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
    assert len(CASES)==8 and 20*len(CASES)<=1000 and len(REQUIRED)==19
    print("E-018 analytical checks passed")
    print(f"field_span_mm={field_span:.2f} aperture_web_mm={PITCH-APERTURE:.2f}")
    print(f"adversarial_cases={len(CASES)} minimum_cycles=1000 required_fields={len(REQUIRED)}")

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
    if not args.check: parser.error("use --check")
    check()
