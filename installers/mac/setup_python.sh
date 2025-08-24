#!/bin/bash
set -e

if ! command -v brew &> /dev/null; then
  echo "Homebrew not found. Please install it from https://brew.sh/"
  exit 1
fi

if ! brew list tcl-tk &> /dev/null; then
  echo "Installing Tcl/Tk..."
  brew install tcl-tk
else
  echo "Tcl/Tk already installed."
fi

if ! brew list python@3.12 &> /dev/null; then
  echo "Installing Python 3.12..."
  export LDFLAGS="-L$(brew --prefix tcl-tk)/lib"
  export CPPFLAGS="-I$(brew --prefix tcl-tk)/include"
  export PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig"
  brew install python@3.12
  brew link python@3.12 --force
else
  echo "Python 3.12 already installed."
fi

echo "Verifying Tkinter..."
python3.12 -m tkinter || echo "Tkinter test failed."
