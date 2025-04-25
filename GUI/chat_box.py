from threading import Thread
from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar

from assistant import Assistant
from commands import Command


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
        self.user_input.bind("<Return>", self._on_enter)

        self.voice_mode_button_label = StringVar(value="Enter Voice Command")
        self.voice_mode_button = Button(self.input_container, textvariable=self.voice_mode_button_label,
                                        command=lambda : Thread(target=self._voice_mode, daemon=True).start())
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        self.input_container.columnconfigure(0, weight=1)
        self._last_ai_msg_index = None

    def _voice_mode(self):
        voice_input = self.__listen()
        self.__process_voice_input(voice_input)


    def __listen(self):
        voice_input = self.assistant.listen(self.display_message)
        self.display_message("You", voice_input)
        return voice_input

    def display_sub_option(self, command: Command, voice_on: bool = False):
        options = command.get_sub_options()
        self.display_message("Assistant", "Choose an option")
        if voice_on: self.assistant.speak("Choose an option")
        for option in options:
            self.display_message("Assistant", option)
            if voice_on: self.assistant.speak(option)

    def __process_voice_input(self, voice_input):
        command = self.assistant.match_command(voice_input)
        if command:
            if command.has_sub_options:
                self.display_sub_option(command, voice_on=True)
                user_input = self.__listen()
                self.__evaluate_sub_option_input(user_input, command)
            else:
                command.execute()
        else:
            self._handle_ai_response(voice_input, voice_on=True)

    def __evaluate_sub_option_input(self, user_input: str, command: Command, voice_on: bool = False):
        if user_input:
            options = command.get_sub_options()
            if user_input in options:
                command.execute(user_input)
            else:
                self.display_message("Assistant", "This is not a valid option.")
                self.assistant.speak("This is not a valid option.")
        else:
            self.display_message("Assistant", "No user input.")
            self.assistant.speak("No user input.")

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(END, f"{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def _on_enter(self, event):
        msg = self.user_input.get().strip()
        if msg:
            self.display_message("You", msg)
            self.user_input.delete(0, END)
            self._handle_ai_response(msg)

    def __handle_ai_start_response(self):
        self.chat_display.configure(state="normal")
        index = self.chat_display.index("end-1c")
        self.chat_display.insert(END, "Assistant: ...\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
        self._last_ai_msg_index = index

    def _handle_ai_response(self, prompt: str, voice_on: bool = False):
        self.__handle_ai_start_response()
        Thread(target=self._display_ai_response, args=(prompt, voice_on,), daemon=True).start()

    def _display_ai_response(self, prompt: str, voice_on: bool = False):
        answer = self.assistant.generate_ai_answer(prompt)
        self._update_ai_response(answer)
        if voice_on:
            self.assistant.speak(answer)

    def _update_ai_response(self, answer: str):
        index = self._last_ai_msg_index
        self.chat_display.configure(state="normal")
        self.chat_display.delete(index, f"{index} +1line")
        self.chat_display.insert(index, f"Assistant: {answer}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
