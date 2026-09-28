#!/usr/bin/env python3
"""Emit the S1 threshold-ratchet replacement coupon as printable solids.

Supersedes the DND-8 CAD-source-only emission. See README section
"Why the first coupon was not printable" for the hostile review.

Design resolution found while building this (a real result, not a parameter):
a single 5.08 mm X-lane cannot hold BOTH the pawl (0.80 mm) and the gate bar
(0.80 mm) beside a printable column body with printable walls. The first
coupon hid them side by side and silently overran the pitch. Fix: the gate bar
is STACKED ABOVE the pawl in Z, in the same X/Y lane, so the X budget only has
to fit the pawl. The pitch budget then closes with a 3.60 mm body:
    3.60 body + 1.48 lane (0.80 pawl + 0.20 clearance + 0.48 rail) = 5.08.
Rack pocket 2.40 W x 1.20 D on the 3.60 body leaves 0.60 mm side rails and a
2.40 mm web, all >= the 0.40 mm FDM minimum.

Parts (separate, printable, assemble):
  frame              - base plate + per-cell guide sleeves + pawl root blocks
                       + gate guide slots + threshold-plate end rails
  column             - visible cap + racked body, straight extrusion
  pawl               - flat cantilever with a wedge toe (prints in Y-Z plane)
  gate_bar           - thin vertical bar that slides in the frame slot
  threshold_plate    - horizontal bar with bosses over armed cells

CAD solid geometry. NOT fabrication or physical validation.
"""

from __future__ import annotations

from pathlib import Path
import json

# ---- fixed project scale ---------------------------------------------------
PITCH = 5.08
NX = 5
NY = 3
LEVELS = 5
TRAVEL = 40.0

# ---- printable dimensions (checked in make_manifest) -----------------------
COL_CAP_W = 4.72      # visible cap
COL_BODY_W = 3.60     # necked body; leaves 1.48 mm lane
COL_H = 44.0
CAP_OVERHANG = (COL_CAP_W - COL_BODY_W) / 2   # 0.56

RACK_PITCH = 10.0
RACK_N = LEVELS
POCKET_W = 2.40
POCKET_D = 1.20
POCKET_H = 2.00

PAWL_T = 0.80         # 2 walls
PAWL_ROOT_L = 2.40
PAWL_FREE_L = 3.60
PAWL_H = 1.60

GATE_T = 0.80         # stacked above the pawl, same lane
GATE_H = 3.00
GATE_TRAVEL = 1.40    # > pocket depth, so the toe is fully cleared
GATE_Z0 = 1.60        # bottom of gate bar above the base (above pawl root)

PLATE_T = 1.20
PLATE_BOSS_H = 1.00
PLATE_GAP = 0.20

BLEED = 0.20
BASE_T = 3.00
RAIL_W = 1.60
MIN_WALL = 0.40

PARAMS = {
    "pitch_mm": PITCH, "nx": NX, "ny": NY, "levels": LEVELS, "travel_mm": TRAVEL,
    "column_cap_mm": COL_CAP_W, "column_body_mm": COL_BODY_W,
    "column_height_mm": COL_H, "cap_overhang_mm": CAP_OVERHANG,
    "rack_pitch_mm": RACK_PITCH, "rack_pockets": RACK_N,
    "pocket_depth_mm": POCKET_D, "pocket_width_mm": POCKET_W,
    "pawl_thickness_mm": PAWL_T, "gate_bar_thickness_mm": GATE_T,
    "gate_travel_mm": GATE_TRAVEL, "plate_thickness_mm": PLATE_T,
    "min_fdm_wall_mm": MIN_WALL, "base_thickness_mm": BASE_T,
    "clearance_mm": BLEED,
    "provenance": "S1 hypothesis; printable CAD solids; not measured",
}


def make_manifest() -> dict:
    """Check the pitch budget closes with printable walls; return a manifest."""
    lane = PITCH - COL_BODY_W
    pawl_lane_need = PAWL_T + BLEED
    rails = (COL_BODY_W - POCKET_W) / 2
    web = COL_BODY_W - POCKET_D
    gate_fits = GATE_T <= lane
    rail_w = (PITCH - POCKET_W) / 2 if POCKET_W < PITCH else -1
    checks = {
        "lane_beside_body_mm": round(lane, 3),
        "pawl_lane_need_mm": round(pawl_lane_need, 3),
        "pawl_fits_lane": pawl_lane_need <= lane,
        "rack_side_rails_mm": round(rails, 3),
        "rack_rails_printable": rails >= MIN_WALL,
        "web_behind_pocket_mm": round(web, 3),
        "web_printable": web >= MIN_WALL,
        "gate_fits_lane": gate_fits,
        "gate_travel_clears_pocket": GATE_TRAVEL > POCKET_D,
        "column_height_covers_travel": COL_H >= TRAVEL + BASE_T,
        "all_printable": all([
            pawl_lane_need <= lane,
            rails >= MIN_WALL,
            web >= MIN_WALL,
            gate_fits,
            GATE_TRAVEL > POCKET_D,
            COL_H >= TRAVEL + BASE_T,
        ]),
    }
    return {"params": PARAMS, "checks": checks,
            "pitch_partition_mm": {
                "body": COL_BODY_W, "lane": lane, "sum": COL_BODY_W + lane}}

# ---- box -> triangles ------------------------------------------------------
def _box_tris(lo, hi):
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
         (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
         (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return [(v[a], v[b], v[c]) for a, b, c in f]


def write_stl(path: Path, boxes) -> int:
    """Write a binary STL from a list of (lo, hi) axis-aligned boxes."""
    import struct
    tris = []
    for lo, hi in boxes:
        tris.extend(_box_tris(lo, hi))
    with path.open("wb") as fh:
        fh.write(b"\x00" * 80)
        fh.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            fh.write(struct.pack("<3f", 0.0, 0.0, 0.0))
            for pt in (a, b, c):
                fh.write(struct.pack("<3f", *pt))
            fh.write(struct.pack("<H", 0))
    return len(tris)


# ---- part geometry (axis-aligned boxes, origin at each part's lower corner) -
def frame_boxes():
    sx, sy = NX * PITCH, NY * PITCH
    b = []
    # base plate
    b.append(((0, 0, 0), (sx, sy, BASE_T)))
    # threshold-plate end rails (grow straight up, no overhang)
    rail_z = BASE_T + COL_H + 0.2
    for rx in (0.0, sx - RAIL_W):
        b.append(((rx, 0, BASE_T), (rx + RAIL_W, sy, rail_z + PLATE_T)))
    # per-cell guide sleeves + pawl root blocks + gate slots
    sw = 1.0
    for i in range(NX):
        for j in range(NY):
            ox, oy = i * PITCH, j * PITCH
            bx = ox + (PITCH - COL_BODY_W) / 2
            by = oy + (PITCH - COL_BODY_W) / 2
            # two sleeve walls on -X and +X of the body, grounded on base
            b.append(((bx - sw, by - sw, BASE_T),
                      (bx, by + COL_BODY_W + sw, BASE_T + COL_H * 0.5)))
            b.append(((bx + COL_BODY_W, by - sw, BASE_T),
                      (bx + COL_BODY_W + sw, by + COL_BODY_W + sw,
                       BASE_T + COL_H * 0.5)))
            # pawl root block on +Y of sleeve
            ry = by + COL_BODY_W + sw
            ax = ox + (PITCH - PAWL_T) / 2
            b.append(((ax, ry, BASE_T),
                      (ax + PAWL_T, ry + PAWL_ROOT_L, BASE_T + PAWL_H)))
            # gate slot: two thin walls +X/-X of the gate lane, above the pawl
            gy = ry
            b.append(((ax - GATE_T - 2 * BLEED, gy, BASE_T + GATE_Z0),
                      (ax - GATE_T - BLEED, gy + PAWL_ROOT_L,
                       BASE_T + GATE_Z0 + GATE_H)))
            b.append(((ax + PAWL_T + BLEED, gy, BASE_T + GATE_Z0),
                      (ax + PAWL_T + GATE_T + 2 * BLEED, gy + PAWL_ROOT_L,
                       BASE_T + GATE_Z0 + GATE_H)))
    return b


def column_boxes():
    """One column: cap + necked body + rack ledges (material under each pocket)."""
    b = []
    # visible cap
    b.append(((-COL_CAP_W / 2, -COL_CAP_W / 2, 0.0),
              (COL_CAP_W / 2, COL_CAP_W / 2, 2.0)))
    # necked body
    b.append(((-COL_BODY_W / 2, -COL_BODY_W / 2, 0.0),
              (COL_BODY_W / 2, COL_BODY_W / 2, COL_H)))
    # rack ledges on +Y face: material below each 10 mm pocket
    for k in range(1, LEVELS):
        z = 2.0 + k * RACK_PITCH - POCKET_H
        b.append(((-POCKET_W / 2, COL_BODY_W / 2 - POCKET_D, z),
                  (POCKET_W / 2, COL_BODY_W / 2, z + POCKET_H)))
    return b


def pawl_boxes():
    """Flat cantilever rooted on the frame block, toe reaching -Y to the rack."""
    b = []
    # root pad (sits on the frame root block top)
    b.append(((0.0, 0.0, 0.0), (PAWL_T, PAWL_ROOT_L, PAWL_H)))
    # cantilever arm reaching -Y
    b.append(((0.0, -PAWL_FREE_L, PAWL_H - 1.2),
              (PAWL_T, 0.0, PAWL_H)))
    # wedge toe at the far -Y end, dropping below
    b.append(((0.0, -PAWL_FREE_L - 1.0, PAWL_H - 1.2),
              (PAWL_T, -PAWL_FREE_L, PAWL_H - 1.2 + 1.2)))
    return b


def gate_boxes():
    """Thin vertical bar that slides down to jam the pawl root."""
    return [((0.0, 0.0, 0.0), (GATE_T, PAWL_ROOT_L, GATE_H))]


def threshold_plate_boxes():
    """Horizontal bar with a boss over each armed (even) cell."""
    sx = NX * PITCH
    b = [((0.0, 0.0, 0.0), (sx, PLATE_T, PLATE_T))]
    for i in range(NX):
        if i % 2 == 0:
            ox = i * PITCH + (PITCH - COL_CAP_W) / 2
            b.append(((ox, 0.0, PLATE_T), (ox + COL_CAP_W, PLATE_T,
                                           PLATE_T + PLATE_BOSS_H)))
    return b


SCAD_HEADER = """// GENERATED by build_coupon.py from params.json. Do not edit by hand.
// S1 threshold-ratchet PRINTABLE coupon: __NX__ x __NY__ cells at true pitch.
// Self-supporting box geometry; every moving part is a separate printed solid.
// CAD solid -- not fabrication or physical validation.
$fn=48;
eps=0.01;
pitch=__PITCH__; nx=__NX__; ny=__NY__;
col_cap=__COL_CAP__; col_body=__COL_BODY__; col_h=__COL_H__;
rack_pitch=__RACK_PITCH__; pocket_w=__POCKET_W__; pocket_d=__POCKET_D__; pocket_h=__POCKET_H__;
pawl_t=__PAWL_T__; pawl_root=__PAWL_ROOT__; pawl_free=__PAWL_FREE__; pawl_h=__PAWL_H__;
gate_t=__GATE_T__; gate_h=__GATE_H__; gate_z0=__GATE_Z0__;
plate_t=__PLATE_T__; boss_h=__BOSS_H__;
bleed=__BLEED__; base_t=__BASE_T__; rail_w=__RAIL_W__; levels=__LEVELS__;

module column() {
    cube([col_cap, col_cap, 2.0], center=false);
    translate([(col_cap-col_body)/2,(col_cap-col_body)/2,0])
        cube([col_body,col_body,col_h], center=false);
    for (k=[1:levels-1])
        translate([(col_body-pocket_w)/2, col_body-pocket_d, 2.0+k*rack_pitch-pocket_h])
            cube([pocket_w,pocket_d,pocket_h], center=false);
}

module pawl() {
    cube([pawl_t, pawl_root, pawl_h]);
    translate([0,-pawl_free,pawl_h-1.2]) cube([pawl_t,pawl_free,1.2]);
    translate([0,-pawl_free-1.0,pawl_h-1.2]) cube([pawl_t,1.0,1.2]);
}

module gate() { cube([gate_t, pawl_root, gate_h]); }

module threshold_plate() {
    cube([nx*pitch, plate_t, plate_t]);
    for (i=[0:nx-1]) if (i%2==0)
        translate([i*pitch+(pitch-col_cap)/2,0,plate_t]) cube([col_cap,plate_t,boss_h]);
}

module frame() {
    cube([nx*pitch, ny*pitch, base_t]);
    rail_z = base_t + col_h + 0.2;
    translate([0,0,base_t]) cube([rail_w, ny*pitch, rail_z-base_t+plate_t]);
    translate([nx*pitch-rail_w,0,base_t]) cube([rail_w, ny*pitch, rail_z-base_t+plate_t]);
    sw=1.0;
    for (i=[0:nx-1], j=[0:ny-1]) {
        ox=i*pitch; oy=j*pitch;
        bx=ox+(pitch-col_body)/2; by=oy+(pitch-col_body)/2;
        translate([bx-sw,by-sw,base_t]) cube([sw, col_body+2*sw, col_h*0.5]);
        translate([bx+col_body,by-sw,base_t]) cube([sw, col_body+2*sw, col_h*0.5]);
        ry=by+col_body+sw; ax=ox+(pitch-pawl_t)/2;
        translate([ax,ry,base_t]) cube([pawl_t,pawl_root,pawl_h]);
        translate([ax-gate_t-2*bleed,ry,base_t+gate_z0]) cube([gate_t, pawl_root, gate_h]);
        translate([ax+pawl_t+bleed,ry,base_t+gate_z0]) cube([gate_t, pawl_root, gate_h]);
    }
}

frame();
translate([(pitch-col_cap)/2,(pitch-col_cap)/2,base_t]) column();
translate([(pitch-pawl_t)/2,(pitch-col_body)/2+col_body+1.0,base_t]) pawl();
translate([(pitch-pawl_t)/2,(pitch-col_body)/2+col_body+1.0,base_t+gate_z0]) gate();
translate([0,0,base_t+col_h+0.2]) threshold_plate();
"""


def scad_source() -> str:
    out = SCAD_HEADER
    vals = {
        "PITCH": PITCH, "NX": NX, "NY": NY, "LEVELS": LEVELS,
        "COL_CAP": COL_CAP_W, "COL_BODY": COL_BODY_W, "COL_H": COL_H,
        "RACK_PITCH": RACK_PITCH, "POCKET_W": POCKET_W, "POCKET_D": POCKET_D,
        "POCKET_H": POCKET_H, "PAWL_T": PAWL_T, "PAWL_ROOT": PAWL_ROOT_L,
        "PAWL_FREE": PAWL_FREE_L, "PAWL_H": PAWL_H, "GATE_T": GATE_T,
        "GATE_H": GATE_H, "GATE_Z0": GATE_Z0, "PLATE_T": PLATE_T,
        "BOSS_H": PLATE_BOSS_H, "BLEED": BLEED, "BASE_T": BASE_T,
        "RAIL_W": RAIL_W,
    }
    for k, v in vals.items():
        out = out.replace(f"__{k}__", str(v))
    return out


def main() -> None:
    here = Path(__file__).resolve().parent
    (here / "params.json").write_text(json.dumps(PARAMS, indent=2) + "\n")
    man = make_manifest()
    (here / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    # Assembly places the loose moving parts at their printed-relative
    # positions so a single viewable STL shows the mechanism.
    def assembly():
        sx = NX * PITCH
        b = list(frame_boxes())
        # one column in cell (0,0), one pawl+gate engaged, threshold plate up
        col = column_boxes()
        cx = (PITCH - COL_CAP_W) / 2
        cy = (PITCH - COL_CAP_W) / 2
        zcol = BASE_T
        for lo, hi in col:
            b.append(((lo[0]+cx, lo[1]+cy, lo[2]+zcol),
                      (hi[0]+cx, hi[1]+cy, hi[2]+zcol)))
        pr = pawl_boxes()
        ox = (PITCH - PAWL_T) / 2
        oy = (PITCH - COL_BODY_W) / 2 + COL_BODY_W + 1.0
        for lo, hi in pr:
            b.append(((lo[0]+ox, lo[1]+oy, lo[2]+BASE_T),
                      (hi[0]+ox, hi[1]+oy, hi[2]+BASE_T)))
        gb = gate_boxes()
        for lo, hi in gb:
            b.append(((lo[0]+ox, lo[1]+oy, lo[2]+BASE_T+GATE_Z0),
                      (hi[0]+ox, hi[1]+oy, hi[2]+BASE_T+GATE_Z0)))
        pl = threshold_plate_boxes()
        pz = BASE_T + COL_H + 0.2
        for lo, hi in pl:
            b.append(((lo[0], lo[1], lo[2]+pz), (hi[0], hi[1], hi[2]+pz)))
        return b

    parts = {
        "coupon_frame.stl": frame_boxes(),
        "coupon_column.stl": column_boxes(),
        "coupon_pawl.stl": pawl_boxes(),
        "coupon_gate.stl": gate_boxes(),
        "coupon_threshold_plate.stl": threshold_plate_boxes(),
        "coupon_assembly.stl": assembly(),
    }
    for name, boxes in parts.items():
        n = write_stl(here / name, boxes)
        print(f"wrote {name}: {len(boxes)} boxes, {n} triangles")
    (here / "coupon.scad").write_text(scad_source())
    print("wrote coupon.scad")
    print(f"pitch {PITCH} mm, {NX}x{NY} cells, {LEVELS} levels, {TRAVEL} mm travel")
    print("printable:", man["checks"]["all_printable"])


if __name__ == "__main__":
    main()
