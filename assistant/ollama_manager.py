import time
from os import setsid, killpg, getpgid
from signal import SIGTERM
from subprocess import Popen, DEVNULL

from assistant.local_ai_manager import LocalAIManager


class OllamaManager(LocalAIManager):
    def __init__(self):
        super().__init__()

    def start_server(self):
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