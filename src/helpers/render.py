import os
import subprocess
from pathlib import Path
from solid2 import OpenSCADObjectPlus, scad_render, scad_render_to_file


def render_to_scad_file(*, model: OpenSCADObjectPlus, file_path: Path) -> None:
    try:
        scad_render_to_file(model, file_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def render_to_stl_file(*, model: OpenSCADObjectPlus, file_path: Path) -> None:
    try:
        process = subprocess.run(
            ["openscad", "-o", str(file_path), "-"],
            input=scad_render(model).encode("utf-8"),
            check=True,
        )
    except (Exception, subprocess.CalledProcessError) as e:
        print(f"An error occurred: {e}")


def render_to_all_formats(*, model: OpenSCADObjectPlus, dir: Path, name: str) -> None:
    os.makedirs(dir, exist_ok=True)
    print(f"> Creating SCAD file: {name}")
    render_to_scad_file(model=model, file_path=dir / f"{name}.scad")
    print(f"> Creating STL file: {name}")
    render_to_stl_file(model=model, file_path=dir / f"{name}.stl")
