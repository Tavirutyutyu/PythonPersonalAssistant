from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar, BooleanVar, font
from assistant import Assistant
from config import Configuration
from utils import threaded


class AIChatBox(Frame):
    def __init__(self, root, assistant: Assistant, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.assistant = assistant
        self.root = root

        font_size = Configuration.get_font_size()
        self.chat_font = font.Font(family="Courier", size=font_size)

        self.chat_display = scrolledtext.ScrolledText(
            self, wrap=WORD, state="disabled", font=self.chat_font
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self.__on_enter)

        self.voice_mode_button_label = StringVar(value="Enter Voice Command")
        self.voice_mode_button = Button(
            self.input_container, textvariable=self.voice_mode_button_label,
            command=self.__voice_mode
        )
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        self.input_container.columnconfigure(0, weight=1)

        self.cancel_request = False
        self._last_user_prompt = None
        self._last_ai_msg_index = None

        self.coding_buddy_mode = BooleanVar(value=False)
        self.uploaded_file_paths = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        Configuration.on_change("font_size", self.change_font_size)

    def change_font_size(self, size: int):
        self.chat_font.configure(size=size)

    def safe_display_message(self, sender, message):
        self.root.after(0, lambda: self.display_message(sender, message))

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")

        if "assistant_prefix" not in self.chat_display.tag_names():
            self.chat_display.tag_config("assistant_prefix", foreground="red")
            self.chat_display.tag_config("you_prefix", foreground="blue")
            self.chat_display.tag_config("msg_text", foreground="black")

        if sender == "Assistant":
            prefix_tag = "assistant_prefix"
            self._last_ai_msg_index = self.chat_display.index("end-1c")
        elif sender == "You":
            prefix_tag = "you_prefix"
            self._last_user_prompt = message
        else:
            prefix_tag = "msg_text"

        self.chat_display.insert(END, f"{sender}: ", prefix_tag)
        self.chat_display.insert(END, f"{message}\n", "msg_text")

        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def cancel_ai_response(self):
        self.cancel_request = True
        self.__clear_last_ai_response()

    def correct_prompt(self):
        self.cancel_ai_response()
        if self._last_user_prompt:
            self.user_input.delete(0, END)
            self.user_input.insert(0, self._last_user_prompt)
            self.user_input.focus_set()

    def toggle_coding_buddy_mode(self, folder_path=None, uploaded_file_paths=None):
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
            self.cancel_request = False
            self.__handle_ai_response(msg)

    def __handle_ai_response(self, prompt: str, voice_on: bool = False):
        self._last_user_prompt = prompt
        if self.cancel_request:
            return
        self.safe_display_message("Assistant", "...")
        self.__generate_ai_response(prompt, voice_on)

    
    @threaded
    def __generate_ai_response(self, prompt: str, voice_on: bool):
        if self.coding_buddy_mode.get():
            answer = self.assistant.generate_ai_answer(
                prompt, mode="code", uploaded_file_paths=self.uploaded_file_paths
            )
        else:
            answer = self.assistant.generate_ai_answer(prompt)

        if not self.cancel_request:
            self.__update_ai_response(answer)
            if voice_on:
                self.assistant.speak(answer)


    def __clear_last_ai_response(self):
        if self._last_ai_msg_index:
            self.chat_display.configure(state="normal")
            self.chat_display.delete(self._last_ai_msg_index, f"{self._last_ai_msg_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)

    def __update_ai_response(self, answer: str):
        self.__clear_last_ai_response()
        self.safe_display_message("Assistant", answer)


