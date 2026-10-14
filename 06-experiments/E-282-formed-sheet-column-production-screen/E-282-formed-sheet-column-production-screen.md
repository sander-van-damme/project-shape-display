---
status: complete
builds-on: [E-277, E-279, E-280, E-278]
---

# Formed-sheet bodies: deposition escape, repeated joining burden

**Retain batch-formed bodies as a conditional process alternative; do not develop individual hand-folded columns or a protruding lap seam.** Replacing the long printed channel can remove384.66 comparison print-hours/1024 sites. It does not remove the149-hour nut or61-hour bare-screw contribution. Hand folding exchanges printer occupancy for8192 manual operations and3072 joins. A viable continuation must demonstrate shared forming/cutting and end joining, not tune another local seam.

Evidence: sourced process capabilities/cautions, analytical section and resource bounds, finite blank packing. Self-review; no formed part, CAD assembly, process qualification, supplier quote or measured fit. Run `python3 tools/curated-experiment-checks/E-282/forming.py`; checks run before JSON output. Generated output belongs in scratch.

## Changed construction and complete machine

Keep E-277's12.7-mm/32² control:10.3-mm square exterior,136-mm overall body,80-mm guide span,10-mm intact nut,2-mm cap and124-mm intervening shell. Substitute a nominal.5-mm formed PP shell for the printed U-channel. Retain the90° included,lead3 printed pair as a manufacturing comparator,not a selected thread. Square-shell inner width9.3 mm; a3-mm inward seam lap with.2032-mm bondline leaves a local8.5968-mm clear width. This is a section allowance,not a constructed fold transition.

Terrain cap→shell walls→nut butt seat→thread→screw collar/bed remains the intended compression path. The cap and nut joints also owe tension under eccentric loading, reverse motion and torque; a butt seat is not capture. No free adhesive strength, finger latch or thin folded cap is assumed. The2-mm cap stays a separate component because replacing it by.5-mm sheet changes its bending behavior. Two shared guide planes provide antirotation; the writer only supplies torque. Passive holding, moving power-loss arrest, end stops, docking and fresh actual-height readback remain unqualified. Unchanged neighbors remain on their own resident pairs. Openable guides/bed and136-mm extraction must permit individual replacement; no bonded whole-bank disposal.

Per cell: shell,cap,nut,screw; three joins (longitudinal seam plus two ends),one threaded pair,two guide apertures,two screw journal contacts,collar seat and socket. A32-cell row has128 pieces/96 joins/64 guide apertures; an8×8 region256/192/128; board4096/3072/2048. The four independent spindle control and shared carriage remain unchanged. Continuous stock forming moves the seam into shared tooling but does not erase its1024 functional failure sites or2048 end joins. Drawing/casting/extrusion could instead supply seamless stock; E-278's retail price is a sampled control,not a universal price floor.

## Section and guide discriminator

Ideal square median-line development is `4(w−t)+lap=42.2 mm`;124-mm blanks assume sharp corners without calibrated bend allowance or springback. The ideal closed-wall torsion surrogate is `J=(w−t)^3*t=470.596 mm⁴`; the same four walls with an unjoined longitudinal slit give `J≈4(w−t)t³/3=1.633 mm⁴`. These inherit E-277's thin-wall approximations. The ratio is288,not evidence of an actual weld or polymer modulus. At assumedG200 MPa,1 Nmm over54 mm gives.0329° versus9.47°; the latter warns against linear small-deformation interpretation. An overlapping but unbonded edge must not receive closed-section stiffness. Ideal5-Nmm shear flow across a3-mm lap implies.00868 MPa average shear,excluding peel,guide force,ends,creep and buckling; this is not a joint rating.

The unchanged E-277 width/center error scenarios give.45854-mm sufficient rigid neighbor separation. Enlarging apertures for a seam protrusion `b` while retaining the original minimum width reduces that bound by `b*(1+104/82)`. It reaches zero at.20215 mm. A.5-mm outward lap gives−.67561 mm; lap plus.2032-mm bondline gives−1.13653 mm. Negative bounds do **not** prove collision. They remove the existing sufficient certificate; tightening guides or pursuing microscopic residue is not justified. Prefer an inward/flush seam or qualified seamless stock. Shell bow,corner radius,crease memory,elastic wall splay and guide wear remain outside this rigid bound. A smaller tube is not a free cure: it changes minimum width,guide play and cap support.

## Sourced process limits

Checked2026-10-14:

- [Primex](https://www.primexplastics.co.uk/polypropylene) identifies modified PP sheet grades suitable for folding,welding and machining. This supports investigating the process family,not our.5-mm stock,10.3-mm section,bend radius,guide tolerance or a production price.
- [3M DP8005](https://www.3m.com/3M/en_US/p/d/b5005321032/) is an industrial adhesive example for many PP grades. Its8-mil spacers correspond to.2032 mm; stated working/handling/full-cure times are3 min/3 h/24 h at22°C. It is not a selected home-use adhesive or a qualified PP-to-PLA joint. Heat welding avoids adhesive cure but still owes access,fixture pressure,cooling,distortion and seam-strength evidence.

These sources establish neither an automatic folding line nor safe loaded speed. Different sheet grade/thickness,tool bias and thermal history need their own evidence.

## Whole-pair resource ledger

Finite nonoverlapping packing on assumed1000×500-mm sheets,10-mm borders and2-mm blank gaps fits70 blanks (7×10); the rotated regular layout fits66. This is not a globally optimized nesting claim. No calibrated kerf,bend allowance or scrap distribution. Yield1 is deliberately favorable.

|Repeated coarse bodies|Sheet area bought m²|Net shell L|Seam m /joins|Channel print h removed|Nut+bare shank print h retained|Manual maker h including base/setup|
|---:|---:|---:|---:|---:|---:|---:|
|1024|7.5|2.679|126.98 /3072|384.66|209.64|26.32–69.82|
|4096|29.5|10.717|507.90 /12288|1538.65|838.54|67.28–189.29|
|6400|46.0|16.745|793.60 /19200|2404.15|1310.22|98.00–278.89|

4096/6400 rows are replication diagnostics:10.3-mm bodies **do not fit**6.35/5.08-mm grids. Actual sliced inputs are E-277/E-279's4057/1571/640 seconds per three channels/nuts/bare shanks. These are comparison-profile repetitions,not X1C production forecasts. Caps,finished screw ends,frame and rejects remain unpaid. An explicitly assumed60/180-s cap deposition adds17.07/51.20 h at1024,leaving226.70/260.84 print-hours before those exclusions; neither is a slice result. Even a free cap cannot remove the209.64-hour residual. Sheet forming and printing can run concurrently; do not sum them into a promised calendar duration.

Manual scenario: eight5–15-s operations per body (handle blank,three corner folds,close seam,join cap,join nut,gauge),plus4–12 h setup and E-276's actual executable four-output installation allocation. Gang cutting,consumable application,fixture fabrication,unloading,cure,cleaning,failed checks,scrap and commissioning remain additional. Retained screw run-on is already in the inherited base; do not add it twice. At1024 the favorable32-hour budget leaves59.97 s/body for **all** additional body work after base/setup;4096 leaves8.99 s and6400 only2.875 s. The adverse base/setup already exceeds32 h. These are tipping points,not measured production rates or hard product gates.

Adhesive seam witness: assume60 s handling per body and parts constrained until3-hour handling strength. Sixteen reusable seats need64 fill/cure batches and209.07 station-hours;64/256/1024 seats give65.07/29.07/20.07 h. This batch model does not credit staggered release; continuous output at one/minute needs at least180 curing positions. It excludes end-joint fixtures and full cure,which may occur elsewhere. A few clamps do not imply production-scale joining throughput. No adhesive process is selected.

Sheet$5–20/m² and tools$100–500 are **allocation bounds,not current offers**. At1024 they add$137.50–650 to E-276's four-output bought allocation,giving$935.18–2418.23 before adhesives,cutting services,cap/nut/screw filament,shipping,scrap and unpaid fixtures. Printed material was outside the bought baseline,so no invented hardware saving is subtracted. No ~$500/~$1000 finished-price or$1000–1500 demonstrator pass;no purchase.

Sheet thickness/crease placement can share a whole-sheet bias (up to70 blanks here); a forming-tool or seam-jig bias affects successive sheets. Warpage and local weld defects add individual variation. No independence or probability is assumed. At80% usable fraction,1024 good shells require at least1280 attempts/19 sheets,not15; the failed parts still consume labor and process capacity. Actual yield and correlated repair costs remain unknown.

## Product consequence and next discriminating evidence

Same lead and intended stroke preserve E-276's **conditional**850-rpm four-output S40/S50 local26.84/31.07 s,scene~201/223 s,paidN20/N30 neutral271/332 s and dense392/452 s. Forming earns no RPM,docking,retention or optical speed improvement. The~30-s gameplay benchmark,~40-mm reference travel,~6400 cells and~$500 bought reference stay visible;coarse12.7-mm pitch/65.8% top coverage and premium costs remain unresolved play choices. Initial neutral is physical preparation,not a software offset.

**Decision:** the dominant-body manufacturing escape is worth retaining,but individual hand folding and external seam buildup are poor next investments. Proceed only with a concrete shared forming/cut-to-length and end-joining route whose total touches,fixture occupancy and guide envelope beat these bounds. Keep the intact thread unsplit and do not start a seam/clearance sweep. No additional owner print; E-281 remains the separate optional fit test. Finite packing,material conservation,torsion identities,guide-bound root,resource scaling and cure-inventory checks passed; this does not qualify hardware.
