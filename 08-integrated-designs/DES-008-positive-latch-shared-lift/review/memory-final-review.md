# Independent memory-coupon review and revision-3 disposition

Reviewed source: `cad/memory_coupon.scad` (canonical copy of the reviewed source), SHA-256 `c6bd26a5f29215c4c34e9e8b53471034562b58a0cf65c35863cc9377d86f89fd`.

## Findings that changed the design

1. **Revision 2's capture guarantee was invalid.** Its long post sleeves constrained cassette rotation, while the 2.4 × 1.2 mm flag shoulder remained free to roll in a 2.8 mm-wide open-top trough. The shoulder diagonal is only 2.68 mm, so this trough could not provide the claimed angular restriction. Applying the cassette's 4.667° angle to the flag was unjustified. Its 0.185 mm tolerance claim has been withdrawn.
2. **A roof alone would make assembly impossible.** Revision 3 therefore adds an explicit loading window at X = 23.2–27.5 mm, beyond the rightmost operating shoulder edge at X = 22.05 mm. Load the first flag through this window and slide it left before inserting the second; this is done off the base. Thirteen additional nominal collision cases cover insertion and sliding.
3. **The wider shoulder invalidated the old flat flag print orientation.** The narrow foot and lug would begin in midair. Revision 3 uses sacrificial end towers and 0.16 mm-thick necks at the foot bottom and lug top. The first spanning layer has anchors at the tower and shoulder; no support touches the functional side walls. The towers are clipped at end faces. This still requires physical bridge-quality and dimension checks.
4. **Captive shoulders do not justify a general three-dimensional tolerance proof.** The cassette roof has a central opening. A simple two-angle calculation only applies while the relevant shoulder points remain under its retaining rails, with zero yaw. That restricted screen gives 0.369 mm, but coupled yaw/translation/tilt remains unresolved. The current handoff explicitly says this and requires deliberate biased acquisition/lowering tests. The screen is not an acceptance pass criterion.

## Final geometry

- Positive pockets remain the stored-bit registers; no friction detent is substituted.
- A 3.4 × 4.0 × 1.2 mm shoulder is captured in a 4.4 mm-wide, 1.4 mm-high channel with 0.8 mm retaining roof and a 2.8 mm central opening.
- Stored foot engagement is 2.1 mm; row lift 2.7 mm; nominal acquisition overlap 1.6 mm.
- Guide sleeves remain 10 mm long. The right post moves to X = 31.5 mm for the loading port.
- The raised foot clears the floor by 0.6 mm; the raised lug clears its channel roof by 0.4 mm; the raised cassette clears the bar by 0.3 mm. Nominal adjacent-cassette gap is 0.95 mm.
- Keyed keepers retain the code bars positively. Local bar lift must be checked at both rows, including tilt rather than just one end's clearance.

## Checks actually performed

`validate.py` exports nineteen closed/watertight plate bodies and checks 83 sampled nominal CSG cases. No positive intersection volume appears. Wrong-OLD acquisition has 2.112 mm³ blocking overlap. These are sampled nominal cases; no continuum or tolerance sweep is claimed.

PrusaSlicer 2.7.4 comparison, 0.4 mm nozzle, 0.16 mm layers, three walls, solid infill, supports OFF and 1 mm brim: 11.02 g; 2 h 1 min 24 s; no warning. Plate size is 82.6 × 99.6 × 16.6 mm. `flag-bridge-preview.png` plots actual first-flag paths at Z = 0.80, 0.96 and 1.12 mm. At Z = 0.96 the thin paths span continuously from shoulder to both towers. The slicer classifies those as Overhang perimeter; it does not create disconnected midair islands there. The cassette guide-hole roofs and base key holes still require physical bridge inspection.

## Disposition

The source is suitable for the root engineer's final independent slice and optional small fabrication handoff. There is no observed physical pass. This is a meaningful multi-bit memory experiment that tests retained addressing and unchanged neighbors, with a much more explicit shoulder load path than revision 2. It does not establish terrain actuation, memory-to-dog/pawl integration, powered decoding, 80 ms row timing, production tolerance yield or complete-machine feasibility.

A centered-only success is insufficient. Repeat OLD acquisition and NEW writing with cassettes biased through their free guide play and with each codebar lifted through its available play over each row. Record jamming, missed coupling, failed pocket seating, neighboring movement, keys moving, cracks and cleanup. Failure identifies a mechanical acquisition or tolerance problem; success permits designing the next integrated memory/readout article. Neither outcome should be rewritten into a claim about full-machine throughput.
