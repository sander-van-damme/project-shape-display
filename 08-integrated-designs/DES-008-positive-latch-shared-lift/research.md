# Mechanism research and source limits

Sources consulted 14 October 2026. Prices are dated public observations, USD before regional freight/tax; the BOM marks unquoted fabrication allowances. No purchase or physical test was performed.

## Useful industrial mechanisms

| Primary source | Useful principle | Why it is not a Shape Display validation |
|---|---|---|
| [Stäubli LX PRO](https://www.staubli.com/us/en/textile/products/jacquard-machine/reliability-power-saving-lx-pro.html) | Shared lifting motion, mechanically retained hook selection | Electronic hook selection remains repeated; load, stroke, routing and selector count differ |
| [Kniterate specifications and FAQ](https://www.kniterate.com/product/kniterate-the-digital-knitting-machine/) | A carriage/cam supplies mechanical work while local selection routes needles | Published industrial pitch and carriage rates do not qualify 10-ms printed gates or a catalog solenoid's loaded response |
| [US4038837A, electromagnetic needle selection](https://patents.google.com/patent/US4038837A/en) | Cam-assisted cocking followed by electromagnetic selection can separate motion energy from control | Not an off-the-shelf implementation of the proposed printed selector; no freedom-to-operate conclusion is made |
| [Jadhav et al., Scalable Fluidic Matrix Circuits](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300011) | Real row/column multiplexing with 25 outputs and ten electromechanical valves | Still uses local fluidic logic. Sealing, leakage, rigid retained terrain, scale and packaging are unqualified here |
| [NTT, MagneShape](https://www.ntt-review.jp/archive/ntttechnical.php?contents=ntr202307ra1_s.html) | A spatial magnetic medium can supply both pattern and drive without a motor on every pin | Reported magnetic interference and dynamic height behavior do not provide independently retained, bidirectional 40-mm loaded terrain |

These analogies motivated explicit mechanical isolation and writing the output state rather than assuming a shared motor solves addressing. Mechanical matrices without geometric disengagement can transmit force into unselected intersections. Frictional holding replaces machining with preload/friction qualification; it does not remove the load path. Ramps and linkages add travel, depth or resident moving bodies. The existing repository's scoped negative evidence was consulted instead of presenting those mechanisms as new discoveries.

## Purchased references and manufacturing processes

- [Adafruit 2776 mini solenoid](https://www.adafruit.com/product/2776): $4.95 single, $4.46 at 10–99, $3.96 at 100+; 5 V, 1.1 A, 3-mm throw/80-g stated force. The page does not establish a loaded 20-ms switching cycle or continuous array duty. The 20-mm body also needs staggered/remote packaging at 6.35-mm pitch.
- [Adafruit 6318 eight-channel solenoid driver](https://www.adafruit.com/product/6318): $14.95 single / $13.46 at 10–99, used in the manufacturing ledger. Shared terminal current and the eight-address I²C limit need system design. A PCB cost reduction is an engineering option, not a quoted price in this package.
- [Tower Pro SG90 manufacturer](https://towerpro.com.tw/product/sg90-7/): 23 × 12.2 × 29 mm and 0.1 s/60° nominal speed. Neither a no-load timing nor an unspecified marketplace clone supports a precision-selector rating. No cheap clone pricing is credited.
- [Precision Micro chemical-etching guidelines](https://www.precisionmicro.com/chemical-etching/technical-guidelines/): fine thin sheet features are a credible process route. Its process tolerances do not establish spring fatigue, assembled alignment, module yield or price.
- [SendCutSend 1075 spring steel](https://sendcutsend.com/materials/1075-blue-temper-spring-steel/): ordinary service stock and cutting tolerances differ from a custom 0.15-mm etched comb. Do not price one as the other.
- [Protolabs injection molding](https://www.protolabs.com/services/injection-molding/) and [design guidelines](https://www.protolabs.com/services/injection-molding/plastic-injection-molding/design-guidelines/): tooling starts above the original whole-machine benchmark. Open racks are easier to mold than long internal threads, but tooling and first-article qualification remain real costs.

## Playability evidence

[WizKids sells actual 25-mm bases](https://shop.wizkids.com/products/wizkids-deep-cuts-clear-25mm-round-base-15-ct); [its D&D miniature page](https://wizkids.com/dnd-unpainted/) identifies examples on those bases. Game-square size does not specify a miniature's exact manufactured diameter. The owner's intended base set has not been measured here. The wall-clearance equation uses physical diameter and panel thickness, not miniature scale.

The repository's mission and current priorities are authoritative for the one-inch grid, meaningful cliffs/ravines, thin grid-line walls, independent signed motion and owner evidence. Synthetic/annotated heightmaps provide engineering workloads; they do not prove corridors are playable or that their sampled distributions describe real game sessions.

## Independent engineering review

Six independent workstreams addressed multiplexing, alternatives, throughput, manufacturing, adversarial review and a fresh falsification review. Follow-up work independently rescheduled the critical timing cases, rejected the crossed-support datum transfer, exposed writer travel and memory-state mismatches, corrected fabrication counts and mass assumptions, and reviewed the small CAD articles. Agreement was not treated as physical evidence.

The retained review notes identify objections and dispositions. Computational checks verify stated models and mesh geometry only. Physical results remain explicitly unknown.
