from enum import Enum
from tkinter import ttk
import tkinter as tk

# Graphics settings classes
class ColorLevel(Enum):
    Background = "#383F51"
    Intermediate = "#DDDBF1"
    Highlight = "#3C4F76"
    Text = "#D1BEB0"
    ALPHA = 1.0


class Styles(object):
    # Use TLabel as parent so styling actually works
    button_default_name = "default.TLabel"
    button_highlight_name = "highlighted.TLabel"
    dimensions = "1200x400+50+600" # width x height + x_offset + y_offset

    @staticmethod
    def init():
        Styles.button_default = ttk.Style()
        Styles.button_default.configure(
            Styles.button_default_name,
            font=("Anonymous Pro", 10, "bold"),
            borderwidth=5,
            justify=tk.CENTER,
            highlightthickness=2,
            margin=5,
            padding=(10, 0, 0, 0),
            foreground=ColorLevel.Highlight.value,
            background=ColorLevel.Intermediate.value,
            relief="flat"
        )

        Styles.button_highlight = ttk.Style()
        Styles.button_highlight.configure(
            Styles.button_highlight_name,
            font=("Anonymous Pro", 10, "bold"),
            borderwidth=5,
            justify=tk.CENTER,
            highlightthickness=2,
            margin=5,
            padding=(10, 0, 0, 0),
            foreground=ColorLevel.Text.value,
            background=ColorLevel.Highlight.value,
            relief="flat"
        )