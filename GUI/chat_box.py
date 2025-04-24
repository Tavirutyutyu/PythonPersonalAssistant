from threading import Thread
from tkinter import scrolledtext, WORD, Entry, END, Frame, Button, StringVar

from assistant import AIHandler


class AIChatBox(Frame):
    def __init__(self, root, ai_handler: AIHandler, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.ai_handler = ai_handler
        self.voice_mode = False  # Initially in text mode

        self.root = root
        self.root.title("Chat Box")

        self.chat_display = scrolledtext.ScrolledText(self, wrap=WORD, state="disabled", height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Container for input and button
        self.input_container = Frame(self)
        self.input_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.user_input = Entry(self.input_container, width=40)
        self.user_input.grid(row=0, column=0, sticky="ew")
        self.user_input.bind("<Return>", self.on_enter)

        self.mode_button_label = StringVar(value="Switch to Voice Mode")
        self.mode_button = Button(self.input_container, textvariable=self.mode_button_label, command=self.toggle_mode)
        self.mode_button.grid(row=0, column=1, padx=(5, 0))

        # Make it expand correctly
        self.input_container.columnconfigure(0, weight=1)

    def toggle_mode(self):
        self.voice_mode = not self.voice_mode
        if self.voice_mode:
            self.mode_button_label.set("Switch to Text Mode")
            self.display_message("System", "Switched to Voice Mode (not yet implemented)")
            # You can trigger your voice assistant logic here later.
        else:
            self.mode_button_label.set("Switch to Voice Mode")
            self.display_message("System", "Switched to Text Mode")

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(END, f"{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def on_enter(self, event):
        if not self.voice_mode:
            msg = self.user_input.get().strip()
            if msg:
                self.display_message("You", msg)
                self.user_input.delete(0, END)
                Thread(target=self.handle_ai_response, args=(msg,), daemon=True).start()

    def handle_ai_response(self, prompt):
        self.chat_display.configure(state="normal")
        index = self.chat_display.index("end-1c")
        self.chat_display.insert(END, "Assistant: ...\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

        answer = self.ai_handler.generate_response(prompt)

        self.chat_display.configure(state="normal")
        self.chat_display.delete(index, f"{index} +1line")
        self.chat_display.insert(index, f"Assistant: {answer}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
