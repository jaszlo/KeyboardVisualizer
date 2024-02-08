from enum import Enum
from tkinter import ttk

# Graphics settings classes
class ColorLevel(Enum):
    Background = "#04151f"
    Intermediate = "#183A37"
    Highlight = "#495283"
    Text = "#A7BBEC"


class Styles(object):
    button_default_name = "default.TButton"
    button_highlight_name = "highlighted.TButton"
    dimensions = "725x260+50+600" # width x height + x_offset + y_offset

    def __init__(self):
        self.button_default: ttk.Style = ttk.Style()
        self.button_default.configure(
            self.button_default_name,
            font=("Anonymous Pro", 10, "bold"),
            borderwidth=1,
            focuscolor="none",
            margin=5,
            foreground="dark blue",
            background="dark blue",
            relief="flat"
        )
        self.button_default.map(self.button_default_name, background=[("active", "dark blue")])

        self.button_highlight = ttk.Style = ttk.Style()
        self.button_highlight.configure(
            self.button_highlight_name,
            font=("Anonymous Pro", 12, "bold"),
            borderwidth=1,
            focuscolor="none",
            margin=5,
            foreground="white",
            background="white",
            relief="flat"
        )
        self.button_highlight.map(self.button_highlight_name, background=[("active", "white")])