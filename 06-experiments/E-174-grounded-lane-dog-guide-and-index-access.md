---
status: complete
builds-on: [E-173, E-054, E-056, E-096]
---

# Clearance indexing loses the lane state; guide and writer grants remain

**Reject the tested clearance-peg embodiment.** Even granting perfect dog
guidance, an inserted index peg permits a .44-mm drift that catches the next
tooth **10.1 mm too high**. Remote amplification reduces index error only with
a sufficiently constrained output connection; a clearance diagonal follower
restores the lost motion. A finite lower guide permits nose/spine interference,
but tilted-contact equilibrium prevents claiming this is inevitable under load.
The same guide blocks straight underside access to the neighboring pickup.
These are bounded failures and unresolved constraints, not a rejection of spatial
tooth addressing or all positive locks. Stop at the assigned retention rejection
gate; no full-machine CAD, printing or purchase.

Input main `1c0a7aa`, E-173; LAB-284. Reproduce:
`python3 tools/curated-experiment-checks/E-174/retention.py`.
Evidence: finite rigid polygons/boxes, unilateral frictionless load scenario,
interval calculations and inherited conditional scheduling; self-review only.
No process calibration, compliant/contact dynamics, physical measurements,
strength/yield/reliability estimate or assembled-machine witness. JSON is
reproducible output and is not retained.
The stage-02 X1C/PLA/.4-mm-nozzle process does not qualify these .3–.5-mm
features. Datum/edge bounds are explicit scenarios; shrinkage, first-layer
effects, layer quantization, warp and bank deformation need additional error
allocation, not an assumed independent-cell distribution.

## Grounded guide: translation clearance is insufficient

Coordinates are E-173's X/Y/Z, mm. Generate a connected moving union: nose
X=1.2…2.65, Z=−1…0, Y=q±.25; tail X=2.05…2.65, Z=−H…−.8,
Y=q±.5; carriage X=2.05…2.05+L, Z=−H…−H+1, Y=q±.5.
H=5, L=1.8; q is one of five centers −1.8…1.8. The nose retains the original
rack overlap. Grounded rigid floor at Z=−5 covers X=2.05…3.85; the roof's
underside is Z=−3.8 and covers X=2.85…3.85. Both span Y=±2.3;
roof thickness .4. Their ground attachments and stiffness are favorable grants,
not newly designed frame members. The clearance index below is a separate
sectional falsifier, not an assembled addition that secretly braces this guide.

Initially, own teeth clear these rails by .25 in X; the neighboring column
spine starts at X=4.48, leaving .63 beyond the carriage. Nose-to-neighbor-pad
gap is .23; roof-to-home-pad vertical gap .40. With the inherited four-term
±e edge/datum accounting, e=.05 leaves .05/.43/.03/.20 respectively.
The wider tail remains within Y=±2.3 throughout all lane settings. Thus nominal
translation packaging is possible, albeit with tiny margins and unqualified
features. The actual loaded attitude is the discriminator.

Every nominal tooth pressure centroid x∈[1.2,1.8] lies left of the floor edge
2.05. Under a strictly vertical dog load a flat lower-floor resultant cannot
lie beneath it. **That does not prove continued tipping:** actual contact on a
tilted face introduces horizontal force. First bound the permitted attitude,
then reconstruct that contact instead of carrying over a vertical force arrow.

Grant X registration of the inner bottom corner. This is a favorable boundary;
the two horizontal shelves alone do not construct its lateral restraint. The
outer upper carriage corner reaches the roof at pitch angle theta satisfying
`L sin(theta) + cos(theta) = 1 + c`, where c is slot excess height. The nose's
inner upper corner becomes `X = 2.05 − .85 cos(theta) − H sin(theta)`.
Transformed polygons and a separating-axis collision test independently check
these limits. Their Y intervals overlap, so the sectional intersection is real.

| Scenario, H=5/L=1.8 | Roof-contact angle | Minimum nose X there | Angular-play limit |
|---|---:|---:|---|
| Nominal c=.20 | 6.591° | .63170 | Only .03170 to spine X=.6 |
| Adverse c=.40 | 13.781° | .03339 | Spine intervenes at 6.965° |

The adverse corner moves the floor downward .10 and roof upward .10 (each is
one ±.05 datum plus one ±.05 face); moving parts otherwise keep nominal shape.
This is a simultaneous legal bound, not a distribution. The floor shift merely
translates the pivot vertically; the spine spans this region. At first spine
contact the roof is still **.18912 mm** clear. The extrapolated roof pose cannot
be reached without penetration. A finite nose .001 rad past first contact
intersects the spine. This is an **admissible angular-interference witness**,
not a simulated trajectory or a proof of jamming under vertical column load.

Reconstruct frictionless contact: the horizontal tooth's right underside
corner at X=1.8 bears against the inclined dog top. For vertical force component
F, force on the dog is `(F tan(theta), −F)`. Taking moments about the granted
registered bottom corner gives equilibrium when
`2.05−1.8 = H sin(theta)`. At H=5 this gives **2.866°**, horizontal reaction
**.05006 F**, and minimum nose X **.95106**: it clears the spine and has not
reached the roof. The executable check transforms the actual dog solids there
and verifies the moment residual. Thus the vertical-force-only tipping inference
would reject too much. No actual X bearing or compliant acquisition is supplied,
so this equilibrium is also **not a guide qualification**.

For comparison, a strictly vertical pressure resultant at the nominal roof
contact would need upward floor reaction 1.149–1.508 F and downward roof
reaction .149–.508 F across x∈[1.2,1.8]. These hypothetical reactions are
nonnegative; they are not the tilted-face normal solution. Loads .1/1/10 N
scale forces without changing these rigid conditions. Friction, imposed side
loads, X restraint, perturbations, guide stiffness and pressure distribution
can change the reachable attitude; no calibrated law or probability is claimed.

Sixteen L=1.2/1.4/1.6/1.8, H=5/6/8/10 holdouts all permit spine interference
before the c=.40 roof limit (some short carriages also miss its X extent).
Shorter L increases the limiting angle and longer H increases nose excursion,
so the best envelope endpoint bounds this continuous parameter box. Confining
**all** such angular play before nominal-spine contact at H=5/c=.40 needs
L≥**3.35970 mm**. Simple lengthening intersects a low neighboring spine by
**.92970 mm³** in its unrotated pose. This is a geometric confinement bound,
not a necessary bearing length for the conditional normal-force equilibrium.
Do not refine this guide before solving the decisive index failure below.

## Five-state index: an engaged peg is not a retained lane

For an independent, deliberately favorable test, grant perfect dog guidance and
a vertically held index peg; no free physical keeper is claimed. Fixed comb
slots have .9-mm pitch and width w; moving peg breadth b=.3. Comb and peg
have independent ±e datums and each facing edge ±e. Slot positions share the
comb datum, permitting coherent bank bias. Require .05 insertion reserve.
With d=(w−b)/2, insertion needs `d≥4e+.05`; a retained peg may then travel
`d+4e` from its commanded coordinate. The comb web is `.9−w−2e`.
At e=.05, minimum w=.8 leaves **zero guaranteed web** and allows **.45 mm**
positive coordinate loss. Enlarging the clearance cannot fix retention.
This is the E-096 insertion/backlash conflict applied to E-173's five lanes,
not a newly discovered general lock principle.

The executable witness preserves real webs: target slot Y=[−.4,.5], peg
Y=[q−.15,q+.05], with adjacent slots recessed so minimum web remains .1.
The peg occupies X=3…3.5, Z=−8.2…−7.3; comb spans X=2.8…3.8,
Z=−8…−7.5. It lifts 1 mm, translates, then re-enters: all 25 old/new pairs
pass 2,675 box poses. Entire translation sweeps are above the comb; entry and
withdrawal stay within each aperture, establishing continuous clearance.
The assumed vertical keeper, writer capture and attachment to the dog remain
grants used only to make this rejection stronger.

With the peg still inserted, q=.44 remains collision-free; q=.46 hits a web.
At q=.44, E-173's actual dog overlaps the next tooth by .04 mm, captures
h=30.3 instead of 20.2, and incurs **.00120 mm³** tooth/dog intersection if
lowered .05 beyond that contact. No extra tooth errors are needed. An engaged
peg or a support-only reader can accept this wrong state. Reading lane only
before an external disturbance also misses later drift. Direct retained-lane
and height proof must control pad clearance; no false-accept probability is known.

Compare remote state r=Aq with .9A-mm index pitch. An exact, backlash-free
transmission reduces this .45-mm loss to .45/A. A physical diagonal slot
`q=r/A` instead adds its own normal clearance, projected by
`sqrt(1+1/A²)` onto Y. Giving that follower the same .05-mm error/insertion
box yields the following **bounds**, not a constructed remote mechanism:

| A | Remote stroke mm | Exact-link loss mm | With clearance follower mm |
|---:|---:|---:|---:|
| 2 | 7.2 | .22500 | .72812 |
| 4 | 14.4 | .11250 | .57635 |
| 8 | 28.8 | .05625 | .50975 |

The follower contribution tends to .45 even as A increases without bound.
Independent error signs can align; neither averaging across cells nor a common
bank reader removes this possible bias. These values already exceed E-173's
.20-mm residual wrong-lane gap before retaining a positive reserve. An exact
A4 link would leave .0875 of that gap; it is a useful **escape condition**, not
an available link. A preload/wedge/flexure can change this model and must supply
its force, stroke, creep and packaging evidence. No claim excludes those routes.

For a hypothetical spring-return peg, axial extraction must overcome keeper
preload plus side-contact friction: `P+mu*|Yload|`. Explicit P=.05 N,
mu=.1/.3/.6 and |Yload|/F=0/.1/.3 at F=.1/1/10 N give .05–1.85 N.
These are sensitivity inputs, not a spring design or sourced material values.
Unload before changing q; E-173's top stroke provides ≥3.85 mm tooth clearance
only under its original upright-dog assumptions. The missing lateral restraint and
retained coordinate prevent inheriting that cycle as an assembled witness.

## Access, complete-machine comparison and stopping decision

The previous X neighbor's guide roof occupies X=−2.23…−1.23 directly below
this cell's home pad. A nominal underside writer prism X=−2.15…−1.35,
Y=±.35, Z=−4.2…−3 intersects it by **.224 mm³**, both for active and clear
pad positions. The .40-mm nominal gap shrinks to .20 under the same bound;
a .40-mm finger cannot be inserted through that gap. This rejects straight
underside capture in the proposed packaging, not all shared writers. Side entry,
ports through rails or remote tongues would be changed geometry. Their capture,
withdrawal, neighbor clearance and assembly access are not demonstrated.

Do not replace the missing writer by an inventory claim. E-173's 328 B4 shared
bundles still grant 320 complete independent setting/readback channels, four
row drives and four deck drives. A proposed bank-wide X/Z access carriage adds
eight axes, giving **336 bundles**, but supplies neither the obstructed pad
port nor a demonstrated selective peg-release mechanism. Independent pad/dog
heads need **652 bundles**: 640 setting channels, eight row drives, four decks.
Separate-contact B8 is 656 and direct-head B4 is 324 richer bundles. An index
head needs capture, release, five-position motion, reseat, actual readback and
withdrawal; those functions cannot be silently counted as one cheap motor.
At $500 ceiling/$250 reserve/free bought sites, 336 bundles permit <$0.74405
each, split 652 <$0.38344. Sensors, keepers and bank brakes are still unpriced.

E-173's complete successful-map allocation remains conditional: B4 word slots
.5/.8/1 s give **22.919/29.219/33.419 s**, versus separate B8 **23.247 s**
and direct B4 **19.469 s**. As an explicitly favorable access-time sensitivity,
two bank-wide round trips 43 mm below the spine plus 5.08-mm X transfer add
**1.1475 s** at 200 mm/s, 5,000 mm/s²; B4/.5 becomes **24.066 s**.
This is not a collision-free route or a completion prediction. It excludes any
new per-row peg/fork dwell beyond the word slot. At .8 s this allowance already
exceeds 30 s. Extra axes alone do not necessarily destroy timing or bundle
advantage; the missing physical port/retention is the decisive evidence here.

Both selectors remain repeated 6,400 times. Unchanged cells must retain loaded
dogs while selected dogs are rewritten; a common release of all row locks is
not local isolation. E-173's pickup pad, late-fault recovery and shared input-loss
arrest obligations remain: an engaged lane peg cannot support an airborne
bank. At B4 the inherited .1/1/10-N scenarios require 160/1,600/16,000-N
bank arrest plus deck weight. No brake, readback error bound or recovery of a
persistent wrong-height capture was created. No favorable timing claims cover
these fault cases, assembly labor, inaccessible repair or structural qualification.

Self-review checks polygon limiting cases, analytic/corner-angle agreement,
force/moment residuals, all five index states/transitions, concrete retained
wrong-tooth contact, opposite retained-web contact and neighboring writer solid
intersection. Seventy bisection steps resolve continuous angle roots; there is
no time integration or mesh-convergence claim. Static existence is not hardware
reliability. Stop detailed work on this clearance-peg embodiment; the guide
remains conditional. Reopening requires
a changed finite constraint/load path that preserves lane accuracy after writer
withdrawal **and** a real shared pickup/dog access route; another exact-link
amplification or nominal-box replay is insufficient. Next compare such a changed
constraint against a support-selection topology that removes this narrow retained
coordinate, keeping direct/separate controls; no architecture is selected.
