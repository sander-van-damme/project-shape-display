---
status: active
builds-on: [DES-005]
---

# E-018: four-plane mask-generator coupon package

## Purpose and evidence boundary

This is a reproducible 5 x 5 coupon for future physical falsification of the
conditional reusable-mask boundary in E-017 and ADR-006. It is a CAD
definition, interface contract, calculation, and test handoff. No printed,
assembled, cycle, wear, reader, or writer measurements exist here. Analytical
checks do not validate hardware.

The executable source is `cad/four_plane_mask_coupon.scad`. It reuses the
5.08 mm final pitch and 40 mm frame envelope from DES-005, but deliberately
does not reuse its rotor mechanism: the rotor's detents and coded vanes would
confound four-plane write yield and registration. This article isolates four
independent binary plane carriers.

## Frozen coupon definition

| Item | Nominal | Basis / purpose |
|---|---:|---|
| active cells | 5 x 5 | E-017 / ADR-006 boundary |
| final pitch | 5.08 mm | inherited project reference |
| active centre span | 25.40 mm | five centres at final pitch |
| frame outside | 40 x 40 x 3.00 mm | DES-005 envelope |
| plane carrier | 34 x 34 x 0.80 mm | four independent planes |
| plane separation | 1.20 mm | clearance between carriers |
| cell aperture | 3.00 x 3.00 mm | 2.08 mm pitch web; provisional |
| fiducials | two Ø2.00 mm holes | diagonal, outside active field |
| fiducial centres | (-15,-15), (15,15) mm | reseat registration |
| positive datum | 2.00 x 6.00 mm north rail witness | clamp registration |
| clamp land | 32 x 2.50 mm south land | positive seating |
| reader target | centre 3 x 3 mm window | frame-fixed, 2.00 mm standoff |
| writer ports | four, one per plane | 4 x 1 x 0.8 mm tongues |
| writer tab x | -10.16 mm | common tab datum on each carrier |
| port stack pitch | 2.00 mm | plane identity / anti-crossing |
| dummy neighbours | N/E/S/W rigid carriers | loaded isolation boundary |

Each plane is a separate carrier with 25 nominal windows and a labelled edge
tab. The coupon does not prescribe the rewritable medium or actuator; the
future fabricator must preserve the carrier envelope, tab, fiducial, datum,
and aperture coordinates. The frame-fixed reader reads the selected plane
combination after settling. Fiducials are outside the map and are read before
and after reseat.

## Writer-channel interface

The fixture supplies four independent channels P0..P3, indexed bottom to top.
Each channel has a 4.00 x 1.00 x 0.80 mm tongue, 1.00 mm nominal insertion,
and 2.00 mm centre pitch matching the plane stack. In the engaged CAD state,
each tongue is registered to the full 1.00 mm tab thickness; in the parked
state its nearest face is 0.20 mm outside the frame edge. All four channels are enabled in one addressed
engagement; a channel can park without touching the other three. The command
record is:

`cycle_id, plane, desired_25bit_row_major, pulse_start_ns, pulse_width_ns,
actual_ack, fault_code`.

This tests parallel engagement and plane cross-talk, but makes no writer-rate,
force, or actuator-selection claim. Actual tongue dimensions and insertion
depth are to be measured before physical testing.

## Assembly and loading sequence

1. Seat the frame against the north positive datum and clamp the south land;
   verify both fiducials are unobstructed.
2. Insert P0..P3 into labelled guides with each tab aligned to its matching
   writer port. The reader head is not a datum.
3. Install four rigid dummy neighbours N/E/S/W at the same 5.08 mm pitch;
   they have no writer port and must remain loaded during isolation cycles.
4. Attach the frame-fixed reader at the defined centre target and record
   unloaded fiducial and centre-window coordinates.
5. For each cycle, command all four planes, wait the predeclared settle
   interval, read both fiducials and all changed cells, then release/reseat
   only when the protocol calls for it.

## Adversarial maps and 1,000-cycle handoff

Use named 4 x 25-bit row-major maps with P0 as least-significant plane:

| Case | Purpose |
|---|---|
| `all_zero` | maximum closed-state dwell |
| `all_four` | maximum open-state dwell |
| `checkerboard` | adjacent edge and plane transitions |
| `single_corner` | boundary registration and one-cell write |
| `single_centre` | reader target discrimination |
| `plane_complements` | opposite states in every plane |
| `cross_neighbour` | active edge beside loaded dummies |
| `walking_one` | one-cell changes through all positions |

Every named case must occur at least 20 times in the future 1,000-cycle run;
include at least 100 reseat events and 100 loaded-neighbour cycles. A cycle is
invalid if a writer acknowledgement, fiducial read, map readback, or neighbour
position is missing. The minimum per-plane and summary fields are enumerated
in `analysis/coupon_protocol.py`: cycle/map identity, plane, commanded and
read-back 25-bit maps, channel timing/ack, fiducial XY errors, reader
classification/confidence, reseat event, neighbour displacement, wear/damage
code, retry count, and operator/environment identifiers. Blank values are
invalid evidence.

## Gates and falsifiers

These are provisional engineering gates, not sourced standards:

* zero unexplained channel or cell misses in the accepted 1,000-cycle sample;
* fiducial and active-cell XY error ≤0.20 mm after every reseat;
* zero wrong reader classifications, with confidence threshold chosen before
  testing;
* no crack, tear, permanent set, blocked aperture, or increasing miss trend;
* each loaded-neighbour displacement ≤0.20 mm per local write and no state
  change; and
* no tongue collision, plane swap, or engagement outside the labelled port.

Any failed gate falsifies this coupon configuration for that boundary claim.
A pass is evidence only for this coupon and sample, not product adoption,
production yield, or full-scale reliability.

## Reproducible analytical checks

```sh
python3 06-experiments/E-018-four-plane-mask-generator-coupon-package/analysis/coupon_protocol.py --check
openscad --export-format binstl -o /dev/null -D 'part="assembly"' 06-experiments/E-018-four-plane-mask-generator-coupon-package/cad/four_plane_mask_coupon.scad
./repo check
```

The Python check verifies field span, aperture web, fiducial placement, port
spacing, writer overlap and parked clearance, reader clearance and XY window
alignment, adversarial-case coverage, and the 1,000-cycle allocation. OpenSCAD
only parses/exports parametric CAD; neither command simulates actuation,
registration, discrimination, wear, or neighbour loading.

## Disposition and unresolved assumptions

Analytical status: **interface geometry repaired; definition checks pass; no
physical result**. The writer tongue now shares a 1.00 mm Y overlap with its
matching plane tab at every plane, while retaining the 4 x 1 x 0.8 mm tongue
envelope. The reader body lower face is 2.00 mm above the upper carrier, and
its 3 x 3 mm window is placed at that lower face over the selected centre
aperture. The writer also has an explicit 0.20 mm parked clearance outside
the frame edge. `analysis/coupon_protocol.py --check` now asserts positive
writer overlap, parked non-interference, reader clearance, and reader-window
alignment; these are CAD/coordinate checks, not physical engagement or read
validation. Unresolved assumptions remain
the rewritable medium construction, shutter force/stroke, reader technology
and confidence metric, clamp preload, process spread, and whether 0.20 mm is
achievable after reseat. These require physical evidence.

Rollback is deleting this E-018 workspace and reverting its commit; DES-004,
DES-005, E-017, and ADR-006 remain unchanged. Do not expand this experiment
into procurement, physical testing, or product adoption.
