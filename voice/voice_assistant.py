from speech_recognition import Recognizer, Microphone
from voice.listener import Listener
from voice.speaker import FestivalTTS


class VoiceAssistant:
    def __init__(self, language="en-US"):
        self.__recognizer = Recognizer()
        self.__microphone = Microphone()
        self.language = language

        self.__tts_engine = FestivalTTS()
        self.listener = Listener()
        self.set_voice_properties()

    def set_voice_properties(self, rate:int=150, volume:float=1.0) -> None:
        """
        Sets the speach rate and volume.
        @:param rate: Speech rate.
        @:type rate: int
        @:param volume: Speech volume.
        @:type volume: float
        """
        self.__tts_engine.set_property('rate', rate)
        self.__tts_engine.set_property('volume', volume)

    def listen(self, adjust_duration:int=2, listen_timeout:int=20, phrase_time_limit:int=10) -> str or None:
        """
        Listens for speach with the microphone.
        Returns the recognised text or returns None and speaks the problem.
        :param adjust_duration:
        :param listen_timeout:
        :param phrase_time_limit:
        :return text -> The recognized text or returns None:
        """
        return self.listener.listen(self.__tts_engine, adjust_duration, listen_timeout, phrase_time_limit, self.language)

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