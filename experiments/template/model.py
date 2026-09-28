#!/usr/bin/env python3
"""Build the template square-column grid with CadQuery from params.yaml."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent


def read_params(path: Path) -> dict:
    """Load parameters shared by CAD and simulation."""
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def make_column(cq, width_mm: float, depth_mm: float, height_mm: float):
    """Create one rectangular display column standing on the XY plane."""
    return cq.Workplane("XY").rect(width_mm, depth_mm).extrude(height_mm)


def make_grid(cq, params: dict):
    """Create a compound containing the guide plate and all zeroed columns."""
    grid = params["grid"]
    column_params = params["column"]
    columns, rows, pitch = grid["columns"], grid["rows"], grid["pitch_mm"]
    guide_width = columns * pitch
    guide_depth = rows * pitch
    clearance = column_params["clearance_mm"]
    hole_width = column_params["width_mm"] + 2 * clearance
    hole_depth = column_params["depth_mm"] + 2 * clearance
    guide = cq.Workplane("XY").box(guide_width, guide_depth, 2.0)

    for row in range(rows):
        for column in range(columns):
            x = (column - (columns - 1) / 2) * pitch
            y = (row - (rows - 1) / 2) * pitch
            hole = (
                cq.Workplane("XY")
                .center(x, y)
                .rect(hole_width, hole_depth)
                .extrude(2.0)
            )
            guide = guide.cut(hole)

    display_columns = []
    for row in range(rows):
        for column in range(columns):
            x = (column - (columns - 1) / 2) * pitch
            y = (row - (rows - 1) / 2) * pitch
            display_columns.append(
                make_column(
                    cq,
                    column_params["width_mm"],
                    column_params["depth_mm"],
                    column_params["body_height_mm"],
                ).translate((x, y, 1.0))
            )

    return cq.Compound.makeCompound(
        [guide.val(), *(part.val() for part in display_columns)]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, default=HERE / "params.yaml")
    parser.add_argument("--output", type=Path, default=HERE / "results")
    args = parser.parse_args()
    cq = importlib.import_module("cadquery")
    params = read_params(args.params)
    assembly = make_grid(cq, params)
    args.output.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(assembly, str(args.output / "model.step"))
    cq.exporters.export(assembly, str(args.output / "model.stl"))
    print(f"Exported model.step and model.stl to {args.output}")


if __name__ == "__main__":
    main()
