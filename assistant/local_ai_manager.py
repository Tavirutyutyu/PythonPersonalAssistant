import subprocess
from abc import ABC, abstractmethod


class LocalAIManager(ABC):
    def __init__(self):
        self._process: subprocess.Popen | None = None

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def stop_server(self):
        pass
