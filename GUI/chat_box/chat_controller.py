import threading
from tkinter import Frame, Entry, END, Button, StringVar, BooleanVar
from utils import threaded
from .chat_display import ChatDisplay


class ChatController(Frame):
    """
    Coordinates user input, Assistant, and ChatDisplay.
    """
    def __init__(self, root, assistant, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.assistant = assistant
        self.root = root

        self.chat_display = ChatDisplay(self)
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self.__on_enter)

        self.voice_mode_button_label = StringVar(value="Enter Voice Command")
        self.voice_mode_button = Button(self.input_container, textvariable=self.voice_mode_button_label, command=self.__voice_mode)
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        self.input_container.columnconfigure(0, weight=1)

        self.cancel_event = threading.Event()
        self.coding_buddy_mode = BooleanVar(value=False)
        self.uploaded_file_paths = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def safe_display_message(self, sender, message):
        self.root.after(0, lambda: self.chat_display.display_message(sender, message))

    def cancel_ai_response(self):
        self.cancel_event.set()
        self.chat_display.clear_last_ai_response()
        self.assistant.clear_last_ai_message()

    def correct_prompt(self):
        self.cancel_ai_response()
        last_prompt = self.chat_display.last_user_prompt()
        self.chat_display.clear_last_user_prompt()
        self.assistant.clear_last_user_message()
        if last_prompt:
            self.user_input.delete(0, END)
            self.user_input.insert(0, last_prompt)
            self.user_input.focus_set()

    def toggle_coding_buddy_mode(self, uploaded_file_paths=None):
        if uploaded_file_paths:
            self.uploaded_file_paths.extend(uploaded_file_paths)

    def upload_files(self, files):
        self.uploaded_file_paths.extend(files)

    def clear_uploaded_files(self):
        self.uploaded_file_paths.clear()

    @threaded
    def __voice_mode(self):
        voice_input = self.assistant.listen(self.safe_display_message)
        self.safe_display_message("You", voice_input)
        self.__handle_ai_response(voice_input, voice_on=True)

    def __on_enter(self, event):
        msg = self.user_input.get().strip()
        if msg:
            self.safe_display_message("You", msg)
            self.user_input.delete(0, END)
            self.cancel_event.clear()
            self.__handle_ai_response(msg)

    def __handle_ai_response(self, prompt: str, voice_on: bool = False):
        if self.cancel_event.is_set():
            print("Canceled by user Before ai response")
            return
        self.safe_display_message("Assistant", "...")
        self.__generate_ai_response(prompt, voice_on)

    @threaded
    def __generate_ai_response(self, prompt: str, voice_on: bool):
        if self.coding_buddy_mode.get():
            answer = self.assistant.generate_ai_answer(
                prompt, cancel_event=self.cancel_event, mode="code", uploaded_file_paths=self.uploaded_file_paths
            )
        else:
            answer = self.assistant.generate_ai_answer(prompt, cancel_event=self.cancel_event)

        if not self.cancel_event.is_set():
            self.chat_display.update_ai_response(answer)
            if voice_on:
                self.assistant.speak(answer)
        else:
            print("Canceled by user After ai response")


