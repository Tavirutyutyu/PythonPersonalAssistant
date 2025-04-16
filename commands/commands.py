import subprocess
import webbrowser

from commands.command_base import Command


class HelloCommand(Command):
    def __init__(self):
        super().__init__(name="hello command", file_name="hello_command.json")

    def execute(self, name: str) -> str:
        return f"Hello {name}! How can i help you?"



class BrowserCommand(Command):
    def __init__(self):
        super().__init__(name="browser command", file_name="browser_command.json")

    def execute(self, text: str):
        sub_options = self.get_sub_options()
        url = sub_options.get(text.lower(), sub_options["default"])
        webbrowser.open(url)


class LaunchIDECommand(Command):
    def __init__(self):
        super().__init__(name="code editor command", file_name="launch_ide_command.json")

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
