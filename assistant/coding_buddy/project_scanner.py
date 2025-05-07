import os
from dataclasses import dataclass

from .call_graph_builder import CallGraphBuilder


class ProjectScanner:
    def __init__(self):
        self.__excluded_dirs = {"__pycache__", ".git", ".venv", "node_modules", ".idea", ".vscode"}
        self.__project_files= {}
        self.__root_directory = None
        self.call_graph_builder: CallGraphBuilder | None = None
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

    def scan(self, root_directory: str) -> dict[str, str]:
        """Scan the project directory and read all non-binary files, skipping excluded dirs."""
        if root_directory != self.__root_directory:
            self.__root_directory = root_directory
        for dirpath, dirnames, filenames in os.walk(self.__root_directory):
            # Filter out excluded directories
            dirnames[:] = [d for d in dirnames if d not in self.__excluded_dirs]

            for file in filenames:
                rel_dir = os.path.relpath(dirpath, self.__root_directory)
                rel_path = os.path.join(rel_dir, file) if rel_dir != "." else file
                abs_path = os.path.join(dirpath, file)

                try:
                    with open(abs_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.__project_files[rel_path] = content
                except (UnicodeDecodeError, FileNotFoundError):
                    continue  # Skip binary or problematic files
        return self.__project_files

    def get_structure(self, root_directory: str) -> str:
        """Return a string representing the structure of the project."""
        if root_directory != self.__root_directory:
            self.__root_directory = root_directory
        lines = [os.path.basename(self.__root_directory) + "/"]
        for dirpath, dirnames, filenames in os.walk(self.__root_directory):
            dirnames[:] = [d for d in dirnames if d not in self.__excluded_dirs]
            level = dirpath.replace(self.__root_directory, "").count(os.sep)
            indent = "    " * level
            rel_dir = os.path.relpath(dirpath, self.__root_directory)

            if rel_dir != ".":
                lines.append(f"{indent}└── {os.path.basename(dirpath)}/")
                indent += "    "

            for f in sorted(filenames):
                lines.append(f"{indent}└── {f}")
        return "\n".join(lines)

    def build_call_graph(self):
        if self.__project_files:
            self.call_graph_builder = CallGraphBuilder()
            call_graph = self.call_graph_builder.build(self.__project_files)
            return call_graph

    def format_file_structure_for_ai(self) -> str:
        output = f"Project Structure:\n{self.get_structure(self.__root_directory)}\n\n"
        for filename in self.__project_files:
            content = self.__project_files[filename]
            output += f"File: {filename}\n{'-' * 60}\n{content}\n{'-' * 60}\n"
        return output

    def get_project_files(self) -> dict[str, str]:
        """Return a dictionary mapping files to their contents."""
        return self.__project_files
    
    def scan_project_and_format(self, root_directory: str) -> str:
        self.scan(root_directory)
        return self.format_file_structure_for_ai()

@dataclass
class File:
    name: str
    content: str
    size_kb: float