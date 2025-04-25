from threading import Thread
from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar

from assistant import Assistant


class AIChatBox(Frame):
    def __init__(self, root, assistant: Assistant, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.assistant = assistant

        self.root = root
        self.root.title("Chat Box")

        self.chat_display = scrolledtext.ScrolledText(self, wrap=WORD, state="disabled", height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Container for input and button
        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self._on_enter)

        self.voice_mode_button_label = StringVar(value="Switch to Voice Mode")
        self.voice_mode_button = Button(self.input_container, textvariable=self.voice_mode_button_label,
                                        command=self._voice_mode)
        self.voice_mode_button.grid(row=0, column=1, padx=(5, 0))

        # Make it expand correctly
        self.input_container.columnconfigure(0, weight=1)
        self._last_ai_msg_index = None

    def _voice_mode(self):
        self.assistant.listen()

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

    def _handle_ai_response(self, prompt):
        self.chat_display.configure(state="normal")
        index = self.chat_display.index("end-1c")
        self.chat_display.insert(END, "Assistant: ...\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

        self._last_ai_msg_index = index

        Thread(target=self._display_ai_response, args=(prompt,), daemon=True).start()


    def _display_ai_response(self, prompt):
        answer = self.assistant.generate_ai_answer(prompt)
        print(f"Answer: {answer}")
        self._update_ai_response(answer)


    def _update_ai_response(self, answer: str):
        index = self._last_ai_msg_index
        self.chat_display.configure(state="normal")
        self.chat_display.delete(index, f"{index} +1line")
        self.chat_display.insert(index, f"Assistant: {answer}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
