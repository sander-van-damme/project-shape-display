#!/usr/bin/env python3
"""Resident screw support screen. All scenario inputs are bounds, not measurements.

Units: mm, N, MPa (N/mm^2). Guide tilt is a small-angle rigid centerline
relaxation, not contact simulation. Euler loads are idealized instability loads,
not permissible loads. Run --check for independent limiting-case checks.
Euler form/end-fixity reference (not polymer properties): Nook miniature screw
catalog, PDF p8, https://www.nookindustries.com/media/2427/pmbs-miniatures-catalog.pdf
checked 2026-10-13. Historical geometry provenance is in canonical E-261.
"""
import argparse
import itertools
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Envelope:
    stroke: float
    span: float  # guide center separation
    nut: float = 10.0
    thread_bottom_margin: float = 2.0
    thread_top_margin: float = 2.0
    guide_thickness: float = 2.0
    pin_bottom_margin: float = 2.0
    pin_top_margin: float = 2.0

    def __post_init__(self):
        if any(v <= 0 for v in asdict(self).values()):
            raise ValueError("Lengths must be positive")
        if self.span < self.guide_thickness:
            raise ValueError("Guide slabs must not overlap")

    @property
    def thread_length(self):
        return (self.stroke + self.nut + self.thread_bottom_margin
                + self.thread_top_margin)

    @property
    def pin_length(self):
        return (self.stroke + self.span + self.guide_thickness
                + self.pin_bottom_margin + self.pin_top_margin)

    @property
    def guide_faces(self):
        lower = self.thread_bottom_margin + self.stroke + self.pin_bottom_margin
        return (lower, lower + self.guide_thickness,
                lower + self.span, lower + self.span + self.guide_thickness)

    def top(self, displacement):
        return self.thread_bottom_margin + displacement + self.pin_length

    def compressed_length(self, load_fraction=0.5):
        """Nut load station; actual thread distribution and seat offset unknown."""
        if not 0 <= load_fraction <= 1:
            raise ValueError("Load station must lie within nut")
        return self.thread_bottom_margin + self.stroke + load_fraction * self.nut


def lateral_envelope(e, clearance, pitch, width, relative_axis_error=0):
    """Opposing independent play at all four slab faces, rigid centerlines.

    Common translation/tilt cancels between equal-height adjacent columns;
    relative_axis_error is their *differential* positioning error at the top.
    Width is treated as constant horizontal section (small-angle relaxation).
    """
    if min(clearance, relative_axis_error) < 0 or min(width, pitch) <= 0:
        raise ValueError("Invalid lateral geometry")
    lo, _, _, hi = e.guide_faces
    overhang = e.top(e.stroke) - hi
    slope = clearance / (hi - lo)
    tip_play = clearance / 2 + slope * overhang
    return {"slope": slope, "tip_play": tip_play,
            "neighbor_gap": pitch - width - 2 * tip_play - relative_axis_error,
            "section_width_correction": width * (math.sqrt(1 + slope**2) - 1)}


def guide_reactions(e, side_load, displacement=None):
    """Static force/moment balance at slab centers; no elastic contact claim."""
    if displacement is None:
        displacement = e.stroke
    if not 0 <= displacement <= e.stroke:
        raise ValueError("Displacement outside stroke")
    lo, _, hi, _ = e.guide_faces
    z1 = lo + e.guide_thickness / 2
    z2 = hi + e.guide_thickness / 2
    top = e.top(displacement)
    upper = -side_load * (top - z1) / (z2 - z1)
    lower = -side_load - upper
    return lower, upper


def euler(modulus, core_diameter, length, effective_length_factor):
    if min(modulus, core_diameter, length, effective_length_factor) <= 0:
        raise ValueError("Invalid elastic-column input")
    moment = math.pi * core_diameter**4 / 64
    return math.pi**2 * modulus * moment / (effective_length_factor * length)**2


def required_core(load, modulus, length, effective_length_factor):
    """Equality at Euler instability: includes NO safety allowance."""
    if load <= 0:
        raise ValueError("Positive load required")
    return (64 * load * (effective_length_factor * length)**2
            / (math.pi**3 * modulus)) ** 0.25


def check():
    # Independent all-position interval containment, not only chosen endpoints.
    n = 0
    for stroke, span in itertools.product((20, 40, 50), (10, 20, 40, 60)):
        e = Envelope(stroke, span)
        for i in range(101):
            q = e.thread_bottom_margin + stroke * i / 100
            assert q >= e.thread_bottom_margin
            assert q + e.nut <= e.thread_length - e.thread_top_margin + 1e-12
            for face in e.guide_faces:
                assert q + e.pin_bottom_margin - 1e-12 <= face
                assert face <= q + e.pin_length - e.pin_top_margin + 1e-12
            n += 1
        # Reducing the derived stock by epsilon loses the last upper guide face
        # at minimum extension, and full nut overlap at maximum extension.
        assert e.guide_faces[-1] > e.thread_bottom_margin + e.pin_length - .001 - e.pin_top_margin
        assert e.thread_bottom_margin + stroke + e.nut > e.thread_length - .001 - e.thread_top_margin
        lo, _, _, hi = e.guide_faces
        c = .24
        # Independent four-face linear program vertex enumeration: every
        # optimum line meets two aperture boundary constraints.
        faces = e.guide_faces
        feasible = []
        for z1, z2 in itertools.combinations(faces, 2):
            for x1, x2 in itertools.product((-c / 2, c / 2), repeat=2):
                slope = (x2 - x1) / (z2 - z1)
                intercept = x1 - slope * z1
                if all(abs(intercept + slope * z) <= c / 2 + 1e-10 for z in faces):
                    feasible.append(intercept + slope * e.top(stroke))
        out = lateral_envelope(e, c, 5.08, 4.4)
        assert math.isclose(max(feasible), out['tip_play'], abs_tol=1e-10)
        assert lateral_envelope(e, 0, 5.08, 4.4)['neighbor_gap'] == 5.08 - 4.4
        assert math.isclose(lateral_envelope(e, c, 5.08, 4.4, .2)['neighbor_gap'],
                            out['neighbor_gap'] - .2)
        r1, r2 = guide_reactions(e, .1)
        center1, center2 = faces[0] + 1, faces[2] + 1
        assert math.isclose(r1 + r2 + .1, 0, abs_tol=1e-12)
        assert math.isclose(r2 * (center2-center1) + .1 * (e.top(stroke)-center1),
                            0, abs_tol=1e-12)
    f = euler(1000, 1.4, 57, 1)
    assert math.isclose(euler(1000, 2.8, 57, 1), 16*f)
    assert math.isclose(euler(1000, 1.4, 114, 1), f/4)
    assert math.isclose(euler(2000, 1.4, 57, 1), 2*f)
    assert math.isclose(euler(1000, 1.4, 57, 2), f/4)
    # Separate SI-unit reconstruction.
    f_si = math.pi**2 * 1e9 * (math.pi * .0014**4/64) / .057**2
    assert math.isclose(f, f_si)
    for force, mod, length, k in itertools.product((.049, .196, .981, 9.81), (1000, 3000), (47, 57), (1, 2)):
        assert math.isclose(euler(mod, required_core(force, mod, length, k), length, k), force)
    # Deeper stroke adds twice its increment to maximum top height, not once.
    a, b = Envelope(40, 40), Envelope(50, 40)
    assert b.pin_length-a.pin_length == b.thread_length-a.thread_length == 10
    assert b.top(50)-a.top(40) == 20
    # Legacy 50.8-mm pin cannot contain a wide fixed guide span throughout40 travel.
    assert math.isclose(50.8-40-2-2-2, 4.8)
    print(f"PASS: {n} axial states, 12 four-face LP extrema, statics, Euler SI/scaling/inverse and stock limits")


def report():
    out = {"evidence": "conditional calculations; no physical qualification", "geometry": []}
    for stroke, span in itertools.product((40, 50), (20, 40, 60)):
        e = Envelope(stroke, span)
        row = {"stroke": stroke, "guide_center_span": span,
               "pin_length": e.pin_length, "thread_length": e.thread_length,
               "top_min": e.top(0), "top_max": e.top(stroke),
               "guide_faces": e.guide_faces,
               "lateral": {f"p{p}_w{w}": lateral_envelope(e, .24, p, w)
                           for p, w in ((5.08, 4.4), (6.35, 4.4), (6.35, 5.6))},
               "guide_reactions_H0.1": guide_reactions(e, .1),
               "euler_E1000_core1.4": {
                   str(k): [euler(1000, 1.4, e.compressed_length(v), k) for v in (0, .5, 1)]
                   for k in (1, 2)}}
        out['geometry'].append(row)
    out['euler_sensitivity_50stroke_midnut'] = [
        {"E_MPa": mod, "core_mm": d, "K": k, "ideal_critical_N": euler(mod, d, 57, k)}
        for mod, d, k in itertools.product((1000, 3000), (1.4, 2, 2.5), (1, 2))]
    out['added_stock_10mm'] = [
        {"sites": n, "tube_liters": n * (4.4**2 - 3.52**2) * 10 / 1e6,
         "screw_core_to_outer_liters": [n * math.pi * d*d/4 * 10/1e6 for d in (1.4, 3.2)]}
        for n in (4096, 6400)]
    out['twenty_gram_critical_diameter_no_margin'] = {
        str(k): required_core(.020*9.80665, 1000, 57, k) for k in (1, 2)}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    check() if args.check else report()
