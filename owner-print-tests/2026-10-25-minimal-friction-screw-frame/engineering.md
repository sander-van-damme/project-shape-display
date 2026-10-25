# Engineering basis and limits

The selected prototype moves the thread start **8.4 mm closer to the motor** and removes the Ø7 / 3.7 mm v3 journal. It retains the successful C radial profile and motor cavity. It is a **physical test article**, not a measured friction improvement or load-rated motor assembly.

## What was unnecessary in v3

The actual v3 body is Ø7 ×12 mm, but only Z21.2–24.9 is a close Ø7.4 radial journal: **3.7 mm**, with 0.20 mm radial clearance. The lower washer pocket is not a second rotor journal. The 40 mm square guide is also real; it can overconstrain a bowed pin or misregistered halves.

The 12 mm body provided a 6 mm deep C cavity and another 6 mm up to the remote shoulder. The gear is only approximately 1.25 mm long. The remote journal/upper-stop architecture, not gear engagement, used most of that space. The former shaft-tip/roof gap was 4.35 mm. Shortening this arrangement is justified without changing the thread.

New body, measured from its bottom:

| Retained section | Dimension | Purpose |
|---|---:|---|
| Entry lead-in | 0–0.25 mm | Same v3 lead-in; avoids replacing the successful radial interface. |
| C cavity | 0–2.40 mm | Retains L gear overlap plus 0.75 mm nominal roof clearance above the shaft tip. |
| Solid roof/web | 2.40–3.60 mm | Ten nominal 0.12 mm layers connect the cavity/hub to the screw core. |
| Thrust flange | Ø7, 0–1.20 mm | Reuses the washer below; provides the opposing shoulder above. Overlaps the cavity section rather than adding stack length. |
| Compact hub | Ø4, to 3.60 mm | At least 0.75 mm nominal wall outside the C cavity; no long solid intermediate cylinder. |

The screw is integral, Ø3.2 nominal / lead3, with **27 mm thread**. The working profile and phase come from the original mesh, unscaled. A 0.6 mm terminal chamfer is outside the working engagement. A small core union at the junction only ensures mesh continuity. This screw replaces the 48 mm thread for a deliberately bounded 15 mm test; it reduces straight-bore overlap from roughly 39 to18 mm at low height. Shorter length can reduce bow/eccentric leverage, but does not prove concentric printing.

## Axial stack and both thrust directions

[Dimensioned actual-mesh section](images/assembly-section.svg). Z=frame bottom; all heights are nominal CAD, not metrology.

| Feature | v3 long screw | New A |
|---|---:|---:|
| Motor metal bottom / top | 2 / 11.2 | same |
| L gear bottom / top; shaft end | 13.2 / 14.45; 14.55 | same |
| K gear bottom / top; shaft end | 12.7 / 13.95; 14.05 | same motor reference, not powered release |
| Lower deck / washer | deck starts11.4; washer12.4–12.9 | same |
| Rotor lower face / upper shoulder | 12.9 /24.9 | 12.9 /14.1 |
| C straight zone / roof | 13.15–18.9 /18.9 | 13.15–15.3 /15.3 |
| L straight gear overlap, seated / lifted | 1.25 /1.00 | 1.25 /1.00 |
| Upper thrust stop underside / top | 25.2 /27.2 | 14.4 /16.0 |
| Float before upward thrust reaction | 0.30 | 0.30 |
| Thread start / end | 24.9 /72.9 | 16.5 /43.5 |
| Motor top → thread start | **13.7** | **5.3** |
| First used pin thread at low | 27.9–33.9 | 19.5–25.5 |
| Pin thread at +15, rotor seated | 42.9–48.9 | 34.5–40.5 |
| Guide stations | 32.7–72.7 | 36–38 and56–58 |
| Overall frame height | 72.7 | 60.0 |

K has about 0.80 mm straight engagement seated, 0.50 mm lifted; it is not silently treated as L. Unknown measurement/printing tolerance is not absorbed into a fictitious guaranteed margin.

**Load paths:** motor torque → three C ribs → integral hub/screw → helical flanks → pin translation. Pin rotation is reacted geometrically at the square guide faces → right frame spine/closed halves → base. A downward load on the screw passes flange → existing washer → deck → frame. An upward reaction passes flange upper annulus → upper stop → frame after 0.30 mm float. Lowering a downward-loaded pin can still use the lower thrust surface; rotation direction does not determine force direction.

Nominal lower rotor/washer contact area is about30.4 mm²; upper annulus about18.8 mm². Both are **sliding thrust contacts**, unavoidable here. No bearing, spring preload or added precision hardware is introduced. C axial freedom and a visibly seated washer are necessary: a sticking C fit can transmit axial friction into the motor even with 0.75 mm roof clearance. CAD contact probes establish a structural path in both directions, not actual zero shaft load.

## Lateral stability: what is and is not removed

A completely unbounded rotor is inappropriate. New A retains only a **0.6 mm long loose Ø4.4 throat** around the Ø4 hub at Z15.4–16.0 (0.20 mm radial gap). The lower 1.0 mm of the stop has a Ø5 opening; the flange circumference is otherwise exposed. There is **no nominal radial rubbing** in the centered sweep. The short throat can contact under eccentricity and is the explicit exception to removing all radial constraints. It is 84% shorter than the old journal; that is a length reduction, **not** a friction prediction.

Pin side force is intended to reach the two square guides. With guide centers37/57 and a50 mm pin tip at69.5–84.8, ideal engaged-contact reactions are about1.63–2.39 times the applied tip force at the upper guide and0.63–1.39 at the lower. The flange/thrust contacts can react some rotor moment; the loose throat limits translation after clearance is taken up. The C connection can share residual lateral force. Its compliance and the motor's permitted radial load are unknown.

**The throat cannot guarantee shaft protection before its 0.20 mm gap closes.** Nor can an assumed flexible C socket be used as proof: its three ribs are integral lobes, not designed springs. This is why A is released only for unloaded free-running prototype checks, with manual eccentricity/wobble inspection before powering. Added side loads, miniature loads and endurance are not qualified. Shaft motion, coupling creep or recurring radial witness marks reject that condition. A positive bearing or compliant torque interface would require another design decision; neither is concealed as a proven property of this prototype.

The misalignment check is instructive: parallel pin offsets0.05/0.10 mm show no nominal interference; about0.15 mm begins contact and0.20 mm produces definite thread/bore interference, while the4.8 guide can still accommodate that offset. Thus simply enlarging the guide is **not** a cure. The nominal square bore is3.52, only0.16 mm per side outside the screw. Clearance, layer ridges and bow remain physically important. This is an explicit stability limit, not evidence of a measured safe force.

## Local guidance and travel

Two **2 mm square bands**, opening4.8, replace40 mm of continuous guidance. Total potential axial guide length is4 mm, a90% reduction. Their20 mm center spacing gives a moment arm while both stay fully overlapped at0–15 mm. Three registration pegs, including near both bands, and hard mating faces limit misregistration; they do not make printed halves perfectly straight or immune to closure pressure. A single right spine leaves the PCB/wire side open and eliminates an unnecessary tall left rail.

A single short collar resists yaw but provides poor pitch/roll restraint. Two perpendicular faces/open corner are unilateral: without a keeper or preload the pin can lift away under reversed torque/load. Opposed corners or a key can constrain it, but introduce delicate small features or a new pin profile. The supplied two square bands preserve the existing pin and react both torque directions with four simple faces. Friction is not required to resist yaw; the faces provide normal reactions. At4.8 opening, centered square yaw play is about±5.5° (about0.046 mm one-way lead equivalent). A5.0 opening would increase it to about±8.5° and increase tilt freedom; no second full frame is printed just to test more play. B's two clearances investigate that trade-off cheaply.

Thread overlap is **6 mm at0,3,7.5 and15 mm**, at both rotor float limits; the thread end retains3 mm margin at+15. A50 mm pin retains both guide bands throughout; a40 mm same-profile pin still reaches Z59.5 at low, above the upper guide's Z58 top. The unthreaded sleeve overlap falls18→3 mm. The lower guide first loses full engagement beyond about+16.2 mm at maximum float. No40 mm travel claim or hidden stop is made. An18 mm pin cannot reach both guides and is used only for orientation coupons.

## Can neighbors replace guide walls?

For an isolated centered square of widtha=4.4 with fixed centered neighbors atp=5.08, the available cage width is **2p−a=5.76**, notp. First contact satisfies

`a(cosθ + sinθ) = 2p − a`, giving **θ=22.769°**.

That is0.1897 mm one-way or0.3795 mm reversal play for lead3. Fixed square-polygon intersections verify the contact. If all squares rotate together at fixed centers, first contact is instead about29.987° (`cosθ=a/p`). Translation and yielding neighbors can permit still more motion: there is no absolute antirotation reference without a structural boundary or occasional fixed guide.

The fixture retains true5.08 mm centers but allows0.6 or0.3 mm radial stem play. Worst opposing translational play is1.2 or0.6 mm, compared with a0.68 face gap; even the closer condition has only0.08 mm nominal opposing-error margin before print-size error. This tests real collision sensitivity rather than assuming fixed neighbors. At15 mm height difference its30 mm bodies retain15 mm overlap; at30 mm they lose it. Raised, missing or recessed neighbors remove particular reaction directions. Boundary pins have no outside neighbors, so the removable ring is a separate, explicit constraint.

Moving contact can transmit vertical friction to stationary neighbors; neighbors that can move or rotate can redistribute torque through the array. More neighbor contact area does not guarantee more Coulomb friction, but contact forces, defects, seams and accumulated grid error can create binding and cross-motion. **Preliminary conclusion:** mutual contact may supplement sparse guides, but it does not yet justify replacing all fixed antirotation/lateral guidance. The held-neighbor and freely sliding conditions deliberately separate geometry from independent-motion failure.

## Actual print orientation evidence

The original saved project has upright pins and flat frame halves. Pin outer paths lie in horizontal layers, transverse to vertical motion. The old frame guide **side-wall** paths are already longitudinal (100% of inspected wall length); the guide floor uses diagonal/top-skin paths. New short-guide walls remain longitudinal; their floor paths are transverse. Rotating the entire frame would not make every contact face longitudinal, and would sacrifice its flat support-free print pose.

The selected horizontal pin puts about**97.3%** of inspected long-side outer perimeter length parallel to sliding. Its bed face and roof/top skin are different surfaces, not four equivalent polished faces. Upright pins avoid horizontal bore roofs and show no internal bridge paths. Horizontal pins require real roof bridges, with a maximum individual free segment about2.57 mm after saving a180° bridge direction across the narrow bore (automatic direction gave5.35 mm); this is **not** a promise of clean bridging. Aligned seams remain potential ridges on both poses.

An initial horizontal roll produced a0.20 mm² detached deposition island near the thread. Three alternative rolls were sliced; the90° roll avoided that island and is saved for both duplicates. Both final/reopened projects have no detached islands or automatic support paths. This makes a useful small comparison possible, not a declaration that horizontal female threads work. Inspect/hand-test the bridges and all four exterior faces; keep upright functional long pins unless the physical comparison supports changing them.
