import sys

from assistant.ai_handler import AIHandler, OllamaHandler
from assistant.ai_manager import LocalAIManager, OllamaManager
from commands import CommandManager
from commands.command_base import Command
from voice import VoiceAssistant


class Assistant:
    def __init__(self):
        self.local_ai_manager: LocalAIManager = OllamaManager()

        self.ai_handler:AIHandler = OllamaHandler()
        self.command_manager = CommandManager()
        self.voice_assistant = VoiceAssistant()

    def greeting(self):
        self.voice_assistant.speak("Welcome to your personal assistant.")
        self.local_ai_manager.start_server()

    def listen(self):
        voice_input = self.voice_assistant.listen()
        if voice_input:
            print(f"You said: {voice_input}")
            command = self.command_manager.match(voice_input)
            if command:
                self.voice_assistant.speak(f"You choose {command}")
                if command.has_sub_options:
                    self.__execute_complex_command(command)
                else:
                    command.execute()
            else:
                self.voice_assistant.speak("Generating answer with AI.")
                ai_answer = self.ai_handler.generate_response(voice_input)
                self.voice_assistant.speak(ai_answer)

    def __choose_option(self, options: list[str]):
        for option in options:
            self.voice_assistant.speak(option)
        voice_option_input = self.voice_assistant.listen()
        return voice_option_input.lower()

    def __execute_complex_command(self, command: Command):
        self.voice_assistant.speak("Choose an option:")
        options = command.get_sub_option_keys()
        voice_option_input = self.__choose_option(options)
        if voice_option_input and voice_option_input in options:
            command.execute(voice_option_input)
        elif voice_option_input not in options:
            print(f"You choose this option: {voice_option_input}")
            self.voice_assistant.speak("Invalid option")
        elif not voice_option_input:
            self.voice_assistant.speak("Could not hear you.")

    def shutdown(self):
        self.voice_assistant.speak("Shutting down the assistant.")
        self.voice_assistant.speak("Good bye!")
        self.local_ai_manager.stop_server()
        sys.exit()