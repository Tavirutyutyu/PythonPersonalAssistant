from voice import VoiceAssistant

assistant = VoiceAssistant()

def main():
    assistant.speak("Welcome to your personal python assistant.")
    text = assistant.listen()
    if text:
        assistant.speak(f"You said {text}")
    else:
        assistant.speak("Sorry, I don't understand.")


if __name__ == "__main__":
    main()
