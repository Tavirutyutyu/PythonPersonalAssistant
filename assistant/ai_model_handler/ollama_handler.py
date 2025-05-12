import ollama

from config import OLLAMA_MODEL
from .ai_handler import AIHandler


class OllamaHandler(AIHandler):
    def __init__(self, model: str = OLLAMA_MODEL):
        super().__init__(model)

    def generate_response(self, prompt: str, mode: str = "assistant", uploaded_file_paths: list | None = None):
        self._message_history.append(dict(role="user", content=prompt))
        full_prompt = self._format_prompt(self._message_history, mode=mode, uploaded_file_paths=uploaded_file_paths)
        try:
            print(f"{full_prompt=}")
            response = ollama.chat(model=OLLAMA_MODEL, messages=full_prompt)
            return response.message.content
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")
