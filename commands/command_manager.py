from commands.command_base import Command
from commands.commands import HelloCommand, BrowserCommand, LaunchIDECommand


class CommandManager:
    def __init__(self):
        self.__commands = self.initialise_commands()

    @staticmethod
    def initialise_commands():
        all_commands = [HelloCommand(), BrowserCommand(), LaunchIDECommand()]
        return all_commands

    def match(self, match_text:str) -> Command or None:
        for command in self.__commands:
            if command.matches(match_text):
                return command


    def match_and_execute(self, match_text: str, execute_text: str):
        command = self.match(match_text)
        if command:
            command.execute(execute_text)
        else:
            print("Command not found")

    def get_possible_keywords(self):
        keywords = []
        for command in self.__commands:
            keywords.append(command.get_keywords())


