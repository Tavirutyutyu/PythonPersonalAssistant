import platform
import shutil
import subprocess
import time
from os import setsid, killpg, getpgid
from signal import SIGTERM
from subprocess import Popen, DEVNULL

from assistant.ai_manager.local_ai_manager import LocalAIManager


class OllamaManager(LocalAIManager):
    def __init__(self):
        super().__init__()

    def _check_install(self):
        return shutil.which("ollama")

    def _install(self):
        system = platform.system()
        if system == "Darwin":
            self.__install_mac()
        elif system == "Linux":
            self.__install_linux()
        elif system == "Windows":
            self.__install_windows()

    def _start_server(self):
        if self._process is None:
            self._process = Popen(
                ["ollama", "serve"],
                stdout=DEVNULL,
                stderr=DEVNULL,
                preexec_fn=setsid,
            )
            time.sleep(1.5)

    def stop_server(self):
        if self._process is not None:
            killpg(getpgid(self._process.pid), SIGTERM)
            self._process = None


    @staticmethod
    def __install_linux():
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.com/install.sh", "-o", "ollama_install.sh"
            ], check=True)
            subprocess.run(["chmod", "+x", "ollama_install.sh"], check=True)
            subprocess.run(["bash", "ollama_install.sh"], check=True)
            subprocess.run(["ollama", "pull", "llama3"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")

    @staticmethod
    def __install_windows():
        try:
            print("Please install Ollama manually from https://ollama.com/download")
            subprocess.run(["start", "https://ollama.com/download"], shell=True)
        except Exception as e:
            print(f"Failed to open browser for Windows install. Error: {e}")

    @staticmethod
    def __install_mac():
        subprocess.run(["brew", "install", "ollama"])
