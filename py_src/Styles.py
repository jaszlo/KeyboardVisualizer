from enum import Enum
from tkinter import ttk

# Graphics settings classes
class ColorLevel(Enum):
    Background = "#04151f"
    Intermediate = "#183A37"
    Highlight = "#495283"
    Text = "#A7BBEC"
    ALPHA = 0.9

class KeyboadLayout(object):
    SPANS = {
        # (COL, ROW)
        "Back": (1, 2),
        "Enter": (2, 1),
        "Space": (6, 1),
    }

    @staticmethod
    def span_of(key):
        return KeyboadLayout.SPANS.get(key, (1, 1))


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
            padding=0,
            foreground="dark blue",
            highlightedbackground="dark blue",
            highlightedcolor="dark blue",
            activeforeground="dark blue",
            background="dark blue",
            activebackground="dark blue",
            relief="flat"
        )

        self.button_highlight = ttk.Style = ttk.Style()
        self.button_highlight.configure(
            self.button_highlight_name,
            font=("Anonymous Pro", 12, "bold"),
            borderwidth=1,
            focuscolor="none",
            margin=5,
            padding=1,
            foreground="white",
            highlightedbackground="white",
            highlightedcolor="white",
            activeforeground="white",
            background="white",
            activebackground="white",
            relief="flat"
        )