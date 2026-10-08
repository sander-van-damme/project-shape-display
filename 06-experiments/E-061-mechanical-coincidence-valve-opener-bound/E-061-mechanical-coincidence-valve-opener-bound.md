---
status: complete
builds-on: [E-060]
---

# Mechanical coincidence can remove hydraulic half-selection, conditionally

Continue A-014 with a normally closed chamber-side poppet operated by a
floating equal-arm beam; stop refining its two-series-fluid-gate embodiment.
This calculation establishes a nonempty bounded kinematic window, not a
pitch-compatible mechanism, seal qualification or architecture selection.
Input main `f94b693`; reproduce with
`python3 tools/curated-experiment-checks/E-061/coincidence_bound.py`.
No sourced process priors, physical measurements, CAD or contact simulation.
All dimensions, forces and uncertainty intervals below are exploratory bounds.

## Operating principle and complete transition

Two independently guided endpoint shoes follow row and column rails. A rigid
beam rests on both shoes; sliding/rotating end contacts accommodate tilt.
A separate light follower preload must maintain both contacts before the beam
reaches the poppet. The beam center pushes a guided stem after a lost-motion
gap g. A closing spring and a pressure-assisted seat isolate the chamber when
the stem is untouched. Supply/return plumbing is outside that single seat:
there is no address-dependent intermediate cavity connected to the chamber.
Pressure differential is assumed to assist closure; reversed differential
requires a bidirectional closing-force design and is not covered here.

Sequence: deselect row, change columns, stabilize pressure, select row, meter
flow, deselect row, verify height. No simultaneous row handoff: overlapping
rows would intentionally open unwanted intersections. Center height is the
mean endpoint height. With either endpoint low the stem stays untouched;
with both high the valve opens. Monotone transitions bounded by those endpoint
heights cannot overshoot the half-select height in this quasistatic model.
Closing returns the seat before the center enters its half-select range.
The moving cell is pressure-supported while open; arbitrary lowering needs a
controlled return/backpressure path. Closed cells depend on seat sealing and
trapped-fluid stiffness. Spring reset, follower preload, seat debris, friction,
dynamic overshoot and a stuck-high rail remain real failure mechanisms.

## Bounded synthesis and sensitivity

Let each endpoint position error be ±e, gap error ±eg, and load-dependent
lost motion/compliance be 0…f. These are adversarial intervals: common print
bias, rail bias, and opposite local errors are included, without probabilities.
For required opening lift L, robust isolation/opening requires
`s/2+e+eg ≤ g ≤ s-e-eg-f-L`, hence `s ≥ 4(e+eg)+2(f+L)`.
Signed negative stem travel means clearance, not physical negative valve lift.

The deterministic grid uses s=1/1.5/2/2.5/3 mm and
g=0.75/1/1.25/1.5/1.75/2 mm. With L=0.3 mm, 30 candidates per
scenario give 8, 5 and 0 survivors for (e,eg,f) respectively
(0.05,0.05,0.1), (0.1,0.1,0.2), (0.2,0.2,0.4) mm.
Rejected points fail isolation and/or opening; no yield follows. The last
scenario needs s≥3 mm and exactly g=1.9 mm at that minimum: its grid rejection
is **not** a topology impossibility. Zero margin is not a practical selection.
This is parameter synthesis of one topology, not three new architectures.

A separate interior point s=2.5, g=1.6 mm under the middle bounds gives:
00 signed travel −2.0…−1.4 mm; either half-select −0.75…−0.15 mm;
11 lift 0.5…1.1 mm. Thus 0.15-mm half-select clearance and 0.2-mm
minimum lift margin over L. The poppet must accept the maximum 1.1-mm travel;
a hard travel stop would otherwise overload the rails. A 4-mm rigid beam at
worst endpoint differential 2.7 mm has only 2.9513-mm horizontal projection:
end shoes need 1.0487-mm total inward sliding accommodation. Fixed vertical
pivots would overconstrain it. Beam thickness, contacts, crossed-rail routing,
seat and seal packaging at 5.08-mm pitch have NOT been checked. This geometric
constraint is a next-step discriminator, not a CAD acceptance.

## Force, scaling and decision

For pressure-assisted seat diameter d, closing differential p, spring force Fs
and valve drag Fd, opening force is `p πd²/4+Fs+Fd`. Each equal-arm endpoint
carries half; one line operating 80 open valves carries 40 times that force.
The 36-case grid d=0.5/1/1.5 mm, p=0.1/1/1.5 MPa,
Fs=0.1/0.5 N, Fd=0/0.5 N gives 4.785…146.029 N per line.
At d=1 mm, p=1.5 MPa and Fs=Fd=0.5 N, that is 87.124 N.
This omits rail friction and follower preload and is not a drive rating;
rail deflection must fit the assumed endpoint/lost-motion bounds. Both rails
rising equally satisfy work conservation. Force sharing presumes symmetric
contacts and no binding; failure of that assumption invalidates this bound.

The change removes intermediate-volume charge transfer only if the chamber
seat stays closed. It replaces 12,800 series seats with 6,400 chamber seats,
6,400 beams and stems, 12,800 sliding endpoint contacts plus follower/closing
preloads, and still 160 shared input lines. It trades fluidic isolation trouble
for repeated mechanical contacts and substantial shared forces. E-060 fluid
volume, flow, compliance and leakage bounds still apply. No cost or <30-s
claim follows: differing heights need metering/readback and may require
serial or grouped scheduling. Recovery needs detection of drifting/half-selected
cells and cartridge isolation; false acceptance remains unbounded.

Next discriminating work is actual swept geometry and shared-rail compliance
for a modular crossed-rail cartridge, including preload, 1.1-mm valve travel,
reverse-pressure closure and common-cause deflection. Reject that embodiment
if packaging or force cannot retain the kinematic margins; reopen with altered
mechanical advantage, rail support or valve topology. Do not print yet: geometry
can cheaply invalidate the current survivor. Keep A-013 and the other A-014
lock-hybrid possibility as comparators; no replacement of demonstrated hardware.

Self-review: exhaustive binary/error corners, independent interval inequality,
zero-stroke and nominal/error counterexamples, rigid-beam projection and
virtual-work check pass. These checks assess the reduced model only. No time
integration, mesh, probability estimate or independent review is claimed.
