from tkinter import Tk

import ollama

from GUI.settings_window import SettingsWindow
from voice.tts_service.festival_service import FestivalService
from random import choice



def test_festival_service(text_to_say):
    festival_service = FestivalService()
    voices = festival_service.get_festival_voices()
    festival_service.set_voice_property(voice=choice(voices), speed=1.2)
    festival_service.say(text_to_say)


def test_settings_window():
    window = Tk()
    settings_window = SettingsWindow(window)
    window.mainloop()

def test_ollama_in_hungarian():
    response = ollama.chat(
        model="llama3",
        messages=[{'role': 'user', 'content': 'Mondj egy viccet.'}]
    )
    print(response.message.content)


#test_festival_service("Hello World")
#test_settings_window()
#test_ollama_in_hungarian()
print(FestivalService.get_festival_voices())