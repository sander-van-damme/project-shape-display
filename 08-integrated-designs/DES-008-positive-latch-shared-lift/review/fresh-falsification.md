# Fresh independent falsification review: retained row-lift architecture

Author/workstream: F, independent reviewer. Date: 2026-10-14. No physical tests were conducted. This review was requested before candidate selection and deliberately treats state diagrams as insufficient mechanical evidence.

## Decision

The retained row-lift concept is a plausible mechanism family, but **the present description does not establish a manufacturable 30-second machine**. Keeping a selected dog engaged while retiring pins at individual displacement thresholds is logically possible and eliminates repeated capture. It does not eliminate mask-writing time, support transfer, resident output memory, or difficult under-array packaging.

The least defensible claims to remove are a 0.1–0.2 second complete eight-position mask rewrite using an ordinary stop-and-index writer, and a collision-free scanned row head inferred without the complete vertical and horizontal swept envelope. These can change the architecture ranking. The fresh review does not approve digital engineering success.

A small four-lane retained-output transfer test is justified if it contains the actual keeper/readout mechanism and demonstrates that rewriting the next mask cannot alter the current loaded outputs. Merely proving a rack can be picked up is not sufficient.

## Mechanism reviewed

The initial concept had OFF / TRANSFER / DRIVE slides. Its refinement has independent binary output banks: A holds the dog engaged; B releases the fixed ground pawl. Each bank has a common keeper comb engaging one of two notches on every output key. A separate 64-bit hole-mask memory is rewritten while both output banks remain locked. A compliant reader passes ON holes and preloads keys that should remain ON, a keeper withdraws, OFF keys return, and the keeper relocks before the reader withdraws. Retirement updates B first, seats the newly restored ground pawls with Z motion, then updates A. Dogs that remain selected continue the same up or down sweep. An eight-writer carriage programs eight groups of eight flags.

There is no fundamental state contradiction in that sequence if all mechanical conditions below are met. Agreement with the logic is not a claim that those conditions fit the proposed pitch.

## Critical objections and required remedies

### 1. Eight-position writing cannot be assigned an arbitrary short duration

Eight equally spaced write positions at 6.35 mm pitch require 44.45 mm one-way travel. For seven independent stop-to-stop moves with symmetric acceleration and no velocity limit,

`t_motion = 7 × 2 sqrt(6.35 / acceleration)`.

At 3,000 mm/s² this is 0.644 seconds before actuator action, settling, or return. Twenty milliseconds per write position gives 0.804 seconds. At 1,000 mm/s² those values are 1.116 and 1.276 seconds. Even 10,000 mm/s² needs 0.353 seconds motion alone. These bounds assume zero reader obstruction, zero dwell for mask verification, zero carriage return, and no velocity limit; actual time cannot be shorter for this stop-and-index scheme.

A continuous-motion writer is a different mechanism and could improve the bound. It requires proven setting/reset windows while passing a flag, minimum spacing between successive changes by the same actuator, synchronization, and reversal/end handling. A fast timing model may use it only as a clearly marked unqualified assumption. Alternating scan direction avoids an empty return, but it does not remove the stroke or the setting windows.

### 2. A common reader requires separate compliance at every blocked output

A rigid 64-finger reader cannot simultaneously stop OFF fingers against a grounded mask and let ON fingers travel roughly 2 mm farther to preload keys. Each finger needs its own compliance or an equivalent selectively released travel joint. A one-piece leaf comb can reduce purchased-part count, but still contains 64 independently loaded flexures and 64 contact paths.

For two retained output banks, per head count at least:

| Function | Quantity per 64-lane head |
|---|---:|
| Writable mask flags | 64 |
| Retained A/B output keys | 128 |
| Compliant A/B reader channels | 128 |
| Common keeper combs | 2 |
| Bilateral dog channels | 64 |
| Fixed-height ground-release tongues | 64 |
| Reused writers | 8 |

This excludes key-return springs if not integrated, guides, keepers' actuators, reader actuators, mask carriage, dog-opening linkage, and row/Z stages. Eight heads therefore have 1,024 retained output keys and 1,024 compliant reader channels, even though they need only 64 expensive data writers. Active-component reduction is real; overall mechanism simplification is not established.

### 3. The shared keeper has a shared failure mode

One partly returned key can prevent the keeper from seating across the entire row. The safe sequence must leave the reader or prior support engaged until the keeper is known mechanically seated. A keyed stop or interlock is preferable to assuming a motor command proves all notches aligned. A stalled keeper is a recoverable head fault only while both dog and ground support remain available. It must not automatically advance to releasing the other support bank.

Readers must preload the retained ON keys before the keeper releases. Otherwise their spring forces can return keys during the gap. Unlocking a keeper against 64 spring loads also requires a credible force and friction allowance; this is not a zero-load latch motion.

### 4. Dog retirement needs real vertical clearance

For a target height `h`, insert the ground pawl while the rack is at `h + δ`, lower Z by δ to transfer load to the ground seat, then retract the dog. A bilateral dog needs sufficient vertical clearance that its upper flank does not pull the now-grounded rack against the seat during this transfer. Its lower flank must still take the lifting load. The error budget includes groove variation, ground-seat variation, beam deflection, guide play, dog deflection, and commanded travel error.

A 0.2–0.4 mm unload/seat stroke cannot be accepted without comparing it with those errors. The final groove/dog geometry may need more clearance or a compliant lost-motion feature, and this may alter the usable height quantum.

For descending motion a mere supporting hook is insufficient. Gravity can fail to overcome guide friction or an unevenly loaded top. The upper dog flank must positively pull downward without wedging against the ground pawl. Both load-transfer directions need testing.

### 5. Under-array collision is a major unresolved layout question

The Z beam cannot rise into the tails of unchanged low pins. A substantial beam cannot simply be placed in a narrow inter-row gap and then indexed sideways through the array.

One bounding layout puts the fixed ground-pawl plane at z=0, and the dog plane at z=-50 to -10 for a 40 mm upward stroke. For the common lower capture plane still to intersect the grooved stem at all permitted initial heights, the grooved tail may need to extend roughly 90 mm below the minimum-height datum. If the main Z beam always stays below the lowest unchanged tails, approximately 80 mm tall fingers result in this example. These are review dimensions, not a universal necessary layout.

An alternative is to retract every projecting feature into continuous X inter-column corridors while scanning in Y. This can avoid withdrawing the entire head below the rack tails, but demands a dimensioned allocation of dogs, vertical state-transfer slots, ground-pawl release interfaces, and adjacent-lane mechanisms within the corridors. A 4 mm rack at 6.35 mm pitch leaves only 2.35 mm before tolerances. Two neighboring bilateral dog systems compete for that space. The arrangement must be demonstrated, not categorically ruled out or assumed.

A thin beam in a Y inter-row corridor may work during lifting, but must descend below rack tails before Y indexing unless every crossing feature retracts. Charge that withdrawal and reacquisition in timing.

### 6. Finger stiffness is more restrictive than basic Euler strength

Independent simple calculations in `F-fresh-checks.py` illustrate the scale. An unguided 80 mm long, 4 × 2 mm polymer cantilever, E=2 GPa, has only 2.06 N ideal fixed-free Euler load and deflects 9.6 mm under a 0.3 N transverse load. A 3 × 1 mm steel strip has ample axial Euler load for a terrain pin but deflects 1.024 mm sideways at that load. A 4 × 2 mm steel finger reduces the transverse deflection to 0.096 mm. Upper guidance or a folded section is therefore essential for thin fingers. Guide friction and packaging then belong in the load path and BOM.

For a simply supported 406.4 mm aluminum beam under a uniformly distributed total 64 N load, a 10 × 10 × 1 mm square tube deflects 1.65 mm; a 20 × 20 × 2 mm tube deflects 0.103 mm. That latter value already consumes a meaningful part of a 0.2–0.4 mm transfer stroke. The 64 N is a review load case, not a measured operating load. Bracing or more supports changes the result, and must be drawn.

## Fixed bank platen / mechanical crosspoint escape

The proposed escape uses a resident dog and binary flag at every pin, a common Z platen per bank, and 64 column data actuators writing one selected row at a time. It removes scanned dog transport but exchanges 512 or fewer head dogs for 4,096 resident dogs, plus 4,096 retained flags and their read/write/output mechanisms.

A row blocker that merely locks unselected flags does **not** isolate a column rod. If the rod contacts all flags, every locked crosspoint must deflect or the rod cannot move. At 32 rows that becomes 31 blocked compliant couplings per selected output, with force and wear on unselected sites. Reject this simplest interpretation.

A true geometric write-enable is possible in principle: 64 column code rails or two-profile shafts run continuously through the bank, while the selected row's 64 flag followers are moved into engagement. Reset that selected row's flags; position the 64 code members; raise/read the row so the high-profile states set selected flags; withdraw the row; retain flags. All other rows remain physically clear of the code members. This has explicit two-coordinate readout or a movable row cassette, and cannot be counted as one simple sliding flag per pin. Positive setting of both states, latching, and readout into the resident dog/ground-pawl sequence still require engineering.

With 32 rows per bank, 0.1 seconds per row, and 8–10 signed binary masks, programming alone is 25.6–32 seconds. A favorable scene with fewer masks may be competitive, but use its actual transaction count. The claimed 0.05–0.12 seconds per row also needs row-index acceleration and read/reset time, preferably continuous scan or a concrete cam sequence. Global lift and pawl-release forces now scale with thousands of cells and must be calculated.

Recommendation: retain this as a distinct fallback, not the current proven winner. Its next decision gate is a one-write-row / two-neighbor-row crosspoint coupon showing no ghost writes. Do not begin a full 4,096-cell CAD package before that mechanism is explicit and its repeated-part burden is credible.

## Comparison with direct inexpensive selectors

Direct three-state actuation of each head lane can remove the flag writer, compliant reader banks, and common keeper system if one actuator can hold OFF / TRANSFER / DRIVE. It still needs the same dog, ground release, transfer clearances, and swept-envelope proof. It is a valuable control architecture for timing and prototype debugging.

At eight 64-lane heads, however, this returns to 512 active selectors. Treat its real installed cost, wiring, driver channels, servo hold behavior, and mass as a complete alternative, not as a cosmetic change. The mechanical-memory design only wins if it materially lowers total delivered cost after those extra 1,024 keys/readers are manufactured and assembled. No supplier-qualified installed-cost comparison was available to this reviewer.

## Minimum meaningful experiment and stop criterion

Build four adjacent lanes at the intended 6.35 mm pitch, with real rack grooves, ground pawls on rigid seats, bilateral dogs, two independent retained output banks, and a separately rewritable mask. Include neighboring dummy rows or physical clearance envelopes. Exercise:

1. Capture lanes 1, 2 and 4 while lane 3 remains ground-held.
2. Raise the selected lanes by one quantum; rewrite the mask to retain only lanes 2 and 4 while all dog keys remain locked.
3. Restore lane 1's ground pawl, seat it, release only its dog; continue raising lanes 2 and 4.
4. Repeat with a different retirement order, then perform controlled downward movement including a lightly friction-loaded lane.
5. Intentionally prevent one key from reaching its notch and verify that the sequence cannot remove the other support.
6. Record capture/release forces, common-stage deflection, setting variation, missed writes, and the actual time of a complete mask change.

A short test is sufficient to falsify the current mechanism or select its next engineering revision. It is not production reliability evidence. For scale context only, an independent per-transfer failure rate of 10^-4 gives a 66% chance that all 4,096 transfers succeed in one nominal update; large arrays eventually need much better reliability or explicit bounded recovery. Do not make comprehensive sensing a prerequisite to the coupon.

The physical boundary is legitimate after a dimensioned and low-waste version of this experiment is delivered. The unresolved issues must remain explicit in the whole-machine recommendation: memory update speed, support-transfer tolerance, full head swept volume, and manufacturing yield. Neither a state simulation nor this review closes them.

## Reproducibility

Run `python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_bounds_independent.py` to regenerate `analysis/bounds-audit-results.json`. It uses only the Python standard library. The model is an independent bound calculation, not a replication of the scene scheduler, and does not use that scheduler's timing assumptions.
