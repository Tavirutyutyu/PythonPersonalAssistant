from abc import ABC, abstractmethod


class TextToSpeechBase(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        pass

    @abstractmethod
    def set_property(self, name: str, value) -> None:
        pass

    @abstractmethod
    def say(self, text: str) -> None:
        pass

    @abstractmethod
    def run_and_wait(self) -> None:
        pass
