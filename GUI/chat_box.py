from threading import Thread
from tkinter import scrolledtext, WORD, Entry, END, Frame

from assistant.ai_handler import AIHandler


class ChatBox(Frame):
    def __init__(self, root, ai_handler: AIHandler, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.ai_handler = ai_handler

        self.root = root
        self.root.title("Chat Box")

        self.chat_display = scrolledtext.ScrolledText(self, wrap=WORD, state="disabled", height=20, width=50)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)

        self.user_input = Entry(self, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=(0, 10))
        self.user_input.bind("<Return>", self.on_enter)

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(END, f"{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def on_enter(self, event):
        msg = self.user_input.get().strip()
        if msg:
            self.display_message("You", msg)
            self.user_input.delete(0, END)
            Thread(target=self.handle_ai_response, args=(msg,), daemon=True).start()

    def handle_ai_response(self, prompt):
        self.chat_display.configure(state="normal")
        index = self.chat_display.index("end-1c")  # Save the position where we insert "Assistant: ..."
        self.chat_display.insert(END, "Assistant: ...\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
        answer = self.ai_handler.generate_response(prompt)
        self.chat_display.configure(state="normal")
        self.chat_display.delete(index, f"{index} +1line")
        self.chat_display.insert(index, f"Assistant: {answer}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)
