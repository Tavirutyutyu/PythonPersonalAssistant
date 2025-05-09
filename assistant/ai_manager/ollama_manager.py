import platform
import shutil
import subprocess
import time
from pathlib import Path
from os import setsid, killpg, getpgid
from signal import SIGTERM
from subprocess import Popen, DEVNULL

from .local_ai_manager_base import LocalAIManagerBase
from ..ai_model_handler import OllamaHandler


class OllamaManager(LocalAIManagerBase):
    def __init__(self):
        super().__init__(OllamaHandler())

    def check_install(self):
        ollama_installed = shutil.which("ollama") is not None
        llama3_model_path = Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library" / "llama3" / "latest" 
        if not ollama_installed:
            return False

        if not llama3_model_path.exists():
            return False

        blobs_path = Path.home() / ".ollama" / "models" / "blobs"
        if not blobs_path.exists() or not any(blobs_path.iterdir()):
            return False

        if not any(blobs_path.glob("sha256-*")):
            return False

        return True

    def install(self):
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
        script_path = Path(__file__).resolve().parents[2] / "installers" / "install_ollama.sh"
        try:
            subprocess.run(["bash", str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")

    @staticmethod
    def _check_server_status():
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost/11434/health"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                return True
        except subprocess.CalledProcessError:
            return False
        return False

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
