#!/usr/bin/env bash
set -euo pipefail

doc() { cat <<'DOC'
project_root: Ascends to the project’s root (3 levels up).
check_requirements: Ensures requirements.txt exists.
remove_old_venv: Deletes .venv if already present.
create_venv: Creates a new venv with python3.12.
install_dependencies: Installs pip, requirements.txt.
DOC
}

project_root() {
  local script_dir project_root
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  project_root="$(cd "$script_dir/../../.." && pwd)"
  cd "$project_root"
}

check_requirements() {
  if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found in $(pwd)"
    exit 1
  fi
}

remove_old_venv() {
  if [ -d ".venv" ]; then
    echo "Removing existing .venv..."
    rm -rf .venv
  fi
}

create_venv() {
  echo "Creating new virtual environment with python3.12..."
  python3.12 -m venv .venv
  source .venv/bin/activate
}

install_dependencies() {
  echo "Upgrading pip and installing dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
}

project_root
check_requirements
remove_old_venv
create_venv
install_dependencies

echo "Virtual environment ready."
echo "Activate with: source .venv/bin/activate"
echo "Run with: python main.py"
