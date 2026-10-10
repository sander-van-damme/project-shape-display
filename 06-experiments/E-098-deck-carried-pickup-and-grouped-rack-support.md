---
status: complete
builds-on: [E-095, E-097, E-094, A-013]
---

# Moving selection to the deck escapes pickup reach but multiplies support scans

**Park the full-bank deck with serial ground-dog writing under the central
allocation.** Its finite contact section can acquire and deposit columns while
unchanged columns remain grounded, but each old/target height group requires a
new support-writing scan. Four banks miss 30 s even with instantaneous dog
setting. Sixteen banks pass the declared 0.1-s setting scenario only with a
$0.19055 mean complete shared-channel allowance. Direct heads remain the faster
control. This is a scoped schedule/budget rejection, not impossibility of rack
support or a priced cost rejection. No complete machine is accepted.

Input main `58a4aa2`. Reproduce with
`python3 tools/curated-experiment-checks/E-098/deck_rack.py`.
Evidence: generated rectangular prisms, rigid quasistatic contact, deterministic
error boxes, executable schedule and self-review. No measured manufacturing
prior, force/stiffness qualification, complete writer/retainer, hardware or
independent validation. Output JSON is reproducible and not retained.

## Changed mechanism and finite section

Fixed lips belong to terrain columns; translating selective pads belong to the
lifting deck. Pads arm/clear at deck home, eliminating E-096's need to reach a
pickup handle at an arbitrary 0–40-mm terrain height. A separate column rack
rests on a ground-level translating dog. Rack tooth selection stores actual
height; there is no upright stepped stop to rotate under a raised foot.
This combines E-095's open contact with A-013's rack principle; it is not a new
rack invention. Its selector location and shared energy differ from direct heads.

Nominal dimensions, mm, inside a 5.08-mm cell:

- Spine x=0…1.2, y=0…3.6, z=column height−41…height+60.
- Fixed pickup lip reaches x=2.5, y=0…1.4, underside height+1,
  nominal thickness .9. Nine rack teeth reach x=2.5, y=2.2…3.6,
  undersides height−5j, j=0…8, nominal thickness 1.2.
- Deck pad and ground dog each have active x=1.85…2.85 and retracted
  x=3.15…4.15: a 1.3-mm translation. They occupy the pickup and rack lanes
  respectively. Nominal thickness .9; dog top is ground datum zero.
- A 4.4-mm-square, 1-mm-thick terrain cap starts at height+60; it clears the
  deck's +45-mm extreme even on an unchanged low column. Nominal top gaps
  are .68 mm (.08 mm at the stated XY error bounds).
  Settled nominal core extent is 142 mm; pickup overshoot makes the nominal
  swept extent **146 mm**, tail −41 to cap +105 (146.7 mm under the declared
  vertical bounds), before structure, drives and service space.
  This is the generated embodiment, not a necessary minimum display thickness.

Root overlap joins each lip/tooth to the spine. Pad/dog guides, ground frame,
positive retention and common writer are **granted boundaries**, not hidden
geometry successes. Ideal prismatic guides react eccentric contact moments.
There is no inherited A-013 pawl strength or E-095 force capacity.

A small generator crosses body widths 1.2/1.6/2, pad widths .8/1/1.2 and
per-body datum bounds e=.1/.2/.3: 27 parameter sections within **one**
translation topology. With independent face bounds ±.1 and a .05 reserve,
required separation/overlap is `r=2e+.25`; its section envelope is
`body+pad+4r`. The detailed route uses the 1.2/1/e=.2 section above.
Finite interval corner enumeration independently gives:

| Per-body datum bound e | Capture / body / inactive minimum | Neighbor gap |
|---:|---:|---:|
| 0 | .45 mm | .73 mm |
| .1 | .25 mm | .53 mm |
| .2 | .05 mm | .33 mm |
| .3 | 0 / −.15 / −.15 mm | .13 mm |

The e=.2 boundary barely preserves the chosen .05 reserve; it is not a
qualified process tolerance or sufficient bearing overlap. Y-lane gap retains
.20 mm under the same datum/face bounds. Coherent print/bank shifts and
opposed local errors are allowed; no independent-cell distribution or yield is
inferred. Tilt, warp, roughness, wear, creep, elastic deformation, layer effects
and guide lost motion remain outside the translational box.

## Support sequence, error clearance and failures

Lip datum δ=.8…1.2, individual tooth-height errors εj=±.2 and ground-dog top
error g=±.2 are explicit competing bounds. Tooth and moving-member thicknesses
are enlarged to 1.3 and 1.0 for collision checks. A seated level j has actual
column coordinate `5j+g−εj`: ±.4-mm height error, and nominal 40-mm endpoint
span can shrink to 39.6 mm across tooth errors; the common dog datum cancels.
No minimum usable travel or height-accuracy qualification is claimed.

1. With the deck at −2, arm selected pads. Every column remains dog-supported.
2. Ascend; the fixed lip lands on its selected pad. At each old level j, stop
   at deck height `5j+2`. The old tooth is at least .4 mm clear of the dog.
   Prove pickup, withdraw only those dogs and prove their clearance before
   continuing. The next lower tooth stays at least 1.1 mm below the dog underside
   during this translation.
3. At +45 all selected columns are carried by their pads. Descend to each
   target level j in decreasing order, stopping at `5j+2`. Insert and retain
   the appropriate dogs in the tooth gap. Descend to `5j` for support proof;
   every target lip has separated from its pad by at least .4 mm.
4. Continue to −2, then clear and prove all selected pads. Unselected pads
   remain retracted throughout; unchanged columns never deliberately unlock.

The source checks a real lip/pad or tooth/dog contact at every sampled state,
zero penetration of all nine teeth, spine, cap, pad and dog, and nonnegative
vertical reaction availability **with ideal guide moment reactions**. Contact
breakpoints are included. Between breakpoints coordinates are affine;
vertical bounds prove unloaded slider sweeps continuously. Independent X/Y
separations cover axial passage and neighboring cells for the stated axis-aligned
section. Surface usefulness of the chosen gaps remains unqualified. This is not
full 3D assembled hardware or a compliant contact solution.

Replays cover **1,296 routes / 29,664 contact states**, **18,432 insertion/release
states** spanning all 512 tooth-error sign patterns, **4,752 unchanged-cell
states**, and **72 holdouts** at 1/16/64 subdivisions. Full routes use coherent
and alternating tooth errors; the all-pattern endpoint check supplies remaining
independent-tooth corners. Horizontal enumeration has 800 assignments across
four bounds. These counts are coverage, not reliability statistics.

A missed old-dog withdrawal jams the next lower rack tooth: a nominal 4-mm
lift gives **.819 mm³** dog/tooth overlap. A missed pad clear first lifts an
unchanged column **1 mm** at deck height 2, before the same eventual jam.
A missed target dog leaves the column carried down toward home; clearing then
removes its last support. Real pickup, dog-clear, dog-retained and grounded-load
proofs are necessary; height readback alone is insufficient. Common datum or
reader bias can defeat many cells together. No retry independence is credited.

## Complete schedule and channel consequences

Full workload fills every row with all 72 nonidentity old/new pairs, repeated
to 80 cells. Every old and target group therefore visits every row. With
n=80/B rows per independently driven bank, there are **18n dog slots + 2n
pad slots**, with 20 serpentine scans. Exact row motion is
`20(n−1) move(5.08)` including final home return. Ground-dog setting cannot
borrow E-094's single unloaded-stop scan. All banks operate in parallel;
writer motion, deck motion and setting/proof are serialized within a bank.
This is a constructive schedule, not a universal optimum over other machinery.

Deck travel remains 94 mm, but insertion and support-proof stops add legs:
`move(4)+8move(5)+2move(3)+9move(2)+8move(3)+move(2)`.
Central E-094 motion is v=200 mm/s, a=5,000 mm/s². Allocate .1 s each for
pad/dog slots, .1 s per pickup/deposition group, 2 s map overhead, one repeated
dog slot and one support retry (.1 s plus 2×move(2.2)). Slots must include
approach, setting, retention, readback and withdrawal; the common writer and
sensor parallelism are unqualified. Persistent faults stop supported operation.

| Banks | Rack-deck seconds | Direct E-094 seconds | Rack-deck dog slots |
|---:|---:|---:|---:|
| 1 | 266.261 | 67.403 | 1,440 |
| 2 | 135.261 | 35.037 | 720 |
| 4 | 69.761 | 18.854 | 360 |
| 8 | 37.011 | 10.762 | 180 |
| 16 | 20.636 | 6.717 | 90 |

At B=4, zero dog-slot duration still takes **33.661 s** under other grants.
At B=8, require dog slots **<.061264 s**; B=16 permits **<.202898 s**.
For .02/.05/.1/.2/.5-s dog slots, minimum passing tested B values are
8/8/16/16/none at central motion; 4/8/16/16/none at fast 400/20,000;
16/16/16/none/none at slow 80/1,000. Pad/proof slots stay .1 s. These are
competing allocations, not measured capability or universal lower bounds.
Across all 76 positions of the initially flat 5×5 patch, B=16 takes
**7.216–9.836 s**; B=8 takes **7.216–10.170 s**. No physical disturbance bound.

The favorable **82B channel grant** shares 80 setting channels, one row axis
and one lift axis per bank across home pads and grounded dogs. It needs a real
dual-plane head/access mechanism. Separate 80-channel pad and dog writers plus
two row axes and one lift instead give **163B**, not a free second mechanism.
At B=16, $500 cap/$250 elsewhere/free bought cell items permit respectively
**$0.19055 / $0.09586 per complete channel**. $0.02 bought per cell reduces the
shared allowance to **$0.09299**. No price quote or zero-cost missing component
is implied. Direct's B=4 allowance is $0.78125 per complete head under its
own functional boundary; selector and positioning channels are not equivalent.

Per cell this section repeats one rack, deck pad and grounded dog, three
sliding guide functions (including column), two binary retention functions,
and lip/pad plus tooth/dog load contacts. It removes a tall stop, not the need
for retained selection or grounded support. At least six individual observations
per changed cell cover pad set/clear, pickup, dog clear/insert and load proof:
**38,400** on this full workload before writer clearance and extra readback.
An unconditional false-accept bound would propagate by the union bound without
independence; none is established. Assembly, service access, full-bank force,
power and material volume remain unpriced/unqualified.

## Disposition and next useful discriminator

Stop parameter refinement of this central full-bank serial-scan architecture;
its schedule loses before guide strength is evaluated. Do not print it. Retain
the contact source, jam witnesses and common-home selection idea. Reopen with
materially changed addressing/scheduling, or a complete setting channel meeting
recomputed timing/cost and retained-support gates. Faster slots alone cannot
rescue B=4 under central motion; novel selection does not establish product value.

The remaining complete-system comparison should test **row-local
shared lift versus bank-wide lift and direct independent heads**, explicitly
trading repeated lift travel against group rescans and selector count. First
use executable batching/schedule synthesis with the same proof/retry and budget
boundary. Stop a partition on a decisive necessary-condition failure before
adding its guides or another lock. This changes energy/selection grouping;
it must not conceal nine target writes, assume instantaneous mechanical decoding,
or revive E-096/E-097 failures. Retain only a useful conditional tradeoff or
close the campaign with scoped exclusions; no new worker or physical experiment.
