import sys
from tkinter import Button, ttk, Frame

from GUI.chat_box import AIChatBox
from GUI.file_uploader import FileUploader
from GUI.settings_window import SettingsWindow
from assistant import Assistant


class Layout:
    def __init__(self, window, assistant: Assistant):
        self.window = window
        self.left_frame = Frame(window)
        self.right_frame = Frame(window)

        self.chat_box = AIChatBox(self.left_frame, assistant)
        self.file_uploader = FileUploader(uploaded_files = self.chat_box.uploaded_file_paths)
        self.settings_window = SettingsWindow(window)

        self.chat_box.display_message("Assistant", "Welcome!")
        self.correct_prompt_button = Button(self.right_frame, text="Correct Prompt", command=self.correct_prompt)
        self.stop_ai_answer_generation_button = Button(self.right_frame, text="Stop AI Answer Generation",
                                                       command=self.stop_ai_answer)
        self.upload_files_button = Button(self.right_frame, text="Upload New Files", command=self.upload_files)
        self.clear_files_button = Button(self.right_frame, text="Clear Uploaded Files", command=self.clear_uploaded_files)
        self.coding_buddy_checkbutton = ttk.Checkbutton(self.right_frame, text="Coding Buddy Mode", variable=self.chat_box.coding_buddy_mode, command=self.coding_buddy_mode)
        self.settings_button = Button(self.right_frame, text="Settings", command=self.open_settings)
        self.exit_button = Button(self.right_frame, text="Exit", command=self.exit)

    def exit(self):
        self.window.destroy()
        sys.exit(0)

    def open_settings(self):
        self.settings_window.open()

    def clear_uploaded_files(self):
        self.chat_box.clear_uploaded_files()

    def place_on_grid(self):
        self.left_frame.grid(column=0, row=0, sticky="nsew")
        self.right_frame.grid(column=1, row=0, sticky="n")

        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)

        self.chat_box.grid(column=0, row=0, sticky="nsew")

        self.correct_prompt_button.grid(column=0, row=0, sticky="ew", pady=2)
        self.stop_ai_answer_generation_button.grid(column=0, row=1, sticky="ew", pady=2)
        self.upload_files_button.grid(column=0, row=2, sticky="ew", pady=2)
        self.clear_files_button.grid(column=0, row=3, sticky="ew", pady=2)
        self.coding_buddy_checkbutton.grid(column=0, row=4, sticky="ew", pady=2)
        self.settings_button.grid(column=0, row=5, sticky="ew", pady=2)
        self.exit_button.grid(column=0, row=6, sticky="ew", pady=2)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)


    def upload_files(self):
        self.file_uploader.open()

    def coding_buddy_mode(self):
        self.window.after_idle(self._process_coding_buddy_mode)

    def _process_coding_buddy_mode(self):
        if self.chat_box.coding_buddy_mode.get():
            self.upload_files()
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
