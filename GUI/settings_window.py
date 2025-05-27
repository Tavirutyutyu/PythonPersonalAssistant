from tkinter import Toplevel, ttk, Label, Button, ttk

from config.config import Configuration
from voice.tts_service import FestivalService


class SettingsWindow(Toplevel):
    voice_model_options = FestivalService.get_festival_voices()

    def __init__(self, window=None):
        super().__init__(window)
        self.voice_model_label = Label(self, text="Voice Model: ")
        self.voice_model_dropdown = ttk.Combobox(self, values=self.voice_model_options, state="readonly")
        self.voice_model_dropdown.set(self.voice_model_options[0])

        self.voice_speed_label = Label(self, text="Voice Speed: ")
        self.voice_speed_input = ttk.Spinbox(self, from_=0, to=3, increment=0.1)
        self.voice_speed_input.set(1.0)

        self.font_size_label = Label(self, text="Font Size: ")
        self.font_size_input = ttk.Spinbox(self, from_=0, to=100, increment=1)
        self.font_size_input.set(12)

        self.submit_button = Button(self, text="Submit", command=self.submit)
        self.withdraw()
        
    def open(self):
        self.voice_model_label.grid(column=0, row=0)
        self.voice_model_dropdown.grid(column=1, row=0)
        self.voice_speed_label.grid(column=0, row=1)
        self.voice_speed_input.grid(column=1, row=1)
        self.font_size_label.grid(column=0, row=2)
        self.font_size_input.grid(column=1, row=2)
        self.submit_button.grid(column=0, row=3, rowspan=2)
        self.deiconify()
        self.grab_set()
        self.wait_window()


    def submit(self):
        voice_model = self.voice_model_dropdown.get()
        voice_speed = self.voice_speed_input.get()
        font_size = self.font_size_input.get()

        if voice_model:
            Configuration.update_tts(voice=voice_model)
        if voice_speed:
            Configuration.update_tts(speed=float(voice_speed))
        if font_size:
            Configuration.set_font_size(int(font_size))

        print(f"{voice_model=}")
        print(f"{voice_speed=}")
        print(f"{font_size=}")
        print(f"{Configuration.TTS=}")

        self.grab_release()
        self.withdraw()