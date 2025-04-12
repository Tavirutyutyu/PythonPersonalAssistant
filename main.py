from voice import listener, speaker

def main():
    text = listener.listen()
    if text:
        speaker.speak(f"You said {text}")
        speaker.speak("This is a text test im interested if you can say it all")
    else:
        speaker.speak("Sorry, I don't understand.")

if __name__ == "__main__":
    main()