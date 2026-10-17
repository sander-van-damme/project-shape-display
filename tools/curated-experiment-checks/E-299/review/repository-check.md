# Repositorycontrole, 17 oktober 2026

`./repo check` is uitgevoerd na de definitieve oplevering. Er zijn geen nieuwe structuurmeldingen; de returncode blijft 1 door zeven bestaande omvangsmeldingen:

- Oversized atomic object: E-266, E-283, E-286, E-288, E-293.
- Oversized instructions: AGENTS.md en owner-print-tests/AGENTS.md.

De onafhankelijke SHA-256-controle van alle 1.257 bestaande tracked bestanden tegenover de opgehaalde broncommit `46a4117d5bbed2c5fc0669be62e27b7c1233a7e2` meldt nul wijzigingen. Nieuwe files staan uitsluitend bij E-299, de nieuwe gedateerde test en lokale scratch. De omvangrijke CAD-/slicerruntime staat buiten de repository; `work/slicer-runtime` is een lokale symlink en geen onderdeel van het afleverpakket.

Alle specifieke CAD-/3MF-/heropencontroles slagen. Dit vervangt geen fysieke test. Zie `delivery-integrity.json`, `geometry-review.json` en het nieuwe printtestpakket.
