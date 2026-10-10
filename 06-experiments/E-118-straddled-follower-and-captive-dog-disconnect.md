---
status: complete
builds-on: [E-117, E-115]
---

# Relocated follower works in section; captive dog cannot independently disconnect

**Keep the permanent straddled power follower as a geometric building block;
reject its closed command fork as an individual jam disconnect.** Separating
the follower from selection removes E-117's permanent-guide contradiction.
It does not remove the need to release a retained dog independently of a stuck
command. Withdrawal also loses the dog's lower guide before clearing its load.
Unequal guide-face friction exposes a wedging mode hidden by a single coefficient.
Stop this embodiment before writer routing, powered-pawl comparison or machine
economics. This is a scoped negative result, not rejection of all dog couplings.

Input main `f8fa8f8`. Reproduce:
`python3 tools/curated-experiment-checks/E-118/dog_disconnect.py`.
Standard-library finite boxes, slot planes, continuous translation events and
quasistatic planar contact calculations. No random seed, sourced process prior,
measurement, dynamics, CAD release or hardware qualification. Dimensions,
friction and stresses are **explicit epistemic scenarios**. Checks are self-review.

## Changed mechanism and checked paths

The power follower is a permanent 2-mm square post spanning z=−2…6 mm,
carried by a translating sled with bearing lands at −1…0 and 4…5 mm. Its
cam contact occupies z=1.5…2.5. A finite oblique cam slot has planes
`|x+.5y|≤1.9` and y ends −1.5…10.5 mm. Relative cam travel y=0…9 gives
follower travel x=0…−4.5; use the reversed x coordinate s=0…4.5 below.
Both lands remain on either side of the contact for the entire stroke.
Guide common-z bias, independent land offsets and cam-z offset ±.1 mm retain
**1.2 mm separation**. Actual square vertices under independent full-width,
x/y registration and slot-half-width errors ±.1 retain **.075 mm plane margin**.
All coordinates are affine, so endpoint plane checks cover the continuous stroke.
This is a finite section, not a complete sled bearing or cam assembly.

A separate 2×2×8-mm dog at y=7…9 has lower end q. It is guided by sled lands
z=0….8 and 4…4.8, and enters a driven tongue at z=2…2.8. Two finite tongue
walls lie x=t−3…t−1.8 and t+1.8…t+3, y=6.5…9.5. q=−1 engages;
q=3.6 clears. At engagement its load is straddled. At disengagement it remains
in the upper guide and has no intended working load. Unlike E-117, the cam
follower never withdraws; the **separate dog** crosses a load layer.

An integral collar spans x=s±1.5, y=6.2…9.8, z=q+6…q+7. Two fork finger
pairs at y=6.3…6.8 and 9.2…9.7 capture it vertically, avoiding the narrower
shaft. They extend x=−2…6.5 through the working stroke. A command coordinate r
sets the lower/upper collar stops at r+6−.4 and r+7+.4: retained q lies
in r±.4. Prescribing r is an external positive drive boundary; an actual
retention lock, writer and channel routing are not implemented. Even granting
a perfect lock on r, the jam contradiction below remains.

Generated boxes check favorable registered set/reset q=−1↔3.6 and both
working directions. The tongue follows only on wall contact: the nominal .8-mm
side gap means outward motion reaches t=3.7 and return ends at t=.8, rather than
silently recentering at zero. 32/128/512 divisions agree; exact translation
contact events supply the collision witnesses. Unselected q=3.6 clears the
stationary tongue over the full stroke. Insertion tolerance, positive idle
ground keeper, carrier, retained-command proof sequence and physical readback
are **not accepted**. Work stops on the necessary disconnect failure before
those downstream obligations. The model grants favorable alignment and an
immobilized output, rather than presenting abstract support bits as hardware.

## Two distinct disconnect failures

For an intermediate stuck command r=q=1.5, the dog still spans the tongue.
Holding the output stationary gives first common-stroke contact at s=.8 mm;
the dog penetrates its finite load wall by .2 mm at s=1.0. A later position
beyond the wall is unreachable without crossing that collision. An independent
positive lifting tool would hit the upper fork after only .4 mm of dog lift.
It cannot reach the required q≥2.9 including a .1-mm vertical clearance.

Enumerate 128 corners with independent ±.1-mm dog width, tongue half-gap,
tongue x/z datum, retained-command position, upper fork face and collar-height
errors. Every case has first stroke contact at **.55…1.05 mm**, and the existing
fork obstructs extraction **.6…1.4 mm short** of clearance. These expressions
are affine in these errors, so their extrema also enclose the continuous box.
Absolute common translation cancels; relative errors can be coherent across a
bank. Counts are uncertainty cases, not fault frequencies or production yield.
Guide play/tilt is omitted from this favorable rigid witness, not qualified away.

Widening the same aperture does not guarantee both functions. At selected
r=−1, full tongue-depth engagement with .1-mm entry reserve requires
`r+gap≤1.9`, hence gap≤2.9. Independent escape with that command frozen needs
`r+gap≥2.9`, hence gap≥3.9. These are incompatible **positive geometric
guarantees without another restraint or force source**. A spring, gravity bias,
load-sensitive latch or separately opening jaw changes the mechanism; it cannot
be silently credited as lost motion. This is not a universal clutch impossibility.

Even after granting removal of the command fork, loaded withdrawal loses the
lower dog land first. There is at least **.9 mm** of full-depth tongue engagement
after lower-land exit in the z-error box. The remaining short upper land carries
opposing reactions; it is not a straddled pair. Nominal contact planes a=4,
b=4.8 and tongue load plane c=2.4 give reaction magnitudes A=3F, B=2F.
With equal Coulomb coefficients mu on tongue and both guide faces, upward pull
is `mu*(F+A+B)=6mu*F`: **4.2F at mu=.7**. Enumerating 32 z corners, two tongue
load planes and five mu values gives 320 scenarios; the maximum is **6.767F**.
The z box includes common guide bias ±.1 and independent guide-face, lower-land
exit and tongue translation ±.1. Monotonic rational expressions enclose the
continuous box. They are not calibrated drag or actuator-force bounds.

Finite-width friction moments matter when surface coefficients differ. Let the
dog width be w, the tongue apply +F at x=−w/2, the lower guide −A at +w/2,
and upper guide +B at −w/2. All axial friction opposes upward withdrawal:

```
A − B = F
B/F = [a−c + (w/2)(mu_t−mu_a)] / [b−a + (w/2)(mu_a−mu_b)]
F_pull/F = mu_t + mu_a*(A/F) + mu_b*(B/F)
```

Force and moment balance reproduce the equal-mu result, the frictionless limit,
and invariance under common translation. With permitted a=4.2,b=4.8,c=1.9,
w=2.1, the denominator vanishes at `mu_b−mu_a=4/7`. The scenario
mu_t=.3, mu_a=0, mu_b=.7 gives denominator −.135 mm and numerator 2.615 mm:
**no upward-sliding equilibrium with these compressive contact signs**.
Ten of 125 independent coefficient cases in {0,.1,.3,.5,.7} reach this failure;
no frequency is implied. At mu_a=.1, mu_b=.67, mu_t=.3, the denominator is
.0015 mm and the model predicts 1,288.9F. That divergence flags an unusable
rigid-contact approximation near wedging, not a credible physical force rating.

This is a planar, zero-clearance edge-contact model. Real clearance/tilt,
contact position, elastic deformation, rounding, roughness and stick-slip can
change the mode; it is **not a certified 3D contact bound**. Equal friction
correlation suppresses this particular divergence; independently varying local
faces admits it. No known manufacturing evidence chooses between those cases.
Hence the modest equal-mu pull estimate cannot release a manufactured design.
Under an additional ideal bending model, w_min=1.9 and lever≤2.3 give capacity
2.485/4.970/9.941 N at assumed allowable stresses 5/10/20 MPa. Bearing pressure,
guide yielding and collar/fork strength are absent; those capacities are not
safe working loads and do not rescue the finite fork obstruction.

## Decision, scope and next discrimination

Retain separation of permanent power follower from command. Stop the closed
capturing fork and short extraction land as a protected selector; do not repeat
its gap sweep or equal-friction estimate. A changed route must open the command
capture **independently of a stuck r**, positively acquire the collar before
release, and guide extraction without the short-land wedging mode. A split cage
with a separate captive retractor and a sleeve spanning the full extraction
path is a specific next topology. Its loaded opening faces, retractor takeover,
stuck-intermediate state and positive reset must be finite, not named actuators.
Preserve command and ground/carrier support through that handover. If those
paths fail, stop that branch and reconsider campaign value before routing work.

This is one coupling topology plus an aperture-widening control, not a new
complete architecture. No selector has passed. LAB-215's full-machine comparison
therefore remains gated. At 6,400 sites this arrangement already adds 6,400
permanent followers, 6,400 dogs with collars and 25,600 guide lands, besides
output supports, command capture, carrier and reader. Collars may be integral;
land count is not purchased-part count. No assembly, complete volume, cost,
<30-s update, disturbance, durability, repairability or production-yield pass
is claimed. Computation has identified the next failure boundary; printing
would not resolve the present geometric obstruction. No fabrication is proposed.
