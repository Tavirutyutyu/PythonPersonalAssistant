from assistant import Assistant


def main():
    assistant = Assistant()
    try:
        assistant.greeting()
        while True:
            assistant.listen()
    except KeyboardInterrupt:
        print("Bye")
    finally:
        assistant.shutdown()

def test_commands(command, execute_command_text: str):
    print(command.execute(execute_command_text))

def test_command_by_voice(voice_assistant, command_manager):
    voice_assistant.speak("What would you like to do? Browse on the internet or launch an IDE?")
    possible_keywords = command_manager.get_possible_keywords()
    print(f"Possible keywords: {possible_keywords}")
    voice_input = voice_assistant.listen()
    if voice_input:
        voice_assistant.speak(f"You said {voice_input}")
        command = command_manager.match(voice_input)
        if command:
            voice_assistant.speak(f"You choose {command.__class__.__name__}")
            print(f"You choose {command.__class__.__name__}")
            voice_assistant.speak("Choose an option:")
            options = command.get_sub_option_keys()
            print(f"Sub options: {options}")
            for option in options:
                voice_assistant.speak(option)
            voice_option_input = voice_assistant.listen()
            if voice_option_input:
                command.execute(voice_option_input)

def test_ai_handler(ai_handler, prompt:str):
    response = ai_handler.generate_response(prompt)
    print(response)

if __name__ == "__main__":
    main()
