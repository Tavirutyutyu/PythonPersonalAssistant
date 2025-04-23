from abc import ABC, abstractmethod


class TextToSpeechManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def check_install(self) -> bool:
        pass

    @abstractmethod
    def install(self):
        pass
