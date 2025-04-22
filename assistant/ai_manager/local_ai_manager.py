import subprocess
from abc import ABC, abstractmethod


class LocalAIManager(ABC):
    def __init__(self):
        self._process: subprocess.Popen | None = None

    @abstractmethod
    def _check_install(self):
        pass

    @abstractmethod
    def _install(self):
        pass

    def start_server(self):
        if not self._check_install():
            self._install()
        self._start_server()

    @abstractmethod
    def _start_server(self):
        pass

    @abstractmethod
    def stop_server(self):
        pass
