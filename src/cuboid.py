"""
© 2024 Sander Van Damme - All Rights Reserved.

This script outputs OpenSCAD code for a rectangular cuboid.
"""

from solid2 import cube
from helpers.dimensions import cuboid_width, cuboid_height

cuboid = cube([cuboid_width, cuboid_width, cuboid_height])
print(cuboid)
