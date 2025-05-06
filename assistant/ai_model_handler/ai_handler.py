from abc import ABC, abstractmethod

from assistant.coding_buddy.coding_buddy import CodingBuddy


class AIHandler(ABC):
    def __init__(self, model:str):
        self._model = model
        self._message_history = []
        self._coding_buddy = CodingBuddy()
    @abstractmethod
    def generate_response(self, prompt:str, mode: str = "assistant", root_directory: str | None = None, entry_point:str | None = None) -> str:
        pass
