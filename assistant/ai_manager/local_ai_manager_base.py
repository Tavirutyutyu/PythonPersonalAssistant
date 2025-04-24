import subprocess
from abc import ABC, abstractmethod


class LocalAIManagerBase(ABC):
    def __init__(self):
        self._process: subprocess.Popen | None = None

    @abstractmethod
    def _check_install(self):
        """
        Checks if the user has local ai installed
        """
        pass

    @abstractmethod
    def _install(self):
        """
        If the user don't have local ai installed this method will install it for and operating system.
        """
        pass

    def start_server(self):
        """
        Checks if the user has local ai installed, if not than installs one and then starts the AI local server.
        """
        if not self._check_install():
            self._install()
        self._start_server()

    @abstractmethod
    def _start_server(self):
        """
        This method starts the AI local server.
        """
        pass

    @abstractmethod
    def stop_server(self):
        """
        This method stops the AI local server.
        :return:
        """
        pass
