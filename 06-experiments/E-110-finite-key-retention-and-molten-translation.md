---
status: complete
builds-on: [A-018, E-063]
---

# Finite keys: retention, translation and material transport

At input main `e4dde0c`, positive circumferential keys remove reliance on
adhesion but increase heated inventory and introduce alloy transport across
the collar ends. **Do not advance a bare keyed through-collar to thermal
optimization as if containment were solved.** Retain it conditionally pending
a finite drainage/return/seal mechanism, or change to an encapsulated thermal
lock that acts on a retracting mechanical support. Neither is a machine pass.

Reproduce: `python3 tools/curated-experiment-checks/E-110/keyed_collar.py`;
`--all` emits all 648 deterministic cases and overlapping rejection reasons.
No random seed, measured material properties, physical evidence, CAD release,
or calibrated X1C tolerance model is present. This is generated piecewise
cylindrical geometry plus idealized load-cut calculations, self-reviewed.

## Generated geometry and cuts

A metal tail of land radius R has rectangular circumferential grooves of depth
k, width w and axial period p. A fixed cup has bore R+g and outward recesses
of the same k,w,p. Tail track spans the collar and complete 40-mm stroke.
Collar length L is finite; all arbitrary groove phases are checked. Continuous
alloy connects tail-groove shoulders to cup-groove shoulders. Solid alloy
blocks both axial directions; molten alloy removes this geometric constraint.
Maximum tail radius R remains below minimum cup radius R+g at every position.
This does not bound viscous drag or prove that every obstructing volume melts.

Exact interval overlap integrates tail and cup groove volumes. Volume extrema
occur when groove edges cross collar ends, so the evaluator includes all such
phases, endpoints and intervening intervals. Collision integration intersects
a moved solid tail with the original frozen alloy, not merely endpoint states:
a 1-mm-period shift ends at a compatible geometry but collides along its path.
A smooth tail gives zero positive-key collision, exposing its adhesion/friction
obligation. Cup collision is excluded analytically by disjoint radial envelopes
for positive effective gap throughout the finite generated track.

For n complete tail keys and nc complete cup keys, the ideal parallel-key
capacity is the minimum of:

- Tail shear: n τ 2πR w; tail bearing: n σ π[R²−(R−k)²].
- Cup shear: nc τ 2π(R+g)w; cup bearing: nc σ π[(R+g+k)²−(R+g)²].

Only complete keys receive credit; partial edge keys are ignored. These are
**conditional cut screens**, not a rigorous bound on whole-collar capacity:
equal load sharing, connected solid material and rigid substrates are assumed.
Bulk splitting, groove-root bending, freeze voids, interface separation,
stress concentration and creep can reduce support. Ignored partial keys could
rescue a marginal rejected geometry. No screen survivor is accepted hardware.

Grid: R=1.5 mm; g=.1/.2; k=.1/.2/.3; w=.25/.5; p=1;
L=2/5/10 mm; angular fraction f=1 or .25. Fractions represent full annuli versus
ideal discrete sector bridges, not a second optimized machine. Capacity and
volume both scale by f; sector walls, axial/radial seals and feed channels are
excluded, making sectors an optimistic envelope. At fixed load, reducing f
usually requires additional keys or strength. It is not a free heat reduction.
A .3-mm cup wall is a packaging allocation, **not qualified printed geometry**.

Uncertainty scenarios: (τ,σ)=(.25,1)/(1,5)/(5,20) MPa are effective long-term
allowable-stress hypotheses, not alloy or polymer property claims. Combined
error e=0/.05/.15 mm closes the gap and separately reduces key depth and width.
These corners apply coherently to the whole board; they are not probabilities.
They bound radial fit/key loss only. Pitch error, axial warp, layer quantization,
roughness, first-layer interference and orientation cannot be compressed into a
qualified e without process evidence. Temperature, dwell, creep, fatigue and
wear would have to justify the effective stresses; rankings below depend on them.

## Results and comparisons

At illustrative 10 N, 466/648 cases miss the full-key cut criterion; 108 close
the radial clearance and 72 erase a key dimension (counts overlap). There is
no yield inference. Minimum nominal collar inventory among surviving annular
cases is shown below; energy uses E-063's generic .5 J/mm³, not a material fact.

| Effective τ/σ MPa | Error e mm | Minimum annulus mm³ | Ideal board average W over 30 s |
|---|---:|---:|---:|
| .25/1 | 0 | 29.217 | 3116.5 |
| .25/1 | .05 or .15 | none in grid | — |
| 1/5 | 0 | 9.739 | 1038.8 |
| 1/5 | .05 | 14.608 | 1558.2 |
| 1/5 | .15 | 25.133 | 2680.8 |
| 5/20 | 0 | 2.922 | 311.6 |
| 5/20 | .05 | 5.843 | 623.3 |
| 5/20 | .15 | 10.053 | 1072.3 |

The optimistic quarter-sector family reaches 1.826 mm³ at strong/zero-error
settings, but has no .05-mm-error survivor at middle strength in this grid.
At strong/.05 it reaches 3.652 mm³. Neither reduced inventory establishes
contained bridges. No specified power ceiling justifies rejecting these
numbers alone; supplies, cooling, neighbor isolation and <$500 bought cost
remain full-machine obligations. The annulus-versus-sector frontier is
conditional on missing containment, with no defensible cost/reliability winner.

A holdout R=1.5,g=.1,k=.2,w=.4,p=1,L=5.2 mm at τ=1,σ=5,e=.05 credits four
complete tail keys and 13.19 N ideal capacity. Inventory is 13.283–13.635 mm³
across phase, requiring .352 mm³ displacement accommodation even before
thermal expansion or freeze shrinkage. Integer-period L cancels this ideal
volume modulation; it does **not** eliminate material carried through the ends,
and length/pitch manufacturing errors break exact cancellation.

| Mechanism | Load path / release | Distinct burden |
|---|---|---|
| Smooth fusible annulus | Adhesion or friction into grounded cup; melt to slide | A-018 inverse bound remains; smooth-interface strength unqualified |
| Keyed fusible annulus | Positive tail/cup shoulders; melt intervening alloy | Higher inventory; axial escape paths, retained liquid, refrozen debris |
| Discrete fused bridges | Same shoulders over angular sectors | Less area and capacity together; sector isolation and replenishment missing |
| Keyed thermoplastic collar | Same geometric keys; soften/flow then recover strength | Same geometry under same stresses; changing material supplies no automatic creep, drainage or cooling pass |
| Retracting mechanical key | Solid shoulder into frame; withdraw key then translate | No bulk melt inventory; actuator must clear k plus error, with wear/return/readback burden; addressing and cost still unresolved |

The retained submillimeter catheter reference uses encapsulated alloy and a
47°C melt point, with a resistive heater and resistance feedback. It supports
small-scale thermal switching, **not** a sliding keyed feedthrough or service
creep allowable ([Lussi et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8456283/),
accessed 2026-10-10). No force/strength or timing is transferred from it.

## Containment decision and next discriminator

With no contacting seals, the positive running gap forms an axial connected
path to each open end. Surface tension/wetting could retain liquid under some
conditions, but geometry alone does not establish retention. A seal on a
smooth land is not automatically a seal on a translating grooved track.

If all exiting grooves stay filled, one 40-mm stroke exports
`f π[R²−(R−k)²] 40 w/p` mm³ of liquid from the locally heated region (40/p is
integer in this grid). The holdout exports **28.149 mm³**, over twice its
collar inventory. Zero export is the competing perfect-drainage scenario;
wetting and entrainment are unmeasured. This is transported volume, not a
measured loss rate: a reservoir might recover it. Without drainage/return it
starves the cup or deposits material outside the hot zone, where refreezing
can obstruct motion. Regional unchanged support also forbids blindly heating
all neighboring cartridges to clear contamination.

Do not solve this by silently assuming a larger sealed cartridge: an enclosed
40-mm track adds heated/wetted inventory and end accommodation; a closed-end
3-mm rod also sweeps up to πR²·40=282.743 mm³ unless a compensating geometry
or compliant boundary accepts it. Two-ended equal-area rods can cancel net
swept volume but still need both moving boundaries and groove-material return.

Next compare two genuinely changed containment paths within A-018: (1) a
finite local drain/return reservoir with a non-keyed sealing land or separated
seal path; (2) an encapsulated thermal structural lock on a short-stroke
retracting jaw, leaving the 40-mm pin dry. The latter must retain a complete
support/energy/reset path and is not novel if it merely reproduces A-017's
thermal command latch. Reject each if its finite geometry cannot close the
material cycle; then thermal analysis is justified only for informative
survivors. No print request follows from this screen.

## Verification and limits

Independent midpoint integration of an off-grid geometry at 1k/10k/100k
slices differs from the exact volume by .008591/.001249/.000081 mm³. A separate
1001-phase sweep stays inside the exact event extrema. Tests include the
smooth-annulus limit, fractional-volume scaling, collision/error failures,
frozen-path collision in both directions and a misleading clear endpoint.
These validate the reduced geometry calculation, not real contact, structural
capacity, sealing, alloy behavior or board reliability. No independent human
or agent review is claimed.
