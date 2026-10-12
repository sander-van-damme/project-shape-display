---
status: complete
builds-on: [E-229, E-228, E-220]
---

# Retained programs save channels but multiply decoding interfaces

**Park the tested nine-position, four-bit and six-bit row programs.** The
lowest assumed-cost timing case reduces E-229's 640 channels to 144, but needs
1,440 program bars, 12,960 index notches and 77,760 decoder lands. Its lean
allocation is $527.80 without force-qualified purchases. No local refinement.

**Next change the load transaction:** join changed columns to one ascending
common plane at their old heights, then retire them onto resident supports at
target heights during descent. The ideal replay below establishes this alternative
without an old-height capture array; safe membership writing remains unresolved.

Input main `15cf99c`. Run `python3 tools/curated-experiment-checks/E-230/screen.py`.
Evidence: **architecture hypotheses, ideal state replay and bounded calculations;
self-review**. All non-product numbers are unqualified assumptions: prices,
motion, load, mass, material, errors and proof times. No sourced prices/process
priors, CAD, measurements or physical qualification. Five 10-mm-spaced heights
are a comparison workload, not an approved resolution restriction.

## Physical programs and decoders

Phases are +10,+10,+20,−10,−10,−20 mm. Nine signed deltas suffice. Canonical
magnitude bits for 0…4 are `000,010,001,011,111`; prepend sign. Thus four
binary sites encode the delta; six masks are not six independent information bits.

| Coupling | Retention and actual output route | Physical overwrite |
|---|---|---|
| P: nine-position pattern bar | Six tracks × nine axial lands/bar. Shared phase carriage selects one track; 80 probes read solid/bypass pattern. Backed output yokes sequence pickups then column bars. Common locking comb enters nine-position notches. | Disconnected register unlocks; stripper resets all bars through 24 mm and returns. q rams push groups to nine 3-mm-pitch positions, retract, index groups and return. Temporary drag retains previous groups until common clamp seats. Read groups and clamped result. |
| B: four binary shutters | Sign and three magnitude slides/column. Each of six phase paths passes sign and magnitude gates in series, then a backed output yoke. Twelve gate lands/column: mechanical AND is not free. | E-229 reset/set/read scanner visits 320 retained sites/head, retracts shoes and returns. Every endpoint retains itself after writer departure. |
| T: six-bit mask strip | One retained bit per phase/column, directly read by phase probe. Simpler decoding, 480 sites/head. | Same scanner visits 480 sites, including erase/set/read and return. |

P probe normal force closes through frame backing; lateral reaction reaches
its index comb. Temporary drag is **80 real sites/head**, not free memory.
B/T need permanent endpoint retention. Clamp-induced displacement, probe escape,
output routing and pickup arrest remain unbuilt. No 160-grip head is restored.

P's 3-mm code pitch and 2-mm axial probe leave `(3−2)/2−e` margin:
**.35/.15/−.20 mm** at adverse combined errors e=.15/.35/.70 mm. This is
finite geometry, not X1C accuracy. Six tracks at 6-mm spacing require 36-mm
pattern width: staggered bays and bridges are owed, not a 5.08-mm packing pass.
A 6-mm axial-pitch comparator gives `2−e` margin but doubles write travel to
48 mm: best lean buffered case B9/q40, **28.084 s/$635.80**. Do not refine
small notches to rescue P. B's two serial 4/2-mm window/probe interfaces can
accumulate `1−2e=.70/.30/−.40 mm` adverse margin, versus `1−e` for one gate.
Common phase error, batch bias, warp and shaft twist can corrupt whole banks;
these are bounds, not probabilities or independent-cell yield estimates.

## Schedule and causal retry

E-229 source reproduces H=4[t(2)+.003]=.138491106 s, B6/free-writing
31.720200 s and direct B8 26.079916 s. Keep v=200 mm/s, a=8,000 mm/s².
Its B8 extra-work budget was **.564107907 s/row**. Charge six decoder
retract/index/proof events J=t(2)+.003=.034622777 s plus two .010-s height
reads. Service including six loaded/empty pulses and one row feed becomes
`S=1.1+6H+6J+t(5.08)+.020=2.209083298 s`.
Only **.336371247 s/row** remains for unbuffered writing at B8.

For P, n=80/q and D=24 mm:
`W=2t(D)+2t(2)+.010+n[2t(D)+.010]+(n−1)t(5.08)+t((n−1)5.08)`.
This includes reset/return, unlock/clamp, group push/return/read, forward feed
and full return. Every group can need maximum push. B/T inherit E-229's
finite-gap scanner at e=.35 mm, 58.364 mm/s, now n=320/q or 480/q.
Contact length `(n−1)5.08+4+2(5.08)`, acceleration outside contact, empty return,
two shoe strokes and terminal read are charged. B/q20 needs 90.786-mm stroke;
wide programmer bays and routes remain unresolved.

Unbuffered map: `2+(ceil(80/B)+1)(W+S)`. The 2 s covers command ingestion,
registration and final settling; +1 charges one recoverable row fault. Double
buffering needs two physical programs/bank, separate writer/service selector
interfaces and shared drives. Write i starts after write i−1 and service i−2;
service i starts after write i and service i−1. Each selection costs J.
All banks run synchronous phases with different programs. No media is prewritten.

**Retry writing occurs after detection.** Read actual supported heights (.010 s),
recompute deltas, rewrite/select, then perform full service/select. Replaying
original +4 after partial 0→1 motion ends at 5. The source replaces an optimistic
prefetched retry with this causal drain. Fault proof precedes row feed, allowing
the affected bank to hold position; the normal feed allowance is conservatively
retained. Off-grid states, jams and structural failures require safe stop/service,
not a <30-s repair claim. Buffering never overwrites a register still in service.

Finite grid B=1…80, q=1/2/4/5/8/10/16/20/40/80. Lowest lean-allocation timing
case per topology/buffering choice:

| Program | Registers/head | B/q | Channels | Media sites | Map s | Lean / larger allocation |
|---|---:|---:|---:|---:|---:|---:|
| P | 1 | 16/16 | 256 | 1,280 | 28.403 | $668.60 / $908.60 |
| P | 2 | 9/16 | 144 | 1,440 | 28.899 | $527.80 / $697.80 |
| B | 1 | 12/40 | 480 | 3,840 | 29.396 | $751.80 / $951.80 |
| B | 2 | 9/20 | 180 | 5,760 | 28.746 | $632.20 / $802.20 |
| T | 1 | 14/40 | 560 | 6,720 | 29.120 | $889.40 / $1,109.40 |
| T | 2 | 9/40 | 360 | 8,640 | 27.847 | $779.80 / $949.80 |

P/B8/q20 buffered takes 26.287 s without retry, **30.391 s with causal retry**.
B9 five-row contiguous patches take P/B/T 19.924/19.771/18.872 s including
retry. Idle banks retain supports; their unloaded heads may move underneath.
Retained bank enables inhibit idle row withdrawal and govern one-pitch feed;
they do not provide arbitrary independent carriage positioning. Sparse changes
may traverse no-op rows at full-map time. No shorter arbitrary-seek claim.

## Replication, fabrication and readback

Resident per cell: one moving column, two guide/wear stations, seven shelf levels,
two support sites, no extra moving local lock. Per row: 80 columns, 160 guides/
bearing sites, 560 shelves, one row-comb axis. Board: 6,400 columns, 12,800
guides/support sites, 44,800 shelves, 80 row axes. At B9 each bank holds up to
nine rows; each head has 80 bars, 80 retained pickups, 80 probes, 160 output
links, lift/carriage, bank enable and local arrest. Board totals are 720 each
bars/pickups/probes and 1,440 links. Monolithic parts still repeat these sites.

| Buffered program, B9 | Media/head; board | Index notches/endpoint faces | Decoder lands |
|---|---:|---:|---:|
| P | 160; 1,440 | 12,960 | 77,760 |
| B | 640; 5,760 | 11,520 | 17,280 |
| T | 960; 8,640 | 17,280 | 8,640 |

Lands are patterned surfaces, not separately assembled parts. P adds 1,440
temporary drag sites, 18 clamps, 144 long-stroke rams/guides; B/T add 180/360
scanner gates. All buffered cases add 18 selector interfaces and two shared
drives. Springs/inserts/sockets lack a selected design; hardware allocations
are not zero-count assertions. Head replacement requires seated resident
supports. Buried bar faults affect up to nine cells and may need temporary
support/module removal; a bank fault can expose 720 columns.

Column stock remains 8.192 L. P blanks 32×36×3 mm add **4.977 L**, B/T bit
blanks 20×4×3 mm add 1.382/2.074 L: **138.24/38.4/57.6 h** at assumed
10 mm³/s, excluding guides/cams/frame. Ten-percent scrap multiplies by 1/.9.
Six-mm P pitch lengthens blanks to 56 mm. At 10 s/site, media placement adds
4/16/24 h; 3,600 common bars/pickups/probes/links add 10 h. Column assembly,
fixtures, wiring, calibration and 256-mm build-plate joints are extra. Flat
pattern printing permits face access but does not qualify warp, roughness or wear.

Reader hypothesis: camera/lighting per bank with folded views of media, pickup,
bar and actual-height strips. It owes 80 nine-level or 320/480 binary program
reads; each phase also needs 80 pickup and 80 bar positions; height reads cover
80 columns. Row-comb end flags do not prove 80 shelf contacts. Occlusion, exposure
latency, arrest and load-bearing contact proof remain unresolved. The 3-ms proof
and .010-s reads are **functional grants**, not achieved specifications. Conditional
union bounds at u=10⁻⁶ are .0064 for row codes, .0256 for binary sites and .0384
for output decisions; no measured rate or common-mode coverage is implied.

## Shared power and bought allocation

Replace per-bank motors with common lift, phase, feed and writer drives, plus
retained bank enables. Complete category allocations, **not quotes**:

| Category | Lean | Larger scenario |
|---|---:|---:|
| Controller/power/frame/wiring/spares-freight | 15/20/25/15/10 | 20/35/35/25/20 |
| Lift motor-driver/brake/phase/feed/writer drives/shafts-bearings | 30/10/10/10/20/30 | 40/20/15/15/20/30 |
| Per-bank reader/enable/local arrest/mounts-guides | 10/3/3/4 | 15/5/5/5 |
| Complete channel/media hardware share | .50/.02 | .50/.02 |
| Buffer interface/two common buffer drives | 2 each/16 total | 2 each/16 total |

Lean base $195+$20B replaces E-229's $130+$65B. The .50 channel optimistically
covers multilevel rams as well as binary gates, command electronics and wiring.
Reader shares include folding/lighting; mechanisms otherwise assume printed
parts. No motor, brake, reader or transmission is force-qualified. P/B9's lean
non-channel allocation is **$455.80**: <$500 requires **<$.306945/channel**;
free media hardware raises this only to <$.506945. These are spending thresholds.

At B8, 640 cells can move together. Assume f=1/3.27/10 N/cell including column
gravity, column mass .003 kg, head mass .5 kg/bank, acceleration 8 m/s², friction
.2 of cell load. `F=80Bf(1+.2)+B(.5)g+(B(.5)+80B(.003))8` includes head
weight. Moving mass 5.92 kg; f=3.27 gives **2,597.96 N**, **25.980 N·m** at
10-mm output radius, **37.114 N·m input-equivalent** at .7 efficiency and
**742.27 W peak input** at .2 m/s. Full-board 0→40-mm useful work is 837.12 J;
full load cannot occur simultaneously in both signed directions. At f=1/10,
peak input is 244/2,219 W. These are scenarios, not product load requirements.

End-loaded 400-mm solid shaft with assumed G=80 GPa: `θ=TL/(Gπd⁴/32)`.
At middle load, 10-mm-radius height-equivalent twist is **3.230/.638/.083 mm
for d=8/12/20 mm**. Distributed takeoffs/center drive change the bound but add
real transmission/alignment obligations. Polymer G=1…3 GPa multiplies twist by
80…26.7. No permissible distortion or material qualification is inferred.
Common static arrest must hold 21.320 N·m before shock margins. Shaft failure
downstream defeats a common brake: each loaded bank also needs local arrest.
Phase, pickup and enable states must remain retained after source loss; the
assumed $3 bank arrest does not establish this behavior.

For P drag R=.3/1/3 N, B9 reset force is **216/720/2,160 N** before inertia;
q16 rams add 43.2/144/432 N during setting. B/q20/B9 scanner force reaches
3RqB=162/540/1,620 N under E-229's three-contact scenario. Buffered writer
power overlaps lift power. Unknown reflected media/cam mass worsens acceleration;
cheap drive allocations therefore remain optimistic, not an engineering BOM.

## Changed transaction: merge and retire

Lift starts at 0. At ascending heights 0,10,20,30,40, insert/prove positive
pickups beneath changed columns whose old height equals the plane, then withdraw
their column bars. Continuing members remain attached to the arrested lift.
Unchanged cells keep column support while the active row comb is out; other rows
keep row support. At 40 all changed columns have joined. Descend through
40,30,20,10,0; seat/prove departing columns' bars before retracting pickups at
their target heights. End at zero without separate empty-return strokes.
All moving members share one z: no independently captured old height is needed.
Descent grants gravity following; hanging columns or a need for captive pull-down
remain unresolved, not permission to add free grips.

Physical state is **80 retained membership channels/head**. Direct endpoint
writing preserves continuing members. E-229's erase-all scanner cannot substitute:
clearing an active member removes its last support. Safe selective overwrite,
pickup access, arrest, bar friction and real readback are the next discriminators.
Changed columns deliberately visit 40 mm, up to 30 mm above both endpoints for
a 0↔10 move. Unchanged columns ideally remain fixed; miniature stability during
the detour and lateral collisions remain risks, not a regional-isolation pass.

Ideal direct-write control: eight 10-mm moves, 22 contact stages (five admissions
and five departures ×2, row withdrawal/reseat), ten masks, two reads and feed.
Cycle **1.778329 s**, B6/**480 channels/28.674933 s**, lean **$564.60**. This
is not a survivor: it changes the physical transaction and removes nine-code
media while exposing safe membership writing as the next system-level question.
Do not refine pickups/comb contacts before that writer/load ledger is competitive.

Checks: 15,625 maps for each of four topologies; exact nine-code reconstruction;
15 injected faults caught by ideal interlocks; 175 partial-row retries; 6,561
two-site overwrites; schedule/resource bounds and E-229 reproduction. These
check the model, not contact dynamics, optical proof or manufactured reliability.
