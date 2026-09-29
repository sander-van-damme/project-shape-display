# Cost, printability, assembly & reliability envelope — DND-104 mechanism classes

> **Issue:** [DND-109](/DND/issues/DND-109) (CostManufacturing), child of [DND-104](/DND/issues/DND-104).
> **Purpose.** Give the reliability-first program an **independent, sourced-class** cost and
> FDM-printability envelope for the *mechanism classes* it is choosing among, so any candidate can
> be costed and screened for printability **without a fresh sourcing pass each time**.
> **Evidence class.** **SOURCED-CLASS LISTING OBSERVATIONS + CALCULATION.** No part has been
> bought, printed or measured ([DND-27](/DND/issues/DND-27)). All prices are point-in-time and must
> be re-verified before purchase. Where a number is *not* a current listing it is labelled
> `sourced-class` (a defensible retail class, usually a marketplace range) or `assumption`.

Companion data: [`cost_envelope_dnd104.csv`](cost_envelope_dnd104.csv) (one row per bought line,
three price scenarios, `printable_excluded` / `consumable` flags, sourcing reference, death note).
Reproducible arithmetic + gate: [`cost_envelope_checks.py`](cost_envelope_checks.py).

---

## 0. How to use this envelope (the point of the deliverable)

A candidate mechanism is costed by **counting actuators, transmission lines, media, sensors and
splice hardware** and looking them up here. Three rules decide most candidates before any CAD:

1. **Actuator count is the cost cliff.** One shared NEMA23 lift motor is ~$30. Six thousand four
   hundred of any bought actuator — even a $1.20 N20 — is **$7,680**. Reliable architectures must
   have **zero bought actuators per cell and per dense row**
   ([DND-104](/DND/issues/DND-104);
   [04-architecture-candidates](../../../04-architecture-candidates/README.md)).
2. **Any bought part required once per cell kills the budget.** At $0.10/cell the board is **$640**
   in that line alone — already above the entire <$215.52 parts ceiling. This is independent of
   which mechanism wins. (`print_reliability.py` reached the same conclusion; re-derived here.)
3. **Media and consumables are not obviously printable-and-excluded.** A punched card / roll film is
   a **bought consumable** if it is card or film. It must be *flagged*, not waved away as "printed".
   ([DND-91 A5](/DND/issues/DND-91).)

### Delivered-uplift convention (restated)

The repo's delivered convention is **additive ×1.16 = +10 % shipping +6 % tax**, applied to the
**purchased-parts subtotal** ([DND-41](/DND/issues/DND-41); restated in [DND-93](/DND/issues/DND-93)
and the S6-LC BOM). It is *not* a multiplicative ×1.166.

```text
delivered = parts_subtotal × 1.16
parts_ceiling_for_$250 = 250 / 1.16 = 215.52 USD
```

For a **< $200 parts ideal** the delivered figure is **$232.00**; for **< $250 parts** (the DND-104
strong target) the parts ceiling is **$215.52** and the delivered ceiling **$250.00**.

---

## 1. Sourced-class cost envelope (the table)

Full per-line figures, three scenarios and flags are in the CSV. Summary by category, with the
**working** scenario (a defensible current retail class, *not* best case):

| Class | Representative lines | Working unit | Where it is bought vs printed |
|---|---|---|---|
| **Actuators** | NEMA17 $11, NEMA23 $30, small index stepper $8, N20 $2.20, latching solenoid $4.50, Adafruit 2776 $4.45, micro pump $5, micro valve $4 | per unit | **bought**, count must be **single digits to low tens** |
| **Transmission** | T8 screw+nut set $13, guide rod $4, MGN12 rail $11, LM6UU $0.45, mini bearing $0.34, GT2 belt+pulleys $7, coupler $1.20, thrust bearing $2.50 | per unit | **bought**, shared axes only |
| **Media** | punched card $0.60/sheet, tape $1.20/m, reusable sheet $1.50, cover film $3, card puncher $20 | per unit | **CONSUMABLE / bought** — see §2 |
| **Electronics** | RP2040 $5, DRV8833/TB6612 $0.80, 74HC595 $0.13, ULN2003 $0.15 | per unit | bought, cents-scale fan-out is fine |
| **Power** | 24 V SMPS $12, buck $1.80, power switch/fuse $5 | per board | bought, one set |
| **Wiring** | loom $14, JST kit $5, cable chain $8 | per board | bought; **scales with any per-cell wiring** |
| **Sensors** | hall/slot home $1.00, encoder $3, whole-board scan $35 | per axis / per board | datum only is cheap; per-cell sensing is fatal; one scan is an allowance |
| **Structure** | splice hardware $8.09, fasteners+inserts $8, optional extrusion $14, lube $8 | per board | printed geometry is free; **splice hardware is bought** |
| **Misc** | spares $8 | per board | per DND-46 policy |

### What is plausibly printed-and-excluded vs must be purchased

| Printed-and-excluded (legitimate per [DND-70](/DND/issues/DND-70)) | Must be **purchased** (flag it) |
|---|---|
| cell columns, pawls, latches, combs, gates, rotors, cams, racks | **all motors, solenoids, pumps, valves, drivers, MCU, PSU** |
| tile/media **carriers** and cartridges | **media where it is card or film** (consumable) |
| frames, platen modules, brackets, housings, guide brackets | **card puncher / writer head** if it is a real machine subsystem |
| splice **geometry** (the tabs/pockets) | **splice hardware** (bolts, inserts) |
| passive memory features (ratchet teeth, hard stops) | bearings, rods, belts, pulleys, couplers, thrust parts |

> **Rule:** the printed-exclusion exception applies to **structure and passive mechanism**, never to
> a **consumable medium** or a **motor/valve**. Every row of the CSV carries `consumable = yes|no`
> and `printable_excluded = yes|no` so a candidate cannot silently absorb either.

### Three scenarios

The CSV gives `optimistic / working / high` per line. For a whole machine the scenarios combine as:

```text
optimistic = sum(unit optimistic × qty)   # best marketplace listing, small packs
working    = sum(unit working    × qty)   # defensible current retail class
high       = sum(unit high       × qty)   # branded / matched / small-qty penalty
delivered  = parts × 1.16
```

A candidate is **screen-pass** only if **working delivered <= $250** *and* all bought-per-cell
counts are zero. Expect a **~1.5–2.5× spread** between optimistic and high on soft lines; that
spread is the sourcing risk, and it is why the S6-LC audit repriced the softest lines upward
([DND-91 A5](/DND/issues/DND-91): $162 → ~$197 delivered).

### Sensitivity to per-cell bought hardware

| Bought hardware per cell | Board cost (6,400 cells) | Verdict vs $215.52 parts ceiling |
|---:|---:|---|
| $0.00 | $0 | any architecture can fit |
| $0.01 | $64.00 | consumes 30 % of the buying ceiling |
| $0.05 | $320.00 | **fails** on this line alone |
| $0.10 | $640.00 | **fails** (≈3× the ceiling) |
| $1.20 (one N20 each) | $7,680.00 | **arithmetic death** |
| $4.45 (one solenoid each) | $28,480.00 | **arithmetic death** |

**This table is the single most important result.** Every credible reliability-first candidate must
have **zero** per-cell bought hardware.

### Where a credible design dies on cost

- **Per-cell or per-row bought actuator** (motor, solenoid, valve, pump): dies immediately (above).
- **Bought per-cell bearing/bushing** at $0.34: $2,176 — dies.
- **Matched micro-stepper for a dense writer head**: the only *traceable* 8 mm 18° bipolar PM
  stepper is MOONS 8PM020S1 at **$40/ea**; 80 channels = **$3,200** (the historical S5 K7 result,
  [sourcing_notes.md](../../test11_cost_printability_reliability/sourcing_notes.md) §9).
- **A bought card-puncher/writer that is not shared**: a real automatic punch is a subsystem, not a
  $0 "shared tool" ([DND-91 A5](/DND/issues/DND-91)).
- **A per-cell height sensor**: even $0.60/cell = $3,840 → dies. Recovery must be **one**
  whole-board scan ($35 allowance) or a sample check, not 6,400 sensors.
- **Any bought part at ~$0.03/cell or above** erodes the whole ceiling: at $0.03 the line is $192,
  leaving **$24** for motors, power, electronics and structure. There is no room.

---

## 2. Media / consumable lines — explicitly purchased vs printable

The DND-104 program treats the mask as a separate subsystem. Media must be classified honestly:

| Medium | Printable? | Consumable? | Cost line to carry | Notes |
|---|---|---|---|---|
| Punched **card** | no (needs purchased stock + punch) | **yes** (one per height-level per map) | $0.15–2.00/sheet | one medium per level; 5 levels → 5 sheets/map |
| Punched **film / roll** | no | **yes** (per metre) | $0.40–3.00/m | sustained cycles consume stock |
| Continuous **tape** | no | **yes** | $1.20/m class | double-buffering still needs stock |
| **Reusable** perforated/embossed sheet | material bought, geometry printed | no (amortised) | $0.60–3.50/sheet | reusable only if rewriteable without a **bought per-cell writer** |
| Printed **comb / gate strip** (passive, part of mechanism) | **yes** | no | **$0** (printed) | legitimate printed mechanism, not media |
| Printed **slotted strip / perforated belt** if fully FDM | **yes** | no | **$0** | must be ordinary 0.4 mm geometry or it is a fine-nozzle risk (§3) |
| Cover / **anti-dust film** over the field | no | **yes** (wear part) | $1.00–6.00/board | consumable wear interface |
| **Card puncher / writer head** | no | no | $8–45 (shared tool) | *shared* tool is legitimate; a per-map automatic writer is a purchased subsystem |

**Rule for candidates:** if the map state is carried by a **consumer stock** (card, film, tape), the
BOM must carry a per-map/per-cycle **media line**. If it is carried by a **reusable printed
mechanism**, the line is $0 but the *printability* and *fatigue* of that mechanism move to §3–§4.
"Printed" may never be used to hide a consumable.

---

## 3. FDM printability at 5.08 mm pitch — PROVISIONAL vs sourced

Baseline: **Bambu Lab X1 Carbon, PLA, 0.4 mm nozzle, 0.2 mm layers**, per
[02-design-criteria](../../../02-design-criteria/README.md). The X1C publishes **no guaranteed
finished-part dimensional tolerance** (7 µm is lidar *sensor* resolution, not part accuracy), so
every clearance below is a **rule to be coupon-validated**, not a certificate.

| Rule | Value | Class | Basis |
|---|---|---|---|
| Minimum robust wall (0.4 mm nozzle) | **0.88 mm** (2 lines) | SOURCED (process) | X1C 0.4 mm line width ~0.42 mm; the repo's fabrication gate uses 2 lines = 0.88 mm |
| Minimum standalone feature (0.4 mm) | **0.44 mm** (1 line) | SOURCED (process) | one extrusion width, no redundancy |
| Fine-nozzle single-wall floor | **0.22 mm** | SOURCED (process) | X1C 0.2 mm nozzle; reinforced filaments discouraged |
| Minimum **inter-body web** at 5.08 pitch | **>= 0.45 mm/side** for 0.4 mm nozzle | **PROVISIONAL** | `print_reliability.py`: 4.68 mm body → 200 µm web = **fine-nozzle/resin only**; 4.48 → 300 µm, 4.40 → 340 µm, both marginal and 4.40 drops surface fill to 75 % |
| Body width to keep ordinary 0.4 mm web | body **<= 4.18 mm** (web >= 0.45) | **PROVISIONAL** | derived: `(5.08 − body)/2 >= 0.45` |
| Nominal top-gap stack | 0.40 mm nominal → **0.05 mm worst case**, **0.18 mm RSS** | **PROVISIONAL** | contributors ±0.10 width, ±0.05 index, ±0.10 deflection; at 5.08 pitch the gap can vanish before dust/creep |
| Sliding clearance (general) | **>= 0.20 mm/side** nominal, coupon matrix | **PROVISIONAL** | no measured X1C tolerance exists; must be a clearance matrix |
| Press / snap fit | **coupon matrix required**, no CAD constant | **PROVISIONAL** | process-dependent (flow, orientation, shrinkage) |
| Hole diameter compensation | **measure per lot**, typical +0.05–0.15 mm | **PROVISIONAL** | published printer spec does not fix it |
| PLA creep under sustained load | **NOT qualified** — sustained-load tolerance must be life-tested | **ASSUMPTION / risk** | PLA creeps; the release-comb/cam toe sits preloaded |
| PLA fatigue across >100 cycles | **NOT qualified** | **ASSUMPTION / risk** | no cycle data; coupon must run >=100 engage/release cycles per cell |
| Wear / friction interface | dry-cleanable, replaceable cartridge mandatory | **ASSUMPTION** | dust and wear at 5.08 pitch are unquantified |

### Geometry that needs the 0.2 mm nozzle or resin (flag it)

- any **web < ~0.30 mm** at the pitch band (a 4.68 mm body leaves 200 µm) — **fine-nozzle/resin**;
- any **single wall < 0.44 mm** — not ordinary 0.4 mm geometry;
- Test08's **0.20 mm guide wall** — below the fine-nozzle floor once any XY compensation is applied;
- **pawl/latch leaf <= 0.45 mm** in the bending axis — the S6-LC pawl leaf is exactly this and was
  flagged **RISK** in its own printability record; it is *not* robust 0.4 mm geometry.

**Ordinary-0.4-mm-goal rule:** a reliability-first candidate should keep every *structural* feature
at **>= 0.88 mm**, every *standalone* feature at **>= 0.44 mm**, and every *web* at **>= 0.45 mm**,
so it prints on the baseline nozzle. Any candidate that depends on a sub-0.44 mm leaf, a 200 µm web
or a 0.20 mm guide wall is a **fine-nozzle/resin** candidate and must say so.

### Print yield, time and count

From the repo's own print data (`08-integrated-designs/s5r-shared-drive-register/fabrication/manifests/print_manifest.csv` and
`print_reliability.py`):

- S5-R prints **6400 rotors + 6400 pawls + 6400 keepers + 6400 detents = 25,600 cell parts** plus
  frames; at 45–300 s/part that is **160–1,600 printer-hours (~1–9 weeks) on one X1C**.
- **Print yield across thousands of identical fine parts is unproven.** Yield < 100 % multiplies the
  effective part count and the assembly workload; a 1 % reject on 25,600 parts is 256 reprints.
- Fine 0.2 mm-nozzle / resin parts are slower and more failure-prone; prefer 0.4 mm geometry where
  the physics allows.

---

## 4. Assembly and reliability scaling

### Part counts and hands-on hours

| Architecture | Cell-level parts | Board cell parts | Assembly estimate |
|---|---:|---:|---|
| S5-R (rotor memory) | 4 (rotor, pawl, keeper, detent) | **25,600** | 10–30 s/part → **71–213 h** |
| S6-LC (pawl + rack) | ~2–3 (column, pawl, [gate]) | **12,800–19,200** | 10–30 s/part → **36–160 h** |
| Any candidate with **0 cell-level bought parts but 2+ printed moving parts** | >=2 | >=12,800 | 36 h+; needs tile/cartridge strategy |
| A candidate with **1 moving part per cell** | 1 | 6,400 | 18–53 h — the reliability-first target |

**Rule of thumb.** Every extra printed part per cell adds ~6,400 parts and **~18–53 hands-on hours**
at 10–30 s each. The reliability-first program should push toward **<= 1–2 cell-level parts** and use
**detachable 10x10 cartridges / replaceable tiles**, never monolithic gluing. Part-count reduction
is both a reliability *and* an assembly lever.

### Per-cell failure and the 99 %-perfect-map goal

From the program's own reliability model
(`06-experiments/test11_falsification_library/reliability.py`):

```text
P(perfect map) = (1 - q)^6400
q needed for 99 % perfect map  = 1 - 0.99^(1/6400) = 1.570e-6
zero-failure independent trials for a one-sided 95 % bound at that q = 1,907,667
```

| Per-cell error q | P(all 6,400 correct) | Expected bad cells/map |
|---:|---:|---:|
| 1e-2 | 0.00 % | 64 |
| 1e-3 | 0.17 % | 6.4 |
| 1e-4 | **52.7 %** | 0.64 |
| 1e-5 | 93.8 % | 0.064 |
| **1.57e-6** (99 % goal) | **99.0 %** | 0.01 |

**Consequences for the reliability-first design (the core of DND-104 §2):**

1. **No small coupon can *demonstrate* q <= 1.57e-6.** 1.9 M zero-failure trials is unreachable in a
   prototype. Therefore the architecture must provide **detection + bounded recovery**, not just a
   low nominal failure rate.
2. **Silent microscopic failures are the enemy.** A mechanism whose correctness depends on a tiny
   printed spring, a sub-mm friction contact, or a pawl engagement force (S6-LC A2: uncertain by 8×)
   has an **unpinned** q. The reliability-first program explicitly prefers **large positive
   engagement, hard stops, compression-loaded structures, and generous clearances** — each of which
   makes q observable and recoverable.
3. **Recovery must be priced.** One whole-board scan allowance (~$35) plus a re-write of the affected
   region is the cheapest credible recovery path. Carrying **no** recovery line (as S6-LC did, $0 by
   design) means a single missed cell silently corrupts an entire map at q = 1e-4.
4. **Correlated faults dominate.** One warped tile, one misaligned head, one shared-drive fault
   invalidates per-cell independence. Model these as **module/bank events**, and prefer
   **individually testable / replaceable modules**.
5. **Per-cell bought hardware with a 0.1 % reject rate** already adds ~6 bad cells per board
   (0.64 expected at q=1e-4) *and* consumes the entire cost allowance — double death. Zero per-cell
   bought hardware is a reliability requirement, not just a cost one.

### Replaceability / tile strategy

- Design at **10x10-cell (or 8x8) cartridge/tile granularity** so a failed region is swapped in
  seconds without disturbing neighbours (regional-update requirement).
- **Individually testable repeated parts**: a cell or bank must be cycle-testable off the machine.
- **Positive hard stops** everywhere a printed spring would otherwise set force or height.
- **Dry-cleanable, serviceable** interfaces; no adhesive-permanent cell assembly.

---

## 5. Per-class screening verdicts (for the DND-104 convergence)

| Mechanism class | Cost verdict | Printability verdict | Reliability verdict |
|---|---|---|---|
| **Per-cell motor/solenoid** | **DEAD** ($7.7k–$28k) | n/a | many bought moving parts |
| **Per-row writer bank** (S5 legacy) | **DEAD** (40 solenoids = $178, plus fixed base > ceiling) | ok | 40 bought actuators, silent misses |
| **Global lift + per-cell passive latch** (S1/S6-LC family) | **conditions**: 1–3 motors, 0 per-cell bought -> fits; must price reset carriage + mask + medium + splice honestly | pawl leaf at 0.45 mm = **RISK**, needs fine nozzle or redesign to >=0.88 mm | needs **detection + recovery**; passive pawl hold-force must be gated |
| **Planar threshold memory + shared strokes** (S2) | plausible **if** 64 addresses and tile couplers are printed; a bought per-tile part at $3 = $192 | tile media printability unproven | fewer repeated moving parts; media consumable must be flagged |
| **Multi-row DMA / dense head** (S3) | **DEAD** (320 bought selectors >= $1,600) | n/a | many bought actuators |
| **Shared-bus tiles** (S4) | **conditions**: 64 printed clutches; a bought coupler at $3 = $192 | fixed stop geometry is 0.4 mm-friendly | testable modules; good recovery |
| **Novel mask/punch/tape classes** (DND-106/107 outputs) | must carry a **media consumable line** and a **shared writer** line | punched media is outside FDM | mask-generation latency must be separated from visible-transition time |

**Bottom line for the program.** The reliability-first candidates that can pass cost are the ones
with **zero per-cell bought hardware** and **few shared actuators**. The two things most likely to
kill them are (a) a **hidden per-cell or per-tile bought part**, and (b) a **consumable medium**
costed as "printed". Printability only survives ordinary 0.4 mm geometry if structural features stay
>= 0.88 mm, standalone >= 0.44 mm and webs >= 0.45 mm — otherwise the candidate is a fine-nozzle /
resin candidate and must say so.

---

## 6. Provenance and limits

- **Sourced-class** = a defensible current retail class for the part (usually a marketplace range),
  consistent with the repo's existing [sourcing_notes.md](../../test11_cost_printability_reliability/sourcing_notes.md)
  (2026-09-28) and [bom_s6lc.csv](../../../08-integrated-designs/s6lc-low-cost/bom_s6lc.csv). Individual `sourced-live` URLs are in those
  files; this envelope does not re-scrape them.
- **No purchase, no print, no measurement** ([DND-27](/DND/issues/DND-27)). Prices are point-in-time
  and volatile; re-verify before any procurement.
- **Delivered uplift** is the repo's additive ×1.16 ([DND-41](/DND/issues/DND-41)), not a
  multiplicative convention.
- **Verified by** [`cost_envelope_checks.py`](cost_envelope_checks.py) (arithmetic + threshold gate;
  no external dependencies).

**Next test:** for each converged DND-104 candidate, substitute its actuator/media/per-cell counts
into this envelope and require (1) working delivered <= $250, (2) zero per-cell bought lines, (3)
no `printable_excluded` flag on a motor/valve, and (4) every structural feature >= 0.88 mm or an
explicit fine-nozzle declaration.
