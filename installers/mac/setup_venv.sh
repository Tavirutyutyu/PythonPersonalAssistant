#!/bin/bash
set -e

# Navigate to project root (PythonPersonalAssistant)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# Ensure we are in PythonPersonalAssistant
if [ ! -f "requirements.txt" ]; then
  echo "requirements.txt not found in $PROJECT_ROOT"
  exit 1
fi

# Remove old virtual environment if present
if [ -d ".venv" ]; then
  echo "Removing existing .venv..."
  rm -rf .venv
fi

# Create new virtual environment in project root
echo "Creating new virtual environment..."
python3.12 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment ready."
echo "Run with: source .venv/bin/activate && python main.py"
