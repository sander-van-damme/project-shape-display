#!/usr/bin/env python3
from ShapeDisplay import *

sd = ShapeDisplay(80, 16)

sd.hole_radius = 4
sd.export(format='openscad')
sd.export(format='stl')
