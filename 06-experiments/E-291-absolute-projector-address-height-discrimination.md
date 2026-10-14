---
status: complete
builds-on: [E-290]
---

# Absolute projector address height discrimination

**Absolute codes escape E-290's weak-reflection phase bias, conditionally; they
do not identify which optical path is direct.** Run
`python3 tools/curated-experiment-checks/E-291.py` (standard library).
This is a new source-address construction, not another periodic-carrier sweep.
[Gupta et al., IJCV 2012 project](https://www.cs.cmu.edu/~ILIM/projects/IL/lightscan/lightscanindex.html)
(accessed2026-10-14) documents conventional Gray-code failures under indirect
illumination and alternatives for different transport regimes. It establishes
neither our transport bounds nor a usable projector. All numerical inputs below
are explicit synthetic scenarios; no captured images or measured PLA behavior.

## Construction and discrimination

Retain D300/b8 and camera ray r from E-290. Projector coordinate
`q=r+8/(300-z)` occupies field[-.025,.025). Divide it into2048 bins and encode
each index as11-bit reflected binary Gray code `n XOR (n>>1)`. Capture each
bit and complement plus all-white/all-black: **24 frames**. This is absolute
addressing within a finite field, not a sinusoidal phase or modulo carrier.
Forward intensity is `ambient+1000*gain*sum(weight*bit(q))`. Nonnegative
transport weights have no direct/indirect label in the measurement. Decoder
subtracts complementary pairs, requires normalized contrast≥.5 on every bit,
checks pair sums against white+black within2DN, rejects flat/saturated returns,
then intersects the decoded bin's height interval with physical0–50mm travel.
It receives calibrated r and travel, never commanded height or oracle masks.

Calculation: 90 rounded12-bit direct controls (z0/10/25/40/50, gain.05/.2/1,
ambient120/300DN, three rays) contain the true height in the returned interval;
maximum midpoint error.11530mm. All2048 index/code roundtrips pass a separate
integer check. Maximum height-bin width is.27441mm near minimum height;
this is quantization only, not a calibrated accuracy bound or product tolerance.

For direct weight1 and total indirect weight≤.2, every point-sampled bit retains
the direct sign: minimum normalized contrast `(1-.2)/(1+.2)=2/3`.
Six indirect-ray cases confirm the analytic bound. In particular true25mm plus
20% return from the45mm projector ray gives interval[25,25.23060]mm instead of
E-290's false28.3788mm. Equal25/45 weights return unknown. This proof assumes
static linear transport, sharp bins and no local temporal drift; it does not
establish that actual caps have a dominant direct path.

**Counterexample:** true25mm with direct weight.2 and reflected weight1 from the
45mm ray returns[44.90948,45.10791]mm, midpoint45.00870mm, with minimum contrast2/3
and exact pair sums. Relabeling the same two weights as a true45mm direct surface
plus a weak25mm reflected path changes **none of the24 raw intensities**. Both
hypothesized cap points lie on the calibrated camera ray within a4.4mm cap.
This is an admitted nonnegative transport ambiguity, not a constructed reflecting
3D scene or evidence that our PLA realizes it. More source patterns alone cannot
label the same transport distribution's direct component. A stronger contrast
threshold can reject this example, but cannot establish directness: a sufficiently
weak direct return can leave an arbitrarily confident reflected address.

## Optical and whole-machine obligations

One bin projects to.006714mm at z25; the coding-axis field spans12.5mm at z50.
Four caps run across the *other* axis, requiring19.64/23.45/48.40mm field widths
at5.08/6.35/12.7mm pitch. Thus2048 independently resolved stripe positions across
one row are assumed; no lens, projector pixel pitch, focus or camera footprint
qualifies them. Uniform finite-footprint controls at a bin center preserve the
result at0/1-bin width and return unknown at2/4 bins;128/256 midpoint quadratures
agree. At a bin boundary even a one-bin direct-only footprint returns unknown.
These box averages are sensitivity controls, not a measured optical PSF. Missing
visibility, prop identity, camera sampling, calibration, noise, drift and motion
remain unqualified. No guarantee of finite scan-to-accept time for covered caps.

No resident parts are added or removed:1024/4096/6400 threaded pairs retain their
manufacture, guides, thrust, capture and holding duties. Shared projector/camera,
references and upper carrier replace no mechanical support. E-290's unsourced
base-plus-optics$1068–1778 allocation is inherited only for comparison; it does
**not** price the fine-pattern capability. Retain ~$500 original case, possible
~$1000 finished value and separate$1000–1500 demonstrator, without purchase.
At assumed.1s/frame and four caps/group, acquisition alone costs614.4/2457.6/3840s
at1024/4096/6400. Local1/4/8 groups add2.4/9.6/19.2s before writing, routing,
undocking, settling, calibration and retries. E-270/E-276 conditional gameplay
schedules, S40/S50, minimum/raised neutral and paid preparation remain unchanged;
these are sensing increments versus~30s, not new representative-map results.

**Decision:** retain the direct-dominant absolute-code control; park optical
pattern refinement. A next optical investment needs actual calibrated cap images
or a physically constructed path discriminator and earned resolution/exposure,
not another code-count or threshold sweep. The positive result removes a specific
weak-reflection alias; it does not close actual-height acceptance. No hardware,
print, holding or manufacturing qualification. E-281 remains optional/unprinted.
