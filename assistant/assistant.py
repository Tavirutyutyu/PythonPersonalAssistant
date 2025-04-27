import sys
from typing import Callable

from assistant.ai_handler import AIHandler, OllamaHandler
from assistant.ai_manager import LocalAIManagerBase, OllamaManagerBase
from commands import Command
from commands import CommandManager
from voice import VoiceAssistant


class Assistant:
    def __init__(self):
        self.local_ai_manager: LocalAIManagerBase = OllamaManagerBase()
        self.ai_handler: AIHandler = OllamaHandler()
        self.command_manager = CommandManager()
        self.voice_assistant = VoiceAssistant()
        self.local_ai_manager.start_server()

    def greeting(self):
        self.voice_assistant.speak("Welcome to your personal assistant.")

    def speak(self, text: str):
        self.voice_assistant.speak(text)

    def generate_ai_answer(self, voice_input: str, ) -> str | None:
        return self.ai_handler.generate_response(voice_input)

    def match_command(self, voice_input: str) -> Command | None:
        if voice_input:
            return self.command_manager.match(voice_input)

    def listen(self, message_displayer: Callable[[str, str], None] | None = None) -> str | None:
        """Listens with the microphone and returns the recognized text or returns None
        :return text -> The recognized text or returns None:"""
        voice_input = self.voice_assistant.listen(message_displayer)
        return voice_input.lower().strip() if voice_input else None

    def execute(self, command: Command, message_displayer: Callable[[str, str], None] | None = None) -> None:
        """
        Gets a command, check if it has sub options, if it has, it runs execute_complex_command method,
        else it executes the command.
        :param command: The command to execute.
        :param message_displayer: The method used to display the conversation in text.
        """
        if command.has_sub_options:
            self.__execute_complex_command(command, message_displayer)
        else:
            command.execute()

    def __execute_complex_command(self, command: Command, message_displayer: Callable[[str, str], None] = None) -> None:
        if message_displayer:
            message_displayer("Assistant", "Choose an option:")
        self.voice_assistant.speak("Choose an option")
        options = command.get_sub_option_keys()
        if message_displayer:
            message_displayer("Assistant", f"{str(options)}")
        voice_option_input = self.__choose_option(options, message_displayer)
        self.__evaluate_sub_option_input(command, voice_option_input, message_displayer)

    def __evaluate_sub_option_input(self, command: Command, sub_option_input: str, message_displayer: Callable[[str, str], None]) -> None:
        if sub_option_input:
            options = command.get_sub_option_keys()
            if sub_option_input in options:
                command.execute(sub_option_input)
            else:
                if message_displayer: message_displayer("Assistant", "This option does not exist.")
                self.voice_assistant.speak("This option does not exist.")
        else:
            if message_displayer: message_displayer("Assistant", "Could not hear you.")
            self.voice_assistant.speak("Could not hear you.")


    def __choose_option(self, options: list[str], message_displayer: Callable[[str, str], None] | None = None) -> str | None:
        for option in options:
            self.voice_assistant.speak(option)
        voice_option_input = self.voice_assistant.listen(message_displayer)
        if voice_option_input:
            return voice_option_input.lower()
        return None

    def shutdown(self):
        self.voice_assistant.speak("Shutting down the assistant.")
        self.voice_assistant.speak("Good bye!")
        self.local_ai_manager.stop_server()
        sys.exit()
