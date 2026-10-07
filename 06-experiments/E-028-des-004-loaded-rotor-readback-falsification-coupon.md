---
status: complete
builds-on: [DES-004, ADR-007, E-016, E-014, E-012]
---
# E-028: rejected loaded-rotor test definition

The proposed DES-004 test aimed to evaluate five-stop loaded motion/return, writer engagement, fixed-standoff readback, loaded-neighbour isolation, timing and wear. It was never fabricated or measured.

E-042 is the consolidated adverse audit: the CAD lacks stops/detents/follower/return and an assembled load path; its modulo schedule does not cover the 20 directed five-state transitions per cell. Synthetic fit/state checks therefore cannot validate this test definition. E-042 retains the corrected count/trace/margin requirements and distinction from E-016's calibration checker.

The full superseded protocol is in Git history at `ce8135eb4f1b1cb138bdf71edd6092f7ac9c1db8`. Executable geometry remains with DES-004. Retire this handoff under ADR-009; only a newly justified mechanism and comparison can warrant further fixture work. No test result, production readiness or hardware rejection is implied.
