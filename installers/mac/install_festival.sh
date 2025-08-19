#!/bin/bash

set -e

if ! command -v brew &> /dev/null; then
  echo "Homebrew not found. Please install it from https://brew.sh/"
  exit 1
fi

if ! brew list festival &> /dev/null; then
  echo "Installing Festival..."
  brew install festival
else
  echo "Festival already installed."
fi
