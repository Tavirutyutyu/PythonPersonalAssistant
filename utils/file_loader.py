import json
import os
from abc import abstractmethod, ABC


class FileLoader(ABC):
    def __init__(self, directory:str):
        self._directory = directory

    @abstractmethod
    def load(self, file_name:str, file_directory:str = None ):
        pass


class JsonLoader(FileLoader):
    def __init__(self, directory:str):
        super().__init__(directory)

    def load(self, file_name: str, file_directory: str = None ):
        if file_directory is None:
            file_directory = self._directory
        file_path = os.path.join(file_directory, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
