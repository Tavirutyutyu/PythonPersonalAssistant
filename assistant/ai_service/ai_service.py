import subprocess
from abc import ABC, abstractmethod
from threading import Event

from config.config import Configuration
from messages.message import Message
from messages.message_history import MessageHistory
from utils import combine_documents, FileLoader, DocumentLoader


class AIService(ABC):
    def __init__(self):
        self._message_history = MessageHistory()
        self.document_loader: FileLoader = DocumentLoader()
        self._process: subprocess.Popen | None = None

    @abstractmethod
    def check_install(self):
        pass

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def generate_answer(self, prompt: str, cancel_event: Event, mode: str = "normal" ,uploaded_file_paths: list | None = None):
        pass

    def initialize(self):
        if not self.check_install():
            self.install()
        self.start()

    def _format_prompt(self, mode:str = "normal", uploaded_file_paths: list | None = None) -> list[dict[str, str]]:
        """Turn message history into a dictionary or JSON format for the AI to understand."""
        return [{"role": "system", "content": Configuration.get_system_prompt(mode)}, *self._message_history.get_messages_as_json_string()]

    def add_message(self, message: Message):
        self._message_history.add_message(message)

    def clear_last_ai_message(self):
        self._message_history.remove_last_ai_message()

    def clear_last_user_message(self):
        self._message_history.remove_last_user_message()

    def del_last_two(self):
        self._message_history.del_last_two()

