---
status: complete
builds-on: [E-255, E-256, E-260, E-261, E-262]
---

# Supported S40 screw calibration article

**Print offer retired; supported CAD remains an unqualified comparator.** Sander
declined the unsupported slender-part layout. The [retirement note](../owner-print-tests/supported-s40/test.md)
replaces the print job; no replacement is READY. Nominal mating, captured thrust,
two openable guides, removable second radial land and travel stops passed geometry
checks, not actual-process fit, stiffness, holding, speed or array qualification.
Evidence: source inspection, CAD/mesh checks, calculations and owner feedback;
self-reviewed, with no new measurements or purchases. E-256's positive manual
holding report and near-extension break remain separate physical observations.

## Reconstructed mate and supported load path

Reinspected trial3 actuator and trial5 actuator/calibration/frame at41484f9699.
[BOSL2 at136e636](https://github.com/BelfrySCAD/BOSL2/blob/136e6367e65d52196a3ea51d03156f8b622c60fc/threading.scad)
confirms E-255: internal mode adds twice `$slop` radially and transforms phase;
trial5 minimum cutter radius1.65 exceeds male crest1.60. The calibration screw
has different dimensions. This is not the known successful print dependency.

The specimen instead subtracts the **same external trapezoidal generator**:
pitch3, depth.9, included angle30°, one right-handed start, no bevel/blunt start.
Male OD3.2/cutter OD3.5: explicit radial relief.15, root radius.7/cutter minimum.85,
maximum1.75, radial engagement.75. Nut width4.4 leaves minimum wall.45; tube wall.44.
These allocations alter friction; owner holding evidence does not transfer.
The periodic cutter extends−3..57 through the10-mm nut into the cavity; extending
its boundaries removes a coplanar CGAL seam, not a tuned physical fit.
Signed mesh mating requires `theta = -360*(q-screw_axial_shift)/3` degrees.

Coordinates below are relative to nominal thread start, in millimetres:

| Duty / feature | CAD allocation |
|---|---|
| Loaded support | Tray→pin→nut→screw→lower handwheel face→frame foot→table; reverse axial force reaches fixed shelf through upper wheel face. |
| Guidance | Pin torque/side force reaches common rails through z44..46 and84..86 guides; screw primary radial land z−4..−2; removable second land z−18..−16 has no axial duty. |
| Pin/travel |86 stock; nut local0..10; q2..42 gives40 travel, N20 gives±20. Guides cover local2..84; centers40 apart. |
| Thread/cavity |54 thread with2 nominal end margins; cavity ends atq+84. Float leaves≥1.80 thread margin and31.82 cap clearance. |
| Captured thrust |Wheel OD24,z−26..−21.98; fixed faces−26.2/−21.8; axial shift−.20..+.18. Union overlap.02 reduces initial sketched endfloat.40 to.38. |
| Fits |OD3.2 journals in3.6 bores;4.4 square pin in4.8 guides; unqualified fits. |
| Manual stops |Top tray28×28×2 touches upper guide atq2; bottom8×8×2 shoulder touches lower guide atq42. Continued turning can damage the fixture. |
| Fixture |70×50 foot; tray top118.2..158.2 above foot underside. Two split frames, two3.2×4×3.2 keys in3.6×4.4×3.6 pockets; external tape closes rails. |

Handwheel remains resident and free to rotate during hold tests. Thrust capture
is not moment fixity or passive-hold proof. Second-land halves slide out after
unloading while main support remains. Pair replacement opens the common frame;
seam stiffness, alignment and handling time are unknown. No added per-cell brake.
A rigid.2-mm pin/screw offset atq22 intersects1.243 mm³: a geometric failure witness,
not an FDM distribution. Stop on forced assembly; no fine-adjustment campaign.

## Reproduction and preserved negative controls

Source: `tools/curated-experiment-checks/E-263/article.scad`, `export.py`, `check.py`.
Use a clean BOSL2 checkout136e6367e65d52196a3ea51d03156f8b622c60fc namedBOSL2;
export verifies revision/clean status. Original OpenSCAD2023.09.11, Python
NumPy/trimesh/manifold3d. In a scratch output directory:

```
python3 tools/curated-experiment-checks/E-263/export.py --bosl2 /path/BOSL2 --output /scratch/exports
python3 tools/curated-experiment-checks/E-263/check.py /scratch/exports --pack /scratch/old-comparator.stl
```

This reproduces retired geometry, **not a print instruction**. CGAL ASCII last-digit
seams normalize through manifold float32 topology: require watertight consistent
winding, one component/part, bounds change<.00002 mm and volume change<.001 mm³.
No hole filling/smoothing/slicer repair. Final binary plate was reloaded as eight
separate solids; its archived original is preserved at d0e2470.

- 252 phase/axial-float states: no computed thread, guide or seat collision;
float endpoints sampled.00001 inside contact, with physical intervals analytical.
- Wrong rotation atq22.25 intersects8.834 mm³; overtravel.1 below/above stops
intersects31.296/4.096 mm³; excess screw float±.3 also collides. Key insertion,
frame halves, journals, lands and separated plate parts clear nominally.
- Original plate bounds x5..229,y5..121.2,z0..86;45.367 cm³ solid. Frame halves
70×116.2×25 each; pin28×28×86; screw24×24×80; lands44×10×2; two keys3.2×4×3.2.
Frame split faces down; wheel down; inverted pin tray down. All bed minima0.
Frame recesses bridge≤4.8; pin's final shoulder has1.8 overhang at~84 high.
The old instruction relied on external slicer-generated tree supports there.

Previous visual inspection of assembly/STL and nominal checks did not inspect
deposition. Old PLA/.4-nozzle/.12-layer,3–5 h/40–65 g suggestions were unsliced
estimates, now withdrawn with the offer. No physical test occurred. Its proposed
manual protocol covered signed travel, reversal/play, free-handed hold at low/mid/
high positions, separate guide/frame compliance and timed replacement. A10-g
external test cap was a precaution, not rated capacity; total moving mass also
includes the pin. Finger feel is not stiffness/torque data. No powered testing.

S40/N20 remains the simpler control; S50/64-thread/96-pin/N30 is separate. Laboratory
tray, shoulders, tape and wheel are not pitch-compatible production hardware.
4096/6400 resident pairs still need thread/thrust/radial support plus8192/12800
guide apertures; a second radial land adds4096/6400 alignment duties. E-262's
conditional64-grid/lead3/850-rpm maxima35.54/43.29 s remain above~30 s, with no safe
RPM earned. E-259's$984.64/$1166.40 subset+unquoted reserve omits further hardware,
against~$500/$1000/$1500 benchmarks. This article selects neither head nor product.

## Print-practice correction and manufacturing discriminator — 2026-10-13

**Owner report, not a failed physical print:** Sander inspected the STL and will
not print this version. He asks for deliberate support geometry, prefers horizontal
slender parts, suggests removable batch connections and several identical samples.
The original owner feedback was committed at b9ab170 (former `.agents/advice/feedback.md`) and is consolidated in [fabrication process](../02-design-criteria/fabrication-process.md).
No result about actual print yield follows. Retire the old offer and remove its
STL; keep CAD/checks and this evidence. No replacement is READY or required now.

Reproduce `python3 tools/curated-experiment-checks/E-263/manufacturing.py`.
It reads the exact old plate from Git at d0e2470, without dependencies or retained
output. Mesh envelope checks across91 horizontal roll angles and an independent
analytical calculation agree. Guide intervals are independently reconstructed
with4001 travel positions and a shortened-travel counterexample. Nut-exit mesh
sections at121/241 positions give the same finite collision witness; a known slab
checks the intersection method. **These are
geometric necessary conditions and labor scenarios, not simulated deposition,
measured wobble, surface finish, anisotropic strength or support-removal force.**

| Manufacturing route | New discriminator / disposition |
|---|---|
| Original upright pair | Pin height86 and screw80 mm; broad feet do not laterally brace their upper lengths. Supports under the pin shoulder alone do not prove shank stability. Retire this offer; no measured wobble threshold is assigned. |
| Lay unchanged whole parts flat | Pin tray holds the4.4-mm body11.80 mm above the bed with a face down; diagonal roll increases this to16.69 mm. Screw handwheel holds its3.2-mm shaft10.40 mm above bed (small facet variation). Rotation alone therefore leaves substantial support/bridging obligations. |
| Upright connected batch | Ties only at the feet do not shorten the upper free span. Mid-height ties contact functional surfaces: the lower guide sweeps pin-local2..44 and the upper42..84, covering the entire82-mm outer shank. Guide-safe scar-free tie placement there is unavailable without changing the part or accepting cleanup. A surrounding cage with clearance does not brace until contact; same-layer ties to equally flexible neighbors are not fixed supports. End tabs remain possible, but need a real load path and removal proof. |
| Horizontal pin with removable laboratory tray/shoulder; screw with separate handwheel | Removes large standoffs, but retains a3.52-mm cavity roof and internal helical surfaces. A3.30-mm rigid support fits the cavity but collides during straight axial withdrawal through the nut: archived mesh x-boundary.850006 versus support edge1.65 gives.800-mm penetration. Removing the top cap instead creates a straight cavity exit with.22-mm total nominal width clearance; assumed.10/.30-mm total aperture loss leaves.12/−.08. This bounds an ideal opening, not release force or a designed joint. Fragmented/soluble support or unsupported bridging are different unqualified routes. Separate wheel/cap joints add torque/thrust/alignment or axial-load/end-stop duties. Prefer this conditional laboratory split over a seam through the nut; no replacement STL yet. |
| Longitudinal split pin / molded or outsourced parts | Opening the cavity improves access but adds a registered seam through the nut and guide faces, plus4096/6400 joining and inspection duties if repeated. Do not select a split merely to improve slicing. E-260's unscrewing-core/tooling alternatives remain controls with their own cost and removal duties; none inherits the old PLA holding observation. |

Generic primary [Prusa support guidance](https://help.prusa3d.com/article/support-material_1698)
recommends considering orientation/splitting, describes stability versus removal
tradeoffs and explains support-interface gaps. It supplies no X1C/PLA calibration
for these threads. A support that separates easily is not automatically a rigid
lateral brace. A geometrically open removal path does not prove easy release.

**Assembly consequence:** using E-260's optimistic8-s handling scenario and its
unchanged illustrative setup/bed/rework allocations, the32-h maker allowance has
only10.08/2.485 added seconds **per pair** left at4096/6400 cells. Divided equally
between pin and screw, this is5.04/1.24 s per part for cleanup and all other missing
labor. Ten seconds removal per part adds22.76/35.56 h, giving43.29/63.14 h before
omitted electronics, fixture development and other work. These are sensitivity
breakpoints, not measured labor or a hard four-day rejection gate. Batch supports
must release in groups without leaving guide/thread scars; individual sanding is
not an assumed production route. No new purchased-cost or update-speed pass follows.
The~$500, premium~$1000 and research$1000–1500 comparisons above remain unchanged.

Group release only helps if individual cleanup stays small. At an **assumed30 s
per16-pair batch** (both parts included), removal alone adds2.13/3.33 h and leaves
4.10/.305 s per part under the same32-h allocation. At64 pairs/batch, allowance
becomes4.81/1.01 s; these larger batches have no constructed support or qualified
common release. Scaling the three-pair diagnostic batch at30 s/group leaves
.037/−3.759 s per part: a useful sample is not a production process. Partial
batches are charged in full. A further10-s joining duty per split pin adds
11.38/17.78 h, before joint inspection, cure time or rework. Retain intact nut and
guide faces where possible; a removable laboratory cap need not become a
production joint. All rates and aperture-loss cases are bounds, not process priors.

**Next physical article only after a manufacturing route earns it:** prefer three
identical pins and three identical screws over three fit variants, in one small
batch with supports actually designed/exported and removal access inspected.
First compare removable laboratory appendages with end-connected external bracing;
retain an intact thread/nut before considering a longitudinal seam. Require slicer
layer inspection of the chosen orientation, roof/thread formation and support
interfaces before reissuing any STL. Inspect the integrated load path again if
appendages change. Current geometry alone does not establish that horizontal or
upright printing is the more reliable process.

Record plate positions/lot and which supports touched which faces; preserve raw
widths at low/mid/high shank on both axes if suitable measuring tools already exist,
straightness observations against the same reference, and each specimen's travel,
fit and removal/handling time. Without a suitable gauge, mark dimensions unknown;
photographs and ruler estimates are qualitative. Use one common guide and one
reference mate across samples, then a small cross-mating matrix if the intact
parts turn freely: matching each pin only to its own screw can hide variation.
Do not force, trim or sort until a preferred fit appears. Separate damage caused
by removal from as-printed geometry. Three samples reveal possible same-plate
variation; they cannot estimate batch correlation or board yield (even an assumed
independent5% defect rate has85.7% chance of three clean samples). Another lot is
needed before a lot-to-lot claim. No print, purchase, owner question or deadline
is created; supported retention/speed and E-268 shared-reader access remain open.
