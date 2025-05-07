from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar, filedialog
from typing import Callable

from assistant import Assistant
from utils import threaded


class AIChatBox(Frame):
    def __init__(self, root, assistant: Assistant, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.assistant = assistant

        self.root = root
        self.root.title("Chat Box")

        self.chat_display = scrolledtext.ScrolledText(self, wrap=WORD, state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self.__on_enter)

        self.voice_mode_button_label = StringVar(value="Enter Voice Command")
        self.voice_mode_button = Button(self.input_container, textvariable=self.voice_mode_button_label, command=self.__voice_mode)
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        self.input_container.columnconfigure(0, weight=1)
        self._last_ai_msg_index = None

        self._current_answer_future = None
        self.cancel_request = False
        self._last_user_prompt = None

        self.__coding_buddy_mode = False
        self.__coding_buddy_directory_path = None
        self.__entry_point = None

        self.__uploaded_file_paths = None

    @threaded
    def __voice_mode(self):
        voice_input = self.__listen()
        self.__process_voice_input(voice_input)

    def __listen(self):
        voice_input = self.assistant.listen(self.display_message)
        self.display_message("You", voice_input)
        return voice_input

    def __process_voice_input(self, voice_input):
        command = self.assistant.match_command(voice_input)
        if command:
            if command.has_sub_options:
                self.assistant.execute(command, self.display_message)
            else:
                command.execute()
        else:
            self.__handle_ai_response(voice_input, voice_on=True)

    # Have to be public or the program crashes
    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        if sender == "Assistant":
            color = "red"
            index = self.chat_display.index("end-1c")
            self._last_ai_msg_index = index
        elif sender == "You":
            color = "blue"
        else:
            color = "green"

        if not color in self.chat_display.tag_names():
            self.chat_display.tag_config(color, foreground=color)
        if "black" not in self.chat_display.tag_names():
            self.chat_display.tag_config("black", foreground="black")

        self.chat_display.insert(END, f"{sender}: ", color)
        self.chat_display.insert(END, f"{message}\n", "black")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def __on_enter(self, event):
        msg = self.user_input.get().strip()
        if msg:
            self.display_message("You", msg)
            self.user_input.delete(0, END)
            self.cancel_request = False
            self.__handle_ai_response(msg)

    def __handle_ai_response(self, prompt: str, voice_on: bool = False):
        self._last_user_prompt = prompt
        if self.cancel_request:
            return
        self.display_message("Assistant", "...")
        self.__generate_ai_response(prompt, voice_on, self.__display_ai_response)

    @threaded
    def __generate_ai_response(self, prompt: str, voice_on: bool, on_done: Callable[[str, bool], None]):
        if self.__coding_buddy_mode:
            print(self.__uploaded_file_paths)
            answer = self.assistant.generate_ai_answer(prompt, mode="code", uploaded_file_paths=self.__uploaded_file_paths)
        else:
            answer = self.assistant.generate_ai_answer(prompt)
        if self.cancel_request:
            return
        on_done(answer, voice_on)

    def cancel_ai_response(self):
        self.cancel_request = True
        self.__clear_last_ai_response()

    def correct_prompt(self):
        self.cancel_ai_response()
        last_prompt = self._last_user_prompt
        if last_prompt:
            self.__clear_last_user_prompt()
            self.user_input.delete(0, END)
            self.user_input.insert(0, last_prompt)
            self.user_input.focus_set()

    def toggle_coding_buddy_mode(self, folder_path: str | None = None, entry_point: str | None = None, uploaded_file_paths:list | None = None ):
        if self.__coding_buddy_mode:
            self.__coding_buddy_mode = False
            self.__coding_buddy_directory_path = None
            self.__entry_point = None
        else:
            self.__coding_buddy_mode = True
            self.__coding_buddy_directory_path = folder_path
            self.__entry_point = entry_point
            self.__uploaded_file_paths = uploaded_file_paths

    def __display_ai_response(self, answer: str, voice_on: bool = False):
        if self.cancel_request:
            return
        self.__update_ai_response(answer)
        if voice_on:
            self.assistant.speak(answer)

    def __clear_last_ai_response(self):
        if self._last_ai_msg_index:
            print("Clearing...")
            self.chat_display.configure(state="normal")
            self.chat_display.delete(self._last_ai_msg_index, f"{self._last_ai_msg_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)

    def __clear_last_user_prompt(self):
        if self._last_user_prompt:
            self.chat_display.configure(state="normal")
            start_index = self.chat_display.search(f"You: {self._last_user_prompt}", "1.0", END)
            if start_index:
                self.chat_display.delete(start_index, f"{start_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)
            self._last_user_prompt = None


    def __update_ai_response(self, answer: str):
        self.__clear_last_ai_response()
        self.display_message("Assistant", answer)

