import ollama

from config import OLLAMA_MODEL, OLLAMA_URL, SYSTEM_PROMPT_VOICE, SYSTEM_PROMPT_CODE
from .ai_handler import AIHandler


class OllamaHandler(AIHandler):
    def __init__(self, model: str = OLLAMA_MODEL):
        super().__init__(model)
        self.url = OLLAMA_URL

    def generate_response(self, prompt: str, mode: str = "assistant", uploaded_file_paths: list | None = None):
        self._message_history.append(dict(role="user", content=prompt))
        full_prompt = self._format_prompt(self._message_history, mode=mode, uploaded_file_paths=uploaded_file_paths)
        try:
            print(f"{full_prompt=}")
            response = ollama.chat(model=OLLAMA_MODEL, messages=full_prompt)
            return response.message.content
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def _format_prompt(self, messages: list[dict], mode: str = "assistant", uploaded_file_paths: list | None = None) -> list[dict[str, str]]:
        """Turn message history into a dictionary or JSON format for Ollama to understand."""
        formatted_messages = []
        if mode == "assistant":
            formatted_messages.append({"role": "system", "content": SYSTEM_PROMPT_VOICE})
        elif mode == "code":
            formatted_messages.append({"role": "system", "content": SYSTEM_PROMPT_CODE})
            files = self._coding_buddy.get_files_as_string(uploaded_file_paths)
            formatted_messages.append({"role": "system", "content": files})
        for message in messages:
            role = message["role"]
            content = message["content"]
            formatted_messages.append({"role": role, "content": content})
        return formatted_messages
