# Minimal friction screw frame — print A first

**Status:** READY for physical prototype testing; no new part has been physically tested.

**Priority:** P1 `A-first.3mf`; P2 optional `BC-comparisons.3mf`.

**Reviewed:** 25 October 2026. No deadline, scheduled printing or follow-on work.

**Source:** current main `1071f695b93951246a2865038e7fb9de9bdf2a05`, [v3 diagnosis](../2026-10-23-low-friction-motor-frame/diagnosis.md), E-295/E-301/E-302. This implements the owner's new request; the older diagnostic is not a prerequisite.

[Printable assembly guide and results form](print-and-test-guide.pdf).

## 1. The decision

Does a shorter, low-contact frame move the same pin smoothly through 15 mm with the enclosure fully closed? Separately, do neighbors provide useful guidance without being dragged, and does horizontal printing help **functional** sliding/thread fit?

**Print [A-first.3mf](A-first.3mf) first.** It contains two frame halves and one integrated C-coupling/screw with two removable printing towers. Reuse the L motor, its successful side shim, ID3.2/OD7/0.50 mm washer, elastic bands and existing footless 40–50 mm pin with the same 4.4 mm square / lower 6 mm thread geometry. The 50 mm reference is shown in the drawing; a plain 18 mm pin is unsuitable for this frame's guide spacing. Do not print an entire replacement set.

| Saved X1 Carbon project | Contents | Bambu estimate, including preparation |
|---|---|---|
| **[A-first.3mf](A-first.3mf)** | 2 halves; 1 supported 30.6 mm rotor/screw | **2 h 20 min; 7.04 g PLA** |
| [BC-comparisons.3mf](BC-comparisons.3mf) | 26 mm stand; 9 manual pins; removable boundary; close-play plate; 8 short + 4 tall height spacers; 2 upright + 2 horizontal 18 mm reference pins; 1 sliding coupon | **4 h 28 min; 10.20 g PLA** |

The comparison plate is optional, independently usable and does not require nine motors. Small mass does not mean short print time: slender parts and the inherited conservative speeds/cooling dominate. Estimated times/material are slicer output, not physical measurements. The v3 *whole* plate was 4 h 59 min / 16.61 g, but included more parts; this is not an equal-content time comparison.

## 2. Saved printing conditions

Bambu Studio **02.08.02.61**, **Bambu Lab X1 Carbon / 0.4 mm / Generic PLA**, Textured PEI. Open the 3MF directly; no CAD export or setting entry is needed.

- Layer and first layer **0.12 mm**; nominal widths **0.45 mm**, **Arachne**, 2 walls, minimum bead 75%, minimum feature 10%. Five top/bottom shell layers; default 25% gyroid; screw, tall manual pins and orientation samples override to 100%.
- PLA **220°C**, bed **55°C**. Fan 100% after the first layer; inherited 8 s cooling threshold / 10 mm/s minimum speed. Auxiliary fan0%, exhaust70%; full settings are saved in `metadata/*-settings.json`.
- Outer/small perimeters **15 mm/s**, inner **20**, bridges **15**, first layer **15**; accelerations 1000 default, 500 outer/first, 1000 inner, mm/s². Cooling can reduce actual speed.
- Aligned seam, normal line interpolation, layer-by-layer order. XY contour, hole and elephant-foot compensation all **0**. No raft or automatic supports, including inside female threads.
- Frame halves flat back down; stand and boundary inverted on flat decks; screw upright with integral towers. Manual pins and upright coupons have 3 mm outer brims; horizontal coupons 2 mm; gap 0.12 mm. Other parts have no brim. Keep the saved poses, especially the horizontal pin's 90° roll before laying it down. Its local bridge angle is180° to cross the narrow bore; other objects retain automatic bridge angle.
- Screw tower contacts: **four 0.45 × 0.24 mm necks**, on the **external** thread. They must be clipped individually. No support contacts occur inside a pin. Contact cleanup and tall-pin adhesion remain physical risks, not slicer-certified successes.

Both archives were saved, reopened **without external profile files**, and resliced in Bambu Studio. Printer, settings, objects and overrides persisted. Both original and reopened toolpaths were checked separately; none contains automatic support or detached deposition islands. Seam/path ordering changes on reslicing, so G-code is not byte-identical. See [verification](verification.md) and [section drawing](images/assembly-section.svg).

## 3. Quick test

1. Follow [assembly.md](assembly.md). With power disconnected, fit the pin on the screw outside the frame; stop at any damaged thread or forceful fit.
2. Assemble without the motor first to observe both frame thrust stops. Then install the motor and check the same free axial float, PCB/wire clearance and full closure. The C fit must permit axial sliding; roof clearance alone is insufficient.
3. Turn gently at low, +3, +7.5 and +15 mm, both ways. Observe guides, screw bow, rotor contact and coupling stability. Repeat fully closed and briefly loosened. **A mechanism that needs loosening fails.** No deliberate lateral load or added weight during powered testing.
4. Compare with v3 using the same motor, pin, washer, shim, material and manual procedure. New screw length also changed, so improvement cannot identify one original rubbing surface by itself.
5. Only after smooth hand motion and no shaft movement/gear creep: a few slow 3 mm powered cycles, then up to the manually verified range, maximum 15 mm. Use the existing controller only when actual driver settings are known. No IRUN increase or firmware changes.
6. On the second plate, compare equal/staggered heights, missing neighbor, both play settings and boundary on/off. Then remove spacers and lay the stand on its side for **freely sliding neighbors in both directions**. This distinguishes neighbor drag from fixed-wall geometry. See assembly instructions.
7. Compare both copies of each orientation using the same bare reference screw and guide coupon. Test every exterior face. Reject damaged or catching internal threads regardless of a smooth-looking outside.

**Stop:** any binding, visible shaft displacement, gear migration/disengagement, rotor witness marks, pin bow, rubbing on PCB/wires, damage, support-removal scars that catch, or need to force/loosen the mechanism. Do not find a mechanical limit by running into it. Fill [results.md](results.md); blanks mean unknown.

## 4. Interpretation

| Physical result | Decision supported |
|---|---|
| A stays smooth closed at low and +15, coupling stable | Compact stack and local guides merit retention for this tested load/travel only. |
| Smooth without motor; binds with motor | C sliding/axis alignment remains limiting; do not compensate with current. |
| Smooth low; binds high | Record guide station, bow and witness marks. CAD clearance has not established usable high travel. |
| Rotor rubs the 0.6 mm land or shaft moves | No-contact hypothesis failed under that condition; no powered/load qualification. A deliberate short radial bearing or compliant torque interface would need a separate owner decision. |
| Neighbor motion drags other pins / loss beside a gap | Neighbor-only guidance is unsuitable for that state; fixed/peripheral guidance remains necessary. |
| Horizontal outside feels smoother but thread catches | Retain upright functional pins. |
| Both horizontal copies retain thread fit and slide better | Orientation is promising locally; it does not qualify a 50 mm horizontal pin or production array. |

Layout: root instructions/projects; `components/` ready-to-slice STLs; `cad/` parametric bodies; `scripts/` reproduction/review; `metadata/` measured digital evidence; `images/` drawings/toolpaths. Clean `A-screw.stl` is the functional part; print the **supported** version supplied in the project. Optional reference `C-pin-50-upright.stl` is included, but is not an extra print job on either plate. Reproduction uses the unchanged legacy thread meshes in this repository; the 3MFs themselves are self-contained.
