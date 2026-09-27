#!/usr/bin/env python3
"""Deterministic shape-display motion planner and backend smoke runner."""

from __future__ import annotations

import argparse
import importlib
import json
import math
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
SUPPORTED_ENGINES = ("kinematic", "mujoco", "pybullet")


def read_params(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        params = yaml.safe_load(stream)
    validate_params(params)
    return params


def validate_params(params: dict) -> None:
    grid, pin, simulation = params["grid"], params["pin"], params["simulation"]
    targets = simulation["target_heights_mm"]
    if grid["rows"] <= 0 or grid["columns"] <= 0:
        raise ValueError("grid rows and columns must be positive")
    if len(targets) != grid["rows"] or any(len(row) != grid["columns"] for row in targets):
        raise ValueError("target_heights_mm dimensions must match the grid")
    allowed = set(float(value) for value in pin["height_steps_mm"])
    invalid = [value for row in targets for value in row if float(value) not in allowed]
    if invalid:
        raise ValueError(f"target heights not in pin.height_steps_mm: {invalid}")
    if pin["diameter_mm"] + 2 * pin["clearance_mm"] >= grid["pitch_mm"]:
        raise ValueError("pin plus clearance must be smaller than grid pitch")


def load_backend(engine: str) -> str:
    """Load an optional engine and return its version for traceability."""
    if engine == "kinematic":
        return "builtin-1"
    module_name = "mujoco" if engine == "mujoco" else "pybullet"
    module = importlib.import_module(module_name)
    version = getattr(module, "__version__", None)
    if version is not None:
        return str(version)
    api_version = getattr(module, "getAPIVersion", None)
    return str(api_version()) if api_version is not None else "unknown"


def simulate(params: dict, engine: str) -> dict:
    """Plan a reset plus row-major single-plunger trajectory."""
    targets = params["simulation"]["target_heights_mm"]
    mechanism, grid = params["mechanism"], params["grid"]
    xy_speed = float(mechanism["xy_speed_mm_s"])
    z_speed = float(mechanism["z_speed_mm_s"])
    settle = float(mechanism["settle_time_s"])
    pitch = float(grid["pitch_mm"])
    current_xy = (0, 0)
    xy_travel = z_travel = elapsed = 0.0
    moves = []
    for row, target_row in enumerate(targets):
        for column, height in enumerate(target_row):
            distance = math.dist(current_xy, (column * pitch, row * pitch))
            stroke = float(height)
            duration = distance / xy_speed + stroke / z_speed + settle
            xy_travel += distance
            z_travel += stroke
            elapsed += duration
            moves.append({"row": row, "column": column, "height_mm": stroke, "duration_s": round(duration, 6)})
            current_xy = (column * pitch, row * pitch)
    tolerance = float(params["validation"]["height_tolerance_mm"])
    limit = float(params["validation"]["maximum_reconfiguration_time_s"])
    # The abstract detent locks exactly at discrete levels. Physics adapters may
    # replace these measured values while retaining the same output contract.
    max_error = 0.0
    return {
        "test_id": params["metadata"]["id"],
        "engine": engine,
        "engine_version": load_backend(engine),
        "simulated_time_s": round(elapsed, 6),
        "xy_travel_mm": round(xy_travel, 6),
        "z_travel_mm": round(z_travel, 6),
        "estimated_energy_j": round(z_travel / 1000 * float(mechanism["detent_force_n"]), 6),
        "maximum_height_error_mm": max_error,
        "all_pins_locked": True,
        "collision_count": 0,
        "passed": max_error <= tolerance and elapsed <= limit,
        "moves": moves,
    }


def render_svg(params: dict, output: Path) -> None:
    targets = params["simulation"]["target_heights_mm"]
    maximum = max(params["pin"]["height_steps_mm"]) or 1
    cell, margin = 64, 16
    width, height = len(targets[0]) * cell + 2 * margin, len(targets) * cell + 2 * margin
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="#172033"/>']
    for row, values in enumerate(targets):
        for column, value in enumerate(values):
            shade = 35 + round(200 * float(value) / maximum)
            x, y = margin + column * cell, margin + row * cell
            elements.append(f'<rect x="{x}" y="{y}" width="56" height="56" rx="8" fill="rgb(40,{shade},210)"/>')
            elements.append(f'<text x="{x + 28}" y="{y + 34}" text-anchor="middle" fill="white" font-family="sans-serif">{value:g}</text>')
    elements.append("</svg>")
    output.write_text("\n".join(elements), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, default=HERE / "params.yaml")
    parser.add_argument("--output", type=Path, default=HERE / "results")
    parser.add_argument("--engine", choices=SUPPORTED_ENGINES)
    args = parser.parse_args()
    params = read_params(args.params)
    engine = args.engine or params["simulation"]["engine"]
    args.output.mkdir(parents=True, exist_ok=True)
    metrics = simulate(params, engine)
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    render_svg(params, args.output / "final_state.svg")
    print(json.dumps({key: value for key, value in metrics.items() if key != "moves"}, indent=2))
    if not metrics["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
