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

**Stop:** park single-frequency fit/extra-step sweeps. Reopen through constructed
direct/global separation with a full frame budget or calibrated cap imagery.
Static-gain cancellation is useful; actual-height acceptance, visibility and
mechanical holding remain unqualified. E-281 stays the sole optional print.
