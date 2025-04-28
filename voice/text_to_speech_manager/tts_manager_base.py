from abc import ABC, abstractmethod

from voice.text_to_speech_handler import TextToSpeechBase


class TTSManagerBase(ABC):
    def __init__(self, tts_model:TextToSpeechBase):
        self._tts_model: TextToSpeechBase = tts_model

    @abstractmethod
    def check_install(self) -> bool:
        pass

    @abstractmethod
    def install(self):
        pass

    def get_tts_model(self) -> TextToSpeechBase:
        return self._tts_model