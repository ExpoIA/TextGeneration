# -- Graphical Interface --
# Code partially extracted from: https://github.com/rdbende/Azure-ttk-theme

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from text_generation import API

# This class implements all the gui and inherits from tk.Frame
class App(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self)

        self.root = root

        # Set number of rows and cols
        for index in [0]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.setup_widgets()


        # initialize GPT-3 API
        self.api = API()

    def setup_widgets(self):
        """self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)"""

        # Entry
        text_font = Font(family="Gotham", size=14)

        self.text_entry = tk.Text(self, font=text_font, padx=10, pady=10)
        self.text_entry.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_entry.bind('<Control_L>', self.complete_text_keybind) # Instead of pressing the button, the user can press Crtl to complete the text.
        self.text_entry.bind('<Control_R>', self.complete_text_keybind)

        # Button
        self.complete_button = ttk.Button(self, text="Completar Texto", command=self.complete_text)
        self.complete_button.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ns")

    """
    When the button is pressed, complete the text using GPT-3.
    """
    def complete_text(self):
        # Get text_entry text
        prompt = self.text_entry.get('1.0', 'end-1c')

        if len(prompt) > 10:

            # Put cursor in the end position
            self.text_entry.see("end")

            # Delete "\n" at the end of the current text in the text_entry
            while self.text_entry.get("end-1c linestart") == '\n':
                self.text_entry.delete("end-1c linestart", "end")

            # Complete it with GPT-3
            completion = self.api.complete_text(prompt, max_tokens=200, stop=".", response_lstrip="\n",
             response_rstrip="\n", response_beginning="\n\n", response_end=".\n\n")

            pos1 = self.text_entry.index('end-1c')

            # Add the text to the text_entry
            self.text_entry.insert('end', completion)

            pos2 = self.text_entry.index('end-1c')

            # Change appearance of text
            self.text_entry.tag_add("response", pos1, pos2)
            self.text_entry.tag_config("response", foreground="blue")

            # <TODO>
            # change text color back to normal if the user edits the GPT-3 response

    """
    Just like complete_text, but called by using a keybind.
    """
    def complete_text_keybind(self, event):
        self.complete_text()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Text Generation demo-v1")

    # Set theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Create the window

    root.config(width=300, height=200)

    """root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))"""

    root.mainloop()