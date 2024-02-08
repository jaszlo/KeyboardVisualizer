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
            padding=0,
            margin=5,
            fg=ColorLevel.Text.value,
            bg=ColorLevel.Intermediate.value,
            color=ColorLevel.Background.value,
            #relief="flat"
        )

        self.button_highlight = ttk.Style = ttk.Style()
        self.button_highlight.configure(
            self.button_highlight_name,
            font=("Anonymous Pro", 12, "bold"),
            padding=0,
            margin=5,
            fg=ColorLevel.Text.value,
            bg=ColorLevel.Highlight.value,
            color=ColorLevel.Intermediate.value,
        )