"""
© 2024 Sander Van Damme - All Rights Reserved.

This script outputs OpenSCAD code for the cuboid frame.
"""

from environs import Env
from solid2 import cube, translate

# Initialize the environment variables
env = Env()
env.read_env()

# Define the slot dimensions
SLOT_WIDTH = env.float("CUBOID_WIDTH") + env.float("CUBOID_FRAME_SLOT_WIDTH_OFFSET")
SLOT_MARGIN = env.float("CUBOID_FRAME_SLOT_MARGIN")

# Define the actuator slot dimensions
ACTUATOR_SLOT_WIDTH = SLOT_WIDTH / 2

# Define the frame dimensions
FRAME_ROW_COUNT = env.int("CUBOID_FRAME_ROW_COUNT")
FRAME_COLUMN_COUNT = env.int("CUBOID_FRAME_COLUMN_COUNT")
FRAME_WIDTH = FRAME_COLUMN_COUNT * SLOT_WIDTH + SLOT_MARGIN * (FRAME_COLUMN_COUNT + 1)
FRAME_DEPTH = FRAME_ROW_COUNT * SLOT_WIDTH + SLOT_MARGIN * (FRAME_ROW_COUNT + 1)

# Add bottom thickness to frame height
FRAME_BOTTOM_HEIGHT = env.float("CUBOID_FRAME_BOTTOM_HEIGTH")
FRAME_HEIGHT = env.float("CUBOID_HEIGHT") + FRAME_BOTTOM_HEIGHT

# Create the frame
frame = cube([FRAME_WIDTH, FRAME_DEPTH, FRAME_HEIGHT])

# Loop through each row and column to create the slots and actuator slots
for row in range(FRAME_ROW_COUNT):
    for col in range(FRAME_COLUMN_COUNT):
        x_pos = SLOT_MARGIN + col * (SLOT_WIDTH + SLOT_MARGIN)
        y_pos = SLOT_MARGIN + row * (SLOT_WIDTH + SLOT_MARGIN)
        
        # Create the slot (main slot where the cuboid sits)
        slot_depth = FRAME_HEIGHT - FRAME_BOTTOM_HEIGHT + 0.2  # Extend depth by 0.2mm
        slot = cube([SLOT_WIDTH, SLOT_WIDTH, slot_depth])
        slot = translate([x_pos, y_pos, FRAME_BOTTOM_HEIGHT - 0.1])(slot)  # Lower by 0.1mm
        frame -= slot
        
        # Create the actuator slot in the bottom
        actuator_slot_depth = FRAME_BOTTOM_HEIGHT + 0.2  # Extend depth by 0.2mm
        actuator_slot_x = x_pos + (SLOT_WIDTH - ACTUATOR_SLOT_WIDTH) / 2
        actuator_slot_y = y_pos + (SLOT_WIDTH - ACTUATOR_SLOT_WIDTH) / 2
        actuator_slot = cube([ACTUATOR_SLOT_WIDTH, ACTUATOR_SLOT_WIDTH, actuator_slot_depth])
        actuator_slot = translate([actuator_slot_x, actuator_slot_y, -0.1])(actuator_slot)  # Lower by 0.1mm
        frame -= actuator_slot

# Print the frame
print(frame)
