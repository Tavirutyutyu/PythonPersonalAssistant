from assistant.ai_handler import AIHandler
from config import OLLAMA_MODEL, OLLAMA_URL

import requests

class OllamaHandler(AIHandler):
    def __init__(self, model: str = OLLAMA_MODEL):
        super().__init__(model)
        self.url = OLLAMA_URL

    def generate_response(self, prompt: str) -> str:
        response = requests.post(self.url, json={
            "model": self._model,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Error: {response.status_code} - {response.text}"