from typing import Callable

from config import TTS_VOICE_SPEED
from voice.listener import Listener
from voice.tts_service import TtsManager
from voice.tts_service import TtsService


class VoiceAssistant:
    def __init__(self, language="en-US"):
        self.language = language
        self.__tts_engine: TtsService = TtsManager.get_installed_service()
        self.listener = Listener()

    def set_voice_properties(self, rate:int=TTS_VOICE_SPEED, voice:str = None) -> None:
        """
        #TODO rewrite the documentation
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