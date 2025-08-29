import platform
import shutil
import subprocess
import time
from os import setsid, getpgid, killpg
from pathlib import Path
from signal import SIGTERM
from subprocess import Popen, DEVNULL
from threading import Event

import ollama

from assistant.ai_service.ai_service import AIService
from config.config import Configuration
from messages.message import Message


class OllamaService(AIService):

    def generate_answer(self, prompt: str, cancel_event: Event, mode: str = "normal", uploaded_file_paths: list | None = None):
        if cancel_event.is_set():
            print("OllamaService canceled before start.")
            return None

        user_prompt = Message(role="user", message=prompt)
        self._message_history.add_message(user_prompt)

        full_prompt = self._format_prompt(mode=mode, uploaded_file_paths=uploaded_file_paths)

        print(f"{full_prompt=}")

        ai_message = Message(role="assistant", message="...")
        self._message_history.add_message(ai_message)

        try:
            response_text = ""
            for chunk in ollama.chat(model=Configuration.OLLAMA_MODEL, messages=full_prompt, stream=True):
                if cancel_event.is_set():
                    print("OllamaService canceled mid-generation.")
                    self._message_history.remove_message(ai_message.ID)
                    return None
                response_text += chunk["message"]["content"]

            ai_message.set_message(response_text)
            self._message_history.update_message(ai_message.ID, ai_message.get_message())
            return response_text

        except ollama.ResponseError as e:
            print(f"Error: {e}")

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
        script_path = Path(__file__).resolve().parents[2] / "installers" / "linux" / "install_ollama.sh"
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
        script_path = Path(__file__).resolve().parents[2] / "installers" / "mac" / "install_ollama.sh"
        try:
            subprocess.run(["bash", str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")

