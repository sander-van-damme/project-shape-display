---
status: complete
builds-on: [E-118, E-115]
---

# Split cage escapes locally; common retractor does not implement mixed reset

**Retain the independently opening cage and long extraction sleeve as local
building blocks. Stop the evaluated synchronous shared-retractor embodiment.**
A narrow common fork cannot acquire unlike command heights. A wide fork *can*
acquire and extract them, so that failure is not universal. However, common
positive return with simultaneous command-jaw closure cannot restore unlike
commands; closing a cage before return instead obstructs entry. Neither variant
is a complete selector. Further dimensional tuning does not resolve the missing
conditional recapture operation.

Input main `2be0701`. Reproduce:
`python3 tools/curated-experiment-checks/E-119/split_cage.py`.
Deterministic standard-library boxes, affine translation paths, contact equilibrium
and interval bounds; no random sampling, sourced priors, hardware measurements,
CAD release or qualification. Dimensions and errors are **epistemic scenarios**,
not calibrated X1C capability. Verification is self-review.

## Changed section and local operating sequence

Retain E-118's permanent power follower separately from selection. Replace the
short dog with a 2-mm-square shaft from z=q to q+17, y=7…9, and integral collar
x=±1.8, y=6.2…9.8, z=q+17…q+18 mm. Two finite sleeve faces have x=−1.6…−1.05
and 1.05…1.6, y=6.8…9.2, z=4…10. The tongue remains z=2…2.8 with load walls
x=−3…−1.8 and 1.8…3. Thus a stalled sled at x=.8 puts the shaft at wall contact.
The sleeve spans the whole **loaded** extraction path: the tongue clears before
the dog tip reaches either sleeve end. This deliberately taller section is not
a pitch/volume or complete-bearing acceptance.

The command cage has two opposed y jaws, each with upper and lower fingers.
Their inner faces are z=r+16.6 and r+18.4, retaining q in r±.4. Each jaw opens
outward in y by 1 mm independently of frozen r. Retractor fingers instead occupy
x=−1.7…−1.3 and 1.3…1.7, y=7.2…8.8; their upper/lower inner faces retain
q in h±g. They open outward in x by 1 mm. Orthogonal jaws leave .4-mm nominal
y separation. At g=.7, a privately registered h axis can:

1. Enclose the collar while the command cage remains closed, then raise the
   lower retractor fingers into contact before release.
2. Open both command jaws without moving r.
3. Raise the retractor; its lower fingers positively lift the collar
   to q=4.3 at h=5. The tip clears the tongue before working motion.
4. With working motion stopped and tongue favorably aligned, lower h until the
   upper fingers positively return q to its original value.
5. Close the command jaws at that value, then withdraw the retractor fingers.

No spring, gravity completion or automatic recentering is used. Contact play is
propagated with q=max(q,h−g) on lift and q=min(q,h+g) on return. Exact registration
of this **private** drive to actual q is granted to isolate common-drive failure;
no physical reader or writer earns credit from it. Generated paths test r=−1,
1.5 (stuck intermediate), 3.6 and q at each cage's two slack endpoints and center.
32/128/512 divisions give the same outcome. Fixed separating planes and affine
contact events certify the ideal continuous translations; sampling is a holdout,
not the only argument. A separate stalled, loaded extraction checks contact at
sled x=.8. Reversing the working motion, actual dog insertion tolerances,
carrier/ground support and retained-command proof remain unaccepted. Opening
loaded horizontal cage faces adds transverse drag mu_j*N for total axial normal
reaction N; geometry supplies no bound on assembly preload or load sharing
during takeover. The path grants sufficient independent drive force and no
preload, not a qualified loaded-jaw actuator. The shared reset exclusion below
persists even under these favorable grants.

Under independent ±.1-mm nearest-face, collar-edge and opening-stroke errors,
open-jaw clearance remains **.1 mm**. A tight retractor's .7-mm half-play merely
covers .4-mm retained slack plus .1-mm q error, .1-mm registration error and
.1-mm inward face error: **zero reserve**. This is sensitivity, not a production
fit pass. Sleeve tilt, straightness, collar/jaw strength, wear and axial drive
mounts remain outside this section. Absolute common translation cancels, while
relative errors can occur coherently across an entire bank.

## Loaded sleeve: changed contact bound

The long sleeve retains the same overhung load topology as E-118 but separates
its two effective edge contacts to a=4, b=10 mm. These are a planar edge-contact
idealization of a clearance guide, not a measured contact distribution. For unit
transverse tongue load at c, dog width w, and independent friction coefficients
mu_t, mu_a, mu_b, moment and force balance give:

```
D = b-a + (w/2)(mu_a-mu_b)
B = [a-c + (w/2)(mu_t-mu_a)] / D
A = 1+B
pull = mu_t + mu_a*A + mu_b*B
```

Use guide-common bias ±.1 plus independent a/b offsets ±.1, tongue planes
2/2.8±.1, w=2±.1 and independent coefficients in [0,.7]. These are explicit
bounds, not sourced material values. Across the **continuous box**, D≥5.065 mm,
the numerator is positive, B≤3.035/5.065 and **pull≤2.23890 times transverse
load**. This loose interval bound permits independently adverse extrema and
therefore need not be attainable. The 8,000 geometry/coefficient corner-grid
checks reach 1.95518F. Equal-coefficient correlation removes friction moments;
independent coefficients are covered by the larger bound. No singularity of
this particular upward-sliding planar mode remains within the box.

Checks reconstruct force/moment balance, common-translation invariance,
zero-friction limit and equal-mu result `2*mu*(b-c)/(b-a)`. The bound excludes
tilting/contact-mode changes, compliance, guide preload, inertia and 3D friction;
it is not an actuator rating or a physical no-jam guarantee. Downward loaded
reset is not qualified. At 80 equally loaded outputs the conditional pull upper
bound sums to 179.12F before carriage friction; correlation prevents treating
rare local resistance as an independent averaging benefit. No F rating is earned.

## Two shared variants and finite exclusions

**Tight common fork, simultaneous opening:** fitting a collar requires
`h in [q_i−g_i, q_i+g_i]`. For q=−1 and 3.6 with g=.7, these intervals are
separated by 3.2 mm. Enumerate common-z bias, independent q offsets and each
fork-gap offset ±.1: the separation is **2.8…3.6 mm** over 32 corners and,
by affine extrema, the full error box. Even two engaged dogs at −1 and stuck
1.5 have **1.1-mm nominal separation**. This failure survives a favorable
assumption of known actual q; unknown cage slack only adds obligations.
A g=2.0, h=1.3 finite finger/collar intersection also witnesses insufficient
aperture; the tighter g=.7 fingers can sit between collars without enclosing
either, so lack of intersection alone is not a takeover certificate.
An equal-command control does fit. Raising the common fork while cages remain
closed does not supply independent takeover: the earlier collar meets its own
upper cage before the other height can be acquired.

**Wide common fork, simultaneous opening/recapture:** g=2.7, h=1.3 encloses both
nominal extreme collars before jaw release. A positive lift to h=7 brings both
to q=4.3. This is a constructive counterexample to rejecting all shared takeover.
The r coordinates may remain independently stored, but the two dog positions
now coincide. A common downward stroke with both cages open keeps them together;
they cannot both lie in disjoint retained intervals [−1.4,−.6] and [3.2,4.0]
when the command jaws close simultaneously.

Closing the low cage first, before descent, does not repair it. Its upper
finger's top is r+18.8; the descending collar bottom is q+17. First contact is
q=r+1.8, hence **q=.8 for r=−1**. A .01-mm further descent intersects the finite
finger, long before q≤r+.4 enters the retaining aperture. With independent
±.1-mm jaw thickness and collar top/bottom errors, the gap between first contact
and possible enclosure is **1.1…1.7 mm** (face translation cancels). This is a
continuous obstruction, not a time-step artifact.

Sequential, per-site cage closure while the common retractor passes each stored
r could escape. It needs a real conditional jaw drive/interlock that acquires
and retains the collar, then permits common travel past already captured dogs.
A release-only wide fork with another reset mechanism could also escape. Neither
is implemented by this synchronous topology. No universal clutch, selector or
shared-energy impossibility is claimed.

## Portfolio disposition and reopening

E-115's crossbolt and powered-pawl support sections survive as references;
E-118's permanent power follower and this local disconnect are useful partial
mechanisms. The explored shared dog route still does not implement selection,
retention through ground proof, local fault recovery and positive mixed reset.
Stop this embodiment before writer routing or full-machine economics. Repeating
fork gaps, sleeve lengths or the equal-friction sweep has low decision value.
The full-machine task has no admitted selector input and should be retired for
this branch. This is an allocation decision after successive finite exclusions,
not evidence that dry supports or all retained-command schemes are impossible.

Reopen only with an executable materially changed conditional acquisition/reset
mechanism, or a complete accessible private/transported drive whose real channels,
travel and repeated burden can be compared with the direct-head reference.
Campaign closure should compare that opportunity with a different architecture
before commissioning another dog refinement. No requirement changes are implied.

At 6,400 sites the section already repeats 6,400 dogs/collars, 12,800 opening
command jaws and 6,400 sleeves, besides permanent followers, retained-r storage,
ground supports and carrier/reader. A permanently replicated split retractor
adds another 12,800 jaws; a transported retractor trades those for acquisition,
registration, travel and sequential recovery. A two-jaw cage is an assembly
burden even if both jaws share a drive. No bought-cost, print/assembly, full-board
<30-s, regional disturbance, false-acceptance, fatigue, creep or reliability pass
is established. Printing cannot repair these sequencing omissions and is not
proposed. No hardware qualification is claimed.
