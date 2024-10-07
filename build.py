#!/usr/bin/env python
# © 2024 Sander Van Damme - All Rights Reserved.

import os
import subprocess
from pathlib import Path

# Directories
SRC_DIR = Path("./src")
DIST_DIR = Path("./dist")

# Ensure directories exist
os.makedirs(DIST_DIR, exist_ok=True)

# Iterate through all Python scripts in the src directory
for name, path in [(path.stem, path) for path in SRC_DIR.iterdir()]:
    if str(path).endswith(".scad.py"):
        try:
            # Create the SCAD file
            print(f"Creating SCAD file for {name}.")
            result = subprocess.run(["python", path], capture_output=True, text=True)
            scad_code = result.stdout
            scad_file = os.path.join(DIST_DIR, f"{name}.scad")
            with open(scad_file, "w") as f:
                f.write(scad_code)

            # Create the STL file
            print(f"Creating STL file for {name}.")
            stl_file = os.path.join(DIST_DIR, f"{name}.stl")
            subprocess.run(["openscad", "-o", stl_file, scad_file], check=True)

        except (Exception, subprocess.CalledProcessError) as e:
            print(f"An error occurred: {e}")
