import sys
from tkinter import Button, filedialog

from GUI.chat_box import AIChatBox
from assistant import Assistant
from assistant.coding_buddy import ProjectScanner


class Layout:
    def __init__(self, window, assistant: Assistant):
        self.window = window
        self.chat_box = AIChatBox(window, assistant)
        self.chat_box.display_message("Assistant", "Welcome!")
        self.correct_prompt_button = Button(window, text="Correct Prompt", command=self.correct_prompt)
        self.stop_ai_answer_generation_button = Button(window, text="Stop AI Answer Generation", command=self.stop_ai_answer)
        self.exit_button = Button(window, text="Exit", command=self.exit)
        self.coding_buddy_button = Button(window, text="Coding Buddy Mode", command=self.coding_buddy_mode)
        #Test Button
        self.test_call_graph_button = Button(window, text="Test Call Graph", command=self.test_call_graph)

    def exit(self):
        self.window.destroy()
        sys.exit(0)

    def test_call_graph(self):
        ps = ProjectScanner()
        folder_path = filedialog.askdirectory()
        ps.scan(folder_path)
        call_graph = ps.build_call_graph()
        print(call_graph)

    def place_on_grid(self):
        self.chat_box.grid(column=0, row=0, rowspan=5)
        self.correct_prompt_button.grid(column=1, row=0)
        self.stop_ai_answer_generation_button.grid(column=1, row=1)
        self.coding_buddy_button.grid(column=1, row=2)
        self.test_call_graph_button.grid(column=1, row=3)
        self.exit_button.grid(column=1, row=4)


    def coding_buddy_mode(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.chat_box.toggle_coding_buddy_mode(folder_path)

    def remove_from_grid(self):
        self.chat_box.grid_forget()
        self.correct_prompt_button.grid_forget()
        self.stop_ai_answer_generation_button.grid_forget()
        self.exit_button.grid_forget()

    def stop_ai_answer(self):
        self.chat_box.cancel_ai_response()

    def correct_prompt(self):
        self.chat_box.correct_prompt()



