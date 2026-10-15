# E — adversarial mechanical review

Date: 2026-10-14. Read current main `b23ed12`, requested DES-007 commit `1c622b0`, root/mission/current criteria, DES-007 source and relevant prior support-transfer failure records. This review is an engineering falsification screen, not measured validation. No prior tolerance scenario is treated as a universal process capability.

## Decisions that change the architecture

1. **Do not promote DES-007 to full-display baseline.** Its source reproduces the stated time/cost problem; independent expensive selectors remain the dominant architecture defect. The small hand rig is useful scoped evidence if ever tested, but completing it is not necessary to select a stronger full machine.
2. **A crossed rigid row/column support array transfers unchanged pins between independent support-height datums.** This is a topology-level problem for neighbor isolation, not merely an adjustable CAD clearance. A higher column datum fixes active-row handoff only by creating a different handoff in inactive rows when that column bar withdraws. Replace dual load-bearing datums with a single passive local load-bearing latch whose release is addressed by reusable row hardware.
3. **Do not use 5.8-mm square working stems at 6.35-mm pitch without showing full retracted hardware.** The 0.55-mm inter-row aisle cannot house an approximately 0.8-mm-deep withdrawn dog plus a root/release mechanism. Wide playable caps can sit over narrower rectangular stems; stagger ground and pickup hardware vertically.
4. **A row head with passive per-pin pawls is a credible surviving mechanism, conditionally.** It repeats inexpensive local retention but reuses actuation and selected release. Its decisive prototype is several neighboring rack columns, a shared lift and retained mask, including drag-forced lowering and witness pins. It is not another single screwdriver.
5. **Thin centered walls and 25.4-mm bases in 25.4-mm corridors are mathematically incompatible at every pin pitch.** A successful mechanism cannot silently mark that geometry passed. A wall-under-base recess or explicit supported base/wall choice must be demonstrated.

## DES-007 independently checked

Executed its ideal replay and source schedule on the unchanged E-258 semantic inputs. All 625 ideal signed four-output replays pass; this establishes command arithmetic only. Four-head finite strip worst scene is 68.9277718 s (`shallow:ruins` to `deep:ravine`), cost allocation $4,872.36–9,197.42. Eight-head loop comparison is 29.3843545 s with 512 servos, allocated $9,071.50–16,257.02. The loop is not constructed/qualified, and wall/miniature handling is additional.

Independently substituting the stated friction assumptions gives:

`T = (0.35 + 0.25*1.2*0.8)/(1 - 0.25*1.2/2.5) = 0.6704545 N mm`.

64 selected outputs require `64*T/2.5 = 17.1636 N` strip pull before guide/shoe drag. The 3 × 0.2-mm strip carries 28.6061 MPa nominal axial stress. These are correct conditional calculations, not qualification. At 0.4 strip friction the stated 0.8 N mm traction capacity is only 19.3% above demand.

`check_geometry.py` does not solve isolation under masks: it appends `2.8 - 2.5` for each OFF bit, yielding the same 0.30-mm gap regardless of neighboring loads. Nominal Boolean mesh checks cannot establish strip deformation, wire flex, adhesive joints, print errors, wear, or a loaded OFF gap. The separator wires are cantilevers anchored in the head; their compliance must also enter any future isolation model.

Owner evidence is materially positive but limited: five 10.3-mm-wide short nuts were manually cycled five times without damage/postprocessing, and 0.20-mm relief felt easiest; historical 4.4-mm Trial 5 operation is owner recollection with unidentified exact parameters. The recent narrow replica had supports filling the bore and no valid fit test. None establishes full-length, powered, load-bearing array behavior; none justifies repeating the completed wide short-thread test.

## Falsification requirements by mechanism family

### Row/column AND selection

A plain row enable AND column enable selects their Cartesian product, not an arbitrary pixel mask. To actuate (r1,c1) and (r2,c2) without the off-diagonal sites, the machine must serialize rows, store local state, or prove an additional disjoint gating mechanism. An arbitrary diagonal needs n product rectangles if only positive Cartesian masks are used. Checkerboards alone are a weak test because two parity rectangles can express them.

Test all four half-selected cases and the sequence: set column A; select row 1; remove row 1; change column B; select row 2; reverse drive; remove columns before/after rows. Test stale retained states and changes while shared power remains available. A blocker that requires force threshold discrimination is not a positive AND merely because it is drawn at an intersection.

**Gate:** full mechanical truth table at bounded displacement/force errors, including intermediate selector travel. Ground support must remain independent of transient address states. Charge all local memory, reset and writing.

### Shared lift with retained columns

The movement sequence must keep a grounded path through either the stationary pawl or captured drive connected to an arrested lift. A normal working transaction is: retained stationary support → dog capture → unload stationary pawl → selected pawl release → signed drive → restore pawl → controlled seating/proof → dog withdrawal → empty lift return. Simply driving ground support as NOT(selection) loses required overlap.

A top-only pad cannot force lowering against guide friction. A rigid two-flank dog can, but its backlash must be accommodated in reacquiring the stationary pawl. A single global elevator cannot simultaneously carry arbitrary-height old columns on one rigid datum without suitable long tracks, periodic racks or variable-height acquisition.

**Gate:** draw actual contact inequalities at every transition; deliberately add guide drag to a selected column in the prototype. Test power loss/stop with drive supporting, and mechanical return without recapturing a deposited pin. Do not add elaborate fault automation before basic motion, but do not leave unsupported intermediate states.

### Positive rotary clutches

Common drive phase does not imply common output phase. A bank of rigid dogs cannot dock arbitrary screw phases simultaneously. A spring-loaded axial clutch needs a finite phase-seeking event, independent axial compliance and confirmed full engagement; phase-seeking can move the output before engagement is complete. Quantized output heights can solve phase only if the quantization is deliberately selected and tolerances fit.

**Gate:** two output shafts initially at worst opposite phases, neighboring clutch OFF, both rotation directions, torque-on disengagement, and a stopped restart. Do not compare a motor RPM-only schedule to a design requiring phase search.

### Row-parallel independent motors

Fewer reusable motors may be cheaper than many reusable motorized selectors. A 64-motor bank is a legitimate control against 512 selectors, provided real loaded motor/gear/driver cost, packaging and docking are included. The slow 28BYJ-style geared stepper cannot inherit 850-rpm screw timing; small fast DC motors require rotation/height metering or justified coarse open-loop behavior.

**Gate:** one full-pitch multi-output docking section and loaded torque-speed operating point, including phasing, gear loss, drive electronics, shaft bearings, and all approach/withdrawal time. Reject fewer-motors-by-slogan comparisons.

### Passive masks and local memory

Sharing energy does not remove the target information channel. For 64² cells and five levels, at least 9,510.6 bits of target information must be represented; for 41 levels, 21,944.5 bits. These information lower bounds alone are weak (317/731 bit/s over 30 s) because the physical write/reset motions dominate. A threshold-mask implementation with n rows and L masks needs nL row transactions unless actual reuse eliminates them. At 64 rows, five masks allow only 93.75 ms per row-mask if the entire 30 s is spent writing; 41 masks allow 11.43 ms.

For a head with w writers and n/w positions, every rewrite must include writer stroke, release, index, settling, verification if required and return/reposition. A spring latch must retain under all common lift accelerations; resetting must not move live drive dogs. Unknown maps cannot be physically prewritten for free.

**Gate:** explicit retained bit geometry and complete sustained write ledger, not just writer datasheet electrical response. A 64-bit mask with eight writers needs eight actual positional addresses per rewrite. Count every mask, including clear and any sign transition.

## Strongest revised candidate: one passive grounded pawl per pin

A reusable masked row head already supplies spatial row addressing; column bars that support other rows are unnecessary. Each pin has a periodic front retention rack and a separate rear captured-drive groove. One spring-return passive pawl engages the front rack and bears on a fixed frame ledge. Its spring only positions the pawl; the ledge, pawl foot and tooth carry vertical service force. A selected head bit gates both a moving drive finger and a stationary-height pawl-release tongue. Unselected pawls never leave their original bearing contact.

Ground release must remain at the stationary support plane while the drive finger moves through the stroke. This needs separate linked/gated tongues or a genuine long slot/follower; a single translating finger does not automatically do both. The mask must survive until pawl reseating, then clear while unloaded.

**Illustrative clearance strategy, not CAD release:** start at 5-mm height pitch. Let groove opening be 2.8 mm, grounded pawl thickness 1.2 mm, drive dog thickness 2.2 mm. Nominal dog backlash is 0.6 mm; grounded insertion window is 1.6 mm. After capture add a 0.2-mm unload displacement. Even if guide drag causes downward lag through all dog backlash, the pin ends 0.2–0.8 mm above its target seating datum, allowing pawl reinsertion followed by controlled downward seating. This only survives if:

`unload + max dog backlash + rack phase + deflection/alignment error < min ground insertion window`.

Using equal thickness for dog and stationary pawl often destroys this margin. The final design must calculate worst coherent tolerance bounds, not sum favorable nominal gaps. Two-mm pitch cannot inherit this interface; it needs a genuinely smaller tooth/opening and requalified load/print window.

**Packing escape:** wide cap on a narrow rectangular working stem. A nominal 5.6-mm X × 3.8-mm Y stem at 6.35-mm pitch provides 2.55-mm inter-row aisle; two opposing 0.6–0.7-mm-deep grooves leave 2.4–2.6-mm core. Put front ground pawls and rear drive dogs at different Z planes to avoid opposite-row hardware overlap. This remains a swept-CAD obligation across arbitrary neighboring heights.

**Manufacturing route:** short comb strips of perhaps 8–16 pawls printed flat with long compliant leaves that become vertical in assembly, and separate rigid supporting ledge/frame. An approximately 16–20-mm leaf can return a submillimeter tooth stroke at low strain; the service load must bypass leaf bending. Avoid tiny horizontal 5-mm leaves requiring several-percent repeated strain. Print orientation should put principal bending tension within layers. Flat-printing and a hard bearing stop require explicit geometry; they are not established by this description.

## Pass/fail qualification gates

The minimum useful prototype has at least four active-row columns with independent retained selection and an adjacent witness row. Use mixed signs and target heights, alternate masks, repeatedly revisit one pin, and leave a loaded witness unchanged. A manual shared drive is acceptable for mechanism proof, but a timing claim requires automatic mask writing and measured cycle times.

1. **Neighbor isolation:** all OFF witnesses retain both their pawl and height throughout selection, lift, release and empty return. Bound instrument resolution. A computed identical support datum removes a failure source; it is not proof against frame bending.
2. **Forced lowering:** impose measured drag exceeding pin gravity on one selected column and show the captured lower flank drives it down without first pushing an adjacent pin.
3. **Support transfer:** stop at each transition, identify actual contact carrying load, and reverse safely. With drive dog engaged, retract selected pawl only after unload; reseat pawl before withdrawing dog.
4. **Retention:** load pin after head withdrawal; observe creep/tooth damage and reproduce multiple cycles. Springs do not become bearing members.
5. **Tolerance/assembly:** print multiple columns/pawl positions from the same small comb; do not hand-fit away failures. Deliberately test end-of-comb and middle positions.
6. **Mask:** retain adjacent differing states through lift reversals, then clear/rewrite while drive coupling is mechanically unloaded.
7. **Playability:** real supported bases, cap gaps, cliff edges and a one-square corridor with nonzero-thickness walls; wall representation remains its own product gate.

For 4,096 independent repeated sites, 99.9% site yield gives 4.096 expected bad sites and only 1.66% probability of a fault-free array; 99.99% gives 0.410 expected bad and 66.4% perfect-array probability. This is an illustrative iid calculation, not a process model; common errors can be worse. Modular service, measurement and replacement are required. One carefully fitted prototype cannot establish whole-array yield.

## Remaining review boundary

No architecture is digitally or physically qualified by this report. The revised passive-pawl row head deserves dimensioned CAD and a decisive small test because it removes expensive resident actuators and the dual-datum neighbor motion mechanism. It must still survive actual swept packaging, return linkage, mask throughput, full hardware cost, and D&D wall/base geometry. Any final recommendation should label those separately, preserve failed candidate evidence, and stop at a real physical qualification boundary rather than bury it in a nominal timing pass.
