---
status: complete
builds-on: [E-081, E-083, E-088, A-005, A-013]
---

# Retained multilevel commands reduce writing, not support operations

**Retain a signed-displacement trip for finite mechanism investigation.** Its
abstract controller handles arbitrary mixed raising/lowering without resetting
unchanged columns. On the 21-level all-displacements map, programming and exact
clearing require **160 multilevel row transactions**, against E-083's **3,440
binary transactions**. Forty deposition groups and 12,800 support observations
remain. This is a conditional workload advantage, **not** a physical decoder,
30-s machine, manufacturing yield or affordable purchased channel.

Input main `a8fcb78`. Reproduce with
`python3 tools/curated-experiment-checks/E-089/retained_controller.py`;
`--trace` emits the mixed `(2,0,1) → (0,2,1)` support history. Deterministic
standard-library coordinate synthesis, discrete support replay and a separate
one-dimensional slot calculation; no randomness, contact solver, CAD, measured
process prior or physical evidence. No generated output needs preservation.

## Coordinate synthesis and materially different comparisons

A gripped column obeys `z=old+e` after acquisition at e=0. Generate memory
`q=a*old+b*target`, a,b in {-1,0,1}, against either elevator reader `e` or
column-tail reader `old+e`. Require equality at `e=target-old` for every
old/target pair in {0,1,2}. Of 18 encodings, 16 fail with retained counterexamples;
two survive: **q=target-old against e**, or **q=target against z**. The same
coefficient identity proves the result for arbitrary real heights. Unit reader
gain removes scaling/sign duplicates. This is a small coordinate synthesis,
not exhaustive mechanism invention. Both survivors belong to one retained-trip
family; changing the coordinate reference is not a new operating principle.

Comparing an absolute target directly with e fails: old=2,target=1 trips at e=1
and leaves z=3. A tail-referenced target trip avoids that error but needs a
moving local reader/ground reference and physical direction selection from
old versus target. It is a reserve, not granted a free comparator/sign bit.

| Architecture / descriptor | Energy, storage and support | Addressing and reset | Principal gate |
|---|---|---|---|
| Retained displacement trip | Shared signed elevator; non-load-bearing position word; independently persistent ground pawl and grip | Banked row setter; sign gate, local trip and global RETURN inhibit; exact word clear after both signs | Finite detents, sign/trigger/return cams, support sequencing, loaded release and individual proof |
| Selective deck with stepped supports | Shared upward pickup/downward deposition; rotor is both target memory and load stop | Write retractable pickup hooks; pick up sequentially; program unloaded rotors; clear hooks after return | Selective hook/deck passage, unloaded rotor setting, load-bearing steps and release |
| Direct-positioning writer (A-013) | Independent reusable head coordinates; persistent ground pawls store actual terrain | Acquire/position/deposit per changed row, withdraw, return and index; no command array | Complete head cost, support geometry, packing and proof time |

The deck is an A-005 operating-principle comparison with explicit selective
pickup, not a claim to invent a new rotor. Direct positioning remains the
simple control; none inherits a priced actuator or qualified support primitive.
No load-bearing binary stack is reopened.

## Signed trip: causal hypothesis and executable support sequence

At each cell, a guided memory cursor has 2H−1 retained positions for signed
commands −(H−1)…0…H−1. A row head positively sets and verifies its position
while all cells are grounded and the output cams are parked. A **single slot
on the cursor** meets a probe linked to the shared elevator coordinate through
ratio alpha. At coincidence the probe can enter and enable a cam follower. A
separate cam supplies support-transfer energy; the probe is a selector, not a
column brake or service-load support. No inertial fly-through capture is
credited: the elevator stops at each used displacement and the probe is
inserted/retracted during dwell; every transfer includes probe withdrawal
and follower reset before the next move. It stays withdrawn during motion.

The cursor's location relative to neutral supplies a proposed sign gate:
phase-specific combs act only on the negative or positive side, with neutral
physically blocked. A common RETURN phase positively withdraws probes and
inhibits output cams on the empty return. These are **physical hypotheses
needing finite parts and transitions**, not implemented couplings. A logical equality
in the replay stands for this unqualified trip. Independent data axes still
set arbitrary row words; no address-bit-only decoder earns channel savings.

The executable cycle is:

1. Write all changed row words, including neutral values in unchanged sites;
   prove the complete vector, then enable output motion.
2. At e=0 acquire the negative-command group. Prove grip before opening ground
   pawls. Descend through the negative destinations; each tripped group closes
   and proves ground support before releasing grip.
3. Return empty to e=0 with the common cam inhibiting crossed trips. Acquire positive
   commands and perform the analogous ascent/deposition/empty return.
4. With every changed cell grounded, rewrite command rows to exact neutral,
   prove clear, then re-enable acquisition. No residual word survives into the next map.

Grip offset stays fixed while engaged. Unchanged cells stay grounded,
ungripped and at their old height; each changed column stays inside its
old/target interval. Clearing cannot open either support. Required logical
support states are ground only, ground+grip, grip only, ground+grip, ground
only; command memory and the global phase are additional independent states.

A second replay variant uses a per-cell done latch to inhibit return trips.
Self-review removes it from the preferred sequence: one acquisition per sign,
monotone deposition, and a globally inhibited return need no separate local
done memory. The simulator still tracks completed cells as verification
bookkeeping, not a physical bit under global inhibition. Omitting either
variant's required return safeguard exposes an invalid trip
without grip. This challenges a controller-induced 6,400-latch burden rather
than treating it as an inherent cost. The shared interlock is a common-cause
failure point; its positive mechanical inhibition and recovery remain gates.

Real unloading/reseating microtravel, compliant load sharing, finite pawl
engagement and proof cannot be replaced by that co-located logical overlap.
The replay deliberately does not certify them. A failed proof must inhibit
release/motion while the existing support remains held; recovery force,
withdrawal path and a reader able to distinguish false support remain open.

## Selective deck and direct-writer controls

An armed hook lets the common deck pick up a column when its elevation reaches
that column's **old** height. Columns initially at different heights are
acquired at different elevator coordinates; every acquired hook consequently
has zero offset. Ground support unloads only after pickup. At a height above
all selected old/target values, program the now unloaded stepped rotors.
Descend, depositing each column when its new stop is reached. Release must
permit the deck to continue: a captured hook needs disengagement, while an open
unilateral lift contact can separate without retracting its lip. Unchanged
hooks stay out of the deck path throughout.
This avoids E-081's forbidden simultaneous unequal-height rigid reset by
changing the acquisition geometry, not by assigning new offsets mid-grip.

The replay uses **one level of top clearance**, hence 10/5/2 mm for H=5/9/21;
this is an explicit scenario, not a required or sufficient physical clearance.
Changed columns can rise above both old and target, even above 40 mm. That
extra envelope and changed-region disturbance are liabilities. Full-map deck
travel is 100/90/84 mm, excluding contact microtravel, versus up to 160 mm for
signed displacement. Hook passage, sustained deck load, rotor sweep and
unload/release remain unproved; no selective hook is assumed to pass through
a neighboring unselected column without finite geometry.

The direct-writer control uses an independent coordinate, acquires each column
at its old height, moves to target, proves the pawl, releases and returns home.
Small-map replay is serial; the ledger conditionally credits 80 simultaneous
heads with one changed-row visit. Per-head return, contact and verification
remain inside that visit. A-013's procurement/geometry failures still apply to
its tested embodiments. No current cost or performance capability is borrowed.

## Full and regional accounting

H=5/9/21 are comparison workloads spanning 40 mm, not new product resolution
requirements. Full adverse maps repeat `(h,0)` and `(0,h)` for each nonzero h
in every row; cyclic, uniform, unchanged and 5×5 initially flat patches are
also executed at 80×80 scale.

| H / adverse full map | Binary row writes incl. clear | Displacement multilevel writes incl. clear | Displacement deposit groups | Deck hook + rotor writes | Direct row visits |
|---|---:|---:|---:|---:|---:|
| 5 | 880 | 160 | 8 | 160 + 80 | 80 |
| 9 | 1,520 | 160 | 16 | 160 + 80 | 80 |
| 21 | 3,440 | 160 | 40 | 160 + 80 | 80 |

These operations are **not equal-cost transactions**. A 41-position word is
not a binary paddle stroke. At H=21 the write-count reduction is 21.5×, but
E-088's 19-mask/eight-bank target cannot be translated into timing acceptance
without a multilevel setter and complete new itinerary. For eight banks,
160 row writes are 20 synchronized bank rounds if each row is written once
and cleared once. With a hypothetical 6-s total reserve elsewhere, the
all-inclusive programming/clear round average must be **<1.2 s**. This is an
allocation equation, not a sufficient bound; support dwell may exhaust the
reserve. Forty deposits plus two acquisitions allow <143 ms/group even if
that entire six seconds is spent on transfer and none on travel/settling.

The five-row patch needs ten multilevel transactions, fifty support observations
and four/five/five deposit groups at H=5/9/21. Deck accounting adds five rotor
row programs. A single patch gets no eight-bank speedup when contained in one
bank. Unchanged maps produce no writes or motion. Logical isolation establishes
no physical displacement bound on neighboring terrain or miniature retention.

A displacement machine still repeats 6,400 memory guides/detents, slots/probes,
sign gates and two output support functions; the alternative adds 6,400 done
latches. Global return inhibition needs shared cam retention and proof. At H=21 a rail with
41 discrete positions implies **262,400 detent positions**, not 262,400 moving
parts. Their manufacture, wear, assembly and service burden is unresolved.
The row setter still needs 80B independently set data coordinates, plus
transport/lift/readback/support drives. At B=8, reserving $250 elsewhere leaves
<$0.390625 per one of 640 data channels **before other channels**, with free
cell purchases. E-088's 656-channel example gives <$0.3811; its package cannot
be inherited automatically. A single $0.02 bought item/cell consumes $128.
No quotation, complete BOM, print-time or Pareto winner is established.

For a changed full board, word-setting and exact-clear proofs inspect at least
12,800 cell states, with 12,800 support observations. Individual grip/probe withdrawal and shared return-inhibit proofs are
additional; the controller does not implement
readback or assign them free time. For measured unsafe-accept bounds p_j, the
union bound is `P(any unsafe acceptance) ≤ min(1,sum(N_j*p_j))`; no p_j is known.
Common reader/rail errors are not averaged away. Retry credit requires detected,
recoverable faults and retained load support; no reliability number follows.

## Bounded slot screen and next finite section

For a single translated rectangular slot and 0.4-mm reader, choose half-window
`a=p/2`, `p=alpha*40/(H−1)` mm; slot width is `0.4+2a`. Full reader insertion
at the commanded state requires total relative error E≤a; rejecting the nearest
wrong state requires p−E>a. Endpoint containment checks both signs of E.
No fictitious land-between-apertures limit is imposed on this **single** slot;
retention detents are a separate ungenerated interface. Reader width is a
geometry scenario, not a qualified X1C feature.

Cross H={5,9,21}, alpha={0.25,0.5,1} with relative-error boxes comprising
(common, spatial, local)={(.05,.025,.025),(.10,.05,.05),(.20,.10,.10)} mm.
The totals are 0.1/0.2/0.4 mm, summed coherently. These are competing epistemic
bounds, not empirical distributions or Monte Carlo yield. They permit fully
correlated print/registration bias and spatial warp. Relative transmission
scale error must fit this budget too: at a 40-mm extreme, a 1% ratio error
alone contributes 0.4 mm at alpha=1 (0.2 mm at alpha=0.5) before other errors.

For 21 levels, alpha=0.25 has 0.5-mm state pitch and fails the 0.4-mm box.
Alpha=0.5 gives a 40-mm signed cursor stroke, 1-mm state pitch, 1.4-mm slot,
and 0.1-mm capture/neighbor margins in that box. Alpha=1 doubles stroke and
increases margin to 0.6 mm. These are one-dimensional reserves, not package
survivors. Lateral clearance, slot/reader size error, detent force, friction, PLA creep, layer
orientation, accumulated wear and dynamic overshoot have not been checked.
No probability is inferred from the surviving scenario count.

**Evidence boundary:** the slot screen does not generate retained detents,
positive setting, sign/return inhibition or support-transfer parts. Width errors,
finite plate ends, independently blocked probes and loaded withdrawal can change
the choice of alpha and topology. The selective deck remains the different
load-path reference; this abstract result does not justify printing.

Self-review, not external validation: all **729 three-cell old/new maps** at
three levels pass three abstract controllers plus the alternative return
policy (2,916 replays). Closed
path formulas independently check displacement/deck travel; all changed cells
need exactly two support observations. Injected missing ground support,
missing done retention, a missing global return inhibit and a stale command
produce unsupported load, trip without grip and unchanged-region motion failures. Sixteen rejected
coordinate encodings preserve counterexamples. The E-083 source independently
reproduces the 880/1,520/3,440 comparison counts. Slot containment is checked
with finite interval endpoints; it is not swept 3D contact. Between stops,
column paths are affine, so endpoint invariants cover those segments; contact
transitions remain ideal. There is no numerical time step or physical
qualification claim.
