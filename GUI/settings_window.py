from tkinter import Toplevel, ttk, Label, Button

from config.config import Configuration
from voice.tts_service import FestivalService


class SettingsWindow(Toplevel):
    voice_model_options = FestivalService.get_festival_voices()

    def __init__(self, window=None):
        super().__init__(window)
        self.voice_model_label = Label(self, text="Voice Model: ")
        self.voice_model_dropdown = ttk.Combobox(self, values=self.voice_model_options, state="readonly")
        self.voice_model_dropdown.set(self.voice_model_options[0])
        self.user_language_dropdown_label = Label(self, text="Language: ")
        self.user_language_dropdown = ttk.Combobox(self, values=Configuration.USER_INPUT_LANGUAGES, state="readonly")
        self.user_language_dropdown.set(Configuration.USER_INPUT_LANGUAGES[0])
        self.system_language_dropdown_label = Label(self, text="Language: ")
        self.system_language_dropdown = ttk.Combobox(self, values=Configuration.SYSTEM_OUTPUT_LANGUAGES,state="readonly")
        self.system_language_dropdown.set(Configuration.SYSTEM_OUTPUT_LANGUAGES[0])
        self.submit_button = Button(self, text="Submit", command=self.submit)
        self.withdraw()
        
    def open(self):
        self.voice_model_label.grid(column=0, row=0)
        self.voice_model_dropdown.grid(column=1, row=0)
        self.user_language_dropdown_label.grid(column=0, row=1)
        self.user_language_dropdown.grid(column=1, row=1)
        self.system_language_dropdown_label.grid(column=0, row=2)
        self.system_language_dropdown.grid(column=1, row=2)
        self.submit_button.grid(column=0, row=3, rowspan=2)
        self.deiconify()
        self.grab_set()
        self.wait_window()


    def submit(self):
        voice_model = self.voice_model_dropdown.get()
        user_language = self.user_language_dropdown.get()
        system_language = self.system_language_dropdown.get()

        print(f"{voice_model=}")
        print(f"{user_language=}")
        print(f"{system_language=}")

        self.grab_release()
        self.withdraw()