---
status: complete
builds-on: [E-175, E-173, E-172, E-095]
---

# Broadcast safe-state reset helps dense maps, but readback limits the gain

**Retain home-only broadcast pickup clearing as a conditional reusable function;
stop load-only retraction and narrow-capture rigid resetting.** A common reset
comb can clear selected and unchanged pads without moving grounded columns in
the generated section. It avoids a third local state required by load-history
clearing. With the existing scanning reader, however, B4 dense timing improves
only **22.919→21.494 s**, versus **19.469 s** for direct heads; a 5×5 update gets
slower under whole-bank readback. No surviving ground keeper, complete machine,
fabrication or purchase follows. This does not reopen E-175's failed lane-key or vertical-stop packages.

Input main `2e0d44c`; LAB-287. Reproduce:
`python3 tools/curated-experiment-checks/E-176/reset.py`.
Source imports unchanged E-173/E-172 controls. Evidence: exhaustive finite-state
synthesis, rigid rectangular sections, bounded scenarios and conditional schedule
calculations; self-review only. No physical measurements, calibrated priors,
priced BOM, dynamic contact, complete CAD or independent qualification. Generated
JSON is discarded.

## Search move and complete functional boundary

The proposed single ground/carrier transfer dog duplicates E-172; it was stopped
before another model. Three alternatives change how **temporary pickup selection
ends**, while retaining separately programmed ground height:

| Combination | Selection, motion, retention, load, verification/recovery |
|---|---|
| Load-only spring return | Writer arms pickup; column load supposedly holds it in; spring clears it on unloading. Empty-before-pickup and empty-after-deposit demand opposite behavior. A static force law alone cannot supply that distinction. |
| Load-history one-shot | Arm latch, load-triggered phase change, then unloading releases spring. Shared deck transports; ground dog retains final terrain. Prove actual load phase and final pad position; hold bank on disagreement. Requires an additional distinguishable local state and physical transition. |
| Home-only broadcast clear | Writer individually arms changed pads; deck and ground supports complete E-173 cycle. At deck home, common comb pushes all pads toward clear; keeper self-completes/retains them. Retract comb, read actual pads, inhibit next ascent on disagreement. Ground supports carry all columns during resetting. |

The independent functional inversion is **broadcast a safe state instead of
individually writing identical clear bits**. This is a new combination relative
to the checked E-095/E-098/E-172/E-173/E-175 interfaces, not a claimed new latch
principle or patent novelty. Load-history sequencing overlaps E-173's push-push
analogy. No global search-saturation claim or independent literature search.
Ground-height selection, row writer, support proofs and bank arrest remain real
obligations; the comb does not supply them.

## Executable minimum-state discriminator

Inputs A/L/U mean arm, loaded, unloaded. Output is pickup active/clear. Initial
clear must ignore L/U; armed pickup must survive arbitrary U before acquisition;
a loaded pickup must survive repeated L and clear on U; rearming must work.
The synthesizer enumerates deterministic Moore machines with initial state zero,
all binary output assignments and all transition tables at 1, 2, then 3 states.
A reachable product-automaton equivalence check covers **arbitrary input words**,
not merely the short trace filters. There are **0/0/2 solutions**; the two
three-state machines differ only by renaming their active states:

| State | Output | A | L | U |
|---|---|---|---|---|
| Clear | clear | Armed | Clear | Clear |
| Armed | active | Armed | Loaded | Armed |
| Loaded | active | Loaded | Loaded | Clear |

Independent lower bound: Clear differs immediately in output; Armed and Loaded
are distinguished by suffix U. Therefore three distinguishable local states are
necessary **for this load-event interface**, not three parts or three actuators.
A hysteretic spring/cam may encode those states; it is not a stateless return.
If the column never supplies a detectable load transition, the commanded cycle
is observationally identical to waiting for pickup. Own weight could supply a
positive trigger margin, but mass, friction, acceleration and threshold bounds
are absent. This rejects a free guaranteed load trigger, not every one-shot.

With independently supplied H=home-clear, load is ignored and the synthesizer
finds **0/1 solutions at 1/2 states**: A sets active, H clears, L/U preserve state.
H must occur only after all columns are grounded and the deck is home. A fixed
cam that resets while passing other heights would need a different exposure
proof. Home clearing never arms an unchanged cell; a common *rearm* would.

## Finite home comb and neighboring bodies

Retain E-173's fixed pickup lips, Y-sliding deck pads and nominal five heights
0…40.4. At deck home d=−2, each pad is X=−2.2…−1.2, Z=−3…−2, Y=q±.5;
q=0 active, q=1.7 clear. A bank-wide translating comb repeats these sections:

- Tooth X=−2.8…−1.3, Y=f−.4…f, Z=−2.8…−2.2.
- Post X=−2.8…−2.5, same Y, Z=−3.5…−2.2.
- Longitudinal rail X=−2.8…−2.5, Z=−4…−3.5, along the bank's Y rows.

Rails connect outside the bank to a shared drive; that external bridge, guidance,
writer-access corridor and the existing pad keeper are **not constructed**.
This is a connected repeating tooth/post/rail section, not a free isolated tooth.
The column's long spine prevents using an unperforated full-area reset plate.
The separate rails instead pass beside the spine and rack-tooth envelopes.

Park f=−.9. During the geometric clearance envelope, advance f to 1.2 and set
`q=max(q_initial,f+.5)`. The side contact area is .9×.6=**.54 mm²**; only the pad
moves, while its column stays on the ground dog. Test all five column heights,
both initial pad states and all eight neighboring sites at every height/pad state.
1/4/16 subdivisions give **20/50/170 central poses**, each with neighbor checks.
The contact breakpoint f=−.5 is checked separately. Affine translation and
constant axis separation bound the intervals. Parked comb checks also cover
active/clear pads and deck heights −2/0/20/45.4; X or Y separation remains valid
through intermediate travel. Nominal solids do not penetrate.

A full 2.1-mm comb excursion is a **clearance envelope**, not a universally
executable drive against imperfect hard stops. The broad-threshold version below
commands f=.85, a 1.75-mm drive stroke; its keeper supplies the remaining pad
motion. Every intermediate pad position lies in the checked envelope, but snap
kinetics, impact and retention are unproved.

Conservative independent center/facing-edge terms ±e give parked tooth/pad gap
`.4−4e`, post/pad gap `.3−4e`, rail/pad vertical gap `.5−4e` and adjacent rack/rail
X gap `.48−4e`. At e=.05 these are .20/.10/.30/.28 mm. Contact-area lower bound
is `(.9−4e)(.6−4e)`=.28 mm². This is a translational sufficient envelope, not
full assembled error simulation; e=.075 loses strict post clearance. Layer shape,
warp/tilt, rail bow, bias, first layer, roughness, keeper friction and elastic
closure require additional budget. The .3-mm posts/rails and .4-mm tooth breadth
are unqualified repeated features; no stiffness/force capacity is credited.
No X1C process capability or yield follows.

## Rigid reset mismatch versus broad self-completion

Two pads with clear stops q=1.7±e cannot both be driven exactly to their stops
by one rigid comb. Stopping at the early stop leaves the late one **2e short**;
driving to the late stop penetrates the early pad by `.54×2e mm³`.
At e=.05 these are **.10 mm and .054 mm³**. A keeper capturing only within
.03 mm of each actual stop fails once e>.015. This is a finite two-pad witness,
not an objection to every shared reset.

A self-completing keeper changes the requirement. Grant a snap/capture threshold
q_c=1.0±e and end stop q_s=1.7±e. For drive error ±b, a safe common command has

`1.0+e+b < q_command < 1.7−e−b`.

Corner enumeration includes coherent bank bias and opposed local thresholds.
Command 1.35 leaves a positive interval at e=b=.1 (allowable command 1.2…1.5).
At e=.2/b=.1 the interval is 1.3…1.4; e=.25/b=.1 loses positive margin.
These are explicit hypothetical bounds on **an unbuilt keeper**. Snap completion
must not rely on merely assuming a reset bit; a failed keeper can remain active.
A broad capture basin avoids compulsory extra compliant fingers, but needs an
actual retained mechanism and return-energy path. Existing E-173 pickup retention
was already unbuilt; no solved component is being inherited.

Alternative per-site compliant fingers can accommodate stop variation. With
reset resistance f, stiffness k, the latest stop needs f/k overdrive and the
earliest sees force f+2ke. At B4, 1,600 sites can share the adverse error:
for e=.05, k=1 N/mm and f=.01/.1/1 N, force sums are **176/320/1,760 N** and
needed extra travel .11/.20/1.10 mm. These are static bounds without contact
friction, rail deflection or dynamic snap loads, not predictions. Broad keepers
still require up to 1,600f=16/160/1,600 N if transitions align. Spatial correlation
cannot be averaged away. .1 N over the .28-mm² contact bound is .357 MPa mean
pressure; no PLA allowable, creep or fatigue qualification. Common rail bending
can invalidate the command window even when drive position is correct.

## Full-map, local and inventory consequences

Retain E-173's dense arbitrary five-height workload, row/deck motion at
200 mm/s and 5,000 mm/s², .1-s arm, .5-s target word, .1-s pickup/support proofs,
2-s preparation/registration/settling allocation and one word/reseat retry.
Add out/back 1.75-mm reset travel and .1-s reset completion allocation. Charge
.02 s per row for final pad readback using the existing 80-channel writer reader;
all rows of each reset bank are visited, because all pads were exposed.
No motion overlap. Returns to row home are included.

| Banks | Explicit clear E-173 | Broadcast + scan | Broadcast + granted parallel proof | Direct control |
|---:|---:|---:|---:|---:|
| 2 | 41.252 | 38.227 | 33.910 | 36.238 |
| 4 | 22.919 | 21.494 | 19.360 | 19.469 |
| 8 | 13.752 | 13.127 | 12.085 | 11.085 |
| 16 | 9.169 | 8.944 | 8.447 | 6.892 |

Seconds, conditional successful-update allocations only. Independent dense hand
sum: saved time is `n(.1−read)−.1−2move(1.75)` for n rows/bank. B4 at read slots
0/.02/.05/.1 takes 21.094/21.494/22.094/23.094 s: **zero reader dwell still pays
reader transport**. Eliminating the scan needs a real parallel observation or
mechanical completion proof for every pad, not drive position/current alone.
The granted parallel case includes that proof in .1 s and is only .109 s faster
than direct B4; no credible superiority margin survives its unbuilt sensing.

An initially flat 5×5 patch (20 changed cells), over all 76 row positions, takes
**8.679–10.709 s** at B4 with bank-wide reset/readback versus 6.660–9.257 for
explicit clear; B8 gives 7.321–9.110 versus 6.622–8.749. Unchanged columns stay
grounded in the nominal section, but the verification cost scales with touched
banks. A conditional alternative trusts already-proven clear pads because the
reset only moves toward clear, retracts the writer in place, and reads changed
rows only. It gives B4 **6.674–9.032 s**, B8 **6.557–8.524 s**. This narrower
proof is valid only with monotone reset and retained known-clear states under the
actual fault model; it is not supplied by the nominal sweep alone. It saves
`n_changed(.1−.02)−.174833 s`, so at least three changed rows/bank are needed
for a gain. A hybrid could choose explicit clear below that threshold. Shared
writer/comb access and physical sensing remain unbuilt in either allocation.

At B4, scanning broadcast uses 320 setter/read bundles + 4 row axes + 4 deck
axes + 4 reset drives = **332 complete bundles**, versus explicit 328 and direct
324. With hypothetical $250 elsewhere under the $500 ceiling, mean allowance is
$.753/bundle before local purchases; this is not a price. Parallel sensing is
**not** costed by that count. Resident inventory still includes 6,400 ground
selectors and 6,400 pickup selectors, plus 6,400 comb teeth/posts; a compliant
repair adds 6,400 flexing interfaces. $.02/site adds $128; a 10-s/site operation
adds 17.8 h. Print mass/time/scrap require generated fabrication geometry/slicing.
No reduction of bank arrest load or of lane-retention burden is established.

A missed clear can repeat E-173's 2-mm unintended lift at deck d=3. Verify actual
pad states before a new ascent; a stuck pad keeps the bank inhibited and columns
grounded. Height-only observation before ascent cannot reveal it. Full-board
common read bias may falsely accept many pads; no false-accept rate is known.
Even with marginal p per pad, expected misses are 6,400p without an independence
assumption; a board-success probability needs a dependence model. Late support
faults, persistent reset jams and power-loss arrest are outside the bounded retry.

## Decision and next discriminator

Stop a stateless load-return claim, and a rigid exact-stop comb with narrow
capture. Retain **safe-state broadcast with a broad self-completing pickup keeper**
as a cross-family option, not a preferred machine. It saves modest dense-map
handling with scanned proof and can worsen regional performance. Load-history
clearing remains possible only with a real third state and a trigger margin;
it has no demonstrated burden advantage over the home clock.

Next useful move: construct one finite **broad-capture binary keeper + shared
reset tooth + opposite-side arm writer**, including full neighboring sweeps,
retained clear/active states, spring energy/force and a stalled reset. Compare
its repeated compliant contacts and dense/local cost with explicit independent
clearing. Stop if broad capture requires a second local release or recreates
E-175's obstructing roof. Do not tune the rejected lane key or claim its ground
support solved. This small geometry test has higher value than another timing
sweep, printing, or full-machine CAD.
