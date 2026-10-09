---
status: candidate
builds-on: [P-008]
---

# Magnetic toggle memory with mechanical shared lifting

**Bounded; priority survivor for selector-field investigation.** Descriptors:
coincident row/column magnetic pulses; bistable magnetic flag memory; shared
mechanical elevator; ground pawl load path; prismatic columns and rotating
flags; two flags/collets and a pawl per site. This is not an XY magnetic writer:
no external magnet lifts or travels from site to site.

Two small permanent-magnet/ferromagnetic over-centre flags command a moving
tail collet and a stationary pawl-release dog. Crossed row/column conductors
with local flux returns add subthreshold fields at their intersection. Scan
one row, pulse selected columns to set flags; reverse polarity resets them.
A shared cam supplies the work to close collets and withdraw unloaded pawls;
the flags only route the cam, so miniature force need not be magnetic holding
force. Detents keep flags stable without current. Separate set/reset commands
and verified flag state are required, not an address-bit-only decoder.

Elevator collets clamp long tails at arbitrary initial heights, unload pawls,
reset changed columns to zero in a down sweep and lift them to requested teeth
in an up sweep. Reinsert ground pawls, proof support, release collets and
reset flags. Unchanged cells never engage release dogs. Ground frame/pawls
support miniatures; elevator motor provides both motion directions. Tail track
must cover roughly 80 mm relative travel plus collet length. A nominal 2-mm
flag in a staggered layer leaves guide space, but no swept packaging proof
exists. Flux returns consume real volume; uniform 40-mm lifts accumulate all
column load, not just flag force.

Repeat 12,800 magnetic flags, collet/pawl interfaces, magnets or magnetized
inserts and local pole pieces; share approximately 320 row/column drive lines
for two arrays, reversible pulse drivers, cam/elevator and optical reader.
Neighbor fields, remanence, coil resistance variation and magnet/air-gap
spread determine half-selection. E-063 gives a necessary threshold window in
5/9 bounded error cases; the middle case has only a 1.353–1.478 normalized
nominal threshold interval. No field solution establishes those errors.
An ideal 1-mm² pole at assumed 0.1–0.3 T supplies only 0.004–0.036 N;
0.1–0.5-mm air gaps need roughly 8–119 ampere-turns per local gap, before
leakage/steel reluctance. The flag must route a powered cam, not retract a
loaded pawl. Stored gap energy is only 0.0025–0.115 J/6,400 sites, but copper
loss and shared-field leakage are unbounded; no electrical-power claim follows.
At $250 reserve, two bought magnets alone must average below $0.0195 each
before pole pieces/electronics; this is an allowance, not an available price.

Read underside tail height and flag fiducials; support-proof unloading tests
actual pawl closure. A mismatch inhibits shared motion. Retry the relevant
set/reset pulse once; retain grip and stop/repair the module on persistence.
A false flag read can unlock an unintended pin: use a mechanical normally
closed release dog and check unchanged heights after each shared cam event.
Field/common-read faults require module isolation, not repeated pulsing.

The E-065 air-core cost/assembly mutation explicitly closes conductor loops
and evaluates arbitrary column masks over 80×80 sites. Seven of nine nominal
geometries retain a scalar threshold window; only three 2-mm-return cases
survive tight ±0.05-mm registration / ±5% current / ±5% threshold scenarios.
All cases fail the middle/wide scenarios. At 0.8-mm row standoff, the best tight
window is 0.1864–0.2106 mT/A; this is not finite-flag switching evidence.
Stop failed air-core cases under those bounds. The original local flux returns
remain unresolved: with 15% intended-field and threshold errors, a conservative
circuit must limit total parasitic projection to <6.125% of one intended field
contribution. A generated guided circuit or measured tighter spread can reopen
that gate; higher current alone cannot repair overlapping intervals.

The direct two-array circuit requires 320 reversible lines/160 dual H bridges;
no complete affordable strip BOM exists. Retain the tight air-core and guided
routes conditionally, but complete the pressure/electroadhesive discriminators
before further magnetic detail. Later work must couple actual finite-flag
torque, detent, layer isolation and strip cost; compare a simple mechanical
coincidence flag. No long-term magnet force, miniature support, manufacturing
yield or lifetime claim follows from the abstract toggle sequence.

E-074 opens a distinct guided-reluctance/soft-armature mutation with a finite
assumed double-well detent. Of 48 bounded gap/stiffness/current/leakage cases,
31 retain quasistatic command windows but only 20 retain the lossless single-
pulse window. This is an ideal gap/energy screen, not a field or detent model
for the original permanent-magnet flag. A soft pole's force is quadratic in
current: reversing current does not reset it. Continue with explicit opposed-
pole reset versus signed magnetic torque and mechanical coincidence; count
reset hardware, repeated half-select dynamics and cam routing. No static-window
survivor is accepted as a complete selector.
