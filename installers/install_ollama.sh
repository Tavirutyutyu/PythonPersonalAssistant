#!/bin/bash


set -e

if ! command -v ollama &> /dev/null; then
	ehco "Ollama not found. Installing..."
	curl -fsSL https://ollama.com/install.sh -o ollama_install.sh
	chmod +x ollama_install.sh
	bash ollama_install.sh &> /dev/null
	rm -rf ollama_install.sh
else
	echo "Ollama is already installed."
fi


if ! pgrep -x "ollama" > /dev/null; then
	echo "Starting ollama daemon..."
	ollama serve &
	sleep 3
fi

if ! ollama list | grep -q "llama3"; then
	echo "llama3 not found. Cleaning up and re-pulling..."
	rm -rf ~/.ollama/models/library/llama3 || true
	ollama pull llama3
else
	echo "llama3 already present."
fi

