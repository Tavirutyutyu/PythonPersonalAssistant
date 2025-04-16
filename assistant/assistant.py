from assistant.ollama_handler import OllamaHandler
from commands import CommandManager
from voice import VoiceAssistant


class Assistant:
    def __init__(self):
        self.ai_handler = OllamaHandler()
        self.command_manager = CommandManager()
        self.voice_assistant = VoiceAssistant()

    def greeting(self):
        self.voice_assistant.speak("Welcome to your personal assistant.")

    def listen(self):
        voice_input = self.voice_assistant.listen()
        if voice_input:
            command = self.command_manager.match(voice_input)
            if command:
                self.voice_assistant.speak(f"You choose {command.__class__.__name__}")
                self.voice_assistant.speak("Choose an option:")
                options = command.get_sub_option_keys()
                for option in options:
                    self.voice_assistant.speak(option)
                voice_option_input = self.voice_assistant.listen()

                if voice_option_input and voice_option_input in options:
                    command.execute(voice_option_input.lower())
                elif voice_option_input not in options:
                    self.voice_assistant.speak("Invalid option")
                elif not voice_option_input:
                    self.voice_assistant.speak("Could not hear you.")
            else:
                ai_answer = self.ai_handler.generate_response(voice_input)
                self.voice_assistant.speak(ai_answer)
