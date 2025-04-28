import subprocess
from abc import ABC, abstractmethod

from ..ai_model_handler import AIHandler

class LocalAIManagerBase(ABC):
    def __init__(self, ai_handler:AIHandler):
        self._ai_handler: AIHandler = ai_handler
        self._process: subprocess.Popen | None = None

    @abstractmethod
    def check_install(self):
        """
        Checks if the user has local ai installed
        """
        pass

    @abstractmethod
    def install(self):
        """
        If the user don't have local ai installed this method will install it for and operating system.
        """
        pass

    def start_server(self):
        """
        Checks if the user has local ai installed, if not than installs one and then starts the AI local server.
        """
        if not self.check_install():
            self.install()
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

    def get_ai_handler(self) -> AIHandler:
        return self._ai_handler
