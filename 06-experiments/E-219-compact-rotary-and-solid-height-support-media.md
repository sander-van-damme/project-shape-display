---
status: complete
builds-on: [E-218, A-005, A-024]
---

# Compact support media trade sweep length for depth or inventory

**Park these rotary sector cassettes and vertically exchanged solid blocks.**
The former improves E-218's 15-deck stair to six decks in favorable scenarios;
the latter removes indexing locks but needs 38,320 sorted pieces and hundreds
of handling lanes. Neither earns writer/contact refinement or printing. These
are scoped failures, not rejection of rotary or solid-length memory principles.

Input main `e36bdd7`. Reproduce:
`python3 tools/curated-experiment-checks/E-219/media.py` (stdlib, stdout only).
Evidence: **constructed geometry, exact discrete enumeration and calculations
with labelled assumptions**; self-review. No CAD, sourced process distributions,
quotes or physical measurements. Five heights 0/10/20/30/40 mm are a comparison
workload, not a product resolution decision.

## Complete support transaction

Both retain E-218's disjoint foot lanes: raise incoming profile from −45 to 0 mm,
then lower old from 0 to −45 mm. Ideal gravity-following contact gives
`h=max(old+a,new+b)`; unchanged heights stay fixed only with exact profiles/docks.
Old cassette stores old code: no copied old-code write or friction grip. Write,
retain and read new code unloaded. Fixed cassettes carry parked terrain. Take
old load on its arrested lift before opening old dock; prove new dock before
old descent; prove actual heights before removing old media.

Shared lifts still owe E-218's two-dog positive arrest, engagement proof and jam
access. Missing proof keeps the old path; one pre-transfer bad-code rewrite is
charged. A hung descending column requires detection and supported recovery,
not forced media removal. After transfer faults retain both cassettes and restore
the arrested lift. This is a required sequence, not built sensing or validated
power-loss behavior. Guide drag, contact impact and downward following remain open.

| Medium | Command / retained state | Grounded compression path / missing interfaces |
|---|---|---|
| Five-sector wheel | Unloaded rotation; common bar engages one of five index slots/wheel | Foot → horizontal sector → base/thrust seat → dock; journals, keeper engagements, setter, decks, reader unbuilt |
| Full-height block | Return old piece to sorted stock; insert selected length; floor/sleeve and common transport lid retain it | Foot → block → socket floor → dock; captured fork, five-way feed, sorting, escapements, lid, seating proof unbuilt |
| E-218 control | Translating staircase/common keeper | Terrace/base → dock; 76-mm swept row envelope already fails |

Unlike A-005's resident rotor, this wheel turns only in an unloaded spare.
Unlike A-024's bead stack, a complete height exchanges outside the loaded path.
These changes remove loaded writing, not lift arrest or arbitrary-media preparation.

## Rotary geometry and packing

A vertical-axis wheel has five solid 72° sectors, heights 4+h above a circular
base bottom. A horizontal land is w=1.6 mm radially by l=2 mm tangentially,
centered r from the axle. Enlarge it by e on all sides; e is an **assumed total
registration/dimension keepout**, not an X1C probability. Minimum sector-fit r
and base radius R are:

`W=w+2e; L=l+2e; r=W/2+L/(2 tan(π/5)); R=hypot(r+W/2,L/2)`.

Inner corners touch sector boundaries; extra margin increases dimensions.
A thrust seat supplies axial reaction; flat lands do not retain angle, hence
7,680 index engagements at 16 heads. A horizontal-axis radial cam control needs
radius ≥44 mm if minimum support radius is 4 mm: ≥88-mm rotation envelope.

Put takeover wheel axles outboard of the 2.4-mm-spaced foot lanes: separation
S=2.4+2r. Own bases require S≥2R. Another column offset (i,j) requires
`min_s hypot(5.08i+s,5.08j) ≥ 2R`, s∈{−S,0,S}, over possible cassette sides.
All columns in an exchanging row use both lanes; other rows can retain either
lane through update history. Circular bases physically fill these disks.

| Assumed e mm | Diameter mm | Own pair gap mm | Deck result |
|---:|---:|---:|---|
| 0 | 6.280 | .473 | Six phases, 3×2 residue layout |
| .15 | 7.336 | .130 | Six phases, 3×2 residue layout |
| .35 | 8.744 | −.327 | Own pair collides; decks cannot fix |
| .70 | 11.208 | −1.128 | Own pair collides; decks cannot fix |

Search all rectangular residue layouts with 1–16 phases/axis and every conflicting
integer offset. Independently, six cells in a 3×2 rectangle pairwise conflict at
e=0/.15: ≥6 layers for these fixed axes, attained by the layout. Weaker area
bounds give three/four. Allocating 44 stock +45 exchange +1 gap per deck gives
**540 mm**, versus E-218's 1,350 mm. This is a sufficient envelope allocation,
**not a universal depth bound or routed CAD assembly**. Differentiated column/
relay lengths, guides, cassette bridges and access remain unconstructed.
The colliding cases need lane centers ≥2.727/3.528 mm and a new packing analysis.

The .130-mm slack is after the assumed keepout, not measured functional margin;
extra base/axle error, debris or deflection consumes it. Solid wheel stock alone
is **5.709/7.790 L** at e=0/.15; **317–106 /433–144 h** at assumed effective
extrusion 5–15 mm³/s, before scrap/carriers/columns. Smaller lands would restore
repeated precision risk. Stop before index-slot or rotary-writer optimization.

## Solid inventory and physical handling

Use blocks 1.6×2 mm in section, length 4+h, in closed-floor lateral sleeves.
Two slots/foot coexist during takeover; no block detent or spring. Old pieces
return to five sorted stocks. This removes swept stairs and rotor indexing.

At B=16 banks of five rows, tight simultaneous demand for each code k is
`N+(80−1)B = 6,400+79×16 = 7,664 pieces`.
Witness: initially all k; change one cell/serviced row away from k. Incoming
cassettes duplicate 79 k pieces/row before old removal. Conversely, any incoming
row with 80 k pieces must replace a row with ≥1 non-k; other changed rows need
≤79 k. Unchanged rows are skipped. Thus the bound is both necessary and sufficient
for this inventory model. Each bank can carry 479/code without inter-bank sharing.
Independent exhaustive two-level/two-row/three-cell enumeration attains the bound
at B=1,2. It checks stock accounting, not physical feeding.

Total: **38,320 pieces including installed stock**; at most 7,680 in resident/
spare cassettes, remainder in magazines/bins. Solid volume **2.943 L**;
**163.5–54.5 h** at 5–15 mm³/s extrusion. Ten percent scrap multiplies by 1/.9.
One initial five/ten-second sorting/loading operation per piece adds
**53.2/106.4 h**. Automatic bulk sorting would require another real mechanism.

Construct a vertical fork route: withdraw old block completely; insert into its
sorted vertical magazine; extract target; insert into empty cassette socket.
Charge 1-mm clearance on each stroke. Even omitting lateral routing, fork returns,
magazine gates and registration, time is at least
`2t(5+old)+2t(5+target)`, t a rest-to-rest trapezoidal move.
Worst distinct codes 40↔30 mm take **1.200/.900 s** at assumed v=200 mm/s,
a=2,000/8,000 mm/s². Side loading, telescoping magazines or continuous carriers
change this route and require new geometry; these are not universal feed limits.

Schedule q parallel forks/bank: ceil(80/q) groups, .020 s/group piece/seat proof,
5.08-mm group indexing, E-218's four 45-mm lift/reset strokes, two 2.4-mm transfers,
row hop, .5 s row auxiliary allowance, 2 s global preparation/proof and one full
worst-row retry. No prewritten map; lateral stock traffic omitted, so **incomplete
optimistic schedules, not machine passes**:

| Arrest / acceleration mm/s² | B×q | Lanes | Calculated s |
|---|---:|---:|---:|
| Continuous relaxation /2,000 | 16×40 | 640 | 29.481 |
| Continuous relaxation /8,000 | 8×80 | 640 | 29.937 |
| Continuous relaxation /8,000 | 16×40 | 640 | 23.060 |
| Indexed two-dog /8,000 | 16×80 | 1,280 | 26.853 |

Grid: B=1/2/4/8/16; q=1/2/4/8/16/40/80. No smaller lane count passes. Continuous
arrest is unbuilt; indexed charges a 1-mm stop +1-ms proof each loaded step.
Fast 16×40 with .25/.5/1/2-s row allowances gives 21.560/23.060/26.060/32.060 s.
Five changed rows in one bank take the full-map critical-path time. Other rows
remain docked; unchanged-cell physical disturbance within serviced rows is
unqualified. Faults beyond one detected retry require safe stop, without <30-s claim.

## Whole-machine ledger and manufacturing consequences

Both: 6,400 columns, 12,800 guide stations; 80 resident +16 spare cassettes;
160 docks; 16 heads; 32 lift/arrest sets (≥64 dog functions); transports/readers.
Per bank: 400 columns/800 guides, five resident +one spare, ten docks, two lifts,
one head, q lanes. Per row: 80 columns/160 guides/80 media; spare adds 80/bank.

| Repeated function at B=16 | Rotary | Blocks |
|---|---|---|
| Resident /total media | 6,400 /7,680 moving wheels | 6,400 /38,320 inventory pieces |
| Guidance/support | 7,680 journals +7,680 thrust interfaces | 7,680 sleeves/floor seats |
| Retention | 7,680 engagements, 38,400 positions, 96 common bars | No individual latch; 96 lids; feed gates unbuilt |
| Writer | Stopped before timing/BOM | 640–1,280 captured forks in passing grid; five stock choices/lane |
| Assembly/service | ≥7,680 wheel placements plus keeper/bearing alignment; buried deck access | ≥7,680 sockets plus stock sort/load; jam removal must retain support |

Monolithic printing retains every functional site. 406.4-mm carriers need joints
on a 256-mm bed. E-216 simple-column stock adds 4.608 L before changed feet/tier
routes. Carrier/frame volume, orientation, support removal and rework are unknown.
Dock failure affects 80 cells, head/sorter 400; shared print or reader errors can
affect a bank/board. No IID yield is assigned.

An **assumed $250 non-lane reserve** leaves <$0.391/$.195 per 640/1,280-way handler
under $500; at $400, $.234/$.117. These are allocations, not quotes or a universal
cost impossibility. Fork/drive/coupling, selection/feed, sensor, wiring and mounting
must fit; reserve owes lifts, arrests, docks, transport and power. No BOM does.
A simple 40-lane/bank axial stock layout needs up to twelve 44-mm pieces/lane:
**528 mm** before escapements. Alternative bins/orientations require feed routing.

With coherent error boxes e=.15/.35/.70 mm, block-pair .8-mm gap minus opposing
errors becomes .50/.10/−.60 mm. Sleeve running clearance/wall thickness is still
owed. A 44-mm unsupported 1.6×2-mm post at **assumed E=1–3 GPa** has pinned Euler
load **3.48–10.44 N**, a stiffness scenario, not a PLA allowable. Sleeves shorten
span but add thousands of drag/wear interfaces. Orientation, anisotropy, roughness,
creep and cycle life are unqualified; common height/dock biases do not average away.

E-218 load scenarios F=1/3.27/10 N still mean 80/261.6/800 N per row,
.8/2.616/8 N·m at 10-mm ideal radius, and 3.2/10.464/32 J per 40-mm rise.
Opposing cassette height errors move unchanged cells by up to 2e=.30/.70/1.40 mm.
Nothing here qualifies force capacity, gravity following, disturbance or readback.

## Decision

Preserve six-deck packing and tight reusable-stock bounds; no local refinement.
Reopening needs changed topology, such as captive media rewritten in place or
side/continuous loading that removes four long handling strokes and fits its stock.
Construct and count the changed route before optimizing its contacts.
Next reconsider E-218's **whole row-cassette substitution**, whose paired lifts
and duplicate target media recur as system costs: compare in-place shared backing/
support-layer reconfiguration against cassette exchange, first proving support
continuity and arbitrary-map state. Selection alone still supplies no load path.
