from config import TTS_VOICE_SPEED, TTS_VOICE_VOLUME
from voice import Listener
from voice import FestivalTTS
from voice import TextToSpeechBase


class VoiceAssistant:
    def __init__(self, language="en-US"):
        self.language = language
        self.__tts_engine: TextToSpeechBase = FestivalTTS()
        self.listener = Listener()
        self.set_voice_properties()

    def set_voice_properties(self, rate:int=TTS_VOICE_SPEED, volume:float=TTS_VOICE_VOLUME) -> None:
        """
        Sets the speach rate and volume.
        @:param rate: Speech rate.
        @:type rate: int
        @:param volume: Speech volume.
        @:type volume: float
        """
        self.__tts_engine.set_property('rate', rate)
        self.__tts_engine.set_property('volume', volume)

    def listen(self) -> str or None:
        """
        Listens for speach with the microphone.
        Returns the recognised text or returns None and speaks the problem.

        :return text -> The recognized text or returns None:
        """
        return self.listener.listen(self.__tts_engine)

    def speak(self, text:str) -> None:
        """
        Speaks the given text with the given TTS engine.
        :param text: Text to speak.
        """
        try:
            self.__tts_engine.say(text)
            self.__tts_engine.run_and_wait()
        except Exception as e:
            print(f"Error in speech synthesis\t|\t{e}")