import speech_recognition as sr
from speech_recognition import WaitTimeoutError, UnknownValueError, RequestError

from voice.text_to_speech_base import TextToSpeechBase


class Listener:
    def __init__(self, noise_adjusting_time: int = 2, listen_timeout: int = 5, phrase_time_limit: int = 10, language: str = "en-US") -> None:
        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone()
        self.__noise_adjusting_time = noise_adjusting_time
        self.__listen_timeout = listen_timeout
        self.__phrase_time_limit = phrase_time_limit
        self.__language = language

    def listen(self, speaker: TextToSpeechBase) -> str or None:
        with self.__microphone as source:
            print("Adjusting to ambient noise")
            self.__recognizer.adjust_for_ambient_noise(source, duration=self.__noise_adjusting_time)
            try:
                print("Listening...")
                audio = self.__recognizer.listen(source, timeout=self.__listen_timeout, phrase_time_limit=self.__phrase_time_limit)
                if audio.frame_data:
                    print("Audio detected")
                    return self.__recognizer.recognize_google(audio, language=self.__language)
                else:
                    print("No audio detected")
                    return None
            except WaitTimeoutError:
                print("⏸ Timeout: No speech detected. Stopping...")
                speaker.speak("Timeout. No speech detected. Stopping...")
                return None
            except UnknownValueError:
                print("🤷 I couldn’t understand what you said.")
                speaker.speak("I couldn't understand what you said.")
                return None
            except RequestError as e:
                print(f"❌ Google API error: {e}")
                speaker.speak("Google API error. Please try again later.")
                return None
