import os
from abc import ABC, abstractmethod

from config import RESOURCES_DIR
from utils import JsonLoader
from utils.file_loader import FileLoader


class Command(ABC):
    def __init__(self, name: str, file_name: str, directory_path: str = RESOURCES_DIR, ) -> None:
        """
        You need to provide a file that contains the command's keywords and if needed than sub options.
        For example keywords: open browser, browse, firefox...
        Sub options: Google, YouTube, GitHub...

        :param file_name: The name of the file containing the command's keywords and sub options.
        @type keywords: str
        :param directory_path: The directory where the file is located.
        @type sub_options: str
        """
        file_loader: FileLoader = JsonLoader()
        command_metadata = file_loader.load_file(os.path.join(directory_path, file_name))
        self._name: str = name
        self.__keywords: list[str] = command_metadata["keywords"]
        self.__sub_options: dict[str, str] | None = command_metadata["sub_options"] if "sub_options" in command_metadata else None
        self.has_sub_options: bool = True if self.__sub_options else False

    def matches(self, text: str) -> bool:
        """Check if this command should handle the given input"""
        return any(word in text.lower() for word in self.__keywords)

    @abstractmethod
    def execute(self, text: str | None = None):
        """Perform the command's action and return response text"""
        pass

    def get_sub_options(self) -> dict[str, str]:
        return dict(self.__sub_options)

    def get_sub_option_keys(self) -> list[str]:
        return list(self.__sub_options.keys())

    def get_keywords(self) -> list[str]:
        return list(self.__keywords)

    def __str__(self):
        return self._name
