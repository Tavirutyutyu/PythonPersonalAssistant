#!/bin/bash

set -e

if command -v apt &> /dev/null; then
  sudo apt update
  sudo apt install -y festival
elif command -v dnf &> /dev/null; then
  sudo dnf install -y festival
elif command -v zypper &> /dev/null; then
  sudo zypper install -y festival
elif command -x pacman &> /dev/null; then
  sudo pacman -Sy --noconfirm festival
else
  echo "Linux package manager not recognized. Install Festival manually."
  exit 1
fi
