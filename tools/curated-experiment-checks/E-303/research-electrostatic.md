# Electrostatic friction: evidence, circuit physics and a buildable stack

[Experiment](engineering-report.md) · [Dimensioned concept](concepts/B-floating-electrode.svg) · [Concept CAD](concepts/B-floating-electrode.scad)

Research checked 23 October 2026. **Recommendation: retain B as an analytical alternative; defer energized hardware.** Low leakage power is credible. A cheap, durable, nearly drag-free, continuously rotating clutch at 5.08 mm pitch is not established. B2 removes the output electrical contact but adds a second input electrode; it does not remove all rotary electrical contacts.

## Primary evidence and its limits

| Original study / evidence | Relevant result |
|---|---|
| [Lee et al., DOI 10.1002/aisy.202500625](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aisy.202500625), online September 2025, issue March 2026 | Measured 20 mm diameter × 1.5 mm, 0.4 g; locking torque 83.4 mN·m at 420 V; OFF 1.1 mN·m; 2.94 mW. Engagement 30 ms, release below 0.8 s. |
| Same study, fabrication and limitations | Laser-patterned flexible metallized PET, 9 µm blade-cast P(VDF-TrFE-CTFE) dielectric, conductive-fabric rotary contacts. Layer fracture and wire breakage occurred. **This is not ordinary PET on an FDM disc.** |
| Same study, unresolved gap notation | Selected geometry lists h = 150 µm; discussion separately gives 17.5 µm clutching-layer gap. We do not equate these quantities or infer a verified coating permittivity/contact area. Supporting ZIP could not be inspected. |
| [Diller, Collins & Majidi, 2018](https://journals.sagepub.com/doi/10.1177/1045389X18799474), measured linear clutches | Simple Coulomb theory did not reproduce material/thickness/age effects. Residual OFF force increased during fatigue. These experiments support treating our electrostatic friction estimates as screening models, not predicted measured torque. |
| [ESTAT patent EP4337874A1, paragraphs 0051–0054, Figs. 11–14](https://patents.google.com/patent/EP4337874A1/en) | Describes split powered electrodes attracting a floating conductor, balanced coverage, and capacitance/resistance effects. **Patent disclosure, not a measured 5 mm rotary prototype.** |
| [ESTAT rotary patent US12407276B2](https://patents.google.com/patent/US12407276B2/en) | Flexible plates and ceramic dielectric are proposed to improve contact and release. Ceramic deposition/anodization is additional processing; patent language is not a commodity-film performance guarantee. |

The published locking torque is not a certified slip limit for a blocked screw. We have no new physical clutch results.

## B1: ordinary two-terminal clutch

A dielectric-coated input electrode faces an independently rotating output electrode. With both connected, their potential difference is prescribed. For an annulus with radii `ri, ro`, active area `A = π(ro² − ri²)` and uniform pressure,

`r_eff = (2/3)(ro³ − ri³)/(ro² − ri²)` and `T = μ p A r_eff`.

If coatings have thicknesses `tj`, relative permittivities `εrj`, and a microscopic air gap is `g`, define `s = g + Σ(tj/εrj)`. Then

- `C = ε0 A / s`;
- `E_air = V/s`, `E_dielectric,j = V/(εrj s)`;
- fixed-voltage force closing the air gap: `p_gap = ε0 V²/(2s²)`;
- stored energy `U = CV²/2`; an ordinary resistive complete charge/discharge cycle draws `CV²` from the supply; leakage consumes `V I_leak` continuously.

The often quoted `ε0 εr V²/(2t²)` instead differentiates a uniformly dielectric-filled capacitor with respect to its dielectric thickness. It is not the same mechanical boundary condition as opening an air gap between coated surfaces. At `g → 0`, the ideal air-gap expression contains `εr²`; this does not prove that every square millimetre of a real rough interface achieves that traction. Air voids, incomplete contact, viscoelastic adhesion, film bending and peeling can dominate. Both expressions are retained as clearly labelled sensitivity models in the calculations.

The microscopic gap is electrically important even when it is mechanically invisible. With 12 µm PET and assumed `εr = 3.25`, `t/εr = 3.69 µm`. A 5 µm air gap reduces ideal gap-closing pressure to 18% of the zero-gap value; 20 µm leaves 2.4%. Printing a smooth-looking support is not sufficient evidence of micrometre conformity.

## B2: floating conductor over split input electrodes

Let powered input nodes be `V1` and `V2`, capacitances to the floating output `C1` and `C2`, output net free charge `Qf`, and parasitic capacitance to surroundings `Cp` at `Vp`. Charge conservation gives

`Vf = (C1 V1 + C2 V2 + Cp Vp + Qf)/(C1 + C2 + Cp)`.

The gap fields are set by `V1 − Vf` and `V2 − Vf`, not by the entire supply voltage twice. If `Qf = Cp = 0` and identical coatings cover equal halves, `Vf = (V1 + V2)/2`. Each half sees `ΔV/2`, total normal force and torque are **one quarter** those of B1 using the same total area, coating and terminal voltage. Terminal capacitance is `Ceq = C1 C2/(C1 + C2) = Cfull/4`. Stored energy is `Ceq ΔV²/2`.

More generally, for identical gaps and area fraction `f` versus `1−f`, `Ceq = Cfull f(1−f)` and the force ratio to full-area B1 is `f(1−f)`, at most 1/4. The voltage on a smaller-area patch increases, so asymmetric coverage can overstress its dielectric while total force falls. Doubling B2 terminal voltage restores B1 fields and ideal force, but raises supply/switch/track insulation requirements; it is not free torque.

With leakage, the late-time floating potential follows conductance balance instead: `Vf = (G1 V1 + G2 V2 + Gp Vp)/(G1 + G2 + Gp)`. The initial capacitive midpoint need not persist. Trapped surface charge is not removed simply by commanding both input nodes to zero. For an initially neutral, perfectly insulating conductor the induced charges redistribute on discharge; real charge injection, triboelectric charging and dielectric polarization invalidate that idealization.

### The two rotating powered connections

Our concrete B2 concept uses two insulated copper tracks on the **input hub**, two stationary conductive-fabric brushes, and two insulated links to the split input sectors. Both tracks rotate with the shared-drive rotor. The floating output carries no wire. The two internal links require covered insulating channels in the input shaft/hub and four electrical terminations; their exact routing is not solid-modelled. Each stationary brush must terminate directly on a module PCB pad, or add two fixed insulated leads to the part count. The concept counts the PCB as shared selection electronics, not a free mechanical part. A common conductive input drivetrain could replace one local return track only after proving electrical continuity through every joint and insulated bearings/support boundaries. It cannot distribute independently switched second-electrode potentials through a single undivided metal shaft.

Putting both powered electrodes on a stationary board avoids rotary electrical contacts but attracts the output toward ground: that is primarily an electrostatic **brake** unless an additional torque-carrying rotating interface is supplied. It is not this clutch.

## Materials and manufacturing

| Component | Practical choice / limitation |
|---|---|
| Printed hubs, split support housing | PLA, X1C; surfaces are structural, not the primary dielectric. No custom metal machining. |
| Dielectric | Purchased 6 / 12 / 25 µm PET for screening. [Mylar capacitor-film manufacturer data](https://www.dupontteijinfilms.com/wp-content/uploads/2024/02/Mylar-Specialty-Films-Product-Capacitors-Brochure.pdf) gives typical εr 3.25 and thin capacitor grades. This is a bulk-material reference, not a working-voltage rating for a cut, worn clutch. |
| Split input electrodes | Two hand-cut copper-foil sectors; edge burrs, wrinkles and exposed conductor around cuts must be controlled. Aluminium foil can serve electrically, but attachment/contact reliability is harder. |
| Floating electrode | Metallized PET, aluminium face toward the dielectric. The PET backing provides flexibility and a bondable hub surface. Metallization is conductive, **not an insulating coating**. |
| Rotary contacts | Two copper-foil ring tracks and two fabric brushes, each supported by the stationary housing. [Adafruit 1168](https://www.adafruit.com/product/1168) is purchasable Ni/Cu-coated polyester fabric, not qualified miniature slip-ring stock. |
| Adhesion to hubs | Bond only the central output attachment and input dielectric perimeter outside the active overlap. Full-area adhesive between electrodes adds `t_adhesive/εr_adhesive` to electrical thickness. Air pockets under foil still impair flatness. |
| Specialized dielectric | Arkema identifies [Piezotech RT terpolymers](https://piezotech.arkema.com/en/Applications/) as the high-κ family; FC copolymer is not interchangeable. Casting/coating, curing and inspection are unusual processing. No low-volume coating quote or DIY process qualification is established. |

The cheap stock-metal/PET approach is worth a passive coupon. It has no evidence of matching the research coating. Actual supplier prices and the total repeated component budget are in the sourcing report; raw film area cost alone is not clutch cost.

## Dimensioned concept B2-10: deliberately a principle fixture

[Drawing](concepts/B-floating-electrode.svg) and [parametric OpenSCAD](concepts/B-floating-electrode.scad) show the following proposed dimensions. The CAD is a packaging and force-path model, **not a released print plate or high-voltage assembly**.

| Feature | Nominal dimension / function |
|---|---|
| Carrier / flexible output film | Ø10 / Ø9 mm |
| Active overlap | Annulus ri = 1.8, ro = 4.5 mm; 0.4 mm split-electrode insulating channel reduces area further |
| Input sector / dielectric / output substrate | 35 µm copper / 12 µm PET / 25 µm metallized PET (stock assumptions) |
| Output central bond land | Ø3.2 mm; output film remains compliant outside this land |
| Output journal and collar | Ø2.0 journal in Ø2.3 printed bores; Ø4.4 × 0.8 mm collar in 0.90 mm axial pocket |
| Input journal and collar | Ø3.0 journal in Ø3.3 bores; Ø5.0 × 0.8 mm collar in 0.90 mm axial pocket |
| Rotary tracks | Two Ø3 mm ring bands, each 1 mm axial width, separated by 2 mm; extended below fixture |
| Electrode nominal position | Film plane initially 0.05 mm above dielectric in CAD; adjustable stationary support elevation, not a claimed as-printed gap |
| Existing screw interface | Ø3.2 nominal, 3 mm lead; 4.4 mm guided pin, 6 mm internal thread. Concept shows envelope only; retain E-295 functional thread geometry. |

Terrain load runs **pin → screw → output collar → stationary support → frame**. Reverse/upward reaction uses the opposite collar face. Two spaced journal bores guide the output radially. The input has its own collar and two bores. During open-gap pull-in, electrostatic attraction and film bending load the output hub and input support through their separate collars. Once contact closes, opposing electrostatic and contact forces largely balance locally: approximately `N_contact = F_ea − F_elastic` for a film held above the input before engagement. The supports then carry the net elastic reaction, terrain load and any assembly preload; do **not** automatically assign the entire electrostatic clamping force to stationary thrust friction. Transmitted torque runs between the film surfaces, through the output central bond into the screw. Output support friction reduces torque available to the screw; input support friction instead increases shared-drive demand. Neither is assumed zero.

The film can bend toward the input while the screw remains axially supported. This is **one deforming moving element**, even without a separate sliding armature or spring. Its elasticity is the only proposed release bias. No dependable return force is claimed. The 0.10 mm collar endplay is already larger than the model's 0.05 mm initial gap; thrust reversal, FDM warpage and collar wear can alter preload or prevent engagement. A physical fixture must measure this movement and set its stationary support elevation with measured shims. At 5 mm the small unsupported film span is stiffer and leaves less bond land. These are manufacturing blockers exposed by the concept, not solved tolerances.

Minimum B2 repeated parts are **12** before adhesive/shims/support allocation: input printed hub (1), output screw/hub (1), floating film (1), input copper sectors (2), PET dielectric (1), rotary copper tracks (2), fabric brushes (2), insulated links (2). Two rotor assemblies rotate independently; the output film and the two brush contacts flex. Add the baseline guided pin, two split housing halves shared across a module, closure hardware and any measured thickness shims. The single-cell concept uses two external M2 screws plus two nuts for housing closure; no hidden rolling bearings. Eight bond locations and four rotor-link electrical terminations are assembly operations, not free interfaces. With one baseline pin, two dedicated housing halves and four closure fasteners, this single-cell concept contains at least 19 physical pieces, plus its shared PCB allocation and any shims. Direct PCB brush termination is assumed; otherwise count two further fixed leads. B1 trades the split electrode for an output connection but does not guarantee fewer rotary contacts when both discs rotate relative to ground.

A Ø10 mm carrier cannot fit a single 5.08 mm plane; four-height checkerboard spacing gives only 10.16 mm between equal-height centers, leaving 0.16 mm diametric clearance before supports and wires. A nominally Ø5 mm carrier leaves only 0.08 mm at the original pitch. Neither is an assembly clearance claim. Ø4.7 mm is a more credible bare-disc envelope, with much less active area after central support and edge insulation. The 10 mm concept and its contacts are consequently **not pitch-compatible**.

## Numerical decision screen

The generated calculations use 300 V terminal voltage, 12 µm PET, εr = 3.25 and assumed μ = 0.3. For B2 at Ø4.7 mm, a 2.2 mm center exclusion and 80% coverage, the gap-closure model gives **0.0428 / 0.00772 / 0.00104 N·mm** at gaps of 0 / 5 / 20 µm. These are not measured capacities. For the Ø10 concept active annulus (before subtracting its split channel), corresponding ideal torques are **0.3916 / 0.07065 / 0.00951 N·mm**. Terminal capacitances are 32.04 / 13.61 / 4.993 pF and stored energies 1.442 / 0.612 / 0.225 µJ. B1 gives four times these values at the same terminal voltage. Neither case includes support drag, peel, coverage defects or validated slip behavior.

The compact geometry therefore relies strongly on essentially complete contact at high electric field. The larger fixture offers a more measurable signal but does not establish a viable array.

## Why scaling the published 20 mm result is not a prediction

At constant pressure, coefficient of friction, contact fraction, number of interfaces and geometrically similar annulus, torque scales as diameter cubed. Counterfactual cubic scaling of the cited measurement gives 1.30 / 3.58 / 10.43 mN·m at 5 / 7 / 10 mm. These are calculations, not demonstrated performance. Electrode/coating thickness, surface roughness, wire size, edge insulation and a support hub do not scale proportionally. For the same film thickness, reducing free span strongly reduces bending compliance; a large fraction may never pull in. Applying the same cubic law to OFF torque is equally unjustified because brush preload, bearing drag and residual adhesion need not scale that way.

A high-κ research film may exceed the plain-PET model substantially. Conversely, a plain PET film wrinkled over FDM can underperform that model. A useful measured torque target must come from the existing screw and the actual purchased surfaces, not this scaling exercise.

## OFF state, release, slipping and finite next step

OFF torque transmitted to the output includes mechanical contact/preload, residual electroadhesion, contamination and film wrinkles. Output support friction affects whether that leakage moves the screw. Input bearing and brush drag instead load the shared drive; they are not directly transmitted OFF torque. Wear can polish asperities and decrease drag, or produce charge/debris/surface damage that increases it. The direction cannot be assumed. [Three-phase electrostatic clutch research](https://pmc.ncbi.nlm.nih.gov/articles/PMC12677595/) experimentally addresses residual charge and stick-slip with more elaborate voltage waveforms; that is evidence of the problem, not justification for adding a complex waveform system here.

**Smallest useful B action:** add a purchased PET/metal-film surface pair to the shared passive torque fixture, without voltage, and measure light-contact drag, friction versus externally applied normal load, repeated-slip wear and release. It tests manufacturability and friction only. It does not establish electrostatic pull-in or insulation.

No owner-built energized setup is released. A later energized test would require a closed, interlocked, current-limited high-voltage supply; rated leads, switches, series resistors and discharge networks; guarding of both rotating powered tracks and the nominally floating output; verified insulation under motion; measured discharge before access; and a design review of the supply's total stored energy. Small calculated clutch capacitance does not bound energy in supply reservoirs or wiring. Terminal voltage zero does not itself prove residual adhesion gone. Stop this investigation at the passive coupon and analytical comparison unless the owner explicitly selects further work.
