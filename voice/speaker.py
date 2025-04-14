import subprocess

from voice.text_to_speech_base import TextToSpeechBase


class FestivalTTS(TextToSpeechBase):
    def __init__(self):
        self._rate = 1.0
        self._volume = 1.0
        self._buffer = ""

    def set_property(self, name: str, value) -> None:
        if name == "rate":
            self._rate = max(0.5, min(2.0, 200 / value))
        elif name == "volume":
            self._volume = max(0.1, min(2.0, value))
        else:
            print(f"Property '{name}' not supported by FestivalTTS")

    def say(self, text: str) -> None:
        self._buffer += text + "\n"

    def run_and_wait(self) -> None:
        if not self._buffer:
            return

        commands = f"""
(Parameter.set 'Duration_Stretch {self._rate})
(set! duffint_params `((volume {self._volume})))
(SayText "{self._buffer.strip()}")
        """

        try:
            subprocess.run(['festival', '--pipe'], input=commands, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in speech synthesis: {e}")

        self._buffer = ""

    def speak(self, text: str) -> None:
        self.say(text)
        self.run_and_wait()

