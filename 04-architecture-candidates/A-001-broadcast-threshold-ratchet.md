---
status: candidate
builds-on: [M-004, M-002, P-001, P-002]
---

Each column stores height in a ratchet. Four patterned threshold strokes increment selected columns through five 0/10/20/30/40 mm levels. Shared lift supplies power; masks select; ratchets carry load.

Risks: release-force accumulation, print variation, silent missed/double steps, scalable reset and physical mask writing. Banking reduces simultaneous force but adds coupling/isolation work. Old force estimates varied with assumed pawl geometry; none were measured.

Test: adjacent final-pitch columns with adversarial masks and shared strokes; measure holding/release force, missed states and untouched-neighbor motion.
