---
status: complete
builds-on: [E-054, A-013]
---

# Side-cheek shelves do not geometrically confine pawl pitch

## Decision

Modify the E-054 continuation: establish angular restraint before spending on
shelf/ground-attachment FEA. Its decoupled-thickness witness remains a clearance
witness, but neither tight nor middle slots provide an upper/lower-shelf pitch
stop for the specified wing. Do not inherit prescribed translation as a guided
support mode. This rejects that restraint claim, not A-013 or side-cheek guides.
Reopen with explicit anti-rotation geometry, a longer/staggered bearing, or a
complete rack/pawl contact equilibrium model that supplies the missing restraint.
No print or hardware-performance claim follows.

Input main `7c3511f`; deterministic rigid geometry calculation, not physical
measurement, dynamic/contact equilibrium, FEA or calibrated manufacturing data.
Run `python3 tools/curated-experiment-checks/E-055/angular_slot.py`.

## Construction and independent check

E-054 gives a rectangular wing of longitudinal length L=0.8 and thickness t=2
mm, inside parallel shelves separated by H=t+e+0.2. Rotate about transverse y;
y extent is unchanged, so the outer side walls supply no pitch stop. The exact
vertical extent at angle theta in [0,90 degrees] is
`h(theta)=L sin(theta)+t cos(theta)`, with maximum `sqrt(L²+t²)`.
A freely translating wing can remain between the shelves whenever h≤H.
This deliberately favorable, infinitely long shelf model retains contact area;
finite shelf ends can remove support but cannot add the missing vertical stop.
End caps, retention and release links were absent from E-054.

| Placement bound e (mm) | Slot H (mm) | Maximum wing height (mm) | First opposing-shelf stop |
|---|---:|---:|---|
| 0.15 | 2.35 | 2.154066 | None through 90 degrees |
| 0.35 | 2.55 | 2.154066 | None through 90 degrees |

An independent corner transform checks 91, 901 and 9,001 angles per bound;
maximum-height errors converge below 1e-8 mm. The analytic maximum proves the
continuum result, avoiding an inference from sampled clearances. Zero-gap and
0.05-mm-gap holdouts recover a stop. Symmetry covers opposite rotation.
No random seed or probability distributions are used.

## Changed-design bounds

Total slot play must be ≤0.154066 mm even to encounter an opposing shelf;
contact by 5 degrees requires ≤0.062114 mm for this wing. These are total gaps,
not per-side tolerances. Both are below E-054's 0.35/0.55-mm rigid placement
allowances. No claim that X1C can achieve them is made. Shelf thickening outward
from the existing slot does not change H and cannot fix restraint.

Alternatively a chosen stop angle alpha requires
`L >= [H-t cos(alpha)]/sin(alpha)` on the first-contact branch:

| e (mm) | L for 5 degrees | L for 10 degrees | L for 15 degrees |
|---|---:|---:|---:|
| 0.15 | 4.103 | 2.191 | 1.616 |
| 0.35 | 6.398 | 3.342 | 2.388 |

Angles are sensitivity probes, **not accepted support-angle requirements**.
Within the unchanged E-052 section, increasing L grows x envelope one-for-one:
5-degree witnesses would need 7.193/10.488 mm versus 5.08-mm pitch. Even the
middle 15-degree probe needs 6.478 mm. This rules out simply lengthening that
same packaging to those angles; it does not exclude staggered internal guides
or a distinct key geometry. Fine clearance is not the only permitted escape.

## Evidence limits and next discriminator

A kinematically admissible rotated pose need not be dynamically reachable or
stable under the actual load. Bottom-shelf contact can be stable; tooth contact,
friction, preload or a gripper can oppose rotation. The calculation does not
predict spontaneous tipping, tooth-overlap loss, load capacity or board yield.
Rack/web collision may stop rotation or cause a jam; it cannot be silently
counted as an engineered bearing. E-054 placement bounds remain uncalibrated
competing scenarios; batch/common biases change many slots together, not
independent cell failure probabilities. Warp, wear and elasticity remain absent.

Next useful geometry must include rack, wing, angular restraint, return and
axial retention with contact load/support transfer in required states. Compare
staggered long bearings or keyed guidance against the simple slot; preserve the
channel-cost gate in Q-012. Only after a retained pose/load path exists does
shelf/attachment stress refinement discriminate viable embodiments. No new
full-machine timing, purchased-cost or reliability pass is established. This
is self-review with exact geometry/limiting cases, not independent validation.
