# Workstream A — reusable mechanical selection

**Preserved initial investigation.** Subsequent timing and hardware reviews rejected the traveling-head recommendation. The DES-008 main report and final disposition govern the current recommendation; these notes retain the alternatives, mechanisms and reasons tested along the way.

Investigation date: 2026-10-14. Basis: current main b23ed12, AGENTS.md, mission/current priorities, E-220, E-228, E-240/241, A-025 and ADR-020/021/022. This is a bounded architecture investigation, not physical validation or a complete CAD release.

## Decision

The best selector family to develop is **a reusable passive punched-gate register, read by common compliant platens into independently grounded binary output keys**. A small number of serial knitting-style writers programs the gate register. Two keys per lane separately control a moving capture dog and a stationary ground-pawl release. The terrain load is carried by the ground pawl or the lift dog; neither the writer nor the mask flag carries terrain weight.

The complete-machine winner is not yet proven. This family is credible because it replaces hundreds of electronic selectors with tens of shared writers while keeping passive precision parts accessible in a few removable heads. It adds real repeated rods, springs, output keys and positive keepers. Their friction, fatigue, assembly and update time must not be omitted.

Six 64-lane heads have 384 flags, 768 reader rods/compliance elements, 768 output keys, 12 common keeper combs, 12 common reader platens, and 48 electrical writers if eight writers/head. Eight heads have 512/1024/1024/16/16/64 respectively. Add one ground pawl/site (4096 at6.35mm), lift/transport/writer/cam motion, guides, returns and positive lift arrest. The site pawls should be made as replaceable molded/printed/formed comb strips rather than 4096 individually assembled servos, but a comb is not proof of 4096 good pawls.

## Distinct families screened

| Family | Mechanically explicit selection | Bidirectionality/retention | Decision-changing weakness | Disposition |
|---|---|---|---|---|
| Electronic Jacquard | Per-hook electromagnet selects hook for common knife | Common knife lifts; hook/double-lift geometry supports textile load | Still one electronic selector/output; industrial source does not erase repeated component count | Reject as direct cost escape; retain load amplification principle |
| Crossed row/column rigid supports | Either row or column comb holds pin; releasing one row and selected columns frees an arbitrary row subset | Positive third-face moving finger can raise/lower; periodic grooves retain height | Independent review identified changed support datums moving unselected cells when support changes. No common global bias fixes arbitrary local datum error | Park until a genuinely compensated datum-transfer geometry exists |
| Resident per-pin bistable clutch plus serial writer | Scan stationary output latches; later apply common drive | Requires 4096 or6400 latches plus local load holding; screws can retain position | Whole field must be reprogrammed for each displacement bit. Thousands of small mechanisms, scanning time and screw torque remain | Secondary comparator, not preferred |
| Traveling row head with passive mask and fixed local pawls | A few reusable flags distinguish selected dogs and ground-pawl release; unaffected local pawls stay on same datum | Captive dog tooth in periodic groove drives both directions; fixed pawl supports at rest | Reusable key/reader/keeper complexity and serial writer throughput; physical support interface remains untested | Preferred selector topology for current architecture |
| Pure row/column mechanical AND without memory | Row opens physical aperture, column bar acts only through open aperture | Selection can have no ghosts when other rows remain physically closed | Two rows opened with different patterns cause cross-intersections. One-row serialization returns; no free arbitrary subset parallelism | Useful addressing element only |
| Direct shared screw head with passive clutch mask | Same reusable register can engage positive drive clutches; screw threads support | Reverse shaft drives down; thread friction/self-lock must qualify | Faster selection does not solve DES007 strip traction or screw lead/torque; still repeated spindle interface | Keep as fallback after current screw evidence, not lead |

## Sources and exactly what they establish

1. [Stäubli LX PRO](https://www.staubli.com/us/en/textile/products/jacquard-machine/reliability-power-saving-lx-pro.html) describes common knife frames, 4608/6144/7680 hooks and MX PRO electromagnet selection. It establishes proven industrial shared power with private hook selection, not affordable Shape Display selection.
2. [US4038837A, Jumberca](https://patents.google.com/patent/US4038837A/en) describes a needle jack cocking the shared selector and an electromagnet retaining the selector in contact for the next jack. Several selector levels increase available selection time. Crucially, its description acknowledges tight tolerance/contact problems and uses a compliant insert. Inference: use main-machine motion to supply selection work; do not assume a small solenoid pulls across its entire gap in10ms.
3. [US4901541A](https://patents.google.com/patent/US4901541A/en) describes separate raising/lowering cam faces and magnetic jack retention. It illustrates positive cam paths and constrained selector presentation; it is not a load-support or cost qualification for terrain.
4. [US3953988A](https://patents.google.com/patent/US3953988A/en) describes a movable electromagnetic selection carriage for a flat needle bed. A shared moving selector is a physically established mechanism family, not merely an abstract addressing analogy.
5. [Kniterate official specifications](https://www.kniterate.com/product/kniterate-the-digital-knitting-machine/) list3.63mm needle spacing and800mm/s in the technical table; the same page's older FAQ says400mm/s. Those give4.54 and9.08ms per needle opportunity. These are supplier specifications with an internal revision inconsistency, **not a measured10ms switching guarantee for a cheap solenoid or printed Shape Display register**. No inspected source establishes our writer's force, stroke, life or cost.

## Gate and writer geometry

Proposed head pitch6.35mm. A vertical X–Z gate sheet sits in a grounded tray. Gate width4.0mm, X travel1.8mm, tray working width5.8mm, leaving0.55mm between adjacent lane envelopes. Gate thickness2.0mm and height12mm are starting dimensions. Two1.6mm through-holes run in Y and are spaced6mm in Z. Reader rods are1.0mm diameter. ON aligns both holes; OFF shifts their centers1.8mm.

Nominal ON radial clearance=(1.6−1.0)/2=0.30mm. Nominal OFF edge clearance=1.8−(1.6+1.0)/2=0.50mm. A two-part combined hole/rod/registration error of0.20mm leaves0.10/0.30mm. These are rigid bounds, not process priors. A larger error may jam ON or cause a false read. A broad steel-backed OFF land should support the entire rod contact, not a thin hanging lip.

A wire/sheet-spring detent engages two pockets1.8mm apart. Its force is provisionally0.2N; neither this force nor print life is measured. A global reset comb pushes all flags OFF only with both reader platens withdrawn. Writers set selected flags ON. Eight vertical writer needles at50.8mm spacing scan positions0,6.35,...44.45mm; each needle serves eight flags. A wedge at the flag top converts the needle's Z stroke to the flag's X stroke. Needle clearance from adjacent flag must be retained over acceleration and carriage yaw.

Knitting-style continuous scan is preferable to eight separate stop/settle moves if the fast selector is qualified. At400mm/s, adjacent opportunities are15.875ms. Traversing44.45mm at400mm/s and8000mm/s² takes161.125ms rest-to-rest, before erase/readback/end settling. At800mm/s and20000mm/s² it takes95.563ms. Thus **0.1s complete mask writing is an aggressive assumption**, not a default. A reasonable first modeled range is0.15–0.25s per mask and a deliberately slower physical coupon.

A direct solenoid design must budget current rise, mechanical stroke, bounce and return. A cam-cocked selector whose coil only holds/releases in contact is the preferred industrial adaptation, but requires actual component construction. A servo can demonstrate the topology slowly without claiming final timing.

## The two-key reader: concrete force paths

Each lane has two independent Y-sliding output keys:

* A-key positions a vertical C-channel selector key beside the moving dog. The dog follower is captured between the channel faces and can slide in Z throughout the lift stroke. Moving the A-key changes dog engagement; the channel then preserves engagement throughout Z motion.
* B-key moves the fixed-z release cam of the resident grounded pawl. It remains at fixed Z while the dog/lift travels.

A gate has two holes but does **not** simply carry two rigid hooks attached to independently moving keys. That tempting drawing has an unmodeled joint. Instead reader A and reader B independently pass through the gate holes and push their own keys.

Each reader rod is retained by an extension collar in its common platen and is backed by a preloaded compliant element. The platen advances far enough to reach the final ON key face. An aligned ON rod passes the gate; an OFF rod hits the grounded gate and compresses its own element. A key already ON presents its face farther away than a key initially OFF. With sufficient platen travel, an ON rod first pushes an OFF key through its full travel or simply preloads an already-ON key. The final force must exceed key-return force plus cam/friction force at the worst condition. OFF rods impose their full blocked compression force on the gate backing and the common platen.

**This compliance is a significant component**, not a0.1mm allowance. The blocked/pass difference may be3–4mm. Plain high-rate short springs make the blocked forces excessive; low-rate preloaded spring arrays need space. For example a hypothesized reader preload1N and rate0.2N/mm gives1.04N with0.2mm final contact compression, versus1.84N at4.2mm blocked compression. A64-lane all-OFF platen then reacts118N. The example demonstrates accounting, not a qualified spring. Printed flexures need fatigue/creep evidence; formed spring strip adds fabrication. The keeper lets these reader forces be removed during terrain movement.

### Positive common key keeper

Use a single grounded keeper comb per A/B key row. Every key has two identical transverse notches whose centers are separated by the ON travel. The same comb can seat when any key is OFF orON. Suggested key travel3.0mm, notch width1.6mm, keeper tooth width1.0mm, notch depth0.6mm: nominal insertion margin±0.3mm and solid web1.4mm. At only1.8mm key travel the same notch widths leave0.2mm web, which is a poor printed detail. **Do not silently use1.8mm flag travel as the output-key travel.**

Reader preload must take the spring/cam force before the keeper withdraws. Once the key has settled at an actual endpoint, the keeper seats fully before reader withdrawal. A key stuck midstroke obstructs the common keeper; drive torque limiting and a visible keeper-position check should inhibit lifting/release. A single keeper sensor does not independently prove every tooth if the comb bends.

The A-key's3mm translation must map to approximately0.8–1.0mm dog lateral engagement using a real cam/lever/slot. Directly translating the dog3mm into a5.6mm pin is not permissible. The final C-channel track must have a straight retaining section spanning the whole Zstroke and a rigid reaction path, not just a spring pushing a beveled tooth. This ratio/conversion geometry is a remaining CAD obligation.

## Admission, movement, retirement and reset

At rest each pin's original ground pawl supports it; A/B keys areOFF and locked. Unselected pins never transfer from that datum.

1. Write admission mask with readers home and terrain grounded.
2. Advance A-reader. ON rods preload selected keys. Withdraw A-keeper, let selected A-keys move toON, reseat keeper, withdraw A-reader. Dog enters periodic groove and is positively retained by its key/channel.
3. Lift a small measured take-up distance to unload selected ground pawls. This moves only selected pins. Its displacement is included in commanded height accounting.
4. Advance B-reader, withdraw B-keeper, drive selected B-keysON to release their ground pawls, reseat B-keeper, withdraw reader.
5. Move the selected terrain with positive dog capture and a positively arrested lift. Both readers are now absent; flag memory may be reset and written with the next **remain-active** mask during movement.
6. Stop at a target level. Advance B-reader through remain-active ONholes to preload continuing B-keys. OFF gate lands block reader force to retiring B-keys. Withdraw B-keeper: retiring keys spring-returnOFF and allow their ground pawls to seat; continuing keys stayON under reader force. Seat B-keeper before withdrawing reader.
7. Lower by the measured seating allowance to load retiring ground pawls. Continuing pins stay under dog support and follow this small reversal, accounted in motion/target schedule.
8. Read A with the remain-active mask, withdraw A-keeper; retiring A-keys returnOFF and withdraw unloaded dogs while continuing keys remainON. Reseat A-keeper, retract reader.
9. Continue next height segment. End with all keysOFF/locked, all pins on their own ground pawls, then return empty lift and index row.

Downward motion uses the same captive dog and release/retirement sequence with vertical motion reversed. Gravity following alone is not credited. A positive lift brake or self-locking/arrested drive must hold the load whenever local pawls are open.

Potential failures: gate false-pass selects wrong output; dog does not fully capture before B release; pawl does not unload; keeper seat blocked by an intermediate key; C-channel ejects or jams during Z motion; same row's released pins have inadequate pin-column guidance; printed pawl hinge carries long-term load instead of its hard backing; reader springs overload gate; gate reset contacts a rod left in the hole. These are architecture qualification questions.

## Timing and economic interpretation

The reusable-memory architecture makes tens rather than hundreds of electronic writers plausible. It does not guarantee30s. Writer scans can be overlapped with lift motion **only after both output keys are positively locked and both readers are physically withdrawn**. Admission and the first mask of a row are unavoidable. Each retirement needs B preload/unlock/settle/relock/withdraw, terrain seating, and A preload/unlock/settle/relock/withdraw. A single camshaft may sequence common motions, but cam travel and dwell are finite.

For a5mm/9-level comparator, signed subset strokes±{5,5,10,20} cover every40mm difference monotonically with8 masks and80mm loaded+80mm empty travel. This is valid but may be slower than the parent's retain-and-retire schedule. At200mm/s and8000mm/s², this subset scheme takes1.2s motion/row before writing/transfers. At2000mm/s² it takes2.166s/row. Six banks with11rows already spend13.2/23.8s on motion alone. The fast scenario only approaches30s with overlap and short transfers. Eight banks provide more margin at extra hardware cost. Five-level±{10,10,20} is a comparator, not approved coarse product resolution.

A48-writer/24-shared-axis assumed allocation can fit roughly$1000–1800 only with inexpensive selector construction, shared cam sequencing and low-cost rails/frame. This is not a supplier-backed BOM. At$10/writer the writers alone cost$480; at$3 they cost$144. At$25 per complete shared motor/driver/axis24axes cost$600 before frame, pins, gates, springs, brackets, guides and power. Thus the$1500 demonstrator target is plausible enough to investigate but not demonstrated. Assembly count and repeatable manufactured yield can dominate materials.

## Cheapest decision-changing prototype

Build4adjacent pins at6.35mm with fixed grounded pawls and one common lift, fourA/B key pairs, two keepers, one4flag gate strip, and hand-operated common reader platens. Use repeatedON/OFF/ON/OFF and OFF/ON/OFF/ON patterns. Demonstrate admission, positiveup/down, partialretirement and arbitrarykeymixtures while neighbors retain their originalgroundpawls. Place a visible witness or dial indicator on untouchedpin. The prototype tests support isolation and key/keeper logic before committing to a high-speed writer or64lanes.

Then one8flag writer-only coupon tests actual serial selection. Record commanded pattern, observed retained state, contact force,20/10/5ms opportunity tests,1000cycles and failures. No physical timing or wear pass is currently claimed. These are new architecture-changing questions; the owner's completed short-thread fit need not be reprinted.

## Updated disposition after independent timing review

The parent throughput workstream reports the retain-and-retire implementation at62.32s for8banks/8writers with stopped indexing, and48.38s with continuous writing;16banks/32writers reaches26.33s but restores512 electrical writers. Those results supersede this workstream's early optimistic timing screen. **Park the reusable serial binary register as the leading full-machine selector.** Preserve its explicit support and reader topology as a mechanism demonstrator/fallback; do not optimize its automated CAD merely because its component count is lower than DES007. The exact reproducible timing source is owned by workstream C/the integrated package; these numbers are communicated results, not independently rerun here.

## Five-minute escape screen: mechanically enabled resident matrix

A nonmagnetic matrix can avoid both ghost intersections and force against63blocked flags per column. Let64column setter bars run across all rows. Each bar shiftsX by1.8mm. Each row contains a64flag cassette that liftsZ by~1mm into setter forks only while that row is addressed; other rows remain below the forks. The column bars select64bits simultaneously, row cassette lowers, nextrow rises. Detents retain bits after lowering. Main terrain read waits until every row cassette is fullyhome. The cassette Zmotion is command-only; it cannot be attached directly to a load-support datum.

Counts:64columnsetter actuators,64row-enable mechanisms (or one traveling/rotary row-enablecam),4096resident flags,64liftable cassettes and theirguides/returns. There are no magnetic halfselectthresholds. Positive clearance between disabled flags and setterforks substitutes a finite geometry obligation. At50ms percomplete row-enable/set/disable transaction, a64row mask costs3.2s, eight masks25.6s before terrainmotion. At25ms it costs1.6s/mask, but three finite motions in25ms are unqualified. A stepped traveling rowcam already spends~56ms moving6.35mm at8000mm/s², before contact; continuous cam presentation could remove stopping but has dwell/force constraints.

This matrix reduces writer electronics but requires resident capture/release mechanisms across the complete field for a global lift. It therefore trades reusable head complexity for4096passive precision sites and an array-wide loaded structure. It is a bounded candidate, not an architecture pass.

An alternative is to write **absolute target heights once** into resident lightweight vertical rods:64shared low-load linear setters, one mechanicallyenabled row atatime, nine5mm positions over40mm. At300mm/s and8000mm/s², a40mm rest-to-rest setterstroke takes0.1708s;64rows11s beforeenable/capture/lock.64actuators are potentially affordable comparedwith512, and5mmcommandsteps allowmillimetreclearance. But4096targetrods/retentions and a mechanically complete equality/target-stop reader remain. The prior ADR016 failure is specific to a44,800slider embodiment, not an impossibility proof. The decision-changing question is whether one simple targetrod can positively terminate a terrain movement and reset its reader without disturbing retained outputs. No such complete geometry was established in this bounded screen.
