# E-305 decision report

**Prepare the isolated reversible-force test; do not adopt this as a6,400-cell clutch or replace DES-009.** The strongest simple demonstrator is a purchased axial NdFeB magnet on one sliding conical carrier, moved by one stationary air-core winding. It avoids angular indexing and stationary selector rubbing. The calculations do not establish moderate torque, safe loaded power-loss release, acceptable array interference or competitive complete cost.

| Owner question | Supported answer |
|---|---|
| Permanent magnet on every screw practical? | StockØ3×2-mm axial N48 discs are practical components, ~€0.17 each at a published volume tier. A magnet rigidly fixed to an independently supported screw cannot select by translation unless the whole screw floats; the selected concept therefore uses one separate sliding screw-keyed carrier. Dense-array interactions and assembly remain substantial. |
| Useful stationary reversible force? | Yes in the calculated constrained air-coil geometry:~30 mN at 0.3 A, ~50 mN at 0.5 A across 0.6-mm stroke. This is a finite-size calculation, not a measurement. A nearby steel core can remain attractive for both polarities. |
| Acceptable ON/OFF? | Isolated powered ON and positive-gap OFF are plausible. Continuous ON current is needed. Unloaded vertical gravity return is conditional; power loss under torque is not fail-safe. Shared drive must stop. Terrain height retention remains open. |
| Arbitrary starting angle? | The continuous cone can contact at rest at every relative angle without angular motion by geometric symmetry. Actual torque/release reliability is untested. Specific positive profiles offer self-alignment regions but no demonstrated all-angle loaded seating margin in the examined simple implementations. |
| Simplest mechanism discovered? | One magnet-equipped axial slider, one cone interface, one stationary coil; no spring or second synchronization stage. This is still15 counted cell-associated mechanical pieces including baseline support/coil/retention, plus electronics and shared hardware. |
| Sufficient torque? | At assumedμ=0.25, nominal0.0756 N mm at 0.5 A versus E-303's provisional0.0597 light/0.343 moderate starting scenarios. Light only, with limited margin; actual screw torque unmeasured. |
| Fits5.08-mm pitch? | No for this concrete concept:14-mm housing,13-mm gear,10-mm cone,8.4-mm flange. Staggering alone fails same-level/through-shaft clearance. Finite magnet-neighbor calculations also find~43.5-mN axial interaction for a0.6-mm state offset at pitch. |
| Simpler/cheaper than E-303 A? | One coil and no stationary selector thrust rubbing are genuine simplifications. Overall support, slider, magnet and bipolar electronics negate an assumed cost win. At0.3 A it predicts0.0428 N mm at 0.243 W; at 0.5 A0.0756 N mm at 0.674 W. E-303 A's ideal0.1005 N mm at 0.547 W is a different idealization, not a measured advantage. |
| Ordinary steel periodically remagnetized? | Material-specific yes: published quenched-C45 writing fields are within the order of actuator fields. But short open geometry, low coercivity and repeated reversal make useful stable retained moment doubtful here. Purchased N48 is simpler and its initial magnetizing field is far beyond normal actuation. |
| What remains uncertain? | Actual screw torque; friction/guide forces; real force/current/gap; coil thermal resistance; magnet retention; manufactured cone runout; loaded release; holding after disconnect; interference and manufacturable assembly cost. |
| Observation justifying continued work? | Repeatable≥45-mN upward force at both stroke endpoints at≤0.5 A, useful downward reversal, ≤2-mN isolated OFF parasitic force and tolerable pulse temperature, with measurement uncertainty resolved. Then the owner could choose a single cone torque test. This does not authorize it automatically. |

## Comparison with existing routes

| Criterion | E-305 selected principle | E-303 electromagnetic friction A | Previous row/column couplings | DES-009 primary route |
|---|---|---|---|---|
| Per-cell hardware |15 counted mechanical pieces/allocations +one coil+full bipolar channel |About14 pieces incl.compliant carrier/shim; two-coil concept |E-297 two sliding halves plus captive selectors/support; E-300 cones with row load |Resident screw/pin/support; motors/coupling functions shared on moving bank |
| Moving selection |One axial slider |Compliant closure |Two moved halves; row/column structures |Bank movement and removable coupling, unfinished |
| Angular engagement |Cone invariant; torque untested |Friction invariant |Specific dogs/points conditional; E-300 cone invariant |Automatic coupling unproven |
| Torque/heat |Light scenario plausible;~0.674 W at 0.5 A |Ideal0.1005 Nmm/~0.547 W, unvalidated |Positive seated torque efficient; selector friction harmed cone force budget |One motor moved one screw; torque unmeasured |
| Support and reliability |Separate screw/input thrust support; guide and gravity-return risks |Separate support plus compliant force path |Physical small-part/stiffness/phase failures specific to tested versions |Latest E-302 alignment-sensitive resistance unresolved |
| Dimensions |14 mm housing concept, not pitch compatible |12.4 mm housing concept, not pitch compatible |Nominal5.08 mm CAD; physical assembly/isolation not qualified |Ø8 mm motors require bank packaging solution |
| Cost/repair at thousands |Repeated material/electronics~€7.4k–14.9k before shared system/labor; winding dominates labor |Earlier~€0.80/cell allowance, lower-confidence different cost basis |Fewer electrical channels but many critical moving interfaces |Fewer repeated actuators; chosen trajectory, no complete qualified cost |

These are complete-function comparisons, not a repeated survey of E-303's eight technologies. No previous failure is generalized to all engagement mechanisms.

## Delivery and evidence

[Material research](materials.md) · [Engagement and load paths](engagement.md) · [Actuator/electronics/array analysis](actuator-and-array.md) · [Reproduction and provenance](verification.md) · [One illustrated print test](../../../owner-print-tests/2026-10-25-reversible-magnet-force/test.md).

Prepared6 small parts, actual STLs, parametric CAD, and a genuine saved/reopened X1C0.4-mm PLA Bambu project: **3.63 g /about 50 minutes**. No physical fabrication, force, temperature or torque measurement was performed in this task. All physical result fields are blank. The full clutch CAD is a dimensioned concept/envelope only; force evidence gates its fabrication.

**Stop here. DES-009 remains active. No issues, purchases, schedules, additional experiments or follow-on tasks. Await an explicit owner decision after this delivery.**
