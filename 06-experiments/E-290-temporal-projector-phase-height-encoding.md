---
status: complete
builds-on: [E-289]
---

# Temporal projector phase height encoding


**Temporal coding cancels static gain, but a clean phase waveform does not
qualify height.** Run `python3 tools/curated-experiment-checks/E-290.py`.
A shared programmable projector replaces the sheet. On a stationary pixel,
`I_j=A+C*cos(phi+2*pi*j/n)` lets Fourier quadrature cancel constant ambient A
and positive gain C, avoiding spatial-centroid bias under direct linear return.
[Gupta et al.](https://www.cs.cmu.edu/~ILIM/projects/IL/lightscan/lightscanindex.html)
(accessed2026-10-14) demonstrate conventional phase errors under interreflection
and scattering; they do not source our assumed amplitudes or hardware.

Calculated geometry: D300/b8, camera ray r, projector ray q;
`q-r=b/(D-z)`, `phi=2*pi*(q+.01)/.02`. Period.02 exceeds the S50 ray interval
.005333. Decoder uses calibrated r and travel, never desired height. Test rays
`-8/275+[-.003,0,.003]`, heights0/10/25/40/50, gains.05/.2/1, ambient120/300DN,
four/eight steps:180 cases. All points fit a4.4-mm cap, granting cap identity.
Forward samples are `ambient+gain*(1000+500*cos(phi+step))`, rounded to12 bits.
No noise, gamma, projector pixels, blur, motion or image segmentation is modeled.
Finite-field source/receiver visibility is unconstructed; sheet-center clearance
is not a temporal-field pass. All180 exact controls reconstruct;172 quantized
cases decode, eight boundary cases return unknown outside a±.1-mm numerical
reserve (not extra travel). Maximum accepted errors at the three gains are
.4952/.1751/.0355mm. Flat/saturated returns are unknown. Acceptance does not assert.25-mm accuracy; atan2 independently checks phase.

**Counterexample:** a25-mm direct return plus20% modulation at the phase of45mm
on that ray decodes **28.3788mm**. Phasors sum into a perfect sinusoid at4/8/16
steps, residual<5e-13DN. Rounded results28.3963/28.3906/28.3957mm pass the1DN
residual check. A direct-only waveform with adjusted mean/contrast matches exactly. This is an
assumed transport path, not measured reflection; extra steps cannot resolve it. Separately, cap-specific
frame gains.98333–1.01667 exactly counterfeit25→26mm;±1.67% is an adversarial
bound, not observed flicker. Shared references do not necessarily remove local
response changes. Prop identity and hidden caps remain unresolved.

No resident additions or removed screw/support duties. Replace sheet/driver
with projector/controller; retain camera, shared references/mount/upper carrier
and undock/settle/register/read transaction. At assumed.1s/frame/k4, four-frame
acquisition costs102.4/409.6/640s for1024/4096/6400 cells; eight doubles it without
fixing the witness. Local1/4/8 groups add.4/1.6/3.2s. All writer/preparation/settling/retry costs remain paid; retain S40/S50, raised
neutral and E-270/E-276 conditional gameplay schedules versus~30s. These dense
scans do not qualify gameplay or obstructed caps.
Unsourced projector/control$100–400 replacing sheet$30–150 makes optics$270–980,
base-plus-optics$1068–1778 before integration/qualification, versus~$500 reference
and$1000–1500 research range. No BOM, source-safety selection, purchase or print.

## Spatial separation extension

**Numerical construction, not captured imagery:** multiply each of four temporal
phase patterns by a binary spatial carrier at four quarter-period shifts. For
each phase take maximum minus minimum across the shifts, then decode those four
differences. [Nayar et al., 2006](https://www.cs.columbia.edu/cg/pdfs/1156189195-Krishnan_TOG06.pdf)
(accessed2026-10-14) derive direct/global separation under sufficiently smooth
global transport; finite projector/camera optics require additional images in
their demonstration. That source does not establish our carrier resolution,
material transport or frame rate.

The same executable now includes30 exact limiting controls (five heights, three
gains, with/without shift-invariant global return). All recover height. A finite
nonnegative Gaussian transport lobe centered on the45-mm ray, width.0008 ray units,
truncated at±.003 and total weight.2, reads25.0065/25.0001mm at2048/4096 midpoint
samples. Quadrature change.00635mm is numerical sensitivity, not optical accuracy.
No material distribution or probability of broad transport is asserted.

**Full raw-data counterexample:** a localized20% path at the45-mm projector ray
and direct25-mm path share the carrier code when its period is their ray
separation/6. With carrier origin offset.13 periods, the falsely inferred28.3788-mm
ray shares that code too. A direct-only return at that false height with fitted
mean/contrast reproduces **all16 samples within1.4e-12DN**, not merely their
max/min or sinusoidal residual. Rounded separation reads28.3963mm. This is a
constructed nonnegative transport witness and unknown-local-contrast scenario,
not a measured PLA reflection or a universal impossibility proof. It shows why
retaining this four-mask address code alone does not certify direct light.

Carrier period.00038027 corresponds to.1046mm at the25-mm plane (half-stripe
.0523mm). Finite projector resolution, defocus and camera footprint are omitted:
even this idealized sharp pattern fails the localized witness. No extra resident
parts; same shared projector/camera and allocated$1068–1778 base-plus-optics
remain, without a verified specification/BOM. More capable optics could cost more.
At the inherited assumed.1s/frame and four caps/group,16-frame acquisition alone
costs409.6/1638.4/2560s at1024/4096/6400 cells (12.7/6.35/5.08-mm pitch controls).
Local1/4/8 groups cost1.6/6.4/12.8s before writer motion, registration, settling
and retries. Retain S40/S50, minimum versus raised neutral, paid preparation,
~30-s gameplay and separate dense benchmarks; these sensing times select no
playable pitch or end-to-end update. Hidden caps still return unknown.

**Decision:** retain spatial separation only as a conditional broad-transport
control. Stop periodic-mask/phase-count tuning without earned transport and
resolution evidence. Reopening needs calibrated cap imagery or a materially
different path discriminator with a full frame/visibility budget. Static-gain
cancellation is useful; height acceptance and mechanical holding remain
unqualified. No new print or purchase; E-281 stays the sole optional print.
