---
status: complete
builds-on: [E-050, E-058, A-013]
---

# Catalog servo channels fail cost before mechanism refinement

Reject an A-013 full-row programmer using one Pololu-supplied FS0307 or FS90
position servo per head at the observed public prices. Even 80 positioning
servos alone exceed the entire $500 purchased-hardware ceiling. Stop this
procurement route before detailed gripper/release design. This is a sourced
comparator exclusion, not rejection of all servos, independent actuation or
shared-elevator programming. No purchase or print release.

Input main `2bc0732`. Reproduce with
`python3 tools/curated-experiment-checks/E-059/servo_screen.py`.
Evidence: supplier listing, manufacturer nominal specifications and analytical
calculation; no measurement, geometry simulation or qualified force–speed curve.

## Sources and transfer limits

Accessed 2026-10-08, USD; listed quantity-five prices are the lowest public tier
shown, not a negotiated 80/160/240-unit quote. Shipping/tax are excluded.

| Position servo | Public unit price | At 6 V: no-load s/60° | Peak stall kgf·cm | Specified angle |
|---|---:|---:|---:|---:|
| FS0307 | $9.35 | 0.09 | 0.6 | 120° |
| FS90 | $7.90 | 0.10 | 1.5 | 120° |

Price sources: [Pololu FS0307](https://www.pololu.com/product/3420) and
[Pololu FS90](https://www.pololu.com/product/2818).
Technical sources: [FEETECH FS0307 specification](https://www.pololu.com/file/0J1429/FS0307-specs.pdf)
and [FEETECH FS90-C specification linked by the FS90 seller](https://www.pololu.com/file/0J1435/FS90-specs.pdf).
Both sheets give standard test conditions of 25±5°C and 65±10% humidity.
No-load values are averages, not worst-case ratings. Stall torque is not
continuous usable torque; loaded speed, acceleration, thermal duty and
unit/batch scatter are not established. Do not combine no-load speed and stall
force as an operating point. The FS90-C naming is retained as a provenance
limit. No unqualified expanded angular range is assumed.

## Cost gate and channel completeness

| Heads | FS0307 positioning only | FS90 positioning only | Entire channel ceiling with $250 shared reserve, free cell hardware |
|---|---:|---:|---:|
| 80 | $748 | $632 | $3.125 |
| 160 | $1,496 | $1,264 | $1.5625 |
| 240 | $2,244 | $1,896 | $1.0417 |

The executable enumerates all 1–80 complete row banks for each part: all 160
price cases fail, even with zero reserve and zero cell purchases. These counts
are deterministic accounting, not a sampled population. More heads worsen
this exclusion. At 80 heads and $250 reserve, price reductions of at least
66.6%/60.4% are needed merely to fit the positioning servo in the *entire*
channel allowance; at 240 heads these become 88.9%/86.8%. Additional channel
hardware requires still lower prices.

A complete channel must also acquire a tail at arbitrary initial height,
retain it while unloading/releasing the pawl, drive both directions, re-engage
and prove support, read actual cell height, release and reset. The listed servo
only supplies the positioning axis. A printed rack transmission, gripper,
release linkage/actuation, guides, electrical distribution/control and independent
support/readback remain necessary; no zero cost or successful implementation is
claimed for them. They cannot rescue an actuator-only budget failure. Repeated
cell pawls/returns and bank transport/power must also be counted. Consequently
there is no reason to finish a detailed BOM or manufacturing model for these
already excluded channels.

## Stroke diagnostic, not a timing qualification

For an ideal constant-ratio rack spanning 40 mm over 120°, effective radius is
19.10 mm. Using nominal no-load speed gives 222.2/200.0 mm/s and 0.36/0.40 s
for the inherited 80-mm acquire/move/return path. Eighty serial stations then
consume 28.8/32.0 s in motion alone; even E-050's optimistic 2-s overhead makes
30.8/34.0 s before contact, verification or indexing. This nominal diagnostic
cannot establish a guaranteed timing rejection because the datasheet averages
are not strict speed bounds. Cost supplies the decisive rejection.

Ideal stall-force endpoints are 3.08/7.70 N at that ratio. Larger effective
radius trades force for speed; smaller radius cannot cover the full travel
within 120° without a different transmission. Loss, backlash, end-stop margin,
loaded slowdown and acceleration are omitted. E-058's force–speed/power gate
therefore remains unmet. A larger pinion, gear ratio or staggered mounting does
not remove the sourced price failure. Geometry and printed-fit uncertainty
need no refinement for this procurement route; no yield or reliability claim
is made.

Self-review: exact rational prices, all row-bank counts, cost monotonicity,
independent four-times-60° round-trip identity and SI torque conversion checked
by executable assertions. No independent review or physical validation claimed.

## Consequence and reopening

Keep A-013 conditional. Reopen this route only with a materially cheaper
like-for-like quote and a complete channel within E-050's allowance, or a changed
head-count/schedule architecture. No inference about cheapest worldwide supply
follows from two listings. The shared elevator avoids a positioning servo per
head, but still needs an affordable independently selectable gripper/release
and support-proof sequence within E-051's dwell limits. Next compare an explicit
shared-energy selector/contact mechanism or a substantiated lower-cost complete
channel; stop catalog-servo layout work and further nominal pawl refinement.
