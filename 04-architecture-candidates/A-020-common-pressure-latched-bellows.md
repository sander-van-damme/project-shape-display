---
status: candidate
builds-on: [M-015]
---

# Common pressure with mechanically latched bellows

**Bounded; rolling-diaphragm route remains conditional after E-064.** Descriptors:
magnetic/mechanical local release flags; positive rack height memory; common
air chamber energy; individual bilateral ground latches supporting service load; guided
prismatic caps on sealed corrugated diaphragms. No per-cell flow valve, piston
sliding seal or trapped volume stores height. This differs materially from
A-014's hydraulic memory.

A proposed molded/formed array of 6,400 corrugated or rolled fingers shares
one/few plenums. E-064 distinguishes these membrane motions.
Each finger carries a guided cap/rack. Common pressure pushes all caps upward;
only selected unloaded latches release, while others hold position. Stop/re-latch
selected caps at their target using tail readback. For downward transitions,
first balance pressure against the local load to unload selected latches, open
them, then reduce pressure so local return springs pull the selected caps down;
latches reset at target. Local force imbalance makes that transfer unresolved.
Independent magnetic flags (A-016 principle) route shared release cams;
E-065 constrains that selector and does not qualify it. Capture
requires speed limiting and an emergency catch; uncontrolled spring return is
not accepted. Pressure ramps must fit both raising and lowering force windows.

Service load goes through engaged latches to the distributed frame. Unchanged
regions do not unlock, though varying pressure loads their locks and can
elastically disturb them. A continuous flat taut membrane spanning neighboring
0/40-mm caps would need approximately 694% additional segment length at
5.08-mm spacing; reject that sheet embodiment. Corrugations or deep rolled
fingers supply stored area, but 40-mm deployment at a 3-mm bore is unresolved
geometry, fatigue and manufacture, not a printed-PLA diaphragm claim.

For a 3-mm effective diameter, 0.05/0.2/1/10 N net force needs at least
7.1/28.3/141/1,415 kPa differential before spring/friction. Set pressure for
*motion*, not 10-N service support; a 0.2-N motion assumption gives 1,280 N
aggregate cap force and about 4,673 N gross reaction over a 406.4-mm-square
plenum lid. Return springs and variable bellows stiffness determine whether
that assumption is possible. Housing, guides, relief and pump flow must carry
this burden. 40-mm stroke displaces 1.81 litres over all 3-mm bores; pumping it
in 10 s needs 10.9 litre/min geometric flow, excluding compression/leakage.

Repeat diaphragms, springs, pawls, flags and guides, but no bought cell valves.
Shared pump/regulator/pressure readback, flag drivers and underside scanner
remain. A puncture is a common-pressure fault; isolate at replaceable small
module plenum, keep ground latches engaged and repair the membrane. Position
mismatch retains the nearest reachable latch; flag/pressure fault inhibits
release. Proof support and unchanged-height scans catch false captures only
within reader limits. Pumps and molded-sheet tooling have no qualifying BOM;
$0.0391/site residual at $250 reserve is a budget threshold, not a price.
E-064 rejects the tested sinusoidal fold grid under explicit 10% bending/20%
hoop-cycle scenarios. A rolling U-fold preserves meridian length across 40 mm
travel, with a ~61-mm skirt sweep. Inverse synthesis gives the necessary pitch
bound `60.5t+12e+w <= 2.54 mm` for those strain allowances (film thickness t,
combined radial error e, sleeve wall w). A 25-µm film, 0.05-mm error and
0.4-mm wall require 5.025-mm pitch; 20% thicker film requires 5.630 mm and
fails. These are unqualified material/process scenarios, not PLA capability.

The marginal rolling witness with bounded spring/drag/hysteresis and 0.2-N
payload needs ~68.5 kPa raising pressure, ≤8.42 kPa for guaranteed return,
and ~11.3 kN gross lid reaction. Its full-board swept volume is 2.90 L. No
complete timing/BOM passes. A one-way ratcheting pawl would let unchanged
cells rise under pressure: bilateral retention, governed motion, release
unloading and capture overlap are mandatory unresolved mechanics. End flanges,
spring/reader packaging, film fatigue, seals and pressure-frame stiffness also
remain open. Stop the failed sine embodiment; retain rolling only conditionally
on improved cyclic-film/manufacturing evidence or changed geometry. Complete
the other cross-physics discriminator before another pressure detail study.
No printing or pump procurement follows from this analytical result.
