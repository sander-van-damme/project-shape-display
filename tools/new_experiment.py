#!/usr/bin/env python3
"""Create a numbered shape-display experiment from the maintained template."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"test\d{2}_[a-z0-9_]+$")


def create_experiment(name: str) -> Path:
    if not NAME_PATTERN.fullmatch(name) or name == "test00_template":
        raise ValueError("name must match testNN_short_description")
    destination = ROOT / "experiments" / name
    if destination.exists():
        raise FileExistsError(f"experiment already exists: {destination}")
    shutil.copytree(ROOT / "experiments" / "template", destination, ignore=shutil.ignore_patterns("results"))
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="testNN_short_description")
    args = parser.parse_args()
    destination = create_experiment(args.name)
    print(f"Created {destination.relative_to(ROOT)}; update its README and params.yaml")


if __name__ == "__main__":
    main()
