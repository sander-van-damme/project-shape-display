---
status: complete
builds-on: [E-178, E-259, E-261, E-267]
---

# Actual screw-pin readback needs a structural optical route

**Retain a coarse-grid, fixed-datum scale as a conditional shared-reader option;
stop direct transplantation of E-178 into the screw array.** A camera below the
board cannot see through the guide/thrust beds. An explicit slotted-bed route
has a geometric window with narrow4.4-mm stems at6.35-mm pitch, but its structural
support, marking process and optical performance remain unbuilt. Do not buy a
camera or add thousands of sensors on this evidence.

Reproduce `python3 tools/curated-experiment-checks/E-268/readback.py`.
Evidence: finite ideal specular rays, bounded geometry, algebraic fault injection
and inherited scheduling calculations; self-review, no hardware qualification.
Error boxes are scenarios, not measured FDM distributions. E-263's optional
manual article remains useful and unchanged. No new print or purchase.

## Observe the pin, distinguish it from the drive

| Observation | Useful detection | Uncovered fault / obligation |
|---|---|---|
| Motor encoder | Motor turn error | Missed socket, transmission slip, thread failure |
| Resident screw angle | Missed socket if the angle is actually read | Stripped thread, wrong lead, axial motion not following angle |
| Top camera | Visible terrain displacement | A miniature can cover an entire top; more cameras cannot see through an opaque base |
| Actual pin scale through fixed datum | Missed drive, slip, wrong lead and stationary wrong height when visible and calibrated | Detached scale, stale/wrong-cell image, broken support that fails later |
| Shared contact probe | Actual contacted height | Access, force-induced movement, independent probe travel and time; not a free substitute |

Executable witnesses command10→20mm at lead2: five motor turns with zero screw
turns leaves10; five screw turns with a stripped thread can also leave10. Both
can report a successful motor count. A scale attached to the actual column
changes this observability, without adding a private encoder at every screw.
A stale/occluded reading must become **unknown**, never a last-known success;
source faults are constructed states, not detection probabilities or camera tests.
A detached mark can still report20 while the terrain is10. Batch registration,
cell identity, contrast, freshness and mechanically integral marks are required.

**Do not import E-178's old pickup/lock machinery.** The screw route retains
pin→thread→screw→thrust bed support throughout docking and withdrawal. There is
no auxiliary pickup to prove clear. A correct-height image cannot qualify future
holding, but that calls for physical retention/moving-loss qualification and
fault handling, not automatically4096/6400 extra brakes or support sensors.

## A finite route, including the plates it must cross

Use E-261's two shared guide planes: lower center z=S+5mm,2-mm thickness;
upper center40mm higher; pin86/96mm for S40/50. Put a scale datum3mm above the
lower guide's top at z=S+9. Local pin coordinate at the datum is `S+7−u`, so
40/50mm travel uses material coordinates7…47/57mm on the existing pin. **No added
tail length** is needed in this construction. Surface marking and its influence
on guide friction/wear remain unresolved. Continuous print texture is not a code.

Marks face +Y on a4.4-mm square pin. A shared45° strip sits midway between rows,
at y=p/2, and reflects toward a camera at global z=−10mm, below the screw bed.
The camera reads16 columns, centered along that group; nominal camera-to-datum
height is59/69mm. Camera/lens/lighting, docking-tip clearance and mounts remain unbuilt;
strip seams and board-edge access still need construction.

The source checks16,384 rays per error/stroke scenario:16 columns, four tracks,
four footprint corners, and64 combinations of row-strip Y/Z, camera Y, pin-face Y,
pupil-edge and mirror-angle signs. Tracks at±.4/±1.2mm use±.08-mm footprints.
Pupil Y radius.25mm and angle±.5° are allocations, not an available lens rating.
It checks finite mirrors, reflection/path identities, incoming swept corridors
and outgoing finite neighbor boxes. Independent
and coherent row/batch offsets are allowed; there is no iid yield extrapolation.
Corner sampling does not certify all nonlinear intermediate poses or image quality.

A strip half-projection of.2/.5mm in Y is used for fine/coarse pitch, with.1/.2mm
normal backing thickness respectively. The moving pin and mirror may each shift
by e. Mechanical clearances include both shifts and mirror rotation. For S40:

| Pitch / e mm | Minimum mirror/backing-to-pin gap mm | Mirror misses | Incoming envelope hits | Required optical slot width mm | Remaining guide web per side mm |
|---|---:|---:|---:|---:|---:|
|5.08 /0|.068|0|0|.450|−.005|
|5.08 /.05|−.032|0|8192|.666|−.113|
|6.35 /0|.330|0|0|.454|.628|
|6.35 /.10|.130|0|0|.885|.412|
|6.35 /.20|−.070|0|0|1.400|.155|

All rows retain±.5° angle and the finite pupil, including e=0. Envelope hits are
conservative access failures, not evidence that every pixel is dark. Negative
mechanical gap is an explicit collision envelope. Fine-grid e=.10 also places
some target rays on the mirror's wrong side. Coarse e=.20 shows why optical rays
alone can pass while the physical backing collides. Wider stems spend this space;
a5.6-mm stem at6.35 pitch cannot inherit the narrow-stem result. Narrower pupils,
different reflectors or specialized fabrication are changed designs, not ruled
out by this screen; no tiny-mirror refinement is warranted yet.

**The unmodified plates obstruct the view even in otherwise clear scenarios.**
The executable constructs a ray crossing the lower guide between its4.64-mm
square apertures: that region is solid. Screws occupy their resident thrust-bed
holes too; no optical transparency is implied. The slotted alternative requires
continuous openings along each observed inter-row corridor in *both* lower guide
and thrust structure. Slot widths above envelope ray intersections at both slab
faces, plus independent plate registration e. Web is `(p−slot−4.64)/2`, a nominal
remaining geometry before aperture error, strength or assembly margin. The fine
case consumes the web even at e=0 in this allocation. The coarse.10 case retains
~.41mm per side, but this is **not a structural pass**: long slots break cross-row
load distribution and leave perforated row strips needing grounded end/module
support. Wider slots for real optics, cables, fasteners or dirt reduce it further.
S50 requires.887mm/.411mm slot/web at coarse e=.10; same conclusion.
The symmetric backing-clearance breakpoints are e≈.034/.165mm for fine/coarse,
not manufacturing tolerances. E-261's nominal.24-mm guide clearance alone allows
.12mm lateral play; e=.10 cannot simply be adopted as the built pin envelope.

Thus slotted shared supports, per-row mirror alignment and integral scale
fabrication are the new system costs. Do not hide them in a camera price or cut
slots in a load-bearing article without a new support calculation. If they force
one precise relay per cell, stop this route and compare a different access topology.

## Resolution, control and recovery boundary

The original four-track/five-level code is not a general continuous sensor.
Six10-mm setpoints over50mm need at least3 information bits;51 integer-mm positions
need at least6, before redundancy, fiducials and error detection. These are
information bounds, not a manufactured scale. Narrower tracks reduce registration
margin. At a hypothetical1600 pixels across101.6mm, a.6-mm track is9.45 pixels;
that arithmetic establishes neither contrast nor accuracy. Absolute scale or
image registration against known markings must survive guide wear and coherent
batch offsets without individual manual calibration.

For acceptance half-width a and bounded aggregate reading error e, true height
error can be as large as a+e. An illustrative a=.3/e=.2mm can accept.5mm true
error; e=.35 already exceeds the nominal a. These are explicit alternative
bounds, not a product tolerance or calibrated reader performance. A10-mm missed
move is distinguishable under such bounds; arbitrarily small slip is not.

Final observation supports stop/read/compare/local retry at the same station.
Recompute remaining displacement from an actual valid reading; do not replay the
original delta. A persistent unreadable/jammed channel leaves that region
unaccepted; unchanged cells retain their resident support ideally. One successful
image cannot prove long-term hold or arrest after power loss.

A final read alone does not replace active position control. At the conditional
850rpm/lead3, speed is42.5mm/s:10/20ms of delayed detection adds.425/.850mm before
braking. At E-259's2000rpm this is1/2mm. A shared reader could eventually control
motion if its rate and coverage are earned; its stopped-row acquisition allowance
is not such a guarantee. Keep reusable head feedback/physical end margins in the
budget until a controlled stopping scheme is built. No camera replaces a load path.

## Full-system consequences

The16-output head retains4096/6400 resident pairs and8192/12800 guide apertures.
This sensing construction adds4096/6400 marked faces,64/80 mirror rows and optical
corridors through two structural layers. Two≤203.2-mm mirror pieces per row imply
128/160 aligned pieces,26.01/32.51m total strip. One16-site camera field can follow
the short writer. Two simultaneous full-row heads need8/10 such fields if this
field size is retained; a larger shared view requires new optical coverage.
No per-cell electronics are selected. Ten seconds of manual marking per pin alone
is11.38/17.78 maker hours, before alignment/calibration; batch marking, molding or
outsourced scales need a demonstrated process and service route. These are labor
scenarios, not production estimates. Marks and strips must remain replaceable and
cleanable without disposing of a whole board.

Replace E-267's20-ms proof slot instead of charging it twice. At conditional
850rpm/lead3 with a single16-output head,133 nonempty local map windows per depth:

| Total stopped read allowance | Coarse S40 / S50 max s | Fine S40 / S50 max s |
|---|---:|---:|
|20ms inherited|18.61 /22.61|33.91 /43.32|
|50ms|19.12 /23.12|35.11 /44.54|
|100ms|19.97 /23.97|37.11 /46.59|
|200ms|21.67 /25.67|41.11 /50.69|

Seeks, drive, return, common4s and one immediate station retry remain included;
this is sensitivity, not measured acquisition or gameplay qualification. Coarse
worst windows visit16 stations: adding80ms costs17×.08=1.36s including retry.
At100ms, the same windows with B2/K32 full-row heads give17.94/21.94s coarse
and20.75/25.69s fine, conditional on simultaneous camera fields. They retain
128/160 drives and8/10 fields rather than16 drives and one field.
Cold neutral, large-scene and dense waits remain the minutes-long E-267 controls;
this reader does not accelerate them. Later detection needing a revisit, repeated
failures, full-board homing and optical setup are not covered by one retry.

At coarse16, E-267's dated motor/driver subset plus **unquoted** reserve is$497.68,
leaving$2.32/$502.32/$1002.32 under$500/$1000/$1500. All reader parts, marking,
structural corrections, feedback, docking and transmission must share that
residual; it is not a sensor-only budget or a complete BOM. The coarse two-row-head
control starts at$984.64 and repeats128 channels. No new catalog price, cost floor,
finished retail estimate or purchase permission is inferred.

**Decision:** retain the short coarse head and investigate optical access only at
the whole supported-module level. It can afford materially slower stopped reads
than20ms in these local scenarios; that removes urgency to source a fast camera.
The next independent discriminator is whether a slotted, openable shared support
module can retain screw thrust and guide registration with an optical corridor
and batch-manufacturable scales, compared with another actual-pin sensing route.
Do not begin camera selection or reflector micro-optimization first. Keep E-263's
manual support/holding test independent and optional.

Verification:262,144 sampled rays; independent reflection/path identities,
finite-slab and opaque-cover witnesses, fault aliases, stock/error bounds,
coarse-clear/fine-collision anchors and exact proof-slot/retry replacement.
These checks validate the model calculations, not an optical or mechanical build.
