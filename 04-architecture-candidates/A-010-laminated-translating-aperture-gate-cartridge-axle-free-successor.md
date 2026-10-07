---
status: candidate
builds-on: [DES-004, M-013, M-014, P-006, P-008]
---

# A-010: laminated translating aperture-gate cartridge (axle-free successor)

## Disposition

**Candidate for one cheap falsification test; not a replacement selection.**
This architecture removes the DES-004 precision-critical cylindrical axle/bore
interface, but moves risk into planar sliding friction, gate registration and
the shared lift/follower interface. It is worth a final-pitch strip test only
if an axle-free architecture is strategically preferred over DES-004's simpler
rotor geometry.

## Operating principle and interface sketch

Each 5.08 mm cell contains a thin printed gate slider captured between two
flat guide laminations. The slider has five indexed aperture positions (one
for each terrain level) and a compliant printed detent at each position. A
travelling writer pushes the gate laterally; a hard end stop, not a shaft,
defines the five locations. A separate vertical follower/post for the cell
passes through the selected aperture and lands on the first solid stop in a
stacked stop plate. The follower carries tabletop load through broad planar
shoulders and the stop plate; the gate stores selection but does not carry
terrain load. A travelling lift head unloads and raises only the addressed
post while the gate is changed. A fixed reader observes the gate code or
follower height after settling.

In section, the stack is: `load post -> broad shoulder -> 5-level stop plate ->
five-position gate aperture -> lower guide`. In plan, the gate is a rectangular
strip with five windows and a writer tongue, with no round pin, bore, bush or
rotating member. Gates can be made as replaceable cartridges in 5x5 regions;
the frame and lift/reader hardware remain shared.

The intended regional-update sequence is: unload target post, move its gate,
raise/lower target post against the selected hard stop, verify, and release it.
Untouched posts remain on their stops. This is an architectural assumption,
not a measured isolation result.

## Comparison with DES-004

| Attribute | A-010 translating gate | DES-004 five-stop rotor |
|---|---|---|
| Precision interface | Planar slider clearance, aperture registration, broad post/stop guidance; no axle diameter or printed rotor bore | Rotor pocket, 1 mm axle/1.4 mm bore, shaft alignment and detent friction |
| New purchased parts | Analytically zero new per-cell metal parts if all guides, detents and gates are printed; likely extra low-cost sheet/fastener only if cartridge reinforcement is needed | 6,400 axle pins; nominal allowance $128, conservative installed/stock allowance $336 |
| State/load separation | Explicit: gate remembers, stop plate/post supports | Rotor both stores state and transmits load |
| Regional update | O(changed cells) in principle; requires target post unload and re-seat | O(changed cells) in principle; rotor actuation/return remains unresolved |
| Compactness | Thicker laminated stack and a post/lift path; cartridge serviceability is favorable | More compact cell, but axle retainers and rotor envelope are dense |
| Assembly | Many thin layers and one slider per cell; cartridge replacement possible | One rotor/follower and one axle per cell; axle insertion is a major operation |
| Reliability risk | FDM flat-surface friction, debris, slider creep, gate skew, stop-plate registration, post buckling | FDM axle/bore fit, rotor friction/wear, detent consistency, neighbour coupling |

The purchased-component comparison is a calculation from the DES-004 BOM, not
a quote. Removing the axle line would make the nominal allowance about $370
before any A-010-specific parts, versus DES-004's calculated $498. Printed
parts, print time and assembly labor are excluded in both figures. The apparent
cost advantage is therefore conditional: if the laminations require bought
stock or the slider fit causes scrap, it can disappear.

## Analytical acceptance criteria

These are gates for a coupon, not claims about the process or hardware:

1. A 5-cell, final-pitch strip must expose all five gate states without a
   cylindrical fit. Under the project's assumed dimensional envelope, the
   slider must have at least 0.20 mm total lateral running clearance while
   the aperture-to-follower registration retains at least 0.20 mm usable
   overlap margin at every state. Actual FDM spread is unresolved.
2. With a representative follower load applied analytically at the stop,
   the gate must remain unloaded by the load path: no gate face may be the
   sole support surface. A CAD section and hand free-body check must show a
   positive shoulder/stop path around the gate.
3. The writer must complete the worst-case four-state travel plus settle in
   no more than 9 ms per changed cell if the DES-004 30 s full-field budget is
   to remain plausible. This reuses DES-004's 8 ms actuation + 1 ms settling
   assumption; it is not a measured timing result.
4. A target update must leave every adjacent unloaded/loaded post within
   0.10 mm of its pre-update position in the analytical stack-up. This is a
   regional-isolation criterion, not evidence of actual displacement.
5. The reader must classify the five gate states with a geometrically positive
   registration margin and reject an aperture partly between states. Optical
   threshold margin remains unresolved until a reader implementation exists.

Fail the architecture if any state requires a tight printed sliding fit,
serial multi-pass writing, gate load-bearing, or a full-region reset to avoid
neighbour disturbance. Those failures would give up the reason to prefer it
over DES-004.

## Explicit failure modes and unknowns

- Flat guide friction or debris prevents a gate from reaching a hard stop.
- Printed detents creep, wear, or become ambiguous after repeated rewriting.
- A skewed slider clips the follower, causing a missed height or a jam.
- Stop-plate registration stacks across laminations and erases aperture margin.
- The post buckles or tilts under load despite the broad shoulder concept.
- Unloading one post transfers force/vibration into adjacent posts.
- A gate can be read geometrically but not with adequate optical/electrical
  threshold margin.
- Cartridge seams, print warp and layer orientation may dominate assembly yield.
- The 9 ms timing bound and 0.10 mm isolation bound are assumptions pending
  physical measurement; no fit, force, wear, reader, cycling or reliability
  claim is made.

## Cheapest decisive follow-up experiment

Print one 5-cell final-pitch gate strip with its two guide laminations, a
five-state stop plate, five dummy followers and one writer tongue. Use the
same nozzle/layer/material metadata required by Q-009. Without a full display,
manually or with one reused actuator command every state and adversarial
patterns (alternating 0/40 mm and one-cell changes beside loaded dummies).
Measure: gate travel force, state reach/return, aperture registration,
neighbour displacement, post/stop load path, and before/after clearances over
at least 1,000 state changes. Add a simple timing log only if the strip reaches
all states reliably. Reject immediately for any state that needs a tight
printed fit, any gate load transfer, or any adjacent displacement above the
criterion. This is a falsification coupon, not life qualification.

## Evidence boundary

DES-004's geometry, BOM and timing values are repository calculations/CAD-derived
or sourced allowances. The A-010 interface, cost delta, timing screen and
acceptance criteria above are analytical inferences. No physical validation is
available, and this candidate does not change DES-004 or close Q-009.

## Reproducibility checks

- Command: `./repo check` — result: passed; the helper also collapsed the
  already checkpointed E-012 workspace to its result document.
- Command: `python3
  08-integrated-designs/DES-004-five-level-rotary-verified-successor/analysis/five_level_successor_bound.py`
  — result: exit 0 with no assertion/error output.
- Command: `git diff --check` — result: passed.
