#!/bin/bash

set -e

# Check for Ollama
if ! command -v ollama &> /dev/null; then
  echo "Ollama not found. Installing via Homebrew..."
  if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Please install Homebrew first: https://brew.sh"
    exit 1
  fi
  brew install ollama
else
  echo "Ollama already installed."
fi

# Ensure Ollama service is running
if ! pgrep -x "ollama" > /dev/null; then
  echo "Starting Ollama service..."
  brew services start ollama
  sleep 5
fi

# Ensure llama3 model is present
if ! ollama list | grep -q "llama3"; then
  echo "Fetching llama3..."
  ollama pull llama3
else
  echo "llama3 already present."
fi
