from assistant.coding_buddy import ProjectScanner


class CodingBuddy:
    def __init__(self):
        self.project_scanner: ProjectScanner = ProjectScanner()


    def get_files_as_string(self, file_paths: list):
        files = self.project_scanner.scan_specific_files(file_paths)
        string = ""
        for file in files:
            string += str(file)
        return string

