# DES-004 purchased-component cost reconciliation

Date basis: 2026-10-06. Currency: USD. 3D-printed parts are excluded from the purchased-component totals.

## Reconciled result

| Case | Purchased total | Delta vs DES-003 | Status against project cost bands |
|---|---:|---:|---|
| DES-003 baseline | $370 | — | Acceptable allowance ($200–400) |
| DES-004 nominal | $498 | +$128 | Last-resort band ($400–500) |
| DES-004 conservative spare/consumable | $729 | +$359 | Unacceptable (> $500) |

The machine-readable calculation is in `bom_des004.csv`. The baseline is the $370 subtotal from `DES-003/bom_a1.csv`; its rows are sourced-class or allowance values, not live purchase orders. DES-004 retains those bought items, including the eight writer actuator positions and eight reader heads, so they are counted once and marked as inferred reuse. No new reader electronics, writer motors, gantry motors, guides, drivers, power supply, loom, switches, or fasteners are silently omitted.

The rotary successor adds one axle per 5.08 mm cell: 6,400 installed metal pins. The nominal case orders 6,400 pins at a $0.020/pin engineering bulk-price target. The conservative case orders 6,720 pins: 6,400 installed plus 320 (5%) combined scrap/service stock, at a $0.050/pin low-volume cut/debur allowance. Neither price is a supplier quote. Availability, exact diameter/length, tolerances, corrosion finish, packaging, freight, and delivered pricing remain unresolved. The axle is the only new purchased item driving the delta and the largest cost uncertainty.

## Axle sourcing evidence and fit gate

Current catalog evidence bounds the risk but does not validate the design fit. A Zoro Select listing reports 1 mm x 10 mm, 18-8 stainless, ISO 2338B h8 pins at $7.99 per 100 ($0.0799 each), with diameter tolerance -0.014/-0.000 mm and length tolerance ±0.25 mm; 68 packs would provide 6,800 pins for the conservative 6,720-piece order at about $543.32 before freight/tax. A Grainger listing for a 1 mm x 10 mm stainless press-fit pin reports $3.02 per 10-pack ($0.302 each). These are sourced catalog observations, not selected parts, and neither listing establishes that 10 mm is the required axle length or that its fit is appropriate. [Zoro listing](https://www.zoro.com/zoro-select-standard-dowel-pin-1-mm-nom-dia-10-mm-l-18-8-stainless-steel-100-pk-dp7x01010h8-100p1/i/G3373772/) and [Grainger listing](https://www.grainger.com/product/Dowel-Pin-41KP32).

The catalog check therefore rejects the implicit idea that a retail 1 mm x 10 mm pin can support the $0.020 target: the observed Zoro price alone would make the conservative DES-004 total about $936.32 ($370 + $543.32 + $9 + $12 + $2), before freight. This is a calculated upper-bound illustration, not a revised BOM. Bulk cut-to-length or manufacturer quotation is required to approach the target.

The design record does not specify axle diameter, free length, engagement length, end treatment, or hole/rotor clearance. Fit is consequently unresolved. The minimum quote request and fit gate are: quote 6,720 pieces (plus a separate 100-piece sample if available), material and finish, nominal diameter and tolerance, cut length and tolerance, chamfer/debur condition, packaging, lead time, stock/MOQ, and delivered freight to the project location; then compare the certificate/drawing against the rotor hole and bearing/retainer geometry. Analytical compatibility with the rotor-fit gate cannot be claimed until those dimensions are defined and checked; no physical validation is implied.

The price ceilings are explicit: to keep the nominal case at or below $500, 6,400 delivered pins must average no more than $0.02031 each (with no spare allowance). To keep the conservative case at or below $500 while retaining 6,720 ordered pins and the three service spares ($23), delivered axle cost must average no more than $0.01592 each. Freight and packaging consume that same ceiling unless quoted separately and added.

## Sourcing evidence and alternatives

The retained component classes are inherited from the DES-003 allowance and are not re-quoted here. Product-class references checked for the inherited items are [NEMA-17 example](https://www.frankhumotor.com/nema-17-stepper-motor), [DRV8833 module example](https://electropeak.com/drv8833-dual-motor-driver), and the [TI DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf). These references support component identity only; they do not establish the CSV prices or current availability.

| Alternative | Purchased effect | Engineering effect | Decision |
|---|---:|---|---|
| Quote bulk stainless/music-wire pins and cut in-house | Only credible route toward the $0.019–$0.020 delivered ceiling; exact delta unknown | Adds cutting, deburring, inspection, corrosion and tolerance work; risks friction and cycle life | Preferred cost-down investigation; quote before gate closure |
| Buy pre-cut precision pins | Higher unit price than bulk target, lower assembly risk | Best dimensional repeatability and maintainability; supplier MOQ/availability unknown | Viable reliability fallback |
| Print integral axles | Removes the estimated $128 nominal / $320 conservative purchase | Adds creep, wear, clearance and replacement risk at 6,400 interfaces; assembly may simplify but durability is unqualified | Not counted as a cost-gate pass without coupon evidence |
| Reuse existing reader/writer interfaces | Avoids 8 new heads and associated wiring | Preserves current performance assumptions; rotor code/read standoff still needs hardware verification | Already included in nominal and conservative cases |

## Printed parts excluded from purchased cost

The DES-004 print set remains: 6,400 five-stop rotor/follower pairs, rotor supports and/or axle retainers, frame-fixed coded vanes, writer interface bodies/prongs where printed, and the existing printed frame/cell structure. Print material, print time, failures, and assembly labor are not assigned a purchased-component price here. Integral printed axles, if selected later, must be treated as a changed reliability/manufacturing assumption rather than silently substituted into this BOM.

## Gate disposition

Cost gate: **conditional pass for continued candidate work; not a procurement or production pass**. The nominal calculation is within the project's $400–500 last-resort band, but the conservative service case is $729 and therefore fails the stated >$500 ceiling. Current retail catalog evidence is materially above the target and does not resolve fit. The single most valuable remaining action is a delivered quote and tolerance/availability confirmation for 6,720 axle pins (6,400 installed plus 5% stock), followed by a drawing-level rotor-fit check. Until both are complete, DES-004 cannot claim a $0 purchased delta, procurement approval, or production cost pass.

This is a sourced/allowance and calculation record only. It contains no hardware validation and does not establish supplier availability.
