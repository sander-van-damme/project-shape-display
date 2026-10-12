---
status: complete
builds-on: [E-167, E-170, E-236, E-249]
---

# Small axial turns cannot release this fixed rail beside unchanged square tops

**Park the tested short-turn embodiment; do not refine its lug, guide or latch.**
A rigid column eliminates a separate resident release member, but the finite
support below needs **14.63762°** yaw while its 4.8-mm square cap first touches
an unchanged same-height neighbor at **7.14839°**. Lifting before turning does
not solve descent through the old support. Quarter-turn transit remains a
separate, conditional escape already demonstrated in E-167; neither route has
an affordable supported writer. No fabrication or machine selection follows.

Input main `522b34b`. Reproduce:
`python3 tools/curated-experiment-checks/E-250/screen.py`.
Standard Python; imports E-167's polygon SAT. Evidence: **analytical calculation,
finite rigid geometry, deterministic error scenarios and self-review**. No CAD,
physical measurement, sourced process prior, contact dynamics, priced BOM or
independent validation. JSON is reproducible output, not retained evidence.

## Architecture first: what rotation does and does not remove

The candidate is one integral cap/stem/periodic-lug column rotating about its
vertical axis, with stationary grounded rails. Five 10-mm-spaced stations over
40-mm travel are a comparison grammar, not a product resolution requirement.
A shared row head must capture selected columns, unload their rail, rotate,
translate to the target, restore orientation, seat, prove support and detach.
Unchanged columns remain seated on their own fixed rail; no row-wide withdrawal
is needed. Their physical disturbance still depends on clearance and frame motion.

| Obligation | Small axial turn / shared-motion interpretation |
|---|---|
| Selection and state | Independently selected column angle; height is stored by seated lug position. A motor command is not retained mechanical selection. |
| Motion and load | Head supplies bilateral Z and yaw reaction until seating. A shared stroke can supply energy, but arbitrary heights require selective coupling and supported disengagement. |
| Rest retention | Vertical load: lug → rail → frame. Bare flat rail does **not** retain yaw; angular restraint remains unconstructed at 6,400 sites. |
| Intermediate retention | Loaded capture, grounded arrest and retained selection required. Removing power while released can drop the column; a shared motor brake does not cover a failed capture. |
| Verification/recovery | Read actual height, angle and seated support before releasing the head. Retry only from known supported state; jams, broken grips and off-grid arrest require supported shutdown. Readers and recovery mechanism are unbuilt. |
| Regional change/service | One changed cell need not transfer its 79 neighbors. Accessible head can serve many cells, but failed resident parts need supported extraction; no service route is constructed. |

Historical evidence is reused within scope: E-167's 90° bayonet clears caps only
with a suitable interlevel turn; its current resolution extension needs
`D > 4.4+2E mm` for the original cap/lug/base. D=5 fails at total axial E=.35;
D=10 retains a window, not a hardware pass. E-170's complementary pickup collides
with the retention pocket; deleting that pocket removes retention. E-249 tilt
has a nominal rail-passage trajectory but fails an ordinary guide. E-236's
five-stroke shared program supplies logical reach, not a rotary capture or
unchanged primary support. These results do not justify another local repair.

## Finite cap/support exclusion

All dimensions mm. Pitch p=5.08; integral cap side d=4.8, thickness 2. A lug
occupies x=[.6,2], y=[−.4,.4], z=[0,1.2] in the seated pose. The fixed rail is
x=[1.2,2.54], y=[−1,−.1], z=[−1.2,0]. Nominal bearing area is .8×.3=.24 mm²;
this is not a strength allowance. A radius-.8 stem can join the lug without
intersecting this rail. Five such fixed forms are integral, not five moving
latches. Ideal guidance and independent head capture are granted for rejection.

A cap with overlapping vertical interval first touches an aligned neighbor at

`(d/2)(cos θ + sin θ) + d/2 = p`, giving θc=7.14839°.

The last support contact during positive yaw is the rail's upper-left corner
on the rotated lug's lower edge:

`1.2 sin θr + .1 cos θr = .4`, giving θr=14.63762°.

At θr the cap intrudes **.24860 mm** into its neighbor's horizontal extent.
Independent SAT checks both analytical thresholds at ±.000001 rad. Checking
16/64/256 subdivisions finds rail overlap at all **17/65/257** poses throughout
[−θc,+θc]. A continuous witness removes dependence on the sampling: the interior
lug point (1.6,−.35) stays inside the rail throughout this interval. Its x/y
coordinates are monotone there, with endpoint ranges x=1.54401…1.63112 and
y=−.54638…−.14818. Both remain strictly inside the fixed rail footprint.

**Descent witness:** let an old seated lug bottom move to z=−.6. Its 1.2-mm
thickness then overlaps the rail; a cap originally at z=[42,44] occupies
[41.4,43.4], overlapping an unchanged neighbor at [42,44]. Staying within the
small cap-safe angular component leaves the lug in the rail; holding the
release angle clears the rail but intersects the cap. A preliminary lift does
not change this later pose. This rejects short-turn transit through that
component, including recentering before crossing, not arbitrary combined motion.

Square symmetry gives another cap-safe component near 90°. There both cap and
this rail clear in XY, but reaching it crosses the forbidden intermediate
angles. E-167's interlevel lift supplies one conditional route; it is not a new
small-turn success. A separated nonrotating cap adds 6,400 captured rotary/thrust
interfaces. Smaller tops or supports at a wider radius change the architecture;
internal mechanisms are not required to fit within one cell.

For context, a point at radius R moves at most `2R sin(θc/2)`: **.24936 mm at
R=2**, irrespective of stem length. Thus axial rotation lacks E-249's long-stem
lever advantage. A .7-mm point displacement needs R≥5.614 mm nominally. This is
a displacement bound, **not** a universal support-overlap theorem; the finite
rail witness supplies the actual exclusion. At the tested release angle, caps
would need d<**4.57607 mm** (81.14% planar coverage at touching); this is an escape
condition, not a product acceptance threshold or permission for cap refinement.

## Manufacturing sensitivity and complete-machine burden

Ec is total adverse horizontal cap-gap loss, realized by reduced relative center
spacing. Es moves the rail's top edge inward toward the lug. They are independent
bounded scenarios; equal values below are competing cases, **not measured X1C
priors, standard deviations or probabilities**. Common registration bias/warp can
consume a whole bank's margin; rigid common translation cancels.

| Ec / Es | Cap-safe angle | Support-release angle | R=2 point travel before cap contact |
|---:|---:|---:|---:|
| 0 / 0 | 7.148° | 14.638° | .249 mm |
| .05 / .05 | 5.793° | 17.068° | .202 mm |
| .10 / .10 | 4.477° | 19.471° | .156 mm |
| .20 / .20 | 1.943° | 24.165° | .068 mm |

At Ec=.28 the aligned caps already touch. Angle error, guide play, loaded bending,
roughness, wear and debris spend additional margin. Nominal failure means no
calibrated distribution or speculative fine-printing capability can rescue the
specified dimensions. Rail strength, creep, yaw restraint and stem stability
remain unqualified; thin stems are not a load-capacity claim.

Ledger below counts the rejected direct short-turn allocation B4, so comparison
precedes detail. Shared-row energy does not eliminate its independent functions.

| Function | Cell / row | Bank / reusable head | Board |
|---|---|---|---:|
| Integral moving column / fixed lug forms | 1/5; 80/400 | 1,600/8,000 resident | 6,400 /32,000 |
| Fixed bearing / angular-retention duties | 1/1; 80/80 | 1,600 each resident | 6,400 each; yaw restraint unbuilt |
| Two assumed guide duties | 2; 160 | 3,200 resident | 12,800 |
| Bilateral capture / held Z / held yaw | shared | 80 each/head | 320 each |
| Height, angle and support proof duties | shared | ≥80 each/head | ≥320 each |
| Feed, grounding, arrest, reader systems | shared | 1 each/head | 4 each, not priced assemblies |
| Separate resident spring, rotor, insert, latch | 0 constructed | head parts unknown | 0 credited; additions must be counted |

Fixed lug forms are not equivalent to moving failure sites. Guide contacts,
angular seats, wear faces, capture joints, sockets, fixtures and inaccessible
failure points need actual designs before a complete part count is possible.
An illustrative 72-mm radius-.8 stem/cap/five-lug **solid union** is 1.259 L/board:
23–70 extrusion hours at assumed 15–5 mm³/s, 26–78 hours for a 10% scrap fraction,
before guides/frame/heads. No slicing estimate. Upright stem stability, horizontal
surface/layer quality and lug strength are unresolved. At assumed 5 s/insertion,
6,400 placements cost 8.89 h; 320 captures at 10 s add .89 h before actual assembly,
wiring/calibration. Bed-size segmentation and module alignment remain required.

## Timing, economics and architecture ranking

Use the E-249 direct-head accounting with assumed linear v200/a8000 mm/s units,
angular v720/a7200 degrees/s units, two unload/reseat strokes, 40-mm loaded travel,
.10-s acquisition/proof/release, two empty strokes of 40+lift, 5.08-mm row feed,
one complete row retry, and 2 s for map ingestion/registration/final settling.
`T=2+(ceil(80/B)+1)*row_slot`. Every allowance starts after receiving the map;
there is no prepared mask credit. These are optimistic **allocations**, not a
built programmer, achieved readback or qualified recovery bound.

| Granted interface | Banks / reusable channels | Calculated map time |
|---|---:|---:|
| Nonrotating direct control, .6-mm release | 3 /240 held Z | 26.249 s |
| Rejected 14.638° turn, .6-mm release | 4 /320 held Z/yaw pairs | 23.974 s |
| 90° turn, 2.3-mm lift, free adjacent concurrency | 5 /400 pairs | 25.226 s |
| Same 90° route, two sequential alternating-column phases | 8 /640 pairs | 26.300 s |

The third row grants impossible coplanar adjacent midturns; the fourth charges a
simple collision-avoiding schedule, **not a universal minimum**. Pipelined phases,
fewer reusable channels or staggered heights need a new supported schedule.
Regional timing uses the number of visited rows and actual seek distance; U's
rail stays installed, but this experiment fails its cap clearance during change.

With an assumed $295 shared reserve, <$500 leaves <$.854 per 240-channel control,
<$.641 per 320-channel pair, or <$.320 per 640-channel pair, before unallocated
resident hardware. No quoted actuator/transmission/brake/reader BOM exists.
At L N/cell, 80 simultaneously loaded outputs require at least 80L N/head before
inertia/drag; a torque selector alone supplies none of that axial load. Full map
0→40 needs 256L joules of payload work before losses; shared drives must pay it.

E-236 has 400 selectors/pickups, seven fixed shelf levels, 26.681 s and $675
independent/$503 lean shared assumed allocation; U transfers support. E-249
allocates 320 Z/pitch pairs, 24.556 s, but its guide fails. Those are differently
scoped conditional results, not equal-fidelity winners. Axial rotation removes
the separate local release part and can preserve stationary U support, but
neither the failed small turn nor the existing quarter-turn has reduced the
loaded independent-output burden relative to the nonrotating direct control.

**Decision:** stop this bounded screen on the finite witness and unresolved
shared capture/arrest burden. No guide, thinner land, latch, rotor or cam study;
no print. Reopen only with a complete shared acquisition/retention topology that
reduces held loaded outputs and explicitly satisfies cap passage and U support.
The next useful synthesis compares a common loaded motion path with independently
selected attachment/release against these direct-head counts, before drawing
any local engagement feature. No claim that all axial-release principles fail.
