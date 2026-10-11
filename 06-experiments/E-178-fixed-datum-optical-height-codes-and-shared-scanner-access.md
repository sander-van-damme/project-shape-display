---
status: complete
builds-on: [E-004, E-046, E-176, Q-006]
---

# Shared optical height readback has a corridor, but cannot replace lock proof

**Retain fixed-datum coded tails with row mirrors as a conditional sensing lead.
Reject height-only replacement of support/pickup proof and direct reuse of the
screened short-working-distance CIS.** Four shared cameras can geometrically
observe 80 columns per row in the constructed section. This does not remove
E-176's 320 setters, its pickup-state proofs or their access problem. No complete
architecture, price advantage, printing or purchase is accepted.

Input main `cb58cd1`; LAB-291. Reproduce with
`python3 tools/curated-experiment-checks/E-178/readback.py` (standard library;
JSON disposable). Evidence: ideal specular rays through finite apertures and
opaque solids, exhaustive binary-code faults, analytical error and motion bounds;
self-review only. No optical render, diffraction/contrast model, fabricated marks,
calibrated manufacturing distribution, real readback or reliability measurement.

## Search and complete-machine comparison

Two different analogies were used: **absolute encoder scales** move position
information through a fixed datum; **document scanners** share image acquisition
across a line. Their combination is new relative to E-004/E-046/E-176's tested
interfaces, not a new optical principle or patent-novelty claim. This is a sensing
axis, not another complete actuation architecture. No search-saturation claim.

| Combination | Selection, motion, retention, load, verification/recovery |
|---|---|
| Direct heads with local/contact readers | Spatial head selection and bidirectional motion; grounded stops retain terrain. Observe actual column and actual support before withdrawing. E-176 direct B4 is the conditional timing control; capture/arrest/cost remain open. |
| Shared lift with underside endpoint camera | Individually program pickup/ground states; deck transports; ground supports retain. Camera observes tail endpoints, but height contrast occludes them just as in E-004. Reset-state proof still needed before ascent. |
| Shared lift or direct heads with fixed-datum codes | Same setters, energy and ground paths; tail attached to actual column carries height marks through one observation plane. Row mirrors and moving cameras read marks; compare expected height, reject ambiguous/stale data, keep support on failure. Additional lock/pickup observation remains necessary. |
| Stationary command flags photographed together | Shared camera is easy to place at a common plane, but flags report commands rather than actual column position. A detached or jammed column aliases correct operation. Stop as sole final verification. |

[Renishaw's encoder explanation](https://www.renishaw.com/pl/safety-first-the-position-determination-and-checking-algorithms-of-the-resolute-true-absolute-optical-encoder--47195)
uses absolute scale redundancy, contrast checks and a separate position estimate;
this motivates checking code faults, not transferring its accuracy or safety claims.
[Mitsubishi's CIS overview](https://www.mitsubishielectric.com/bu/contact_image/cis/index.html)
describes a sensor line, rod-lens array and illumination. These are real integrated
functions, not evidence of a cheap camera, usable working distance or our optical
performance. Sources accessed 2026-10-11.

## Finite path around a moving tail

Coordinates are mm; Z up. At each 5.08-mm XY site a hypothetical solid tail is
3.2 wide in X, 1.2 thick in Y and extends Z=`h−42.4…h+2`, for five column heights
h=0/10.1/20.2/30.3/40.4. Marks lie on its Y=+.6 face. The tail is rigidly part of
the column, not a separately latched proxy. The 44.4-mm tail over its full 40.4-mm travel is clear of
the nominal optical strips; integrating this added extension with existing
supports/guides is **not constructed**.

Each row has a stationary mirror strip spanning X across the board. Its nominal
section is `Y+Z=1.6`, endpoints (Y,Z)=(.9,.7)/(2.3,−.7), giving 1.98-mm inclined
width. A .3-mm backing on the positive-normal side would stay away from incoming
and reflected rays and nominal tails; end attachments, straightness, modular
seams and structure remain unbuilt. Two 203.2-mm pieces per row fit the X1C module
length, making **160 aligned pieces / 32.512 m** of optical strip, not 6,400 mirrors.

Four cameras at Z=−50, spaced every 20 columns, move together in Y to each row;
one local camera center is (48.26,1.6,−50). Each covers 101.6 mm nominal width.
Reflection puts the central marks in a virtual plane Z=1, independent of height.
This is a geometric working-distance construction; no affordable lens, sensor,
illumination, focus, housing, cable or controller has been selected.

The executable reflects each target in the mirror plane, intersects the camera
ray with the **finite** mirror, verifies the specular direction and optical path
length independently, then checks the incoming segment against opaque row
swept envelopes and the reflected segment against eight finite neighboring tails.
The envelope union Z=−42.4…42.4 encloses all heights and intermediate motion; it
allows every neighbor to take its own adverse height. A clipping witness is
resolved to a finite 3.2×1.2 tail, rather than claiming every envelope hit is real.
Mirror X-edge checks include the first camera segment; translating other segments
preserves the interior geometry. Marks on either side of a seam need a separate
usable-aperture/registration design.

Each scenario tests **20,480 rays**: 20 columns × 4 tracks × four sample-footprint
corners × 64 sign combinations. Independent signs cover mirror Y/Z offset,
camera Y registration, tail face offset, pupil Y edge and mirror-angle error.
Errors may be coherent for an entire row/batch; expanded neighbor boxes admit
opposed local errors. No iid assumptions or yield estimates.

| Translation bound / angle / pupil Y radius | Finite mirror misses | Incoming envelope obstructions | Minimum mirror-edge reserve |
|---|---:|---:|---:|
| 0 / 0° / .5 mm | 0 | 0 | .864 mm |
| ±.05 mm / ±.2° / .5 mm | 0 | 0 | .781 mm |
| ±.10 mm / ±.5° / .5 mm | 0 | 0 | .691 mm |
| ±.20 mm / ±1° / .5 mm | 0 | 0 | .508 mm |
| ±.10 mm / ±.5° / 1.5 mm | 0 | 10,240 | .651 mm |

Last-row witness: ray from (48.26,0,−50) via
(−.3373,1.4690,−.0684) to (−1.28,.5,−.08) hits row 0, column 5 at height 0.
This proves pupil clipping, not total image loss: the center rays can still pass.
Small-pupil illumination, noise and image quality have not been evaluated.

**Visibility alone misses a mechanical collision.** The finite mirror's minimum
Y gap to the tail is `1−2e−.7√2 sin(45°+angle)`: .300/.198/.094/−.112 mm for
the first four scenarios. A segment/solid check confirms the ±.2-mm/±1° case
cuts into a lowered tail despite all its rays being visible. Reject that assembly
error box. The ±.1-mm/.5° case retains only .094-mm geometric clearance; roughness,
backing attachment and unbudgeted bow could consume it. This is not qualified fit.

An independent continuous incoming-corridor bound at ±.1 mm/±.5°/.5-mm pupil
is positive: the whole mirror has Y≥`1.5−.7√2 sin(45.5°)` and the whole pupil
Y≥1.0, versus the opaque row edge at .7. The reserve is **.094 mm**.
The next row is farther away. Segment subdivisions 1/4/16 agree with the exact
slab test. Error-box corners alone do not certify every nonlinear intermediate
mirror pose or a real optical image. The wider ±.2-mm scenario already fails
physical clearance.
Tail lean/bow must be inside the swept lateral envelope; it is not automatically
covered by a root-position tolerance. Real PLA/X1C warp, layer texture, first-layer
bias and dimensional capability are unknown. Mark placement, optical distortion,
mirror shape and model discrepancy need separate calibration/error budgets.

Direct underside endpoint imaging has an exact counterexample: camera (0,0,−100)
looking at column 10's raised tail tip (50.8,0,−2) is blocked by column 9's lowered
tail spanning Z=−42.4…2. Merely moving E-004's camera below the board does not solve
universal visibility. The mirror path changes the observed surface and route.

## Codes reject some faults, not support failures

Four .6-mm-wide tracks on .8-mm centers fit the face. Five words
`0011/0101/0110/1001/1010` have weight 2 and minimum Hamming distance 2;
all dark/light are invalid. Exhaustive synthesis finds no five-word, single-bit
error-detecting code at three bits and 68 codebooks at four bits when both uniform
words are excluded. No error correction is attempted: reject nonmembers and
compare the decoded level to the requested level.

Exhaustive faults: **0/20 single-bit** changes become another valid word, but
**16/30 two-bit** changes do, and global inversion swaps valid levels in **4/5**
cases. These are counts of constructed faults, not probabilities. Five tracks
with weight-2 cycle words remove the inversion alias but narrow each mark to
.48 mm at .6-mm pitch: at ±.2-mm registration and .08-mm half-footprint the
horizontal reserve becomes −.04 mm, versus +.02 mm for four tracks. Trade spatial
margin for redundancy explicitly. Known dark/bright references and exposure checks
are still needed; a code does not authenticate row identity or freshness.

Marks occupy only ±.4 mm vertically around each correct level, with dark space
between. Sample half-footprint is .08 mm; edge-straddling samples are rejected.
A total vertical datum/mark/optical error bound e gives guaranteed acceptance
within `.32−e` and possible same-level acceptance out to `.32+e` mm. At e=.1/.2,
these are .22/.12 and .42/.52 mm. At e=.35, nominal acceptance is no longer
assured. These are hypothetical aggregate bounds, not surface accuracy requirements
from 02 or finished-print capability. Broad 10.1-mm bands would accept large
between-level errors and are not used. Correlated bias can shift all 6,400 readings.
Target-directed rays above prove access only; actual pixel-to-datum registration
must meet these budgets. At a granted 1,280 pixels per 101.6-mm field, .6-mm marks
span 7.56 pixels before distortion/fiducial margins; resolution is not contrast.

For every height, changing ground support or pickup state leaves the marks
unchanged: **15 unsafe/undesired support–pickup combinations** alias the five
properly grounded/clear states. A retained active pickup before the next ascent
is invisible. E-176's reset proof cannot be replaced by this camera. Support
breakage, column/tail separation, old frames and row misassociation are additional
uncovered faults. Reject/retain support/reacquire once is a protocol requirement;
no mechanical repair or false-accept probability is demonstrated.

## Full-board time, cost and decision

A flat scanner housing must lie below the deepest tail (−42.4). The virtual marks
are at +1, giving **>43.4 mm** optical working distance before body clearance.
[Mitsubishi's screened KD-AX/MX specifications](https://www.mitsubishielectric.com/bu/contact_image/general/lineup/index.html)
give 12/14.5-mm focal distances; the
[2022 KD-CXF specification](https://pl.mitsubishielectric.com/global/common/pdf/global-news/pr/2022/221130-a_3559_en_g.pdf)
gives 27.1 mm. Neither directly fits this below-tail layout. A new long-distance
lens or relay would be a new subsystem; do not borrow a CIS line rate as a pass.

Use the previous hypothetical 200 mm/s and 5,000 mm/s² carriage limits, no overlap,
.5-s registration/preparation, and one in-place .2-s retry plus a repeat read.
For stopped acquisition, `T=79 move(5.08)+move(401.32)+81 t_row+.7` includes
return to home and all accelerations. Total scan is **8.188/9.403/11.833/15.883 s**
for t_row=.005/.02/.05/.1 s. The slot must include settling, exposure, transfer
and decoding, which have no measured timing. At .02 s, a far-end five-row patch
needs **5.067 s**; localization saves reads but not travel from home.

Adding the .02-s scan to the existing B4 allocations, while retaining their
unresolved proofs, gives **28.872 s direct / 30.897 s broadcast lift**. This is
an incremental allocation, potentially double-counting replaceable height checks;
it neither certifies direct heads nor universally rejects shared lift. Removing
old time requires identifying which physical observation this replaces. The
broadcast package as unchanged plus this scan misses 30 s.

A continuous one-pass/return floor is **4.813 s**, conditional on pipelined
acquisition every 25.4 ms and exposure ≤.5 ms for .1-mm motion blur, with the same
prep/reacquisition allowance. Illumination and processing must earn that overlap;
stop/go cannot use the long-traverse motion time while adding stopped row slots.
Persistent read failures halt acceptance; restoring a wrong column is not included
in a camera-only retry. Final scans cannot provide fast active-motion arrest.

Inventory: 4 camera/lighting channels, one carriage/drive, controller/cables,
160 mirror sections and mounts, 6,400 coded faces, and (if wholly additional)
**1.091 L** of tail blanks before supports/scrap. No print-time or mass estimate
without material/slicing. Marking each tail for 10 s alone is 17.8 h; $.01 purchased
cost per face adds $64. The purchased boundary is
`4 c_camera + c_axis/control/illumination + 160 c_strip + 6400 c_mark`, in addition
to the entire actuation machine. No price band is claimed. Replaceable mirror
rows/marks and access for cleaning require construction; dust, delamination,
creep and wear remain common/local fault sources.

**Next discriminator:** construct a shared view of the *actual load stop and
pickup output* alongside the column mark, or show why its projected states alias.
Compare backed comb, direct head and field-jaw layouts; stop if the view requires
one precision relay per cell or cannot expose engaged overlap. Also test whether
locally known fiducials can bound registration within .2 mm without 6,400 manual
calibrations. This offers more decision value than sourcing a fast camera or
refining a height-only scanner. No mechanism is selected and no print is requested.
