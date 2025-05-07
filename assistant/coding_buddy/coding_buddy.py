from assistant.coding_buddy import ProjectScanner
from assistant.coding_buddy.call_graph_builder import CallGraphBuilder
from assistant.coding_buddy.file_collector import FileCollector


class CodingBuddy:
    def __init__(self):
        self.project_scanner: ProjectScanner = ProjectScanner()
        self.call_graph_builder: CallGraphBuilder = CallGraphBuilder()
        self.file_collector: FileCollector = FileCollector()
        self.files = None
        self.graph = None
        self.necessary_files = None


    def combine_files(self, file_paths: list) -> str:
        files = self.project_scanner.scan_specific_files(file_paths)
        combined = ""
        total_file_size = 0
        for file in files:
            combined += f"{file.name}\n\n{"-"*60}\n\n{file.content}\n\n{"="*60}\n\n"
            total_file_size += file.size_kb
        combined += f"Files total size: {round(total_file_size, 2)} Kb\n\n{"="*60}\n\n"
        return combined

    def generate_project_string(self, root_directory: str, entry_point) -> str:
        files = self.get_project_files(root_directory)
        graph = self.get_call_graph(files)
        project_structure = self.get_project_structure(root_directory)
        self.get_necessary_file_names(graph, [entry_point])
        formatted_string = self.get_needed_content(project_structure, files)
        return formatted_string


    def get_project_structure(self, root_directory: str) -> str:
        output = f"Project Structure:\n{self.project_scanner.get_structure(root_directory)}\n\n"
        return output

    def get_project_files(self, folder_path) -> dict[str, str]:
        self.project_scanner.scan(folder_path)
        project_files = self.project_scanner.get_project_files()
        self.files = project_files
        return project_files

    def get_needed_content(self,project_structure: str, full_content: dict):
        return_string = project_structure
        if self.necessary_files:
            for file in self.necessary_files:
                return_string += f"File Name: {file}\n\n{"-"*60}\n\n{full_content[file]}\n\n{"="*60}\n\n"
        return return_string


    def get_call_graph(self, project_files):
        call_graph = self.call_graph_builder.build(project_files)
        self.graph = call_graph
        return call_graph

    def get_necessary_file_names(self, call_graph, entry_point) -> list[str]:
        necessary_files = self.file_collector.get_needed_files(call_graph, entry_point)
        self.necessary_files = necessary_files
        return list(necessary_files)
