---
status: candidate
builds-on: [P-010]
---

# Thermal unlock-only selectors with shared mechanical motion

**Bounded; long-wire and serial-row embodiments screened out.** Descriptors:
row-enabled transistor/current channels; thermal contraction selecting a
mechanical dog; mechanical pawl memory; motor elevator energy; ground-pawl
service support. A resistive polymer cantilever could replace SMA but has no
validated force/temperature bounds here; it remains a lead, not a second
complete architecture.

At each pin, a short SMA wire retracts an unloaded pawl-release dog; a global
cam and selectively engaged collet provide lift/unload, 40-mm bidirectional
motion and reseating. Spring reset follows cooling; neither SMA nor its hot
mount carries terrain service force. Use the dual-support selected reset/up
sequence, with collets held until wire cooling, pawl seating and proof. A
second mechanically stored collet-enable flag is programmed before cam motion;
if SMA sets both flags sequentially, charge both pulses and reset time. The
fast one-wire calculation does not hide this additional channel burden.

Digital row-enable and column data with per-site transistor isolation prevent
sneak heating. Simple passive half-voltage matrices are not accepted: quarter-
power heating accumulated across scans can still release adjacent sites.
Unchanged pawls stay engaged; shield thermal paths at seams. Tail/flag optical
readback and proof unload precede collet release. Failed cooling retains grip
and stops that module; a broken wire defaults the ground pawl closed. Replace
wire/terminal cartridges from below. Thermal common bias and stuck-on drivers
remain dangerous until detection/temperature limiting is implemented.

A 0.050-mm wire nominally fits vertically at pitch. At assumed 4% working
strain, 0.2/0.5/1-mm release needs 5/12.5/25-mm active length, excluding crimps.
Dynalloy's current guide gives 500 ohm/m, 85 mA for roughly one-second heating,
0.4-second LT cooling in static air, and about 0.353-N heating pull. These
manufacturer conditions do not transfer to densely packed PLA supports.
Subtract spring return/friction before comparing to 0.05-N release demand.

At least 6,400 wires, 12,800 terminals, switches/isolators, collet flags and
pawls repeat. One pulse/site uses 116/289/578 J/board. All-parallel wire current
would total 544 A at low voltage; series groups/regulated drive trade current
for voltage and selected-site bypass hardware. Eighty serial 1.4-s rows need
112 s before movement. Parallel thermal time alone need not exceed 30 s,
but complete switching, power distribution and cooling have not passed.

Public guide ranges imply wire-only lower scenario $192/$480/$640 for the
three lengths (32/80/160 m); termination, waste and drivers are excluded.
Reject 1-mm stroke on wire alone and 0.5-mm stroke with a $250 shared reserve.
Keep only short-stroke/bistable mechanically reset selector exploration if a
complete cost and thermal-isolation model changes that decision. No print.
Sources: [wire data](https://dynalloy.com/technical-data-wires/) and
[price guide](https://dynalloy.com/flexinol-actuator-wire-price-guide/), accessed
2026-10-08; guide ranges, not quotes.
