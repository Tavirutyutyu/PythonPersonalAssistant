from ai_handler import AIHandler, OllamaHandler
from ai_manager import LocalAIManager, OllamaManager
from commands import CommandManager
from voice import VoiceAssistant


class Assistant:
    def __init__(self):
        self.local_ai_manager: LocalAIManager = OllamaManager()
        self.local_ai_manager.start_server()

        self.ai_handler:AIHandler = OllamaHandler()
        self.command_manager = CommandManager()
        self.voice_assistant = VoiceAssistant()

    def greeting(self):
        self.voice_assistant.speak("Welcome to your personal assistant.")

    def listen(self):
        voice_input = self.voice_assistant.listen()
        if voice_input:
            print(f"You said: {voice_input}")
            command = self.command_manager.match(voice_input)
            if command:
                self.voice_assistant.speak(f"You choose {command}")
                self.voice_assistant.speak("Choose an option:")
                options = command.get_sub_option_keys()
                for option in options:
                    self.voice_assistant.speak(option)
                voice_option_input = self.voice_assistant.listen().lower()

                if voice_option_input and voice_option_input in options:
                    command.execute(voice_option_input)
                elif voice_option_input not in options:
                    print(f"You choose this option: {voice_option_input}")
                    self.voice_assistant.speak("Invalid option")
                elif not voice_option_input:
                    self.voice_assistant.speak("Could not hear you.")
            else:
                self.voice_assistant.speak("Generating answer with ai.")
                ai_answer = self.ai_handler.generate_response(voice_input)
                self.voice_assistant.speak(ai_answer)

    def shutdown(self):
        self.voice_assistant.speak("Shutting down the assistant.")
        self.local_ai_manager.stop_server()
