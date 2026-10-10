---
status: complete
builds-on: [E-130, E-129, E-100, A-007, E-126]
---

# Grounded sliding support trades release gaps for travel and friction dependence

**Retain continuously engaged sliding support as a distinct conditional load path;
stop the long solid-wedge implementation. Counterbalance alone is not retention.**
The wedge below supports raising and forced lowering without releasing its
load-bearing contacts, escaping E-130's missing static arrest under explicit
friction bounds. Travel, replication and kinetic-friction counterexamples prevent
machine admission. Interlocking bands change stored structure but do not by
themselves close input arrest. No architecture is selected.

Input main `679617b`. Reproduce with Python standard library:

```
python3 tools/curated-experiment-checks/E-131/grounded.py
```

Evidence: sourced principles, analytical bounds and a finite rigid prism/shoe
construction; no assembly CAD, validated dynamics, measurements or independent
review. Loads, friction, errors and speeds are **engineering scenarios**, not
product requirements or X1C priors. This is a bounded screen.

## Causal combinations and novelty

| Combination | Selection, energy, retention and ground load | Verification/recovery |
|---|---|---|
| Translating wedge | Bilateral travelling heads dock to local wedge ends. Each column rides a sliding shoe; wedge rests on a fixed bed. Displacement stores height; load-generated friction holds without brake release. | Read actual top; proof stationary hold before undocking. Low friction defeats recovery. |
| Counterbalanced head | Capture output before releasing its ground stop. A ground-anchored constant-force strip spring assists the head; return load to the stop after motion. | Read top and supported stop before releasing capture. Spring alone leaves residual force; add explicit permanent drag or stop. |
| Helical bands | Dock rotary writer to assembly rotor; two stored bands form a guided compression column. Rotor/rollers/base carry load during reversal. | Read top and band engagement; isolate jammed cartridge. Rotor arrest remains missing. |
| Screw A-007 | Spindle turns grounded thrust-supported screw; antirotating nut lifts top. Sliding threads retain height conditionally. | Read actual top; input-loss behavior depends on friction/lead. Prior rejection retained. |
| Direct head E-129 | Positive drive moves output; two continuously contacting spring-loaded pads react to ground. Cell stop holds after handback. | Verify supported stop seating and top. Preload, wear, kinetic arrest and capture remain unresolved. |

Three varied searches: machine-leveling wedges (continuous ground contact),
constant-effort supports (energy cancellation), and stage-lift bands (assembled
compression structure). E-078 uses short selector ramps; E-100 already has this
raising equation for 2.5-mm rail lift, but no loaded-lowering retention construction.
The 40-mm memory wedge is recombination, not a new wedge principle. A-007 covers
screws, A-021 planar multistable stacks, M-009/E-120 tendons. Bands change inventory,
not arrest. No search-saturation claim.

Primary sources, accessed 2026-10-10:

- [NPTEL Mechanics, lesson 16, PDF pp.1–3](https://archive.nptel.ac.in/content/storage2/courses/112105164/lec16.pdf): wedge push/pull force diagrams and self-locking. PDF p.3 inconsistently follows `2φ>α` with `α<atan μ`; use the preceding force equations and independently resolved vectors, not that sentence.
- [Lee Spring, Constant Force, Constant Load](https://www.leespring.it/en/constant-force-constant-load?language_content_entity=en): strip springs supply near-constant load; stated stock fatigue lives span 2,500–25,000 cycles depending on size/load. This is not a selected part, lifetime prediction or PLA spring prior.
- [PACO Spiralift DC053, March 2019, PDF pp.1–2](https://www.pacospiralift.com/wp-content/uploads/2017/11/Brochure_Product-EN.pdf): two bands form the column; cam rollers lift through rotor motion. The ND6 optional permanent brake distinguishes column interlock from drive arrest; it does **not** establish that every variant backdrives. Industrial performance is not transferred here.
- [Roton screw backdriving explanation](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/): self-locking requires positive driving torque even to lower. This supports the continuous sliding comparison, not a qualified small printed thread.

## Finite grounded wedge and loaded reversal

Use mm and N. Wedge local coordinates are `u=x−q∈[−530.4,1.4]`,
`y∈[−1.5,1.5]`, bottom `z=0`, top `z=1−t*u`, nominal slope `t=.08`.
A vertically guided shoe spans `x∈[−1.2,1.2]`; its underside is
`z=1+t*q−t*x` and upper face `z=2.5+t*q`. A stem carries a 4.8-mm square
top; a neighbor lies 5.08 mm away in y. Translate q from 0 to 500 mm and back:
shoe travel is **40 mm**, with coincident inclined faces in both directions and
positive thickness. The ideal vertical guide supplies moment reaction; its actual
bearings/housing are unbuilt. With centered shoe resultant and bilateral input at
z=.4 mm, the bed center of pressure stays inside the base at both travel endpoints,
in raising, lowering and input-absent states, across all friction/dimension corners.
Its affine q dependence bounds the interior. The extended base prevents tipping
without tensile bed reaction or a free bed couple. Input fits below the thin-end
surface, but its dock is unbuilt. Weight and added friction are omitted from sizing.

At 64/256/1024 intervals, including common slope `.0798/.08/.0802` and height
bias ±.05 mm, input travel `40/t` retains at least **.20-mm end land** and
**1.40376-mm shoe thickness**. Affine endpoint inequalities also bound intermediate
coverage; refinement is a consistency check. Reversal follows the same surfaces,
without a free lift, clutch, latch closure, preload, return spring or frozen input.
Positive W supplies follower contact; zero/upward effective load, sticking guides
and shock need captive guidance and are outside this downward-load section.

Parallel y lanes retain **2.08-mm prism clearance**, **1.08 mm** between assumed
4-mm guide envelopes and **.28-mm top gap**, regardless of their different heights.
This checks geometric separation, not bed deformation or vibration. Inline x
replication fails: all 80 zero-position prisms share **130.48 mm** of x overlap
and positive z thickness. Simple independent vertical layers at maximum envelope
height consume **3,474.56 mm** before beds, routing and guides. Stage 02 permits
other routing, but none is constructed here. Literal solid prisms total **226.27 L**
of printed volume; hollow/trussed ramps change the support calculation. A
531.8-mm ramp also needs modular construction for the 256-mm build volume.
These are disadvantages, not new hard depth/material limits.

With frictionless vertical guidance, top/bed Coulomb coefficients μt/μb and
negligible wedge weight, exact horizontal force requirements are:

```
P_raise/W = (t+μt)/(1−μt*t) + μb
P_pull_lower/W = (μt−t)/(1+μt*t) + μb
```

Positive `P_pull_lower` means forced extraction is needed: input removal at rest
cannot spontaneously withdraw the wedge within those contact cones. No released
unsupported interval like E-129 is needed. Negative means an overhauling load
requires input restraint. Wedge weight adds bed friction, helping hold but raising
both driving forces. At t=.08, μt=μb=.05, factors are **.180522 / .020120**;
raising work is **2.25653 W·40 mm** before other losses. Across 81 deterministic
combinations of W={1,3.27,10}, μt/μb={.05,.1,.3}, and the three common slopes,
raising requires **.18032–6.89573 N**, lowering **.01992–5.15052 N**.
These are scenario ranges, not force percentiles.

Equal-coefficient static hold requires `t≤2μ/(1−μ²)`. Zero-margin full-travel
input lengths at μ={.02,.05,.1,.3} are **999.6/399/198/60.67 mm**. Friction
choice therefore materially changes packaging ranking. At μ=.05 the .08 slope
has margin, but a local +1.5° slope perturbation makes the lowering factor
**−.006110**. Average dimensional bias cannot bound local layer stairs, warp,
roughness or worn joints. At sliding coefficients .02, the nominal lowering factor
is **−.039904**: even bed friction from a .04-kg wedge leaves negative force at
W=1 N. Static hold at .05 therefore does not establish arrest after input removal
during motion. No stopping-distance or allowed-drop criterion is invented;
acceleration/contact dynamics remain open.

The box is ±.10-mm differential rise over 500 mm and ±.05-mm datum error, not
print accuracy. Independent registration, hole shrinkage, first layers, joints,
roughness, warp and elastic distortion remain unmodeled. Common friction/bias,
wear, PLA creep, anisotropy and batch correlations can move a whole bank outside
these bounds. No manufactured yield, lifetime or board failure probability follows.

## Counterbalance reduces force but does not remember position

For W∈[1,10] N and constant upward force C, residual support required is
`max(|1−C|,|10−C|)`: minimax **4.5 N at C=5.5 N**. With multiplicative common
spring-force error ±e, balancing adverse endpoints still gives C=5.5; residual is
**4.5+5.5e N**, or **5.05/5.6 N** at e=.1/.2. One payload's balance cannot hold
another; even exact equality is neutral balance, not restoration after disturbance.
A paired falling cell cannot support arbitrary all-raising maps, and borrowing
an unchanged cell violates local isolation.

Counterweights need .561 kg/head, **3,588 kg** if repeated per cell. Reusable-head
springs avoid that inventory but need anchors, coils, travel, fatigue and handover.
Retuning adds sensing/actuation and cannot anticipate later payload changes. W
includes follower bias; no free return force is credited.

Recombine with E-129's two permanent pads, each nominally preloaded 100 N. With
20% common preload loss, capacity is **8 N** at μ=.05: insufficient for the
original 10-N load but above the **5.6-N** counterbalanced residual. Worst drive
magnitude is bounded by drag plus residual, 13.6 N at that corner. At μ=.1 drag
is 16 N and dissipation at 300 mm/s is **4.8 W/head**, **768 W** for 160 moving
heads. At kinetic μ=.02 drag is only **3.2 N**, below residual. The combined head
is neither reliable nor thermally solved. This new conditional margin does not
repair E-125 capture, E-127 dock fit or E-128 replication.

## Full-display bounds and disposition

For all 6,400 cells changing by 40 mm, assume independent channels, v=300 mm/s,
a=3,000 mm/s², .05 s/site for docking/proof/release, and 6 s/map for preparation,
registration, remaining transport, final verification, settling and bounded retry.
These are **unvalidated optimistic allocations**, not measured times. Rest-to-rest
time is `d/v+v/a` for these distances. At 160 channels, wedge time is **78.67 s**,
direct travel **17.33 s**. Strict <30 s in this model needs at least **493 wedge
channels** or **77 direct channels**. Additional head reset/reader/retry work adds
time. With $250 shared reserve and $500 ceiling, even granting free local parts,
this leaves **$0.507/head** for the wedge versus **$3.247/head** for direct control.
These are allocation ceilings, not actuator prices or a passed BOM. At $400/$500
with that reserve, all permanent bought parts share **$0.02344/$0.03906 per cell**.

The screw folds sliding travel into rotation. A favorable square thread at μ=.05
has zero-margin maximum lead `π*d*μ`: .4712 mm at d=3 mm, **84.88 turns** over
40 mm. At 160 channels, the same overhead leaves <.55 s rotation/site, demanding
**>9,260 rpm** before acceleration. A 12-mm internal diameter changes this to
**>2,315 rpm**; top pitch does not forbid it, but 6,400 wider nuts, offsets and
strokes need actual multilayer routing. No critical-speed, heat, geometry or cost
pass, and no basis for reversing A-007's disposition.

Repetition: 6,400 wedge/shoe/bed/guide sets, or ≥12,800 bands plus magazines,
interlocks/formers/arrests, or 6,400 screw/nut/thrust/dock sets. Counterbalanced
heads retain cell stops plus head coils/anchors and two preloaded pads each.
Printing does not erase wear/assembly. False acceptance or common sensor bias
can release unsupported outputs; neither error probability nor power-loss recovery
is qualified. Unchanged outputs keep local support; frame compliance couples them.

**Decision:** stop monolithic long-wedge detailing, pure-balance retention and
band-as-arrest claims. Preserve sliding friction's continuous lowering path and
the bounded counterbalanced-drag margin as comparison evidence. Do not tune E-130
pockets or E-129 release pegs. No printing, purchase or full-machine optimization.

**Next discriminator:** put continuously engaged low-lead sliding retention in
reusable grounded heads instead of 6,400 cells. Compare grounded screw/nut-driven
bilateral carriages against counterbalanced pad heads: raising/lowering, moving
input loss, motor speed, heat, inertia, reactions and two-output access. No inherited
working dock or A-007 reopening. Stop on release of sole support, inadequate
kinetic arrest or unchanged-output disturbance. CTO owns this probe; no approval gate.

Self-review: independent normal/tangent force resolution, frictionless virtual
work, nonnegative dissipation, bed moment equilibrium, exact equal-friction
threshold, affine geometry endpoints/three refinements, minimax balance, strict integer channel scheduling
and unit conversions. These check reduced calculations, not printed contacts
or hardware reliability.
