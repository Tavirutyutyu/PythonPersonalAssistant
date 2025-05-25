from abc import ABC, abstractmethod
class TtsService(ABC):

    @abstractmethod
    def check_install(self):
        pass

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def say(self, text):
        pass

    @abstractmethod
    def set_voice_property(self, speed: float = None, voice: str = None):
        pass

