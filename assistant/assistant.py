import asyncio
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
        ai_answer = asyncio.run(self.ai_handler.generate_response(voice_input))
        return ai_answer

    def match_command(self, voice_input: str) -> Command | None:
        if voice_input:
            return self.command_manager.match(voice_input)

    def process_user_input(self, voice_input: str,
                           message_displayer: Callable[[str, str], None] | None = None) -> str | None:
        """
        Processes a string as voice input.
        First it checks if the voice input contains any keywords for a command, it executes the command.
        If it cant find any keywords, it just sends the string to the AI to generate an answer to it.
        :return text -> The method will return the AI response text if there was an AI response.
                        Otherwise, it returns the name of the command.
        """
        if voice_input:
            command = self.command_manager.match(voice_input)
            if command:
                self.execute(command, message_displayer)
            else:
                return self.generate_ai_answer(voice_input)

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

    def choose_option(self, command: Command) -> str:
        options = command.get_sub_option_keys()
        for option in options:
            self.voice_assistant.speak(option)
        option_input = self.voice_assistant.listen()
        return option_input.lower()

    def __execute_complex_command(self, command: Command, message_displayer: Callable[[str, str], None]) -> None:
        if message_displayer:
            message_displayer("Assistant", "Choose an option:")

        self.voice_assistant.speak("Choose an option:")
        options = command.get_sub_option_keys()

        if message_displayer:
            message_displayer("Assistant", f"Options: {str(options)}")

        voice_option_input = self.__choose_option(options)

        if voice_option_input and voice_option_input in options:
            print(f"You choose this option: {voice_option_input}")
            command.execute(voice_option_input)

        elif not voice_option_input:
            self.voice_assistant.speak("Could not hear you.")

            if message_displayer:
                message_displayer("Assistant", "Could not hear you.")

        elif voice_option_input not in options:
            print(f"You choose this option: {voice_option_input}")
            self.voice_assistant.speak("Invalid option")

            if message_displayer:
                message_displayer("Assistant", "Invalid option")

    def __choose_option(self, options: list[str]) -> str | None:
        for option in options:
            self.voice_assistant.speak(option)
        voice_option_input = self.voice_assistant.listen()
        if voice_option_input:
            return voice_option_input.lower()
        return None

    def shutdown(self):
        self.voice_assistant.speak("Shutting down the assistant.")
        self.voice_assistant.speak("Good bye!")
        self.local_ai_manager.stop_server()
        sys.exit()
