import platform
import shutil
import subprocess
import time
from os import setsid, getpgid, killpg
from signal import SIGTERM
from subprocess import Popen, DEVNULL
from abc import ABC
from pathlib import Path

import ollama

from assistant.ai_service.ai_service import AIService
from configuration import Configuration


class OllamaService(AIService, ABC):

    def generate_answer(self, prompt: str, mode: str = "assistant", uploaded_file_paths: list | None = None):
        self._message_history.append(dict(role="user", content=prompt))
        full_prompt = self._format_prompt(self._message_history, mode=mode, uploaded_file_paths=uploaded_file_paths)
        try:
            print(f"{full_prompt=}")
            response = ollama.chat(model=Configuration.OLLAMA_MODEL, messages=full_prompt)
            self._message_history.append(dict(role="assistant", content=response.message.content))
            return response.message.content
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")


    def check_install(self):
        ollama_installed = shutil.which("ollama") is not None
        llama3_model_path = Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library" / "llama3" / "latest"
        if not ollama_installed: return False
        if not llama3_model_path.exists(): return False
        blobs_path = Path.home() / ".ollama" / "models" / "blobs"
        if not blobs_path.exists() or not any(blobs_path.iterdir()): return False
        if not any(blobs_path.glob("sha256-*")): return False
        return True

    def install(self):
        system = platform.system()
        if system == "Darwin":
            self.__install_mac()
        elif system == "Linux":
            self.__install_linux()
        elif system == "Windows":
            self.__install_windows()

    def start(self):
        if self._process is None:
            self._process = Popen(
                ["ollama", "serve"],
                stdout=DEVNULL,
                stderr=DEVNULL,
                preexec_fn=setsid,
            )
            time.sleep(1.5)

    def stop(self):
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
    def __install_windows():
        try:
            print("Please install Ollama manually from https://ollama.com/download")
            subprocess.run(["start", "https://ollama.com/download"], shell=True)
        except Exception as e:
            print(f"Failed to open browser for Windows install. Error: {e}")

    @staticmethod
    def __install_mac():
        subprocess.run(["brew", "install", "ollama"])