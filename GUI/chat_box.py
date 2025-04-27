from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar
from typing import Callable
from assistant import Assistant
from utils import threaded


class AIChatBox(Frame):
    def __init__(self, root, assistant: Assistant, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.assistant = assistant

        self.root = root
        self.root.title("Chat Box")

        self.chat_display = scrolledtext.ScrolledText(self, wrap=WORD, state="disabled", height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self.__on_enter)

        self.voice_mode_button_label = StringVar(value="Enter Voice Command")
        self.voice_mode_button = Button(self.input_container, textvariable=self.voice_mode_button_label,
                                        command=self.__voice_mode)
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        self.input_container.columnconfigure(0, weight=1)
        self._last_ai_msg_index = None

        self._current_answer_future = None
        self.cancel_request = False
        self._last_user_prompt = None


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
        self.chat_display.insert(END, f"{sender}: {message}\n")
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
        self.__ai_response_placeholder()
        self.__generate_ai_response(prompt, self.__display_ai_response)

    @threaded
    def __generate_ai_response(self, prompt: str, on_done:Callable[str, None]):
        answer = self.assistant.generate_ai_answer(prompt)
        if self.cancel_request:
            return
        on_done(answer)

    
    def __display_ai_response(self, answer: str, voice_on: bool = False):
        if self.cancel_request:
            return
        self.__update_ai_response(answer)
        if voice_on:
            self.assistant.speak(answer)

    def clear_not_needed_ai_response(self):
        if self._last_ai_msg_index:
            print("Clearing...")
            self.chat_display.configure(state="normal")
            self.chat_display.delete(self._last_ai_msg_index, f"{self._last_ai_msg_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)

    def __ai_response_placeholder(self):
        self.chat_display.configure(state="normal")
        index = self.chat_display.index("end-1c")
        self.chat_display.insert(END, "Assistant: ...\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
        self._last_ai_msg_index = index

    def __update_ai_response(self, answer: str):
        index = self._last_ai_msg_index
        self.chat_display.configure(state="normal")
        self.chat_display.delete(index, f"{index} +1line")
        self.chat_display.insert(index, f"Assistant: {answer}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
