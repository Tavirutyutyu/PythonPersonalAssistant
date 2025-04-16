import subprocess
import webbrowser
from commands.command_base import Command
import utils
from config import RESOURCES_DIR


class HelloCommand(Command):
    def __init__(self):
        command_metadata = utils.load("hello_command.json", RESOURCES_DIR)
        super().__init__(command_metadata["keywords"])

    def execute(self, name: str) -> str:
        return f"Hello {name}! How can i help you?"


class BrowserCommand(Command):
    def __init__(self):
        command_metadata = utils.load("browser_command.json", RESOURCES_DIR)
        super().__init__(keywords=command_metadata["keywords"], sub_options=command_metadata["sub_options"])

    def execute(self, text: str):
        sub_options = self.get_sub_options()
        url = sub_options.get(text.lower(), sub_options["default"])
        webbrowser.open(url)


class LaunchIDECommand(Command):
    def __init__(self):
        command_metadata = utils.load("launch_ide_command.json", RESOURCES_DIR)
        super().__init__(keywords=command_metadata["keywords"], sub_options=command_metadata["sub_options"])

    def execute(self, text: str):
        text = text.lower()
        try:
            sub_options = self.get_sub_options()
            command = sub_options.get(text.lower(), sub_options["default"])
            subprocess.Popen(command)
        except FileNotFoundError as e:
            print(f"IDE not found: {e}")
        except Exception as e:
            print(f"{e.__class__.__name__} error: {e}")
