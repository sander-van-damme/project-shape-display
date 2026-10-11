---
status: complete
builds-on: [E-116, E-201]
---

# Double tapers repair transfer only after changing the pin and vertical package

**Retain a wider, longer tapered transfer as a geometric alternative; reject a
simple taper substitution in E-116's package.** The latter still catches on reset
and cannot combine the stated straight-shank overlap with sliding recentering at
μ=.5. A .8-mm pin with 5.4-mm length clears both directions in the bounded finite
model. This changes the disposition of the transfer interface, not the machine:
its row allocation exceeds 5.08 mm, most shared-jam force scenarios still fail,
and no head, supported cassette removal or outage arrest is implemented.

Input main `271dcce`; LAB-329. Reproduce:
`python3 tools/curated-experiment-checks/E-202/taper_transfer.py`.
Standard-library Python, deterministic finite geometry and analytical contact
bounds; no process distributions, measurements, contact dynamics, hardware
qualification or independent review. Verification is self-review. JSON is
reproducible output and is not retained. No printing or purchase proposed.

## Changed interface and bounded construction

E-116's full-width blunt pin cannot transfer from every allowed keeper position
into an independently displaced cam slot, and vice versa. Its maximum mismatch
is reconstructed as .2225 mm. A double-ended square frustum can move laterally
while a positive external fork drives z, so initial slot containment need not
hold for the **full-width** pin. The tip still must enter without an instantaneous
lateral jump. The fork must permit that lateral motion; it is a boundary condition,
not an implemented capture or readback mechanism.

Keep the keeper top at z=0, cam underside at G=4 mm, 1.2-mm plate thickness,
cam slope m=.3 and working run 3 mm. Keeper walls are `|x−ck|≤p/2+.2+wk`;
cam walls are `|x+.3y−cc|≤p(1+.3)/2+.2+wc`. These are finite extruded slots,
with y ends ±Y for the keeper and [−3−Y,Y] for the cam, Y=p/2+.2.
The pin has a square straight middle and two symmetric linear frustums of
length t, ending in a finite square tip. It translates in x,z; y and orientation are fixed by ideal constraints.
Finite bearings and their moment/friction reactions are not implemented.
Cam remains at home throughout selection/reset.

| Nominal section, mm | Original package + taper | Changed transfer |
|---|---:|---:|
| Full pin / tip width | .6 / .1 | .8 / .2 |
| Pin length / each taper length | 4.8 / .225 | 5.4 / .4 |
| Idle / selected lower-end z | −1.4 / .6 | −2.0 / .6 |
| Command stroke | 2.0 | 2.6 |

All uncertainties are **epistemic bounds**, not calibrated X1C capability:
full pin width, tip width, pin length, taper length, independent keeper/cam x
positions and wall positions, fixed y registration and each plate z translation
vary ±.05 mm. The two tapers share their length error in enumerated cases;
using their independent worst extrema gives the same overlap/slope bounds.
Both finite y openings additionally shrink by .05 mm at each end. Plate thickness
is fixed; tilt, nonstraight walls, fillets/burrs, roughness, contact indentation,
warp, first-layer effects, compliance, creep and wear are not represented.

Retained z drift remains E-116's ±.30 mm, from its ideal two-groove gate section.
All paths cover the enlarged endpoint interval, including opposite endpoint
drifts. Minimum idle cam clearance is .20 mm; selected keeper clearance .25 mm.
The new 2.6-mm command stroke fits the existing **section-only** gate-height
budget: `.4+2.6+2(.175)+4(.05)=3.55<4 mm`. This is neither an assembled gate nor
proof of withdrawal. Its lateral routing, load capacity and false acceptance
remain unresolved. No passive gravity or spring completion is credited.

## Actual entry, paths and straight-shank continuity

At each z, intersect the finite pin with both plate slabs and enumerate vertices
of the clipped square frustums. Their four horizontal corners must lie within
all slot half-planes. The greatest pin width in each slab independently gives
its allowed x interval. Event nodes include every tip/shoulder crossing of a
plate face; between nodes the half-plane bounds are affine. Interpolating feasible
endpoint poses therefore supplies a continuous geometric path. A new plate's
entry constraint must contain the incoming pose; projection across a jump is
reported as a collision, never accepted as recentering. Both extreme starting x
positions are traced in both directions; intervening starting positions are
bounded by the ordered interval projection.

The full-shank keeper/cam intervals overlap by at least **.1275 mm** in both
packages. This bounds all narrower tapered sections too, but alone does not
prove entrance capture. The original package has **−.0225 mm** tip-entry reserve
on reset. A finite witness has b=.55, tip=.15, ck=−.05, cc=.05, y=−.05,
keeper half-width .45 and cam half-width .64. Its cam permits x=.3475, while
the incoming keeper permits at most x=.325: the tip penetrates its wall by
**.0225 mm**. At these bounds the original nominal tip must be ≤.055 mm to
avoid that mismatch when its ±.05-mm width error is included. A near-zero apex
is not a credible default printed repair.

The changed package has **+.0275 mm** minimum tip-entry reserve and needs up to
**.2225 mm lateral recentering**. All 2,048 cases (64 horizontal × 32 axial/tip
corners) have continuous set/reset paths and at least .175 mm straight-shank
overlap with one plate. The original gives 32 entrance failures in 2,048 cases;
these are corner counts, **not** yield or failure probabilities. Common absolute
translation cancels. Shared adverse width/registration errors can repeat the
same failure across a bank; no independent-cell assumption is used.

Straight-shank overlap is a deliberate geometry gate: at least .05 mm with one
plate throughout transfer, so retention is not entirely through axially ejecting
taper contact. It does not establish bearing strength or column load support.
With extra pin length E above the plate gap, the worst minimum overlap is
`max(0,(E−3e−2(t+e))/2)`, here e=.05. Finite clipping recovers .050/.175 mm for
the two sections. This bounds unequal taper lengths too. For the original package
it requires **t≤.225 mm**. Longer tapers without added pin length lose the gate.

The blunt control reproduces .2225-mm entry penetration. An adverse changed
section checked at 16/64/256 subdivisions preserves .175-mm minimum shank overlap
and face clearance ≥−1e−9 mm. Entrance-limit numerical residual falls from
1.73e−9 to 1.08e−10 mm; real collisions are .0225/.2225 mm. Analytical aperture
and overlap bounds supplement the finite corner grid; no sampled reliability
claim follows from passing it.

## Friction trade and remaining jam protection

An ideal square-frustum corner sliding against an oblique slot mouth has radial
slope `r=(b−tip)/(2t)` and required lateral/axial speed ratio `a=(1+m)r`.
The contact normal is proportional to `(1,m,−a)`, perpendicular to both lip and
frustum-edge tangents. For unit transverse resistance, a frictionless bilateral
y guide and Coulomb coefficient μ, define `k=sqrt(1+m²+a²)/sqrt(1+a²)`:

`Fz/R = (a+μk)/(1−μak)`.

A nonpositive denominator gives no positive transverse thrust on this prescribed
sliding branch. This is a conditional contact bound, not a dynamic jam prediction
or proof that other contact modes cannot occur. The source checks all three force
components through the y-guide reaction, μ=0 virtual work and m=0 wedge limit.
Guide friction, fork rubbing, inertia and edge damage add obligations.

Original-package worst r is .3/(t−.05). Even ignoring k≥1, μ=.5 requires
t>.245 mm, inconsistent with t≤.225 for straight-shank overlap. Changing only
taper length therefore cannot pass these bounds, even if the tip entry were fixed.
The changed section has worst r=1; its cam insertion Fz/R is **1.62/2.66/5.33**
at μ=.1/.3/.5. At μ=.8 it loses positive sliding thrust. A nine-length screen
(.10/.15/.20/.225/.25/.30/.40/.60/.80 mm) passes all three entrance, overlap and
μ=.5 necessary gates only at .30/.40 for the changed section; .30 has Fz/R=28.87.
This motivates .40, without declaring an optimized or reliable part.

The working cam's **separate** shared limiter remains problematic. Reuse E-116's
optimistic unsupported lever 2.4 mm and allowable stress scenarios 5/10/20 MPa;
these are not PLA properties. At 20 MPa the full-width pin bending limit increases
from .2311 to .5859 N. For 80 outputs, drag .005/.01/.05 N and cam μ=.1/.3/.5,
only **3/27** changed-section combinations permit a common limiter window:
20 MPa and .005 N/output. The other 24 do not. Transfer loads act on the tapered
region and need their own strength/contact analysis; full-shank capacity cannot
be silently assigned to a .15-mm minimum tip. No double-supported bearing or
per-output limiter has been added.

## Machine consequence and next discriminator

Under E-116's independent row reservation, the new cam-y allocation is
`3+.8+2(.2)+.8+4(.05)=5.20 mm`, exceeding 5.08 by .12 mm. A wider/staggered
cartridge could change that allocation; internal pitch is not required to equal
surface pitch. Such packaging, transport and attachment remain to be constructed.
This result does not revoke E-116's same-plane .10/.20-mm error-box failures.

The transfer still repeats at least 6,400 pins and 6,400 crossbolts, with two
shaped ends per pin, guides, command retention and proof. A larger pin does not
remove those assembly or service contacts. No quotes, build yield, print time,
fatigue, wear, regional disturbance or update-time pass is earned. The bought
boundary remains `Cshared+H*chead+6400*ccell<500 dollars`; a hypothetical $250
shared/head reserve leaves <$0.03906/site. The illustrative inherited schedule
`6+ceil(6400/H)*s` gives 26 s for H=160,s=.5 s, but s=.6 reaches 30 s and fails.
Capture, recentering, command/proof, motion, reset, registration, settling and
bounded supported recovery all belong in s/overhead; this model provides no times.

**Decision:** stop the original-package taper substitution; retain the wider,
longer interface as a geometric lead. Its distinct gain is bilateral recentering
with uninterrupted straight-shank capture, not completed ground-support transfer.
Next construct a finite **laterally floating positive fork and its supported
withdrawal/service path** around this changed section, comparing it with a direct
bilateral slider in a removable row cassette. Require actual retained-state
engagement, space for .2225-mm recentering and a local overload path. Stop if the
fork merely imposes the old incompatible fixed x datum, if removal disturbs
unsupported neighbors, or if the package needs an unaccounted precision channel
per site. Do not tune more taper lengths or request friction coupons before that
construction can change the architecture decision. Outage arrest and honest
support/readback remain independent obligations.
