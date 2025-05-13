import json
import os
from abc import abstractmethod, ABC
from dataclasses import dataclass


class FileLoader(ABC):
    @abstractmethod
    def load_file(self, file_path: str):
        pass

    def load_files(self, file_paths: list[str]):
        return [self.load_file(file_path) for file_path in file_paths]


class JsonLoader(FileLoader):

    def load_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)


class DocumentLoader(FileLoader):

    def load_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
            filename = os.path.basename(path)
            size_kb = len(data.encode("utf-8")) / 1024
            return Document(name=filename, content=data, size_kb=size_kb)


@dataclass
class Document:
    name: str
    content: str
    size_kb: float

    def __str__(self):
        return f"{self.name}\n{"-" * 60}{self.content}\n{"=" * 60}\n{round(self.size_kb, 2)} Kb\n{"=" * 60}\n"
