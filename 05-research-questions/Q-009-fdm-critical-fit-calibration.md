---
status: open
builds-on: [M-003, M-005, M-012]
---
# Q-009: manufacturing uncertainty and critical-fit calibration

Which dimensional, friction, material and assembly uncertainties change mechanism feasibility or architecture ranking on the stage 02 fabrication process?

Start with source-backed process priors or labelled bounds and test sensitivity, correlation and transferability. Rank missing parameters by their effect on decisions. Request a small actual-process calibration only when its information value warrants fabrication; update the reusable model and rerank affected candidates.

E-016 and `tools/fdm-critical-fit-calibration/` retain a historical rotor/writer/reader calibration matrix and checker. They are possible future instruments, not measurements or a mandatory next task. Reuse requires a concrete mechanism and review of applicable loads, margin definitions and sampling. No general X1C/PLA accuracy, friction, creep or yield distribution is yet qualified by these records.
