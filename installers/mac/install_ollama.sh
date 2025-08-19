#!/bin/bash

set -e

if ! command -v ollama &> /dev/null; then
  echo "Ollama not found. Installing..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "Ollama already installed."
fi

if ! pgrep -x "ollama" > /dev/null; then
  echo "Starting ollama daemon..."
  ollama serve &
  sleep 3
fi

if ! ollama list | grep -q "llama3"; then
  echo "Fetching llama3..."
  rm -rf ~/.ollama/models/library/llama3 || true
  ollama pull llama3
else
  echo "llama3 already present."
fi
