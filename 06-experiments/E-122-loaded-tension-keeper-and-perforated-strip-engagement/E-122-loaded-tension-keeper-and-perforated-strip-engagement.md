---
status: complete
builds-on: [E-121, E-099]
---

# Spring keeper obstructs travel; perforated tape needs a different loaded mesh

**Close the bounded tension-transmission campaign without admitting a complete
force path.** A finite central spring keeper intersects the moving carriage.
A positively engaged perforated tape escapes smooth-cord traction, but the tested
radial and linearly tapered teeth fail the full error box. A tall tapered profile
also loses load-support continuity; shorter profiles retain conditional mesh value.
Neither proceeds to private locks, printing or machine timing. These are scoped
embodiment exclusions, not impossibility of springs, belts or larger internals.

Input main `1df8cb1`. Reproduce:

```
python3 tools/curated-experiment-checks/E-121/finite_routes.py
python3 tools/curated-experiment-checks/E-122/transmission.py
python3 tools/curated-experiment-checks/E-122/transmission.py --population
```

Evidence: generated sections, reduced elastic closure, finite witnesses and
self-review; no physical measurements, process calibration, CAD-kernel solve,
priced parts or qualified hardware. Generated output is not retained.

## Bounded generation and comparison

| Family | Address, energy, storage and force path | Outcome |
|---|---|---|
| Maintained smooth loop | Private lower drive, retained angle still required; upper sheave on spring-loaded yoke; force closes through coil seats/frame and lower axle | Central cartridge obstructs carriage; higher preload repairs a force corner but not geometry |
| Perforated steel-strip loop | Private sprocket, retained angle still required; finite teeth engage holes, outer edge rails oppose lift; upper return sheave and two carriage joints | Full error box has incompatible contact constraints; tall profile loses support; joints/take-up stopped before detail |
| Direct rigid rack heads | Shared transported heads acquire individual grounded columns, lift/set/proof and withdraw | E-099 control; avoids both flexible-loop subsystems, but acquisition, retention and affordability remain unqualified |

Two principles; parameter variants are not architectures. No missing lock,
reader, joint or recovery operation is credited.

## Loaded spring closure, not externally prescribed preload

Coil: .4-mm wire, 1.8-mm mean diameter, 40 active/two inactive turns; 34-mm
installed height. Assumed G=77,000 MPa gives `k=Gd⁴/(8D³n)=1.056241 N/mm`.
Free height 43.183506 mm supplies nominal 9.7 N without an adjuster. The ±1.5-mm
yoke stops leave 15.7 mm before coil solid. Nominal Wahl stress 938.5 MPa is
unqualified; buckling, ends, fatigue and procurement are not accepted.

Source generates seats at z=6 and 40+x, yoke plates to the upper axle at 48+x,
rails, lower-frame posts and the coil helix. Reaction closes from spring through
upper sheave/cord/column/lower axle into the frame, not external ideal preload.

Let `F=Tupper−Tbottom`, `b=Tupper−Tleft`, and
`S=9.7−k(x−frame_shift)−force_deficit`. Then

`Tupper=(S+b)/2; Tleft=(S−b)/2; Tbottom=Tupper−F`.

`F=±.55 N`, `b=±.1 N` cover both directions of the upper bend/bearing loss;
`|Tleft−Tbottom|=|F−b|≤.65 N`. This explicitly allocates E-121's load-plus-drag
budget; it does not add another .1 N for free. Signed force and velocity are
separate. Both loss signs are checked, including the unfavorable combination.

For geometric branch lengths
`A=48+x−4−h−.4+πr/2`, `B=48+x+πr`, `C=4+h−.4+πr/2`, solve
`A/(1+Tupper/EA)+B/(1+Tleft/EA)+C/(1+Tbottom/EA)=free_length`.
The driven lower material segment fixes C's natural length at each command;
**h and x are both solved**, so spring travel cannot silently absorb position error.
This is a piecewise-uniform tension model of the arcs, not a contact solution.

Bounds, not distributions: EA=20/200/2000 N; cutting ±.5 plus irreversible drift
0/.5 mm; spring rate ×.8/1/1.2; force deficit −.5/0/.5 N; relative frame movement
±.1 mm; arc natural-length discrepancy ±.05 mm and lower material partition
±.01 mm; command heights 0/20/40. At EA≥200, independent tension bounds limit
those arc discrepancies to .017672/.007658 mm. EA=20 is outside credible linear
small-strain use. Force deficit includes setting, relaxation and slide stiction;
b covers reversible bearing/bend loss. Creep bounds have no measured timescale.

10,368 cases include 6,912 EA≥200 cases. Trial yoke shifts span
−.376940…+.609152 mm, inside the stops. Worst traction case has S=8.428474 N,
drive tensions 4.264237/3.614237 N and ratio **1.179844**, exceeding
`exp(.05π)=1.170089`: taut but slipping. Heights after slip are trial equilibria,
not achieved positions. Maximum sampled trial error is .608440 mm, not an
acceptance limit. At the high-rigidity drift corner, S0=12/14 N repairs traction
(ratios 1.134565/1.111488); higher preload does not repair the collision below.

## Actual spring/carriage collision and relocation limits

At nominal x=0, coil centerline point **(.9,−1.3,12.92) mm** lies in the carriage
bridge at **h=8.92 mm**. The entire .4-mm wire section is inside remaining solid
bridge material: .30-mm outer-wall and .201110-mm cavity clearance. The source
excludes the bead cavities and cord bore: this is not an AABB-only
collision. The witness persists for h=8.12…9.72 mm at x=0, and h=8.42…9.42 mm
for **every** x within ±1.5-mm stops. It therefore obstructs continuous 40-mm
travel in both directions independently of uncertain spring force or cord EA.
Stop this cartridge before refining spring ends, rail contacts or fasteners.

Translating the cartridge ±3 mm sideways increases the combined cell hull to
6.54 mm along x: 5.08-mm neighbor hulls overlap by 1.46 mm. At 10.16-mm internal
pitch, the x hull screen instead has 3.62-mm separation. **That is a possible
escape, not a failed larger-pitch architecture.** It needs a new finite connection
from the offset spring to the upper axle and full-density fanout/staggering;
none is credited. The bounded comparison does not recursively develop that route.

E-121's terminals and fits also remain material limitations. Opposed radius
errors e give bead/throat retention `.13−2e` and minimum wall `.13−2e` mm:
.08/.03/−.07/−.27 at e=.025/.05/.1/.2. Existing axial fits give `.1−3e`, already
interfering at e=.05. Increasing preload cannot qualify these seats. No hidden
replacement clamp or tightened X1C tolerance rescues the central collision.

## Finite tape entry, capture and loaded transfer

Generate .025-mm tape with 2-mm hole pitch; sprockets with 5/8/12 teeth have
neutral radius `R=n/π`. Tape width 1.6 mm, central hole width 1 mm, leaving two
.3-mm side bands; tooth axial width .6 mm. Longitudinal slots are 1/1.3/1.6 mm,
leaving at least .4-mm bridges. Tooth polygons extend from R−.2 to R+H,
H=.4/.8/1.3 mm, root width .8 mm, tip width .8 (rectangular) or .2 (linear taper).
Dimensions are unqualified design assumptions.

Use straight tangents and circular half-wraps. The 40-mm stroke traverses all
phases over 20 pitches; mirror symmetry checks reverse motion. Polygon/slab
clipping at `R±t/2` gives exact finite intersections. For five rectangular teeth,
H=.8 and θ=.7 rad, a tooth point (R,1.822777) exceeds a centered 1.3-mm hole by
.058693 mm. This is a configuration witness, not a mechanism rejection: another
tooth can take load as tape phase shifts. Positive samples never certify clearance.

Errors e=.025/.05/.1/.2 are opposed dimensional/feature bounds, not distributions
or a transfer of PLA accuracy to foil. Edge rails need `g>3e` against pinch and
`H−g>3e` against lift-off, hence H>6e even at favorable g=H/2. Tapered flanks
require rail reaction; no friction hold substitutes for capture.

54 profile/slot variants span radii 1.592–3.820 mm; the tallest requires up to
10.839-mm internal pitch including .3-mm rim space. Centered entry tests alone
cannot decide the mechanism. **Fixing one seated tooth as permanent load carrier
would falsely reject contact takeover.** The executable therefore intersects all
engaged-tooth constraints, including the finite straight sections and annular wrap.

For tooth j, let its tape-material intersection be [a_j,b_j], nominal hole
center c_j, half-slot w and location error e_j. Feasible common tape phase is

`max_j(b_j−c_j−w−e_j) ≤ δ ≤ min_j(a_j−c_j+w−e_j)`.

Signed load chooses an edge of this interval; changing its active tooth permits
load transfer. Circle/line intersections calculate the curved portions. Negative
interval width is a finite contradiction; sampled positive widths are not a
continuous contact/strength certificate. The 8/12-tooth, H=.8 tapered sections
retain nominal sampled widths .795642/.849873 mm at 512 phase steps. Their
support-phase increments shrink approximately fourfold from 128 to 512 steps.
These remain conditional building blocks, **not** failed fixed-flank interfaces.

**Full-box witness:** at e=.2, H=.4/.8 cannot satisfy both rail-clearance and
anti-lift inequalities for any gap. For all 18 H=1.3 profile/slot combinations,
shrink each half-slot by .2 and assign opposite ±.2-mm position errors to two
conflicting holes. Source reconstructs the actual error assignment, then allows
any common δ. Every combination has an empty phase interval; the least
incompatibility is **.268839 mm**. This excludes the declared box without
assuming centered holes, identical load sharing or a fixed carrier. Correlated
opposed feature errors can repeat; global phase adjustment cannot remove them.

**Independent nominal support-loss witness:** 12 teeth, H=1.3, .2-mm tip,
1.6-mm slot. At wheel phase **.228443713 rad**, carrier tooth j=1 leaves the
straight tape slab. Immediately before/after, the loaded lower phase boundary
changes from approximately −.248178 to −.432203 mm: **.184025 mm unsupported
travel** under one signed load/motion combination. Event offsets 1e−4/1e−5/1e−6
rad give gaps .184393/.184062/.184029 mm, demonstrating a finite jump rather
than coarse sampling. An independent corner-support equation locates detachment:
`(R+1.3)cos(θ)+.1sin(θ)=R−t/2`, θ=phase+2π/12. Other teeth are present but do
not yet contact the loaded flank; arithmetic tooth count misses this loss.

Scope: rigid teeth and taut circle/tangent tape path. Elastic relief over the
entire half-wrap at .65 N, E=200 GPa and .6×.025-mm side bands is only .0026 mm
for the 12-tooth case. Tape lift/bowing, tooth flexure, different profiles/pitch
or articulated chains could change these results and remain unexamined. Smaller
error boxes are not banned, but need justified construction, continuous load/
capture checks, finite length take-up, terminals and full-density routing before
admission. No commercial-belt impossibility or complete tape machine is claimed.

## Construction provenance and transfer limits

Sources accessed 2026-10-10:

- [Samson, Rope User's Manual, pp. 13–14 and 38–39, manufacturer-authored distributor mirror](https://www.elishawebb.com/Samson%20Rope/RopeUsersManual.pdf): distinguishes elastic response, delayed recovery and permanent extension; recommends sheave D/d≥8 for braided and ≥10 for twisted/plaited ropes, with groove diameter at least 10% larger than rope. E-121's D/d=10 is therefore not automatically a bend failure, but this guidance does not qualify .3-mm cord, PLA friction, bead ends or life. No microcord strength is inferred.
- [Alleima 20C strip datasheet, updated 2025-05-09](https://www.alleima.com/en/technical-center/material-datasheets/strip-steel/alleima-20c/): nominal proof strength 1900 MPa below .125-mm thickness. Its 90-degree forming test uses 35-mm-wide samples and a 25-mm die opening; that is not repeated sprocket flexure. Assumed E=200 GPa gives .05-mm tape bending stress 3142/1963/1309 MPa at the three radii. The first two exceed nominal proof; .015/.025-mm variants reduce stress but remain unqualified for perforation fatigue, burrs, wear and availability.
- [Gates, PowerGrip GT3 Design Manual, p. 173](https://www.gates.com/content/dam/documents-library/catalogs/powergrip-gt3-drive-design-manual-en.pdf): entry/exit clearance and backlash depend on tooth profile; belt deformation depends on load and construction. Those observations motivate the loaded check; no Gates rating is transferred to this custom strip.

## Scale, consequences and stopping

For one cell / 80-cell row / 1,600-cell bank / 6,400-cell board, the smooth
route repeats 1/80/1600/6400 cords, coils, yokes and installation settings;
2/160/3200/12800 ends, sheaves and spring seats; 4/320/6400/25600 shaft/bearing
interfaces. Both routes still require one private retainer per cell. Positive
tape substitutes 6,400 strips, 12,800 end joints and at least 12,800 edge-rail
halves; about 339,200–384,000 perforations carry cyclic engagement exposure.
Tape length is 673.28–762.88 m versus 669.60 m cord. Counts are lower bounds:
joining hardware, tension management and access cannot be assumed free.

Dense full-sweep allocation is 21.01 L; 10.16-mm internal pitch at unchanged
height allocates 84.03 L. These are occupied-cell sums, not material volume or
implemented layers. Springs need compressed assembly; foil needs cutting,
deburring, threading and registration. Buried-loop repair needs temporary column
support and access to both ends/sheaves; no service time is claimed.

The <$500 bought ceiling permits **<$0.078125/cell bundle** with everything else
free, or <$0.039063 with $250 elsewhere. These are allowances, not quotes.
E-099's direct control has 320 heads at four banks, conditional 18.854-s full
update and <$0.78125/head allowance with shared transport reserved. No loop
inherits that timing: takeover, proof, retry, relock and return remain missing.
No complete feasible Pareto winner is selected.

Length/setting bias, tooth growth and differential pitch errors can correlate
across a batch, frame or board; no independent-cell averaging is used. Local slip
or jams can lose column support; arbitrary neighbors do not cure either witness.
No reader, false-accept rate, yield, service life or reliability estimate follows.

Self-review checks units, spring energy reciprocity, force balance, constant-force
and exact zero-load closure limits, residuals, cavity-excluding coil collision,
polygon clipping limits, mirrored teeth, independent entry and carrier-detachment
equations, simultaneous error reconstruction and witness/event convergence. Reconstruct E-121 and run
`./repo check`. This is self-review, not independent physical validation.

**Allocation decision:** close this bounded campaign without lock/print work.
Reopen with finite relocated keeper/full-density passages or changed loaded mesh,
capture and terminals, not another radius/clearance sweep. These escapes remain
possible and unexplored. Next portfolio allocation should compare complete
accessible direct-head acquisition with such a changed route. No successor
campaign or staffing expansion is created here.
