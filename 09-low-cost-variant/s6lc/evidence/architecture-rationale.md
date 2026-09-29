# S6-LC architecture rationale and alternatives considered

**Evidence class: CALCULATION + CAD; no print/measurement** ([DND-27](/DND/issues/DND-27)).

## 1. The binding constraint

[DND-70](/DND/issues/DND-70): same product, purchased parts **< $250 excluding
printed**. At the additive 1.16 uplift this is a **parts budget of $215.52**.
S5-R's fixed legacy base alone is $218.70, so S5-R cannot be trimmed; the machine
must change.

## 2. Design levers, ranked by dollars

| Lever | S5-R | S6-LC | Saving |
|---|---|---:|---:|
| Remove the 40-solenoid writer bank | 40 × $2.50 = $100.00 | **$0** (passive mask) | $100.00 |
| Remove the 2 bank motors | 2 × $12 = $24.00 | (1 lift + 2 small) $28 | net −$4 |
| Replace legacy lift/scan stock | $218.70 fixed base | ~$92 lean axis | ~$127 |
| Remove the 80-channel driver block | in fixed base | (3 driver channels) | (in above) |
| Keep frame/columns/pawls printed | partly bought | **all printed** | (in above) |

The dominant saving is the writer bank plus the legacy lift/scan stock. This is
why the answer is a **broadcast passive-mask** machine, not a cheaper solenoid.

## 3. Alternatives considered (and why rejected)

| Alternative | Verdict | Reason |
|---|---|---|
| Trim S5-R BOM lines | **rejected** | fixed base ($218.70) alone busts the $215.52 parts budget |
| Per-cell solenoid + latch | rejected | 6,400 coils → thousands of $ and wires ([Test10]) |
| One XYZ writer | rejected | >213 cells/s serial; modelled ~76 min ([Test10]) |
| **S6-LC broadcast mask (chosen)** | **adopted** | 3 bought motors, all gates pass, $139.77 parts |
| S2 planar first-stop tiles | held | needs 256 plates + a writer; more bought structure |
| Keep 40 soldenoids but cheaper ones | rejected | still ~$60–100 and 40 bought actuators; cost cliff remains |

## 4. Why banking (8 × 10 rows)

A single all-armed broadcast stroke would have to release every armed pawl at
once: 6,400 × 0.160 N = **1,024 N**, above the S1 2.4 kN-style failure. Banking
the **reset** to 800 cells bounds it to **128 N**. Banking is not needed for
*writing* because writing is passive (the mask decides), so S6-LC keeps the fast
global 4-stroke write and pays the reset bank-by-bank.

## 5. Discriminating next tests (no print allowed)

The most informative **no-physical** test that could kill S6-LC is a **CAD +
mechanism-dynamics study of the release-comb trip under a loaded neighbour**,
followed by a **release-force-spread sensitivity** that answers: at what
per-part sd does the broadcast decode become unreliable, and does per-bank
gating survive it? [DND-78](/DND/issues/DND-78) (Falsifier) owns the adversarial
version; [DND-75](/DND/issues/DND-75)/[DND-76](/DND/issues/DND-76) invent
alternatives.
