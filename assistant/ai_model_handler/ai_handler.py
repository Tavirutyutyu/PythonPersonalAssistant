from abc import ABC, abstractmethod


class AIHandler(ABC):
    def __init__(self, model:str):
        self._model = model
        self._message_history = []
    @abstractmethod
    def generate_response(self, prompt:str, mode: str = "assistant") -> str:
        pass
