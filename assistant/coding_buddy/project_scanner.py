import os
from dataclasses import dataclass


class ProjectScanner:

    @staticmethod
    def scan_specific_files(file_paths: list) -> list:
        files = []
        for file_path in file_paths:
            with open(file_path, "r") as file:
                data = file.read()
                filename = os.path.basename(file_path)
                size_kb = len(data.encode("utf-8")) / 1024
                files.append(File(name=filename, content=data, size_kb=size_kb))
        return files


@dataclass
class File:
    name: str
    content: str
    size_kb: float

    def __str__(self):
        return f"{self.name}\n{"-" * 60}{self.content}\n{"=" * 60}\n{round(self.size_kb, 2)} Kb\n{"=" * 60}\n"
