from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, *args):
        self.__keywords = list(args)
        self.__sub_options = {}

    def matches(self, text: str) -> bool:
        """Check if this command should handle the given input"""
        return any(word in text.lower() for word in self.__keywords)

    @abstractmethod
    def execute(self, text: str):
        """Perform the command's action and return response text"""
        pass

    def get_sub_options(self) -> list:
        return list(self.__sub_options.keys())