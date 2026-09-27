# Historical evidence audit

Inspected 2026-09-27: root README, design target, test guide, template source and
parameters, framework tests, all test00–07 READMEs and mechanism source files,
archived document/spreadsheet content, and the archived micro-stepper datasheet.
Historical experiments were not modified. These are designs, not physical test
records: there are no measured friction, cycle-life, full-map timing or procurement
results establishing product compliance in the inspected files.

| Experiment | Actual mechanism/evidence | Useful contribution | Scaling issue |
|---|---|---|---|
| 00 pneumatic multiplexer | SolidPython generates binary-pattern aperture layers; 80 mm module, 16×16 outlets at 5 mm | Binary addressing and low-cost motor research | Apertures are not sealed, qualified valves; no pressure dynamics, leakage, cell locking or full-map schedule |
| 01 threaded rods | OpenSCAD/BOSL2 screw/nut variants: 2–4 mm diameters, 1–2 mm lead, 50–70 mm length | Passive screw memory, calibration geometry | Thousands of drives or a slow shared drive; printed fine threads and thrust support unqualified |
| 02 Python cubes | 4×4 SolidPython geometry, nominal 5 mm pitch, 50 mm sliders, dimensional sweep | Explicit clearance coupons | No actuation, holding or reset mechanism |
| 03 threaded actuator | 4 mm screw, 2 mm lead, 6 mm body, slotted drive head; frames/calibration parts | Shared screwdriver interface | Body alone exceeds pitch; engagement and complete update time absent |
| 04 plain cubes | 4.64 mm columns and 0.44 mm guide walls at 5.08 mm, 45×45 frame; pump-pressure coupon | Earlier work already targets appropriate pitch | No complete actuated/locked system; pump coupon is not a measured seal result |
| 05 grid/cubes/rod | 4.4 mm hollow body, 3.2 mm screw, 3 mm lead; 45×45 grid | Screw variant near target density | Nut wall/clearance and shared drive not qualified; no full-scale timing |
| 06 sandwich detent | 1×5, 8.5 mm pitch, 6 mm columns, 30 mm stroke, 5 mm steps, one sliding comb | Flat load-bearing tooth, common release | One rising column cams the entire comb: other cells on that comb can release; shrinking pitch is not a scale transform |
| 07 capped grid/caddy | 5×5 at 8.5 mm pitch; one comb per row; flexible rods; schematic feeders; two servo ranks | Separates large actuators from cell pitch; accessible row modules | Per-row comb isolates other rows, NOT other columns within the same row. Two ranks at target pitch provide 10.16 mm against 12.6 mm servo width; need ≥3. Tube OD is 5.1 mm against 5.08 mm pitch. No closed-loop rod-length measurement |
| template | Serial XY–Z travel sum, ideal discrete heights | Reproducible lightweight framework | No retraction, physical reset, acceleration or contact solver. `all_columns_locked`, zero error and zero collisions are assigned. Optional backends only import/version-check packages |

The three archived `shape-display-dev.odt` files have identical content XML
(SHA256 `e0376492ffa31e80114bf9cef9332680fca1fbe16fe3ede2a7372dc09f575c0d`).
The three `multiplexing-layout.ods` files also match
(`4c054428c527fa63efcdafc9e96f41ceceae5367213e21c8e6c8085ad0176ee1`).
They contain the earlier architecture comparison and bit-selection layouts,
not three independent experimental validations. Old 50 cm / 200×200 / four-hour
assembly aspirations are superseded by the current target and current request.

The archived PM08-2 datasheet says 8 mm diameter, 18° steps, 3.3 V, 40 ohm phases,
5 gf·cm pull-in torque, and response above 800 pulses/s **without load**. The
components note instead suggests 5–6 V and 0.12 A. Use the datasheet's 3.3 V
for this hypothesis; do not silently combine voltage, price and torque claims
from possibly different surplus motors. The quoted old €0.52/pair is not a
2026 delivered-price guarantee.

Retain: passive memory, square tiling, calibration coupons and shared actuation.
Discard as evidence: render appearance, ideal simulator flags and unsupported
claims that a comb or feeder “works well.”
