---
status: complete
builds-on: [A-022, E-067, E-050]
---

# Retractable structural-layer dog: bypass and common-rail handoff bounds

**Retain a narrow fixed-reference access witness; reject this section under
middle/wide dimensional bounds.** Lateral retraction can make parked carriages
clear a continuous shared rail at every lower-stage offset. It does not solve
load transfer. A rigid rail encountering unequal dog heights needs differential
unload travel or individually sequenced latch release. Enlarging its acquisition
mouth alone cannot supply that compliance.

Input main `0e218d8`. Reproduce with
`python3 tools/curated-experiment-checks/E-068/dog_sweep.py`; `--all` emits every
case and rejection. Standard-library deterministic enumeration, no random seed.
Evidence: finite extruded box sweeps, independent geometric bounds and necessary
transfer/timing calculations. No complete CAD, contact solver, physical data,
qualified material strength, production yield or hardware timing.

## Generated section and coverage

Use E-067's selected-column normalization. At each of three stacked stages,
an output carriage has a dog sliding in x into a vertically moving fork rail.
The rail runs along y, beside the carriage rather than through its body. The
same section may be repeated at different z levels; inter-layer stacking,
vertical rails/links, lateral guides and the latch are **not yet generated**.
Do not transfer this result to the nested-stage realization without new geometry.

Generate core width c=2.4/2.8/3.2 mm, gap g=0.2/0.4/0.7, overlap o=0.6/0.9/1.2,
dog root r=0.6/0.9/1.2 and rail web w=0.4/0.8: 162 geometries per error scenario,
486 total. These are parameter variants of one topology, not 486 mechanisms.
Dog height is 1.2 mm; upper/lower fork cheeks are 0.8 mm thick; preserve an
assumed 0.8-mm core spine and ≥0.4-mm residual root/drive bearing overlap.
Those minima are design assumptions, not load/print qualifications. The 0.4-mm
web is especially unqualified as a loaded single-extrusion feature.

Explicit solids in x,z, extruded through the same 2-mm y section:

- Carriage envelope ends at x=c. Deployed dog spans x=c−r to c+g+o; withdrawal
  by g+o parks its outer end flush at c. Its internal bore is an allocation,
  not modelled contact geometry; the carriage envelope tests exterior bypass.
- Rail cheeks start at c+g and end at R=c+g+o+e+0.1+w; the web occupies
  [R−w,R]. For acquisition allowance a, cheeks occupy z=[−a−0.8,−a] and
  [1.2+a,2+a], and the web joins them. A dog at z=[δ,δ+1.2], |δ|≤a, slides
  through that mouth. Boundary touch is allowed; positive running clearance
  beyond the stated bounds still needs design margin.
- Parked dog/core and rail are inflated by e/2 each for bypass; e is the total
  **relative** error budget, not an error assigned independently to both.
  Require g−e≥0.05 mm, r−e≥0.4, o−e≥0.4,
  c−r−g−o−e≥0.8 and R+e≤5.08. Tip clearance e+0.1 is reserved separately.

Each geometry checks 144 exact swept box/obstacle pairs: three layers, all eight
bit words (including the 70-mm arithmetic holdout), three rail solids and two
obstacles. Rail translation through 10/20/40 mm uses the exact swept volume,
so forward and return strokes have identical coverage; no time-step sampling.
Dog deployment is also a continuous swept box, tested at both extreme reference
errors. For motion of parked upper stages with lower stages, x separation is
an independent sufficient proof for **every** continuous vertical position:
rail x≥c+g, parked solids x≤c, g>e. This does not prove clearance against
omitted lateral mechanisms, other layer rails or a neighboring y carriage.

| Relative-error bound | Surviving grid sections | Continuous minimum pitch |
|---|---:|---:|
| Tight, e=0.15 mm | 15 / 162 | 3.80 mm |
| Middle, e=0.35 mm | 0 / 162 | 5.40 mm |
| Wide, e=0.60 mm | 0 / 162 | 7.40 mm |

A tight witness has c=2.4, g=0.2, o=r=0.6, w=0.4 mm: allocated width 4.00 mm,
remaining spine 0.85 mm, residual dog/root overlap 0.45 mm and bypass gap
0.05 mm. The continuous bound follows independently by substituting
r≥0.4+e, g≥0.05+e, o≥0.4+e, w≥0.4 into
`pitch ≥ 0.9+r+2g+2o+w+3e`, giving **pitch≥2.6+8e**.
Thus e≤0.31 mm is necessary for this cross-section even off-grid. Middle/wide
rejection is not repaired by finer parameter sampling. Different dog storage,
drive orientation, shared lane allocation or smaller justified support sections
can escape it; this is not a rejection of structural memory.

## Correlated reference error and supported acquisition

Use E-050's explicitly uncalibrated batch/spatial/local contributions:
0.05/0.05/0.05, 0.10/0.10/0.15 and 0.20/0.20/0.20 mm. They aggregate fit,
wall/hole error, quantization and alignment; they are not X1C probability priors.
Keep first-layer artifacts away from contact faces. Here, conservatively apply
one aggregate per lower collapsed reference **and one for the dog mounting**.
Additionally allocate common bank registration b equal to the batch component.
Layer i (zero indexed) therefore requires mouth allowance a=b+(i+1)e.
This accumulation is an assumption to revisit with actual datum geometry.

Common registration and batch bias shift all dogs in a bank together and cancel
from the **difference** that drives simultaneous transfer. For a bank spanning
opposite regional errors, maximum height difference is
`Δ=2(i+1)(spatial+local)`; for a coherent region it is `2(i+1)local`.
Neither is a random-sample prediction. The adverse case requires aligned error
signs across stacked parts; shared material/orientation can make this relevant.

Consider two load-bearing dogs differing in height by Δ. Starting below both,
a rigid lower fork cheek must rise Δ after touching the first to touch the
second. If the first column's still-engaged latch allows only u free upward
motion, **u≥Δ is necessary before common release of both latches**. Otherwise
it jams against its latch before acquiring the last dog. Exact opposing-face
geometry, load-dependent deflection and a positive unload margin would tighten
this condition. This is a kinematic counterexample, not a generated latch.

| Scenario | Mouth allowances, layers 0/1/2 mm | Minimum u, split regions mm | Minimum u, coherent region mm |
|---|---|---|---|
| Tight | 0.20 / 0.35 / 0.50 | 0.20 / 0.40 / 0.60 | 0.10 / 0.20 / 0.30 |
| Middle | 0.45 / 0.80 / 1.15 | 0.50 / 1.00 / 1.50 | 0.30 / 0.60 / 0.90 |
| Wide | 0.80 / 1.40 / 2.00 | 0.80 / 1.60 / 2.40 | 0.40 / 0.80 / 1.20 |

An assumed 0.5-mm free-unload latch already fails the upper tight layer when
a bank spans both regional extremes; it passes that necessary bound within a
coherent tight region. Treating common bias as independent would overstate
mismatch; assuming perfect spatial coherence would hide the failure.

Possible escapes to evaluate are greater latch overtravel with positive seats,
a floating/equalizing dog, or proof followed by individual latch release as each
dog is acquired. Each changes contacts, control, lost motion or bank segmentation.
Deposition must likewise prove each fixed seat before withdrawing its dog;
blind simultaneous release can leave an unsupported column. No support-continuity
pass is claimed from the acquisition bound or the rail's two cheeks.

## Alternative access and complete-system implications

A single rigid rail that co-moves with an entire row cannot follow layer-1
bases at 0 and 10 mm simultaneously (neighbor states 0 and 1). Per-site
followers, segmented drives or normalized access remain possible, with their
extra guides/contacts charged; this counterexample rejects only the undivided
row-following idea.

A travelling head can reach variable offsets but serial contact time matters.
E-067's uniform 25-pair workload has 1.6 normalized events/site: 10,240 events
on 6,400 sites. At an **assumed optimistic** 20 ms per complete event, a single
head needs 204.8 s before any travel. A full map of worst three-event pairs
needs 384 s. Even ideal parallelism needs ≥13 heads for that worst case to fit
<30 s before travel, positioning, proof and recovery; 13 is not a sufficient
machine specification. Rack E-050 remains the implemented accounting comparator.

Fixed rails retain E-067's 5.1314-s serial traversal allocation, not an achieved
update time. Larger mouths/unload travel, individual proof/release and common
force must enter its <3.1448-s complete-event budget. Three stages still mean
19,200 dogs, latches and guide sites. All carry the column payload serially.
No bought-component cost, print time, service-life or reader false-acceptance
advantage has been established. Finite box checks omit strength, creep, fatigue,
friction, wear, deflection and readback; no printing or FEA is justified yet.

**Next discriminator:** generate a finite dog/latch/support-transfer realization
for the tight section, including actual release/deposition paths and failed
proof behavior, then all three stacked layers and neighboring guides. First
compare rigid large-clearance and floating-dog transfer; stop an implementation
on missing positive support or unavoidable collision. Reopen a middle-bound
section only by changing its packing assumptions/topology, not refining the
same grid. LAB-190 remains a healthy campaign; this result completes its first
bounded bypass investigation, not its geometry or full-machine gate.

Self-review: exact-box limiting/touching/translation checks; independent
continuous packing inequality; x-separation proof covering unsampled offsets;
and correlation cancellation in the two-dog transfer counterexample. No external
review or independent physical validation is claimed. Reproducible JSON is not
retained.
