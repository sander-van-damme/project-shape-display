# E-304 — guided cone, captured row cam, column ceiling

**Scope:** one concrete bench experiment, not a replacement for DES-009. All performance below is calculated or geometric unless explicitly attributed to owner testing in [evidence-and-selection.md](evidence-and-selection.md). No E-304 physical result exists.

## Selected arrangement and mechanical AND

Each resident screw has a downward-facing 30° half-angle female cone. An always-meshed input gear and male cone share one sliding shaft. Two stationary journals locate that shaft; two separate stationary journals locate the output screw. A nonrotating follower presses the input through a small central thrust contact. A retaining lip withdraws it. Neither moving selector locates a rotating shaft.

A full-length row slides **2.54 mm along its length**. Its captured cam track lifts the follower bottom 1.4 mm. A perpendicular full-length column slides the same distance, changing the follower's upper stop. The stop is 0.1 mm above OFF in the low state and 1.1 mm above OFF in the high state. The cone seats after nominally 0.6 mm of shaft travel. The remaining 0.8 mm compresses the follower. This produces the following truth table:

| Row | Column | Input lift | Follower compression | Contact |
|---|---|---:|---:|---|
| 0 | 0 | 0 | 0 | Open |
| 0 | 1 | 0 | 0 | Open |
| 1 | 0 | 0.1 mm | 1.3 mm | Open; ceiling carries spring load |
| 1 | 1 | 0.6 mm | 0.8 mm | Cone loaded |

The 0.3-mm flat dwell at each end of the cam makes state retention less sensitive to end-stop positioning. The 1.94-mm sloping run gives a steep 0.722 rise/run. It is easy to manufacture but does **not** provide large force reduction. In normal operation unload rows before moving columns; this follows from the force calculation, not a need to search rotational phase. Loaded column release is included in the bench observations and must not be forced.

The compliant feature is justified here by an explicit conflict: a rigid row must finish its stroke when one column blocks a follower and another cone seats early. A rigid connection cannot satisfy different local stopping heights. The six-fold printed flexure supplies that accommodation without a separate spring, holder and assembly operation. It is a spring function with creep and fatigue risk, not complexity-free plastic. Other architectures may solve the conflict differently.

## Dimensions, constraints and force paths

The exact E-295 thread and pin meshes are retained from E-297's archived copies: Ø3.2-mm screw, 3-mm lead, 4.4-mm square pin, approximately 6-mm internal threaded region. Thread mesh is translated to Z55–71 mm; the pin is at Z61–79 mm at neutral. Positive screw rotation gives **negative** pin translation for this actual handedness. The bench range is ±1.5 mm, not a full-height terrain stroke.

| Function | Delivered geometry | Consequence |
|---|---|---|
| Input radial/tilt support | Ø1.8 shaft / Ø2.06 guides; centres Z33.6 and 38.6, span 5 mm | Two stationary lands; nominal diametral clearance 0.26 mm |
| Output radial/tilt support | Ø1.6 neck / Ø1.88 guides; centres 46.6 and 51.8, span 5.2 mm | Screw location independent of row/column deflection |
| Output axial support | Ø2.8 collar between lower journal top Z52.4 and upper keeper Z53.4; collar thickness .8 mm | .2-mm axial float; loaded cone pushes collar against the upper deck; gravity can place it on the lower deck |
| Input axial force | Central dome/pad, effective friction radius screened 0.267 mm | Lower drag than E-300's rotating contact near r 1.85 mm |
| Release | Follower cage around rotor flange, 0.3-mm running clearance | Positive withdrawal after lost motion; not gravity-only |
| Terrain antirotation | 4.7-mm square guides at 64.5 and 75.8 | 0.3-mm nominal total square clearance; both guide planes remain engaged over bench stroke |
| Cone | r 1.1–1.9 mm; cup OD4.6, half-angle 30° | Neighbor cup gap 0.48 mm; axisymmetric ideal contact |
| Permanent drive | Module 0.3, 12-tooth, 25° pressure angle; OD4.2 mm | Neighbor gear gap 0.88 mm; no selection-time gear meshing |
| Row structure | 4.6-mm width, 10.4-mm box core plus cam walls to 14.7 | 0.48-mm neighbor gap; two Ø2.2 stock channels |
| Column | Two parallel 1.1-mm rails; minimum roof depth 5.5 mm | Central slot clears follower; fixed transverse guides needed |
| Pin neighbor clearance | 5.08−4.4=0.68 mm | Actual retained pin, not an enlarged stand-in |

Axial load goes row cam → follower spring → central thrust contact → input cone → output cone → collar → stationary deck → frame → row guide. Torque goes common rack → permanent input gear → cone surface → output neck → retained screw thread → pin. Radial cone and gear reactions go to fixed journals. Columns carry the spring reaction at half-selected cells. Captured row tracks keep the follower bottom against the cam during release; the upper stem and feet have shared stationary guides.

The 2×2 frame opens on opposite sides of its two rows. Two shared keeper strips per row close the guide slots. A separate cam cap allows followers to be placed into their tracks rather than requiring threading every follower through a closed comb. These are real additional shared parts. The bench uses tape at external tabs for retention. A large array would need shared split guide decks/caps with accessible edge or top assembly and retained joins; the complete large-array assembly/service route is **not yet designed or qualified**. A fully inaccessible interior-pixel repair is unacceptable and remains a scale-up gate.

The mechanism consumes about 55 mm below the working thread and 79 mm to the neutral pin top in this coupon. The reinforced row costs roughly 13 mm more depth than a flat 1.6-mm strip. That is plausible for a tabletop base but a significant height penalty. No project evidence establishes that this is an accepted final enclosure height. A shorter optimized stack is deliberately not another prototype here.

## Force, torque and tolerance budget

The six-leg follower is analysed as a plane Euler–Bernoulli beam frame, constrained in lateral translation and end rotation. At nominal E=2 GPa, width 3.6 mm and thickness 0.40 mm, k=1.378 N/mm. At 0.8-mm compression F=1.102 N and peak linear bending stress≈19.1 MPa; half-selection at 1.3 mm gives 1.79 N and≈31.0 MPa. Curved joints, large displacement, print anisotropy, residual strain, contact and creep are not resolved. E=1.2–2.8 GPa and t=0.35/0.40/0.45 are tabulated. Vertical leg pitch is 0.9 mm; the lower neck clears the row tracks and connects the bed-supported foot and spring across a short printed bridge. The flat back is at Y=−1.8 mm so the six ligaments print directly on the bed. A small back web supports the column foot. The two thickness alternatives are diagnostic coupons; four nominal followers test simultaneous behavior. Do not keep half-selected followers compressed in storage.

For a cone under uniform wear, gross torque is T=μc F R/sinα, with R=1.5 mm and α=30°. The equivalent coefficient is 3μc Nmm/N. Unlike a flat disc, the cone increases normal force and can centre within guide clearances. It also introduces radial forces and possible wedging. The simple release screen μc<tan 30°=0.577 is necessary context, not proof against local staircase interlocking or adhesion.

A conservative working calculation subtracts input/output thrust drag and an explicit unknown lateral term:

`Tnet = F [3 μc − 1.437 μt − k_lateral] Nmm`, with k_lateral screened 0–0.25 Nmm/N.

At μc=.25, μt=.20, k_lateral=.10, F=1.102 N, **Tnet=.400 Nmm**. This exceeds E-303's assumed light starting torque .0597 Nmm and only narrowly exceeds its assumed moderate .343 Nmm. At μc=.30 the same model gives .565 Nmm; at μc=.15 only .0690 Nmm. Thus neither moderate torque nor even reliable light margin is established by CAD. Raising preload also increases half-selection force, creep and guide losses. E-303's loaded/imperfect 2.20 Nmm and obstruction 9.80 Nmm cases are outside this small clutch's intended capacity; slipping is preferable to forcing a blocked pin.

The cone contact area is approximately 15.1 mm². At F=1.102 N, total normal force 2.20 N gives a nominal average pressure≈.146 MPa. FDM ridges initially carry only part of that area; local contact stress can be much higher. Bidirectional friction capacity is symmetric in the ideal model. Reversal backlash comes mainly from the permanent rack and retained screw, and surface wear can change both grip and release. Slow manual testing controls heating; continuous motor duty is unqualified.

At 1 N/cell and μcam=.20, an 80-cell row needs about 102 N during its steep ramp, including an estimated sliding shoe term. At the nominal 1.102 N/cell this is≈113 N; eighty half-selected cells at 1.79 N approach 183 N. A two-cell bench stroke should be a few newtons. The load is mainly spring/cam reaction, not selector mass. Column gate friction may reach μ·ΣF (about 29 N at 80 half-selected cells) before roof-ramp effects. This is why columns normally change with rows unloaded. No claim is made that a cheap micro-servo can actuate a complete row.

Differential row/column deflection changes local compression rather than moving shaft centres. A±.15-mm height error changes nominal force by±.207 N. That allowance is related to the 0.8-mm preload and 0.3-mm cam dwell, not an arbitrary precision requirement. A blocked follower compresses further, so nearby followers can still travel **if** the selector completes its stroke. The actuator and support must still withstand the extra force; compliance cannot eliminate total reaction.

Tolerance deserves separate caution. Input radial clearance is 0.13 mm and output 0.14 mm. Opposing radial offsets can total 0.27 mm before tilt. Individual worst-case tilt screens are roughly 0.26/5=3° and 0.28/5.2=3.1°. Their simultaneous extremes are not an operating prediction, but can consume the 0.6-mm axial opening gap. The supplied actual-mesh phase/eccentricity/tilt sweep reports first contact rather than silently assuming coaxiality. Fixed guides bound wobble; they do not prove freedom from rubbing. Nominal,−.10 and+.10-mm input shaft variants test this fit tradeoff. Tightening guides without print evidence is not a solution by assertion.

## Complete repeated mechanism and scale costs

| Item/function | A1 guided cone, selected | Two individually guided cones in series | Guided dog plus local lost motion |
|---|---:|---:|---:|
| Printed moving bodies per pin, including terrain pin | 4 | 8 | 5 |
| Purchased local parts | 0 | 0 in all-printed version | 0 with integral compliance |
| Independent local elastic functions | 1 | 2 | 1 |
| Rotating bodies | 2 | 3 | 3 |
| Radial support planes | 4 | At least 6 | At least 4 plus sliding spline guidance |
| Separate local thrust/release interfaces | Central input pad, output collar, withdrawal lip | Two clutch reactions, intermediary thrust/release | Axial dog reaction, follower and spline interfaces |
| Pin guide planes | 2 | 2 | 2 |
| Components for 6400 pins before shared hardware | 25,600 | 51,200 | 32,000 |
| Main residual risk | Friction margin, guide rubbing, flexure creep | Extra drag, stack height, doubled adjustment | Angular engagement conditions and spline friction |

The four A1 bodies are pin, output-screw/cup, input-gear/cone and follower. They contain three rigid motion functions (pin translation, output rotation, input rotation+axial sliding) plus follower deformation/translation. Count the input's two degrees of freedom and the six bending ligaments explicitly; integrating them into four STLs does not remove those functions. The stationary frame supplies repeated sliding-bearing surfaces without 6400 separate bearing inserts. Each cell still needs at least four part placements, threading the pin, and checking free motion, grip and release. At 10–30 seconds per cell that alone is 18–53 hours for 6400 cells, excluding shared assembly; this is an illustrative labour sensitivity, not measured work time.

At 80×80, long functional members are 80 row bases+80 caps+80 columns+80 drive racks+160 keeper strips=480. Add two common drive/bus functions, fixed-guide components G, edge actuators and retention hardware. Ideal continuous-part count is therefore 26,082+G before edge hardware. Four printed sections per long member would instead give 27,522+G before joins/hardware. This segmentation is **passive manufacture of one continuous selector**, not separately controlled modules. End-to-end alignment and cap retention need evidence. Two 2-mm carbon rods per row require 160 cut lengths, about 430 mm including edge attachments:80 one-metre stock rods if two lengths can be cut from each. Rod price is€156 ex VAT at the observed 20+ tier, or€244 at single-unit prices; cuts and shipping are extra. Columns initially use printed rails with fixed supports; adding their reinforcement would increase cost.

| Full-array budget line | Illustrative allowance | Basis / limits |
|---|---:|---|
| Printed material | €120–300 | 6–12 kg at€20–25/kg; covers cells, large shared guides, waste; not a sliced full-array BOM |
| Row reinforcement | Steel≈€80 incl listed VAT; CF€156–244 ex VAT | 80×1m rods, two cuts each; steel is conservative for the final 183-N force case |
| Common bearings, joins, retainers, drive stock | €75–250 | Budget allowance; common-drive and guide assembly remain unresolved |
|160 selector actuators/transmissions | €800–2,400 | €5–15/axis placeholder, **not a vendor quote or force-qualified actuator** |
| Shared motor/transmission | €50–200 | Force/duty dependent placeholder |
| Power, drivers, wiring | €100–400 | Architecture-dependent allowance |
| Total excluding labour, shipping and tax normalization | **about€1,300–3,800** | Broad screening range; not a purchase-ready cost claim |

The source-price table uses mixed tax bases explicitly. The actual prototype mesh volume and print usage are separately recorded; do not infer a complete manufacturing quote from four cells. The two-series design roughly doubles the local mechanism parts, adds at least one more rotating assembly and stationary support plane pair, and raises repeated material/assembly cost. It could still win if single cones can use fewer stressed interfaces, but no evidence currently offsets those penalties. Printed-only supported row boxes save the corresponding rod cost; they merit the included short beam comparison before any purchase.

## Shared power and what 5.08-mm feasibility means

The bench has two permanent racks joined to one shuttle and one 36-tooth hand pinion. It drives all four input rotors in the same direction, even when no clutch is selected. No individual hand-positioned input substitutes for common-drive engagement. Each 10° knob notch corresponds to 30° input rotation and 0.25-mm ideal pin travel. The larger side pinion is outside the raster.

For an 80-wide field the same principle is a full-length rack per row, all coupled to one bus. At moderate assumed screw torque .343 Nmm, load-only rack force is Nselected×.343/1.8:15.2 N for 80 loaded pins, 1.22 kN for 6400. The corresponding 5.4-mm pinion torque is .082 and 6.59 Nm before drive and clutch losses. All unselected input bearings still rotate; their drag is unmeasured. These numbers prevent an unjustified claim that one tiny motor solves the array. No update-scheduling research is repeated.

A40-mm pin stroke with 3-mm lead requires 83.8 radians of screw rotation and 150.8 mm of rack travel; a rack covering the 406.4-mm field would need roughly 557 mm plus end margins. The bench provides a short travel representative common drive, with a marked rack window−9.5 to+2.8 mm about the CAD assembly position. Full phase testing starts at−8.5 mm and resets with clutches OFF; the input cannot rotate indefinitely. A different continuous common transmission is possible, but is not designed or claimed here.

**Local packing is plausible:** actual retained threads, four neighboring cups/gears, two guide spans, shared selectors and fixed decks fit at 5.08-mm pitch in the exported assembly. **The complete 80×80 mechanism is not yet demonstrated manufacturable or economically superior:** full-stroke common power, large guide-deck assembly, thermal/print variation, selector force, repair and lifetime remain unresolved. The only next evidence sought is the small physical result defined in the owner pack. Development stops for an explicit owner decision afterward.

## Same-assumption comparison of the strongest candidates

For a common screening target 0.343 Nmm, μc=.25, μt=.20 and lateral allowance .10 Nmm per newton, the single 30° cone requires F≥.946 N per cell. The chosen nominal linear spring prediction is 1.102 N. The corresponding flat annulus has coefficient 1.5μc−1.437μt−.10=−.0124 Nmm/N: under this adverse drag assumption **more preload cannot create a useful net margin**. At μt=.10 it instead needs 2.61 N/cell; it remains a real candidate if measured thrust drag is low. “Half the gross torque” must not be mistaken for merely double the net force.

Two identical cones in series require both stages to exceed the target, not half the target each. If the extra intermediate assembly contributes a separately assumed .05 Nmm drag, each stage would need at least 1.08 N in the same screen; actual force placement changes that result. Each full row/column then directly operates 80 preload functions, approximately 110 N/ramp at the present cam ratio. A has one controlled normal force, with its highest approximately 183-N row case arising from blocked half selections; B removes the roof-gate contact but adds the second preload, intermediary journals and assembly.

A two-dog clutch at r 1.5 mm transmits .343 Nmm with total tangential reaction .229 N. Even two .24-mm² nominal load faces would have only .48-MPa average shear/bearing stress. That attractive torque scale does **not** answer whether the teeth seat. Its minimum clearance and engagement force depend on the keyed sleeve and chosen indexing profile. The repository's roughly .3-mm double-D diametral allowance did not prevent wobble; A removes that fit, B and the selected A3 concept retain at least one extra sliding torque fit. A3 therefore remains unranked for reliable stationary-phase operation rather than being assigned a fictitious success probability.

All candidates can use the same full-length supported beam. None earns an unsupported 400-mm span or automatically cheap actuation. B adds at least 6,400 intermediate shaft assemblies and 6,400 more compliant followers compared with A, before sleeve parts; guide surfaces and friction scale with them. A2's component count/cost matches A but its pressure or bearing design changes. A3 has at least 6,400 additional sleeves and repeated sliding connections. For all three, every local fit would need inspection and replacement access; only A receives CAD and one print in this assignment.

### Explicit adverse guide-clearance corner

At cone height Z42, an input journal centre at +.13 mm in its upper guide and−.13 mm in the lower guide extrapolates to+.307 mm. Opposite output offsets (lower−.14, upper+.14) extrapolate to−.388 mm. The relative cone eccentricity can therefore approach .695 mm in this deliberately adverse rigid-clearance corner, exceeding the nominal .6 tan 30°=.346-mm radial opening allowance. The mesh sweep includes .4-mm/3° and .7-mm/6° imposed cases to expose the resulting OFF interference. **The delivered tolerances do not guarantee drag-free disengagement at every possible guide-clearance corner.** Cone centring under load and ordinary gravity/rack forces may prevent that corner in practice, but this is not established. The fit variants and the OFF shared-drive test are essential; an owner result showing rubbing is a no-go for this exact fit, not something to “solve” by forcing or phase searching. A production clearance/guide-length revision is deliberately left to a decision after the physical result.

The output collar has 0.2-mm axial clearance between its two stationary faces. The nominal loaded CAD places it at the upper face. Under gravity it may fall 0.2 mm; ideal coaxial initial contact then begins at input lift 0.4 mm and final loading lifts the output back to its upper stop. This small terrain-height jog is observable and must be recorded. With the column OFF and input at 0.1 mm, the remaining nominal gap can be 0.3 mm. Combining axial float with adverse radial offset further reduces OFF clearance: the .27-mm offset sweep's roughly .13-mm first-contact lift becomes roughly−.07 mm after a .2-mm output drop. The broad guide tolerances therefore need physical fit evidence; nominal no-collision results are expressly not a worst-case tolerance qualification.

At .343 Nmm, the solid 1.6-mm output neck has nominal torsional stress `16T/(πd³)≈.43 MPa`; the thin teeth, printed interfaces and guide fit are more credible first failures than bulk shaft torsion at this load. A12-tooth 25° full-depth involute is above the ideal unshifted undercut screen `2/sin²25°≈11.2 teeth`. This geometric result does not guarantee printable tooth tips: the .3-module pitch thickness after backlash is about .39 mm and is explicitly checked in the Arachne toolpaths. A .12-mm layer on a 30° cone produces an ideal radial staircase step of about .069 mm, so the smooth-cone friction model is only a starting approximation.

### Physical component total, including stock and edge functions

The preceding 26,082+G figure counts printed parts/functions before stock and actuators. Add 160 cut reinforcing rods and 161 actuator assemblies (160 selector axes plus one shared rotary source in the explicit direct-actuation budget): **26,403+G+H total component assemblies**, or **27,843+G+H** with four printed sections per long member. H denotes unresolved fasteners, rod-end retainers, segment joins and electrical hardware; motor internals are not disassembled into fictitious individual-part counts. G is explicitly unknown because the full stationary guide structure is not designed. An exact finished-array total cannot honestly be given at this stage. The complete bench assembly contains 29 retained printed parts, plus ordinary retention tape; the extra four fit/preload variants and three structural-test pieces are not installed simultaneously.

For B, replacing the column roof with a second captured cam also adds 80 column caps, so a comparable shared printed count is 560 long functions rather than 480. Its continuous printed subtotal becomes 51,762+G_B. If both loaded selector sets receive two rods per selector, add 320 cut rods and the same 161 actuator assemblies: **52,243+G_B+H_B**, before sectioning. This explicitly includes the intermediate rotating assembly in the eight local bodies. Unresolved guide/retainer counts are retained as variables rather than hidden zeros.

### Unselected height retention is also unproved

No per-pixel holding brake is hidden in the four-part count. With lead 3 mm and mean diameter 2.3 mm, the simple 90° V-thread self-locking threshold is approximately `μ_thread ≥ [3/(π·2.3)] cos45° ≈ .294`. E-303's light running scenario predicts a small negative lowering torque (about−.0021 Nmm after its assumed guide/thrust/drag terms), so unselected loaded pins may backdrive. The owner's smooth hand-fit result did not measure retention. The bench therefore observes unloaded and lightly loaded pins with every clutch OFF before crediting isolation. Rapid gravity-driven descent is a no-go; small drift is recorded according to the project's present priorities. Adding a brake would change repeated components and cost and is not assumed or developed in this assignment.
