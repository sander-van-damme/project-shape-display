# Whole-machine cost and manufacturing disposition

**The $500 benchmark fails for the catalog-selector implementation. Conventional two-bank construction also exceeds $1,500 before custom resident mechanisms. No cheaper complete manufacturing route is qualified.** These are incomplete allocations, not supplier quotes.

## Account for the actual reference machine

The reference is 4,096 sites, 406.4 mm square, two banks and 128 reused data actuators. USD prices were observed on 14 October 2026, before freight and tax. Sources, stock limits and unquoted provisions are in [research.md](research.md) and [bank-drive.md](bank-drive.md). The [independent revised audit](review/revised-system.md) reproduces the arithmetic.

| Item | Quantity / basis | Allocation |
|---|---|---:|
| Adafruit 2776 data solenoid | 128 at $3.96 | $506.88 |
| Adafruit 6318 eight-channel driver | 16 at $13.46 | $215.36 |
| Remaining generic motion accounting pairs | Four assigned plus two reserve, $20.95 each | $125.70 |
| Two conventional lift transmissions | Four 1605 screws/bank; motor/driver, supply, supports, synchronization and guide/catch provisions | $903.34–1,423.82 |
| Reference solid PLA terrain columns | 14.9298 kg at assumed $20/kg | $298.60 |
| Main frame allowance | Incomplete, unquoted | $80 |
| Controller allowance | Unquoted | $30 |
| Selector/control power allowance | Capacity and duty unqualified | $100 |
| Common wiring/fusing/connectors | Unquoted | $50 |
| **Incomplete allocation** | Excludes custom resident fabrication | **$2,309.88–2,830.36** |

Removing the two reserve axes reduces this by $41.90. Six assigned duties are two terrain lifts, two row-address mechanisms and two A/B sequencers. Two cheap lift entries have been replaced by conventional transmissions. A two-track sequencing cam would have to generate the separate A/B motions and carry their forces; it is not a qualified $20.95 mechanism simply because one motor could turn it.

The $100 common power allowance concerns selectors/control; the lift provisions separately count 36-V supplies. Neither is a sized specification. Reference coils can draw **704 W / 140.8 A at 5 V** simultaneously. Duty, loaded force versus stroke, return mechanism, distribution, board current and staggering latency remain unresolved.

Without the suitable lifts, the earlier $889.84 electronics anchor plus actual polymer and minimal common allowances leaves only **$51.56, or 1.26 cents/site**, under $1,500. The former $208.89 remainder used lighter columns and is superseded. Neither remainder pays for the resident mechanism.

## Repeated construction cannot be free

The study requires at least 4,096 each of terrain columns, C-guides, A lifting keys, B release followers and ground pawls; 8,192 key-guide interfaces; 8,192 positive end-register interfaces with 16,384 pockets; 8,192 programming lugs and matching pockets; and local rigid pawl seats. Add 64 row cassettes, 256 codebars, 128 A rails, 128 B rails, bank frames, paired-bar links, guidance and indexing. Combining contacts into combs reduces piece count without removing their tolerance or friction.

| Construction family | Process to investigate | Present obstacle |
|---|---|---|
| Broad columns and rack tails | Side-printed open racks for experiments; molding or stock bodies with attached tails for scale | Solid reference is 221.2 mm long and 14.93 kg total. Hollow or assembled alternatives need their own joints and mass accounting |
| Ground-pawl combs and rigid seats | Etched/formed spring metal with stiff backing | Return force, formed phase, fatigue and yield unmeasured; ordinary laser-cut stock is not a quote for a fine etched spring |
| Bilateral C-guide memories | Formed/laminated precision metal or qualified custom profile | About 8.25 kg of channels, tiny lips, thousands of joins and paired register alignment; no affordable process demonstrated |
| A/B keys and guides | Metal micro slides or a redesigned constrained coupling | Reference 0.10-mm walls and 0.15-mm lips are not ordinary FDM. Longer-guide variant still lacks guaranteed vertical unloading margin |
| Paired bars and row cassettes | Pocketed sheets, distributed supports and exterior linkage | Reference bars add 3.45 kg; 20-ms data motion requires about 0.463 N inertia/setter including one channel, before friction. Unsupported full-width cassette bending is unacceptable |
| Bank frames and transmissions | Standard bearings/screws with fabricated stiff structures | End connections, neighboring-bank clearance, brake/catch and force-limited seating remain unreleased |

No quoted low-cost process for thousands of channels and closures was found. Welding, crimping, lamination or molding must be demonstrated and priced before receiving credit. Closed channels require inserting both T-feet before the final closure, or a real removable face; there is no concealed microscopic service screw.

One minute of fitting per site adds **68.3 hours**. The nominal channel construction adds 8,192 closure/join operations before other assembly. At an illustrative effective deposition rate of 5–15 g/hour, reference columns alone require **995–2,986 print-hours**. Those are throughput sensitivities, not production-pin slicer predictions. A successful 52-g rig cannot establish array yield or an economical print farm.

## Manufacturing decision

Build the manual rack article before committing to precision resident hardware. Its ordinary PLA/M3 construction tests support transfer and is intentionally different from the metal micro slides. Success must be followed by a toleranced neighboring resident module, an actual process quote and powered row-cycle evidence. The short-flag memory coupon is deferred; it is not a current manufacturing qualification request.

The earlier traveling-head and material comparisons remain in [the preserved manufacturing screen](review/manufacturing-screen.md), with `analysis/cost.py` and its CSV/JSON outputs. They explain rejected options; they are not prices for the current geometry or a complete machine.
