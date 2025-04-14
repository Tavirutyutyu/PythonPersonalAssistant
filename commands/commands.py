import subprocess
import webbrowser
from commands.command_base import Command


class HelloCommand(Command):
    def __init__(self) -> None:
        super().__init__(["hi", "hello", "hey"])

    def execute(self, name: str) -> str:
        return f"Hello {name}! How can i help you?"


class BrowserCommand(Command):
    def __init__(self) -> None:
        super().__init__(keywords= ["browser", "firefox", "browse", "browse on the internet"],
                         sub_options= {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            "default": "https://www.duckduckgo.com"
        })

    def execute(self, text: str):
        url = self.__sub_options.get(text.lower(), self.__sub_options["default"])
        webbrowser.open(url)


class LaunchIDECommand(Command):
    def __init__(self) -> None:
        super().__init__(keywords=["launch pycharm", "start pycharm", "open pycharm", "launch intellij", "start intellij", "open intellij"],
                         sub_options= {
            "pycharm": "pycharm",
            "intellij": "idea",
            "neovim": "nvim",
            "default": "nvim"
        })

    def execute(self, text: str):
        text = text.lower()
        try:
            command = self.__sub_options.get(text.lower(), self.__sub_options["default"])
            subprocess.Popen(command)
        except FileNotFoundError as e:
            print(f"IDE not found: {e}")
        except Exception as e:
            print(f"Unknown error: {e}")
