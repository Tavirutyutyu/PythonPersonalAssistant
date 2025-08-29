#!/usr/bin/env bash
set -euo pipefail

doc() { cat <<'DOC'
require_homebrew: Ensures Homebrew exists or exits with install hint.
ensure_tcl_tk: Installs Tcl/Tk if missing.
ensure_python312: Installs Homebrew python@3.12 if missing. Avoids force-link.
py312_bin: Prints absolute path to Homebrew Python 3.12 binary.
test_tk: Verifies Tkinter import with the requested snippet; retries once if needed.
DOC
}

require_homebrew() {
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew not found. Install it from https://brew.sh/"
    exit 1
  fi
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
    brew install python@3.12
  else
    echo "Python 3.12 already installed."
  fi
}

py312_bin() {
  local p
  p="$(brew --prefix python@3.12 2>/dev/null)/bin/python3.12"
  if [ -x "$p" ]; then
    echo "$p"
    return 0
  fi
  if command -v python3.12 >/dev/null 2>&1; then
    command -v python3.12
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
  if "$PY" - <<'EOF' | grep -q 'NOT available'
try:
    import tkinter
    print("Tkinter is available.")
except ImportError:
    print("Tkinter is NOT available.")
EOF
  then
    echo "Attempting to enable Tkinter by reinstalling python@3.12..."
    brew reinstall python@3.12
    PY="$(py312_bin)"
    "$PY" - <<'EOF'
try:
    import tkinter
    print("Tkinter is available.")
except ImportError:
    print("Tkinter is NOT available.")
EOF
  fi
}

require_homebrew
ensure_tcl_tk
ensure_python312
test_tk
