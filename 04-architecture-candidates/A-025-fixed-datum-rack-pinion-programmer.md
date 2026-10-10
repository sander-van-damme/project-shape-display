---
status: candidate
builds-on: [A-007, A-013]
---

# Fixed-datum rack-and-pinion programmer

Each guided column carries a full-travel rack engaging a **stationary pinion**.
A travelling row bank docks rotary drives to pinion shafts at one common height.
The rack moves; the docking shaft does not. A positively retained ground bolt
arrests the shaft/gear between updates. Unlike A-007's screw, displacement per
turn is the pinion circumference; unlike A-013's foot clamp, docking need not
follow the column's previous height. This is a topology recombination, not a new
gear principle or a reopening of the rejected screw geometry.

Sequence: dock keyed drive → take load → unload/retract only the addressed bolt
→ turn pinion to target → reinsert bolt → seat/prove ground support → verify
rack height → undock. An independently retained selection state survives proof.
Bilateral powered drive and an arrested drive shaft are needed while the ground
bolt is open, including loss of power. E-127 constructs a nominal single-head
powered contact sequence; a spring-return ground bolt is blocked at mid-index
and does not supply continuous passive arrest. Bolt actuation and its grounded
guide remain unbuilt.
A shared rotating bus with selectable head clutches is the economical hypothesis;
independent drives are the timing control, with no affordable BOM yet.

Load path: cap → rack teeth → pinion → shaft bearings/positive arrest → module
frame. Unselected bolts stay locked during regional updates. Repeat 6,400 racks,
pinions, bearing sets and arrests; teeth/backlash/wear and shaft alignment replace
the jaw-acquisition problem. Internals may be staggered beneath 5.08-mm tops,
but no tileable mesh/shaft/bolt package is demonstrated. A 3-mm pitch diameter gives
4.24 turns per 40 mm and about 1,910 rpm at 300 mm/s, **kinematic assumptions**,
not a motor or printable-gear qualification.

A rack mark plus ground-support proof must detect docking/mesh skips and false
bolt seating; motor angle alone does not prove height or support. On disagreement
keep the drive supported/arrested and selection retained, attempt one controlled
reseat, then stop/service the module. Common registration or reader failure can
corrupt a row. E-126's continuous-motion bound remains conditional.

E-127 rejects simultaneous engagement of its six-dog rigid bank to shafts 30°
apart. Matching twelve ground slots to twelve dock dogs removes that nominal
phase conflict, yielding a 1.88496-mm height grid with a 7.2-mm pitch-diameter
pinion. This is an unapproved discrete terrain option, not arbitrary-angle
coupling. Its dock fit fails the labelled ±.05-mm error scenario. Two axial
gear lanes clear gear envelopes but the tested straight shaft hits the adjacent
rack backing by .62 mm. Neither result rejects other shaft routes or gear forms.

Retain only conditional alternatives: independently phased continuous heads, or
matched-index heads with an actually arrested shared bus. Before timing/cost
work, a changed joint must show finite routed access, two distinct retained
heights, selective load transfer and power-loss support. Stop further dimensional
tuning of the failed straight-shaft/six-dog embodiment. No fabrication justified.
