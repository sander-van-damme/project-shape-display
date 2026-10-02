#!/usr/bin/env python3
"""part set; CAD/calculation source, no physical validation."""
from __future__ import annotations

from dataclasses import dataclass, field

# --- machine layout (mirror of s5r_parts_common.scad) ------------------------
PITCH_MM = 5.08
ROWS_FULL = 80
COLS = 80
BANK_ROWS = 4
CARTRIDGE_COLS = 27          # 27 * 5.08 = 137.16 mm (<= ~150 mm support spacing)
CARTRIDGE_ROWS = 27
CARTS_PER_AXIS = 3           # ceil(80 / 27) = 3 -> 81 columns across
FIELD_COLS = CARTS_PER_AXIS * CARTRIDGE_COLS   # 81 (1 spare column of 80 used)

# --- sourced FDM process limits (tools/fdm-limits/fdm_process_limits.py) ------
NOZZLE_MM = 0.4
LAYER_MM = 0.20
EXTRUSION_W_MM = 1.1 * NOZZLE_MM      # 0.44 one extrusion line
MIN_FEATURE_MM = EXTRUSION_W_MM
MIN_WALL_MM = 2.0 * EXTRUSION_W_MM    # 0.88 two lines
BED_MM = 256.0
PLA_DENSITY_G_CM3 = 1.24              # sourced typical PLA solid density


@dataclass
class Part:
    """One distinct printed part of the S5-R machine."""
    key: str                 # STL / selector name
    scad_part: str           # `part=` value in s5r_parts.scad
    title: str
    qty: int
    material: str = "PLA"
    nozzle_mm: float = NOZZLE_MM
    layer_mm: float = LAYER_MM
    orientation: str = ""
    supports: str = "none"
    # sourced-limit citation: (feature, value_mm, limit_mm, rule, verdict)
    critical_feature: tuple = ()
    note: str = ""
    # design calculation: every structural part now renders at its TRUE full-tile size.
    # `analytic_envelope_mm` is retained only as a cross-check of the rendered
    # bbox; `solid_volume_mm3` is the real mesh volume for the mass line.
    analytic_envelope_mm: tuple | None = None
    solid_volume_mm3: float | None = None
    # Set ONLY when a part's committed STL is still a reduced representative of a
    # larger part. Empty string means the STL is the real, full-size part.
    # Non-empty must name the documented sub-tile print route (see design calculation).
    witness_of: str = ""
    subtile_route: str = ""

    @property
    def lines(self) -> float:
        if not self.critical_feature:
            return float("nan")
        return self.critical_feature[1] / MIN_FEATURE_MM


# ---------------------------------------------------------------------------
# THE PRINTED PART SET. Quantities are for ONE full machine (80x80 field, R=4).
# ---------------------------------------------------------------------------
PARTS: list[Part] = [
    Part(
        "cell_cartridge", "cell_cartridge", "cell cartridge (27x27 cell tube block)",
        qty=CARTS_PER_AXIS * CARTS_PER_AXIS,   # 3x3 = 9 cartridges = 81x81 cells
        orientation="floor DOWN, cells open +Z; frame lip up",
        supports="none (all walls vertical; bores vertical)",
        critical_feature=("cell wall / pawl chamber (WALL)", 0.90, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        analytic_envelope_mm=(CARTRIDGE_COLS * PITCH_MM,
                              CARTRIDGE_ROWS * PITCH_MM, 14.0),
        solid_volume_mm3=141347.5,
        note="design calculation: committed STL is the TRUE full 27x27 block = 729 cells "
             "(137.16 x 137.16 x 14 mm, single watertight solid). Mass is the "
             "real mesh solid volume (upper bound). A 3x3 sub-tile route "
             "(9x9 cells, 45.72 mm) is documented for a <137 mm bed.",
    ),
    Part(
        "rotor", "rotor", "5-level stepped rotor cam", qty=COLS * ROWS_FULL,
        orientation="axis +Z (upright)",
        supports="none (round, self-supporting)",
        critical_feature=("rotor core diameter (2 x 1.0)", 2.00, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        solid_volume_mm3=3.14159 * (1.5 ** 2 * 2.0 + 1.0 ** 2 * 5.0),
        note="6400 cells; the printed height memory. Unchanged S5 geometry.",
    ),
    Part(
        "drive_pawl", "drive_pawl", "drive pawl (load-bearing cantilever)", qty=COLS * ROWS_FULL,
        orientation="cantilever Z, tip down; flat on its 0.70 face",
        supports="none",
        critical_feature=("pawl leaf thickness (PAWL_T)", 0.90, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        solid_volume_mm3=0.90 * 0.70 * 8.0 + 1.40 * 1.20 * 1.60,
        note="6400 cells; the load-bearing leaf (design calculation keeps it 2 lines).",
    ),
    Part(
        "keeper", "keeper", "keeper latch (leaf + 5-gate nose + compression shoulder)",
        qty=COLS * ROWS_FULL,
        orientation="leaf upright; shoulder bearing DOWN",
        supports="none",
        critical_feature=("keeper leaf thickness (KEEPER_T)", 0.90, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        solid_volume_mm3=0.90 * 0.90 * 4.0 + 5 * 0.20 * 0.90 * 0.15
                         + 0.90 * 0.50 * 0.50,
        note="6400 cells; design calculation re-profile (was 0.45 mm = 1 line RISK).",
    ),
    Part(
        "detent_leaf", "detent_leaf", "rotor detent leaf (0.40 mm scallop)", qty=COLS * ROWS_FULL,
        orientation="leaf upright, scallop toward rotor",
        supports="none",
        critical_feature=("detent leaf wall", 0.90, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        solid_volume_mm3=0.90 * 0.70 * 6.0,
        note="6400 cells; K2 detent (design calculation/45).",
    ),
    Part(
        "rack_strip", "rack_strip", "printed rack strip (clamps to sourced rod)",
        qty=BANK_ROWS * CARTS_PER_AXIS,   # 4 rows x 3 modules per bank pass
        orientation="teeth UP, base web DOWN",
        supports="none (teeth on top)",
        critical_feature=("rack tooth gap (pitch - tooth)", 0.50, MIN_FEATURE_MM,
                          "min standalone feature (1 line)", "PASS"),
        note="Rack pitch 1.00 / tooth 0.50 mm (design calculation corrected). Rod is sourced.",
    ),
    Part(
        "bank_drive_housing", "bank_drive_housing", "bank drive housing (2 motors + pinion)",
        qty=1,
        orientation="motor bosses horizontal, bed flat on the base",
        supports="none (bores vertical in print orientation)",
        critical_feature=("housing wall (60-2x11-... )", 18.0, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="Carries the 2 bank motors + pinion; the sourced rod passes through.",
    ),
    Part(
        "reset_comber", "reset_comber", "reset comber (rake tines)", qty=BANK_ROWS - 1,
        orientation="body rail DOWN, tines +Z",
        supports="none",
        critical_feature=("comber tine thickness", 0.90, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="One comber per bank group (20 groups) -> 3 tines each.",
    ),
    Part(
        "writer_carriage", "writer_carriage", "writer carriage (40 stations)",
        qty=1,
        orientation="pockets +Z, travels in X",
        supports="none (pockets vertical)",
        critical_feature=("carriage wall", 1.20, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="40 writer solenoid pockets in 8 stations; off the dense field.",
    ),
    Part(
        "platen_module", "platen_module", "platen lift module (27x27 tile)",
        qty=CARTS_PER_AXIS * CARTS_PER_AXIS,
        orientation="plate flat, ribs UP",
        supports="none",
        critical_feature=("stiffening rib width", 3.00, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        analytic_envelope_mm=(CARTRIDGE_COLS * PITCH_MM,
                              CARTRIDGE_ROWS * PITCH_MM, 7.0),
        solid_volume_mm3=80539.5,
        note="design calculation: committed STL is the TRUE full 27x27 plate "
             "(137.16 x 137.16 x 7 mm, single watertight solid); it was already "
             "full geometry in design calculation and is now labelled as such. Supports the "
             "column field; <= ~150 mm spacing (design calculation flatness).",
    ),
    Part(
        "lift_frame_rail", "lift_frame_rail", "lift frame rail (module joiner)",
        qty=2 * (CARTS_PER_AXIS + 1) * 2,
        orientation="rail lengthwise on bed, pockets UP",
        supports="none",
        critical_feature=("rail wall / pocket wall", 6.00, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="Joins the 3x3 module array into a spliced frame.",
    ),
    Part(
        "guide_bracket", "guide_bracket", "guide-rod / lead-screw bracket", qty=8,
        orientation="bores horizontal, bracket on its back face",
        supports="none",
        critical_feature=("bracket wall (16-2x(4.2+... ))", 3.00, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="Mounts guide rods + lift screws (design calculation Step-6 layout).",
    ),
    Part(
        "solenoid_mount", "solenoid_mount", "writer solenoid pocket plate",
        qty=1,
        orientation="pockets vertical",
        supports="none",
        critical_feature=("pocket plate wall", 1.20, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="One 8-pocket plate per writer station (8 stations).",
    ),
    Part(
        "comber_cam", "comber_cam", "comber drive cam", qty=1,
        orientation="axis +Z, flat",
        supports="none",
        critical_feature=("cam web", 2.80, MIN_WALL_MM,
                          "min robust wall (2 lines)", "PASS"),
        note="Converts the bank reverse pass into the comber Z swing.",
    ),
]

PARTS_BY_KEY = {p.key: p for p in PARTS}


def total_parts() -> int:
    return sum(p.qty for p in PARTS)


def mass_g(part: Part) -> float | None:
    """Rough solid mass from the analytic volume (upper bound; PLA density)."""
    if part.solid_volume_mm3 is None:
        return None
    return part.solid_volume_mm3 * part.qty * PLA_DENSITY_G_CM3 / 1000.0


if __name__ == "__main__":
    print(f"{len(PARTS)} distinct printed parts, {total_parts()} pieces total")
    for p in PARTS:
        m = mass_g(p)
        mstr = f"{m:.1f} g" if m is not None else "n/a (witness block)"
        print(f"  {p.key:<22} x{p.qty:<6} {p.critical_feature[3]:<34} {mstr}")
