#!/usr/bin/env python
# © 2024 Sander Van Damme - All Rights Reserved.

from pathlib import Path
from solid2 import OpenSCADObjectPlus
from environs import Env
import numpy as np
from models.pixel import create_pixel_slider, create_pixel_slider_with_label, create_pixel_holder
from models.frame import pixel_holder_frame
from helpers.render import render_to_all_formats

# Initialize the environment variables
env = Env()
env.read_env(path="./dimensions.env")

PIXEL_WIDTH = env.float("PIXEL_WIDTH")
PIXEL_WIDTH_OFFSETS = [0]  # np.arange(-3, 3.1, 0.1).tolist()
PIXEL_HEIGHT = env.float("PIXEL_HEIGHT")
PIXELS_PER_ROW = env.int("PIXELS_PER_ROW")
PIXELS_PER_COLUMN = env.int("PIXELS_PER_COLUMN")
PIXEL_HOLDER_WALL_THICKNESS = env.float("PIXEL_HOLDER_WALL_THICKNESS")
OUTPUT_DIRECTORY = Path("../output")


def main():

    # PIXEL SLIDERS
    for pixel_width_offset in PIXEL_WIDTH_OFFSETS:
        pixel_width = PIXEL_WIDTH + pixel_width_offset
        name = f"pixel_slider_width_{pixel_width:.1f}_mm"
        render_to_all_formats(
            model=create_pixel_slider(width=pixel_width, height=PIXEL_HEIGHT),
            dir=OUTPUT_DIRECTORY / "pixel_sliders",
            name=name,
        )
        render_to_all_formats(
            model=create_pixel_slider_with_label(width=pixel_width, height=PIXEL_HEIGHT),
            dir=OUTPUT_DIRECTORY / "pixel_sliders_with_label",
            name=f"{name}_with_label",
        )

    # PIXEL HOLDER
    render_to_all_formats(
        model=create_pixel_holder(
            width=PIXEL_WIDTH,
            height=PIXEL_HEIGHT,
            wall_thickness=PIXEL_HOLDER_WALL_THICKNESS,
        ),
        dir=OUTPUT_DIRECTORY,
        name="pixel_holder",
    )

    # PIXEL HOLDER FRAME
    render_to_all_formats(
        model=pixel_holder_frame(
            pixel_width=PIXEL_WIDTH * PIXELS_PER_ROW,
            pixel_height=PIXEL_HEIGHT * PIXELS_PER_COLUMN,
            pixel_wall_thickness=PIXEL_HOLDER_WALL_THICKNESS,
            pixels_per_row=PIXELS_PER_ROW,
            pixels_per_column=PIXELS_PER_COLUMN,
        ),
        dir=OUTPUT_DIRECTORY,
        name="pixel_holder_frame",
    )


if __name__ == "__main__":
    main()
