from abc import ABC, abstractmethod

from assistant.coding_buddy import ProjectScanner


class AIHandler(ABC):
    def __init__(self, model:str):
        self._model = model
        self._message_history = []
        self._project_scanner = ProjectScanner()
    @abstractmethod
    def generate_response(self, prompt:str, mode: str = "assistant", root_directory: str | None = None) -> str:
        pass
