from .file_loader import JsonLoader
from .file_loader import FileLoader
from .file_loader import DocumentLoader
from .threaded import threaded
from .file_loader import Document

def combine_documents(documents: list[Document]) -> str:
    combined = ""
    for document in documents:
        combined += str(document)
    return combined