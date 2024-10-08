from solid2 import union, OpenSCADObjectPlus
from models.pixel import create_pixel_holder


def pixel_holder_frame(
    *,
    pixel_width: float,
    pixel_height: float,
    pixel_wall_thickness: float,
    pixels_per_row: int,
    pixels_per_column: int
) -> OpenSCADObjectPlus:
    frame = union()
    for row in range(pixels_per_column):
        for col in range(pixels_per_row):
            frame += create_pixel_holder(
                width=pixel_width,
                height=pixel_height,
                wall_thickness=pixel_wall_thickness,
            ).translate([col * pixel_width, row * pixel_width, 0])

    return frame
