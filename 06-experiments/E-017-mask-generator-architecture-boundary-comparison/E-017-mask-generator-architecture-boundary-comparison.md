---
status: active
builds-on: [Q-010, P-009, DES-002, DES-003, DES-004, A-010]
---

# Analytical comparison: complete mask-generator boundary

## Question and boundary

This is a calculation and architecture screen, not a hardware test. The
minimum complete generator for an arbitrary-map product must include the
state-bearing medium, a writer, media transport or clamping, registration,
verification, fault handling, and the consumed/reusable media path. A prepared
mask, offline serial writer, or stock of masks is not free machinery.

The comparison uses the current 80 x 80 reference field (6,400 cells), 5
visible levels, 5.08 mm pitch, and a 30 s arbitrary-map target. A 5 x 5 cell
tile is the regional-update unit unless otherwise noted. These are inherited
screening assumptions, not product validation.

## Architectures screened

| Class | Operating principle | Complete arbitrary-map product? | Main reason |
|---|---|---:|---|
| Reusable prepared masks | Select and clamp a pre-made perforated/profile mask from a library | No | The library is a finite prior map set; arbitrary maps require an uncosted preparation process |
| Consumable serial writer | Raster-write a disposable sheet, then register and read it | Conditional only for slow/prepared mode | One channel cannot meet the current full-field bound; media, waste, registration, and writer faults are recurring costs |
| Prepared cassette | Exchange a rigid cassette containing a complete mask or tiles | No for arbitrary on-demand maps | Cassettes make transport/serviceable media, but do not generate a new unseen map |
| Buffered media | Keep several prepared masks or a queue ahead of the display | No as a boundary | Buffering hides expected latency only; an unanticipated map still needs a generator or consumes a prepared cassette |
| Reusable rewritable tiled medium with parallel writer | Clamp a reusable 4-plane binary mask (or equivalent 5-state code), write changed tiles, register on fiducials, verify after writing | Yes, conditional | This is the smallest complete boundary that preserves arbitrary-map capability and regional updates; media wear and channel yield remain open |

The surviving class is a product boundary, not a selected detailed geometry.
It can be implemented with A-010-style replaceable planar cartridges or a
different reusable mask, but it cannot omit the writer, fiducials/clamp,
reader, transport/unload sequence, or retry path.

## Channel and information-throughput accounting

For a direct five-level mask, use four binary aperture planes as the explicit
conservative encoding. (A 3-bit code is possible but adds invalid-code and
correlated-channel handling; it is not used to make the comparison look
cheaper.) The reference field therefore contains 25,600 plane-cell writes.

DES-003 supplies the current analytical rate anchor: eight travelling
writer/reader head positions and a conservative 71 cells/s/head lower rate.
The parallel reusable boundary writes the four planes in one addressed
engagement, so the lower-rate full-field write term is:

`Twrite = 6400 / (8 x 71) = 11.27 s`.

This is a geometry/rate calculation from the existing candidate assumptions,
not a measured mask-write rate. With one writer channel, four serial planes
would require `4 x 6400 / 71 = 360.6 s`; even a single direct 5-state serial
code would require at least 90.1 s at that rate. Serial writing is therefore
rejected for the 30 s arbitrary-map mode before media overhead is added.

## Complete sequence and latency bounds

The following conservative accounting makes previously omitted work visible.
It assumes local clamping of the active reusable tile, fiducial registration,
readback of every changed cell, bounded retry, and no global reset.

| Operation | Full arbitrary map | One 5 x 5 regional tile | One 20 x 20 region |
|---|---:|---:|---:|
| map encode/queue | 0.05 s | 0.05 s | 0.05 s |
| media select/transport/clamp/register | 1.50 s | 0.50 s | 0.75 s |
| parallel write at 71 cells/s/head | 11.27 s | 0.044 s | 0.704 s |
| verify changed cells | 5.864 s full-field anchor | 0.023 s proportional bound | 0.366 s proportional bound |
| settle/release | 0.50 s | 0.10 s | 0.20 s |
| retry allowance | 1.00 s | 0.006 s | 0.060 s |
| **analytical total** | **20.18 s** | **0.72 s** | **2.13 s** |

The full-field verification anchor is retained from DES-003; regional
verification is a proportional calculation, not a claim that a reader can
actually maintain that rate. If a regional change requires a full-cassette
transport/register cycle, add up to the full 1.50 s registration allowance;
the local-update totals then become 1.72 s (5 x 5) and 3.63 s (20 x 20).
If a four-plane writer is accidentally serialized, the full-field bound is
already over 360 s before verification. The 20.18 s result therefore has
about 9.8 s analytical margin to 30 s, but only under the parallel-channel,
local-clamp assumptions.

## Physical completeness and fault accounting

| Required subsystem | Minimum boundary item | Fault that must be detected or contained |
|---|---|---|
| medium | reusable four-plane tile/cartridge with wear/service limit | tear, creep, blocked aperture, plane mismatch |
| channels | four independent plane writers per addressed engagement, with parked-safe state | missed stroke, double stroke, channel dropout, cross-plane skew |
| transport | unload/reseat or local clamp and a positive mechanical datum | half-seated tile, drag, jam, neighbour disturbance |
| registration | at least two fiducials plus hard edge datum per tile | accumulated pitch error, skew, seam offset |
| verification | read every changed aperture/state after settle | wrong map, unreadable contrast, stale media |
| recovery | bounded retry, quarantine/replace tile, and fail-safe display hold | repeated miss, torn media, reader disagreement |
| consumables | replacement media plus cleaning/wear allowance | finite life silently becoming a reliability loss |

No architecture passes if it relies on visual inspection alone, treats a
prepared mask as an input with zero time/cost, or cannot identify a failed
write before the load is released.

## Purchased-component cost model

Costs below are engineering allowances and allocations, not supplier quotes;
3D-printed parts, print material/time/failures, and labour remain excluded as
in ADR-005. Use DES-003's documented $370 purchased baseline as the shared
display, gantry, reader and controller starting point. Add only the mask
generator boundary items:

| Class | Incremental purchased items that cannot be omitted | Analytical cost form | Product implication |
|---|---|---:|---|
| prepared reusable/library | mask set, storage and selection hardware | `Cbase + Cset + Cselect` | finite-map accessory, not arbitrary generator |
| consumable serial | writer, sheet stock, feed/registration, reader, waste/spares | `Cbase + Cwriter + Cfeed + Creader`; plus `Csheet/map` per update | slow and recurring cost; fails 30 s at current rate |
| cassette | cassette frame, fiducials, latch, inventory of prepared media | `Cbase + Cframe + Cinventory` | arbitrary only after adding a writer |
| buffered | all cassette or writer items plus buffer storage and duplicate media | `Cbase + Cwriter + Cbuffer + Cmedia` | reduces expected wait, not worst-case arbitrary latency |
| surviving reusable parallel | reusable four-plane tiles, clamp/fiducials, four writer channels, verification and service stock | `370 + Ctile + Cclamp + C4write + Cservice` | minimum complete boundary; every term requires a BOM before procurement |

ADR-005's $370 is not a mask-generator quote. This table deliberately does
not invent prices for unresolved writer heads, media stock, or cartridge
hardware. Sensitivity is decisive: any architecture that requires one
serial writer or a finite prepared-mask inventory fails on timing or
arbitrary-map completeness regardless of a low initial purchase price.

## Unknowns and cheapest falsification

The highest-value unresolved assumptions are parallel four-plane write yield,
tile registration after removal/reseat, media wear/cleanability, reader
classification margin, and loaded-neighbour disturbance during local clamp.
The cheapest credible test is one 5 x 5 final-pitch reusable four-plane
coupon with two fiducials, a clamp, one writer channel per plane, and a
frame-fixed reader. Apply adversarial maps (all-zero/all-four, checkerboard,
single-cell changes beside loaded dummies) for 1,000 write/verify cycles.
Record channel misses, invalid plane combinations, registration error,
reader margin, clamp/reseat time, media damage, and adjacent displacement.
This falsifies the boundary assumptions; it does not qualify life or board
reliability.
