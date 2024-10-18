from pathlib import Path
import numpy as np
from models.pixel import create_pixel_slider, create_pixel_slider_with_label
from models.grid import create_pixel_holder_grid
from helpers.render import render_to_all_formats


########################################################################################
# Shape display dimensions.
# Use this file to configure the dimensions of the shape display.
# All dimensions are in millimeters (mm).
########################################################################################

# the width of a pixel, including both the pixel slider and the pixel holder.
PIXEL_WIDTH = 5
# the height of a pixel; TODO: related to range of motion of the pixel slider
PIXEL_HEIGHT = 50
# the number of pixels in a row
PIXELS_PER_ROW = 4
# the number of pixels in a column
PIXELS_PER_COLUMN = 4
# ncrease if the shape display is too weak; decrease this if you want to reduce the gaps between the pixels.
PIXEL_HOLDER_WALL_THICKNESS = 0.5

PIXEL_SLIDER_WIDTH_OFFSETS = [num / 10 for num in range(-30, 31, 1)]
RENDER_OUTPUT_DIRECTORY = Path("../output")


def render_pixel_sliders():
    for pixel_slider_width_offset in PIXEL_SLIDER_WIDTH_OFFSETS:
        pixel_slider_width = (
            PIXEL_WIDTH - PIXEL_HOLDER_WALL_THICKNESS * 2 + pixel_slider_width_offset
        )
        if pixel_slider_width > 0:
            name = f"pixel_slider_width_{pixel_slider_width:.1f}_mm"
            render_to_all_formats(
                model=create_pixel_slider(
                    width=pixel_slider_width, height=PIXEL_HEIGHT
                ),
                dir=RENDER_OUTPUT_DIRECTORY / "pixel_sliders",
                name=name,
            )
            render_to_all_formats(
                model=create_pixel_slider_with_label(
                    width=pixel_slider_width, height=PIXEL_HEIGHT
                ),
                dir=RENDER_OUTPUT_DIRECTORY / "pixel_sliders_with_label",
                name=f"{name}_with_label",
            )


def render_pixel_holder_grid():
    render_to_all_formats(
        model=create_pixel_holder_grid(
            pixel_width=PIXEL_WIDTH,
            pixel_height=PIXEL_HEIGHT,
            pixel_wall_thickness=PIXEL_HOLDER_WALL_THICKNESS,
            pixels_per_row=PIXELS_PER_ROW,
            pixels_per_column=PIXELS_PER_COLUMN,
        ),
        dir=RENDER_OUTPUT_DIRECTORY,
        name="pixel_holder_frame",
    )


def main():
    render_pixel_sliders()
    render_pixel_holder_grid()


if __name__ == "__main__":
    main()
