from utils.file_loader import DocumentLoader, FileLoader


class CodingBuddy:
    def __init__(self):
        self.document_loader: FileLoader = DocumentLoader()


    def get_files_as_string(self, file_paths: list):
        files = self.document_loader.load_files(file_paths)
        string = ""
        for file in files:
            string += str(file)
        return string

