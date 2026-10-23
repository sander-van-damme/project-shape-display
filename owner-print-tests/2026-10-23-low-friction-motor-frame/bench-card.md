# One test before another print

**Use the existing long screw and pin. No new parts, extra current, sanding or knife trimming.** This isolates the cause of your already observed v3 binding; it is not a first test of v3. The detailed protocol and results form are in `test.md` and `results.md`.

1. **Power off. Record the parts.** Pin length: ____; frame/revision: ____; shim: ____; bands: ____. Note which rotor surfaces were shaved and whether those changes helped. Keep observations from before and after shaving separate.

2. **Mark actual height against the stationary frame.** Choose a visibly free low position, then mark +3 mm. Use a ruler or paper marks, not commanded steps. Turn the exposed rotor gently by hand with the frame properly closed. Compare low/high, relieve band pressure briefly while supporting the assembly, then reclose. Record smooth / drag / catch. A loose or shifting motor is not a passing result.

3. **Check the higher position only while free and supported.** Your long screw and removed artifacts make the reported 15 mm plausible. Inspect clearance and thread engagement with the frame open first. Compare manual motion at +3, +6, +9, +12 and up to +15 mm; stop at the first drag, obstruction or lost support. Do not force it to reach a mark. No powered 15 mm run is specified.

4. **Isolate the first failing interface; stop when the result is clear.** Remove the rotor/screw and slide the pin alone through the same marks, closed versus relieved. Keep the unpowered motor and shim seated so their preload remains. If the pin still binds, guide/closure or pin exterior is implicated. If it is free, test the same screw/pin pair outside the frame at those positions. If that is also free, turn rotor + washer without pin/motor with light down/up bias; then, only if free, add the motor without the pin. A change after each addition identifies the constraint that introduces drag. If only the full assembly binds, record an alignment interaction rather than declaring a unique rubbing surface.

5. **Power only after smooth manual motion and secure closure.** Run three slow up/down cycles over the marked 0–3 mm interval with the existing conservative configuration. Record requested and confirmed IRUN, Vref, speed and UART status. Do not increase current. A reset, UART fault or uncertain actual setting makes the powered comparison inconclusive.

**Stop immediately:** jam, shaft moving axially, motor pressing on PCB, unreliable gear engagement, thread damage, excessive heat or lost pin/rotor support.

| Record | Result |
|---|---|
| First measured rise with drag; closed / relieved / reclosed | ____ mm; ____ / ____ / ____ |
| First failing stage; rubbing location; wobble or slip | ____ |
| Actual driver configuration confirmed? UART errors? | ____ |
| Three powered up/down cycles completed? | ____ |

**Pass:** smooth low/high manual movement, normal closed frame, secure motor, retained thread/gear engagement, no excessive wobble or shaft motion, and three documented powered cycles without extra current. This qualifies only the tested range. More freedom with lost support is a failure; electrically obscured powered results remain inconclusive. No new physical pass has yet been recorded.
