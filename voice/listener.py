import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎙 Adjusting for ambient noise... Please be quiet for a moment.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"📝 Ambient noise level: {recognizer.energy_threshold}")

        print("🎙 Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)  # Adjust timeout as needed
            if audio.frame_data:
                print("🔊 Audio detected.")
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"🧠 You said: {text}")
                return text
            else:
                print("❌ No audio captured.")
                return None

        except sr.WaitTimeoutError:
            print("⏸ Timeout: No speech detected. Stopping...")
            return None
        except sr.UnknownValueError:
            print("🤷 I couldn’t understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"❌ Google API error: {e}")
            return None

