# Reproduction and evidence boundaries

This package contains calculations and nominal CAD, not a physically tested machine. The development baseline is current `main` b23ed12, including the DES-007 history and newer owner short-thread observations. Work is isolated on `codex/des008-multiplexed-lift`. On 15 October, `main` was fetched again at `20ebaa1`; its intervening benchmark-file additions/removals have no net tree difference from b23ed12. No newer engineering file was overwritten or merged.

## Reproduce the engineering comparisons

Run from the repository root. Timing and cost use Python's standard library. Independent reproduction with Python 3.12.14 from a different working directory produced byte-identical timing JSON (SHA-256 `f630338b13f4c860aad0b9c4c4a644521947d895683a3eb2adeef4c3a44b9216`), matching independent-audit and cost results, and matching BOM CSV data. The released CSV generator now uses explicit LF line endings for portable Git checks; numeric content is unchanged. Preserve the relative repository directories: the timing model deliberately imports unchanged DES-007 and E-079/E-081/E-082/E-083/E-254/E-257/E-258 evidence rather than replacing historical workloads.

```sh
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/run_timing.py --output work/des008-timing.json
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_timing_independent.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_bounds_independent.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/cost.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/bank_drive.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/mechanics.py --output work/des008-mechanics
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_revised_system.py --output work/des008-revised-system.json
```

`timing-results.json` records assumptions, architecture comparators, separate category ledgers, row-cycle sensitivity and ideal support/movement replay. `check_timing_independent.py` independently rebuilds the stopped-retirement schedule and records slower physically explicit mask scenarios. The review also independently reconstructs the stationary full-scan critical ledger. Agreement verifies arithmetic under assumptions, not mechanisms or actuator rates.

`cost-results.json` and `bom-comparisons.csv` distinguish catalog price anchors, unquoted allowances, material estimates and repeated operations. Neither is a supplier quotation for the complete resident mechanism. `mechanics.py` states beam, flexure and bank-force assumptions explicitly. Its wall equation is geometric; its spring and drive values are engineering bounds rather than measured material ratings.

## CAD and print handoffs

OpenSCAD source resides in `cad/`. Owner folders contain actual ready-to-slice files; exporting source is not an owner prerequisite. The support-transfer article tests the recommended new load-transfer question. The two-row memory article is a deferred principle study whose result would presently have limited effect on the resident design decision. Neither is a full-machine fabrication drawing.

Mesh checks require OpenSCAD, Python `numpy`, `trimesh` and `manifold3d`; figures require `matplotlib`. Tested Python package versions are in `analysis/requirements.txt`. Collision tests distinguish expected contact from forbidden overlap. Nominal manifold meshes and nonintersections do not qualify printed clearances, flexure creep, wear, fast sequencing or elastic neighbor isolation.

The common slicer comparison uses PrusaSlicer 2.7.4, 0.4-mm nozzle, 0.16-mm layers, three walls, solid PLA and the saved `analysis/print-comparison.ini`. Individual handoffs specify brim and orientation. Estimated filament/time are software predictions, not an X1C measurement. Machine-specific G-code is intentionally not distributed.

### Released rack article

Source SHA-256: `0d75dbccb58f0134b698a23b19b4550c2cabab21a4e8aa852bce8a03ef6c3964`. Independent checks pass 240 operation, 648 mixed-drag retirement, 2,048 guide-play and 686 assembly poses. Stored results are `analysis/rack-poses.json`, `rack-mixed.json`, `rack-play.json` and `rack-assembly.json`. Read [the final independent review](review/rack-final-review.md) for the exact limits; individual manual retirement is not a qualified global-frame operation.

```sh
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/export_rack_parts.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/pack_rack_plate.py --parts work/des008-rack/parts --output work/des008-rack --gap 8
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_rack_poses.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_rack_play.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_rack_assembly.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_rack_mixed.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/draw_rack.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/rack_fixture_bounds.py
```

The regenerated plate has 46 watertight bodies with exactly matching sorted triangle coordinates and volume. OpenSCAD face ordering can change binary STL hashes; the released artifact's own hash is recorded in `analysis/rack-plate-manifest.json`. The final slice uses **split-to-objects**, unchanged orientations, supports off and 3-mm brim: **52.12 g / 9 h 20 min 17 s**, with no warning. The combined single-object slice produces a loose-extrusion warning; all distinct oriented part types also sliced independently without warnings. Do not substitute automatic support filling for the documented import method.

### Deferred memory article and resident study

```sh
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_memory.py --output work/des008-memory
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/draw_memory.py --input work/des008-memory
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident.py --output work/des008-resident
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/draw_resident.py --output work/des008-resident
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident_independent.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident_counterexample.py
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident_escape.py
```

Memory revision 3, source `c6bd26a5f29215c4c34e9e8b53471034562b58a0cf65c35863cc9377d86f89fd`, independently regenerates 19 bodies and 83 nominal checks. Its 0.369-mm planar screen is explicitly **not** a general tolerance guarantee. Comparison slice: 11.02 g / 2 h 1 min 24 s, no warnings. Physical priority is deferred; see its owner instructions.

The resident study is not a print release. Its nominal checks must be read alongside the independent admitted-play counterexample and bank-junction collision. The bounded guide variant is a separate exploration, not an implied tolerance pass. The revised system audit reproduces both historical scene anchors and all corrected category ledgers with the final ideal forced-seating sequence; comparison against the independently generated numeric result is exact, apart from the deliberately updated source path in provenance.

## Export the report

```sh
python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/make_report.py --output work/des008-report.pdf
```

This requires `reportlab`; appending generated PDF drawings with `--append-pdf` also requires `PyMuPDF`. Markdown and source remain authoritative. The portable source archive includes the unchanged historical calculation dependencies needed to rerun the comparisons.

## Qualification still required

No new physical validation was performed in this investigation. In particular, positive loaded support transfer, forced downward travel, unchanged-neighbor isolation, matrix acquisition, complete row-cycle time, guide drag, spring fatigue, assembled module yield and the playable wall/base interface remain unknown. Record failures as well as successes on the supplied result forms. An attractive CAD assembly or successful single article is not permission to infer a qualified 4,096-site array.


## Repository checks

A clean archive of the starting commit fails `./repo check` only on five pre-existing oversized atomic documents: E-266, E-283, E-286, E-288 and E-293. These historical files are preserved. The final staged delivery snapshot was checked separately and reports exactly those same five errors, with no new structure/reference failure. Scratch investigation files are excluded from that snapshot. `git diff --cached --check` passes; the released analysis scripts compile. Final formatting cleanup changed no calculation values, and the revised-system provenance hash was regenerated.
