import shutil
from tkinter import Tk

from GUI import Layout
from assistant import Assistant

def main():
    window = Tk()
    window.lift()
    window.update()
    window.deiconify()
    assistant = Assistant()
    print("Hi")
    try:
        assistant.greeting()
        layout = Layout(window, assistant)
        layout.place_on_grid()
        print("Grid set up")
        window.mainloop()
    except Exception as error:
        print(f"Error: {error}\n\nQuitting...")
    finally:
        assistant.shutdown()

if __name__ == "__main__":
   main()
   
