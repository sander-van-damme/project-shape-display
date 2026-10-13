---
status: complete
builds-on: [E-178, E-259, E-261, E-267]
---

# Screw-pin readback must retain structural support and pay for access

**Retain coarse, supported optical bays as a conditional comparator; stop direct
transplantation of E-178 and thin-polymer continuous-slot detail.** Under the
examined support layout, the previous free-field local-reveal maximum23.97s
becomes39.52s. This is a reported tradeoff, not automatic product rejection.
No camera, architecture, scale process, print or purchase is selected. E-263's
print offer is retired after owner feedback; supported CAD remains a comparator.

Reproduce `python3 tools/curated-experiment-checks/E-268/readback.py` and
`python3 tools/curated-experiment-checks/E-268/support.py`. Evidence: finite ideal
specular rays, algebraic fault injection, elastic beam bounds and scheduling
calculations; self-review, no physical qualification. Errors, loads, stiffness
and acquisition rates are scenarios, not calibrated FDM/optical distributions.

## Observe the pin, not merely the drive

| Observation | Useful detection | Uncovered fault / obligation |
|---|---|---|
|Motor encoder|Motor turn error|Missed socket, transmission slip, stripped thread|
|Resident screw angle|Missed socket if actually read|Wrong lead, stripped thread, pin not following|
|Top camera|Visible terrain displacement|Miniature covering the entire top; more cameras cannot see through it|
|Actual pin scale at fixed datum|Wrong stationary height, slip and missed drive when visible/calibrated|Detached mark, wrong-cell/stale frame, later support failure|
|Shared contact probe|Actual contacted position|Physical access, probe travel, contact-induced movement and time|

Executable10→20mm/lead2 witnesses: five motor turns with zero screw turns leave10;
five screw turns with a stripped thread also leave10. Both alias successful motor
counts. A detached mark can still report20 while the terrain is10. Invalid,
occluded or stale readings become **unknown**, never last-known success. Cell
identity, fresh frames, integral marking, batch registration and contrast remain
obligations; these witnesses establish no detection probability.

The resident load path remains pin→thread→screw→thrust bed throughout writer
docking/withdrawal. No E-178 auxiliary pickup lock exists here. Correct height
cannot establish future retention or moving-loss arrest; neither does that
limitation automatically require4096/6400 extra brakes or support sensors.

## Finite optical route through the actual beds

E-261 lower guide center is z=S+5mm,2mm thick, with an upper guide40mm higher.
Put the scale datum at z=S+9,3mm above the lower guide. For stroke40/50, pin-local
coordinate `S+7−u` covers7…47/57mm on existing86/96mm stock: no added tail length.
Marks and guide wear/drag remain unresolved; print texture is not a scale.

Marks face+Y on4.4mm square pins. A shared45° strip sits midway between rows at
y=p/2 and reflects toward a camera at global z=−10, centered on16 columns.
Camera-to-datum height is59/69mm. Lenses, lighting, mounts, docking-tip clearance,
strip seams and board-edge access remain unbuilt.

Each scenario checks16,384 rays:16 columns, tracks±.4/±1.2mm, footprint corners
±.08mm and64 combinations of row-strip Y/Z, camera Y, pin-face Y, pupil-edge and
mirror-angle signs. Pupil Y radius.25mm and tilt±.5° are allocations. Independent
or coherent batch offsets are allowed, not iid yield assumptions. Finite mirrors,
swept pin/neighbor envelopes and both slab faces are checked. Corner sampling
does not certify nonlinear intermediate poses or image quality.

Strip half-projection/backing are.2/.1mm fine and.5/.2mm coarse. Both pin and
mirror may shift by e. S40 results, including tilt even at e=0:

|Pitch / e, mm|Backing-to-pin gap, mm|Mirror misses|Incoming envelope hits|Optical slot, mm|Guide web each side, mm|
|---|---:|---:|---:|---:|---:|
|5.08 /0|.068|0|0|.450|−.005|
|5.08 /.05|−.032|0|8192|.666|−.113|
|6.35 /0|.330|0|0|.454|.628|
|6.35 /.10|.130|0|0|.885|.412|
|6.35 /.20|−.070|0|0|1.400|.155|

Negative gap is a physical envelope collision even when rays clear. Fine e=.10
also has wrong-side mirror rays. Backing-clearance breakpoints e≈.034/.165mm are
not manufacturing tolerances. Wider5.6mm stems cannot inherit the narrow-stem
result. E-261's.24mm guide clearance alone permits.12mm lateral play; e=.10 is
not established for the built assembly. Envelope hits are conservative access
failures, not proof every pixel is dark. Narrower pupils or different reflectors
are changed designs; no microscopic mirror optimization is warranted yet.

Unmodified guide/thrust plates obstruct the view. An explicit ray crosses solid
material between4.64mm guide apertures; occupied screw holes are not optical
windows. The alternative needs slots through **both lower guide and thrust bed**.
Slot includes ray intersections plus independent plate registration e;
`web=(pitch−slot−4.64)/2`. S50/coarse/e.10 needs.887mm slot/.411mm webs.
Continuous slots break cross-row support; these webs are geometry, not strength.

## Supported bays: structural and optical costs together

Stop slots at transverse ribs between16-column bays. Pin load passes through
resident thrust seats into perforated row strips, then end ribs and a grounded
frame. Upper guides can remain unslotted. Proposed1mm ribs fit the coarse1.71mm
gap between4.64mm apertures, leaving.51mm after opposing.10mm edge errors; the
fine grid's.44mm gap cannot fit them. **Rigid ends are only a model assumption:**
transverse-rail bending, grounded frame, attachments, writer transit, thrust
collars and openable joints remain unconstructed.

A16-cell/101.6mm row with.90mm slots is5.45mm wide. Allocated3.6mm circular journal
holes leave minimum net width1.85mm. Compute simply supported center displacement
from discrete equal cell-center forces with `integral(M*m/(E*I),dx)` and
`I(x)=net_width(x)*t^3/12`. The [AWC beam formulas, figures1/7/8](https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf)
provide constant-section controls; wood properties are not imported. This beam
approximation excludes local hole deformation/stress concentrations, seat
pressure, shear, creep, anisotropy, joints and support settlement. Large results
flag small-deflection breakdown, not a precise deformed shape. Solid and minimum
net-section controls bracket this calculation, **not hardware compliance**.

|Cells / assumed E MPa / thickness mm|Deflection at.05N/site, mm|Solid–minimum-section controls, mm|
|---|---:|---:|
|16 /1000 /2|5.136|3.011–8.872|
|16 /3000 /2|1.712|1.004–2.957|
|16 /1000 /4|.642|.376–1.109|
|16 /1000 /6|.190|.112–.329|
|16 /200000 /2|.0257|.0151–.0444|
|8 /1000 /2|.323|.189–.557|

E1000/3000 are polymer scenarios; E200000 is a metal-like control, not a sourced
stock specification. At.02/.2N per cell, multiply by.4/4. These are sensitivities,
not typical miniature loads: even.02 everywhere totals81.92/128N at4096/6400
sites, including actual pin self-weight. Thin polymer strips are poor stiffness
candidates in these scenarios; shorter spans or metal address this compliance
without adding moving locks. A.05mm illustrative budget is not a product gate:
the metal case meets it at.05N/site but not.2. Guide4.64mm square holes instead
leave.405mm webs; guide reaction/registration needs its own model. Circular
thrust-hole results cannot qualify guides or unchanged-neighbor displacement.

Finite-ray recheck: camera centered in bay, end ribs1mm wide, independent.10mm
X allocations for ray/registration; thrust thickness2/4/6 grows down from z=+1.
Lower guide stays2mm, camera z=−10. S50 slots become.8873/.8901/.8930mm; checked
16-column end-rib margin3.772mm (8 columns2.434mm). S40 also clears the sampled
ends. The.90mm slot is near the optical envelope, **not a manufacturing
recommendation**. Adding.20mm width reduces guide webs to.305mm and thrust net
width to1.65mm. Collars, screws, mounts, dirt, lens quality and actual slot
fabrication remain unqualified; thicker bed means a changed seat assembly.

An interior crossbar has an explicit ray-intersection witness. A freely sliding
16-output writer therefore cannot inherit an unobstructed full-width camera
field across every support boundary. Tested alternative: align writer/reader
with fixed bays and select only changed outputs. This is a sufficient restricted
policy, not proof every cross-boundary ray fails. Extra cameras, separate reader
motion or alternative relays are changed systems with unpaid cost/time.

## Resolution, stopped verification and recovery

Five-level/four-track E-178 code is not a continuous sensor. Six10mm setpoints
need≥3 bits;51 integer-mm positions≥6, before fiducials/redundancy. A hypothetical
1600px/101.6mm view gives9.45px per.6mm track, not qualified contrast or accuracy.
Narrower tracks spend registration margin. Scales must survive guide wear without
thousands of manual calibrations; no marking process is selected.

With acceptance half-width a and bounded reading error e, accepted true error
can reach a+e. Illustrative a=.3/e=.2mm can accept.5mm error; e=.35 exceeds a.
A10mm missed move is distinguishable under these bounds; tiny slip is not.
Stop/read/compare/retry uses the valid actual height, not replay of the original
delta. Persistent unreadable/jammed channels remain unaccepted. Later failures,
repeated retries, revisits and full-board homing are not covered by one retry.

A final image does not replace active control: at assumed850rpm/lead3,10/20ms
latency adds.425/.850mm before braking; at2000rpm,1/2mm. Keep head feedback/end
margins budgeted until active stopping is earned. Neither image nor motor brake
establishes future hold after power loss.

## Full-system timing, manufacture and cost

Replace E-267's20ms proof slot, never double-charge it. Free16-field coarse
S40/S50 maxima at20/50/100/200ms are18.61/22.61,19.12/23.12,19.97/23.97 and
21.67/25.67s. Fine values:33.91/43.32,35.11/44.54,37.11/46.59,41.11/50.69s.
Coarse worst visits16 stations;80ms extra costs17×.08=1.36s including retry.
These are conditional rates, not acquisition measurements. At100ms two full-row
heads give17.94/21.94s coarse and20.75/25.69s fine but need128/160 drives and8/10
simultaneous fields, versus16 drives and one field.

**Adding support boundaries changes that comparison.** At assumed850rpm/lead3,
100ms read, same133 nonempty four-square windows per depth:

|Pitch / stroke mm|Free16 field, s|Fixed16 bays, s|Fixed8 bays, s|
|---|---:|---:|---:|
|6.35 /40|19.97|31.75|31.50|
|6.35 /50|23.97|39.52|39.26|
|5.08 /40|37.11|50.58|64.44|
|5.08 /50|46.59|64.22|82.79|

Seeks, return,4s common allowance and one immediate retry are paid. Fine-grid
numbers are scheduling controls only, lacking this rib/optical clearance. Coarse
fixed16 leaves128/126 windows≤30s atS40/S50, versus all133 with free fields;
maximum individual penalties12.28/16.05s. A two-cell boundary reveal needs two
stations instead of one. Some fixed routes improve the travel heuristic, so
penalties are evaluated per case. Coarse fixed16 large-scene maxima179.25/208.66s;
cold neutral196.06/256.53s remains separate. Three annotated maps are scenarios,
not measured representative play. No safe RPM or30s gameplay pass is claimed.

The board retains4096/6400 resident pairs and8192/12800 guide apertures. Two
slotted layers add512/800 row spans; joining their ends in16×16 panels gives
32/50 panels total. Grounded support-grid locations25/36 and transverse rail
lines5/6 are **locations, not a built frame**. Unchanged screws share elastic
supports, so neighbors may move under changed loading despite fixed screw angles.
Slots do not grant regional-isolation qualification.

Scales still require4096/6400 marked faces. Two≤203.2mm mirror pieces per row
mean128/160 pieces,26.01/32.51m total strip, before seams/mounts. Ten seconds
manual marking per pin alone costs11.38/17.78h. Batch marking, molded features,
laser processing or outsourced scales need real production/repair evidence.
Laser-cut/machined metal support or molded guides may concentrate precision in
shared parts, but burrs, warp, flatness, bearing wear, seams and pair replacement
remain unpaid. Bonding a stack that traps failed pairs is not the assumed service
route. No per-cell sensor or extra latch is added.

Inherited coarse16 dated motor/driver subset plus **unquoted** reserve is$497.68,
leaving$2.32/$502.32/$1002.32 against$500/$1000/$1500. All optics, structural metal,
frame, scales, docking, feedback and transmission share this remainder. The
coarse two-row-head control starts$984.64. No complete BOM, price floor, finished
retail price or purchase authority follows. Shorter spans have a latency cost;
metal has an unquoted fabrication/service cost.

**Next discriminator:** compare a cross-bay actual-pin observation route with the
supported fixed-bay control, including grounded frame and acquisition cost,
before camera/reflector detail. Batch marking stays unqualified. No owner print
or new question blocks this independent work; E-263 remains retired.

Verification: original262,144 ray samples plus114,688 supported-bay samples;
reflection/path identities, finite slabs, opaque-top and interior-rib witnesses,
fault aliases, stock/error controls; constant-section point-load closed form,
solid/net envelopes,400→800 samples/cell (<.005% circular-hole change), zero-load
and E/t scaling;1176 signed-cell replays, two-cell boundary witness and exact
proof-slot/retry replacement. Scheduler accepts a station-builder callback;
default behavior retains E-267's checks. These validate calculations, not optics,
mechanics, process yield or physical safety.
