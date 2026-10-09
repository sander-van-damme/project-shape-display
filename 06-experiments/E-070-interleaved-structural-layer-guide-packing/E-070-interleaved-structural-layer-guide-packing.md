---
status: complete
builds-on: [E-069, E-068, A-022]
---

# Interleaved structural layer: a guide-play packing rejection

**Reject the tested clearance-only interleaved guide at the stated bounds.**
Two centered, connected finite geometries fit 5.08-mm pitch; both fail when
allowed guide translation is included. This closes an omitted degree of freedom
in E-068/E-069, not the structural-displacement principle. Do not print or run
strength optimization on this embodiment. A changed datum restraint or packing
must first escape the failure below.

Input main `beacd13`. Reproduce with
`python3 tools/curated-experiment-checks/E-070/guide_packing.py`.
`--all` emits the rejected population and reasons; `--geometry` emits the
upper-stage witness solids. Deterministic standard-library construction and
exact axis-aligned swept boxes, all lengths in mm. No random seed, external
solver, calibrated process distribution, measurement or hardware qualification.
These are three **guide topologies within one architecture**, not 72 inventions.

## Generated assembly and coverage

Join the E-069 latch shelves to an 0.8-mm-wide carriage neck; put an actual
blind dog bore above the fixed vertical guide. The bore has a floor, roof,
two side walls and backstop. Interleave the tongue guide behind the dog lane,
with a finite bridge/backplate joining it to the vertical guide. Generate:

- Closed rectangular sleeve around the neck: front wall blocks translating
  latch shelves.
- Open C guide: shelves clear, but the neck can escape through the open side.
- Captured T guide: a rear flange and two retaining lips leave the shelf path
  open. Stop the flange below the bore; continuing it through the bore blocks
  the dog. This relief still leaves the flange covering the guide throughout
  full stroke, overtravel and E-069's failed-proof descent.

Generate each profile for relative fit-error bounds e=0.15/0.35/0.60, residual
lip engagements B=0.2/0.4, wall/web thickness w=0.4/0.8, and guide lengths
L=1.6/4.0: **72 sections**, each checked at 10/20/40-mm stage strokes. Parameters
are constructed at necessary packing limits, not optimized for strength. The
middle/wide cases are packaging counterfactuals; E-069's tight contact bounds
are not transferred to them as qualified load-transfer paths.

Each T realization contains 27 box primitives, grouped into joined carriage,
joined mount, dog, tongue and fork; these are not 27 separately assembled parts.
Connectivity requires positive face area or volume overlap. Check the carriage
against every fixed guide/mount wall over its entire vertical interval, dog
translation through the finite bore, tongue translation through its sleeve,
acquisition/release/deposition in both directions, rail/mount clearance, and
parked-body bypass over a 70-mm lower-offset holdout. Swept bounds also include
a 0.25/0.45/0.65-mm descent on failed proof. The bore is raised accordingly;
omitting that space produces a guide collision in the deliberate failure test.
E-069 retains its isolated quasistatic contact/proof result and unsafe false
acceptance case. New bore vertical play and rocking have not been propagated
through that model: these prescribed paths do **not** prove assembled support
continuity. No actuator, stroke-stop or reader is inferred from a box sweep.

## Prescribed-translation result and independent width bound

Let g=0.05+e be nominal running clearance, r=o=0.4+e dog root/rail overlap, and
c the core width. A real blind backstop adds a 0.05-mm running margin to E-068:

`c ≥ 0.8+r+g+o+e+0.05`.

The right rail edge is `R=c+g+o+e+0.1+w`. A T wing needs projection
`p ≥ B+g+e`; its outer guide wall extends left by `p+g+w`. Thus, within this
constructed topology (including its stated outer relative-error reserve),

`P_x ≥ R+e+p+g+w = 2.35+B+2w+11e`.

The orthogonal dog lane/tongue arrangement independently needs
`P_y ≥ 3.7+3e+2w`. Equality is a necessary packaging allocation, not a claimed
manufacturing capability. Both expressions are checked against generated
extrema across every parameter combination.

| Bound e | P_x, B=0.2 / 0.4, w=0.4 | P_y, w=0.4 |
|---|---:|---:|
| 0.15 | 5.00 / 5.20 | 4.95 |
| 0.35 | 7.20 / 7.40 | 5.55 |
| 0.60 | 9.95 / 10.15 | 6.30 |

Only tight T sections with B=0.2 and w=0.4 pass prescribed translation, for
both guide lengths: **2/72**. At e=0.15 their core is 2.30 mm, wing 0.55 mm,
nominal clearance 0.20 mm, and x/y envelope reserves are only 0.08/0.13 mm.
Increasing guide length raises the dog datum/depth but does not improve pitch.
A 0.4-mm loaded printed wall and 0.2-mm residual engagement remain unqualified.
Centered neighbor clearance follows from the generated x/y envelopes for
arbitrary vertical states; it must not be transferred to a freely moving guide.

## Allowed guide motion falsifies both centered witnesses

The carriage has nominal lateral free play **±0.20 mm**, even with perfect
parts. This is a mechanism degree of freedom, not another draw from e.
Construct a permitted +0.19-mm carriage displacement and a common −0.15-mm
rail datum offset. Keep every other solid nominal. Executable exact geometry
finds:

- The shifted carriage remains clear of the fixed guide/mount.
- The centered carriage remains clear of the biased fork.
- Their combination intersects both bore floor/lower fork and bore roof/upper
  fork at the upper-stage acquisition state.

A common rail error can affect a bank; it need not occur independently in all
6,400 cells. This counterexample uses one shared bias and a permitted local
position, with no invented probability. Longer guides (including an off-grid
11.137-mm check) do not remove the translational freedom. Rotation, elasticity,
wear and adverse guide-size errors can worsen it but are unnecessary to reject
this case.

Even keeping every other allowance unchanged, accommodating lateral play j
requires increasing the bypass gap and dog storage length, giving the necessary
bound `P_x ≥ 5.00+2j`. With nominal j=0.20, **P_x≥5.40 mm**. The pitch permits
at most j=0.04 mm before accounting for engagement loss or tilt. Reducing running
clearance to that level conflicts with the current e=0.15 and 0.05 running-margin
scenario. The corresponding necessary error bound is e≤0.1254 mm for B=0.2,
w=0.4 and j=0.05+e; this is a reopening condition, not evidence that the actual
printer meets it. No finer sampling of these parameters repairs the current
bound. **Zero robust survivors remain among the tested profiles.**

## Evidence limits and next decision

The e scenarios inherit explicitly uncalibrated aggregate dimensional/alignment
bounds from E-068. Pairwise e/2 box expansion on each solid represents a total
relative fit budget, not independent errors. Common rigid translation cancels;
the final adverse rail registration is shared and separate from unconstrained
guide motion. No yield, timing tail, fatigue life or false-acceptance rate is
reported. Contact pairs allow intended touching; internal-pocket erosion and
proof uncertainty remain the separate E-069 bounds. Strength, friction, creep,
guide rotation and dynamic settling have not been simulated.

Stop this symmetric-clearance T-guide embodiment before stacked connectors,
FEA or fabrication. Do not reinterpret 2 centered passes as survivors. Reopening
requires a mechanism that bounds lateral position under changing loads, a
materially different allocation of guide space, or process evidence changing
the bound. Next compare a positively biased datum against guide relocation to
a shared/bank frame, including retained bypass of unselected cells and the
force/friction/assembly burden of up to 19,200 guided stages. Only a surviving
restraint/packing mechanism earns stacked geometry and full-system comparison;
otherwise conclude this campaign with scoped rejection. Rack/mask alternatives
retain their existing evidence status.

Self-review: exact touching/sweep cases, connected-body tests, both latch
stroke directions, an off-grid geometry, deliberate omitted-proof-clearance
and excessive-error failures, the open-guide escape, and a common-bias/free-play
counterexample. These are model checks, not independent physical validation.
Reproducible JSON is not retained.
