# Reproduce the Bambu projects

The owner prints the delivered `.3mf` files directly; these scripts are only for engineering reproduction.

- `build-project.py` writes named source meshes from each test's `layout.json`, loads the official X1 Carbon 0.4-mm machine preset including its start/end G-code, and reuses the process/filament values from the **physically printed unchanged E-295 compact project**. It disables arrangement and reorientation. It saves the sliced project, reopens that saved project without external profiles and slices it again.
- `validate-project.py` independently reads the saved archive, transforms its meshes, compares source facets, and inspects every actual linear G-code extrusion. It checks configured values, layer support, bridge spans and start/end distances, and saves legible layer images. Line-width buffers represent nominal deposited material, not measured bead dimensions.
- `critical-paths.py` separately examines DD bore openings, thin neck walls and both dog teeth, with local images of real extrusion footprints. Pass `--dog-root 6.2` for the final rotor. The central 0.60-mm-radius free-space test is a blockage screen; it does not establish the complete DD/thread fit.

Use Python with numpy, trimesh, scipy, shapely and matplotlib, plus the official **Bambu Studio 02.08.02.61** executable and resources. The pinned Ubuntu 24.04 AppImage is at:

`https://github.com/bambulab/BambuStudio/releases/download/v02.08.02.61/BambuStudio_ubuntu24.04-v02.08.02.61-20260820225108.AppImage`

SHA-256: `d501b103fac5424513ec0e8d6bc145fb30719de2c7d94d7320d723740c81a7fd`.

Example, from the repository root, substituting installed executable/resources paths:

```sh
python tools/curated-experiment-checks/E-297/printing/build-project.py \
  --bambu /path/to/bambu-studio --resources /path/to/resources \
  --scratch work/two-half/rebuild-fit \
  --stl owner-print-tests/2026-10-16-two-half-clutch-fit/clutch-fit.stl \
  --out owner-print-tests/2026-10-16-two-half-clutch-fit/clutch-fit.3mf
```

For the matrix use the corresponding matrix paths and add `--brim 3 --brim-gap 0`. The baseline's 0.12-mm layers, Arachne walls, temperatures, cooling and slow speeds are preserved. Both jobs have supports off; the matrix uses an external 3-mm brim with zero separation.

The headless session used the unmodified official executable, WebKit runtime libraries, Weston and Xvfb, and Mesa OSMesa software rendering. A small GLX/OSMesa symbol bridge supplied a real software OpenGL context to Bambu's thumbnail renderer; it did not alter meshes, slicer configuration or G-code. Rendered thumbnails were visually inspected. This is CLI reopen/reslice plus independent path inspection, not an interactive Bambu GUI session or a physical print.

Keep binaries, extracted packages, G-code scratch and failed/replaced candidates under `work/`; do not commit them. Final project/source SHA-256 values and per-project reopen results are recorded beside the deliverables. Reopen may produce tiny floating-point toolpath/time differences, so a successful reopen is not represented as byte-identical G-code unless the comparison actually found that.
