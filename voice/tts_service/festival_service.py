import platform
import shutil
import subprocess
from pathlib import Path

from config import Configuration
from voice.tts_service.tts_service import TtsService


class FestivalService(TtsService):
    def __init__(self):
        self.speed = Configuration.TTS["voice_speed"]
        self.voice = Configuration.TTS["voice_model"]

    def check_install(self):
        return shutil.which("festival") is not None

    def install(self):
        system = platform.system()
        if system == "Windows":
            self.install_windows()
        elif system == "Darwin":
            self.install_mac()
        elif system == "Linux":
            self.install_linux()
        else:
            print("Unsupported os")

    def say(self, text):
        speed = Configuration.TTS["voice_speed"]
        voice_model = Configuration.TTS["voice_model"]
        scheme_script = ""
        if self.voice is not None:
            print(f"{voice_model=}")
            scheme_script += f"(voice_{voice_model})\n"
        if self.speed is not None:
            scheme_script += f"(Parameter.set 'Duration_Stretch {self.speed})\n"
        scheme_script += f'(SayText "{text}")\n(quit)'
        subprocess.run(["festival", "--pipe"], input=scheme_script.encode(), check=True)


    def set_voice_property(self, speed: float = None, voice: str = None) -> None:
        if voice:
            self.voice = f"voice_{voice}"
        if speed is not None:
            duration_stretch = 1.0 / speed if speed != 0 else 1.0
            self.speed = duration_stretch

    def calculate_speed(self, speed):
        duration_stretch = 1.0 / speed if speed != 0 else 1.0
        self.speed = duration_stretch

    @staticmethod
    def get_festival_voices():
        process = subprocess.Popen(
            ['festival', '--interactive'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        process.stdin.write('(voice.list)\n(quit)\n')
        process.stdin.flush()
        output, _ = process.communicate()

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("festival> (") and line.endswith(")"):
                return line.removeprefix("festival> ").strip("()").split()
        return []


    @staticmethod
    def install_windows():
        print("Festival is not officially supported on Windows.")
        print("Consider using another TTS engine like pyttsx3 or install WSL (Linux on Windows) to use Festival.")


    @staticmethod
    def install_linux():
        script_path = Path(__file__).resolve().parents[0] / "installers" / "install_festival_tts.sh"
        try:
            subprocess.run(["bash", str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")


    @staticmethod
    def install_mac():
        if shutil.which("brew"):
            subprocess.run(["brew", "install", "festival"])
        else:
            print("Homebrew is not installed. Please install it and rerun.")
