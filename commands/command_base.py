from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, *args):
        self.keywords = list(args)
        self.sub_options = {}

    def matches(self, text: str) -> bool:
        """Check if this command should handle the given input"""
        return any(word in text.lower() for word in self.keywords)

    @abstractmethod
    def execute(self, text: str):
        """Perform the command's action and return response text"""
        pass

    def get_sub_options(self) -> list:
        return list(self.sub_options.keys())