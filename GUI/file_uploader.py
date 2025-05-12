from pathlib import Path
from tkinter import Toplevel, Label, Listbox, Button, filedialog, messagebox, END
from config import TOKEN_LIMIT
from transformers import LlamaTokenizer

class FileUploader(Toplevel):
    def __init__(self, master=None, uploaded_files=None):
        super().__init__(master)
        self.withdraw()  # Start hidden
        self.title("File Uploader")
        self.geometry("600x400")
        self.uploaded_files = uploaded_files
        self.total_tokens = 0

        self.token_label = Label(self, text=f"Used {self.total_tokens} / {TOKEN_LIMIT} tokens")
        self.listbox = Listbox(self, width=80, height=15)
        self.add_button = Button(self, text="Add files", command=self.add_files)
        self.remove_button = Button(self, text="Remove Selected", command=self.remove_selected)
        self.submit_button = Button(self, text="Submit", command=self.submit)


    def open(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.token_label.grid(row=0, column=0, columnspan=3, pady=(10, 0), sticky="w", padx=10)
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.remove_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.submit_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        self.update_token_label()
        self.deiconify()
        self.grab_set()
        self.wait_window()

    def add_files(self):
        file_paths = filedialog.askopenfilenames(parent=self ,title="Select Files")
        for file_path in file_paths:
            path = Path(file_path)
            if path not in self.uploaded_files:
                try:
                    content = path.read_text(encoding="utf-8")
                    tokens = len(content) // 4
                    if self.total_tokens + tokens > TOKEN_LIMIT:
                        messagebox.showwarning(title="Exceeding token limit!", message=f"Adding {path.name} would exceed the token limit.")
                        continue
                    self.uploaded_files.append(file_path)
                    self.total_tokens += tokens
                    self.listbox.insert(END, f"{path.name} - ~{tokens} tokens")
                    self.update_token_label()
                except Exception as e:
                    messagebox.showerror("File Error", f"Could not read {path.name}: {e}")

    def remove_selected(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            path = self.uploaded_files.pop(index)
            try:
                content = path.read_text(encoding="utf-8")
                tokens = self.count_tokens(content)
                self.total_tokens -= tokens
            except:
                pass
            self.listbox.delete(index)
            self.update_token_label()

    def submit(self):
        if not self.uploaded_files:
            messagebox.showinfo("No Files", "Please upload some files first.")
        else:
            self.grab_release()
            self.withdraw()

    def update_token_label(self):
        self.token_label.config(text=f"Used: {self.total_tokens} / {TOKEN_LIMIT} tokens")

    def count_tokens(self, text):
        tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3B-hf")
        tokens = tokenizer.encode(text)
        return len(tokens)

