# S5-R assembly manifest (DND-60)

**Evidence class: CAD + sourced BOM + calculation.** This is an assembly route over the printed set and the ratified purchased BOM. It is NOT a build report: no part has been printed or measured ([DND-27](https://github.com/sander-van-damme/project-shape-display)).

## Exploded ordering

| # | Stage | Action | Parts consumed |
|---:|---|---|---|
| 1 | cartridge | Print 9 cell cartridges + 6400 rotors/pawls/keepers/detents. Do NOT assemble loose rotors into cells by hand at this stage. | 9 cell_cartridge; 6400 rotor/pawl/keeper/detent_leaf |
| 2 | cell_insert | Insert each rotor into its cell bore from +Z (the bore is 2R+0.20 = 3.20 mm; the rotor 3.00 mm spins free). The pawl and keeper drop into their side chambers; the pawl tip reaches the rack plane. | 6400 rotor, 6400 drive_pawl, 6400 keeper, 6400 detent_leaf |
| 3 | rack | Slide the sourced Ø6 steel rod through the cartridge rack channel; clip one rack strip per row onto the rod (pitch 1.00 / tooth 0.50). The engaged pawl tip bears on a tooth top. | sourced rod x1/row; rack_strip x BANK_ROWS per module |
| 4 | module_frame | Bolt the 3x3 cartridge array onto the lift-frame rails; splice at <= ~150 mm support spacing (DND-43 flatness). | lift_frame_rail; M3 fastener allowance |
| 5 | platen | Bolt the 9 platen modules under the cartridges; fit the guide rods + lead screws through the guide brackets. | platen_module x9; guide_bracket x8; M3 |
| 6 | bank_drive | Fit the 2 bank motors + pinion into the bank drive housing; couple both rod ends (drives the bar from both ends). | bank_drive_housing x1; NEMA17-class x2 |
| 7 | comber | Fit the reset comber + comber cam at each bank group's return end. | reset_comber x3; comber_cam x1 |
| 8 | writer | Fit the 40 writer solenoids into the writer carriage pockets (8 stations x 5); mount the solenoid pocket plate. | writer_carriage x1; solenoid_mount x1; solenoid x40 |
| 9 | wiring | Wire the 2 bank H-bridge channels + 5 writer darlington chips + limit sensors; runs to the controller. | wire/loom allowance |
| 10 | tension | Set pawl pre-load so each engaged tip bears on its rack tooth; verify a full forward+reverse bank pass drops/relatches the field (the DND-59 dropout/re-engage function). | no purchased parts |

## Printed-part count

- **14 distinct printed parts, 25661 pieces total.**

## Purchased fasteners / inserts

| Interface | Fastener | Qty class | Source line |
|---|---|---:|---|
| cartridge -> frame rail | M3x10 + heat-set insert | ~4 per cartridge seam | M2/M3 fastener allowance (BOM) |
| platen module -> frame | M3x12 | 4 per module | M2/M3 allowance (BOM) |
| guide bracket -> frame | M3x8 | 4 per bracket | M2/M3 allowance (BOM) |
| bank housing -> frame | M3x16 | 4 | M2/M3 allowance (BOM) |

## Purchased BOM (ratified, sourced)

Reproduced from `06-experiments/test12_winner_convergence/s5r_bom_ratified.csv` (DND-56). **No part is purchased by this package** ([DND-27](https://github.com/sander-van-damme/project-shape-display)); the listing is the board's sourcing reference.

| Item | Qty | Unit $ (sourced) | Deliverable $ | Evidence |
|---|---:|---:|---:|---|
| Fixed no-channel base (E1-E6: rods, belts, shafts, fasteners, power, loom, PCBs, lift/scanner motors, controller, registers) | 1 | 218.7 | 253.69 | SOURCED-reduced |
| Bank motor (NEMA17-class >=0.30 N.m, 4-wire bipolar) | 2 | 12.39 | 28.74 | ALLOWANCE->SOURCED-LIVE |
| Writer solenoid (5 V push, >=1.2 N design target) | 40 | 2.2 | 102.08 | ALLOWANCE->SOURCED-LIVE |
| Bank H-bridge channel (TB6612FNG dual, 1 IC/motor working) | 2 | 0.7955 | 1.84 | SOURCED (LCSC C88224) |
| Writer switch (ULN2803-class 8-channel darlington) | 5 | 0.3 | 1.74 | ALLOWANCE |
| TOTAL (working scenario, sourced units) |  |  | 388.1 |  |

Source links for each line are in the ratified BOM note column and the DND-54/56/58/59 ADRs under `07-evidence-and-decisions/`.
