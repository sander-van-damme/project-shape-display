# Components, manufacturing operations and cost boundaries

[Experiment](engineering-report.md) · [E–H evidence](sources-rejected-families.md)

Supplier pages checked **23 October 2026**. These are public catalogue observations, not supplier quotations, stock reservations or orders. Prices exclude delivery unless stated; VAT and currency are preserved below. A cached/indexed price is identified explicitly. No currency conversion or unquoted volume discount is used. The estimates describe experimental components, not a validated 5.08-mm production cell.

## Standard metal and magnetic parts

| Component and supplier | Observed size/material and price | Consequence for this experiment |
|---|---|---|
| [DHZ-proshop, Belgium, DIN 9021 M3 steel/Zn](https://www.dhz-proshop.be/en/200st-sluitringen-din-9021-m3-zn) | ID3.2 × OD9 × 0.8 mm; page offers 100 pieces at **€4.65 including VAT**; pickup only displayed | Correct standard large washer for the approximately 10-mm A experiment: one armature and one return washer per cell. The URL's “200st” is not the displayed pack count. |
| [Prokope, Germany, same DIN 9021 M3 washer](https://www.prokope.de/DIN-9021-Stahl-verzinkt-M3-32-x-9-x-08-mm-VE-100-Stueck) | Steel 140HV, 3.2 × 9 × 0.8 mm; **€0.83/100 including 19% VAT**, limited stock | Approximately €0.0070 each before VAT at this listed pack price; a cheap washer is credible, but its magnetic curve, flatness and finish remain unqualified. |
| [Raptor EU, M38130.016.0001, DIN125-1A M1.6](https://eu.raptorsupplies.com/pd/approved-vendor/m38130-016-0001) | Zinc-plated steel; ID1.7, OD4, nominal thickness0.3 mm; **€12.59/100 excluding VAT** | Miniature standard washers exist. Their small holes need a separate small journal/hub; they do not pass over a 3.2-mm screw body. |
| [Automotion, P0330 zinc-plated-steel washer family](https://www.automotioncomponents.co.uk/am/products/mechanical-components/standard-fasteners/flat-washers/form-a/p0330.zp/groups/g%2Bm%2Bc%2Bs%2Ba%2Bview) | M1.6: 1.7 × 4 × 0.3 mm; M2: 2.2 × 5 × 0.3 mm. Indexed catalogue **£2.14/100**, tax status not established | Dimensional and UK cost cross-check, not the EU budget basis. OD5 leaves only 0.08 mm between adjacent nominal 5.08-mm centers before tolerances or housing. |
| [Metrofixings, M2 × 10 DIN7985Z pan screw](https://www.metrofixings.co.uk/product/m2-x-10-pan-pozi-machine-screw-steel/2535) | Mild steel grade4.6; head diameter up to4 mm; indexed **£1.75/100 including VAT**, falling to **£0.88/100 at 2,000+** | Unmodified stock magnetic core candidate. Its threaded root section is smaller than nominal2 mm; thread, plating, head and washer joints add reluctance. The budget below uses an explicit euro allowance rather than converting this unconfirmed UK price. |
| [Dibolt M2×8 DIN912, SKU10161.020.008](https://dibolt.co.uk/products/m2-x-8mm-socket-cap-screw-high-tensile-grade-12-9-self-colour-din-912/) | Actual A-concept geometry: head Ø3.8 ×2 mm, 8-mm shank, 0.4-mm thread pitch; steel grade12.9; displayed **£0.04–0.05 excluding VAT**, exact quantity split not shown | A stock shape match, **not mild-steel magnetic qualification**. Heat-treated steel can have different permeability/remanence; μr300 in the model remains an assumption. The separate M2×10 grade4.6 pan screw is a material alternative needing geometry changes. |
| [Reichelt / Donau LD10-6 enameled copper wire](https://www.reichelt.com/de/en/shop/product/enameled_copper_wire_0_10mm_100m_violet-398436) | Nominal copper diameter0.10 mm,100 m; **€11.95 including 19% VAT** | €0.10042/m before VAT. Actual insulated diameter and termination process must be checked before claiming the winding fits. |
| [Magnethandel / EarthMag SKU2435](https://www.magnethandel.de/neodymium-ringmagnets-4-2-2-mm) | NdFeB N45 ring, OD4 × ID2 × height2 mm; axial magnetization; ±0.1-mm tolerance; NiCuNi; **€0.24 single, €0.19 at500**, including19% VAT | Useful stock part for C's rotationally symmetric sleeve. Backordered: cached category/product pages disagree about expected date and4–6-week delay. Availability and Belgium delivery need confirmation. Its 2-mm hole requires a smaller journal, not the existing screw diameter. |
| [Supermagnete Belgium S-02-01-N](https://www.supermagnete.be/eng/disc-magnets-neodymium/disc-magnet-2mm-1mm_S-02-01-N) | Axial NdFeB N48 disc,2 × 1 mm; **€0.20 at20, €0.14 at360**, including VAT; quotation requested above1,300 | A genuinely small inexpensive magnet, but an off-axis rotating disc is not an equivalent replacement for C's coaxial ring. |

Vendor magnet pull-force ratings refer to contact with a favorable steel target. They do not establish force across a printed spacer or bistability. Steel washers must be specified as ferromagnetic steel: the same dimensional standard in austenitic stainless steel is not an equivalent magnetic component. No drilling, grinding, lapping or custom-cut metal is assumed in A's build. A core cut from metal rod would introduce a metal-cutting operation, so unmodified fasteners are the preferred test stock.

The two proposed80-turn windings at mean turn diameter3.1 mm consume `2×80×π×0.0031 + 0.20 = 1.758 m` including a0.20-m lead allowance. At the retail spool price that is **€0.177 of copper wire per cell before VAT**, or approximately **11.25 km / €1,130 consumed wire for6,400**. Whole100-m spools and winding waste increase the cash purchase. Winding, stripping and four coil terminations are repeated assembly work even when the coils are series-connected and share one driver.

A commercial comparison is [Intertec ITS-MSM-1010-12VDC at Rapid](https://www.rapidonline.com/intertec-its-msm-1010-12vdc-electromagnet-3n-12v-dc-1w-1piece-non-magnetic-09-5103): a10 × 10-mm,12-V,1-W part listed at **£21.87 single / £19.81 at100 excluding VAT**. Its stated3-N attraction does not transfer to A's magnetic circuit. It demonstrates why buying thousands of finished electromagnets is unattractive. A PCB coil is manufacturable by a normal PCB supplier, but its turns, resistance, board layers and central magnetic path still need design; **no small-cell PCB-coil price or force has been verified**.

## Films and electrostatic interfaces

| Material/source | Observed catalogue offer | What it establishes |
|---|---|---|
| [KOA France, synthetic-film catalogue](https://www.kingdom-of-arts.com/films-synthetiques) / [12-µm Melinex product](https://www.kingdom-of-arts.com/films-synthetiques/film-polyester-melinex-12-microns) | Clear PET12 µm,1.52 × 100 m; regular **€145 excluding VAT**; category showed €130.50 promotion, while another indexed product page showed a different promotion | Affordable thin stock film. Use the regular price for budgeting, not a promised sale. Archival PET is not automatically qualified clutch dielectric. |
| [DuPont Teijin Films capacitor-film brochure](https://www.dupontteijinfilms.com/wp-content/uploads/2024/02/Mylar-Specialty-Films-Product-Capacitors-Brochure.pdf) | Manufacturer describes capacitor PET in2.5–12-µm range and relative permittivity about3.25 | A useful material-property/source-family reference, with no verified small-quantity quotation here. |
| [Sigma GF95968535](https://www.sigmaaldrich.com/US/en/product/aldrich/gf95968535) | PET6 µm,1 m × 315 mm; US listing **US$380** | Small research-film purchases can be expensive even when industrial roll area is cheap. Do not assume12-µm roll price applies to6-µm laboratory stock. |
| [CS Hyde PET film catalogue](https://catalog.cshyde.com/viewitems/films/mylar-polyester-pet-film) | Indexed manufacturer listings: metallized PET48-1F-1M-1-100,25.4 µm,1 in × 100 ft, **US$5.55**; plain25.4-µm version **US$7.00**. Live page blocked access | A stock metallized-film lead, **indexed prices only**. Exposed conductive face, sheet resistance, coating adhesion and availability are unverified. No claim that this is a finished clutch electrode. |
| [DigiKey Germany, Adafruit1168](https://www.digikey.de/en/products/detail/adafruit-industries-llc/1168/5356770) | Conductive woven fabric20 × 20 cm, **€4.24 excluding VAT** single | Alternative flexible electrode stock, but weave texture/thickness and sliding durability differ from smooth metallized PET. |

At the conservative KOA regular price,12-µm film costs **€0.954/m²**. A10 × 10-mm cut square consumes only **€0.000095** of film;6,400 such squares consume0.64 m²/€0.61 before cutting waste, but buying the roll still costs€145. This is **raw area cost**, not a finished electrode cost. Cutting, alignment, tab formation, rejected pinholes, cleaning, edge insulation and bonding are the actual repeated operations. A second film layer doubles the consumed area, and a different thickness/material needs its own price. The specialized high-permittivity blade-cast film in the published electrostatic clutch is not included in this plain-PET estimate.

B needs two input electrodes, a floating compliant output electrode, dielectric film, film retention, supported input/output rotation and OFF separation. In the proposed rotating-input configuration it also needs **two physical sliding electrical contacts and two tracks per cell**:12,800 brushes and12,800 tracks for6,400 cells. Electrical sharing of a common node does not remove its physical contact with each independently rotating input. Patterned copper foil, thin metal foil and cut PET are ordinary supplies/operations; conductive tape adhesive must not be treated as zero dielectric thickness. Put adhesive outside the active electrostatic gap. Brushes, metallization and dielectric are wear items; their lifetime and replacement labor are unpriced.

## Repeated electronics, with procurement quantities exposed

All following DigiKey Belgium prices are **EUR excluding VAT**, from the linked product pages. They are individual components, not assembled controllers.

| Part/function | Catalogue tiers used | Count for6,400 cells and cost implication |
|---|---|---|
| [AO3400A, AOS,30-V N-MOSFET](https://www.digikey.be/en/products/detail/alpha-omega-semiconductor-inc/AO3400A/1855772) | €0.46 single; €0.17940 at100; €0.10153 at3,000; €0.08748 at9,000 | One per unipolar coil channel. Two3,000 reels plus400 at the100-tier cost **€680.94**. The9,000-tier price cannot be applied to a6,400-piece order. |
| [SS14, onsemi,40-V1-A Schottky](https://www.digikey.be/en/products/detail/onsemi/SS14/965729) | €0.39 single; €0.11020 at500; €0.07236 at7,500 | One flyback diode per channel: purchase7,500 for **€542.70**, leaving1,100 spares. A low-voltage diode clamp prolongs current decay; its release time must be tested. |
| [Nexperia74HCT595D,118](https://www.digikey.be/en/products/detail/nexperia-usa-inc/74HCT595D-118/763163) | €0.52 single; €0.25424 at500 | Eight output bits/IC:800 ICs cost **€203.39**, or€0.03178/channel. HCT at5 V accepts3.3-V controller logic. |
| Gate resistor1 kΩ and pulldown100 kΩ | **Assumed** €0.003 each at volume; no exact sourcing claim |12,800 resistors add **€38.40**. Decoupling, PCB, OE enable, connectors, power distribution and controller are additional. |
| [HV507PG-G, Microchip,64-channel300-V push-pull driver](https://www.digikey.be/en/products/detail/microchip-technology/HV507PG-G/4902491) | €17.55 single; €14.12480 at100 |100 ICs cost **€1,412.48**, or **€0.22070/channel**, assuming one controllable high-voltage output per cell and a shared reference. This cannot reproduce a420-V experiment;300 V is the upper rating. |
| [STN1NK60Z, ST,600-V N-MOSFET](https://www.digikey.be/en/products/detail/stmicroelectronics/STN1NK60Z/669373) | €1.16 single; €0.37344 at500; €0.28575 at4,000 | A comparison for a discrete HV circuit, **not a complete selector**. Charge/discharge paths, level shifting, gate drive, discharge resistors, isolation boundaries and layout remain necessary. Its600-V rating does not make its gate3.3-V compatible. |

The low-voltage purchase example totals **€1,465.43** including spare diodes, before boards, soldering, power supplies, connectors and control. Consumed parts at those rates are approximately€0.217/channel; cash purchased is approximately€0.229/channel. The experiment's scheme may use TI [SN74HCT595PWR](https://www.ti.com/product/SN74HCT595/part-details/SN74HCT595PWR); the priced Nexperia SO16 part is a family alternative, **not a footprint substitution**. C's bipolar pulse actuation needs an H-bridge or equivalent extra switches; the one-MOSFET example does not price that function.

The HV507 number is economically useful but not a complete HV-system bill. Its high-voltage supply current, logic current, discharge losses and HV converter loss belong in the power budget. The main report evaluates its datasheet0.5-mA/chip example:100 chips at300 V give15 W before those other loads. A single inexpensive600-V transistor also does not establish the cost of6,400 independently addressable, fail-OFF channels above300 V. That complete design remains unquoted.

For a separate global comparison, [LCSC AO3400A C20917](https://www.lcsc.com/product-detail/MOSFET_Alpha-Omega-Semicon-AO3400A_C20917.html) was indexed at **US$0.0482 at6,000**, roughlyUS$308.48 consumed for6,400 transistors. This is not an EU landed cost: VAT, freight, duties and the rest of the circuit are absent. It is kept separate from the euro budget.

## Full repeated-function budget

These are **planning ranges**, not sourced assembled-product offers. They deliberately count supports and retention. They exclude the baseline display pin/lead screw, shared motor/transmission, shared power supplies, enclosure, commissioning, labor, taxes and delivery. The approximately10-mm A/B test geometries do not establish final display packing.

| Family | Repeated mechanical/material functions that must be supplied | Mechanical allowance / pin | Electronics allowance / pin | Sum / pin;6,400 cells |
|---|---|---:|---:|---:|
| A: stationary-coil friction |2 steel washers,2 stock cores,2 wound coils, printed bobbins/keeper, driven input annulus, output carrier/flexure, friction interface, independent input/output journal and thrust support, retention |€0.30–0.80 |€0.25–0.55 |**€0.55–1.35; €3,520–8,640** |
| B: plain-PET electrostatic,≤300-V example | Split input electrode, dielectric, compliant output electrode, printed holders,2 tracks,2 brushes, supports, OFF spacing and edge bonds |€0.08–0.35 |€0.30–0.65 |**€0.38–1.00; €2,432–6,400** |
| C: bistable permanent-magnet friction | Ring magnet, coil/core,2 magnetic stops, guided output slider, friction pair, flexure/latch details, independent supports and retention |€0.30–1.00 |€0.35–0.90 |**€0.65–1.90; €4,160–12,160**; incomplete magnetic design |
| D: conventional electromagnetic clutch | Coil/core and shaped rotating rotor, axially compliant armature, friction pair, flexible torque link/return, independent supports and retention |Unknown |LV excitation may resemble A |No pitch-compatible off-the-shelf assembly or compliant stock-parts construction priced |
| E: hysteresis | Specialty rotor, rotating shaped poles, coil/return,2 supported rotating assemblies |Unknown |LV excitation may resemble A |No compliant component set priced |
| F: electropermanent |AlNiCo+NdFeB,2 poles, coil, friction/compliance parts, supports, bipolar pulse driver/storage |Unknown |Unknown |Indexed AlNiCo alone **US$1,664/6,400**; wrong geometry, not a complete price |
| G/H: MR fluid / magnetic powder |2 rotors, coil/return, sealed chamber, fluid/powder, sealing interfaces, supports, fill/retention |Unknown |LV excitation may resemble A |Containment and assembly dominate; no defensible total |

For A, the bottom of the material allowance is constructed from approximately€0.177 wire,€0.014 washers, **assumed**€0.02–0.14 for two stock cores,€0.0125–0.05 printed plastic,€0.05–0.20 additional printed supports/retention and€0.02–0.08 friction/bonding consumables. The range includes a modest material contingency, not assembly wages. Printed masses are placeholders until the production geometry is fixed. The plastic assumption is0.5–2 g at€25/kg;6,400 cells would consume3.2–12.8 kg/€80–320 for that mass category. It is not a sliced estimate for the larger test rig.

B's allowance is dominated by **unquoted** brushes/tracks, patterning and support materials, not its fractions-of-a-cent raw PET. The HV driver alone costs approximately€0.221/channel. B's lower mechanical cost is therefore a hypothesis; reliable film fabrication and contact life could reverse the ranking. A continuous metal spring brush, bought as strip and cut, is an ordinary-material operation, but its wear force, contact stability and production cost are not yet verified. No high-permittivity custom dielectric or420-V driver is hidden in that allowance.

### One normalized example including baseline printed parts

For a reviewable single estimate, the following includes the baseline pin and screw/output body in **both** concepts. A has13 physical pieces before its selected shim and adhesive retention; B has19 when its pin, two housing halves and four closure fasteners are included. Consequently the often quoted “A13 versus B12” is not a like-for-like comparison. A's concept bonds its support halves and adds a selected PET shim (14 discrete pieces); the example below retains a shared-frame closure allowance for a later serviceable implementation. It is a cost allocation, not hidden fasteners in the CAD.

| Repeated cost item | A example, €/cell | B example, €/cell | Basis |
|---|---:|---:|---|
| Baseline printed pin and screw/output body,2 pieces |0.060 |0.060 |Assumption; A includes the carrier flexure in its output body |
| Printed input rotor,1 piece |0.020 |0.020 |Assumption |
| Two split support/keeper or housing pieces |0.050 |0.050 |Assumption; journals and thrust surfaces are integral printed features, not omitted bearings |
| Two insulating bobbins |0.020 |— |Assumption |
| Two M3 DIN9021 washers |0.014 |— |Prokope pack price before VAT |
| Two M2 pole/core screws |0.060 |— |Assumed euro purchase cost, not a currency conversion |
| Two80-turn coils, consumed wire |0.177 |— |Reichelt retail wire; winding labor excluded |
| Floating metallized output film and PET dielectric,2 pieces |— |0.0021 |Raw consumed-film allowance; €0.0001 PET plus assumed €0.002 metallized film, with no fabrication labor |
| Two copper electrode sectors plus two tracks |— |0.020 |Assumed foil allocation;4 separate pieces |
| Two fabric/metal brush pieces plus two insulated links |— |0.030 |Assumed material allocation;4 pieces, no asserted lifetime |
| Closure hardware |0.030 |0.040 |A: shared-frame allocation. B:2 screws+2 nuts at assumed €0.01 each |
| Adhesive/friction treatment/shim material allowance |0.030 |0.030 |Assumption; no labor or measured shim selection |
| Consumed switching/logic components |0.217 |0.221 |A: MOSFET, diode,1/8 HCT595,2 resistors. B:1/64 HV507; rounded |
| PCB, decoupling, additional resistors and local connector/routing allocation |0.120 |0.120 |Assumption, not a fabricated PCB quotation |
| **Estimated repeated material/electronics total** |**€0.80** |**€0.59** |Unrounded arithmetic:€0.797/€0.593 |
| **6,400 repeated cells** |**approximately €5,100** |**approximately €3,800** |Consumed components; whole-pack purchasing costs more |

This is a **fully enumerated repeated-function estimate**, not a complete display quotation: shared supplies, controller infrastructure, motor/transmission, enclosure, engineering, assembly labor, yield loss, service spares, shipping and VAT remain excluded. The low B value depends especially on unmeasured brush life and inexpensive repeatable film fabrication. Neither estimate proves assembly throughput or fit at5.08-mm pitch. For the same baseline and closure scope, a prudent estimate remains broad: roughly€0.6–1.5 for A and€0.4–1.2 for the plain-PET≤300-V B candidate, before the listed system exclusions.

At6,400 repetitions, every extra€0.10 is€640. Even **10/30/60 seconds of assembly per cell** gives17.8/53.3/106.7 hours; at an explicitly assumed€25/hour that is€444/€1,333/€2,667. These are scenarios, not measured cycle times. Two hand-wound coils or aligned tiny film stacks can easily exceed them. All approaches need accessible modular replacement: a damaged dielectric, worn brush or failed winding should not require dismantling a full display. Adhesive-only, inaccessible assemblies reduce nominal part count while increasing repair cost.

The procurement result is narrow: stock steel, copper wire, PET and small permanent magnets are obtainable at low raw-material cost. It does **not** establish a low-cost, low-drag, pitch-compatible clutch. The decisive price unknowns are repeated supports, contacts/coil assembly, usable yield, thermal management, qualified HV switching above300 V and service life. Those remain explicit limitations rather than zero-cost BOM lines.
