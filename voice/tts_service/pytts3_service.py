import pyttsx3

from voice.tts_service import TtsService


class Pytts3Service(TtsService):
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)

    def check_install(self):
        return self.engine is not None

    def install(self):
        pass

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def say_a_sentence(self, sentence):
        for word in sentence.split(" "):
            self.engine.say(word)
            self.engine.runAndWait()

    def set_voice_property(self, speed: float = None, voice: str = None):
        pass