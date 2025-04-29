import requests

from config import OLLAMA_MODEL, OLLAMA_URL, SYSTEM_PROMPT_VOICE, SYSTEM_PROMPT_CODE
from .ai_handler import AIHandler


class OllamaHandler(AIHandler):
    def __init__(self, model: str = OLLAMA_MODEL):
        super().__init__(model)
        self.url = OLLAMA_URL

    def generate_response(self, prompt: str, mode: str = "assistant") -> str:
        self._message_history.append(dict(role="user", content=prompt))
        full_prompt = self._format_prompt(self._message_history, mode)

        response = requests.post(self.url, json={
            "model": self._model,
            "prompt": full_prompt,
            "stream": False
        })

        if response.status_code == 200:
            content = response.json().get("response", "").strip()
            self._message_history.append({"role": "assistant", "content": content})
            return content
        else:
            return f"Error: {response.status_code} - {response.text}"

    @staticmethod
    def _format_prompt(messages: list[dict], mode: str = "assistant") -> str:
        """Turn message history into a plain text prompt Ollama understands."""
        prompt = ""
        if mode == "assistant":
            prompt = f"System: {SYSTEM_PROMPT_VOICE}\n"
        elif mode == "code":
            prompt = f"System: {SYSTEM_PROMPT_CODE}\n"
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        return prompt
