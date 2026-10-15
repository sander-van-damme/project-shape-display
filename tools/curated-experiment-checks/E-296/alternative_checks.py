#!/usr/bin/env python3
"""Finite BREP packaging checks for B2 face dogs and C serial couplings.

Run with CadQuery/OCP: python alternative_checks.py. These one-cell precision
layouts are NOT a qualified full fixture, contact solve or manufacturing plan.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import cadquery as cq
import generate as g

HERE = Path(__file__).resolve().parent
EPS = 1e-6


def sector(r0, r1, width, center, z, height):
    def point(r, a):
        return r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
    a, b = center - width / 2, center + width / 2
    return (cq.Workplane("XY").moveTo(*point(r0, a))
            .lineTo(*point(r1, a)).threePointArc(point(r1, center), point(r1, b))
            .lineTo(*point(r0, b)).threePointArc(point(r0, center), point(r0, a))
            .close().extrude(height).val().translate((0, 0, z)))


def ring(inner, outer, z, thickness):
    return g.cyl(outer, z, thickness).cut(g.cyl(inner, z-.01, thickness+.02)).clean()


def b2_sleeve():
    # No B1 upper hex lead-in: it would remove the front-dog roots.
    s = (g.cyl(3., -.6, 4.7).fuse(g.cyl(4.2, 3.7, .4))
         .fuse(g.cyl(3.4, -.6, .4)).cut(g.hexprism(1.95, -.7, 4.8)))
    for angle in (0, 120, 240):
        s = s.fuse(sector(1.2, 1.7, 35, angle, 4.1, .8))
    return s.clean()


def b2_output():
    s = g.cyl(3.4, 5.65, 1.25)
    for angle in (0, 120, 240):
        s = s.cut(sector(1.1, 1.8, 50, angle, 5.64, .86))
    return s.clean()


def mirror(s):
    return s.rotate((0, 0, 8.4), (1, 0, 8.4), 180)


def intermediate():
    return (g.hexprism(1.8, 4.7, 3.).fuse(g.cyl(2., 7.7, 1.4))
            .fuse(g.cyl(3.6, 7.7, .2)).fuse(g.cyl(3.6, 8.9, .2))
            .fuse(g.hexprism(1.8, 9.1, 3.)).clean())


def collisions(parts):
    bad = []
    count = 0
    for (na, a), (nb, b) in itertools.combinations(parts.items(), 2):
        aa, bb = a.BoundingBox(), b.BoundingBox()
        if any(min(getattr(aa, k+'max'), getattr(bb, k+'max')) -
               max(getattr(aa, k+'min'), getattr(bb, k+'min')) <= 1e-8 for k in 'xyz'):
            continue
        count += 1
        volume = a.intersect(b).Volume()
        if volume > EPS:
            bad.append(dict(a=na, b=nb, volume_mm3=volume))
    return count, bad


def export(parts, name):
    assy = cq.Assembly(name=name)
    for key, shape in parts.items():
        assy.add(shape, name=key)
    cq.exporters.export(assy.toCompound(), str(HERE / 'cad' / (name+'.step')))


def main():
    out = dict(evidence='Nominal finite BREP packaging and interference checks only; no physical qualification',
               cadquery_version=cq.__version__, length_unit='mm', volume_unit='mm^3',
               limitations=[
                   'Alternative layouts are one-cell studies, not complete guided 2x2 fixtures.',
                   'No friction, compliance, forces, fatigue, loaded withdrawal or assembly-yield qualification.',
                   'C selector rings indicate reserved cassette geometry; external connections, guides and assembly remain unqualified.',
                   'B2 input sliding hex remains a precision interface; face dogs do not remove this manufacturing burden.',
                   'Aligned positive torque graphs and interference-free solids do not establish physical phase seating.',
                   'Face-dog slots open at the outer circumference; rotational retention requires the independent shaft supports.'])
    bs, bo = b2_sleeve(), b2_output()
    assert bs.isValid() and bo.isValid()
    b2 = dict(dimensions=dict(dog_radii=[1.2, 1.7], dog_width_degrees=35,
                             dog_z_off=[4.1, 4.9], slot_radii=[1.1, 1.8],
                             slot_width_degrees=50, output_bottom=5.65,
                             slot_roof=6.5, output_top=6.9, roof_id=3.6, roof_od=4.7),
              states=[], phase_probes=[])
    for r, c in itertools.product([0., 1.4], repeat=2):
        q = min(c, r+.2)
        parts = dict(input=g.input_shaft(), sleeve=bs.translate((0, 0, q)),
                     output=bo, row=ring(3.2, 4.7, r, .3),
                     roof=ring(3.6, 4.7, 4.1+c, .4))
        assert all(s.isValid() for s in parts.values())
        assert all(max(s.BoundingBox().xlen, s.BoundingBox().ylen) <= 4.7+1e-7
                   for s in parts.values())
        count, bad = collisions(parts)
        assert not bad, bad
        b2['states'].append(dict(row=r, column=c, q=q, brep_pair_tests=count,
                                 collisions=bad, tip_gap=max(0., 5.65-(4.9+q)),
                                 straight_flank_overlap=max(0., min(4.9+q, 6.5)-5.65),
                                 input_key_overlap=3.3-(-.6+q)))
        if r == c == 1.4:
            export(parts, 'alternative_B2_one_cell_ON')
    for phi in [-7.6, -7.4, 0, 7.4, 7.6]:
        volume = bs.translate((0, 0, 1.4)).intersect(
            bo.rotate((0, 0, 0), (0, 0, 1), phi)).Volume()
        assert (volume < EPS) if abs(phi) < 7.5 else (volume > EPS)
        b2['phase_probes'].append(dict(degrees=phi, interference_volume=volume,
                                       fits=volume < EPS))
    b2['clearances'] = dict(dog_inner_radial=.1, dog_outer_slot_cut_radial=.1,
                           roof_to_output_radial=.1, roof_to_dogs_radial=.1,
                           roof_stop_radial_land=.3, on_tip_to_slot_roof=.2,
                           on_straight_flank=.65, adjacent_roof_gap=g.P-4.7)
    out['B2'] = b2

    hub = intermediate()
    plate = g.box(-2.35, 2.35, -2.35, 2.35, 7.92, 8.88).cut(g.cyl(2.02, 7.91, .98))
    assert hub.isValid() and plate.isValid()
    cdata = dict(mirror_plane_z=8.4, states=[], dimensions=dict(
        lower_intermediate_hex_z=[4.7, 7.7], upper_intermediate_hex_z=[9.1, 12.1],
        upper_output_hex_z=[13.5, 18.7], cassette_return_lash=0.,
        maximum_one_cell_xy_envelope=[4.7, 4.7]), intermediate_journal=dict(
        diameter=2., bore=2.02, plate_z=[7.92, 8.88],
        collars_z=[[7.7, 7.9], [8.9, 9.1]], radial_gap=.01, axial_gap_each=.02),
        selector_cassette='Zero return lash: lower ring bottom=-.2+command; roof underside=4.1+command. Upper cassette is mirrored. Spring geometry/force not solved.')
    for r, c in itertools.product([0., 1.4], repeat=2):
        parts = dict(input=g.input_shaft(), output=mirror(g.input_shaft()),
                     lower_sleeve=g.sleeve().translate((0, 0, r)),
                     upper_sleeve=mirror(g.sleeve().translate((0, 0, c))),
                     intermediate=hub, central_plate=plate,
                     row_return=ring(3.2, 4.7, -.2+r, .3),
                     row_roof=ring(2.4, 4.7, 4.1+r, .4),
                     column_return=mirror(ring(3.2, 4.7, -.2+c, .3)),
                     column_roof=mirror(ring(2.4, 4.7, 4.1+c, .4)))
        assert all(s.isValid() for s in parts.values())
        assert all(max(s.BoundingBox().xlen, s.BoundingBox().ylen) <= 4.7+1e-7
                   for s in parts.values())
        count, bad = collisions(parts)
        assert not bad, bad
        cdata['states'].append(dict(row=r, column=c,
             lower_sleeve_z=[-.6+r, 4.1+r], upper_sleeve_z=[12.7-c, 17.4-c],
             lower_gap=max(0., .6-r), upper_gap=max(0., .6-c),
             lower_overlap=max(0., r-.6), upper_overlap=max(0., c-.6),
             lower_straight_flank=max(0., r-.975), upper_straight_flank=max(0., c-.975),
             input_key_overlap=3.9-r, output_key_overlap=3.9-c,
             complete_torque_path=bool(r and c), brep_pair_tests=count, collisions=bad))
        if r == c == 1.4:
            export(parts, 'alternative_C_one_cell_ON')
    # Axial negative controls distinguish a real captured journal from a floating rotor.
    probe = []
    for shift in [-.03, -.02, 0., .02, .03]:
        volume = hub.translate((0, 0, shift)).intersect(plate).Volume()
        assert (volume < EPS) if abs(shift) <= .02 else (volume > EPS)
        probe.append(dict(shift=shift, interference_volume=volume))
    cdata['journal_axial_probes'] = probe
    cdata['neighbor_envelope'] = dict(max_selector_diameter=4.7, pitch=g.P,
                                    nominal_gap=g.P-4.7,
                                    check='Independent one-cell solids translated to neighboring cell centers')
    # Exercise actual adjacent roof/ring shapes at opposite command extrema.
    ring0 = ring(3.2, 4.7, 0., .3)
    neighbor = ring0.translate((g.P, 0, 0))
    v = ring0.intersect(neighbor).Volume()
    assert v < EPS
    cdata['neighbor_envelope']['brep_adjacent_ring_interference'] = v
    out['C'] = cdata
    (HERE/'alternative-geometry.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(dict(B2_states=len(b2['states']), C_states=len(cdata['states']),
                          phase_probes=len(b2['phase_probes']), status='PASS'), indent=2))


if __name__ == '__main__':
    main()
