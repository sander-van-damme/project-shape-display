#!/usr/bin/env bash
# Rootless OpenSCAD installer for the Shape Display dev container (aarch64).
#
# WHY THIS EXISTS
# ---------------
# The agent dev container has NO root, NO `sudo`, NO FUSE and NO writable apt
# state (the dpkg/apt lock and `/var/lib/apt` are not writable). The repo's CI
# installs OpenSCAD with `apt-get install` on an x86_64 runner; that path does
# not work inside the container where the geometry harness actually runs.
#
# This script installs a real OpenSCAD binary *without root* by:
#   1. downloading the upstream aarch64 AppImage and verifying its SHA-256,
#   2. extracting it with `--appimage-extract` (no FUSE needed),
#   3. resolving + fetching the few shared libs the AppImage does not bundle
#      (harfbuzz, freetype, fontconfig, X/GL, ...) via `apt-get download` using
#      a *private, writable* apt state dir, then unpacking them rootlessly with
#      `dpkg-deb -x`,
#   4. writing an `openscad` wrapper that points LD_LIBRARY_PATH at that prefix
#      and forces QT_QPA_PLATFORM=offscreen for headless rendering.
#
# Version resolution is delegated to apt (not hardcoded pool URLs), so the
# install survives Debian point-release bumps.
#
# USAGE
# -----
#   tools/openscad-install/install-openscad.sh
#   export PATH="$HOME/.local/bin:$PATH"
#   openscad --version
#
# The exact version/method observed on this container is recorded in
# TOOL_AVAILABILITY.md. Nothing installed here is committed to the repo; only
# this script and that record are versioned. The binary lives under $HOME.

set -euo pipefail

OC_HOME="${OPENSCAD_HOME:-$HOME/.local/openscad}"
BIN_DIR="$HOME/.local/bin"
DEB_DIR="$OC_HOME/debs"
PREFIX="$OC_HOME/deps"
APT_DIR="$OC_HOME/apt"

APPIMAGE_URL="https://files.openscad.org/snapshots/OpenSCAD-2023.09.11.ai-aarch64.AppImage"
APPIMAGE_SHA256="84d7bb1c71e14b4e248a84fbe0a4b02f58bcbf5326f0ee81c8a4de3653a3b568"

# Runtime libs the AppImage does not bundle. Names only -- apt resolves versions.
LIBS=(
  libgpg-error0 libharfbuzz0b libfreetype6 libfontconfig1 libexpat1
  libpng16-16t64 libgraphite2-3 libbrotli1 libfribidi0 libthai0 libdatrie1
  libx11-6 libxcb1 libxau6 libxdmcp6 libxext6 libxrender1 libxi6
  libxfixes3 libxrandr2 libxcomposite1 libxdamage1 libxkbcommon0
  libgl1 libglvnd0 libglx0 libcairo2 libpixman-1-0 libuuid1 libffi8
  libbsd0 libmd0 libselinux1 libpcre2-8-0 liblzma5 libzstd1 libbrotli1
)

need() { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: missing tool: $1" >&2; exit 1; }; }
need curl; need sha256sum; need dpkg-deb; need apt-get

mkdir -p "$OC_HOME" "$BIN_DIR" "$DEB_DIR" "$PREFIX" \
         "$APT_DIR/lists/partial" "$APT_DIR/cache/archives/partial" "$APT_DIR/state"

echo "==> [1/3] OpenSCAD AppImage"
APPIMAGE="$OC_HOME/OpenSCAD-arm64.AppImage"
if [[ ! -x "$OC_HOME/squashfs-root/usr/bin/openscad" ]]; then
  [[ -f "$APPIMAGE" ]] || curl -fSL -o "$APPIMAGE" "$APPIMAGE_URL"
  echo "    verifying SHA-256 ..."
  echo "$APPIMAGE_SHA256  $APPIMAGE" | sha256sum -c -
  chmod +x "$APPIMAGE"
  ( cd "$OC_HOME" && "$APPIMAGE" --appimage-extract >/dev/null )
  echo "    extracted to $OC_HOME/squashfs-root"
else
  echo "    already extracted -- skipping"
fi

APTOPTS=(
  -o Dir::Etc::sourcelist="$APT_DIR/sources.list"
  -o Dir::Etc::sourceparts=/dev/null
  -o Dir::State="$APT_DIR/state"
  -o Dir::State::lists="$APT_DIR/lists"
  -o Dir::Cache="$APT_DIR/cache"
  -o APT::Get::List-Cleanup=0
)

echo "==> [2/3] dependency .debs (rootless apt) -> $PREFIX"
if [[ ! -f "$APT_DIR/sources.list" ]]; then
  cat > "$APT_DIR/sources.list" <<'SRC'
deb http://deb.debian.org/debian trixie main
deb http://deb.debian.org/debian-security trixie-security main
SRC
fi
apt-get "${APTOPTS[@]}" update >/dev/null
( cd "$DEB_DIR" && apt-get "${APTOPTS[@]}" download "${LIBS[@]}" ) \
  || echo "    WARN: some packages could not be downloaded"
for deb in "$DEB_DIR"/*.deb; do
  [[ -e "$deb" ]] || continue
  dpkg-deb -x "$deb" "$PREFIX"
done
echo "    unpacked $(find "$PREFIX" -name '*.so*' | wc -l) shared objects"

echo "==> [3/3] wrapper + smoke test"
cat > "$BIN_DIR/openscad" <<'WRAP'
#!/usr/bin/env bash
OC_HOME="${OPENSCAD_HOME:-$HOME/.local/openscad}"
export LD_LIBRARY_PATH="$OC_HOME/deps/usr/lib/aarch64-linux-gnu:$OC_HOME/squashfs-root/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
exec "$OC_HOME/squashfs-root/usr/bin/openscad" "$@"
WRAP
chmod +x "$BIN_DIR/openscad"

if PATH="$BIN_DIR:$PATH" openscad --version; then
  echo "OK: OpenSCAD installed at $BIN_DIR/openscad"
  echo "    add to PATH:  export PATH=\"$BIN_DIR:\$PATH\""
else
  echo "FAIL: openscad did not run" >&2
  exit 1
fi
