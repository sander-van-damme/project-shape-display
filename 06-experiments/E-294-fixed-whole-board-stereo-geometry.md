---
status: complete
builds-on: [E-270, E-276, E-293]
---

# Fixed whole-board stereo removes scanning, not terrain shadows

**Retain one fixed stereo assembly as a partial exposed-terrain monitor; park it
as sole full-board actual-cap proof.** One neighboring 40-mm column completely
hides a real edge cap from one imager at all three pitches. This obstruction
holds with perfect images, whereas a shallow coarse scene retains useful
geometric access. No camera, decoder, accuracy, print or purchase is selected.

Reproduce `python3 tools/curated-experiment-checks/E-294.py` (standard Python).
Evidence: sourced component specifications, analytical bounds and 7,536 finite
ray/box cross-checks; self-review, not hardware validation. This changes E-293's
moving four-cap reader to a fixed whole-board observation, eliminating its
reader XY, transported datum and separate head-witness camera duties.

## Concrete sourced comparator

Sources checked 2026-10-14:

- [RealSense D455 product page](https://www.realsenseai.com/products/real-sense-depth-camera-d455f/)
  identifies a 95-mm baseline, nominal 87°×58° depth field, ~520-mm minimum depth
  at maximum resolution and 600-mm lower end of its ideal range. Its advertised
  <2% depth error at 4 m is **not** a submillimetre specification at our distance.
- [D400 datasheet](https://realsenseai.com/wp-content/uploads/2025/09/Intel-RealSense-D400-Series-Datasheet-October-2025.pdf),
  tables 3-14 and 4-3: D450 imagers have nominal 90° horizontal field, 1.93-mm
  focal length, f/2 and 1280×800 active pixels. USB3 1280×720 depth and left/right
  luminance modes run at up to **30 fps**, not the advertised maximum 90 fps.
  The projector supplies a static infrared texture, not E-291's Gray sequence.
- [Official store](https://store.realsenseai.com/buy-realsense-depth-camera-d455.html)
  lists $499 before shipping/tax and applicable surcharge. This is a dated
  component listing, not a delivered quote or authorization.

Assume parallel, undistorted nominal pupils at (±47.5,0,650) mm above the lowest
terrain; highest S50 surface is 600 mm away. Camera y aligns with one central
row. All grids span 406.4 mm. A nominal 87°×58° field covers the board at the
highest plane (about1138×665 mm); the camera need not scan for *field coverage*.
Occlusion is different. Real intrinsics, distortion, image crop and working
modes must be read/calibrated; the nominal model is not a unit calibration.

Use f=640 pixels from the individual-imager horizontal field, pupil radius
1.93/2/2=.4825 mm. Ignore blur, noise, indirect light, correspondence windows and
IR-pattern coverage: optimistic geometry. At z0, widths4.4/10.3 mm span only
4.33/10.14 pixels. Output depth units do not establish depth resolution.

|Height z, mm|mm/pixel|Error for bounded ±.05 / .10 / .25 pixel disparity, mm|
|---:|---:|---:|
|0|1.016|.348 / .696 / 1.742|
|30|.969|.316 / .633 / 1.585|
|50|.938|.296 / .593 / 1.484|

For depth L=650−z, d=fb/L, exact worst error is `L*e/(d-e)`.
At z0, a .5-mm diagnostic bound needs e≤.0719 pixel **before** scale, pose,
mount or cap-identity error. These are competing error allocations, not claimed
D455 performance or a new product tolerance. Static texture is an implementation
advantage over an invented projector, not evidence of correspondence on these
small printed caps. Averaging cannot remove common bias or see a hidden cap.

## Whole-board access and a complete obstruction witness

Widths/pitches are4.4/5.08,4.4/6.35 and10.3/12.7 mm. The quarter-grid narrow
cap remains a comparison, not a selected tabletop. Independently place one low
cap at each board address, with eight high neighbors. These are relocated pit
stress cases, **not one simultaneously realizable map or gameplay statistics**.
For t=(H−z)/(650−z), local coordinates of a sufficient clear rectangle satisfy

```
center_i = t*c_i/(1-t)
half_i = (pitch-width/2-t*(baseline_i/2+pupil_radius))/(1-t)
```

Intersect with the cap square; baseline_i=(95,0). This guarantees both complete
pupils remain within a square opening through the neighbor tops. Zero rectangle
does **not** prove no rays pass between separated columns. Independent segment/
box checks confirm sampled claimed-clear points; the continuous bound supplies
the sufficient guarantee. No mesh-grid convergence is needed for this bound.

|Pitch / cells|Nonzero sufficient patch, z0/H40|z0/H50|z30/H50|
|---|---:|---:|---:|
|5.08 /6400|0|0|2562|
|6.35 /4096|496|250|2806|
|12.7 /1024|744|450|1024|

Flat terrain grants all cap areas clear. Coarse z30/H50 retains mean67.16% cap
area in this bound, but z0/H50 only11.87%. Raised neutral improves local wall
access while genuine lower pits remain difficult. Initial neutral setup and
actual signed mechanical travel remain paid E-276 obligations.

**Exact all-ray obstruction, independent of the sufficient rectangle:** take
rightmost cap center x=(n−1)p/2,y0,z0 and the immediately adjacent column toward
the center at x−p,y0,H40. For every point on that target and every ray to the left
pupil, the near wall face is crossed below

`zmax = 650*p/(x+width/2+47.5−.4825)`.

The maxima are13.214/16.560/33.150 mm at fine/quarter/coarse pitch, all below40.
The y segment contracts toward a pupil lying inside the neighbor's y interval;
it cannot escape sideways. Thus one actual square column, without a seamless
wall or opaque miniature, blocks **the entire target** from one stereo imager.
Fractional-linear extrema establish the bound; 1,936 sampled rays per grid
cross-check it. More accurate disparity or higher frame rate cannot fix this.
Changing a concealed cap height slightly preserves the obstruction and cannot
be certified from that camera pair. Broad unobstructed terrain can still work;
this does not reject every fixed-camera location or multi-camera system.

## Complete-machine implications and stop rule

Adds one factory stereo/IR assembly, overhead mount, cable/host acquisition and
board datum references. No resident marks, apertures or sensors at1024/4096/6400
cells; existing threaded pairs, support, guide, manufacturing and service duties
remain unchanged. The fixed camera still needs fresh board-relative calibration,
identity and mechanical rigidity, but no transported head-to-optics transform.
E-270's covered-cap ambiguity remains, and hands/props can interrupt observation.

At1280×720, one frame period is33.3 ms; an **assumed** three-frame observation is
.1 s for all visible cells, versus E-293's conditional640/2560/4000-s dense local
reader+witness totals. Neither is complete update time or verified acquisition
latency. Exposure, processing, fresh settled frames, readback rejection/retry and
camera/board motion remain unpaid. E-276's four-spindle S40/S50 local26.84/31.07 s,
scene201/223 s, neutral271/332 s and dense392/452 s already granted .1-s proof per
station. A real fixed camera could support that allocation on exposed caps;
**do not subtract all old read time or report these waits as qualified**. Unknown
hidden caps stop completion rather than licensing blind motion or clearing
unchanged miniature-bearing neighbors. There is no finite recovery promise.

Accounting control: E-272/E-276 coarse four-spindle bought allocation$797.678–1768.233
contains reader+carrier+three extra paths$175–490 before10/15% reserves. Replacing
those with$499 camera plus an **unquoted** $40–120 fixed mount allocation yields
$1198.078–1916.583 with the same reserves. Camera tax/surcharge, metrology and host
capability remain unresolved. This exceeds the ~$500 and ~$1000 references; the
favorable case leaves about$302 under a$1500 demonstrator before exclusions.
No claim of a completed BOM, maker-time saving or premium player value follows.

**Stop fixed-single-camera decoding or mounting detail for universal proof.**
Retain the simpler monitor conditional on actual exposed-cap image/calibration
and support/isolation evidence. Reopen complete readback only through a constructed
observation path that covers the shadow witness, with total hardware/time costs,
or an explicitly narrower playable scope backed by owner evidence. Do not tune
thresholds, move uncommanded terrain to expose it, or infer hidden actual heights
from motor commands. No additional owner print; E-281 remains optional/unperformed.
