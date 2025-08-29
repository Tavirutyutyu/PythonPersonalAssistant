from tkinter import scrolledtext, WORD, END, Frame, font
from config import Configuration


class ChatDisplay(Frame):
    """
    Handles displaying messages in the chat window.
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        font_size = Configuration.get_font_size()
        self.chat_font = font.Font(family="Courier", size=font_size)

        self.chat_display = scrolledtext.ScrolledText(
            self, wrap=WORD, state="disabled", font=self.chat_font
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)

        self._last_ai_msg_index = None
        self._last_user_prompt = None
        self._last_user_msg_index = None

        Configuration.on_change("font_size", self.change_font_size)

    def change_font_size(self, size: int):
        self.chat_font.configure(size=size)

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
            self._last_user_msg_index = self.chat_display.index("end-1c")
        else:
            prefix_tag = "msg_text"

        self.chat_display.insert(END, f"{sender}: ", prefix_tag)
        self.chat_display.insert(END, f"{message}\n", "msg_text")

        self.chat_display.configure(state="disabled")
        self.chat_display.yview(END)

    def clear_last_ai_response(self):
        if self._last_ai_msg_index:
            self.chat_display.configure(state="normal")
            self.chat_display.delete(self._last_ai_msg_index, f"{self._last_ai_msg_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)

    def clear_last_user_prompt(self):
        if self._last_user_msg_index:
            self.chat_display.configure(state="normal")
            self.chat_display.delete(self._last_user_msg_index, f"{self._last_user_msg_index} +1line")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview(END)

    def update_ai_response(self, answer: str):
        self.clear_last_ai_response()
        self.display_message("Assistant", answer)

    def last_user_prompt(self):
        return self._last_user_prompt
