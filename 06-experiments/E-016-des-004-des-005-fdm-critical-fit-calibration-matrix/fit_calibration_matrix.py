"""Print or check E-016's FDM fit-calibration plan.

This validates result structure and provisional gates only; it never creates
or implies printed measurements.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

POCKET = (2.10, 2.20, 2.30)
BORE = (1.20, 1.40, 1.60)
IDENTITY = ("article", "test", "orientation", "location", "pocket_radius_mm",
            "bore_diameter_mm", "writer_clearance_mm", "reader_offset_mm")
REQUIRED = set(IDENTITY) | {
    "attempts", "fit_ok", "writer_ok", "reader_ok", "clearance_mm",
    "reader_margin_mm", "process_id", "printer", "nozzle_diameter_mm",
    "layer_height_mm", "filament_lot", "slicer_profile_hash",
    "xy_compensation_mm", "elephant_foot_compensation_mm", "part_id",
    "clock_positions_deg", "stop_results", "loaded_3p27N_result",
    "writer_engagements", "reader_reads", "measurement_mean_mm",
    "measurement_min_mm", "measurement_max_mm", "measurement_range_mm",
    "actual_dimensions_mm",
}
UNRESOLVED = {"", "unresolved"}


def _decimal(value: str, field: str, line: int) -> Decimal:
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError(f"line {line}: {field} is not numeric") from None


def _identity(row: dict[str, str], line: int) -> tuple[object, ...]:
    result: list[object] = []
    for field in IDENTITY:
        raw = row.get(field)
        value = "" if raw is None else str(raw).strip()
        if not value:
            raise ValueError(f"line {line}: empty identity field {field}")
        result.append(_decimal(value, field, line) if field.endswith("_mm") else value)
    return tuple(result)


def _require_value(row: dict[str, str], field: str, line: int) -> str:
    value = (row.get(field) or "").strip()
    if value.lower() in UNRESOLVED:
        raise ValueError(f"line {line}: {field} is unresolved")
    return value


def _require_bool(row: dict[str, str], field: str, line: int) -> None:
    value = _require_value(row, field, line).lower()
    if value not in {"true", "false"}:
        raise ValueError(f"line {line}: {field} must be true or false")
    if value != "true":
        raise ValueError(f"line {line}: functional gate false ({field})")


def _require_result(row: dict[str, str], field: str, line: int,
                    allowed: set[str]) -> None:
    value = _require_value(row, field, line).lower()
    if value not in allowed:
        raise ValueError(f"line {line}: invalid {field}: {row[field]!r}")


def _require_summary(row: dict[str, str], line: int) -> None:
    values = {field: _decimal(_require_value(row, field, line), field, line)
              for field in ("measurement_mean_mm", "measurement_min_mm",
                            "measurement_max_mm", "measurement_range_mm")}
    if values["measurement_min_mm"] > values["measurement_max_mm"]:
        raise ValueError(f"line {line}: measurement min exceeds max")
    if not (values["measurement_min_mm"] <= values["measurement_mean_mm"]
            <= values["measurement_max_mm"]):
        raise ValueError(f"line {line}: measurement mean is outside min/max")
    if values["measurement_range_mm"] != (values["measurement_max_mm"]
                                            - values["measurement_min_mm"]):
        raise ValueError(f"line {line}: measurement range does not equal max-min")


def plan() -> list[dict[str, object]]:
    rotor_rows = [{"article": "rotor", "test": "fit", "orientation": o,
             "location": loc, "pocket_radius_mm": p,
             "bore_diameter_mm": b, "writer_clearance_mm": 0.40,
             "reader_offset_mm": 0.00, "attempts": 5}
            for o in ("F", "A") for loc in ("centre", "boundary")
            for p in POCKET for b in BORE]
    writer_rows = [{"article": "writer", "test": "engagement",
                    "orientation": "F", "location": "witness",
                    "pocket_radius_mm": 2.20, "bore_diameter_mm": 1.40,
                    "writer_clearance_mm": c, "reader_offset_mm": 0.00,
                    "attempts": 30} for c in (0.20, 0.40, 0.60)]
    reader_rows = [{"article": "reader", "test": "read",
                    "orientation": "F", "location": "witness",
                    "pocket_radius_mm": 2.20, "bore_diameter_mm": 1.40,
                    "writer_clearance_mm": 0.40, "reader_offset_mm": offset,
                    "attempts": 150} for offset in (0.00, -0.20, 0.20)]
    return rotor_rows + writer_rows + reader_rows


def check_results(path: Path) -> None:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise SystemExit("results CSV has no header")
        missing = REQUIRED - set(reader.fieldnames)
        if missing:
            raise SystemExit(f"missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise SystemExit("results CSV is empty")

    planned_rows = {_identity(row, 0): row for row in plan()}
    expected = list(planned_rows)
    actual = []
    failures = []
    for number, row in enumerate(rows, 2):
        try:
            identity = _identity(row, number)
            actual.append(identity)
            attempts = int(_require_value(row, "attempts", number))
            if attempts != int(planned_rows.get(identity, {}).get("attempts", -1)):
                raise ValueError(f"line {number}: attempts do not match plan")
            for field in ("fit_ok", "writer_ok", "reader_ok"):
                _require_bool(row, field, number)
            for field, minimum in (("clearance_mm", Decimal("0.10")),
                                   ("writer_clearance_mm", Decimal("0.20")),
                                   ("reader_margin_mm", Decimal("0.20"))):
                if _decimal(_require_value(row, field, number), field, number) < minimum:
                    raise ValueError(f"line {number}: {field} < {minimum} mm")
            for field in ("process_id", "printer", "nozzle_diameter_mm",
                          "layer_height_mm", "filament_lot",
                          "slicer_profile_hash", "xy_compensation_mm",
                          "elephant_foot_compensation_mm", "part_id",
                          "actual_dimensions_mm"):
                _require_value(row, field, number)
            if _require_value(row, "clock_positions_deg", number) != "0,120,240":
                raise ValueError(f"line {number}: clock_positions_deg must be 0,120,240")
            _require_result(row, "stop_results", number, {"5/5"})
            article = row["article"].lower()
            expected_results = {
                "loaded_3p27N_result": "pass" if article == "rotor" else "not_applicable",
                "writer_engagements": "30/30" if article == "writer" else "not_applicable",
                "reader_reads": "150/150" if article == "reader" else "not_applicable",
            }
            for field, expected_result in expected_results.items():
                _require_result(row, field, number, {expected_result})
            _require_summary(row, number)
        except (KeyError, ValueError) as error:
            failures.append(str(error))

    if len(rows) != len(expected):
        failures.append(f"row count {len(rows)} does not match planned count {len(expected)}")
    if len(actual) == len(set(actual)) and set(actual) != set(expected):
        missing = set(expected) - set(actual)
        extra = set(actual) - set(expected)
        failures.append(f"planned identities mismatch: missing={len(missing)}, extra={len(extra)}")
    elif len(actual) != len(set(actual)):
        failures.append("duplicate planned identity")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"checked {len(rows)} measured rows: provisional gates pass; physical evidence complete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    if args.plan:
        keys = ("article", "test", "orientation", "location",
                "pocket_radius_mm", "bore_diameter_mm", "writer_clearance_mm",
                "reader_offset_mm", "attempts")
        print(",".join(keys))
        for row in plan():
            print(",".join(str(row[key]) for key in keys))
    if args.results:
        check_results(args.results)
    if not args.plan and not args.results:
        parser.error("choose --plan or --results")


if __name__ == "__main__":
    main()
