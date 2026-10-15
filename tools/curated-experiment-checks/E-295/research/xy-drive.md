# Underside XY screw driver: few resident features, measured docking still needed

**Recommendation:** retain a single underside rotary head as the lowest-repetition
baseline and the first selectable-drive experiment. Use a positive axial socket
integral to each screw, a captive thrust collar, and simple square pin guidance.
Put compliance, phase finding and controlled engagement in the reusable head. A
four-spindle carriage can increase useful local throughput later; one head is not
a fast full-board scene writer. This is a conditional architecture recommendation,
not a demonstrated mechanism or an instruction to build a full gantry now.

**Evidence:** repository inspection; manufacturer documentation fetched on
2026-10-15; ideal coupling calculations and finite polygon checks; independent
review by the critical-review subagent. No new motor torque, engagement time,
friction, endurance or physical neighbor-isolation measurements exist. The
companion manual demonstrator supplies the concrete small test; its actual CAD
and print instructions govern fabrication.

## What the existing evidence does and does not say

- The completed `short-thread-fit` pairs all moved both ways five times by hand;
  the 0.20-mm radial clearance felt best in those **10.3-mm-wide** nuts. That is
  evidence for thread motion, not the torque/rpm of a compact guided array.
- The owner recalls successful 4.4-mm Trial 5 hollow pins. The support-filled
  replica did not test their thread fit. Neither observation proves an automatic
  coupling, but neither supports declaring the screw principle unsuitable.
- [E-272](../../../../06-experiments/E-272-spaced-direct-spindle-architecture-comparison.md) already
  describes underside direct spindles at 25.4-mm spacing and warns about narrow
  motor packing. Its 0.08-s engagement and 850-rpm operation were assumptions.
  Its optical obligations are not prerequisites for this mechanical test.
- [A-007](../../../../04-architecture-candidates/A-007-scanning-screw-column-matrix.md)
  rejected an earlier dense-update performance model. The present owner request
  explicitly reopens screw actuation, permits slower preparation and prioritizes
  independent motion. Preserve that historical result within its assumptions;
  do not apply its 50-ms full-cycle requirement to every useful local update.

## 1. Complete torque and support paths

With a fixed screw and a nonrotating internally threaded pin, a right/left motor
command produces opposite vertical motion. Software records the assembly's
actual handedness and first verifies the sign by hand.

**Torque:** motor → short compliant coupling → metal hex tip → socket in screw
collar → screw thread → pin's short internal nut. Two spaced square guide regions
react the pin's torque into the common frame. Support from adjacent pins alone
would make isolation depend on friction and neighboring heights; use fixed guides
for this discriminator.

**Gravity/load:** pin → engaged threads → screw → lower thrust face → frame.
**Underside engagement or upward screw force:** screw collar → upper keeper face
→ frame. Both reactions must exist with the head removed. A socket alone is not
a thrust bearing; the motor must not become the only pin support. Plain printed
thrust faces in a common plate are a legitimate first test, with friction and
wear still unmeasured. No individual rolling bearing or resident clutch is
required by this construction.

A nominal 3.6-mm collar in a 3.9-mm captive chamber has 0.3 mm axial float.
Approaching from below can lift the screw and its pin by that amount before
rotation starts. Record this separately from thread backlash or neighbor motion.
The first fixture accepts this visible error; reducing it later is a support
tolerance decision, not a reason to add sensors now.

The pin remains threaded over the full commanded stroke. End of travel must leave
thread engagement and guide overlap. Driving a nut off the screw or hard into a
closed pin roof is not acceptable homing.

## 2. Why drive from below

| Head location | Actual consequence at a 5.08-mm pin pitch | Disposition |
|---|---|---|
| Below stationary screw ends | A constant docking plane; terrain height does not change access; tops stay square and closed; miniatures can remain above | Preferred. Allow a roughly 70–110-mm head/slide service envelope under the support, plus frame/gantry; exact stack remains a layout task. |
| Above screw through the moving pin | Requires a through-hole in each top and a long thin tool entering varying depths; closed square tops obstruct the screw; tall neighboring terrain/props constrain routing | Poor default for this product. A removable top and through access could work, but adds a new repeated feature and interferes with play. |
| Turn the pin from above | Violates the specified nonrotating guided pin and disturbs the terrain surface | Excluded. |
| Edge drive routed through rows | May reduce under-board carriage travel but needs a separate selectable path to each screw | Belongs to shared-drive candidates; it does not remove selection. |

Only the slim tip enters the plane of the screw ends. Motor, chuck, spring housing
and cabling stay below **all** lowest screw/frame surfaces, including during
approach and retraction. A large ordinary screwdriver bit holder is therefore
permitted below the array; its diameter is not required to fit one pin cell.

Thin wall elements above the pin surface do not intersect this head. Their mounts
must avoid attaching a descending pin to a fixed wall or spanning two independently
moving pins. No additional wall mechanism is needed to establish underside access.

## 3. A concrete positive coupling

Proposed demonstrator interface, developed with the demonstration subagent:

| Feature | Nominal geometry | Reason and limitation |
|---|---:|---|
| Integral screw collar | Diameter 4.4 mm, thickness 3.6 mm | Leaves 0.68 mm between nominal collars; avoids a separately assembled driver on every screw. |
| Female hex socket | 2.2 mm across flats, 2.0 mm straight depth | Accepts an existing 2.0-mm metal hex tool; side allowance is 0.10 mm before printer errors. |
| Socket entry | 0.4-mm-deep 45° expansion to 3.0 mm across flats | A lead-in for centering, with only 0.468 mm minimum radial wall at the mouth's corners. This is not a strength-qualified edge. |
| Socket roof | 1.2 mm above the 2.4-mm total recess | Short bridge over a 2.54-mm corner-to-corner throat when printed collar-down; slicer verification belongs to the actual print package. |
| Journal above collar | Diameter 3.2 mm in nominal 3.5-mm common-plate hole | Defines screw location separately from the socket; 0.15-mm radial journal play is part of the position stack. |
| Lower keeper access | Diameter 3.6 mm through the 1.2-mm-thick base floor | Exposes the socket entry and leaves a nominal 0.4-mm radial shelf under the collar. |
| Square pin guidance | 4.60-mm openings for 4.4-mm pins, guide planes 10.2 mm apart | Fixed guides provide antirotation; thin guide webs and tilted-pin friction remain physical checks. |
| Driver | Metal hex, 2.0 mm across flats | Positive rotation both ways; a printed hand tip is a low-force assembly aid, not a qualified production wear surface. |
| Reusable head | Axial spring travel and about ±0.2–0.3-mm lateral float | Compliance reduces jamming after capture. It cannot find a mouth that the tip misses. |

Reproduce the coupling calculations with
`python3 tools/curated-experiment-checks/E-295/research/xy_geometry.py`.
The independent reviewer challenged the mouth, keeper shelf, accumulated position
error and passive hold; those objections are retained below.

The tip's corner radius is `2/sqrt(3) = 1.1547 mm`. At 0.20-mm lateral error,
nominal clearance to the neighboring 4.4-mm collar is
`5.08 − 2.2 − 1.1547 − 0.20 = 1.5253 mm`. This is a **tip-to-neighbor** clearance,
not permission for a 6-mm chuck to enter that plane, and not a proof that the
shared frame is stiff. A tip located over the correct screw does not touch any
other socket; no mechanical selection state is needed at untouched screws.

The 3.0-mm-AF entry hex conservatively accepts all tip phases only within a
`1.5 − 1.1547 = 0.3453 mm` center-offset radius at its mouth. The straight throat
has just 0.10-mm centered side allowance. Thus rigid ±0.2-mm positioning will
**not** guarantee full engagement. The head must first capture the mouth, then
center through the taper. Plate bow, journal play, thermal growth, tip runout and
gantry error enter this same budget. For example, two separately printed grids
do not gain accurate alignment merely from nominally identical 5.08-mm pitches.
A shallow local search after failed seating is possible with the reusable head;
its cost belongs in measured docking time.

The lower retaining plate also matters: the mouth's corner diameter is 3.464 mm.
The demonstrator's 3.6-mm circular access hole exposes it but leaves only a
0.4-mm nominal radial thrust shelf under a 4.4-mm collar, in a 1.2-mm-thick common
base floor. Its loaded deflection and rubbing are unproven. Making the hole smaller
increases bearing area but reduces angular/lateral entry access. The manual
fixture can accept deliberate alignment; automatic mouth capture cannot be
claimed from that alone. The 0.15-mm journal radial allowance also permits collar
eccentricity, reducing that nominal shelf locally to 0.25 mm before print errors.

### Engagement phase is a separate operation

A centered 2.0-mm hex in a 2.2-mm hex has a calculated insertion window of about
±12.29° per 60° period. At other phases it cannot seat axially. Chamfers are not a
reason to push harder on thin printed walls.

Use: park/retract → move XY → approach lightly → rotate slowly to find phase →
seat fully → accelerate/turn the commanded signed angle → decelerate to zero →
retract → move XY. During phase search, small incidental screw rotation can occur;
measure it in the first motorized trial. The first demonstrator uses a person's
eyes and fingers for centering/phase, without pretending to prove automation.

At 60 rpm, sweeping one complete 60° phase period takes 0.167 s. Ideal centered
geometry's maximum blocked angular interval takes about 0.098 s, before axial
motion, friction, sensor latency or retries. A 0.1–0.3-s phase-search allocation
is a hypothesis to test. It is not the whole dock/drive/retract cycle. Full seating
must precede torque; a shared head stroke stop/simple contact can support a future
interlock. Fine absolute terrain sensing is unnecessary for this stage.

### Why this coupling ahead of alternatives

| Alternative | Benefit | Decisive limitation or next test |
|---|---|---|
| Straight slot and blade | Easiest visible/manual alignment and simple screw geometry | Only two phases per turn; blade easily rides on the rim and imposes corner contact. Useful manual control, weaker automatic candidate. |
| External hex or double-D screw end with female cup | No hidden socket roof; robust solid male end | A sleeve must surround the screw end, enlarging the tool at the neighbor plane. Still possible at this pitch if the complete sleeve envelope is ≤4.4 mm; finite corner/wall and insertion checks are needed. |
| Rubber friction cup against flat end | No angular phase search | `T ≤ μ F r`; at T=2 Nmm, μ=0.4, effective r=1.3 mm, it requires at least 3.85 N axial force. These are illustrative assumptions, not measured need. Force lifts the screw into its keeper and raises thrust drag; contamination/slip changes turn-to-height correspondence. Keep as a control if positive docking proves too slow. |
| Magnetic rotary coupling | No direct mechanical insertion contact | Needs repeatable magnetic/ferromagnetic features at each screw and controlled field/gap; adjacent 5.08-mm screws can see torque. Torque, neighbor isolation and holding become new tests. No assumption of contactless perfect selection. |
| Small friction wheel on collar side | Leaves axial access free | Needs normal-force reaction, side access in the 0.68-mm intercollar gap, or deliberately different axial levels. A wheel drawn beside an isolated screw is not a fine-grid solution. |

The hex/socket adds one molded/printed feature to a screw already required. A
multi-part clutch or latch at every pin is not needed for local XY selection.

## 4. Honest time model

Separate translation, engagement and useful screw rotation:

`T_site = t_seek + t_approach + t_phase/seat + t_spin + t_retract/settle`.

For a rest-to-rest XY move of distance d, speed limit v and acceleration a,
`t_seek = 2 sqrt(d/a)` below `d = v²/a`; otherwise
`t_seek = d/v + v/a`. With illustrative v=100 mm/s and a=1,000 mm/s²,
one 5.08-mm pitch takes 0.1426 s and a 100-mm jump takes 1.1 s. This ignores cable
oscillation and frame settling; neither a quoted printer travel speed nor grid
pitch alone determines the visit time.

Use total approach/phase/seat/retract/settle allocations of **0.45 / 0.75 / 1.50 s**
as fast / planning / cautious scenarios, separate from XY and rotation. A possible
0.75-s allocation is 0.10 approach + 0.20 phase search + 0.10 seat confirmation +
0.20 retract + 0.15 settle. None has been measured. Count retries when seen; do not
hide them by assuming instant registration. The fast case requires measured
evidence, especially when the tip starts at an unfavorable phase or offset.

For lead L and n rpm, steady motion is `v_z = L n/60`. At lead 3 mm and 600 rpm,
10 mm needs 0.333 s steady rotation. Add about 0.1 s for the two speed ramps if
angular acceleration is 100 rev/s² and full speed is attained. Short motions may
be acceleration-limited. Reversal takes up thread/coupling backlash; turns alone
cannot establish actual travel.

At 600 rpm, lead 3, a 10-mm local change then costs approximately 1.326 s per
nearby sequential site in the planning scenario. A single changed cell is useful;
25 adjacent changed cells (one D&D square) take roughly 33 s plus initial/return
travel. A 100-cell patch takes roughly 133 s. These are transparent workload
examples, not measured play frequencies or claims about every scene.

For 6,400 pins from minimum to 20-mm neutral, the same assumptions give roughly
177 min with one head, or an **ideal fully packed** four-head lower comparison of
44 min. The dense scan adds actual turns on every pin; neutral cannot be a free
software offset. The integrated timing model covers the more useful global and
hybrid alternatives. Reducing lead for better fit/holding increases the rotation
term: use the selected physical coupon's lead, not a convenient old number.

Suggested eventual speed characterization is 300, 600 and 1,200 rpm, with the
last a stretch scenario. The longest screw's straightness, whip, friction, heat
and thread wear remain unmeasured. A supplier's 3,300-rpm **unloaded** motor does
not establish that a printed screw will run reliably at 1,200 rpm.

## 5. More heads without making each pin complex

One automatic head needs two XY drives, one rotary drive and one Z engagement
actuator (which can be a servo/solenoid rather than a fourth continuously rotating
motor). A four-spindle common carriage needs two XY drives, four reversible rotary
drives and four independent docking actuators. Whole-carriage docking would touch
unchanged screws, so selective retraction is essential. If all tips are required
to run in the same direction, a common motor plus four head-mounted clutches is
another candidate, with phase acquisition and clutch duties explicitly added.

The verified catalog control motor [S3] has a 10×12-mm gearbox section and
32-mm body length before its output; the encoder extends beyond the section.
It cannot stand at 5.08-mm centers. Approximately 22×24-mm per-channel carrier
allowances at **25.4-mm spacing** leave room for one four-spindle 2×2 carriage of
roughly 60×60 mm including structure. This is a reservation, not final CAD.
Four tips five pitches apart address the fine lattice by shifted passes: no
change to pin pitch is required. A compact changed patch may use fewer than four
channels at once; dividing every time by four is unjustified. For a 5×5-pin
single-square patch, 25.4-mm-separated tips cannot work on two patch pins at once.

An adjacent 5.08-mm multi-tip head instead needs offset motors and narrow shafts,
belts/gears, or clutches in the shared head. That may be worthwhile because the
complexity is repeated only a few times, but its shaft routing, bearings and
individual axial slides need finite clearance checks. Do not infer a printable
16-tip bank from a drawing with 16 motor symbols at pin pitch.

Independent quadrant gantries help distributed scenes but not a change confined
to one quadrant. Their bodies can collide near region boundaries even if each
tip stays inside its assigned cells. Reserve exclusion zones/time coordination or
different vertical tiers before claiming concurrent edge access. A common
carriage is the simpler first parallel option. Complete cost scenarios and
global/local combinations are in the companion system analysis.

## 6. Failure tests that can change the decision

The requested four-neighbor manual test is sufficient before building XY axes:

1. Operate all four guided pins up/down individually with the same removable
   underside tool, including alternating high/low neighbors. Verify their support
   with the head removed and no screw run-off at endpoints.
2. Mark all four screw collars and pin heights. Record unwanted neighboring
   rotation/height changes separately from common frame motion and the selected
   screw's possible 0.3-mm docking lift. A simple ruler/video is sufficient.
3. Repeat insertion at several socket phases. Compare a printed hand tip with an
   existing metal 2-mm hex key where available. Record rim riding, false seating,
   socket damage, thrust-plate rubbing and manual assistance; do not call a fit
   requiring cleanup a production pass.
4. Check unattended height with a small, stated load representative of the test
   miniature, and immediately after disconnecting following up/down motion.
   Reuse the already positive owner holding observation as motivation, not a
   calibrated allowable load. Smooth running alone does not prove passive hold.

If these pass, the smallest **future** automation discriminator is one unchanged
2×2 array and one spring-loaded driver on simple XY adjustment, initially moving
slowly. Measure at least the bad alignment/phase cases, not only prealigned
insertion. The present deliverable stops at the owner-reviewable manual fixture
and proposed test; it does not open another task or imply its physical success.

An ordinary current-limited drive can limit damage during a later motorized test;
a stalled motor is not a calibrated measure of printed thread strength. For a
trapezoidal approximation self-holding depends on lead angle, flank angle and
friction, plus real thrust-collar friction. [S4] explains this distinction. If
holding fails, first test smaller lead/contact geometry within the same screw
principle; do not preemptively add thousands of brakes.

For the explicitly assumed **3-mm lead, 2.3-mm mean thread diameter and 90°
included profile**, `tan(lambda) = 3/(pi*2.3) = 0.4152`, giving a thread-only
static self-lock threshold `mu >= tan(lambda)*cos(45°) = 0.2936`. This is an ideal
sliding-thread calculation, not the actual friction of the printed material or
the selected compact coupon. The collar can contribute holding torque, while
static and moving friction can differ. The owner's positive holding observation
is retained, but no general unattended holding guarantee follows from the word
"screw", its nominal lead, or a smooth hand-fit result. Use the small stated-load
disconnect/dwell check above; no new brake or sensor campaign is requested.

## Sources and scope of transfer

**[S1] DEPRAG, _Screwdriver Function Module with Electronic Stroke (E-SFM)_,
[manufacturer brochure D0062en](https://www.deprag.com/fileadmin/bilder_content/emedia/broschueren_pics/emedia_Automation/D0062/D0062en.pdf),
pp. 2 and 6, fetched 2026-10-15.** Explicitly separates fast approach, gentle
engagement, low-force assembly, final tightening, depth sensing and withdrawal.
It supports the staged process and force/speed/position control, including
upward screwdriving. Its large industrial force/rate specifications do not rate
a 2-mm socket or establish the cycle times above.

**[S2] OnRobot, [Screwdriver product page](https://www.onrobot.com/en/products/onrobot-screwdriver),
fetched 2026-10-15.** Integrated 55-mm axis, torque control, insertion checks,
M1.6–M6 fasteners and up to 340 rpm show an existing reusable robotic screwdriving
tool architecture. This is architectural precedent, not a purchase suggestion,
cost benchmark or ready-made fit for the 5.08-mm grid.

**[S3] Pololu, [product 5180 specifications](https://www.pololu.com/product/5180/specs),
fetched 2026-10-15.** 10×12×32-mm motor body, 3-mm D output, 9.96:1 gearbox,
12-count motor encoder, 3,300-rpm typical no-load speed at 6 V; listed $32.45
single/$29.85 at five. Stall figures are explicitly theoretical; the maker warns
that stalls can damage the motor/gearbox. This is a sourced dimensional/cost
control, not the selected production motor.

**[S4] Roton, [Screw Backdriving Efficiency](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/),
fetched 2026-10-15.** Distinguishes forward and backdrive efficiency and explains
the effect of lead angle on self-locking. Its bronze-nut friction example is
not a PLA friction measurement.
