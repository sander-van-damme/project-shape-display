# DES-004 purchased-component cost reconciliation

Date basis: 2026-10-06. Currency: USD. 3D-printed parts are excluded from the purchased-component totals.

## Reconciled result

| Case | Purchased total | Delta vs DES-003 | Status against project cost bands |
|---|---:|---:|---|
| DES-003 baseline | $370 | — | Acceptable allowance ($200–400) |
| DES-004 nominal | $498 | +$128 | Last-resort band ($400–500) |
| DES-004 conservative spare/consumable | $729 | +$359 | Unacceptable (> $500) |

The machine-readable calculation is in `bom_des004.csv`. The baseline is the $370 subtotal from `DES-003/bom_a1.csv`; its rows are sourced-class or allowance values, not live purchase orders. DES-004 retains those bought items, including the eight writer actuator positions and eight reader heads, so they are counted once and marked as inferred reuse. No new reader electronics, writer motors, gantry motors, guides, drivers, power supply, loom, switches, or fasteners are silently omitted.

The rotary successor adds one axle per 5.08 mm cell: 6,400 metal pins. The nominal $0.020/pin is an engineering bulk-price target, not a supplier quote. The conservative $0.050/pin basis represents low-volume cut/debur handling and adds one writer actuator, one reader head, one driver module, and 5% axle scrap/service stock. Availability, exact diameter/length, tolerances, corrosion finish, and a delivered quote remain unresolved. These are the single largest cost uncertainty and the only new purchased item driving the delta.

## Sourcing evidence and alternatives

The retained component classes are inherited from the DES-003 allowance and are not re-quoted here. Product-class references checked for the inherited items are [NEMA-17 example](https://www.frankhumotor.com/nema-17-stepper-motor), [DRV8833 module example](https://electropeak.com/drv8833-dual-motor-driver), and the [TI DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf). These references support component identity only; they do not establish the CSV prices or current availability.

| Alternative | Purchased effect | Engineering effect | Decision |
|---|---:|---|---|
| Quote bulk stainless/music-wire pins and cut in-house | Could approach nominal case; exact delta unknown | Adds cutting, deburring, inspection, corrosion and tolerance work; risks friction and cycle life | Preferred cost-down investigation; quote before gate closure |
| Buy pre-cut precision pins | Higher unit price than bulk target, lower assembly risk | Best dimensional repeatability and maintainability; supplier MOQ/availability unknown | Viable reliability fallback |
| Print integral axles | Removes the estimated $128 nominal / $320 conservative purchase | Adds creep, wear, clearance and replacement risk at 6,400 interfaces; assembly may simplify but durability is unqualified | Not counted as a cost-gate pass without coupon evidence |
| Reuse existing reader/writer interfaces | Avoids 8 new heads and associated wiring | Preserves current performance assumptions; rotor code/read standoff still needs hardware verification | Already included in nominal and conservative cases |

## Printed parts excluded from purchased cost

The DES-004 print set remains: 6,400 five-stop rotor/follower pairs, rotor supports and/or axle retainers, frame-fixed coded vanes, writer interface bodies/prongs where printed, and the existing printed frame/cell structure. Print material, print time, failures, and assembly labor are not assigned a purchased-component price here. Integral printed axles, if selected later, must be treated as a changed reliability/manufacturing assumption rather than silently substituted into this BOM.

## Gate disposition

Cost gate: **conditional pass for continued candidate work; not a procurement or production pass**. The nominal calculation is within the project's $400–500 last-resort band, but the conservative service case is $729 and therefore fails the stated >$500 ceiling. The single most valuable remaining uncertainty is a delivered quote and tolerance/availability confirmation for 6,400 axle pins (including scrap/spares). Until that quote and a matching fit/wear check exist, DES-004 cannot claim a $0 purchased delta or a final cost pass.

This is a sourced/allowance and calculation record only. It contains no hardware validation and does not establish supplier availability.
