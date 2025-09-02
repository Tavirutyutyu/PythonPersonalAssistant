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
        full_prompt = [{"role": "system", "content": Configuration.get_system_prompt(mode)}, *self._message_history.get_messages_as_json_string()]
        if mode == "code":
            file_list = self.document_loader.load_files(uploaded_file_paths)
            files = combine_documents(file_list)
            full_prompt.append({"role": "system", "content": files})
        return full_prompt

    def _prepare_prompt(self, prompt:str, mode:str = "normal", uploaded_file_paths: list | None = None) -> list[dict[str, str]]:
        user_message = Message(role="user", message=prompt)
        self._message_history.add_message(user_message)
        full_prompt = self._format_prompt(mode = mode, uploaded_file_paths=uploaded_file_paths)
        ai_message = Message(role="assistant", message="...")
        self._message_history.add_message(ai_message)
        return full_prompt

    def clear_last_ai_message(self):
        self._message_history.remove_last_ai_message()

    def clear_last_user_message(self):
        self._message_history.remove_last_user_message()

