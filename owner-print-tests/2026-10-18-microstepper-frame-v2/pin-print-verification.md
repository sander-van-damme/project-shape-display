# E-302 revision 3 — independent tall-pin slice review

This is a **computational slice check**, not a physical print qualification. The new
50 mm pin retains the E-301 lower threaded geometry and integral print foot; only
the straight square tube is extended. The unchanged 18 mm pin is its reference.

`review_pins.py` inspected the initial saved slice and the Bambu Studio reopened,
resliced project. Machine-readable results are in `pin-review.json` and
`pin-review-reopened.json`, with the exact archive hashes and every layer recorded.
The two runs give the same summary results:

| Check | Pin 18 mm | Pin 50 mm |
|---|---:|---:|
| Extrusion layers | 150 | 417 |
| Highest slicer Z | 18.00 mm | 50.04 mm |
| Upper layers above Z 6.12, closed contour around bore | 99 / 99 | 366 / 366 |
| Layers with central radius 0.60 mm clear | 150 / 150 | 417 / 417 |
| Deposited components without previous-layer contact | 0 | 0 |
| Support paths anywhere inside local part bounds | 0 | 0 |
| First-layer foot extent | 12 × 12 mm | 12 × 12 mm |
| First-layer nominal deposited area | 137.14 mm² | 137.14 mm² |
| Maximum upper-tube extrusion speed | 15 mm/s | 15 mm/s |
| Maximum upper-tube extrusion acceleration | 500 mm/s² | 500 mm/s² |

The 50.04 mm slicer Z is rounding to the 0.12 mm layer grid; the CAD/STL height is
50.00 mm. Checking a clear central disk does not certify the complete female
thread surface or its physical fit. The lower 51 layers of both pins were compared
after XY alignment: largest footprint symmetric difference 0.0553 mm² and largest
Hausdorff distance 0.0864 mm. They are close but not bit-identical slice paths;
these numbers are not measured printer repeatability or a physical tolerance.

The pin stands on its existing 12 × 12 × 0.24 mm integral foot. Every later
material component overlaps the previous layer. The tube is 4.4 mm wide, with
nominal 0.44 mm walls above the threaded region. Its height/body-width ratio is
11.36. That means the footprint check establishes a continuous printing route,
but cannot establish adequate lateral stiffness, bed adhesion, or absence of
nozzle strikes. The foot supports adhesion only; there is no side support along
the 50 mm height. No support material is deposited in the female thread, so there
is no internal support removal operation or associated thread-scarring mechanism.

For the physical test, check that the full thin foot adheres on the first layers.
Stop the print if the foot lifts or the tube visibly wobbles under nozzle travel.
After cooling, release the complete part from the flex plate. **Leave the integral
thin foot attached**: as in E-301 it remains below the frame guide throughout
the 3 mm trial stroke. No cutting or sanding of this foot or female thread is
required. Inspect the lower thread and tube for cracks or tearing.
The stability and removal outcome remain **unperformed / unknown** until printed.

The companion `support-review-reopened.json` checks the nine unmodified support-free parts for disconnected
layer components; the horizontal long screw has a separate support-interface review. It retains three full-width spring bridge paths anchored at both ends in
each frame half, maximum free spring span 9.98 mm and square coupling roof span
10.38 mm. The bridge image shows the previous layer in grey and current bridge
paths in orange. These checks do not establish physical bridge sag or spring force.
