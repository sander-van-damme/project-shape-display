---
status: complete
builds-on: [E-148, E-165, E-216, E-236, E-244]
---

# Collective smooth-pin clamps exchange shelves for preload and compliance

**Park the same-plane compressed-pad and serial-spacer embodiments before local
clamp development.** Crossed collective clamps can remove E-236's **44,800 shelf
levels**, and a moving grip supplies downward motion without E-244's cords or
gravity-only return. They retain **12,800 resident friction holds / 25,600 faces**.
The illustrative four-bank schedule is **29.663 s / $441.40 before pads and force
corrections**. Its resident pad needs .95 mm compression inside a section allowing
only .54 mm pad thickness. It is not a feasible machine or a fabrication selection.

Input main `cd37c14`. Reproduce with
`python3 tools/curated-experiment-checks/E-245/screen.py` (stdlib; imports E-236).
Evidence: **architecture hypotheses, ideal support replay and deterministic
force/geometry/schedule calculations; self-review**. All new physical inputs are
labelled scenario bounds, not sourced process priors, material selections, CAD,
measurements or probabilities. Five heights 0/10/20/30/40 mm are a comparison
alphabet, not an approved terrain-resolution limit. JSON output is disposable.

## Complete mechanism and alternatives

E-148 preserves opening-work/arrest obligations; E-165 preserves independent
clamps despite shared carriers. E-216 retains 160 grips/head and two programs.
E-236 supplies tooth-independent support logic. E-244 preserves independent axes.

**Crossed collective clamps:** one resident row strip pair and one resident column
strip pair at separate elevations grip each smooth pin. Each column pair spans
only its bank. Either resident path must hold the entire local load alone.
Shared cams supply clamp energy; retained commands select the column clamp and
moving head grip. A bit actuator is not assumed to generate loaded jaw force.
There are 80 command/grip functions per head, not 80 independently positioned
height axes. Continuous strips still repeat every force-critical contact.

With both resident paths closed: write/read 80 commands; close/prove selected
moving grips on an arrested common datum; open the visited row clamp and selected
column clamps; execute the signed stroke; close/prove resident paths; open/prove
moving grips; then overwrite. Unselected cells retain column support; other rows
retain row support when a column clamp opens throughout the bank. Retain E-236's
[-20,-10,+30,-10,+10]-mm walk. Grips engage any position on the smooth land; there
is no shelf alignment or separate retained height program. This is a changed load
interface, not a new addressing algorithm.

Ideal replay checks **15,625 three-cell maps**, two unchanged rows, **5,765,625
support observations**, 150 regenerated retries and three missing-support/erase
faults. It grants adequate friction, no slip, local arrest and retained commands.
Fractional checks prove bounded logical coordinates, not dynamics. Changed cells
may detour 10 mm; continuous heights need new codes. Command and total-force
readback cannot prove individual support.

Source loss during writing requires closed mechanical clamp keepers; during motion
it requires retained moving grips and a **downstream** local datum arrest. A motor
brake does not cover broken transmission. Friction loss, clamp creep, a broken pad
or a false support proof can defeat both the schedule and containment. Detected
stable wrong heights can be held, reread and reprogrammed once; lost support or
unseatable faults require temporary support and a stopped module. No such hardware
or fault reader is constructed. Real lateral squeeze, frame compliance and stick-slip
may disturb unchanged miniatures even though logical coordinates remain fixed.

| Alternative complete-machine route | Benefit | Scale obligation / decision |
|---|---|---|
| Single common row clamp + independent positioned head outputs | Only 6,400 resident holds | Opens whole row; needs 80 arrested loaded axes/head. E-244's three-head control remains $623 allocated, with cords deleted but axis/hold duties retained. No renewed axis development. |
| Crossed compressed-pad strips + selected moving grips | Smooth columns, positive downward drive, five shared strokes | 12,800 resident holds plus 80B grips; force/travel/packing screen below fails the declared section. |
| Serial floating grounded spacers, squeezed from row ends | Ideal series contact gives equal normal force | Restores 6,400 spacers and vertical grounding interfaces in one plane; cumulative width error displaces pins. Crossed use doubles those resident sites. Screen below. |
| Pressure-backed membranes, same crossed transaction | Ideally equal pressure despite gap variation | Needs 80+80B separately retained resident pressure zones, 80B selected moving grip duties, membranes/seals/volume supply, passive isolation and proof. No pressure source, valve-free retention, routing or purchased budget is granted. |
| E-236 positive-comb control | Direct compression support without sustained friction preload | 44,800 shelf levels; B5/400 commands/26.681 s/$503 lean allocation, still unqualified. |

## Correlated force, stroke and packing

Let each of two opposed faces supply `N_i=k max(0,u-e_i)` newtons. k is each face's
effective local stiffness in N/mm; u and e are **per-face** compression and gap
error. The continuous strip is favorably granted independent local compliance;
real lateral coupling and platen bending could worsen distribution. Coulomb
capacity is `2 mu N_i`. With total static weight L and holding multiplier S=1.5,
all sites in `e_i∈[-E,E]` require:

`u = E + S L/(2 mu k)`

`maximum compression = 2E + S L/(2 mu k)`

`each-jaw release stroke = maximum compression + .2 mm clear gap`.

E=.05/.15/.35/.70 mm, k=2/20/200 N/mm, mu=.1/.15/.3 and L=.2/1/10 N are competing
bounds. **L is total supported static weight, including the pin**; it is not an
assumption that 6,400 sites simultaneously carry the maximum load. A common clamp
must nevertheless be capable at every site where that concentrated load might be
placed. S is an illustrative design factor, not a safety or durability standard.
For the moving grip, the same weight at 8 m/s² ascent/braking needs
`L_motion=L(1+8/9.81)` before any additional axial drag; its compression/stroke is
calculated separately. No gravity-following assumption is used.

For mu=.15, L=1 N, E=.35 and k=20, u=.6 mm; minimum/maximum holding capacities are
1.5/5.7 N. A coherent half-row thin/half-row thick profile gives **960 N on each
row platen**, not 960 N of payload. An all-thick row requires 1,520 N per platen.
Maximum nominal contact stress is .742 MPa on an assumed 3.2×8-mm face. The moving
grip needs 2.723-N minimum capacity and **1.354-mm per-jaw release travel**, versus
1.150 mm for resident clamps. Stress, stiffness and friction have no qualified
material or manufacturing basis.

A whole-row force check is insufficient: at u=0 with ±.35-mm half-row offsets,
40 pins receive zero contact, while the others have **84 N summed friction
capacity**, exceeding a 16-N row test load. There is no mechanism to redistribute
that capacity to the untouched pins. Common compression bias, warp or half-module
misalignment are coherent errors; no IID yield is inferred.

**Finite necessary section:** 3.2-mm pin + two bulk compression pads + .8-mm total
backer allocation must fit 5.08 mm at each support plane. Thus each pad is at most
**.54 mm thick**. Granted usable compressive strains .1/.3/.5 permit only
.054/.162/.270 mm travel. Already `2E=.30 mm` at E=.15 exceeds all those allowances,
even before supplying load. E=.35 needs .95 mm: it exceeds even the entire pad
thickness. Across 324 force/strain cases, only 15 meet this section, assumed timing
and pre-pad cost; **all require E=.05 mm**. This is not qualified ±50-micrometre
manufacturing. Stiffness and allowable strain were varied independently as generous
bounds; the survivors are not known materials.

Staggered planes, bending strips, thinner pins or pressure membranes could escape
this section. Each owes new routing, force distribution and manufacture/service
accounting. Flexural strips still repeat 12,800 compliance duties. No universal
FDM clearance limit follows.

For the serial-spacer comparator, a uniform pin-width bias b accumulates along the
80-pin force chain. Centered end datums give outer-pin shift `39.5b`: b=.05/.15/.35
mm gives **1.975/5.925/13.825 mm**, versus an optimistic .94-mm pin lateral allowance.
Total takeup is 4/12/28 mm. Fixed lateral guides arrest that equalization rather
than making it free. Short independent segments need extra reaction zones; tapered
or different force routing is a changed topology, not a pass of this chain.

A pressure oracle needs `p=SL/(2 mu A)` = **.1953 MPa** at L=1/mu=.15/A=25.6 mm²,
giving 400 N per row platen without stiffness amplification. It still needs .7-mm
local gap accommodation and 400 independently retained resident pressure zones at
B4. Membrane tension, squeeze volume, leakage, seals, source-loss support and
selected moving grips are absent. This is a useful changed force-distribution
principle, not a qualified pneumatic or hydraulic machine.

## Full-machine schedule, work and cost

Each pulse charges physical bit write/read `t(2)+.003`, grip closure/proof,
resident release/proof, loaded motion, resident closure/proof, and grip opening/
proof. Opposed jaws and the row/column clamps move simultaneously **by assumption**.
`t(d)` is rest-to-rest motion at 200 mm/s, 8,000 mm/s². Nothing is prepared offline.
Full cycle is `2+.185+(ceil(80/B)+1)Srow`, including initial registration/final
settling, one full causal row retry and 30-mm empty recovery/read. An independently
expanded event list checks the formula. No inherited write overlap is credited.

| E / k | Resident / moving-grip throw mm | Fewest banks | Seconds | Allocation before pad/force corrections |
|---|---:|---:|---:|---:|
| .05 /20 | .550/.754 | 4 | 26.723 | $441.40 |
| .15 /20 | .750/.954 | 4 | 27.817 | $441.40 |
| .35 /2 | 3.400/5.439 | 6 | 28.326 | $564.60 |
| .35 /20 | 1.150/1.354 | 4 | 29.663 | $441.40 |
| .35 /200 | .925/.945 | 4 | 28.246 | $441.40 |
| .70 /20 | 1.850/2.054 | 5 | 26.548 | $503.00 |

At E=.35/k20 only .337 s additional full-map allowance remains. Five visited rows
in one bank cost 10.036 s including one retry under the same bounds; longer seeks
must be charged explicitly. Softening to k2 reduces the mixed-row platen force
960→456 N but needs six banks. Stiffening to k200 raises it to **6,000 N**. No row
section in these E=.35 cases passes. Faster motion does not qualify force capacity.

The two-face elastic work is `sum(k compression_i²)` N mm. E=.35/k20 stores .772 J
per resident row equivalent. One fully selected B4 pulse closes all 6,400 column
clamp sites, four active row strips and 320 moving grips: **69.768 J**, including
the stronger moving grips. The resident closing stage alone requires **2.704 kW
mean mechanical input during its 23.979-ms move** if newly supplied without energy
recovery. A realizable full-board 40→0 map has three selected pulses per row and
requires **4.186 kJ** over 20 row services, excluding retry, under that same model.
The all-thick column-platen reaction sum can reach 121.6 kN; this is internal clamp
preload, not terrain weight or lift force.

These are not universal electrical power lower bounds. Springs/accumulators could
recover work, but storage, sequencing, losses and supported overlap must exist.
A lever trades force for travel; it does not delete work. The inherited $30 common
drive and $20 supply are not rated for this closure. Frame bending, joint strength,
buckling, actual pad hysteresis, creep and output slip are unmodelled.

Lean allocation remains `$195 common +$20B +$.52×80B` from E-236. At B4 only $58.60
remains below $500 for new contact material, force-rated frame/drive, keepers and
proof. Two 2-mm pads at 12,800 sites total **1.311 L** (already geometrically too
thick); raw-material scenarios $20/60/100 per litre cost $26.21/78.64/131.07 before
cutting, bonding, scrap and assembly. These are unquoted sensitivity allocations,
not a market cost floor. Printed compliant alternatives do not get free lifetime.

## Replication and decision

| Duty | Per cell / row | B4 bank / shared head | Board |
|---|---|---|---|
| Smooth moving pin / ordinary guide stations | 1/2; 80/160 | 1,600/3,200 resident | 6,400/12,800 |
| Resident hold sites / friction faces | 2/4; 160/320 | 3,200/6,400 | **12,800/25,600** |
| Resident collective clamp/keeper axes | shared | 20 row +80 column | 80 row +320 column |
| Selected grip / faces / retained commands | shared | 80/160/80 per head | 320/640/320 |
| Lift/local arrest/carriage/read systems | shared | one set/head | four sets |

No independent resident motor, return spring, insert or socket is proposed.
Contact compliance, keepers, guide bearings, force selection links and clamp
opening duties remain real; finite jaw carriers and inter-plane routing are
unbuilt. A row failure exposes 80 heights, a column clamp fault up to 20, and a
head fault interrupts 1,600 cells. Temporary support and accessible strip removal
are required before repair; crossed support alone is not permission to service
live faulty hardware.

One illustrative allocation puts 8-mm-high row/column pads at z=-10/-24 mm,
and the moving pad at `z=-40+10q`. For q down to -3 and a 40-mm-high column, a
116-mm land keeps its bottom 2 mm below the lowest pad edge. This is vertical
reach only, not routed CAD. 3.2-mm-square stems then total **7.602 L**, 156–469 h
at assumed 15–5 mm³/s extrusion with 10% scrap. Each is 1.485 g before its cap;
active gripping supplies descent. Column insertion at 5–15 s takes 8.89–26.67 h.
Two faces per 400 strip axes give 800 strip placements, 2.22–6.67 h at 10–30 s,
before head grips, anchors, pad bonding, fixtures, calibration and inspection.
406-mm row backers need modular printing on the X1C; their joints add correlated
errors. PLA orientation, roughness, wear and pad adhesion remain unqualified.

**Decision:** remove this same-plane bulk-pad implementation from deep development.
It replaces shelves with a coupled tolerance/preload/space burden and an unpriced
closure-energy machine. Do not tune pad ribs, tiny springs or keeper pockets.
The failed series-spacer chain also does not earn detail. No print is justified
by a timing-only near-budget case.

Next bounded discriminator: test a **mechanically driven, sealed shared pressure
equalizer** against the positive-comb control, starting with complete pressure-zone
routing, local retention and cost/assembly rather than membrane detail. It must
actually replace stiffness-amplified preload, fit the pin grid with generous error
accommodation, and preserve all supported selection phases without hundreds of
additional powered valves. Count fill/seal/repair operations and failure domains;
reject before CAD if the $58.60 residual or support obligations cannot cover a
credible construction. A pressure oracle alone cannot reopen smooth-pin tooling.
