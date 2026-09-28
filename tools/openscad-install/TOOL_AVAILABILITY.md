# Tool availability record — OpenSCAD in the agent dev container

**Observed:** 2026-09-28, by [@Fabricator](/DND/agents/fabricator) on issue
[DND-29](/DND/issues/DND-29).

This file records **sourced fact** about what geometry tooling could be installed
in the shape-display agent container, how, and with what evidence. It is the
availability evidence required by DND-29 scope item 1.

## Result: OpenSCAD IS installed and renders the CAD fixtures

| Field | Value |
|---|---|
| Tool | OpenSCAD |
| Version | `2023.09.11` (nightly snapshot) |
| Artifact | `OpenSCAD-2023.09.11.ai-aarch64.AppImage` |
| SHA-256 | `84d7bb1c71e14b4e248a84fbe0a4b02f58bcbf5326f0ee81c8a4de3653a3b568` (verified) |
| Host arch | `aarch64` / arm64 |
| OS | Debian GNU/Linux 13 (trixie) |
| Container privileges | uid 1000 (`node`), **no root, no sudo, no FUSE, no writable apt state** |
| Install method | rootless: AppImage `--appimage-extract` + `apt-get download` of runtime .debs into a private apt state, unpacked with `dpkg-deb -x` |
| Installer | [`install-openscad.sh`](install-openscad.sh) (committed, idempotent) |
| Renders | **yes** — see evidence below |

## Why the repo's CI install method does not work here

`.github/workflows/ci.yml` job `j2-cad-render` installs OpenSCAD with:

```sh
sudo apt-get update
sudo apt-get install -y --no-install-recommends openscad
```

That is correct on an x86_64 GitHub runner but is **not reproducible in the
container**, because:

- `sudo` is absent and the process is not root;
- the dpkg/apt lock files and `/var/lib/apt/lists` are not writable
  (`E: Could not open lock file /var/lib/dpkg/lock-frontend ... Are you root?`);
- there is no `pip` OpenSCAD package that actually renders (only Python bindings
  such as `solidpython2`, which still need the `openscad` binary);
- AppImages need FUSE, which is not present (`dlopen(): error loading
  libfuse.so.2`), so the executable must be extracted instead.

`install-openscad.sh` closes exactly this gap so the harness can run **inside the
container**, not only in CI.

## Evidence

### 1. Version banner

```
$ export PATH="$HOME/.local/bin:$PATH"
$ openscad --version
OpenSCAD version 2023.09.11
```

### 2. It renders the real J2 fixture (not just a trivial cube)

```
$ openscad -o /tmp/j2_isolation_rig.stl \
    06-experiments/test11_falsification_library/j2_isolation_rig.scad
...
Top level object is a 3D object:
   Facets:        276
   Volumes:         2
```

The binary STL is ~169 KB and the repo's mesh checks parse it.

### 3. The repo's own fixture gate now runs its render step

`check_fixture.py` reports `SKIP` when `openscad` is absent. With the wrapper on
`PATH`, the same script passes all six part renders plus the socket probe:

```
[5] OpenSCAD render check
  PASS  holder_5x5 renders to STL
  PASS  holder_10x10 renders to STL
  PASS  base_rail renders to STL
  PASS  indicator_bracket renders to STL
  PASS  miniature_tray renders to STL
  PASS  plate renders to STL
  PASS  fixture socket is an open pocket (slab at z=2.5 is void)
```

## Reproduce

```sh
tools/openscad-install/install-openscad.sh
export PATH="$HOME/.local/bin:$PATH"
openscad --version          # -> OpenSCAD version 2023.09.11
```

Then run the geometry harness (see [`../validate/README.md`](../validate/README.md)):

```sh
python tools/validate/validate_geometry.py
```

## Scope / honesty notes

- This establishes **CAD** evidence (geometry renders and passes mesh/envelope
  gates). It is **not** a print and **not** physical validation. Per program
  policy the program does not perform physical print tests.
- The install is under `$HOME/.local`, intentionally **outside** the repo. No
  binary, key, or credential is committed. Only the installer and this record
  are versioned.
- The AppImage snapshot is a nightly build pinned by URL + SHA-256. If upstream
  removes the URL, re-pin to the current `files.openscad.org/snapshots/*-aarch64`
  artifact and update the hash here.
