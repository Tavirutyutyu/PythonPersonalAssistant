from typing import Callable

from config.config import Configuration
from .listener import Listener
from voice.tts_service import TtsManager
from voice.tts_service import TtsService


class VoiceAssistant:
    def __init__(self, language="en-US"):
        self.language = language
        self.__tts_engine: TtsService = TtsManager.get_installed_service()
        self.listener = Listener()

    def set_voice_properties(self, rate:float=Configuration.TTS["voice_speed"], voice:str = None) -> None:
        """
        You can set the speed of the tts model, or the used voice model.
        The speed has to be a float number. 1.0 is the default speed.
        The voice model has to be the name of the model you want to use. (It needs to be installed.)
        :param rate: The speaking speed.
        :type rate: float
        :param voice: The voice model.
        :type voice: str
        """
        if rate:
            self.__tts_engine.set_voice_property(speed=rate)
        if voice:
            self.__tts_engine.set_voice_property(voice=voice)

    def listen(self, message_displayer: Callable[[str, str], None] | None = None) -> str or None:
        """
        Listens for speach with the microphone.
        Returns the recognised text or returns None and speaks the problem.
        :return text -> The recognized text or returns None:
        """
        return self.listener.listen(self.__tts_engine, message_displayer)

    def speak(self, text:str) -> None:
        """
        Speaks the given text with the given TTS engine.
        :param text: Text to speak.
        """
        try:
            self.__tts_engine.say(text)
        except Exception as e:
            print(f"Error in speech synthesis\t|\t{e}")