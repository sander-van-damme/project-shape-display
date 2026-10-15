# DES-008 construction principles and mechanical bounds

The full-machine arrangement is a conditional engineering hypothesis. See the main report for its failed and unresolved product requirements.

## Full-machine construction principle

The comparison surface is **406.4 × 406.4 mm**, sixteen one-inch squares per side. Two banks each contain 32 × 64 sites at 6.35-mm pitch. The 5.08-mm comparison has 40 × 80 sites per bank. Height shelves at 5-mm intervals provide nine levels over 40 mm, or eleven over 50 mm. The 2-mm case is a performance sensitivity; its smaller physical engagement geometry is not qualified.

Each terrain column has a guided upper body and an open lower rack. The upper body supplies a broad miniature-supporting cap; the narrower lower rack leaves room for the mechanisms. Two guide planes constrain rotation and lateral motion. A **normally engaged grounded pawl**, backed immediately by a rigid seat, holds a rack shelf. Its spring supplies lateral engagement bias, not the terrain's vertical load path. The same pawl remains loaded throughout every unrelated update.

A captured dog can enter a second rack face. Its groove has both upper and lower flanks: it pushes up and pulls down. Gravity is not the return actuator. A bank lift moves all selected dogs by the same signed increment. Different heights result from different subsets participating in successive increments; targets are not limited to one common height.

The resident memory is written only when all pins are on their grounded pawls and all moving dogs are unloaded and withdrawn. It gates **two separately sequenced functions**: A, dog engagement; B, grounded-pawl release. Two common actuation frames may drive these functions while the fixed mask is held. A positive guide or equivalent follower must carry lateral engagement through the entire Z excursion. A flag that simply makes the ground pawl the logical inverse of the moving dog is invalid: it leaves no supported overlap.

**Construction limit:** the [resident-cell study](resident-integration.md) replaces the earlier separate mask readers with a stored bilateral C-guide carrying two captured T-feet. A moves the dog; B independently releases the ground pawl. Paired end registers retain the bit, and paired pocketed codebars must capture both ends before writing. The package does not release the complete bank frames, adjacent-bank junction, row decoder or manufacturing process for thousands of metal micro slides. The support-transfer article is the recommended physical experiment. The older short-flag memory article is deferred because it does not qualify this new writer.

### One signed subset stroke

1. Keep every ground pawl seated. Return the lift to its known writing datum. Write the complete new mask, including changed zeros; retain it mechanically. Unknown old memory requires a supported reset, not blind writing.
2. Extend selected captured dogs with frame A while every ground pawl remains engaged. Verify mechanical seating. Unselected dogs remain clear.
3. Move the lift a small take-up distance to establish support and unload the selected ground pawls. Selected pins may move by the take-up amount; unchanged pins must not.
4. Frame B retracts only selected ground pawls. A and B remain positively held. Lift the selected subset through its signed commanded increment. Downward motion uses the opposite dog flank.
5. Stop at an admissible rack phase. Restore selected ground pawls while dogs still hold the pins. Apply a controlled seating movement; accommodate dog backlash without crushing a pin against its grounded pawl.
6. Withdraw selected dogs only after fixed support is seated. Return the empty lift. Rewrite the mask only in this supported state.

If a pawl or engagement frame has not seated, retain the previous supporting path and stop. An undetected partial engagement is an unresolved failure mode. Basic travel limits, guarded motion, a stop/disconnect and anti-drop retention of the powered lift are necessary; elaborate height-camera correction is not part of this proof.

Each rack face must cover **the range of old terrain heights plus engagement margins**. Once captured, the dog and pin translate together, so dog-to-rack position is constant during that pulse. Adding the full terrain range to an independent full lift excursion double-counts this relative motion. The ground and acquisition planes are vertically offset, however: their two rack faces, upper guides, cap and the fixed-frame capture track still require a long complete assembly. The track must cover the actual bank-lift envelope, including signed pulses and handoff excursions. The integrated-cell study records these dimensions; the short-stroke article cannot be scaled by changing only one number.

### Memory principle and the resident writer

The earlier small memory article uses passive lateral flags. In its down position, each flag's foot occupies an OFF or ON pocket: a positive positional register. A row rises out of these pockets to engage its flag lugs with continuous transverse code channels. Only that row reaches the channels; all other rows are physically disengaged. This is the **deferred principle coupon**, not the final resident writer. The resident C-guide instead needs paired upper/lower discrete pockets because its codebars translate along their own length; both ends must be captured before either register releases. See the dimensioned resident study for that distinct construction.

The column channels first match the selected row's **old** bits. Raise the row, move the columns to its **new** bits, then lower the row into its new pockets. Moving a column while another row remains down cannot write that row. Merely locking unselected flags while leaving their followers in contact would create blocked forces, not isolation.

Thus a complete row write includes **old-data positioning, row acquisition/lift, new-data positioning, row lowering/retention, checks and settling**. The quoted 80 ms is an unmeasured allowance for all of them, not 80 ms per sub-action. A misaligned old bit must obstruct acquisition and cause a stop rather than be forced. The small memory coupon demonstrates this geometric question manually; it does not demonstrate 80-ms powered operation or load-bearing actuation.

## Mechanics, tolerances and manufacturing

The captured dog and grounded pawl have different thicknesses intentionally. The final integrated section uses a 3.2-mm-high groove, 2.6-mm captured dog and 1.2-mm ground pawl, leaving 0.6-mm dog backlash and a 2.0-mm nominal ground-pawl insertion window. The manual rack article also has up to 0.25-mm key-slot clearance; its motion allowances differ. These are distinct mechanisms despite sharing nominal groove dimensions. Nominal Boolean replay cannot establish tolerance or force margins.

**Use both load extremes.** In the integrated section, take up 0.4 mm (0.3 backlash plus 0.1 terrain unload), move by the signed increment, then restore the fixed pawl. A freely following pin and a sticky pin can occupy different positions within the dog's clearance. Only after fixed-pawl insertion, lower the dog another 0.7 mm and raise it 0.3 mm to centre it. This common sequence seats both upward and downward moves without relying on gravity. Early downward backlash compensation can put a free pin below its intended latch; merely centring after upward movement can leave a sticky pin unseated. Force-limited seating and tolerance margin remain unqualified. The corrected timing ledger includes these motions.

At 6.35-mm pitch, a 5.8-mm full-width working stem leaves only 0.55 mm for mechanisms. That is insufficient for the proposed pawl/dog withdrawal. Narrow working tails and vertically separated mechanism planes are necessary. Narrowing the entire exposed column is also insufficient: a roughly 2.4-mm residual core can deflect approximately 1.65 mm under a 1 N lateral load at a 40-mm cantilever. Use full-width guided upper bodies and qualify clearance, guide span and cap collision together. No production pin pitch is promoted merely because a small rig fits.

Open racks are inspectable and can be printed without an internal thread. Rigidly backed spring combs are a credible retention process, but their manufacture is not free. Etched thin spring steel and ordinary laser-cut stock are different processes. Avoid thousands of individually bent or hand-fitted pawls. One extra minute of fitting is **68.3 hours** at 4,096 sites. Module assembly, repair access, scrap and guide registration must be included.

A global platen trades travel for force. A bank contains 2,048 sites. An assumed additional 0.03 N guide drag per moving site adds 61.4 N; 0.10 N adds 204.8 N. Printed-pin weight, moving-frame mass, miniatures, acceleration and transmission loss are extra. The small test must measure drag and handoff under modest known loads before choosing a motor. Catalog stall torque is not a continuous rating at 80 mm/s. The low-cost motion-motor entries in the comparison BOM are accounting references, not a qualified global-lift selection.
