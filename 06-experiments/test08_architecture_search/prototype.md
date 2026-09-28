# Next physical experiment and decision gates

## Print the six-cell passive coupon first

Use the **3×2 geometry at full 5.08 mm pitch**, not an enlarged demonstration.
It is the smallest useful coupon with an interior column in a row, both lateral
neighbors, a neighboring row, different heights, and guide-wall interactions. The active
rectangle is 15.24×10.16 mm; allow an external fixture for clamping the guide
tiers at their documented heights. Print six solid followers, six rotors, six
slotted follower guides, the two upper guide tiers and the lift plate. Default
STLs come from `cad_check.py`. The guide tiers are separate solids in one export;
split them in the slicer and preserve z=110.2–114.2 /118.2–122.2 on assembly.

**These are contact/guide coupons, not an assembled automated printer.** The
fixture must hold rotor axes and guide tiers square. Support rotors in reamed
printed bushes, rotate them by hand without lifting their shafts, and raise
the common plate with a micrometer or an external screw stage. A final thrust
retainer, brake, detent leaf and motor head are not included in these STLs.
Do not interpret their omission as proof that those parts fit or work.

Suggested first fabrication: a 0.2 mm nozzle / fine layer process for the 0.2 mm
upper-guide walls, with the follower printed on its side and the toe layer
orientation recorded. If the walls cannot be printed reliably, that is a
geometry failure, not a reason to quietly enlarge the pitch. Resin is a second
process experiment, not an assumed tool already available to the builder.
Use a 0.01 g balance or better, calipers, a dial indicator, calibrated small
weights, a camera, and a low-range force measurement setup. An ordinary luggage
scale cannot resolve the critical millinewton friction.

Record the printer, nozzle, layer height, material/lot, orientation and every
manual reaming/sanding operation. First run as printed; then document a single
controlled cleanup method. Keep failed coupons and dimensions.

| Measurement | Method | Continue / abandon gate |
|---|---|---|
| Miniature travel requirement | Identify one actual representative D&D miniature, including its base; measure maximum height and record identity/photo | 40 mm stroke must exceed measured height. If not, enlarge stroke and rerun density, timing and load calculations before any compliance claim |
| Sliding return | Weigh each follower; measure breakaway force across entire stroke, all orientations, clean and with realistic dust; repeat after cycles | Maximum downward drag < half the measured weight (nominal solid-body gate **10.1 mN**). Every column must follow lowering and settle in the allotted 0.4 s. Any persistent stick fails |
| Independent heights | Exercise all 25 old/new height combinations and all neighboring low/high patterns; measure final tops | Within ±0.25 mm, no neighbor displaced by >0.1 mm, no extra operator nudge |
| Load support | 1 N on one cell at each height for 24 h; 5 N for 10 s; observe toe, sector and guide | No level change, crack or permanent displacement >0.25 mm. 5 N is a screening abuse load, not a whole-hand safety certification |
| Lateral handling | Apply 0.1 N then 1 N at maximum extension with neighboring cells low/high | Quantify deflection. No permanent jam or unintended level change after unloading; establish an honest permitted side load |
| Clearance under reset | Measure minimum gap between lifted toe/body and every rotating sector under representative platen deflection | ≥0.5 mm everywhere; baseline nominal is 1 mm |
| Process viability | Log hands-on time and scrap over at least 30 cell sets | If each assembly needs bespoke sanding or matching, stop full-scale fabrication and redesign guidance |

The cam-beam model predicts only 4.96 N ideal critical load even after the core
revision. Use a sacrificial coupon for the 5 N test; expect that a support or
material redesign may be necessary. A passed miniature-weight demonstration
must not override this failure gate.

For friction, a calibrated 0.1 g mass provides roughly 0.98 mN. Small differential
weights or a calibrated compliant force gauge can resolve the requirement.
The full device may not rely on added miniature weight to make columns return.

## Only after that passes: one driven cam, then an eight-channel head

The passive coupon does not test mechanical memory under vibration. Print and
test a replaceable detent leaf around the modeled wheel: starting hypothesis
10 mm free length, 0.45 mm thickness, 1 mm width, 0.2 mm deflection. The beam
estimate is only 6.8 mN and 0.135% surface strain. Add an individual angular
home stop and a thrust retainer; measure their space and loads. These details
are intentionally not treated as solved by the sector model.

Use one actual candidate PM motor, dual H bridge, thrust-retained rotor and
spring-loaded friction face coupling. Record part identity, delivered price,
voltage, coil resistance, loaded torque/speed, temperature and supply current.
Do **not** substitute the DFRobot no-load speed or the old surplus price for
measurements on the bought motor.

The qualification transaction is: engage; home 22 steps; settle; write up to
16 steps; settle; disengage; detent-seat. Nominal durations in `params.json`
must hold together. After random starting angles and intentional slips, require
the seated rotor angle within **±6°**, not merely an apparently correct motor
step count. The complete 80-channel extrapolation must stay below 27 s using
measured conservative durations, leaving at least 3 s for variability. The motor
must supply at least **0.15 mN·m running torque at 400 pps** for the initial
hypothesis, with measured total rotor/coupler friction less than half that.
If it cannot, rerun at measured rate: 200 pps already fails the full-map limit.

An eight-channel, two-row head then tests simultaneous engagement, shaft fan-in,
80-channel electrical extrapolation, neighboring selection and row motion. Use
at least 10,000 randomized operations per cell, including power cuts during
homing and disengagement. Zero failures at this stage permits a larger test;
it does not establish full-system reliability. No per-cell indexing feedback
exists in the current cost model, so a plan to detect silent miswrites must be
priced and timed if required to meet reliability.

Separately test a full-width dummy platen with the predicted 13.24 kg column
mass plus structure, four synchronized screws and deliberately uneven loading.
Require <0.25 mm flatness change, no racking, an adequate torque-speed margin and
controlled behavior on power loss. Small coupons cannot validate that structure.

## Stop criteria

- Abandon the current five-level cam geometry if it cannot retain/seat within
  ±6° without power or if a single-step error escapes the detent's correction.
- Abandon gravity return if the measured drag gate fails after controlled
  cleanup, wear or dust. Adding 6400 return springs is a new architecture/cost
  assessment, not a minor fix.
- Reject any purchased BOM above $500 delivered, including required braking,
  sensing, better motors and spares. Seek $400 or less; the current working BOM
  plus contingency fails this gate.
- Reject if conservative full-map timings reach 30 s, or if readiness requires
  manual fault repair. Never remove homing/reset from the timing to obtain a pass.
- Abandon ordinary-FDM fabrication at this geometry if guide-wall yield and
  surface tolerance cannot be maintained across multiple print batches.

Continuation needs **all** timing, cost, pitch, measured travel, holding and
return gates. If they fail, revisit the Jacquard/custom-selector branch with
its own measured actuator and catch coupon; do not finish the cam head on faith.

## Measurement record

Copy `physical_measurements.csv` per build. Empty cells deliberately mean “not
measured.” Do not replace them with simulated values. Record every failure,
including its recovery time; report full-map readiness separately from command
completion.
