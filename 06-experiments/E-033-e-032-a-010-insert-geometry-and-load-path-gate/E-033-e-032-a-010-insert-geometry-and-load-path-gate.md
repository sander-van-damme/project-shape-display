---
status: active
builds-on: [E-032, E-031, A-010, A-011, E-018]
---

# E-033: A-010 insert geometry and load-path gate

## Disposition and evidence boundary

This package closes a nominal analytical/CAD definition for the A-010
axle-free translating cartridge inside the frozen E-032-G1 5x5 coupon. It is
dimensioned enough for an independent falsifier to identify contact points,
clearances, and measurements. It does not select A-010, validate hardware, or
claim process capability.

Evidence labels in this document are deliberate: E-032 and E-018 values are
**sourced repository interfaces**; dimensions in the insert tables are
**design assumptions**; script outputs are **calculated**; the SCAD model is
**CAD/geometry-derived**; no values are physically measured; force, material,
friction, compliance, wear, reader margin, and actuator capability remain
**unresolved**.

## Frozen common interface (unchanged)

The A-010 insert uses E-032 configuration `E-032-G1` without changing its
common frame or protocol: 40.00 x 40.00 x 3.00 mm frame, 5.08 mm pitch,
20.32 mm centre span, 25.40 mm active envelope, F1/F2 Ø2.00 mm at
(-15,-15)/(15,15), north D+ witness 2.00 x 6.00 mm, south 32.00 x 2.50 mm
clamp land, centre R0 3.00 x 3.00 mm, and W0 at x=-10.16 mm. The reader is
not a seating datum. The five-state names, witness coordinates, event chain,
0.20 mm reseat/writer and 0.10 mm isolation limits remain E-032 limits.

## Insert definition

XY origin is the E-032 active-field centre. Z datum is the frozen frame upper
face, `z=0`; positive Z points toward the reader. The cartridge footprint is
30.48 x 30.48 mm, centred on the active field, leaving 9.52 mm total nominal
frame margin (4.76 mm per edge). The 25 sliders are repeated at the 5.08 mm
cell centres. A row/column slider is independently addressable; the SCAD
file shows all 25 representative sliders in state S2.

| Layer, bottom to top | z range | nominal dimensions / function |
|---|---:|---|
| lower guide | 0.00..0.40 | 30.48 square; 4.50 x 4.90 guide pockets; captures slider laterally |
| gate slider | 0.40..0.80 | 4.20 transverse x 4.60 travel envelope x 0.40; one 3.00 square aperture |
| upper guide | 0.80..1.20 | 30.48 square; same guide pockets; prevents lift/skew |
| five-stop plate | 1.20..2.00 | 30.48 square; 3.40 square follower openings and five shelves at 0.80 pitch |
| follower / shoulder | 2.00..4.00 | Ø1.20 follower, Ø3.00 x 0.35 broad shoulder; representative only |

The guide pocket gives 0.30 mm total longitudinal running clearance and 0.30
mm transverse clearance relative to the slider. The five gate aperture
centres are `x = -1.60, -0.80, 0, +0.80, +1.60 mm` from each cell centre;
these are S0..S4. The aperture/follower nominal diametral difference is 1.80
mm. The stop shelves are 0.60 mm wide in travel and separated by 0.20 mm
nominal relief; the stop plate, not the slider, defines the settled Z state.

The writer interface is the common W0 channel. The representative tongue is
4.00 x 1.00 x 0.80 mm, engages a 0.60 mm-deep slider tab, and has a 4.00 mm
commanded stroke: 3.20 mm S0-to-S4 travel plus 0.20 mm approach/settle at
each end. Parked tongue clearance outside the frame edge is 0.20 mm. These
are envelope inputs, not actuator or fit results. A bidirectional tongue is
required; a one-way writer would not close the return path.

## State reach, return, and service path

The analytical command sequence is S0→S1→S2→S3→S4→S3→S2→S1→S0, then its
reverse and S0↔S4. Every transition must record writer contact, selected stop
identity, settled return, and the E-032 reader event chain. The geometry
requires 0.80 mm indexed travel per state and 3.20 mm extreme-to-extreme;
it does not establish the E-032 9 ms timing screen.

For service, first unload every follower and park the writer, then remove the
reader head from its declared 2.00 mm nominal standoff, release the two
non-datum side clips, lift the upper guide/stop subassembly vertically at
least 2.60 mm, and withdraw the cartridge vertically from the frame datum.
The 2.60 mm lift is a removal envelope, not a claim that a fixture exists.
The north D+ and south clamp lands, fiducials, R0, W0, and witness positions
remain untouched. Reinstallation is down to z=0 against D+, then south clamp;
F1/F2 transform and the E-032 <=0.20 mm residual gate are mandatory.

## Section / free-body load path

For a downward follower load `Fz` at R0, the intended reaction chain is:

```text
follower shaft (Fz ↓)
        │
        ▼
Ø3.00 shoulder (z=2.00) → five-stop shelf / stop-plate body → lower guide/frame
        │                         (direct compressive reaction)
        └─ Ø1.20 shank passes through selected 3.00 gate aperture
           (radial clearance; no vertical contact in the nominal section)

writer tongue → slider tab → gate slider / guides only (state-setting force)
```

The gate face is intentionally not a reaction surface: the Ø3.00 shoulder is
above the stop plate and the Ø1.20 shank has 0.90 mm radial nominal clearance
to the 3.00 aperture. The independent falsifier should inspect the section
for any contact at a gate face, guide lip, slider edge, or aperture corner
under the declared load. Any such contact fails load separation even if the
state still reaches.

The section is a geometry-derived force-path hypothesis. Unresolved inputs
are applied `Fz` and lateral load components, shoulder/stop contact area,
stop-plate and guide material modulus/strength, layer adhesion, flatness,
slider friction, writer force, post buckling/tilt, clamp preload, contact
compliance, debris/wear, and fixture stiffness. No stress, deflection, or
force capacity is calculated because those inputs are absent.

## Reproducible checks and tolerance-derived bounds

Run from the repository root:

```sh
python3 06-experiments/E-033-e-032-a-010-insert-geometry-and-load-path-gate/analysis/a010_insert_gate_check.py
openscad --export-format binstl -o /dev/null 06-experiments/E-033-e-032-a-010-insert-geometry-and-load-path-gate/cad/a010_insert_gate.scad
./repo check
git diff --check
```

The script calculates nominal state travel (3.20 mm), writer stroke (4.00
mm), layer stack height (2.00 mm before follower), edge clearance, and the
following explicitly bounded analytical exercise: ±0.10 mm each for guide,
gate, and stop placement gives ±0.30 mm residual budget; the nominal radial
aperture/follower margin is 0.90 mm, leaving 0.60 mm calculated residual
margin. This is a declared tolerance bound, not a measured distribution or
process capability. The script also checks the 0.20 mm E-032 writer and
reseat screens where geometry can state them.

## Falsifier observables and unresolved closure

An independent falsifier can pass/fail the definition by checking: all five
hard-stop identities are reachable and returnable in both directions; the
writer has 0.60 mm tab engagement and 0.20 mm parked clearance; no gate face
carries follower load in section/FBD evidence; the cartridge remains within
the frozen frame/fiducial/reader/writer/witness envelope; and the assembled
stack can be removed by the stated unload/lift path. The E-032 physical gates
still additionally require measured writer clearance >=0.20 mm, transformed
reseat residual <=0.20 mm, adjacent displacement <=0.10 mm, complete reader
event chain, and 1,000 state-changing records.

Unresolved: actual layer/process capability, friction and writer force,
follower load and lateral disturbance, stop/guide compliance and material
properties, reader optical/electrical margin, timing, debris/wear, fixture
stiffness/preload, and whether the nominal stack can be fabricated and
assembled without warpage. Consequently this package closes geometry for
falsification only; it does not close A-010 selection.
