from solid2 import cube, text, OpenSCADObjectPlus


def create_pixel_slider(*, width: float, height: float) -> OpenSCADObjectPlus:
    return cube([width, width, height])


def create_pixel_slider_with_label(
    *, width: float, height: float
) -> OpenSCADObjectPlus:
    pixel = create_pixel_slider(width=width, height=height)
    label = (
        text(f"{width:.2f}", size=10, direction="ttb")
        .linear_extrude(width / 5)
        .rotate([90, 0, 0])
        .resize([width / 2, 0, height / 10])
        .translate([width / 2, 0.1, height / 2])
    )
    return pixel - label


def create_pixel_holder(
    *, width: float, height: float, wall_thickness: float
) -> OpenSCADObjectPlus:
    outer_cube = cube([width, width, height])
    inner_cube = cube(
        [width - 2 * wall_thickness, width - 2 * wall_thickness, height + 0.2]
    ).translate([wall_thickness, wall_thickness, -0.1])
    return outer_cube - inner_cube
