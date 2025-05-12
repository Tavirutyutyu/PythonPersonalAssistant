import sys
from tkinter import Button, ttk

from GUI.chat_box import AIChatBox
from GUI.file_uploader import FileUploader
from assistant import Assistant


class Layout:
    def __init__(self, window, assistant: Assistant):
        self.window = window
        self.chat_box = AIChatBox(window, assistant)
        self.file_uploader = FileUploader()

        self.chat_box.display_message("Assistant", "Welcome!")
        self.correct_prompt_button = Button(window, text="Correct Prompt", command=self.correct_prompt)
        self.stop_ai_answer_generation_button = Button(window, text="Stop AI Answer Generation",
                                                       command=self.stop_ai_answer)
        self.upload_files_button = Button(window, text="Upload New Files", command=self.upload_files)
        self.clear_files_button = Button(window, text="Clear Uploaded Files", command=self.clear_uploaded_files)
        self.coding_buddy_checkbutton = ttk.Checkbutton(window, text="Coding Buddy Mode", variable=self.chat_box.coding_buddy_mode, command=self.coding_buddy_mode)
        self.exit_button = Button(window, text="Exit", command=self.exit)

    def exit(self):
        self.window.destroy()
        sys.exit(0)

    def clear_uploaded_files(self):
        self.chat_box.clear_uploaded_files()

    def place_on_grid(self):
        self.chat_box.grid(column=0, row=0, rowspan=6)
        self.correct_prompt_button.grid(column=1, row=0)
        self.stop_ai_answer_generation_button.grid(column=1, row=1)
        self.upload_files_button.grid(column=1, row=2)
        self.clear_files_button.grid(column=1, row=3)
        self.coding_buddy_checkbutton.grid(column=1, row=4)
        self.exit_button.grid(column=1, row=5)

    def upload_files(self):
        self.file_uploader.open()

    def coding_buddy_mode(self):
        self.window.after_idle(self._process_coding_buddy_mode)

    def _process_coding_buddy_mode(self):
        if self.chat_box.coding_buddy_mode.get():
            files = self.file_uploader.uploaded_files
            if files:
                self.chat_box.toggle_coding_buddy_mode(uploaded_file_paths=files)

    def remove_from_grid(self):
        self.chat_box.grid_forget()
        self.correct_prompt_button.grid_forget()
        self.stop_ai_answer_generation_button.grid_forget()
        self.exit_button.grid_forget()

    def stop_ai_answer(self):
        self.chat_box.cancel_ai_response()

    def correct_prompt(self):
        self.chat_box.correct_prompt()
