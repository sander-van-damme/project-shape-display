# 08 — Current design

This directory is the end of the numbered engineering flow: the place for the best-supported integrated Shape Display design **as it exists now**.

## Current status

There is not yet a product-qualified architecture.

The rotary-stop investigation reached a conditional analytical/CAD candidate, but Test09 records unresolved mechanical, structural, sourcing, reliability and physical-measurement gates. A newer research direction is investigating externalized planar mechanical memory and selectively updateable tiles.

Until one architecture survives the required evidence gates, this folder remains a status page rather than pretending that a final design has been selected.

Cost is currently a **hard blocker independent of mechanism choice**: Test11 shows
no survivor (S1–S5) has a credible sub-$500 purchased path at working allowances,
and the only traceable 8 mm PM stepper is $40/ea. Any bought part required on all
6,400 cells adds at least $320–640 on its own. Selection/programming must be
printed or heavily shared, and a traceable low-cost motor quote is required before
any full-scale build.

Authoritative supporting material:

- [Architecture investigation](../07-evidence-and-decisions/)
- [Evidence matrix](../07-evidence-and-decisions/)
- [Current research direction](../05-research-questions/)
- [Test09 validation](../06-experiments/test09_test08_validation/README.md)

When an architecture becomes sufficiently supported, its integrated system description, BOM, build plan and remaining risk register should live here.
