---
status: complete
builds-on: [E-213, E-212, E-211, E-124, E-125, E-054, E-056, E-209]
---

# Moving guidance into the writer does not remove the resident moment path

**Stop both tested embodiments; retain pose-seeking guidance and transverse
float as component ideas. Redirect from remote tail capture to co-located ground
support, release and writer takeover.** Resident guides amplify their play at the
remote pin. A floating pin removes that particular interference in prescribed
poses, but its retained slide hits manufactured stock, adds outputs and takes
both signs of axial load. More fundamentally, removing the reusable guide at
completion leaves the inherited toe unable to balance a tail-centered load.
Neither alternative establishes the requested complete supported transaction.
Do not retune the miniature rail/window or request fabrication.

Input main `651b97c`. Reproduce with NumPy:

```
OPENBLAS_NUM_THREADS=1 python tools/curated-experiment-checks/E-214/compare.py
```

Evidence: generated convex prisms, exact translational swept volumes, finite
contact geometry, necessary reaction cones and deterministic bounds. Prescribed
contact-seeking output positions are not constructed actuators or sensors.
No physical measurements, manufacturing priors, priced BOM, dynamic simulation,
independent review or machine qualification. JSON output is disposable.

## Reconstructed controls

E-124/E-125's bilateral cup is not new: 5.002082-mm retained housing at
5.08-mm spacing leaves .077918 mm, consumed by opposite .046667-mm head
translations before rotation. At sparse spacing, loaded overlap
`.2−sqrt(2)*.125=.023223 mm` is less than .025-mm foot-face error, causing
side contact. E-125 retains the finite collision and coupled-contact evidence.
Source imports preserve E-212's jaw collision at 1.099/1.101-mm lift and E-213's
nine passive guide/pin failures. No depth staggering is credited here.
E-054's .4-mm wall/.8-mm shelf gives 5.00-mm width and favorable 5.859-MPa
strip demand at 10 N, not strength acceptance. E-056 retains zero guaranteed
pitch margin under arbitrary edge pressure. Pawl guidance is not column guidance.

## Two causal architectures, with the resident release explicitly retained

Both use the E-213 76-mm tail, 40-mm travel plus 1.5-mm unload, positive short
cross-pin, single-depth sparse heads, independently supported unchanged cells,
and E-211 uncut rocking toe with widened seats. Service force passes from rack
tooth to toe pad, heel/front ledges and grounded frame; the return does not
carry tabletop load. Height power requires a carrier-grounded vertical drive
and arrest. These drives/arrests are counted obligations, not built hardware.

| Function | A: load-centered axial writer, resident guidance | B: reusable pose-seeking guidance, floating pin |
|---|---|---|
| Selection/access | Shared carriage indexes below selected tail; pin inserts along x | Same axial route; open guide approaches before pads close |
| Height force | Floor carries downward load; pin carries opposite signed load | Floor removed to avoid another fixed pose constraint; pin carries **both** signs |
| Moment during writing | Two resident E-212 guide stations at z=8/20, ten bearing faces/cell | Eight independently advancing pads at local z=6/18, contacting actual shaft extremities |
| Capture fit | Fixed pin; guide play must fit the remote eye | Pin bearing rides a retained y slide; x plunge supplies insertion, with declared x/z carriage play |
| Resident release | Four E-211 shoes; independent y/z/pitch pose plus x insertion | Identical explicit release assembly; float does not release the toe |
| Completion | Re-establish toe support, verify rack and unload head before departing | Same, but **grounded moment support after guide departure is missing** |

The explicit release tool reproduces E-211's four finite shoe envelopes,
.5-mm span, .4×.12-mm stem and nominal y/z expansions .2/.3 mm. It retains
four unresolved internal drives plus y/z/pitch positioning and x insertion;
no frictional grip or free resident release is added. E-211 remains authoritative
for pocket acquisition and the bowed released-pose sequence, not re-solved here.
The new upper guides and full lower-head travel envelope clear this tool during
.22-rad rocking/1.2-mm withdrawal at 16/32/64 subdivisions. This is new-interface
access clearance, not a repaired release drive or complete uncertainty stack.
Its E-209/E-211 force and section limits remain below.

## A — real resident guide contacts amplify at the remote eye

The web is .5 mm thick in y. Let c be remaining guide center half-play after
form/alignment, not a specified hole tolerance. Opposite finite-band contacts
at z=7.5 and 20.5 obey

`13 tan(theta) + .5/cos(theta) = .5 + 2c`.

Generate the rotated web against the actual E-212 guide solids and verify no
penetration. At tail pin global z=−74+h, relative to guide midpoint z=14,
its center excursion is `(h−88) tan(theta)`. Load-centered axial forcing avoids
a nominal writer moment but does not erase manufactured pose or seated play.

| c (mm) | Pin offset magnitude at h=0 / 20 / 40 (mm) | Full pin section fits nominal window at those heights |
|---:|---|---|
| .005 | .06769 / .05231 / .03692 | yes / yes / yes |
| .025 | .33844 / .26152 / .18460 | no / no / yes |
| .075 | 1.01516 / .78444 / .55372 | no / no / no |
| .150 | 2.02987 / 1.56854 / 1.10720 | no / no / no |

The last row can miss the tail entirely: inverse-transformed window containment
is tested as well as collision. Zero collision is not capture. These are rigid
guide-admitted poses, not loaded equilibria. Full tilted rack/frame/top clearance
is unproven; earlier contact elsewhere would add another reaction interface.

The .20-mm transverse gap less .05 registration, .05 window-size and .02
pin-size bounds leaves .08 mm. At h=0, `theta<=atan(.08/88)` requires
**c<=.005909 mm**; angular eye effects can tighten it. This is a residual
precision requirement, not a measured X1C floor. Correlated alignment does not
average away. Stop this remote fixed-pin embodiment at the declared bounds.

## B — manufactured pose acquisition, actual slide retention and its limit

Open head: 4.9-mm outer envelope, 3.3-mm aperture, four posts and bridges.
Eight pads independently advance to actual rotated-shaft extrema clipped to
finite 1-mm bands. These oracle contact targets do not grant centering, sensing,
force-limited drives or arrest; those remain implementation obligations.

The hollow pin bearing at x=1.05…1.85 has flanges at x=.95…1.95. Connected
rails begin at x=.85 and retain y=±.75, x=±.05, z=±.10-mm travel/play. Solids
just beyond each limit hit a stop. Flanges are .3 mm thick; x keeper lips are
.05 mm. These are constructed retention geometry, not qualified printable or
load-bearing parts. No frictional height lock is credited.

At each pitch bound ±.005/.010/.020 rad, enumerate 64 corners: pitch sign,
tail half-size ±.05, x/y placement ±.05, slide z play ±.10 and x play ±.05.
The tail bottom defines an oracle z datum; no floor support or real readback is
granted. The pin seeks the transformed eye.
Required y float reaches **.05998/.06993/.08971 mm** respectively. Pin insertion
and carriage bodies clear in all these prescribed corners. Unlike E-213's
passive guide, contacting pads do not allow the later free take-up assumed there.

But **16/64 cases at each angle fail acquisition and final shaft clearance**.
The +.05 size/+.05 x-placement corner reaches x=.90; the rail starts at .85:
actual bottom-bridge intersection is .05 mm. The acquisition sweep includes
rails, not just the aperture. Pin clearance in a collided head is diagnostic.
Moving the rail would not repair departure, release or output burden; stop
miniature-section refinement here.

Without the floor, the .6-mm pin carries both axial signs. E-213's favorable
1.05-mm cantilever arm demands **291.67 MPa at 10 N**, versus A's nominal
3.906-MPa full-area floor pressure; neither is an allowable. A floating floor
would require another generated path. Assumed slide friction mu=0/.1/.3 at
10 N gives transverse resistance 0/1/3 N and 0/12/36 N·mm at a 12-mm arm.
A sliding interface therefore need not decouple force. These are bounds,
not calibrated friction or solved reactions.

## Departure is the stronger architectural discriminator

The inherited rack/toe vertical bearing spans y=.8…1.2. Toe keys and ledges
restrain the **toe**, not the column above it. Give the entire bearing its most
favorable arbitrary nonnegative endpoint pressure. For downward F at yL and a
horizontal load H at a 40-mm scenario arm, moment balance requires

`Rright = [F(yL−.8)+40H]/.4; Rleft=F−Rright`.

At the tail-centered yL=1.95, F=10, H=0 this demands **28.75 N and −18.75 N**.
A negative unilateral reaction is impossible. Even placing all vertical force
at the front edge leaves **7.5 N·mm** without a resident moment path. This is
an exact necessary-condition failure of that load-path combination; changing
pin fit, guide pad count or material cannot repair it.

The favorable yL=1/H=0 case admits 5/5 N; yL=.8 or 1.2 has zero adverse
pitch reserve. H/F=±.005 at a 40-mm scenario arm shifts the resultant .2 mm.
For H≠0 the model generously grants another horizontal reaction; it too needs
construction. These are scenarios, not new product requirements.
B must add a resident reaction pair, spread its ground capture, or justify a
restricted load envelope. Adding A's guides restores its repeated burden.
Neither changing pin fit nor material repairs the negative-reaction witness.

## Reach, proof, unchanged neighbors and full-board accounting

The inherited nominal short-pin construction still clears all twenty unequal
five-height transitions and exact intermediate vertical sweeps across 40 mm.
New head/frame and unchanged-neighbor shaft unions also clear nominal translation.
Service heights remain the inherited indexed rack positions; no continuous-height
lock or new terrain resolution is claimed. Manufactured acquisition failures
prevent extending the nominal reach result into a working uncertain transaction.

The executable sequence requires acquisition/proof before unloading and releasing
the toe, resident reseating/proof before head departure, and unchanged-neighbor
support. These are actual-support flags, not sensors. False resident acceptance
explicitly permits unsupported departure. Failed proof retains the head and stops
the module; power loss still requires a constructed axis arrest. Nominal pin
lost motion .4 mm plus slide range .2 mm prevents borrowing E-213's .04-mm proof
stroke without a new model. Expected missed supports would be 6,400p for false
acceptance probability p, without independence; p is unbounded. No vibration or
regional-disturbance qualification follows.

| Obligation | A | B |
|---|---|---|
| Common residents | 6,400 toes, returns, pockets and tail windows; 12,800 keyed seat interfaces; assumed 160 comb placements | same |
| Resident column guidance | 12,800 station fits / 64,000 bearing faces; 6,400 spines | absent after departure; cannot be silently credited |
| Active guided outputs at H=40/80/160 | 400 / 800 / 1,600 | 720 / 1,440 / 2,880 |
| Additional passive retained slides | none beyond inherited axes | 40 / 80 / 160 transverse carriages |
| Counting basis per head | height + pin + four release shoes + release y/z/pitch/insertion = 10 | same 10 + eight contact-seeking pads = 18 |
| Added modeled material | resident guides 117.504 cm³/board | head frame/rail 62.478 mm³ and carriage 2.24 mm³/head, before drives |

Both retain E-213's ~547.94 cm³ tail stock. Ten-second cell inspections would
total 17.78 h (assumption). Print time/scrap are unestimated; integrated printing
does not remove fits. Modules remain necessary for the 256-mm bed.
Independent head phases collide at 5.08-mm x spacing and clear at 10.16 mm:
H=40/80/160 needs 1/2/4 rows of 40 heads before drives/cables. B's 4.9-mm y
envelope leaves .13 mm at adverse 5.03-mm row pitch. No motor packing pass.
Aligned 10-N loads give 400/800/1,600-N frame reactions. A removed sleeve might
permit a faster route; the common 20-mm park below is constructed for comparison,
not a necessary lower bound for every resident-guide architecture.

With six seconds map overhead, strict slots are .15/.30/.60 s. Use E-213's
constructed safe park: approach 20+old height, two 1.5-mm unload/reseat moves,
height change, departure 20+new height and two 1.7-mm pin strokes. Rest-to-rest
triangular motion at a=1,000/5,000/20,000 mm/s² takes 1.50256/.67197/.33598 s at
the worst 10→40 or 40→10 pair. Add .08/.16/.32 s for release, guide closure,
registration, settling, proof and bounded retry: **0/9, 0/9, 2/9** scenarios fit
H=40/80/160. No velocity limit is favorable. B has more operations within the
same assumed allowance; it earns no performance credit from this table.

Purchased-cost requirement remains `Cshared+H*chead+6400*ccell < $500`.
With $250 elsewhere, head allocations are <$6.25/$3.125/$1.5625, including all
release, guide, drive, arrest and readback functions. Resident purchases at
$.01/.02/.04 per cell consume $64/$128/$256; the last exceeds the residual
before any heads. At the $400 band only $150 remains; $250 shared already misses
the ideal <$200 band. These are allocations, **not quotations or cost rejection
of an entire mechanism family**. Shared power/sensing is not uncounted hardware.

Where the rocking return remains, E-209 still contributes **2.247/3.188%** strain
in nominal/short-thick root-error scenarios, **3.44/4.31%** at the tensile edge,
and force tails **7.56/14.80 N**. E-211's 302-MPa nominal thin-stem demand and
1,420/4,119-MPa stock/root holdouts remain model demands. Neither new rack capture
changes them. No tensile bias, free release force or qualified metal replacement.

## Evidence limits and next decision

All fit/pose/friction/force cases are assumed bounds, not priors or iid yield.
Bank registration, stock bias, warp and shared-head calibration can be common
cause. Hole shrink, layers/first layer, roughness, anisotropy, creep, wear,
fatigue, elasticity and frame dynamics remain uncertainty. Geometry and reaction
signs stop these embodiments before material refinement is useful.
Self-review checks inverse containment versus missed capture, finite guide
contact, independent enclosure algebra, stop overshoots, exact affine sweeps,
force/moment residuals, inherited failures and release subdivision. No whole
loaded transfer certificate or independent validation is claimed.

**Next:** co-locate resident support, release and writer takeover; retain moment
reaction after departure without the long remote eye. Compare an explicit
E-054/E-056 guided slider with a changed coarse release/support topology. Count
resident fits and every head output; stop on hidden column guides, unsupported
departure or recreated tiny grippers before optimizing material/timing. Reopen
axial float only if a changed ground interface removes the release penalty and
supplies a finite departure certificate. No new physics or saturation claim.
