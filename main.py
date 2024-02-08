# Global imports
import tkinter as tk
from tkinter import ttk

# Local imports
from py_src.KeyHook import KeyHookThread, KeyActionType
from py_src.Styles import ColorLevel, Styles

# CTRL + F1 = Show/Hide the window
# Ctrl + Esc = Quit the application
FUNCTIONAL_KEYS =  ["F1", "Esc"]
CTRL_KEY = "Ctrl"

class KeyboardApp(object):
    def __init__(self, root):
        self.root = root
        self.styles = Styles()
        self.root.geometry(self.styles.dimensions)
        self.root.title("Keyboard Visualizer")
        self.root.attributes("-topmost", True)

        # Remove default window decorations 
        self.root.overrideredirect(True)
    
        # Flag to check if the CTRL key is pressed
        self.ctrl_pressed = False

        # Thread running keyHook.exe as subprocess reading its stdout and calling the callback in the main thread
        self.key_listner = KeyHookThread(self.on_key_action)
        self.key_listner.start()

        # Make background transparent
        self.root.attributes('-alpha', 0.9)
        self.root.configure(bg=ColorLevel.Background.value, borderwidth=7, highlightthickness=0)

        # Define the updated keyboard layout
        self.keyboard_layout = [
            ["Tab", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Caps", "Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
            ["Shift", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Back"],
            ["Ctrl", "Alt", "Y", "X", "C", "V", "Space", "B", "N", "M", "Enter"]
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
                button = ttk.Button(self.button_canvas, text=key, style=self.styles.button_default_name)
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

    def dragging(self, _event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        self.root.geometry(f"+{x}+{y}")

    def __quit_internal(self):
        # Call to close subprocess so the thread running it can join
        self.key_listner.stop()
        self.key_listner.join()
        self.root.quit()
        exit(0)

    def quit(self):
        # Needs to be executed from main thread
        self.root.after(0, self.__quit_internal)

    def on_key_action(self, action_type, pressed_key):
        # Set CTRL Flag if pressed to enable function keys
        if pressed_key == CTRL_KEY:
            self.ctrl_pressed = KeyActionType.is_press(action_type)

        # Highlight the corresponding button when the key is pressed, or reset it when released
        if pressed_key in self.keys:
            new_style = self.styles.button_highlight_name if KeyActionType.is_press(action_type) else self.styles.button_default_name
            self.key_buttons[pressed_key].configure(style=new_style)
        # Check for exit or minimize/maximize commands
        elif pressed_key in FUNCTIONAL_KEYS and KeyActionType.is_press(action_type):
            if (not self.ctrl_pressed):
                return
            # CTRL has been pressed, therefore function keys are now available
            match pressed_key:
                case "F1":
                    self.root.attributes("-alpha", 0.0) if self.root.attributes("-alpha") > 0.0 else self.root.attributes("-alpha", 0.9)
                case "Esc":
                    # Closing takes some time so immediately hide the window
                    #self.root.attributes("-alpha", 0.0)
                    self.quit()
                case unknwon:
                    pass

if __name__ == "__main__":
    app = KeyboardApp(tk.Tk())
    app.root.mainloop()