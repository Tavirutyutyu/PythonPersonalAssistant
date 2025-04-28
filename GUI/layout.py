import sys
import tkinter as tk

from GUI.chat_box import AIChatBox
from assistant import Assistant


class Layout:
    def __init__(self, window, assistant: Assistant):
        self.window = window
        self.chat_box = AIChatBox(window, assistant)
        self.chat_box.display_message("Assistant", "Welcome!")
        self.correct_prompt_button = tk.Button(window, text="Correct Prompt", command=self.correct_prompt)
        self.stop_ai_answer_generation_button = tk.Button(window, text="Stop AI Answer Generation", command=self.stop_ai_answer)
        self.exit_button = tk.Button(window, text="Exit", command=self.exit)

    def exit(self):
        self.window.destroy()
        sys.exit(0)

    def place_on_grid(self):
        self.chat_box.grid(column=0, row=0, rowspan=3)
        self.correct_prompt_button.grid(column=1, row=0)
        self.stop_ai_answer_generation_button.grid(column=1, row=1)
        self.exit_button.grid(column=1, row=2)

    def remove_from_grid(self):
        self.chat_box.grid_forget()
        self.correct_prompt_button.grid_forget()
        self.stop_ai_answer_generation_button.grid_forget()
        self.exit_button.grid_forget()

    def stop_ai_answer(self):
        self.chat_box.cancel_ai_response()

    def correct_prompt(self):
        self.chat_box.correct_prompt()



