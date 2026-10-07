import csv
import tempfile
import unittest
from pathlib import Path

import fit_calibration_matrix as checker


EXTRA_COLUMNS = [
    "process_id", "printer", "nozzle_diameter_mm", "layer_height_mm",
    "filament_lot", "slicer_profile_hash", "xy_compensation_mm",
    "elephant_foot_compensation_mm", "part_id", "clock_positions_deg",
    "stop_results", "loaded_3p27N_result", "writer_engagements",
    "reader_reads", "measurement_mean_mm", "measurement_min_mm",
    "measurement_max_mm", "measurement_range_mm", "actual_dimensions_mm",
]


def valid_rows():
    rows = []
    for number, planned in enumerate(checker.plan(), 1):
        row = {key: str(value) for key, value in planned.items()}
        row.update({
            "fit_ok": "true", "writer_ok": "true", "reader_ok": "true",
            "clearance_mm": "0.40", "reader_margin_mm": "0.40",
            "process_id": "fixture-only", "printer": "fixture-printer",
            "nozzle_diameter_mm": "0.4", "layer_height_mm": "0.2",
            "filament_lot": "fixture-lot", "slicer_profile_hash": "fixture-hash",
            "xy_compensation_mm": "0", "elephant_foot_compensation_mm": "0",
            "part_id": f"fixture-{number}", "clock_positions_deg": "0,120,240",
            "stop_results": "5/5",
            "loaded_3p27N_result": "pass" if planned["article"] == "rotor" else "not_applicable",
            "writer_engagements": "30/30" if planned["article"] == "writer" else "not_applicable",
            "reader_reads": "150/150" if planned["article"] == "reader" else "not_applicable",
            "measurement_mean_mm": "1.0", "measurement_min_mm": "0.8",
            "measurement_max_mm": "1.2", "measurement_range_mm": "0.4",
            "actual_dimensions_mm": "fixture-only; no physical measurement",
        })
        rows.append(row)
    return rows


def write_results(rows, columns=None):
    columns = columns or list(rows[0])
    handle = tempfile.NamedTemporaryFile(mode="w", newline="", suffix=".csv", delete=False)
    with handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return Path(handle.name)


class CheckerContractTests(unittest.TestCase):
    def assert_rejected(self, rows, columns=None, text=None):
        path = write_results(rows, columns)
        self.addCleanup(path.unlink)
        with self.assertRaises(SystemExit) as raised:
            checker.check_results(path)
        if text:
            self.assertIn(text, str(raised.exception))

    def test_complete_planned_fixture_passes(self):
        path = write_results(valid_rows())
        self.addCleanup(path.unlink)
        checker.check_results(path)

    def test_incomplete_row_count_is_rejected(self):
        self.assert_rejected(valid_rows()[:1], text="row count 1")

    def test_duplicate_identity_is_rejected(self):
        rows = valid_rows()
        rows[-1] = dict(rows[-2])
        self.assert_rejected(rows, text="duplicate planned identity")

    def test_mismatched_identity_is_rejected(self):
        rows = valid_rows()
        rows[0]["location"] = "witness"
        self.assert_rejected(rows, text="planned identities mismatch")

    def test_process_metadata_is_required(self):
        rows = valid_rows()
        for row in rows:
            del row["printer"]
        self.assert_rejected(rows, text="missing columns: printer")

    def test_attempt_count_is_required(self):
        rows = valid_rows()
        for row in rows:
            del row["attempts"]
        self.assert_rejected(rows, text="missing columns: attempts")

    def test_loaded_clock_and_summary_evidence_are_required(self):
        for field in ("loaded_3p27N_result", "clock_positions_deg", "measurement_mean_mm"):
            rows = valid_rows()
            for row in rows:
                del row[field]
            self.assert_rejected(rows, text=f"missing columns: {field}")

    def test_gate_evidence_must_match_article(self):
        rows = valid_rows()
        rows[36]["loaded_3p27N_result"] = "pass"  # first writer row
        self.assert_rejected(rows, text="invalid loaded_3p27N_result")


if __name__ == "__main__":
    unittest.main()
