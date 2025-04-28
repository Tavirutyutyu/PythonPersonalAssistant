import sys
from typing import Callable

from assistant.ai_manager import LocalAIManagerBase, AIManager
from assistant.ai_model_handler import AIHandler
from commands import Command
from commands import CommandManager
from voice import VoiceAssistant


class Assistant:
    def __init__(self):
        """
        The general_ai_manager is responsible for choosing the correct AI manager.
        The local_ai_manager is checking if a specific AI is installed, if not than installs one according to the operating system.
        The local_ai_manager is also providing the ai_handler according to the installed AI.
        The ai_handler is responsible for the communication with the AI.
        The command_manager is providing the command to execute by a keyword.
        The voice_assistant is responsible for the voice recognition and the text-to-speech.
        And on the end of the init we start he local ai server.
        """
        self.general_ai_manager = AIManager()
        self.local_ai_manager: LocalAIManagerBase = self.general_ai_manager.get_installed_manager()
        self.ai_handler: AIHandler = self.local_ai_manager.get_ai_handler()
        self.command_manager = CommandManager()
        self.voice_assistant = VoiceAssistant()
        self.local_ai_manager.start_server()

    def greeting(self):
        self.speak("Welcome to your personal assistant.")

    def speak(self, text: str):
        self.voice_assistant.speak(text)

    def generate_ai_answer(self, voice_input: str, ) -> str | None:
        """
        Accepts a string as an input, and it generates an AI answer.
        :param voice_input: String to generate an AI answer for.
        :return:
        """
        return self.ai_handler.generate_response(voice_input)

    def match_command(self, voice_input: str) -> Command | None:
        """
        Accepts a string as an input, and it checks if it contains any keywords for any commands.
        :param voice_input: String to check for keywords.
        """
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
        """
        Shows the sub-options of a command, calls self.__choose_option() which will return the chosen sub options in a string,
        than we call the self.__evaluate_sub_option_input() which will execute the command with the sub-option.
        :param command: The command to execute.
        :param message_displayer: The method used to display the conversation in text.
        """
        if message_displayer:
            message_displayer("Assistant", "Choose an option:")
        self.speak("Choose an option")
        options = command.get_sub_option_keys()
        if message_displayer:
            message_displayer("Assistant", f"{str(options)}")
        voice_option_input = self.__choose_option(options, message_displayer)
        self.__evaluate_sub_option_input(command, voice_option_input, message_displayer)

    def __evaluate_sub_option_input(self, command: Command, sub_option_input: str,
                                    message_displayer: Callable[[str, str], None]) -> None:
        """
        Gets a command and a sub-option input.
        Then it checks if the sub-option input is valid.
        If it's valid, it executes the command.
        :param command: Command to execute.
        :param sub_option_input: The sub-option input to execute.
        :param message_displayer: The method used to display the conversation in text.
        """

        if sub_option_input:
            options = command.get_sub_option_keys()
            if sub_option_input in options:
                command.execute(sub_option_input)
            else:
                if message_displayer: message_displayer("Assistant", "This option does not exist.")
                self.speak("This option does not exist.")
        else:
            if message_displayer: message_displayer("Assistant", "Could not hear you.")
            self.speak("Could not hear you.")

    def __choose_option(self, options: list[str], message_displayer: Callable[[str, str], None] | None = None) -> str | None:
        """
        Gets a list of sub options. Say them one-by-one.
        Also, if provided than uses the message_displayer method to display the sub options.
        Then it listens for a voice input and returns the chosen sub options.
        :param options : List of sub options (strings).
        :param message_displayer: The method used to display the conversation in text.
        :return: Returns the chosen sub options or None.
        """
        for option in options:
            self.speak(option)
        voice_option_input = self.voice_assistant.listen(message_displayer)
        if voice_option_input:
            return voice_option_input.lower()
        return None

    def shutdown(self):
        """
        shuts down the assistant and the local ai server.
        """
        self.speak("Shutting down the assistant.")
        self.speak("Good bye!")
        self.local_ai_manager.stop_server()
        sys.exit()
