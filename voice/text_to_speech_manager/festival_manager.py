import platform
import shutil
import subprocess
from pathlib import Path

from voice.text_to_speech_manager import TTSManagerBase
from voice.text_to_speech_handler import FestivalTTS

class FestivalManager(TTSManagerBase):
    def __init__(self):
        super().__init__(FestivalTTS())

    def check_install(self) -> bool:
        return shutil.which("festival") is not None

    def install(self):
        system = platform.system()
        if system == "Linux":
            self.__install_linux()
        elif system == "Darwin":
            self.__install_mac()
        elif system == "Windows":
            self.__install_windows()
        else:
            print("Unsupported OS. Please install Festival manually.")

    @staticmethod
    def __install_linux():
        script_path = Path(__file__).resolve().parents[0] / "installers" / "install_festival_tts.sh"
        try:
            subprocess.run(["bash", str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")


    @staticmethod
    def __install_mac():
        if shutil.which("brew"):
            subprocess.run(["brew", "install", "festival"])
        else:
            print("Homebrew is not installed. Please install it and rerun.")

    @staticmethod
    def __install_windows():
        print("Festival is not officially supported on Windows.")
        print("Consider using another TTS engine like pyttsx3 or install WSL (Linux on Windows) to use Festival.")
