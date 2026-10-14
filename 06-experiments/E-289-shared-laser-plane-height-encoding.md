---
status: complete
builds-on: [E-270, E-288]
---

# Shared laser-plane height encoding

**Retain a small-field active-light comparator; do not select a sensor or call it
final verification.** A shared vertical light sheet changes the observable from
matching passive texture to intersecting a calibrated plane. This is a distinct
escape from the failed central-patch matcher, with no per-column marks, bores or
witness parts. Reproduce `python3 tools/curated-experiment-checks/E-289.py`.
The original screen uses ideal projected coordinates and ray/box visibility.
The extension below adds sampled one-dimensional stripe images and a decoder;
neither establishes actual laser/PLA behavior or physical accuracy. No print is
needed for this bounded model test.

[Micro-Epsilon's scanCONTROL manual, sections 6.5.4–6.5.7](https://www.micro-epsilon.com/fileadmin/download/manuals/man--scanCONTROL-29xx--en.pdf)
(accessed2026-10-14) identifies receiver and illumination shadowing separately,
and warns about reflections, rough surfaces and vibration. It supports the
principle and failure categories, not the following dimensions, error allocations,
scan rates or affordable sensor availability. Missing terrain returns must remain
unknown; interpolating across a missing cap is not independent verification.

Proposed transaction: stop/undock/settle, register the upper optical head against
independent frame references, acquire illumination-off/on observations, decode
only exposed identified caps, then accept/reject/unknown. Retain the opaque
support and all screw/guide/thrust/capture functions. Nothing contacts or releases
a column. A shared camera at(0,b,D) looks downward at a light sheet y=0 from a
source at(0,0,D); D is above the lowest cap and the sheet spans a short row segment.
For focal length f in pixels, `u=f*x/(D-z)`, `v=f*(y-b)/(D-z)`.
On the ideal plane, `z=D+f*b/v`, `x=-b*u/v`. Thus uniform caps need no stereo
correspondence or commanded height. Wrong sheet location, calibration, identity,
reflections or a prop can nevertheless produce the wrong surface result.

The source checks108 exact round trips, separate source/receiver shadows,
covered-cap ambiguity, and a calibration witness. A pin at z0/y0 and a pin at
z1/y.026667 produce identical pixels at x0 for D300/b8. The latter decodes as0.
A finite stripe with uneven return can shift its effective centroid; this witness
does not claim the actual line has that width or that PLA produces that bias.
A common sheet translation can be calibrated as an effective baseline. A
cap-dependent centroid shift cannot be removed by one shared constant. No
manufacturing micrometre tolerance is imposed on resident parts: the missing
quantity is an earned optical centroid/calibration error bound.

Assume1920×1080 pixels with10% reserve, favorably centered field, focal length
chosen to fit full caps at maximum height and stripe displacement over travel.
This is an abstract pinhole instrument, not a sourced lens/camera assembly.
Use a.4-mm central cap patch and.2-mm aggregate ray/solid placement reserve.
For field width W=(k−1)p and cap width w, sufficient adjacent-column/row margins
at the tallest S neighbor are `p−w/2−(W*S/(2D)+.2*(1−S/D))−.2` and
`p−w/2−b*S/D−.4`. Finite pupils, sheet thickness, yaw/lean, roughness, focus,
distortion, indirect reflections and housing are not qualified by these margins.
Nominal ray tests include three rows and two extra end neighbors, separately
putting each target at0 and every other cap at S; these are adverse local scenes,
not one simultaneously realized whole map. Negative sufficient margin alone is
not a nominal collision; ray tests distinguish the two.

|Pitch/cap, mm; S50|k /D /b, mm|X /Y margin, mm|Nominal hidden centers|Max height error, mm: pixel only /+centroid±.005 /±.02|
|---|---|---|---|---|
|5.08 /4.4|4 /300 /8|1.243 /1.147|0/4|.051 /.239 /.803|
|6.35 /4.4|4 /300 /8|2.196 /2.417|0/4|.061 /.249 /.813|
|12.7 /10.3|4 /300 /8|4.008 /5.817|0/4|.126 /.314 /.879|
|5.08 /4.4|16 /600 /40|−.678 /−.853|14/16|.076 /.151 /.377|
|6.35 /4.4|16 /600 /40|−.202 /.417|0/16|.094 /.169 /.395|
|12.7 /10.3|16 /600 /40|−.771 /3.817|2/16|.190 /.265 /.491|

Errors are exact maxima of sampled z0/S/2/S and independent signed centroid/pixel
error corners, granting known D/b/f and±.1-pixel localization. They are not
confidence intervals, precision specifications or proof of centroid extraction.
The favorable.25-mm diagnostic comparison is inherited, not an approved product
tolerance. Larger b improves triangulation but loses low-cap sightlines. S40
results are emitted by the source: k4 retains positive margins; k16 quarter-grid
has.588/1.083mm margins while the fine grid lacks the sufficient reserve.
Eight-cap fields at D600/b16 retain positive margins at all three pitches but
centroid±.005 already produces.282/.303/.423mm S50 error. No fine-margin tuning
follows. Missed motion/post-release slip can change an exposed cap return; hidden
caps at28/29 under the same opaque base remain indistinguishable. Later creep,
broken support and unchanged-neighbor isolation still require separate evidence.

**Scale and economics:** allocate.1s light-off+.1s light-on per group, one camera
and one sheet source, without claiming that exposure or settling is sufficient.
Full scans at k4/k8/k16 cost51.2/25.6/12.8s for1024 cells,
204.8/102.4/51.2s for4096, and320/160/80s for6400, **before** upper XY routing,
reference checks, undocking, settling, writing or retries. Failed wide-field
geometry cannot earn its cheaper time. Local1/4/8 groups add.2/.8/1.6s acquisition
only, not total gameplay waits. Reuse the earlier map schedules as conditional
controls; these counts do not claim a new representative map benchmark. Real
raised neutral/downward travel, S40/S50 and cold preparation remain paid. A
miniature obstruction has no finite automatic scan-to-accept time.

No resident hardware is removed: there are still1024/4096/6400 threaded pairs
and their guide/retention duties. Compared with passive two-camera stereo, the
shared equipment changes to one camera, sheet source, mounting, illumination
control/filtering, reference targets and an upper XY carrier; no claim that this
costs less. As **unsourced screening allocations only**, camera/lens$50–200,
source/driver$30–150, carrier/reference/guarding$100–300 and electronics$20–80
add$200–730. Adding E-276's optimistic$798 base gives$998–1528 before omitted
integration and qualification, not a BOM quote or selected$1000 product. The
~$500 reference remains unmet; a$1000–1500 demonstrator is not purchase authority.
Any real emitter selection owes an accessible-emission assessment appropriate to
players' eyes, interlocks/guarding and cost; no open laser installation is proposed.
Shared machined optical fixtures could reduce per-site work; no cap coating,
marking or individual finishing is credited as free.

**Decision:** the ideal plane encoder merits retention because it removes passive
texture correspondence without modifying repeated columns. The next discriminating
optical evidence would be actual or independently modeled stripe formation and
segmentation on exposed unmarked caps, with reference correction and scene-dependent
centroid/shadow errors; another ray-margin or pixel-error sweep is not sufficient.
It cannot solve hidden-cap verification. No physical accuracy, safety, speed,
sensor selection, purchase, print or full-machine qualification follows.


## Finite stripe and pixel decoder extension

**A clean stripe shape does not establish a correct height.** Reproduce
`python3 tools/curated-experiment-checks/E-289-stripe.py` (NumPy). This is a
forward radiometry calculation feeding a separate pixel-only decoder, not a
full two-dimensional scene renderer or an empirical material model. Cap identity,
exposure and an unobstructed central strip are granted; arbitrary cap segmentation,
prop recognition and correspondence remain outside this test. The manufacturer's
[triangulation overview](https://www.micro-epsilon.com/wiki/laser-triangulation/?sLang=en)
(accessed2026-10-14) identifies surface and ambient conditions as accuracy factors;
it does **not** source the following optical parameters or return gradients.

Explicit scenario: D300/b8/k4, original field-derived focal lengths, planar caps,
Gaussian sheet sigma.05mm, optical Gaussian blur sigma.65pixels, pixel-area
integration at32 subpixels and12-bit off/on images. Ambient+dark is120DN;
nominal peak signal1200DN. No random noise, speckle, distortion, motion or rough
geometry is simulated. Effective directional return is `.1*exp(a*y)`, clipped
to[0,1]. This is a bounded sensitivity construction, **not measured PLA albedo**.
The ambient return is held uniform: directional laser response need not equal
ambient response. A calibrated Lambertian scalar-albedo model could permit
ambient normalization; this experiment does not reject that conditional control.

The decoder subtracts off/on images, segments above max(2DN,1%peak), requires
one component, computes its centroid/width/skew and rejects missing, saturated
or |skew|>.1 returns. It receives neither target height nor an oracle stripe
window. These are illustrative quality checks, not a validated acceptance policy.
Uniform returns at0/10/25/40/50mm give the following controls. At true25mm,
a=8/mm shifts the optical distribution by.020mm; across y±.15mm its return
factor ranges.0301–.3320. Gaussian multiplication explains the result exactly:
`exp(-y²/(2s²))*exp(a*y) = exp(a²s²/2)*exp(-(y-a*s²)²/(2s²))`.
A reflectance gradient can therefore preserve a Gaussian shape while moving it.

|Pitch, mm|Uniform maximum height error, mm|25mm cap: single camera / two-reference correction, mm|Two opposed views: common / opposite gradients, mm|
|---|---|---|---|
|5.08|.0031|24.308 /24.310|24.999 /24.308|
|6.35|.0041|24.310 /24.311|24.998 /24.310|
|12.7|.0090|24.309 /24.301|24.997 /24.309|

All gradient returns pass the chosen shape check (|skew|≤.0101). Two known-height
references remove a common.7-pixel image shift but not the cap-dependent error.
The noiseless16/32/64-subpixel convergence difference is below.000001mm; this
checks numerical integration only. Missing and saturated controls return unknown.

A stronger whole-profile witness fixes the sheet width and changes true height
25→26mm. Define `y0=(y-b)*(D-25)/(D-26)+b` and directional return
`.1*exp((y²-y0²)/(2s²))`, clipped[0,1]. This makes the central sensor profile
match the25mm uniform cap. Its return range over y±.15mm is.0141–.4734;
clipped tails leave maximum **.034DN** discrepancy before quantization, with
essentially the same accepted centroid. This is a near-identical 1D profile under
explicitly different surface response, not proof that a real PLA cap takes this
form or that every image feature is ambiguous. Width/skew refinements alone do
not establish a robust guarantee over this admitted response class.

**Changed shared-sensor construction:** two cameras at y=±8mm can recover
`z=D-2*f*b/(vminus-vplus)` without knowing the stripe's y centroid **if both views
weight the same stripe distribution**. Common gradients cancel in the table.
Opposite effective gradients recreate the.69mm error. This adds one shared
camera/lens, synchronization and calibration, not any per-column part. It merits
retention only conditionally: view-dependent return, surface slope, two-sided
visibility and calibration require earned bounds. Existing ray margins for the
symmetric cap scene apply on either side; miniature obstruction remains unknown.
No hardware or safety selection follows.

One extra camera/lens adds the earlier unsourced$50–200 allowance: the optimistic
base-plus-optics comparison becomes$1048–1728 before extra mount/sync/integration,
versus single-view$998–1528, the ~$500 reference, and the distinct$1000–1500
research range. No quote or purchase. Simultaneous capture could retain the
allocated k4 acquisition51.2/204.8/320s at1024/4096/6400; sequential capture can
double it. Neither rate is earned. Local groups, all writer/preparation/settling
costs, S40/S50 reach and raised-neutral preparation remain as above. No resident
screw, guide, load-retention or manufacturing duty is removed.

**Disposition:** retain dual-view common-centroid triangulation as a conditional
shared-readback comparator. Park single-view stripe-shape qualification and
further assumed-gradient sweeps. Reopen through independently characterized
view-dependent returns on exposed caps, a constructed illumination method that
removes that nuisance, or actual calibrated images; hidden caps and safe physical
holding remain separate obligations. No new owner print is requested.

## Temporal-pattern control: static gain cancels, mixed paths do not

**Retain temporal coding as a distinct conditional observable; do not qualify
single-frequency phase readback from a clean waveform.** Reproduce
`python3 tools/curated-experiment-checks/E-289-temporal.py` (standard library).
A programmable projector replaces the fixed sheet and presents four sinusoidal
phase steps. At one stationary camera pixel, a direct return has
`I_j = A + C*cos(phi + 2*pi*j/n)`. Fourier quadrature removes constant ambient A
and positive static gain C. Unlike a spatial stripe centroid, different static
reflectance at different pixels need not shift the recovered projector coordinate.
This is an analytical escape under a direct, linear, stationary-return model,
not a calibrated PLA or camera result.

[Gupta et al.'s research project](https://www.cs.cmu.edu/~ILIM/projects/IL/lightscan/lightscanindex.html)
(accessed2026-10-14; CVPR2011/IJCV2012) reports conventional phase/Gray-code errors
under interreflection and scattering, and investigates patterns tailored to
those effects. That supports testing mixed light paths; it does not supply the
scenario amplitudes below or establish feasibility at our pitch/cost.

**Construction and explicit bounds:** use the previous D300/b8 mm geometry;
projector at y0, camera at y8. For normalized camera ray r and projector ray q,
`q-r=b/(D-z)`, hence `z=D-b/(q-r)`. Project
`phi=2*pi*(q+.01)/.02`. The .02 angular period exceeds the .005333 full S50
q-range on each fixed camera ray. Decoder branch selection uses calibrated
r and allowed travel only, never the desired height. Test three rays centered
on `r=-8/275` and offset by ±.003, five heights0/10/25/40/50,
three static gains.05/.2/1, ambient120/300DN, four/eight frames:180 cases.
All tested points fit within even a4.4-mm cap, granting known cap identity.
The forward model generates `ambient+gain*(1000+500*cos(phi+step))`, then rounds
to12-bit integer samples. No random noise, projector quantization/gamma, lens
blur, motion or spatial image segmentation is modeled. Projector pixel address,
focus, synchronization and source/receiver visibility over this finite patch
remain unconstructed; the original sheet's central-ray clearance does not
qualify the whole temporal field.

All180 unquantized direct cases reconstruct to numerical precision. Of the
quantized cases,172 return a height; eight at travel boundaries return unknown
when quantization moves them beyond the decoder's ±.1-mm numerical reserve.
That reserve is not additional mechanical travel. Maximum accepted errors are
.4952/.1751/.0355mm for gains.05/.2/1 respectively. These are finite deterministic
scenarios, not noise bounds or a claim that every accepted result meets.25mm.
Missing/flat and saturated signals return unknown. An independent four-step
atan2 identity checks the Fourier convention; exact forward re-projection
checks the ambiguity witnesses.

**New failure witness:** at a true25-mm surface, add a second transport path
carrying the projector phase corresponding to45mm on the same calibrated camera
ray, at20% of direct modulation. This labels a possible indirect contribution,
not a simulated physical wall or measured20% interreflection. Their sum is
exactly another sinusoid: phasors add. The decoder returns **28.3788mm** with
residual below5e-13DN for4,8 and16 steps. Rounded samples return28.3963/28.3906/
28.3957mm and pass the illustrative1DN residual threshold. A direct-only signal
with the resulting mean/contrast and this wrong height matches every unrounded
sample. More phase steps at the same frequency cannot distinguish these cases.
Absolute contrast is not independently known; enforcing the assumed forward
contrast would require its own material/optical calibration.

A separate exact witness holds true height25mm but varies cap-specific gain
between **.98333 and1.01667** across four frames. It reproduces the26-mm direct
signal. This is an adversarial ±1.67% drift construction, not a measured flicker
rate or statistical prior. Shared references can detect global illumination
changes, but not necessarily local motion/response changes. Spatially mixed
pixels, indirect paths and changing gain require earned limits or a different
encoding/separation method. Hidden caps still return no independent information;
a prop surface must not be accepted as the cap merely because it has valid phase.

**Whole-machine consequence:** zero new resident parts/joins/marks, but no removal
of1024/4096/6400 screw pairs or guidance, thrust, holding, anti-rotation and repair
obligations. Retain undock/settle/register/read/accept-or-unknown sequencing;
unchanged loaded neighbors are not deliberately moved. Replace one fixed sheet
source/driver with one programmable projector/controller plus camera, shared
mount/calibration and upper positioning. Optical setup is shared; it does not
repair uncertain mechanical support or guarantee later power-loss retention.

At the same explicitly unearned .1s/frame and four-cap group, four-frame
acquisition alone costs **102.4/409.6/640s** at1024/4096/6400 cells versus the
sheet's51.2/204.8/320s. Eight steps double those times without resolving the
witness. Local1/4/8 groups add.4/1.6/3.2s before all routing, writing, digital
preparation, reference checks, settling and retries. No new gameplay distribution
is claimed; E-270/E-276 schedules stay conditional. These S50 tests also contain
S40, and neither raised neutral nor initial preparation is free. Dense scan time
is separate from the~30s gameplay reference. An obstructed cap has no finite
automatic acceptance latency.

As **unsourced allocation only**, replace the earlier$30–150 sheet/driver with
$100–400 projector/control: optics total$270–980; adding the same optimistic$798
base gives$1068–1778 before integration/qualification. This is not a supplier
quote, rated projector or a full BOM. It exceeds the~$500 reference and partly
exceeds the$1000–1500 research range without proving superior play. A~$1000
finished product remains an owner-value option, not a selected price. No purchase,
light-source safety selection, physical test or additional owner print follows.

**Stop/next evidence:** park single-frequency phase-fit refinement and extra-step
sweeps. Temporal coding earns static-gain cancellation, not reliable actual-height
acceptance. A distinct useful next investigation is a constructed direct/global
separation code with an independent decoder and its complete frame budget, or
actual calibrated cap imagery. It must challenge mixed paths and occlusion,
not simply regenerate noiseless phase controls. E-281 remains the sole optional
short-thread print; the manufacturing/support campaign is not blocked on it.
