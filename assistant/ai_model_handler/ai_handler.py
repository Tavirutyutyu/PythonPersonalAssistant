from abc import ABC, abstractmethod

from assistant.coding_buddy.coding_buddy import CodingBuddy
from config import SYSTEM_PROMPT_VOICE, SYSTEM_PROMPT_CODE


class AIHandler(ABC):

    def __init__(self, model:str):
        self._model = model
        self._message_history = []
        self._coding_buddy = CodingBuddy()

    @abstractmethod
    def generate_response(self, prompt:str, mode: str = "assistant", uploaded_file_paths:list | None = None) -> str:
        pass

    def _format_prompt(self, messages: list[dict], mode: str = "assistant", uploaded_file_paths: list | None = None) -> list[dict[str, str]]:
        """Turn message history into a dictionary or JSON format for the AI to understand."""
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
