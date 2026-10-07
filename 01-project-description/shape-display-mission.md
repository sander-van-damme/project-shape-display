# Shape Display: purpose and research mandate

Develop an affordable, manufacturable, reliable physical Dungeons & Dragons battle map. Dense independently height-adjustable square/rectangular column tops form terrain, walls, stairs, pits and platforms while supporting normal miniatures. Product requirements live in `02-design-criteria/`.

## Computational invention

The research program must search broadly for mechanisms and complete machine architectures that substantially improve the product. Computational invention is a primary responsibility: generate, combine, synthesize and optimize mechanical operating principles, addressing and multiplexing, state storage, load paths, actuation, sensing and recovery. Existing designs are seed ideas and comparison references, never the boundary of the search or a protected solution.

Invest research effort in materially different ways of performing these functions. Small dimensional changes, another coupon layout, renamed variants, or repeated audits of the same assumptions do not constitute architectural exploration. Explore unfamiliar combinations and cross-disciplinary principles, including mechanisms generated through parametric synthesis, inverse design or topology optimization where appropriate. A new proposal must explain its causal mechanism and potential advantage; novelty alone is not feasibility or value.

Simple components and simple winning machines are welcome. The objective is ambitious invention that produces a practical product, not complexity for its own sake. Conventional designs provide control comparisons. A family earns further work through new evidence, a meaningful change in operating principle, or a credible route to better performance; familiarity and accumulated documentation do not confer priority.

## Search and comparison

Represent candidates by their addressing method, state/memory principle, energy source, load path, degrees of freedom, contact topology, selection fanout, repeated precision interfaces, verification and recovery. Use these descriptors to detect duplicates and track which regions of the design space have actually been explored. Do not count parameter sweeps within one topology as a broad architecture search.

Build executable generators and evaluators when they can answer a concrete design question. Start with a small reproducible end-to-end search, validate that its encoding and models represent real mechanisms, then increase coverage. Record generation rules, parameter ranges, constraints, solver settings, random seeds, rejected populations and reasons, and representative survivors. Do not build a large generic search framework before demonstrating useful discrimination.

Evaluate complete machines, including all selection, programming, lifting, locking, sensing, transport, registration, reset, retry and service operations. Address bits or a nominal fanout count do not establish a physical selector, energy path or throughput. Check arbitrary reachable maps, unintended activation, simultaneous selection, regional isolation and recovery from faults.

Compare feasible candidates on a Pareto frontier covering purchased cost, printed material/time/scrap, assembly and calibration effort, update time, reliability, durability, disturbance, compactness, repairability and D&D usefulness. Enforce the product constraints and show uncertainty and margins. Use novelty/diversity to allocate exploration and retain distinct promising families; do not let a novelty score compensate for an impossible mechanism or missed hard requirement. Keep a simple comparator to expose unnecessary complexity. No fixed number or fraction of surviving designs is required.

## Simulation before fabrication

Maximize useful computational learning before printing. Use the least expensive model that can discriminate between candidates:

1. Check kinematic reach, state encoding, geometry, energy/force bounds, information throughput and full-scale cost/timing.
2. Screen sensitivities and manufacturing uncertainty with analytical/reduced-order models and appropriately sampled Monte Carlo or bounded scenarios.
3. Use rigid-body/contact simulation or parametric structural analysis for survivors whose ranking depends on those effects.
4. Use nonlinear contact, friction, buckling, snap-through, anisotropic material or time-dependent models when those phenomena drive a decision.
5. Propagate bank and board interactions, correlated deformation, scheduling, failure detection and recovery. Full-scale accounting begins at the first screen; it is refined throughout.

Refine fidelity only where it can change a decision. Validate reduced models and surrogate predictions against independent calculations or higher-fidelity cases, including holdouts and failure cases. Record applicability, numerical convergence and model discrepancy. Optimizer success, a rendered CAD assembly and a solver returning normally do not prove mechanical feasibility. Model every required state and transition, actual contacts and load-support continuity; check the generated geometry rather than only inequalities among nominal parameters.

## Manufacturing-aware uncertainty

Model the manufactured mechanism rather than perfect nominal CAD. Start with documented literature, manufacturer/process data and relevant existing measurements for the fabrication process in stage 02. Record each source, material, printer/process, nozzle, orientation, slicer/compensation, conditioning and test conditions, plus why it transfers to our process. Published machine motion resolution is not finished-part accuracy.

Consider decision-relevant dimensional bias and spread, hole shrinkage, wall variation, first-layer effects, warp, layer quantization, roughness/contact friction, orientation-dependent stiffness and strength, inter-layer weakness, creep, fatigue, wear, assembly clearance and alignment. Include shared batch/print/material biases and spatial correlation as well as local variation; do not assume 6,400 independent identical cells by default. Include uncertainty in the model itself.

Use probability distributions only when their form and parameters have a defensible basis. Otherwise use labelled ranges, bounded scenarios or alternative priors. Separate manufacturing variability from uncertainty about it; test sensitivity to the prior and correlation assumptions. Do not manufacture precise probabilities from guessed tolerances or treat generic PLA data as calibrated X1C capability.

Report relevant yield and force/time distributions, failure modes, sensitivity drivers and conditional board-level consequences, with sample sizes and uncertainty bounds. Zero observed simulation failures do not establish zero failure probability. Account for common-cause faults, reader false acceptance, retries and repair; a cell-yield estimate alone is not a map-yield estimate.

## Physical evidence and research economy

Printing is a targeted later tool. Request a physical experiment when its expected information value exceeds further computation: for example, to calibrate a parameter that changes rankings across several families, distinguish competing model predictions, investigate an effect that cannot credibly be bounded, or qualify a selected mechanism. Choose the smallest representative article and state how its result will update the model or decision. A 5×5 coupon is one possible article size, not the project architecture, default next task or required search unit.

Simulation can reject concepts and support conditional selection. Physical validation remains necessary before claims of hardware performance, production reliability or final product qualification. Calibration of one parameter does not validate an entire machine. Keep sourced facts, assumptions, calculations, CAD, simulation and measurements distinct.

Preserve durable negative knowledge, executable source and irreplaceable measurements. Consolidate repeated reviews into the canonical result and remove obsolete proposals and management narrative from the working tree; Git history retains their provenance. A new task should add a distinct mechanism, reusable model, decision-changing evidence or substantive improvement. Repeating that physical evidence is absent is not new progress.
