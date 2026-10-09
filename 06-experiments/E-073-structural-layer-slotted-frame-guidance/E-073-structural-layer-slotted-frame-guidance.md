---
status: complete
builds-on: [E-072, E-070, E-069, A-022]
---

# Stationary slotted guidance trades tilt amplification for bending

**Retire this captured-T structural-layer embodiment under the retained bounds.**
The stationary split guide has a connected, collision-free prescribed path, but
clearance alone still permits fork collision. Even granting perfect datum bias
and fixed guide-end rotations, its long unsupported carriage fails the lateral
stiffness screen at the upper end of the retained side-load scenario. This closes
the bounded A-022 access/guide campaign with no supported machine survivor; it
does not disprove binary structural memory or every shared-frame implementation.

Input main `8ae6d06`. Run
`python3 tools/curated-experiment-checks/E-073/slotted_frame.py`.
Standard-library constructive boxes, exact straight sweeps, and a piecewise
Euler–Bernoulli beam calculation; units mm/N. No sourced process prior, random
sampling, physical measurement, finite-element solution or qualified CAD.

## Changed topology and finite motion

Replace E-070's carriage-local guide with two stationary captured-T stations
straddling the entire absolute dog/bore travel. A left jamb connects the stations
outside the bore sweep; the remaining guide walls have a through-slot. Extend
the moving neck and add separate upper/lower T flanges, joined by that neck.
Each fixed station retains its matching flange through the full motion interval.
The dog bore cannot be crossed by an uninterrupted flange.

The ground latch must remain relative to the lower stage: a stationary tongue
would stop lower-layer motion. Retain a **co-moving tongue carrier**, shortened
to the existing forward lane. The old rear-reaching carrier intersects the new
stationary jamb; the executable preserves this negative control. Carrier-to-lower-
stage attachments and stacked output connectors are not constructed. Connection
within each carriage/frame/carrier is checked by finite face or volume adjacency,
not by edge contact.

Use the required five-height workload 0/10/20/30/40 mm, E-067's normalization
schedule, and E-069's failed-proof/overtravel bounds. Lower offsets are 0;
0/10; and 0/10/20/30 mm for successive stages. Maximum absolute carriage motions
are 10/30/40 mm, **not 10/30/70**: 70 mm is an unused binary code. Continuous
motion envelopes cover all valid offsets and transitions, including conservative
extra overtravel at their endpoints. Active-layer lower offsets are zero.

| Stage stroke | Absolute interval | Slot height | Moving carriage length | Swept height |
|---|---|---:|---:|---:|
| 10 mm | −0.25…10.40 mm | 13.45 mm | 33.50 mm | 44.15 mm |
| 20 mm | −0.45…30.60 mm | 33.85 mm | 73.30 mm | 104.35 mm |
| 40 mm | −0.65…40.80 mm | 44.25 mm | 95.10 mm | 136.55 mm |

Table stations are 4 mm tall. All three centered paths fit 5.00 × 4.95 mm
including the existing 0.15-mm relative-error reserve; adjacent identical
channels have sufficient axis separation under this allocation. Exact sweeps
check carriage/frame, dog/frame, fork/frame, carrier/frame, carrier/carriage,
parked tongue, carrier/fork and arbitrary parked-carriage bypass. Guidance
coverage is an affine interval containment check at both endpoints. Station
heights 1.6/4/7.137 mm and an off-grid additional slot gap of 0.037 mm also
pass these **prescribed-path checks**. These 18 cases are parameter holdouts
within one changed topology, not 18 architectures or manufactured yield samples.

Separating the three swept envelopes vertically would consume **285.05 mm**
before interstage connectors, top surface and shared frame. This is an accounting
reference, not a proven stack minimum or a stage-02 height rejection. Count
38,400 guide stations, 19,200 moving carriages/dogs/latches, and their selector/
proof interfaces across 6,400 cells. Sharing a stationary frame removes neither
independent channels nor these repeated contacts.

## Manufacturing correlation and ideal-datum counterfactual

The previous clearance-only counterexample remains admissible: a +0.19-mm
carriage shift stays clear of both guide stations, while an independent −0.15-mm
rail registration error produces finite bore-floor/lower-fork and bore-roof/
upper-fork intersections. Both errors can affect a whole bank. The first is
mechanical free play, not an additional manufacturing draw. The second consumes
the existing aggregate relative-error allocation. A common translation of frame,
carriage and rail cancels. Accounting for nominal guide play still requires
5.40 mm width for this section, above pitch.

A positive datum has one new benefit here: the dog housing remains **between**
the two fixed datum stations. In the rigid affine model, lateral error there is
`(1−t)e_lower + t e_upper`, 0≤t≤1, so opposing pad errors ±a do not amplify
beyond a. Adding opposing rail registration e−a remains bounded by e=0.15 mm.
This is a necessary ideal-restraint bound, not generated bias hardware, finite
contact-pressure proof, or a bound on bowing, guide deformation and pad wear.
It avoids E-072's stroke extrapolation but leaves only 0.20−0.15=0.05 mm lateral
bypass margin. No additional error expansion is applied in the next calculation.

## Stiffness screen of the actual section

The frame slot removes intermediate lateral support. At the centered housing
position, compute the union of the generated carriage cross-sections, including
its stronger bore walls and weaker T flange/neck. Integrate rectangle areas and
second moments exactly; the weakest section has `I_y=0.2457 mm^4`. Overlapping
neck/flange material is counted once. A uniform thin-neck surrogate would miss
the actual section changes.

Use a fixed-fixed linear beam between the **inner edges** of the stationary
stations, lateral force H at the dog center. This grants perfect bias, zero
end translation/rotation, rigid frame and instantaneous elastic material. It
omits shear, axial compression/eccentric thrust, creep, section-transition
warping, interface compliance and dynamics. It is a favorable reduced model,
not a rigorous lower bound for every possible 3-D reinforcement. Slot geometry
and all generated section changes enter the calculation. The assumed elastic
modulus **1,000–4,000 MPa is an exploratory bound, not a claimed PLA/X1C prior**;
H=0…0.2 N carries forward E-071's side-force scenario, not a product load mandate.

For unit load at a, solve `M(x)=m+r x+max(0,x−a)` using zero end rotation and
displacement: `integral M/I dx = integral x M/I dx = 0`. Integrate curvature
piecewise to obtain wall displacement. Simpson integration is exact on each
polynomial interval, splitting at section changes and the point load. The
strain-energy result independently matches displacement at the force point.

| Stage | Wall displacement at H=0.2 N, E=4,000 MPa | H reaching 0.05 mm | E needed for 0.05 mm at 0.2 N |
|---|---:|---:|---:|
| 10 mm | 0.00158 mm | 6.35 N | 126 MPa |
| 20 mm | 0.0340 mm | 0.294 N | 2,721 MPa |
| 40 mm | **0.0793 mm** | **0.126 N** | **6,347 MPa** |

Reported values use the larger bore-floor/roof midpoint displacement, not only
the dog center. The upper stage exceeds its 0.05-mm budget even at the stiff end
of this modulus bound; at E=1,000 MPa the same force gives 0.317 mm and the
force threshold falls to 0.0315 N. These are linear-model screening thresholds,
not allowable loads or probabilities. Modeling rail contact could prevent
further deflection by interference, which fails the required free bypass.
Smaller side load changes the result; zero side load does not prove a machine.
The 20-mm case is sensitive to material/boundary conditions. Neither is given a
hardware pass. No further physical or nonlinear fidelity is economical until
a substantially stiffer/support-isolated path is proposed.

## Disposition and verification

Stop this implementation's geometry refinement, stacked qualification, selector
BOM development and print preparation. No complete cost, <30-s update, service
load, durability or repairability claim is available; those cannot outrank the
failed guidance gate. Existing E-067 timing and E-069 support guards remain
conditional submodels, not cumulative machine acceptance. A new topology may
reopen with a packed near-drive reaction path, a changed section/rail geometry,
or credible combined error/force evidence below the computed boundary. A finer
grid, ideal preload alone, or a renamed long guide does not reopen it.

Self-review checks preserved E-070 failures, connected solids, continuous
interval guidance, off-grid geometry, common-shift cancellation, restored-slot
collisions, and the old carrier/jamb collision. Beam checks reconstruct the
independent uniform fixed-fixed closed form at central/off-center loads,
energy/work equality, force/modulus scaling and zero end displacement. This is
self-review, not independent physical evidence. Reproducible output is omitted.
