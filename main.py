# Global imports
import tkinter as tk
from tkinter import ttk
from enum import Enum
from dataclasses import dataclass

# Local imports
from py_src.KeyHook import KeyHookThread, KeyActionType

# F1 = Minimize/Maximize the window
# Ctrl + Esc = Quit the application
FUNCTIONAL_KEYS =  ["F1", "Esc"]
CTRL_KEY = "Ctrl"

# Graphics settings classes
class ColorLevel(Enum):
    Background = "#04151f"
    Intermediate = "#183A37"
    Highlight = "#9097C0"

@dataclass
class Styles(object):
    button_default_name: str = "TButtonDefault"
    button_default: ttk.Style = ttk.Style().configure("TButtonDefault", font=("Arial", 12), padding=7, foreground=ColorLevel.Background.value, background=ColorLevel.Intermediate.value, relief="flat")

    buttuon_highlight_name: str = "TButtonHighlighted"
    button_highlight = ttk.Style = ttk.Style().configure("TButtonHighlighted", font=("Arial", 12), padding=7, foreground=ColorLevel.Background.value, background=ColorLevel.Highlight.value, relief="flat")

class KeyboardApp(object):
    def __init__(self, root):
        self.STYLES = Styles()
        self.root = root
        self.root.geometry("600x300")
        self.root.title("Keyboard Visualizer")
        self.root.attributes("-topmost", True)
        self.ctrl_pressed = False
        # Remove default window decorations
        self.root.overrideredirect(True)
    

        # Thread running keyHook.exe as subprocess reading its stdout and calling the callback in the main thread
        self.key_listner = KeyHookThread(self.on_key_action)
        self.key_listner.start()

        # Make background transparent
        self.root.attributes('-alpha', 0.9)
        self.root.configure(bg=ColorLevel.Background.value)

        # Define the updated keyboard layout
        self.keyboard_layout = [
            ["Tab", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Caps", "Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
            ["Shift", "A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Ctrl", "Y", "X", "C", "V", "Space", "B", "N", "M"]
        ]

        self.keys = [key for row in self.keyboard_layout for key in row]
    
        # Create a canvas to hold the key buttons
        self.button_canvas = tk.Canvas(root, bg=ColorLevel.Background.value, highlightthickness=0)
        self.button_canvas.pack(expand=True, fill='both')

        # Create a dictionary to store the key buttons
        self.key_buttons = {}
        # Create and place the key buttons on the canvas with resizable options
        for row_idx, row in enumerate(self.keyboard_layout):
            for col_idx, key in enumerate(row):
                button = ttk.Button(self.button_canvas, text=key, style=self.STYLES.button_default)
                button.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                # Make buttons resizable
                self.button_canvas.columnconfigure(col_idx, weight=1, uniform="group1")
                self.button_canvas.rowconfigure(row_idx, weight=1)
                self.key_buttons[key] = button

        # Override default controll key behaviour
        self.root.bind("<Tab>", lambda _: "break")
        self.root.bind("<Caps_Lock>", lambda _: "break")
        self.root.bind("<Control_L>", lambda _: "break")
        self.root.bind("<Shift_L>", lambda _: "break")
        self.root.bind("<Alt_L>", lambda _: "break")

        # Dragging the window anywhere
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.dragging)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def dragging(self, event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        self.root.geometry(f"+{x}+{y}")

    def quit(self):
        # Call to close subprocess so the thread running it can join
        self.key_listner.stop()
        self.root.quit()
        exit(0)

    def on_key_action(self, action_type, pressed_key):
        # Set CTRL Flag if pressed to enable function keys
        if pressed_key == CTRL_KEY:
            self.ctrl_pressed = KeyActionType.is_press(action_type)

        # Highlight the corresponding button when the key is pressed, or reset it when released
        if pressed_key in self.keys:
            new_style = self.STYLES.button_highlight if KeyActionType.is_press(action_type) else self.STYLES.button_default
            self.key_buttons[pressed_key].configure(style=new_style)
        # Check for exit or minimize/maximize commands
        elif pressed_key in FUNCTIONAL_KEYS and KeyActionType.is_press(action_type):
            if (not self.ctrl_pressed):
                return
            # CTRL has been pressed, therefore function keys are now available
            match pressed_key:
                case "F1":
                    print(self.root.attributes('-alpha'))
                    self.root.attributes('-alpha', 0.0) if self.root.attributes('-alpha') > 0.0 else self.root.attributes('-alpha', 0.9)
                case "Esc":
                    self.quit()
                case unknwon:
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardApp(root)
    root.mainloop()

