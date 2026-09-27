from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "tests" / "template"


def load_simulation():
    spec = importlib.util.spec_from_file_location("shape_display_simulation", TEMPLATE / "simulation.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_template_produces_passing_machine_readable_results(tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(TEMPLATE / "simulation.py"), "--output", str(tmp_path)],
        cwd=ROOT,
        check=True,
    )
    metrics = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["passed"] is True
    assert metrics["collision_count"] == 0
    assert len(metrics["moves"]) == 9
    assert (tmp_path / "final_state.svg").read_text(encoding="utf-8").startswith("<svg")


def test_invalid_target_dimensions_are_rejected() -> None:
    simulation = load_simulation()
    params = simulation.read_params(TEMPLATE / "params.yaml")
    params["simulation"]["target_heights_mm"] = [[0.0]]
    with pytest.raises(ValueError, match="dimensions"):
        simulation.validate_params(params)


def test_ci_workflow_uses_the_root_dependency_file_for_its_cache() -> None:
    """Prevent setup-python from selecting a legacy trial requirements file."""
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    jobs = workflow["jobs"]
    setup_steps = [
        step
        for job in jobs.values()
        for step in job["steps"]
        if step.get("uses", "").startswith("actions/setup-python@")
    ]
    assert setup_steps
    assert all(step["with"]["cache-dependency-path"] == "requirements-dev.txt" for step in setup_steps)
