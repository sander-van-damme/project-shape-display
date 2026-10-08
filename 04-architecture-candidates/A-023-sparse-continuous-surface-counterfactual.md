---
status: candidate
builds-on: [P-008]
---

# Sparse continuous surface — requirement counterfactual

**Counterfactual only; not eligible under current independent-column envelope.**
Descriptors: individually addressed sparse screw jacks; thread/brake position
memory; shared supply with distributed motors; continuous sheet/bending lattice
load path; coupled out-of-plane deformation. This trades terrain degrees of
freedom for fewer purchased channels rather than silently preserving fidelity.

An 81–100-node grid at roughly 50.8-mm spacing drives a segmented compliant
sheet through 40 mm using bidirectional jacks; encoders and top depth sensing
close the terrain fit loop. Self-locking threads or positive brakes retain
height. Printed ribs spread miniature load between jacks; soft joints permit
slope changes. A broken actuator is braced and its replaceable tile disabled;
neighbor jacks can reduce sag but cannot recover lost fine terrain. The surface
and supported miniatures may move beyond the requested region due to elastic
coupling. No fog-of-war isolation equivalent is asserted.

E-063's bilinear interpolation is a reproducible kinematic surrogate, not sheet
mechanics or an optimized elastic surface. Across grid offsets, a smooth
40-cm-period hill has 0.449–0.504-mm RMS error at 81–100 jacks; a one-cell-wide
40-mm wall can disappear completely (40-mm maximum error); a step smears with
up to 36-mm error; checkerboard error is 27.3–28.3 mm RMS. Even ~25.4-mm grids
need 289–324 actuators and still miss walls depending on alignment. Dense
independent pins reproduce these sampled maps exactly in this comparison.

A continuous sheet cannot provide vertical steps without folds/slack/openings.
An interpolated 40-mm rise across 50.8 mm has slope 0.787; stable miniatures
require compatible base friction and centre of gravity, not simply vertical
load capacity. A nominal 25.4-mm base encounters up to 20-mm height difference
on that ramp. A bilinear basis change influences a square up to 101.6 mm wide
at 50.8-mm node spacing; actual elasticity can spread farther. Continuous
opaque cover also removes independent cell openings/occlusion opportunities;
projection may color fog-of-war but does not restore walls or isolated motion.

At $250 shared reserve, 100 complete channels have $2.50/channel under $500;
289 channels have $0.865/channel, before sheet/fasteners if outside the reserve.
These are thresholds, not supplier BOMs. Aggregate load still reaches frame;
membrane sag, creep, jack backlash, repair seams, power and update time remain
unqualified. Benefits are fewer repeated guides/drives and accessible tiles;
losses are arbitrary walls, narrow stairs/pits and strict regional independence.
Retain as quantified assumption-value evidence, not a recommended requirement
change. Reopen only for a separately authorized product variant or a hybrid
with explicit extra wall/step hardware and full cost/isolation accounting.
