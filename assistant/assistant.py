import asyncio
import sys

from assistant.ai_handler import AIHandler, OllamaHandler
from assistant.ai_manager import LocalAIManagerBase, OllamaManagerBase
from commands import CommandManager
from commands import Command
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

    def generate_ai_answer(self, voice_input: str, voice_on: bool = False) -> str | None:
        ai_answer = asyncio.run(self.ai_handler.generate_response(voice_input))
        if voice_on:
            self.voice_assistant.speak(ai_answer)
        return ai_answer

    def process_user_input(self, voice_input: str) -> None:
        """
        Processes a string as voice input.
        First it checks if the voice input contains any keywords for a command, it executes the command.
        If it cant find any keywords, it just sends the string to the ai to generate an answer to it.
        """
        if voice_input:
            command = self.command_manager.match(voice_input)
            if command:
                self.__execute(command)
            else:
                self.generate_ai_answer(voice_input, voice_on=True)

    def listen(self) -> str | None:
        """Listens with the microphone and returns the recognized text or returns None
        :return text -> The recognized text or returns None:"""
        voice_input = self.voice_assistant.listen()
        return voice_input

    def __execute(self, command: Command | None) -> None:
        """
        Gets a command, check if it has sub options, if it has, it runs execute_complex_command method,
        else it executes the command.
        :param command: The command to execute
        """
        if command.has_sub_options:
            self.__execute_complex_command(command)
        else:
            command.execute()

    def __execute_complex_command(self, command: Command):
        self.voice_assistant.speak("Choose an option:")
        options = command.get_sub_option_keys()
        voice_option_input = self.__choose_option(options)
        if voice_option_input and voice_option_input in options:
            command.execute(voice_option_input)
        elif not voice_option_input:
            self.voice_assistant.speak("Could not hear you.")
        elif voice_option_input not in options:
            print(f"You choose this option: {voice_option_input}")
            self.voice_assistant.speak("Invalid option")

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
