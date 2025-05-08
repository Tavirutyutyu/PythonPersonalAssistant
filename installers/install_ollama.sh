#!/bin/bash


set -e

curl -fsSL https://ollama.com/install.sh -o ollama_install.sh
chmod +x ollama_install.sh
bash ollama_install.sh &>/dev/null

ollama serve &

for i in {1..10}; do
	sleep 1
	if curl -s http://localhost:11434 > /dev/null; then
		echo "Ollama is ready"
		break
	fi
done


ollama pull llama3
