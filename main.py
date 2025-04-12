import voice

speak = voice.speak
listen = voice.listen


def main():
    speak("Welcome to your personal python assistant.")
    text = listen()
    if text:
        speak(f"You said {text}")
    else:
        speak("Sorry, I don't understand.")

if __name__ == "__main__":
    main()
