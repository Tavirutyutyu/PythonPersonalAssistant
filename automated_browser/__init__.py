import tkinter as tk
import webview

def load_url():
    url = url_entry.get()
    if not url.startswith('http'):
        url = 'https://' + url
    browser.load_url(url)

def go_back():
    browser.evaluate_js("history.back()")

def go_forward():
    browser.evaluate_js("history.forward()")

root = tk.Tk()
root.geometry("800x600")

toolbar = tk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X)

back_btn = tk.Button(toolbar, text="⬅️", command=go_back)
back_btn.pack(side=tk.LEFT)

forward_btn = tk.Button(toolbar, text="➡️", command=go_forward)
forward_btn.pack(side=tk.LEFT)

url_entry = tk.Entry(toolbar)
url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

go_btn = tk.Button(toolbar, text="Go", command=load_url)
go_btn.pack(side=tk.LEFT)

browser = webview.create_window("Voice Browser", "https://www.google.com", frameless=False, easy_drag=False)
webview.start()
root.mainloop()
