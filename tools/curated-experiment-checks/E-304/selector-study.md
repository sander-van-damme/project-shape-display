# Full-length selectors: structure and manufacture

The design uses one **continuous control member per complete row and per complete column**. Printed sections may join on continuous reinforcement, and stationary shoes may support them. None of these joints or supports has its own motor, address or selection state.

## First resolve the boundary conditions

A vertically lifted beam cannot receive fixed intermediate support in that same vertical direction without an additional following mechanism. Quoting a short supported span for such a beam would be false. E-304 instead slides each selector **along its length by 2.54 mm**. Repeated cam tracks convert this movement to vertical follower motion. Stationary shoes now carry transverse contact load while permitting longitudinal travel. This makes short support spacing mechanically meaningful.

The field reference is 80×80 at 5.08 mm: **406.4 mm overall pitch allocation**, 401.32 mm between extreme pin centers. The structural model uses 406.4 mm, conservatively. The new stack is taller because force distribution and journals have their own space. The bench CAD reaches about 79 mm at the neutral pin top versus about 57 mm in E-300's two-pin assembly. This is roughly 22 mm additional bench height, not an established complete-display depth. No project height limit rules it out; handling, access and an eventual 40-mm pin travel still need a complete machine layout.

## Comparison mechanics

`I=∫z²dA`, `δ_point=PL³/(48EI)`, and `δ_uniform=5qL⁴/(384EI)` are used for simply supported spans. The point-load case places one obstruction at midspan. The uniform case uses 0.3–1.8 N/cell as a plausible selection-force range, **not measured load**; the comparison CSV normalizes to 1 N/cell and a separate 3 N obstruction. Adding both is conservative if the obstructed cell already belongs to the distributed load. End-fixed joints would be stiffer but are not assumed.

Closed thin-wall torsion uses `J≈4Am²/Σ(l/t)`; open sections use `J≈Σbt³/3`. Actual tiny sections are not very thin, and FDM shear modulus is uncertain, so these are comparative screening values. Axial shortening for a uniformly loaded selector pulled from one end is `Δ≈Ftotal L/(2EA)`; a single end obstruction uses `FL/EA`. Buckling uses `Pcr=π²EIweak/Lsupport²`, with no claimed postbuckling capacity. For a tension-driven ON stroke buckling is irrelevant to that stroke, but can matter when pushing the return or a jammed bar.

[All section results](analysis/results/selector-sections.csv), [load/force sweep](analysis/results/selector-forces.csv), [support-spacing plot](analysis/results/support-spacing.svg). PLA screening values: E=2 GPa, G=0.74 GPa, density 1.24 g/cm³; modulus sensitivities and creep are not material certificates.

| Structure | Bending / torsion / manufacturing result |
|---|---|
| Flat 4.6×1.6-mm strip | At 25.4-mm support spacing, about 0.340 mm distributed deflection plus 0.326 mm for the 3 N point case. Too flexible for the selected approximately 0.15-mm deformation allowance even on short spans. |
| Solid 4.6×10-mm rectangle | About 0.0014 +0.0013 mm at 25.4 mm;23.2 g per 406.4-mm member before cams. Stiff, simple, but wasteful and prone to long-print warp. |
| Closed 4.6×10×0.8-mm box | About 0.0023 +0.0022 mm;10.5 g before cams. Better material use and torsion than an open rib or truss. Can carry guide flats without opening the main load-bearing section at every pin. |
| I section | Similar strong-axis bending efficiency to the box, lower mass, but much weaker torsion. Eccentric cam/follower forces need anti-roll shoes. |
| T section | Unsymmetric centroid and shear center; weaker lateral restraint, twist under eccentric load. Useful as a guided rib, not an unsupported replacement for the box. |
| Warren / triangular web | Chords separated in height provide bending stiffness; triangulation transfers shear. Chord-only EI is an **upper bound** because diagonals stretch and joints rotate. Compression diagonals need buckling checks; thin FDM nodes concentrate stress. A plane truss is torsionally weak. |
| Pratt | For one load direction, long diagonals can mainly carry tension and short verticals compression. Selection/withdrawal can reverse forces, so the favorable load sign is not guaranteed. More nodes and a weaker reverse-load case remove much of its advantage at this scale. |
| Ribbed/lattice box | Keep closed outer skins and add ribs at cam-force entry/support points. A sparse internal lattice helps local crushing; it adds little global EI unless it transfers shear between separated chords. Decorative triangles do not create torsional closure. |
| Two insertedØ2-mm CF rods | Put rods near opposite vertical extremes and transfer shear through the printed core. Merely pushing loose rods into bores does **not** earn the parallel-axis composite-EI term. The model gives both unbonded/sliding and full-composite bounds. |
| One continuous stock rod + printed attachments | Feasible when shoes carry alignment and anti-roll. A round rod alone does not set attachment angle or cell pitch. It trades less printing for many bonded/clamped attachments and a joint-slip tolerance stack. |

The selected printed core is a box with **twoØ2.2-mm channels for nominalØ2-mm rods**, centered at z 2.2 and 8.1 mm. A 0.8-mm internal vertical web supports the upper rod sleeve during printing and carries local shear. Its extra web, channel sleeves and cam rails make it heavier than the idealized bare box table; the actual CAD volumes are in the mesh manifest. The table intentionally does not count a cam as a full unnotched chord. The main lower box is uncut by the repeating follower openings. A separate shared upper cam cap allows followers to be placed without threading every small part through a closed track. This cap is a repeated **row component**, not another per-cell part.

A local cam lip is a short cantilever, not the whole selector. With 0.6-mm projection, about 0.7-mm thickness and 0.8-mm loaded width, 0.75 N on one lip gives order 0.002-mm elastic movement and 7 MPa nominal bending stress atE2 GPa. Corner stress, layer adhesion and contact crushing are omitted. The thin lip and the cap's withdrawal load therefore remain physical inspection points even when the main beam is stiff.

## Stock-material comparison

Commercial dimensions/prices and exact source links are in [sources.md](sources.md). Mechanical properties not stated by a source are explicit screening assumptions.

| Stock |406.4-mm nominal mass | Practical implication |
|---|---:|---|
| CFØ2 rod, density 1.5 |1.92 g | Very light; at 25.4-mm supports, low-end 20-GPa bending modulus gives roughly 0.068 +0.065 mm in the normalized cases. One tiny rod is not a 400-mm bridge. |
| CFØ3 rod |4.31 g | More efficient as a mostly purchased member; about 0.0135 +0.0129 mm at 25.4 mm. Attachment angle still needs shoes. |
| CFØ3/2 tube |2.39 g | Better bending per mass than a 2-mm solid; thin wall is easier to crush at a clamp. |
| GlassØ3 rod, assumedE30 GPa |5.75 g | Cheap, insulating and forgiving; stiffness must be measured for the bought variant. |
| SteelØ2 rod |10.0 g | Cheap and stiff;≈0.0068 +0.0065 mm at 25.4 mm. Higher moving mass but much less axial shortening. |
| SteelØ3 rod |22.6 g | Mechanically simplest stiff stock option. Less printing with attached cam strips; heavier than CF but inexpensive. |
| AluminiumØ3/2.1 tube |3.96 g | Useful compromise;≈0.0051 +0.0049 mm at 25.4 mm. Avoid point set-screws on the thin wall. |

**Do not use generic aerospace carbon modulus.** The linked manufacturer's TDS lists tensile 28–40, flexural 20–30 and compressive 10–20 GPa. Calculations use the lower 20-GPa bending value and 28-GPa tensile value for the reinforced member's pull stroke. A pushed CF member can shorten substantially more. The pure-stock CSV's EA uses its listed screening E; use the TDS's appropriate tensile/compressive modulus for an actual actuator direction.

## Recommended construction

Use the **guided closed printed cam beam with continuous inserted reinforcement**, assembled from four approximately 101.6-mm print sections along each full row. Two 2-mm steel rods are the conservative low-cost default at the calculated worst row force. Two 2-mm CF rods are the lighter alternative, conditional on measured axial stiffness and joint slip. The same printed channels accept either material. Use paired guide shoes at **25.4-mm intervals initially**. Their placement and attachment to the stationary guide structure are part of the load path. Do not infer stiffness from the 4-mm bore alone or leave a long span unsupported.

Pull the loaded ON stroke from the far end so the CF primarily carries tensile load. Local printed sections must transfer axial cam load into the stock: use prepared, bonded sleeves or positive end capture plus a verified continuous load-transfer path. For a roughly 100 N worst-case row force, each of two rods carries order 50 N. A25-mm bond length on a 2-mm rod has nominal average shear about 0.32 MPa, but peel, surface preparation, adhesive creep and print-layer failure can dominate. Adhesive is not assigned a guaranteed strength. Do not cut screw threads into carbon or use a crushing point clamp. Use broad split collars/end shoes; leave the far support free to accommodate length change.

A long printed shell can be thermally incompatible with a bonded rod. Using illustrativeα values PLA70, aluminium 23, steel 12 and axial CF0–3 µm/(m K), a 20 K change over 406.4 mm creates about 0.54–0.57 mm PLA/CF mismatch. These α values are assumptions. Short printed attachments with controlled gaps reduce accumulated thermal stress; tightly bonding the entire length gives better composite stiffness but more thermal/creep risk. The short-support design deliberately does not require the ideal full-composite EI to succeed.

Check supplied rod straightness on a flat reference and dry-fit all shoes. The seller's OD tolerance is not a straightness specification. Shoes should constrain roll/lateral position without forcing a bowed rod into high friction. Rod-to-sleeve clearance, joints, bond slip and shoe clearance belong in the same measured stroke budget. A single rod with tiny individual clips needs 6,400 angular/pitch placements; longer printed multi-cell cam strips reduce this assembly burden.

Column roofs are unloaded when changed in the normal sequence (rows returned first). Their split-rail section must still resist the transverse load of blocked half-selected followers while stationary. At 25.4-mm supports, two approximately 1.1×6.5-mm rails give an estimated 0.02–0.04-mm combined normalized distributed/point deformation at E=2 GPa (roughly twice that at E=1 GPa), before guide flexibility. They do not need the same tensile reinforcement as the loaded row pull. Attempting a fully loaded column return across 80 cells is a different force case and is not credited as a qualified low-force operation.

## Deformation allowance and actuator force

The cam has a **0.30-mm dwell half-width**, and the nominal local spring compression after contact is 0.8 mm. An initial 0.15-mm budget for beam movement plus connection error consumes half the dwell margin and changes nominal spring force by about 0.21 N. This is a functional tenth-of-a-millimeter requirement, not a micrometer positioning demand. It excludes measured rod bow and frame misalignment until those are characterized; all cannot each consume the whole budget.

For cam slope `m=1.4/(2.54−0.6)=0.722` and assumedμ=0.2, input-force ratio is `(m+μ)/(1−μm)≈1.078`, plus shoe friction. At 1.102 N/cell, 80 loaded cells require about **113 N** during the ramp. At 1.79 N/cell the same assumptions give about **183 N**. The 0.3–1.79 N and μ0.10–0.35 sweep is supplied. Dwells remove the ideal geometric holding force; they do not remove friction, tolerance or motor retention requirements. A 5:1 edge mechanism would trade about 12.7 mm actuator travel for lower force, before its losses. It is an actuator interface allowance, not a designed motor bank.

A bare printed box can shorten about 0.49 mm under the normalized 100 N distributed axial load over 406.4 mm. Two properly loaded 2-mm CF rods reduce the tensile estimate to about 0.093 mm; bond slip could erase that gain. This axial result is a stronger reason for reinforcement than the already small transverse deflection between shoes. Steel is an economical fallback where moving mass is acceptable.

## One structural measurement, not another print campaign

The same plate includes a 100-mm representative beam and two supports. Compare empty channels with inserted rods on 50/75-mm support spans using the **same** beam, same load and orientation. Record rod material/diameter, measured span, load and midspan movement. Loose rods measure the unbonded case. They cannot validate full-composite action; if the owner elects to bond the same specimen, record that separately. Do not infer 406-mm performance from a short beam without preserving its support/connection model.

The final bed-supported follower geometry (0.40-mm thickness, 3.6-mm depth, 0.9-mm vertical leg pitch) predicts 1.102 N selected and 1.79 N half-selected at E=2 GPa. The final force CSV includes these values: about 113 and 183 N per 80-cell row at μ=.20. Scale the distributed deflection linearly to 1.79 N/cell; the 3-N single obstruction remains a separate case.

The reproducible Warren-web screen uses 5.08-mm panels, 8.4-mm chord separation and a 2×0.8-mm diagonal. Its effective shear rigidity is `GA≈EA_diagonal a h²/l³`. Over 25.4 mm, web shear alone adds about 0.013 mm under the normalized distributed load and 0.016 mm under the 3-N point load, **on top of** the chord-only bending entry. The combined maximum diagonal force is about 4.7 N versus roughly 17.5 N ideal pinned Euler buckling capacity. Thin-joint rotation, printed defects and reversed load reduce that margin. This is why a space-filling triangle pattern is not automatically superior to a closed box at this pitch. Exact values are in `analysis/results/truss-web.json`.

At the final 183-N half-selection row case, the lower-bound CF tensile model predicts about 0.17-mm distributed axial shortening, slightly above the initial 0.15-mm budget before joint error. The corresponding two 2-mm steel rods in the same box predict about 0.029 mm. Steel adds roughly 16 g per row versus the carbon rods (about 1.3 kg across 80 rows), but this extra inertia is negligible beside the hundred-newton cam force. Eighty 1-m steel rods cost about€80 including listed VAT versus€156 ex VAT for the carbon tier. Thus **steel is the simplest conservative reinforcement for this force envelope**; carbon remains attractive if its measured modulus/joints and allowed stroke error justify the weight saving. No stock is bought or separately prototyped here.
