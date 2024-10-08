from environs import Env
from pathlib import Path
import numpy as np
from models.pixel import (
    create_pixel_slider,
    create_pixel_slider_with_label,
    create_pixel_holder,
)
from models.grid import create_pixel_holder_grid
from helpers.render import render_to_all_formats


# Import the environment variables
env = Env()
env.read_env(path="./dimensions.env")


# Define the shape display dimensions
PIXEL_WIDTH = env.float("PIXEL_WIDTH")
PIXEL_SLIDER_WIDTH_OFFSETS = np.arange(-3, 3.1, 0.1).tolist()
PIXEL_HEIGHT = env.float("PIXEL_HEIGHT")
PIXELS_PER_ROW = env.int("PIXELS_PER_ROW")
PIXELS_PER_COLUMN = env.int("PIXELS_PER_COLUMN")
PIXEL_HOLDER_WALL_THICKNESS = env.float("PIXEL_HOLDER_WALL_THICKNESS")
RENDER_OUTPUT_DIRECTORY = Path("../output")


def render_pixel_sliders():
    for pixel_slider_width_offset in PIXEL_SLIDER_WIDTH_OFFSETS:
        pixel_slider_width = (
            PIXEL_WIDTH - PIXEL_HOLDER_WALL_THICKNESS * 2 + pixel_slider_width_offset
        )
        name = f"pixel_slider_width_{pixel_slider_width:.1f}_mm"
        render_to_all_formats(
            model=create_pixel_slider(width=pixel_slider_width, height=PIXEL_HEIGHT),
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


def render_pixel_holder():
    render_to_all_formats(
        model=create_pixel_holder(
            width=PIXEL_WIDTH,
            height=PIXEL_HEIGHT,
            wall_thickness=PIXEL_HOLDER_WALL_THICKNESS,
        ),
        dir=RENDER_OUTPUT_DIRECTORY,
        name="pixel_holder",
    )


def render_pixel_holder_grid():
    render_to_all_formats(
        model=create_pixel_holder_grid(
            pixel_width=PIXEL_WIDTH * PIXELS_PER_ROW,
            pixel_height=PIXEL_HEIGHT * PIXELS_PER_COLUMN,
            pixel_wall_thickness=PIXEL_HOLDER_WALL_THICKNESS,
            pixels_per_row=PIXELS_PER_ROW,
            pixels_per_column=PIXELS_PER_COLUMN,
        ),
        dir=RENDER_OUTPUT_DIRECTORY,
        name="pixel_holder_frame",
    )


def main():
    render_pixel_sliders()
    render_pixel_holder()
    render_pixel_holder_grid()


if __name__ == "__main__":
    main()
