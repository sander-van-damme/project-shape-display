"""E-018 protocol/schema checks; no measurements are created or implied."""
import argparse
from math import isclose

PITCH=5.08; N=5; APERTURE=3.0; FRAME=40.0; FID_OFFSET=15.0
PLANE_Y=34.0; PLANE_T=0.8; PLANE_GAP=1.2; FRAME_T=3.0
PORT_T=1.0; WRITER_INSERTION=1.0; WRITER_PARK_CLEARANCE=0.2
READER_STANDOFF=2.0; READER_BODY_T=4.0; READER_WINDOW_X=0.0; READER_WINDOW_Y=0.0
CASES=("all_zero","all_four","checkerboard","single_corner","single_centre",
       "plane_complements","cross_neighbour","walking_one")
CASE_CYCLES=125
TOTAL_CYCLES=len(CASES)*CASE_CYCLES
PLANES=("P0","P1","P2","P3")
NEIGHBOURS=("N","E","S","W")
CALIBRATION_THRESHOLD=0.85
MAX_ACTIVE_RESIDUAL_MM=0.20
RESEAT_INTERVAL=10
NEIGHBOUR_INTERVAL=10
REQUIRED={"cycle_id","map_case","plane","commanded_25bit","readback_25bit",
"pulse_start_ns","pulse_width_ns","actual_ack","fault_code","fiducial_error_x_mm",
"fiducial_error_y_mm","reader_class","reader_confidence","reseat_event",
"neighbour_displacement_mm","wear_code","retry_count","operator_id","environment_id",
"commanded_4plane_25bit","readback_4plane_25bit_complete","fiducial_transform_id",
"max_active_residual_mm","reader_calibration_id","reader_ambiguous","neighbour_observations",
"wear_inspection_id","as_built_port_measurement_id","active_cell_residuals_mm",
"reader_threshold","reader_reject_semantics"}

def cycle_plan(cycle_id):
    """Return the frozen 1-based run-sheet allocation for one cycle."""
    if not 1 <= cycle_id <= TOTAL_CYCLES:
        raise ValueError("cycle_id is outside the frozen run")
    case = CASES[(cycle_id - 1) % len(CASES)]
    return {"cycle_id": cycle_id, "map_case": case,
            "reseat_event": cycle_id % RESEAT_INTERVAL == 0,
            "neighbour_event": cycle_id % NEIGHBOUR_INTERVAL == 1}

def cycle_tags(cycle_id):
    """Compatibility view of the two deterministic event tags."""
    plan = cycle_plan(cycle_id)
    return plan["reseat_event"], plan["neighbour_event"]

def validate_record_shape(record):
    """Validate required evidence shape before a physical record can pass."""
    assert REQUIRED <= set(record)
    assert tuple(record["commanded_4plane_25bit"]) == PLANES
    assert tuple(record["readback_4plane_25bit_complete"]) == PLANES
    for plane in PLANES:
        assert len(record["commanded_4plane_25bit"][plane]) == 25
        assert len(record["readback_4plane_25bit_complete"][plane]) == 25
        assert set(record["commanded_4plane_25bit"][plane]) <= {0, 1}
        assert set(record["readback_4plane_25bit_complete"][plane]) <= {0, 1}
        assert record["readback_4plane_25bit_complete"][plane] == record["commanded_4plane_25bit"][plane]
    assert len(record["active_cell_residuals_mm"]) == 100
    assert {r["plane"] for r in record["active_cell_residuals_mm"]} == set(PLANES)
    assert all(set(r) >= {"plane", "row", "column", "x_mm", "y_mm", "residual_mm"}
               for r in record["active_cell_residuals_mm"])
    assert record["max_active_residual_mm"] <= MAX_ACTIVE_RESIDUAL_MM
    assert record["reader_threshold"] == CALIBRATION_THRESHOLD
    assert record["reader_reject_semantics"] == "wrong_or_ambiguous_or_missing_is_reject"
    assert set(record["neighbour_observations"]) == set(NEIGHBOURS)
    for observation in record["neighbour_observations"].values():
        assert set(observation) >= {"before_state", "after_state", "datum_id",
                                    "signed_displacement_x_mm", "signed_displacement_y_mm"}

def expected_run_counts():
    plans = [cycle_plan(i) for i in range(1, TOTAL_CYCLES + 1)]
    return {case: sum(p["map_case"] == case for p in plans) for case in CASES}

def schema_probe():
    """Exercise required evidence shape without inventing a measurement."""
    maps = {plane: [0] * 25 for plane in PLANES}
    residuals = [{"plane": plane, "row": row, "column": column,
                  "x_mm": 0.0, "y_mm": 0.0, "residual_mm": 0.0}
                 for plane in PLANES for row in range(5) for column in range(5)]
    neighbours = {side: {"before_state": "known", "after_state": "known",
                         "datum_id": "fixture-datum-0", "signed_displacement_x_mm": 0.0,
                         "signed_displacement_y_mm": 0.0} for side in NEIGHBOURS}
    record = {field: None for field in REQUIRED}
    record.update({"commanded_4plane_25bit": maps, "readback_4plane_25bit_complete": maps,
                   "active_cell_residuals_mm": residuals,
                   "max_active_residual_mm": 0.0,
                   "reader_threshold": CALIBRATION_THRESHOLD,
                   "reader_reject_semantics": "wrong_or_ambiguous_or_missing_is_reject",
                   "neighbour_observations": neighbours})
    validate_record_shape(record)

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
    assert len(CASES)==8 and CASE_CYCLES==125 and TOTAL_CYCLES==1000
    assert TOTAL_CYCLES % len(CASES)==0 and len(REQUIRED)==31
    assert PLANES == ("P0", "P1", "P2", "P3") and NEIGHBOURS == ("N", "E", "S", "W")
    assert 0 < CALIBRATION_THRESHOLD < 1 and MAX_ACTIVE_RESIDUAL_MM == 0.20
    assert expected_run_counts() == {case: CASE_CYCLES for case in CASES}
    reseats=sum(cycle_tags(i)[0] for i in range(1,TOTAL_CYCLES+1))
    neighbours=sum(cycle_tags(i)[1] for i in range(1,TOTAL_CYCLES+1))
    assert reseats==100 and neighbours==100
    assert all(cycle_plan(i)["map_case"] == CASES[(i-1) % 8] for i in range(1, TOTAL_CYCLES+1))
    assert all(cycle_plan(i)["reseat_event"] == (i % 10 == 0) for i in range(1, TOTAL_CYCLES+1))
    assert all(cycle_plan(i)["neighbour_event"] == (i % 10 == 1) for i in range(1, TOTAL_CYCLES+1))
    schema_probe()
    print("E-018 analytical protocol checks passed")
    print(f"field_span_mm={field_span:.2f} aperture_web_mm={PITCH-APERTURE:.2f}")
    print(f"writer_overlap_mm={writer_overlap:.2f} parked_clearance_mm={-FRAME/2-parked_inner:.2f} reader_clearance_mm={reader_bottom-upper_top:.2f}")
    print(f"adversarial_cases={len(CASES)} cycles_per_case={CASE_CYCLES} total_cycles={TOTAL_CYCLES} reseat_tags={reseats} neighbour_tags={neighbours} planes={len(PLANES)} active_residuals_per_record=100 required_fields={len(REQUIRED)}")

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
    if not args.check: parser.error("use --check")
    check()
