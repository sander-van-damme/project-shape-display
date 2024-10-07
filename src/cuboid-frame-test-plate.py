"""
 © 2024 Sander Van Damme - All Rights Reserved.

This script outputs OpenSCAD code for a cuboid frame test plate.
It creates slots with different offset options to test the fit of a cuboid.
The test plate dimensions are based on the following environment variables:

- CUBOID_WIDTH: Width of the cuboid
"""

from environs import Env
from solid2 import cube, translate, linear_extrude, text

# Initialize the environment variables
env = Env()
env.read_env()

# Define the label dimensions
LABEL_FONT = "Arial"
LABEL_HEIGHT = 1
LABEL_SIZE = 6

# Define the slot dimensions
SLOT_WIDTH = env.float("CUBOID_WIDTH")
SLOT_MARGIN = 10
SLOT_WIDTH_OFFSET_OPTIONS = [1, 1.4, 1.8, 2.2, 2.6, 3]
SLOT_COUNT = len(SLOT_WIDTH_OFFSET_OPTIONS)

# Define the test plate dimensions
TEST_PLATE_HEIGHT = 5
TEST_PLATE_WIDTH = (
    SLOT_WIDTH * SLOT_COUNT
    + SLOT_MARGIN * (SLOT_COUNT + 1)
    + sum(offset for offset in SLOT_WIDTH_OFFSET_OPTIONS)
)
TEST_PLATE_DEPTH = SLOT_WIDTH + 2 * SLOT_MARGIN

# Create the test plate
test_plate = cube([TEST_PLATE_WIDTH, TEST_PLATE_DEPTH, TEST_PLATE_HEIGHT])

# Starting position for the first slot
x_pos = SLOT_MARGIN
y_pos = SLOT_MARGIN

# Loop through each offset option to create slots and labels
for slot_offset in SLOT_WIDTH_OFFSET_OPTIONS:
    # Create the slot
    slot_width = SLOT_WIDTH + slot_offset
    slot = cube([slot_width, slot_width, TEST_PLATE_HEIGHT + 0.2])
    slot = translate([x_pos, y_pos, -0.1])(slot)
    test_plate -= slot

    # Create the label for the slot
    label_text = f"{slot_offset:.1f}"
    label = linear_extrude(height=LABEL_HEIGHT)(
        text(text=label_text, size=LABEL_SIZE, font=LABEL_FONT, halign="center")
    )
    label = translate(
        [
            x_pos + slot_width / 2,
            y_pos - LABEL_SIZE - 2,
            TEST_PLATE_HEIGHT,
        ]
    )(label)
    test_plate += label

    # Update x position for the next slot
    x_pos += slot_width + SLOT_MARGIN

# Print the test plate
print(test_plate)
