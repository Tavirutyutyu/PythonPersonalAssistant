from typing import Callable

import speech_recognition as sr
from speech_recognition import WaitTimeoutError, UnknownValueError, RequestError

from voice.tts_service.tts_service import TtsService


class Listener:
    def __init__(self, noise_adjusting_time: int = 2, listen_timeout: int = 5, phrase_time_limit: int | None = None, language: str = "en-US") -> None:
        self.__recognizer = sr.Recognizer()
        self.__microphone: sr.Microphone | None = self.__initialise_microphone()
        self.__noise_adjusting_time = noise_adjusting_time
        self.__listen_timeout = listen_timeout
        self.__phrase_time_limit = phrase_time_limit
        self.__language = language

    @staticmethod
    def __initialise_microphone():
        try:
            microphone = sr.Microphone()
            return microphone
        except OSError as e:
            print(f"Microphone not found! Error: {e}")
    
    def set_language(self, language):
        self.__language = language

    # def listen(self, speaker: TtsService, message_displayer: Callable[[str, str], None] | None = None) -> str or None:
    #     with self.__microphone as source:
    #         print("Adjusting to ambient noise")
    #         if message_displayer: message_displayer("System", "Adjusting to ambient noise")
    #         self.__recognizer.adjust_for_ambient_noise(source, duration=self.__noise_adjusting_time)
    #         try:
    #             print("Listening...")
    #             if message_displayer: message_displayer("System", "Listening...")
    #             audio = self.__recognizer.listen(source, timeout=self.__listen_timeout, phrase_time_limit=self.__phrase_time_limit)
    #             if audio.frame_data:
    #                 print("Audio detected")
    #                 return self.__recognizer.recognize_google(audio, language=self.__language)
    #             else:
    #                 print("No audio detected")
    #                 return None
    #         except WaitTimeoutError:
    #             print("⏸ Timeout: No speech detected. Stopping...")
    #             speaker.say("Timeout. No speech detected. Stopping...")
    #             return None
    #         except UnknownValueError:
    #             print("🤷 I couldn’t understand what you said.")
    #             speaker.say("I couldn't understand what you said.")
    #             return None
    #         except RequestError as e:
    #             print(f"❌ Google API error: {e}")
    #             speaker.say("Google API error. Please try again later.")
    #             return None



    def listen(self, speaker: TtsService, message_displayer: Callable[[str, str], None] | None = None) -> str or None:
        with self.__microphone as source:
            if message_displayer: message_displayer("System", "Adjusting to ambient noise")
            self.__recognizer.adjust_for_ambient_noise(source, duration=self.__noise_adjusting_time)
            try:
                if message_displayer: message_displayer("System", "Listening...")
                audio = self.__recognizer.listen(source, timeout=self.__listen_timeout, phrase_time_limit=self.__phrase_time_limit)
                if audio.frame_data:
                    return self.__recognizer.recognize_google(audio, language=self.__language)
                else:
                    return None
            except WaitTimeoutError:
                speaker.say("Timeout. No speech detected. Stopping...")
                return None
            except UnknownValueError:
                speaker.say("I couldn't understand what you said.")
                return None
            except RequestError as e:
                speaker.say("Google API error. Please try again later.")
                return None
