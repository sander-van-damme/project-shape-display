"""Check the delivered files and their recorded provenance, without regenerating CAD."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
import zipfile
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TESTS = [ROOT / "owner-print-tests" / ("2026-10-16-two-half-clutch-" + name)
         for name in ("fit", "matrix")]
errors = []
checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        errors.append(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


for path in HERE.rglob("*.py"):
    ast.parse(path.read_text(), filename=str(path))
    checks += 1

for name, expected in read(HERE / "drawings/source-manifest.json")["source_sha256"].items():
    check(sha(ROOT / name) == expected, "Drawing source changed: " + name)

for entry in read(HERE / "print-and-assembly.sources.json")["sources"]:
    check(sha(ROOT / entry["path"]) == entry["sha256"], "PDF instruction source changed")

geometry = read(HERE / "independent-geometry.json")
check(sha(HERE / "independent_geometry.py") == geometry["source_sha256"],
      "Independent geometry script changed after its recorded run")
for name, expected in geometry["actual_meshes"]["source_mesh_sha256"].items():
    check(sha(HERE / "cad/parts" / (name + ".stl")) == expected,
          "Independent mesh changed: " + name)
check(geometry["actual_meshes"]["all_nominal_and_sampled_states_clear"],
      "Unexpected sampled nominal/assembly collision")

projects = []
for directory in TESTS:
    validation = read(directory / "validation.json")
    project = directory / validation["project"]
    check(sha(project) == validation["project_sha256"], "Stale project validation: " + str(project))
    check(sha(directory / validation["source_stl"]) == validation["source_stl_sha256"],
          "Stale source validation: " + str(project))
    with zipfile.ZipFile(project) as archive:
        check(archive.testzip() is None, "Corrupt 3MF archive: " + str(project))
        gcode = archive.read("Metadata/plate_1.gcode")
        check(hashlib.sha256(gcode).hexdigest() == validation["gcode_sha256"],
              "G-code differs from path validation: " + str(project))
        settings = json.loads(archive.read("Metadata/project_settings.config"))
        check(settings["printer_model"] == "Bambu Lab X1 Carbon", "Wrong printer")
        check(settings["nozzle_diameter"] == ["0.4"], "Wrong nozzle")
        check(settings["enable_support"] == "0", "Unexpected support")
        if directory.name.endswith("matrix"):
            check(settings["brim_object_gap"] == "0", "Matrix brim does not contact feet")
    roundtrip = read(directory / "roundtrip.json")
    check(roundtrip["reopened_without_external_profiles"], "Reopen used outside profiles")
    check(roundtrip["return_code"] == 0, "Reopen/reslice failed")
    check(not roundtrip["settings_differences"], "Saved settings changed during reopen")
    check((directory / "reopened-critical-paths.json").exists(), "Missing reopened critical paths")
    check(not validation["unsupported_layer_components"], "New floating layer components")
    projects.append({"file": str(project.relative_to(ROOT)), "sha256": sha(project),
                     "layers": validation["layer_count"]})

documents = list(HERE.rglob("*.md")) + [p for d in TESTS for p in d.glob("*.md")]
documents.append(ROOT / "06-experiments/E-297-two-half-row-column-clutch-print-tests.md")
for document in documents:
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", document.read_text()):
        target = target.strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or not parsed.path:
            continue
        check((document.parent / unquote(parsed.path)).exists(),
              f"Missing local link in {document.relative_to(ROOT)}: {target}")

result = {"scope": "Delivery integrity only; not a physical or continuous tolerance proof",
          "checks": checks, "errors": errors, "projects": projects}
(HERE / "validation/delivery-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
sys.exit(bool(errors))
