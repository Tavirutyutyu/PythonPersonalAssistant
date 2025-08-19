#!/bin/bash

set -e

if ! command -v brew &> /dev/null; then
  echo "Homebrew not found. Please install it from https://brew.sh/"
  exit 1
fi

if ! brew list python@3.11 &> /dev/null; then
  echo "Installing Python 3.11..."
  brew install python@3.11
else
  echo "Python 3.11 already installed."
fi

echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
echo "Setup complete. Run with: source .venv/bin/activate && python3 main.py"
