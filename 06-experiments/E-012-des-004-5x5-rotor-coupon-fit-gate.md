---
status: complete
builds-on: [DES-004, Q-009, E-011]
---

# E-012: DES-004 5x5 rotor coupon fit gate

## Scope and evidence boundary

This experiment freezes the coupon geometry and executes reproducible nominal
and independent worst-case arithmetic. It does not substitute for printing,
inspection, force measurement, optical readback, or cycling. There was no
physical coupon available in this run; all results below are calculated or
simulated.

## Frozen coupon

| Interface | Nominal definition | Tolerance used for analytical screen |
|---|---:|---:|
| Array/frame | 5 × 5 at 5.08 mm pitch; 25.40 mm span; 40.00 × 40.00 × 3.00 mm frame | pitch ±0.03, frame ±0.10 mm |
| Rotor/pocket | Ø3.00 × 3.00 mm rotor; Ø3.40 mm pocket | rotor radius ±0.05, pocket radius ±0.05 mm |
| Axle/bore | Ø1.00 × 10.00 mm candidate pin; Ø1.40 mm rotor bore; 8.00 mm retained stack | axle/bore ±0.05 mm |
| Coded vane | integral 0.45 × 1.20 mm vane; five stops at 22.5° increments | width ±0.05 mm |
| Writer | 0.80 × 1.00 × 1.00 mm blunt tongue; 1.20 × 1.40 mm receiving pocket | ±0.05 mm |
| Reader | 2.00 × 2.00 × 4.00 mm fixed head; 0.70 × 1.00 mm aperture; 1.80 mm standoff | aperture registration to be measured |
| Load station | centre-cell service-load point, 3.27 N target | physical load application unresolved |

Source CAD is `08-integrated-designs/DES-004-five-level-rotary-verified-successor/cad/des004_rotor_coupon_5x5.scad`.

## Results

The initial script passed the rotor-body checks but omitted vane-to-frame
clearance. That omission is a geometry blocker: the original 1.70 mm pocket
radius was smaller than the vane's 2.016 mm nominal outer corner radius.

The repaired script uses a 2.20 mm pocket radius. It passes the nominal and
assumed-tolerance vane-to-frame check with approximately 0.055 mm minimum
radial margin, while retaining 0.70 mm nominal rotor radial clearance and
0.68 mm nominal adjacent-pocket web. The other nominal checks remain passing:
7.30 mm frame margin/side, 0.40 mm axle/bore diametral clearance, 2.08 mm
nearest rotor-edge gap, 1.355 mm vane-to-neighbour-body gap, 2.00 mm pin-end
margin, 0.40 mm writer side clearance, 0.40 mm writer width clearance, and
0.50 mm vane-to-reader-aperture width margin.

The independent worst-case screen passes the geometric assertions: 7.175 mm
frame margin/side, 0.60 mm pocket radial clearance, approximately 0.055 mm
vane-to-frame radial clearance, 0.30 mm axle/bore diametral clearance, and
1.95 mm rotor-edge gap. These are assumed tolerance
limits, not a reliable FDM clearance rule; the candidate pin must not be
released until measured process spread and actual pin tolerance are known.

The ideal logical smoke model ran 10,000 commanded transitions through all
five states with 10,000 reads and zero model state errors. This is a software
simulation of command/read bookkeeping only. It is not the requested physical
smoke sequence and provides no evidence for detent time, return force, reader
margin, or adjacent displacement.

## Fit-gate disposition

Analytical envelope after repair: **PASS with vane-margin and axle-clearance
risk flags**. Physical fit
yield, registration, detent time, commanded/read error rate, return force,
and adjacent displacement: **UNRESOLVED / no measurements**. Therefore the
physical fit gate did not pass, and no physical 10,000-transition sequence
was authorized or claimed. The smallest justified correction is not yet
selectable: changing the bore or pin without measured X1C/PLA spread would
be an ungrounded design change. Q-009 remains open for a printed matrix with
nozzle, layer, orientation, filament lot, compensation, measured clearance,
fit yield, friction, and before/after cycling records.
