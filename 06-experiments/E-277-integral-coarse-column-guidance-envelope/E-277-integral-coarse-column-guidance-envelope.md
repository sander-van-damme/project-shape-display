---
status: complete
builds-on: [E-276, E-261, E-260]
---

# Integral coarse columns trade cap yaw for guide lean, seams and stock

**A wider integral square column does not by itself make E-276's close-packed tops safe.** It removes the narrow-stem/wide-cap yaw amplification, but two guides still permit neighboring columns to lean together above their support. Retain a reduced-width integral column only as a conditional geometry control: at 12.7-mm pitch, 2.4-mm nominal seams and 80-mm guide separation, the bounded rigid model leaves .459 mm separation. This uses 136-mm stock for 50-mm travel and covers only 65.8% of the nominal plane. It is not a selected playable surface or a qualified screw assembly.

Reproduce `python3 tools/curated-experiment-checks/E-277/guidance.py --check`; omit the flag for the finite comparison. Evidence: **analytical bounds and exact rigid-strip geometry**, self-reviewed. No new material priors, measured loads, simulation of friction, CAD fit, print or purchase. The inherited 4.4-mm-stem/large-top construction remains parked. No tightening of thousands of fits or added resident latch is assumed.

## Changed construction and full-travel bound

Compare a straight square hollow column whose top and guided exterior have the **same width**, with E-276's wider cap on a narrow stem. The internal bottom thread, resident screw, thrust bed and opaque support frame retain their functions. The writer supplies torque; it never takes over the terrain load. Two shared square guide slabs supply lateral/anti-rotation reactions. A wider tube needs an integral bottom web/block connecting the original thread to its outside walls, and an integral roof. These must be manufactured and carry load; the old thin tube's material allowance cannot simply transfer.

Use E-261's two 2-mm guide slabs, center separation `b`, travel `S`, and end reserves. Projected stock remains `P=S+b+6`; maximum top-center height above the upper guide face is `h=S+2`. The extreme guide faces are `B=b+2` apart. Guides and columns are rigid and straight in this screen. Elastic bow, twist along the column, actual thread restraint, roof bending, contact forces and wear remain outside it.

Let nominal column width be `w=p−s` (pitch minus seam), nominal guide opening `w+c`, total-width error bound `±e` on each separately, and guide-center placement bound `±r` per aperture at each layer. These are **competing bounds, not print distributions**. The broad opening is `G=w+c+e`, slender column is `w_min=w−e`; minimum aligned fit clearance is `c−2e`. A positive value does not prove that both guides and the resident screw can align without binding.

A straight square prism contains an inscribed circular cylinder, so its horizontal cross-section width in either guide coordinate is at least `w_min`, including yaw/tilt. Guide confinement therefore bounds coordinate slope by `(G−w_min+2r)/B`. Extrapolating the prism above the upper guide gives a conservative combined occupied width for opposing neighbors:

`W = G + 2r + 2h(G−w_min+2r)/B`, hence `separation >= p−W`.

Positive separation is sufficient in this rigid model for independently moving neighbors at **all smaller heights**, including different heights. A negative lower bound alone is not proof of collision. Independently solve the exact yaw-zero strip relation `B tan(theta)+w_min/cos(theta)=G+2r`; realize opposite guide contacts and check finite ends. This supplies the nominal failure witness below. The screw may constrain the admitted lean, but then its lateral reaction/stiffness must be established rather than credited invisibly.

Errors can be correlated. A common rigid translation of both guide planes cancels between neighbors. A common inter-plane skew also cancels at equal heights, but at unequal heights leaves `(h2−h1)*skew/B`; a .2-mm skew across42 mm and50-mm height difference gives .238 mm relative displacement. Independent local error or opposite module-edge registration can realize the adverse bound. No independent-identically-distributed yield is claimed. Enlarged apertures can also consume the separating web; check that before treating a mathematical column position as a manufacturable grid.

## Discriminating results

The first control uses .4-mm seams and the inherited **.24-mm nominal total clearance**, without manufacturing error. Broad columns constrain yaw more strongly than the small stem, but the following guide-only separation bounds remain negative:

| Travel / guide span, mm | Stock, mm | Separation bound, mm |
|---|---:|---:|
|40 /40|86|−.320|
|50 /40|96|−.434|
|40 /80|126|−.086|
|50 /80|136|−.144|

At half-square pitch/S50/b40, the exact strip tilts only **.327°**. One millimetre below both finite top faces, opposing columns overlap by **more than .42 mm**, with both guides satisfied. This is a geometric witness under granted guide freedom, not a physical jam measurement. The nominal grid web is only .16 mm. No stiffness/printability claim is made for it.

With the same seam, clearance and errors, widening the whole column does **not** improve the conservative separation: width cancels. The absolute required seam is the same at5.08,6.35 and12.7-mm pitch; coarser pitch loses less surface area to that seam.

For S50 and **c=.5, e=.1, r=.1 mm**, minimum aligned fit is .3 mm. These bounds are deliberately looser than nominal perfect geometry; they are not qualified X1C tolerances. At b40 the required seam for zero separation is3.029 mm; at b80 it is1.941 mm. The original .4-mm seam gives negative grid web (−.4 mm), so the shared aperture layer itself fails before a complete mechanism can be claimed. With c=.8/e=.2/r=.2, b80 needs3.429-mm seams even for zero separation. Retaining c=.24 while assigning e=.2 instead fails fit (−.16 mm); reducing clearance is not a free rescue.

A finite grammar compares b40/60/80 and seams .4/.8/1.2/1.6/2.0/2.4/3.2 mm at the first bounded scenario. Six of21 combinations have nonnegative rigid separation. Three useful controls are:

| Half-square seam / b, mm | Separation bound | Stock | Nominal plane coverage | Tube-only volume at .8-mm wall |
|---|---:|---:|---:|---:|
|3.2 /40|.171 mm|96 mm|56.0%|2.737 L|
|2.4 /60|.090 mm|116 mm|65.8%|3.611 L|
|2.4 /80|.459 mm|136 mm|65.8%|4.234 L|

The .090-mm result has little unallocated margin; it is not a selected tolerance. A2.0-mm seam/b80 option leaves only .059 mm despite70.98% coverage. **Keep the2.4/b80 construction as the clearer geometric comparator**, not a product winner. The same2.4-mm seam at quarter/fine pitch retains38.7/27.8% coverage, and at fine pitch the resulting2.68-mm column is narrower than the inherited3.2-mm screw: that is not a valid threaded embodiment. Deleting caps while retaining the4.4-mm stem covers only12% at half-square pitch. Reduced tops do not preserve a continuous table surface by assertion.

Even at nominal equal height,2.4-mm gaps may affect miniature bases, props, dice, fingers and appearance. E-276's footprint counts granted filled cells, so they do not establish support over these gaps. A25.4-mm base can bridge multiple columns, but this is not a stability or edge-placement test. Wall thickness changes from12.3 to10.3 mm; the coarse opening/connectivity trade remains. No new subjective preference is inferred.

## Manufacture, load and whole-machine consequence

The selected **comparison geometry** has1024 columns/screws/threads/roofs/bottom-web duties and2048 guide apertures. A32-cell row retains32 pairs/64 apertures; an8×8 region has64/128. Two guide layers retain62 row ribs plus their frame joints. Quarter/fine references remain4096/6400 pairs and8192/12800 apertures. No private moving guide, top hinge, anti-backlash nut or added latch appears. Individual replacement through openable shared layers remains an architectural requirement; physical extraction of a136-mm column, bed access and re-registration are unconstructed.

At width10.3,136-mm stock, .8-mm wall, the1,024 tubes alone occupy4.234 L. A concrete material control adds a10-mm solid bottom block with a cylindrical3.2..1.4-mm bore bound and a2-mm integral roof: **5.081–5.148 L total column material**, excluding screws, guides, scrap and print supports. This volume bound does not construct a mating thread. At .44-mm walls, tube-only volume falls to2.417 L, but broad-wall stiffness and roof bridging are unqualified; do not select thin walls from volume alone. Integral ribs connecting a smaller nut boss could reduce material but require a different structural construction, not a granted saving.

Manufacturing comparison:

- Monolithic FDM avoids assembly joints but adds long broad walls, an internal roof and bottom thread. Horizontal printing exposes cavity/roof/support-removal problems; upright printing revives the owner's long-part stability objection. Temporary batch connections must avoid the entire sliding exterior. No support plan, yield or ready STL is supplied.
- A molded/cast monolithic shell requires a withdrawable internal cavity core and separate thread-forming/unscrewing provision. Tool access, shrinkage, straightness and cycle time are unqualified;1024 parts can amortize tooling, but no price is assigned.
- Cut square tube with separately fitted threaded bottom and cap simplifies stock production, but adds2048 joining operations and2048 joint-quality duties. At an illustrative10 s/join this alone adds5.69 h; at30 s it adds17.07 h before the inherited handling/calibration. It is not automatically the simpler maker process.

Broader/slower columns do not inherit a motor rating: additional moving mass, screw side restraint, guide drag, roof load and stiffness change the drive problem. No new load or850-rpm pass follows. E-276's four-direct-spindle **conditional** S40/S50 local waits26.84/31.07 s, scene201.24/222.88 s, neutral271.15/331.62 s and dense391.62/452.09 s remain a granted-actuation comparison only. S40/neutral20 and S50/neutral30 retain real downward headroom and paid preparation. The8-output control remains18.46/20.81 s for local reveals, with a larger shared-head cost.

E-276's dated/unquoted four-output bought allocation$798–1768 (versus$500 reference, $1000 possible finished-value discussion and$1000–1500 research envelope) is **not a revised BOM** for these enlarged columns. Its printing/support/material allowance and maker10.94–23.69 h cannot be silently transferred. Another minute fitting each pair adds17.1 h. No sourced current quote, purchase authority or improved whole-session speed is claimed.

## Decision and limits

Stop near-continuous integral-column detailing: broad sections remove the old cap-yaw amplifier but leave a demonstrated nominal lean witness and a thin/absent guide web. Do not add tiny per-cell guides or tighten every fit. The meaningful escape is an explicit compromise among **larger surface seams, longer shared guidance, or quantified lateral support from the screw**. The2.4-mm-seam/136-mm-stock control earns only a bounded rigid-envelope result; actual screw alignment, flex, batch manufacture, roof load, readback and recovery remain unresolved.

The next discriminating independent work is to construct the integral threaded-bottom/roof load path and compare its batch manufacture/material burden with a joined-stock control, before head refinement or another optional print. If neither preserves simple manufacture, park this coarse embodiment instead of optimizing microscopic clearances. A player-facing seam choice should wait for a mechanically credible surface comparison.

Checks:432 exact-strip/guide-contact reconstructions across pitch, travel, span and competing error bounds; finite-end witness; zero-clearance limit; fit failure; increasing-span monotonicity; pitch cancellation; common translation/skew; volume arithmetic and21-case finite grammar. These verify the model, not hardware. No optical decoder or loaded-neighbor qualification is inherited.
