#!/usr/bin/env bash
set -euo pipefail

doc() { cat <<'DOC'
require_homebrew: Ensures Homebrew exists or exits with install hint.
remove_other_pythons: Uninstalls any Homebrew Python versions except python@3.12.
ensure_tcl_tk: Installs Tcl/Tk if missing.
ensure_python312: Installs Homebrew python@3.12 if missing. Uses env vars if built from source.
link_python312: Forces python3 symlink to point to 3.12.
py312_bin: Prints absolute path to Homebrew Python 3.12 binary.
test_tk: Verifies Tkinter import.
DOC
}

require_homebrew() {
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew not found. Please install it from https://brew.sh/"
    exit 1
  fi
}

remove_other_pythons() {
  echo "Removing other Homebrew Python versions..."
  brew list --formula | grep '^python' | grep -v '^python@3\.12$' | while read -r pkg; do
    echo "Uninstalling $pkg..."
    brew uninstall --force "$pkg"
  done
}

ensure_tcl_tk() {
  if ! brew list --versions tcl-tk >/dev/null 2>&1; then
    echo "Installing Tcl/Tk..."
    brew install tcl-tk
  else
    echo "Tcl/Tk already installed."
  fi
}

ensure_python312() {
  if ! brew list --versions python@3.12 >/dev/null 2>&1; then
    echo "Installing Python 3.12..."
    export LDFLAGS="-L$(brew --prefix tcl-tk)/lib"
    export CPPFLAGS="-I$(brew --prefix tcl-tk)/include"
    export PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig"
    brew install python@3.12
  else
    echo "Python 3.12 already installed."
  fi
}

link_python312() {
  echo "Linking Python 3.12 as default python3..."
  brew link python@3.12 --force --overwrite
}

py312_bin() {
  local p
  p="$(brew --prefix python@3.12 2>/dev/null)/bin/python3.12"
  if [ -x "$p" ]; then
    echo "$p"
    return 0
  fi
  echo "python3.12 binary not found after installation." >&2
  exit 1
}

test_tk() {
  local PY
  PY="$(py312_bin)"
  echo "Testing Tkinter with $PY ..."
  "$PY" - <<'EOF'
try:
    import tkinter
    print("Tkinter is available.")
except ImportError:
    print("Tkinter is NOT available.")
EOF
}

require_homebrew
remove_other_pythons
ensure_tcl_tk
ensure_python312
link_python312
test_tk

echo "Installation complete. Only Python 3.12 with Tkinter remains."
