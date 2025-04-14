from commands import CommandManager
from voice import VoiceAssistant

assistant = VoiceAssistant()
command_manager = CommandManager()

def main():
    assistant.speak("Welcome to your personal python assistant.")
    text = assistant.listen()
    if text:
        print(text)
        assistant.speak(f"You said {text}")
    else:
        assistant.speak("Sorry, I don't understand.")

def test_commands(command, input_text: str, execute_command_text: str):
    if command.matches(input_text):
        print(command.execute(execute_command_text))

def test_command_by_voice():
    assistant.speak("What would you like to do? Browse on the internet or launch an IDE?")
    voice_input = assistant.listen()
    if voice_input:
        assistant.speak(f"You said {voice_input}")
        command = command_manager.match(voice_input)
        if command:
            assistant.speak(f"You choose {command.__class__.__name__}")
            assistant.speak("Choose an option:")
            options = command.get_sub_options()
            for option in options:
                assistant.speak(option)
            voice_option_input = assistant.listen()
            if voice_option_input:
                command.execute(voice_option_input)


if __name__ == "__main__":
    #main()
    test_command_by_voice()
    #test_commands(command_manager.match("open intellij"), "open intellij", "intellij")