"""Print or check E-016's FDM fit-calibration plan.

This validates result structure and provisional gates only; it never creates
or implies printed measurements.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

POCKET = (2.10, 2.20, 2.30)
BORE = (1.20, 1.40, 1.60)
REQUIRED = {"article", "orientation", "pocket_radius_mm", "bore_diameter_mm",
            "writer_clearance_mm", "reader_offset_mm", "location", "stop",
            "fit_ok", "writer_ok", "reader_ok", "clearance_mm",
            "reader_margin_mm"}


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
        rows = list(csv.DictReader(stream))
    if not rows:
        raise SystemExit("results CSV is empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise SystemExit(f"missing columns: {', '.join(sorted(missing))}")
    failures = []
    for number, row in enumerate(rows, 2):
        if any(row[key].lower() != "true" for key in ("fit_ok", "writer_ok", "reader_ok")):
            failures.append(f"line {number}: functional gate false")
        if float(row["clearance_mm"]) < 0.10:
            failures.append(f"line {number}: clearance < 0.10 mm")
        if float(row["writer_clearance_mm"]) < 0.20:
            failures.append(f"line {number}: writer clearance < 0.20 mm")
        if float(row["reader_margin_mm"]) < 0.20:
            failures.append(f"line {number}: reader margin < 0.20 mm")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"checked {len(rows)} measured rows: provisional gates pass")


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
