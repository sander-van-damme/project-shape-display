# Bounded guide revision after an admissible-pose collision

The frozen `cad/resident_cell.scad` source with SHA256 `780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157` **fails its angular-clearance guarantee** despite270 centred nominal geometry checks. The independent reviewer supplied this exact admissible A-dog transform:

- Rotate−4° about Z at(3,−2.2,−30.4) mm.
- Then translate X−0.0817508698 and Y+0.0487983689 mm.
- The transformed dog does not intersect its channel or key guide, but intersects the seated pin by0.1013509 mm³. Its toe reaches Y−0.47349, beyond the groove backY−0.55.

This is a real rigid-body counterexample, not a presumed manufacturing defect. The corresponding embodiment must not be offered as fabrication-ready. The independent reproducer is `analysis/check_resident_counterexample.py`, with `counterexample.json` and dimensioned images in the generated `work/des008-resident-counterexample/` directory. It also preserves a14.688-mm³ counterexample for directly abutting unmirrored bank links. Canonical evidence is retained in `analysis/resident-counterexample.json`.

## One bounded escape

A2-mm Y bearing is not a free fix. To put the fixed guide ahead of the ON L-beam while retaining the full2.45-mm stored-bit/common-A travel requires roughly5.35 mm of key length. Opposite-bit neighboring keys then require5.35+1.60=6.95 mm at6.35-mm pitch, even before an inter-key gap. Staggering guides or changing the load path would be a new design.

`cad/resident_cell_guide_escape.scad` instead tests a1.0-mm guide with4.5-mm keys, preserving the existing0.05-mm per-side X clearance, and shortens the A tooth's nominal penetration from0.50 to0.35 mm. Its mixed-bit key envelope is4.5+1.6=6.1 mm, leaving only0.25 mm nominal inter-key separation. Reducing tooth depth increases nominal groove-root clearance from0.15 to0.30 mm, but reduces positive capture overlap. Both changes must be tested together with guide play and deflection. No tighter fitting has been assumed.

The exact previous−4° pose no longer intersects the pin in this variant, but it is still admitted by its guides. This single result is **not** a new tolerance pass. Independent adversarial review must examine other yaw/translation combinations, neighboring keys/pins, OFF ramp clearance and minimum retained overlap. A longer body can trade a root jam for a neighbor collision; those are not equivalent improvements.

Reproduce centred checks with:

```sh
python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident.py --source 08-integrated-designs/DES-008-positive-latch-shared-lift/cad/resident_cell_guide_escape.scad --output work/resident-escape
```

The baseline270-check record remains separate and valid only for centred nominal poses. A full-array frame, powered writer, assembly method and manufacturing yield are unresolved in either version. This revision is a bounded mechanism comparison, not another owner print request.

## Independent disposition of the bounded escape

Final variant SHA256: `24eb609bdb034dccbd72d93b6ee8af8cca14b333965516dce820bfd237af07e9`. The independent reviewer screened1,954 candidate planar poses;1,924 were admissible against the actual channel and key-guide meshes. The tested admissible poses produced zero own-rack collisions and the extremal neighbor-key shortlist produced zero opposite-bit adjacent-key collisions. Reproducer: `analysis/check_resident_escape.py`; detailed result: `analysis/resident-escape-review.json`. The variant also passes the270 centred nominal checks in `analysis/resident-escape-checks.json`.

This supports the **bounded escape as the preferred next resident-cell study**, superseding the rejected0.5-mm-bearing embodiment for further mechanism testing. It is not a six-degree-of-freedom clearance proof or a whole-machine construction release. The independent reviewer found that **±0.10 mm vertical key-guide play consumes the entire nominal0.10-mm unloading margin**. Therefore positive unloaded support transfer is still UNRESOLVED, even when planar root interference is removed. A designed preload/compliance or force-limited seating mechanism and physical qualification remain necessary. The directly abutting bank-frame collision also remains.

The variant does not demonstrate lower cost, manufacturable yield or an80-ms row write. It trades a larger key and smaller capture overlap against a repaired planar collision. Preserve the original failed case, the bounded result and these remaining limits together; do not summarize them as an integrated design pass.
