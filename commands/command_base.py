from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, keywords:list[str], sub_options:dict[str, str] = None) -> None:
        """
        You need to provide keywords and if needed than sub options.
        For example keywords: open browser, browse, firefox...
        Sub options: Google, YouTube, GitHub...

        :param keywords: These keywords trigger the command.
        @type keywords: list[str]
        :param sub_options: These are the sub options of this command.
        @type sub_options: dict[str, str]
        """
        self.__keywords = keywords
        self.__sub_options = sub_options

    def matches(self, text: str) -> bool:
        """Check if this command should handle the given input"""
        return any(word in text.lower() for word in self.__keywords)

    @abstractmethod
    def execute(self, text: str):
        """Perform the command's action and return response text"""
        pass

    def get_sub_options(self) -> dict[str, str]:
        return dict(self.__sub_options)

    def get_sub_option_keys(self) -> list[str]:
        return list(self.__sub_options.keys())

    def get_keywords(self) -> list[str]:
        return list(self.__keywords)