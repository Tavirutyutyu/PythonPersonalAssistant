import subprocess
from abc import ABC, abstractmethod

from config import SYSTEM_PROMPT_VOICE, SYSTEM_PROMPT_CODE
from utils import combine_documents, FileLoader, DocumentLoader


class AIService(ABC):
    def __init__(self):
        self._message_history = []
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
    def generate_answer(self, prompt: str, mode: str = "assistant", uploaded_file_paths: list | None = None):
        pass

    def initialize(self):
        if not self.check_install():
            self.install()
        self.start()

    def _format_prompt(self, messages: list[dict], mode: str = "assistant", uploaded_file_paths: list | None = None) ->  list[dict[str, str]]:
        """Turn message history into a dictionary or JSON format for the AI to understand."""
        formatted_messages = []
        if mode == "assistant":
            formatted_messages.append({"role": "system", "content": SYSTEM_PROMPT_VOICE})
        elif mode == "code":
            formatted_messages.append({"role": "system", "content": SYSTEM_PROMPT_CODE})
            file_list = self.document_loader.load_files(uploaded_file_paths)
            files = combine_documents(file_list)
            formatted_messages.append({"role": "system", "content": files})
        for message in messages:
            role = message["role"]
            content = message["content"]
            formatted_messages.append({"role": role, "content": content})
        return formatted_messages


