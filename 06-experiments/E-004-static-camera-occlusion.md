---
status: complete
---
Hypothesis: A cheap single static camera can verify every cell of arbitrary terrain without scanner motion.
Method: Geometric shadow calculation for 5.08 mm pitch, 40 mm height contrast and an 80×80 grid; finite-distance pinhole and 45° parallel-view bounds.
Result: A 40 mm rise casts a 40 mm shadow at 45°, about 7.87 pitches. An 80-cell wall hides roughly 640 low cells in that view. Finite-distance overhead views also hide valleys away from the optical axis. Flat tops of equal albedo under diffuse light provide no reliable height-dependent brightness ratio.
Conclusion: Reject the specified single-view camera as universal per-cell verification. Multi-view, structured illumination, calibrated fiducials or telecentric optics require a separately evaluated subsystem.
Risk: Historical simulated cell counts and contrast constants were not physically validated. The geometric counterexample is sufficient to reject universal visibility; it does not reject every camera-based sensing architecture.
Evidence class: Geometric calculation and idealised optical assumptions.
