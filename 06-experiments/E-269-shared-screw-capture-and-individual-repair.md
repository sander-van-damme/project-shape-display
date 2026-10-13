---
status: complete
builds-on: [E-268, E-261, E-260]
---

# Shared screw capture permits local service, but frame ribs obstruct the reader

**Keep coarse capture/service as conditional geometry; park the present optical-frame
combination.** A shifted shared keeper releases an intact pair while neighbors retain their
fixed downward load paths. Fine-pitch optical cutouts disconnect retaining patches. Coarse
full-span frame ribs block a required raised-target stereo view. An opaque frame is a control,
not a qualified machine or reader. No print, purchase or selected head; E-263 remains retired.

From the repository root run `python3 tools/curated-experiment-checks/E-269/capture.py --check`
and `python3 tools/curated-experiment-checks/E-269/frame.py --check`; omit flags for scenarios.
Python + numpy. Evidence:
**bounded geometry, ideal service replay and linear statics**, self-reviewed; no process
measurements, force rating, safe speed, reliability or manufacturing qualification.

## Capture and service construction

Retain E-261's solid screw,4.4-mm square pin,4.64-mm intact guide openings,54/64-mm usable
thread and86/96-mm pin for S40/S50. In thread-origin coordinates:

- Fixed bed z−5…−3 has3.6-mm journal holes. Drive end≤3.2 diameter ends at z−7;
  its socket strength remains unconstructed.
- Integral collar diameter4.4 at z−3…−1 seats on the fixed bed. No separate clip.
- Keeper z−.8…+.8 has .2-mm axial float. Each opening is a radius1.8 capsule
  along y0…1.2 united with a radius2.4 service circle centered at y1.2.
- Shift keeper−1.2y to align service circle and screw. The3.2-mm neck fits throughout.
  Optical holes are registered only in the operating position, not during maintenance.

Downward path: pin→thread→screw→collar→fixed bed→frame, including service. Upward docking
path: collar→keeper→frame, only when locked. This keeper is not a thread brake. Float and
shared flex permit disturbance; fixed screw angle holding remains a separate physical duty.

Service, granting passive thread hold and an intact or jammed-but-straight pair: park and
de-energize the writer, clear the target miniature, keep the board horizontal and prevent
upward loads. Unlock/shift keeper; pull pin and engaged screw together without unthreading.
The4.4 collar clears the4.8 service circle and4.64 guides; the3.2 drive end clears the3.6 bed.
Lift94/104 mm to clear the upper guide at z86/96 with1 mm allowance; maximum pin top reaches
z222/252. Lower an assembled replacement, seat collar, restore/lock keeper, verify registration,
target and neighbors and locally correct height. No free homing or measured repair time.

All cells on the keeper temporarily lose upward capture, so service is not playable actuation.
Bent/fractured trapped screws, separated stripped pins, inaccessible grip, wide top caps and
displaced guides still require module access. A5-mm collar cannot pass4.64 guides; neither
blind collar enlargement nor forcing the part is a repair plan.

## Optical holes and connected retaining material

Reuse E-268's two.5-mm pupils at z−10, .2-mm bottom patch and independent±.1-mm optical bounds;
baseline2 mm coarse/.5 mm fine. Recompute envelopes through both faces of the relocated layers:

|Pitch, mm|Keeper optical diameter, mm|Bed optical diameter, mm|Neighbor ray margin, mm|
|---|---:|---:|---:|
|6.35|3.8872|3.0889|+.2112|
|5.08|2.2661|1.9276|−.1190|

S50 values. The bed retains the nominal collar footprint with .7457/.4283-mm ligament before
edge loss, not a stiffness pass. Pupils lie only3 mm below the drive-end plane; reader/driver
body clearance remains unpaid. The shifted bed also changes E-262 support; no RPM transfers.

A3×3 keeper kernel plus2-mm outer rim is rasterized: enlarge holes by pixel half-diagonal,
retain only whole solid squares and flood edge-connected material from the external boundary.
Count only whole collar-contact squares connected to that boundary. This is a sufficient
material subset, not a stress/contact solution or a tileable module; interior2-mm rims
cannot repeat without consuming pitch.

Fine openings overlap vertically by.32 mm (`4.2−(5.08−1.2)`); optical circles overlap adjoining
service circles horizontally by.6613 mm. Closed aperture chains isolate retaining material:
(±2,−.5) are solid collar witnesses but ungrounded. Raster finds zero grounded contact and
14.82 mm² isolated whole-cell material. Removing optics restores connected strips. Coarse
vertical gap is.95 mm and passes this connectivity test. This rejects the combined fine layout,
not every fine-pitch keeper.

Let a expand every hole and shrink collar radius; r independently bounds lateral registration
per axis, shrinking the guaranteed collar disk by another sqrt(2)r. These are correlated
competing bounds, **not X1C priors or independent-cell yield**:

|a/r, mm|Grounded whole-cell contact, mm²|Midpoint estimate, mm²|Step, mm|
|---|---:|---:|---:|
|0/0|2.0347|2.4001|.040|
|0/0|2.2249|~2.40|.020|
|.10/0|.7740|1.1155|.040|
|.10/.05|.5359|.6882|.020|
|.10/.10|.1567|.2965|.020|
|.20/0|0|0|.040|

At a=.20 the radius2 neck opening contains the contracted radius2 collar exactly: no capture.
Neck/service radial clearance is independently only.20 mm; hole inward error, part growth and
registration consume it. Edge-loss contact results do not prove insertability. Under assumed
uniform pressure, nominal contact centroid y−1.343 gives1.343F Nmm eccentric moment; a2-mm
journal alone would need.671F radial reaction per edge (.0336/.134/.671 N at F.05/.2/1 N).
Pressure redistribution, binding and deformation remain unknown; contact area is not a rating.

At4096/6400 sites retain that many thread pairs, integral collars, journals and drive duties,
plus8192/12800 guide apertures. Add4096/6400 keeper openings and the same number of optical
holes in **each** keeper and bed; no private spring/cartridge/fastener. Gross406.4-square keeper
at1.6 mm is.264 L, .713/2.074 kg at assumed2700/7850 kg/m³ before holes/rim. It exceeds the
X1C256-mm bed; sheet cutting/machining, molding or tiling need actual process/assembly evidence.
Ten seconds cleanup per keeper opening adds11.38/17.78 h, before optical holes. E-260's pair
assembly/inspection costs remain. Shared movement does not erase thousands of fit duties.

Capture checks:294 service states,35,329 neck boundary points, independent negative-y release
witnesses, fixed-keeper/wide-collar failures, exact aperture chains and .04→.02 contact-grid
refinement with midpoint agreement within.04 mm². These qualify only the stated model.

## Full-span frame control: straight ribs conflict with the optical construction

**Stop the combination of these ribs and the present interstitial stereo route.**
The opaque keeper remains a structural control, **without qualified actual-pin readback**.

Construction control: put a fixed rib along x in every inter-row pin corridor, at y halfway
between row centers. Its bottom is z1, above the keeper top z.8; its upper face is z21 for
20-mm depth. The keeper slides freely below it during powered-off service. Coarse ribs are
1 mm wide; all pin heights occupy at most the same4.4-mm lateral envelope. Nominal side
clearance is .475 mm; independent .1-mm pin expansion and .1-mm rib positioning bounds leave
.275 mm. The fine control needs .4-mm ribs even to retain .14-mm nominal clearance; the same
bounds give−.06 mm. These are competing bounds, not process capability or a chosen tolerance.
Do not thin the fine ribs or pins to rescue this control.

At each end, each rib seats under a removable common cap in an external end beam. The two end
beams connect to four external corner posts. Positive seats carry upward load; the common caps
retain ribs. This is a proposed accessible assembly route, not a manufactured joint or stiffness
proof. A matching lower rib layer at z−25…−5 can ground the fixed thrust bed's downward loads;
its socket/body clearance and bed bending remain to be constructed. It does not require a
mount at each cell. Upper-guide support, end-beam joints, frame torsion and broken-part module
access remain unresolved; intact-pair extraction still fits between the upper ribs.

Service-lock concept: an external keeper tab slides1.2 mm in a peripheral guide. A removable
transverse pin through the tab and fixed bracket locks either operating or service position;
separate bracket shoulders set the two stops. A second external guide prevents skew. Allocate
at least1.4 mm travel with±.1-mm placement bounds. The lock remains outside the terrain and
writer envelope and carries in-plane registration duty; it cannot substitute for upward rib
support. No actuation is allowed until the keeper is seated, locked and registration checked.
Pin/guide clearance, force rating, electrical interlock and human access are unqualified.
No per-cell clip is added, and the lock does not establish passive thread holding.

**Optical counterexample:** at coarse pitch, one nominal entrance pupil is
(x,y,z)=(2.468,3.882,−10), looking at pin-bottom(2,2,52). At z1 the ray has y3.548,
inside the rib's y[2.675,3.675] and x span. Thus one required stereo view is blocked even with
nominal perfect parts. With E-269's full pupil/error corners,20/32 raised-target ray samples
intersect the rib, versus0/32 at the lowered target. These are geometric samples, **not**
probabilities or percentages of usable pixels. The fine control blocks16/32 raised samples
and already fails its pin-clearance bound. An intact ray at low height cannot establish
full-travel sensing. Opaque plates intentionally remove the interstitial route altogether;
encoder counts alone still alias failed engagement/stripped threads. Moving pupils, notching
all ribs or a different reader would be a new construction and are not credited here.

### Force and replication consequences

Grant a central contiguous16-tip head and .2 N upward docking force/tip; also test .05 and1 N.
The force is an assumed insertion scenario, **not miniature weight or measured docking load**.
Two neighboring ribs take the row load; half to each is an optimistic sharing case and all to
one is a sensitivity control. Grant simple end supports, linear elastic ribs,10×20-mm external
end beams, grounded corner posts and zero keeper/contact/joint deformation. Integrate point-load
beam responses and add end-beam displacement. No stiffness credit from the sheet is taken.
E=70,000 or1,000 N/mm² are inherited material scenarios, not a selected stock specification.

|Pitch / rib width×depth, mm|Tips|E, N/mm²|Half-share rib, mm|End beam, mm|Sum, mm|
|---|---:|---:|---:|---:|---:|
|6.35 /1×10|16|70,000|.3724|.00479|.3771|
|6.35 /1×20|16|70,000|.04654|.00479|.05134|
|6.35 /1×20|64|70,000|.1199|.01917|.1390|
|6.35 /1×20|16|1,000|3.258|.3355|3.594|
|5.08 /.4×20|16|70,000|.1176|.00479|.1224|

For the coarse16-tip/20-mm metal case, all load on one rib gives .09788 mm including the end
beam. If one *illustratively allocates* .05 mm to these beams, the maximum modeled force is
.195 N/tip under half sharing or .102 N/tip under one-rib loading. This is **not a safe force
budget**: local keeper bridges/contact, eccentric collar loading, rib lateral stability,
seat/cap/post compliance, strength, creep and dynamic insertion are unpaid. Nor is .05 mm a
product disturbance requirement. The two nominal gaps already allow .2 mm collar float plus
.2 mm keeper-to-rib lift; the half-share case totals .451 mm before missing deformation.
Neighbor movement through shared flex remains unqualified. Lowering rib depth to10 mm trades
half the stock for eight times the rib bending; replacing metal with an assumed polymer modulus
is not supported by this control. Nominal stress is not a strength acceptance.

At64/80 rows, **one** rib layer adds63/79 long members and126/158 end seats/cuts, versus4096/6400
private mounts. Two layers double these to126/158 members and252/316 seats. At assumed density
2700 kg/m³, the coarse1×20 upper layer alone weighs1.383 kg; matching lower ribs double that
before end beams, posts, keeper, bed and guides. The fine .4×20 layer is .693 kg but fails the
stated lateral bound. Common end caps avoid one fastener per rib only if their distributed
retention and assembly are actually demonstrated. Four fasteners per cap is an allocation,
not a strength result; four caps for two layers imply16 fasteners before frame/guide mounts.
At1 minute handling per rib, two layers add2.10/2.63 h; at5 minutes,10.5/13.17 h. No measured
assembly time or stock quote is claimed. Saw-cut strip and machined end-combs are feasible
process hypotheses to cost; flatness, burr removal, batch fixtures and repair remain duties.

The opaque control deletes8192/12800 optical holes across keeper and bed, not4096/6400 keeper
openings, thread pairs or journal seats. It trades the current readback access for a clearer
support route. The earlier$497.68 subset+reserve leaves$2.32/$502.32/$1002.32 below the
$500/$1000/$1500 comparison tiers for **all** missing hardware. Neither rib stock nor a
replacement reader is quoted, so no price winner follows. S40/N20 and S50/N30 retain real
up/down travel and paid neutral preparation; no timing improvement is calculated. The earlier
21.67/25.67-s local and234.28-s S50 scene estimates cannot transfer to the obstructed reader;
282.23-s neutral preparation and403.17-s dense stress remain conditional references only.

**Decision:** park this full-span rib + interstitial-view combination and further keeper optical
refinement. Retain the opaque shared-frame control without calling it a finished architecture.
Before another head/keeper detail, resolve actual-pin observation at architecture level against
this solid support/control; a clear ray that requires weakening every support is insufficient.
Use a genuinely different readback placement or operating sequence and count its preparation,
neighbor disturbance and fault coverage. No new print, purchase or owner question is justified
by these calculations.72 curvature-integration cross-checks, force balance, linear force/cubic
depth scaling and the independent nominal ray witness check the model; they do not qualify it.
