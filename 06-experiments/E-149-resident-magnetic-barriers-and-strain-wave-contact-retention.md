---
status: complete
builds-on: [E-148, E-138, E-131, E-135, A-007, A-016]
---

# Resident retention: magnetic wells are not arrest; phased friction keeps contact

**Stop the tested spherical-magnet track and synchronized intermittent friction
feet. Keep opposed-phase resident friction only as a conditional load-path lead.**
Magnetic wells hold light rest states but do not guarantee capture from arbitrary
writing phase/energy. Opposed friction contacts avoid a simultaneous gap, without
establishing an actuator, residual-vibration arrest, affordable replication or
local isolation. The screw control retains friction/speed/routing failures.
No machine, printing or purchase selected; no whole physical principle rejected.

Input main `2282b42`; LAB-249. Reproduce with Python + NumPy:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-149/retention.py`.
JSON is disposable. Evidence: sourced principles, fixed-magnetization field
calculation, conservative board bounds, generated runner/contact envelopes,
prescribed-ellipse Coulomb quadrature and analytical limits. Self-review only;
no solved elastic wave, assembly CAD, calibrated manufacturing prior, validated
contact dynamics, physical measurement or yield. Loads 0/.02/1/10 N and masses
below are scenarios, not new product requirements.

## Causal combinations and novelty

| Combination | Selection/energy | Resident load path |
|---|---|---|
| Magnetic track | Spatial PM writer follows rider; carriage supplies signed work | Column magnet → fixed track → frame; guide reacts side force/torque |
| Strain-wave friction | Shared piezo head docks to two resident feet/rail terminals; phased motion drives runner | Two preloaded wear contacts → grounded feet/frame |
| Screw control | Spatial spindle rotates resident screw | Nut/thread/thrust frame, conditional on friction |

All need actual height and loaded hold proof, not shaft/current readback. Wave
proof follows decay. Mismatch inhibits withdrawal; retain head and permit one
supported correction after independent cut. Magnetic escape needs supported
reacquisition; cutting a backdriving screw does not restore hold.

A-016 stores commands and E-138 transmits rack torque to separate supports;
here the field stores height and carries load. E-135/M-010 deliver commands;
here waves transport through the retaining friction contacts. These are functional
recombinations; A-007/E-131 are controls. No new A/M object or saturation claim.
Three search axes—magnetic energy, ultrasonic contact mechanics, opposed contact
phasing—yielded the latter discriminator, not a newly invented motor principle.

Sources (2026-10-11): [Fitzpatrick](https://farside.ph.utexas.edu/teaching/jk1/Electromagnetism/node61.html)
and [McDonald](https://kirkmcd.princeton.edu/examples/twomagspheres.pdf) supply the
prescribed-M sphere field/force method. [Sob’yanin](https://arxiv.org/abs/2501.01978)
challenges extension to responding materials: fixed M/no induced response here
is not an exact-real-magnet claim. [Zhu 2004](https://pubmed.ncbi.nlm.nih.gov/15244280/)
treats ultrasonic contact layers/preload; [PI U-521](https://www.physikinstrumente.com/en/about/news-press/news-detailpage/compact-linear-stage-with-ultrasonic-piezomotor)
describes unpowered friction retention in a 35×35×15-mm, 18-mm-travel stage.
No stage performance, price or packaging transfers to this mechanism.

## Finite magnetic track and full-board bound

Geometry: radius-1-mm rider, 13 equal fixed spheres at `(-(2 mm+g),0,4j mm)`,
j=−1…11; rider x=y=0, z=0…40 mm. Moments are fixed parallel to x. Mounts carry
torque/side attraction. Nonintersection is checked. Four-mm detents are a scenario;
extended rails do not remove loaded height offsets. End-stop shock is unbuilt.

Stipulate `mu0*M=1.2 T`, common scale .9/1/1.1; this is not predicted internal B.
For `m=4*pi*r³*M/3`, `C=mu0*m²/(4*pi)`, R²=x²+y²+z²:
`U=C*(R^-3−3*x²*R^-5)`,
`Fz=−dU/dz=C*(3*z*R^-5−15*x²*z*R^-7)`.
Sum the 13 finite sources. Dipole equivalence applies to the prescribed-M spheres,
not arbitrary shapes. Material response, temperature and orientation are unmodeled.

| Gap, mm | Isolated peak axial force, nominal M | Common-M .9…1.1 envelope |
|---:|---:|---:|
| .3 | .14482 N | .11731… .17524 N |
| .5 | .09856 N | .07984… .11926 N |
| 1 | .03934 N | .03187… .04761 N |

Each case has ten stable equilibria inside 0…40 mm at .02 N, none at 1 N.
The lowest loaded well is below zero; no endpoint pass. Signed axial force,
not magnetic pressure, determines raising/lowering work and energy absorption.

Nominal well z=20 mm and crest z=21.99992 mm differ by **.123112 mJ**. A .02-kg
moving mass at .110956 m/s has that energy. More decisively, start at the crest
at .1 m/s, zero applied load, no dissipation: total energy exceeds every potential
value from 2 to 38 mm by **>.0952 mJ**, including between-sample allowance.
No turning point exists there; motion crosses successive wells. This is an energy
witness, not a transient simulation. Near a crest the forward barrier can vanish.
A damping/capture device must be counted. Coil-writer outage leaves resident
wells but does not remove kinetic energy; PM-writer outage also leaves its coupling
and potentially free carriage. Energized wrong commands remain indistinguishable
from valid force application.

An isolated radius-1.5-mm writer at x=+3 mm gives peak force **.182854 N**;
even ideal head-height choice allows only **.084290 N** worst-phase bidirectional
load after opposing the track. This is a ceiling, not a trajectory. Direct writer
and resident-rider fields on the y-adjacent cell peak at .000844/.002063 N;
these pair values do not guarantee cumulative isolation.

Replicate 80×80 at 5.08-mm pitch, indices −40…39 about an interior cell. The
neighbor's fixed track is only 2.58 mm from the nominal rider. Resolve all tracks
in a 7×7 neighborhood over height; bound the remaining fixed sources and all
other riders at arbitrary heights using `|Fz|≤18*C/rho⁴`, lateral separation rho.
Height samples are ≤1.25 µm away; `|dFz/dz|≤153*C/rho⁵` bounds interpolation.
At nominal g/M, near-track peak .184228 + far .118306 + interpolation .079072
+ arbitrary-rider .260561 gives **.642167 N upper bound**. Nine coherent gap/M
scenarios give **.52016… .92839 N**, below 1 N even with favorable neighbors.
This rejects support of the central 1-N cell in those fixed-M cases. Discrete
scenarios do not bound every intermediate manufacturing or constitutive error.

The favorable writer **collides with the adjacent track**: centers .42 mm apart
versus 2.5-mm summed radii, clearance **−2.08 mm** at equal height. The 2-mm axial
clear gap between track spheres cannot pass a 3-mm writer. Tiers/other approaches,
steel returns or changed magnet media need new geometry/fields. This embodiment
fails packing independently of force and coast capture.

## Friction contact continuity, energy and interruption

Finite envelope: 2-mm-wide runner spans z=q−42…q+2 mm for q=0…40 mm; two fixed
opposed shoes each have 1-mm axial extent and assumed 1-mm² area. Including ±1-µm
tangential motion, minimum end land is **1.499 mm**. Remaining lateral pitch
3.08 mm is unallocated, not a fit proof for feet, springs, guides and couplers.

Prescribe `delta_i=N0/k+(Na/k)*cos(theta+phi_i)`,
`N_i=k*max(delta_i,0)`, `u_i=s*U*cos(theta+phi_i)`,
`f_i=mu*N_i*sign(u_i−v)`. s=±1 reverses drive; U=omega*b.
This is compliant-layer indentation, not rigid penetration. Set k=60 MN/m,
N0=60 N/foot, b=1 µm, f=40 kHz: U=.251327 m/s. Na/N0=.5/1.5 gives normal
amplitude .5/1.5 µm and off compression 1 µm. **No elastic/head solver establishes
these motions.** Guides react unequal normal forces; their compliance/drag is omitted.
Peak contact stress is **150 MPa** at Na=90 N on 1 mm²; no PLA contact/flexure is
qualified. A larger pad changes packing, stiffness and wave loading.

| Contact state, mu=.1 | Min. total normal | Contact duty | Mean stall traction | Stall contact heat |
|---|---:|---:|---:|---:|
| Same phase, Na/N0=.5 | 60 N | 100% | 3.820 N | 1.920 W |
| Opposed phase, Na/N0=.5 | 120 N | 100% | 3.820 N | 1.920 W |
| Same phase, Na/N0=1.5 | 0 N | 73.22% | 10.401 N | 2.168 W |
| Opposed phase, Na/N0=1.5 | 120 N | 100% | 10.401 N | 2.168 W |

Synchronized high-modulation feet lose all frictional ground contact for **26.78%**
of a cycle; one-foot failure in the opposed pair has the same gap. Opposed phases
remove that simultaneous gap while preserving mean drive. Instantaneous axial
traction still varies through zero: no rigid instantaneous hold follows. For
Na≤N0, independent integration gives mean stall `4*mu*Na/pi`. Finite-speed
quadrature satisfies `Pdriver=Fmean*v+Q`, Q≥0, and signed reversal symmetry.
Tangential stick/compliance, runner inertia ripple and wave loading can change the
mean force-speed curves. Lowering may require driver energy absorption.

24 cases cross N0=20/60 N, Na/N0=.5/1.5, mu=.02/.1/.3 and contact phase.
Twelve coherent preload .8/1.2, drive .8/1.2 and relative-phase −.2/0/+.2-rad
cases give opposed minimum normal **74.44…144 N**, mean stall **8.321…12.481 N**,
off capacity at mu=.1 **9.6…14.4 N**. Common weak preload loses 10-N hold.
These are bounded scenarios, not distributions or yield.

After vibration is actually absent, capacity `C=2*mu_k*N0`. For m=1.1 kg,
downward .1 m/s, W=10 N, mu_k=.1: C=12 N and first-stop distance **2.75 mm**;
at zero load, **.4583 mm**. With mu_k=.02, C=2.4 N cannot arrest the 10-N
lowering load even if static mu_s=.1 held it. Upward motion can stop then reverse;
first stop is not retention. Static hold needs its own coefficient bound.
These grant instantaneous wave removal and are generalized mass/load scenarios.

Assumed entrainment at U*exp(−t/tau) integrates to .251/2.513/25.133 mm for
tau=1/10/100 ms: **not predicted displacement or a loaded-coast bound**.
Ringdown remains missing. Energized stall heats; wrong sustained excitation can
drive. Independent cut, stored-energy discharge and actual observation count;
supply loss does not prove excitation loss or authenticate commands.

The prescribed sliding limit gives directed zero-load neighbor traction even for
small correlated normal/tangential vibration. Real stick may create an unmodeled
deadband. Head-local excitation needs actual resident-foot/frame isolation;
E-135's loaded coupling and repeated-exposure limits remain.

## Full-display accounting and next decision

Retain 6,400 columns/guides, 5.08-mm tops and 40-mm travel. Magnetic route adds
**89,600 magnets**, oriented retainers/tracks plus H writers. Iron/patterned stock
requires new field/manufacturing models. Wave route adds **12,800 wear contacts**,
two preload paths/cell, grounded feet and couplers; H heads add piezo parts,
phase drivers, matching electronics, cables, docking, readers and independent
abort. Local piezo forfeits shared-head cost. Summed preload **768 kN** closes
mostly locally, not as net board load; frames still carry local force/creep.
Screws repeat nuts, screws, supports, antirotation and docks.

With $250 hypothetical shared frame/power/control/reader reserve,
`6400*c_cell+H*c_head<$250` is needed for <$500 purchases; <$400 leaves $150,
<$200 is already missed. Free heads allow **$.03906/cell**, **$.002790/magnet**
or <$.01953/contact-preload module before other local parts. These are ceilings,
not quotes/BOM passes. Assembly at 10–30 s/site is 17.8–53.3 h before preload,
orientation/inspection; accessible repair, print material/time/scrap, resonator
manufacture and lifetime remain additional burdens.

Optimistic `T=6+ceil(6400/H)*(.04/v+.05)` includes .05 s/site for acquisition,
local read/proof and withdrawal, and 6 s for map preparation, registration,
shared travel, final proof, one supported retry and settling. Neither allocation
is earned; arbitrary old heights, returns and actual paths can worsen it.
At v=.025/.05/.1/.2 m/s, strict <30 s needs **458/229/121/68 heads**, allowing
<$0.546/1.092/2.066/3.677 per complete head if cell parts are free.

Surface speed U is not travel speed. The nominal opposed sliding surrogate at
10 N gives only **.0125–.0127 m/s** raising (4,096/16,384 phase samples): **915
heads**, about 2.04 W contact heat/head or **1.87 kW** for simultaneous operation,
before driver/transducer losses. At 1 N it gives ~.178 m/s and 74 heads. Ranking
is load/friction-sensitive; these are reduced-model points, not hardware predictions.
Reverse-wave lowering at 10 N gives ~−.248 m/s and **−1.25 W/head** at the contact
driver, requiring an energy sink. Useful all-raising work is independently 256F J.

Square-thread control, d=3 mm and zero-margin lead pi*d*mu: **212.2/84.88/42.44
turns** for mu=.02/.05/.1. With 160 heads and <.55 s rotation/site, this requires
**>23,150/9,260/4,630 rpm** before acceleration. Kinetic friction, zero-load input
inertia and wider internal routing retain E-131/A-007's failures.

No X1C prior is claimed. Common gap/M/preload/drive/phase were propagated;
hole shrinkage, wall bias, layers/first layers, warp and alignment can overwhelm
micron compression. Count adjustment or purchased contact structures. Roughness,
contamination/wear affect friction; PLA anisotropy, creep, fatigue and interlayer
weakness affect frames/returns. No accuracy, yield or lifetime is qualified.
Assumed false-accept p=1e−4 gives .64 expected misses/6,400 observations without
independence, not demonstrated reliability. Common bias defeats retries.
Unchanged-region disturbance remains unqualified; no numerical limit invented.

**Decision:** retire this spherical track/writer, synchronized high-modulation feet
and magnetic-wells-alone arrest claim. Retain opposed friction conditionally, with
screw and E-148 field-jaw controls. No magnet/motor fabrication refinement.
Reopen magnetic retention only with changed flux/packing and explicit energy
capture, not stronger unsupported fields.

**Next:** small load-dependent elastic/contact model of shared-writer excitation
of opposed resident feet. Compare coupled resonator/tangential stick with ideal
ellipses and permanent-preload direct sliding. Test signed transport, post-cut
arrest and adjacent loaded/unloaded runners; count coupling, ringdown, correlated
preload/phase, friction, hard contacts and joint time/cost. Stop on per-cell powered
drivers, hidden capture brake, unsupported micron preload, or repeated known
failure without a changed mechanism. This probe precedes printing/waveform tuning;
CTO owns execution, with no approval wait.

Self-review: force/energy derivative error <1.8e−11 N; peak changes <1e−7 N from
16,001→64,001 height samples; work error <4.1e−13 J. Board/coast bounds include
analytic interpolation allowances. Contact mean matches independent 4*mu*Na/pi
within 2.4e−8 N at 16,384 phases; reversal/power balance and generated overlap/gaps
checked. These verify prescribed models, not constitutive laws, actual waves,
transient arrest, hardware or independent qualification.
