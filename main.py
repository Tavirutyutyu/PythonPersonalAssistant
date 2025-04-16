from assistant.ollama_handler import OllamaHandler
from commands import CommandManager
from voice import VoiceAssistant

assistant = VoiceAssistant()
command_manager = CommandManager()
ai_handler = OllamaHandler()

def main():
    pass

def test_commands(command, execute_command_text: str):
    print(command.execute(execute_command_text))

def test_command_by_voice():
    assistant.speak("What would you like to do? Browse on the internet or launch an IDE?")
    possible_keywords = command_manager.get_possible_keywords()
    print(f"Possible keywords: {possible_keywords}")
    voice_input = assistant.listen()
    if voice_input:
        assistant.speak(f"You said {voice_input}")
        command = command_manager.match(voice_input)
        if command:
            assistant.speak(f"You choose {command.__class__.__name__}")
            print(f"You choose {command.__class__.__name__}")
            assistant.speak("Choose an option:")
            options = command.get_sub_option_keys()
            print(f"Sub options: {options}")
            for option in options:
                assistant.speak(option)
            voice_option_input = assistant.listen()
            if voice_option_input:
                command.execute(voice_option_input)

def test_ai_handler(prompt:str):
    response = ai_handler.generate_response(prompt)
    print(response)

if __name__ == "__main__":
    #main()
    #test_command_by_voice()
    # executable = command_manager.match("browse")
    # test_commands(executable,  "journey")
    test_ai_handler("What is dependency injection?")