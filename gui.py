# -- Graphical Interface --
# Code partially extracted from: https://github.com/rdbende/Azure-ttk-theme

import tkinter as tk
from tkinter import ttk

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

    def setup_widgets(self):
        """self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)"""

        # Entry
        self.text_entry = tk.Text(self)
        self.text_entry.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Button
        self.complete_button = ttk.Button(self, text="Complete Text")
        self.complete_button.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ns")

        

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