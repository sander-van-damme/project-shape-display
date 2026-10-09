---
status: complete
builds-on: [E-068, E-067, A-022]
---

# Structural-layer supported transfer: finite pockets and proof clearance

**Retain rigid overtravel as a contact-path witness, not an assembled machine.**
A free floating dog with a single hard load stop does not remove bank mismatch.
An independently locked floating dog could, at the price of another repeated
load lock. The straightforward disjoint dog/latch lane embedding fails pitch.
Do not proceed to FEA or printing before packing and support proof are resolved.

Input main `341114a`. Reproduce with
`python3 tools/curated-experiment-checks/E-069/support_transfer.py`; `--all`
emits all 24 cases. Standard-library deterministic geometry/contact model;
no random priors, physical measurements, calibrated sensor or strength model.
This adds finite latch contacts, deposition and failed-proof consequences to
E-068; it does not replace its bypass screen or claim assembled three-layer CAD.

## Mechanisms and generated contacts

Compare three causal mechanisms: rigid dog plus latch overtravel; vertically
free dog terminating at one load-bearing hard stop; independently lockable
floating dog. Only the first is generated as finite contacts. A spring-only
float is not a positive structural support. The third remains an unbuilt
escape, not a survivor credited with zero lock cost or proof time.

The latch section is a local y,z plane extruded 0.8 mm in x. Its tongue spans
y=[−0.8,0.6], z=[−0.8,0]. Withdraw it 0.8 mm to y=[−1.6,−0.2]. A carriage
has two pockets separated by the stage stroke S=10/20/40 mm. For each pocket,
at offset k=0 or −S, upper shelf spans y=[0,1.2], z=[k,k+0.8]; lower shelf
spans y=[0,1.2], z=[k−u−1.6,k−u−0.8]. A 0.8-mm backbone at y=[1.2,2]
joins them. Thus the upper shelf rests on the tongue at q=0; lifting q through
[0,u] opens that support without collision; at q=u the lower shelf touches
the tongue underside. This explicitly models the contact which limits unload.
The withdrawn tongue clears all shelf/backbone travel by nominal 0.2 mm.
Tongue actuator, its grounded guide, dog bore and full carriage body are absent.

Generate nominal pocket travel U=0.3/0.5/0.7/0.9 mm, three stages and two
correlation bounds: 24 sections, **16 pass the isolated path screen**. Apply
an additional explicit 0.15-mm internal fit erosion: u=U−0.15 and usable fork
free height G=2a−0.15. This is an uncalibrated adverse dimension bound, separate
from E-068's seat/dog reference mismatch. Their simultaneous extremes are
conservative epistemic scenarios, not independent random errors. Tongue/shelf
thickness, root bearing and backbone strength are unqualified design allocations.

Use E-068 tight split-region mismatch Δ=0.2/0.4/0.6 mm, or coherent-region
Δ=0.1/0.2/0.3. Common registration/batch bias cancels. Allow 0.05 mm positive
unload clearance m and a 0.05-mm proof separation p. The continuous bounds are:

- Pocket: **U ≥ Δ+m+0.15**; split-region minima 0.40/0.60/0.80 mm.
  Smallest sampled passes are 0.5/0.7/0.9; coherent passes 0.3/0.5/0.5.
- Fork: **2a−0.15 ≥ Δ+p+m**. Original a=0.20/0.35/0.50 needs the
  lower-stage mouth widened to **0.225** mm; other two remain unchanged.
  Acquisition clearance alone did not account for deposition proof clearance.

Sweeps cover acquisition with tongue engaged, tongue release, full travel with
it withdrawn, destination insertion, and deposition in both stroke directions.
An independent finite dog/fork section checks withdrawal across cheeks/web.
These are exact axis-aligned swept rectangles, not time-step collision samples.
The pocket and dog sections are tested separately: connecting them without
collisions remains a machine-geometry obligation. Contact equality is allowed;
positive margin is allocated where stated, not inferred from floating-point
nonintersection. No frictional release or elastic deformation is simulated.

## Support sequence, proof and failure

Let d_j be each dog's bottom height when seated at an endpoint. At acquisition,
raise the rail to max(d)+m. Each selected carriage lifts by at most Δ+m;
all dogs then carry load before tongues retract. Translate with tongues
withdrawn, approach the destination at max(d_new)+m, insert tongues, and lower
the rail to min(d_new)−p. Independent endpoint errors, including reversed
extremes, are allowed; this is not a same-error-at-both-ends assumption.

For a present tongue, dog height is z_j=max(R,d_j) as rail height R lowers.
Therefore it rests on the rail or tongue at every intermediate position,
with both contacting at equality. Finite pocket walls remain clear along
that path. Once every tongue is seated/proven, retract dogs with gaps in
[p,Δ+p], hence the additional fork-mouth bound. A two-site extremal bank
is sufficient for these interval bounds; arbitrary interior sites cannot
increase maxima/minima. Checks also include an interior off-grid holdout.

For an absent destination tongue, z_j=R: the rail still supports the site.
**Any failed proof must inhibit the whole bank's dog withdrawal.** An upper
split-bound site can descend **0.65 mm below its intended endpoint** by the
end of the common proof stroke. Recovery raises the engaged rail to reacquire
all successful seats before another release attempt; the same unload bound
applies. The model assumes a functioning rail remains held. A brake/service
support and recovery under drive/power loss are unresolved. Partial insertion,
jammed or fractured tongues and inertia are outside this absent-tongue model.

A position proof is conditional on an actual reader. With error bound r on the
reported displacement and possible seated deflection c, success/failure
intervals separate only if **p > 2r+c**. At p=0.05, r=0.03 already fails even
with c=0. Sweep r=0.01/0.03/0.05, c=0/0.02/0.05 and p=0.05/0.10/0.15;
these are sensitivity bounds, not sensor specifications. A larger probe
requires a larger mouth and creates more failed-site motion. Bias cancellation
in a differential reader cannot be assumed for separate reference readings.
A false acceptance followed by dog withdrawal leaves an absent-tongue site
unsupported. No false-acceptance probability, bank yield or hardware-safe
recovery follows from ideal-reader support equations.

## Floating dog and packing rejection

A free vertical dog slot of length L can align with the rail initially, but
cannot lift its carriage until reaching its load-bearing hard stop. Contact
heights become d_j+L; their difference stays Δ. A common L therefore leaves
the same rigid-rail overtravel requirement. Per-site adjustable positive locks
could freeze different offsets before lifting, adding up to **19,200** load
locks plus commands, guides and proof. That materially different mechanism
needs generated contacts before it earns preference over the rigid witness.

The simplest disjoint-lane embedding places E-068's 2-mm dog section beside
this latch's 3.6-mm full lateral swept envelope. With assumed 0.2-mm separation
and 0.15-mm outer relative error it needs **5.95 mm**, exceeding 5.08 mm even
before latch guides. Reject that embedding. This is not a lower bound on
interleaved x/y geometry: the latch might occupy part of the residual core
spine, or share vertical lanes. Either must generate the connecting body,
finite guide walls and neighboring volumes, not add isolated-section passes.

Next discriminate interleaved latch/dog packing and stacked-stage swept volumes
under arbitrary lower offsets, with failed-proof rail retention included. Stop
if positive support requires an inaccessible interface. If geometry survives,
charge proof/readback, rail brake, addressing, repair and bank force in the
complete rack/mask comparison. E-067's <3.1448-s event budget remains an
allocation; none of these added strokes, readers or locks has measured timing
or purchased cost. No purchases, fabrication or calibration request follows.

Self-review checks finite-wall collision at and beyond the analytic unload
limit, deliberate mouth failure, both stroke directions, reversed endpoint
errors, off-grid interior errors, each absent-seat case, and floating-stop
mismatch invariance. These establish model consistency, not independent
physical validation. Reproducible JSON output is not retained.
