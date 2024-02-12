# Global imports
import tkinter as tk
from tkinter import ttk

# Local imports
from py_src import KeyboardLayout
from py_src.KeyHook import KeyHookThread, KeyActionType
from py_src.Styles import ColorLevel, Styles

class KeyboardApp(object):
    def __init__(self):
        self.root = tk.Tk()
        Styles.init()
        self.root.geometry(Styles.dimensions)
        self.root.title("Keyboard Visualizer")
        self.root.attributes("-topmost", True)

        # Set the window background color and border
        self.root.attributes('-alpha', ColorLevel.ALPHA.value)
        self.root.configure(bg=ColorLevel.Background.value, borderwidth=7, highlightthickness=0)

        # Remove default window decorations 
        self.root.overrideredirect(True)
    
        # Flag to check if the modifer keys have been pressed
        self.modifiers_pressed = dict()
        self.caps_already_toggled = False
        for modifier in KeyboardLayout.MODIFIERS:
            self.modifiers_pressed[modifier] = False

        # Thread running keyHook.exe as subprocess reading its stdout and calling the callback in the main thread
        # Start the thread at the end of the initialization to prevent exceptions
        self.key_listner = KeyHookThread(self.on_key_action)


        # Define the updated keyboard layout
        self.rows = len(KeyboardLayout.LAYOUT)
        self.cols = max(len(row) for row in KeyboardLayout.LAYOUT)
        self.keys = [key for row in KeyboardLayout.LAYOUT for key in row]
    
        # Create a canvas to hold the key buttons
        self.button_canvas = tk.Canvas(self.root, bg=ColorLevel.Background.value, highlightthickness=0, background=ColorLevel.Background.value)
        self.button_canvas.pack(expand=True, fill='both')

        # Create a dictionary to store the key buttons
        self.key_buttons = {}
        # Create and place the key buttons on the canvas with resizable options
        for row_idx, row in enumerate(KeyboardLayout.LAYOUT):
            for col_idx, key in enumerate(row):
                if (key == ""):
                    continue
                button_text = KeyboardLayout.VISUAL_LAYOUT[row_idx][col_idx]    
                button = ttk.Button(self.button_canvas, text=button_text, style=Styles.button_default_name)
                # Get the column and row span of the key
                colspan, rowspan = KeyboardLayout.span_of(key)

                button.grid(row=row_idx, column=col_idx, sticky=tk.NSEW, padx=1, pady=1, columnspan=colspan, rowspan=rowspan)
                # Make buttons resizable
                self.button_canvas.columnconfigure(col_idx, weight=1, uniform="group1")
                self.button_canvas.rowconfigure(row_idx, weight=1)
                self.key_buttons[key] = button

        # Override default controll key behaviour
        self.root.bind("<Tab>", lambda _: None)
        self.root.bind("<Caps_Lock>", lambda _: None)
        self.root.bind("<Control_L>", lambda _: None)
        self.root.bind("<Shift_L>", lambda _: None)
        self.root.bind("<Alt_L>", lambda _: None)

        # Dragging the window anywhere
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.dragging)

        # Start the key listener thread
        self.key_listner.start()

    def start_drag(self, event):
        self.start_x = event.x_root - self.root.winfo_rootx()
        self.start_y = event.y_root - self.root.winfo_rooty()

    def dragging(self, event):
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.root.geometry(f"+{x}+{y}")

    def _quit_internal(self):
        # Call to close subprocess so the thread running it can join
        self.key_listner.stop()
        self.key_listner.join()
        self.root.quit()
        exit(0)

    def quit(self):
        # Needs to be executed from main thread
        self.root.after(0, self._quit_internal)


    def run(self):
        self.root.mainloop()

    def on_key_action(self, action_type, pressed_key):
        key_name = pressed_key
        # Set modifier flags if pressed to enable function keys
        if key_name in KeyboardLayout.MODIFIERS and key_name != KeyboardLayout.CAPS_KEY:
            self.modifiers_pressed[key_name] = KeyActionType.is_press(action_type)
        # Caps toggle needs to be handled differently
        elif key_name == KeyboardLayout.CAPS_KEY:
            if not self.caps_already_toggled and KeyActionType.is_press(action_type):
                self.modifiers_pressed[KeyboardLayout.CAPS_KEY] = not self.modifiers_pressed[KeyboardLayout.CAPS_KEY]
                self.caps_already_toggled = True
            if not KeyActionType.is_press(action_type):
                self.caps_already_toggled = False

        if key_name in KeyboardLayout.SHIFT_KEYS or key_name == KeyboardLayout.CAPS_KEY:
            # if not self.modifiers_pressed[KeyboardLayout.ALT_GR_KEY]:            
            self.toggle_buttons_shift()

        if key_name == KeyboardLayout.ALT_GR_KEY:
            self.toggle_buttons_altgr()


        # Highlight the corresponding button when the key is pressed, or reset it when released
        if key_name in self.keys:
            new_style = Styles.button_highlight_name if KeyActionType.is_press(action_type) else Styles.button_default_name
            self.key_buttons[key_name].configure(style=new_style)

        # Check for exit or minimize/maximize commands
        if key_name in KeyboardLayout.FUNCTIONAL_KEYS and KeyActionType.is_press(action_type):
            if not any(self.modifiers_pressed[ctrl] for ctrl in KeyboardLayout.CTRL_KEYS):
                return
            # CTRL has been pressed, therefore function keys are now available
            print(key_name)
            match key_name:
                case "F1":
                    self.root.attributes("-alpha", 0.0) if self.root.attributes("-alpha") > 0.0 else self.root.attributes("-alpha", ColorLevel.ALPHA.value)
                case "ESC":
                    self.quit()
                case "+":
                    # Increase window size bit by bit
                    geometry = self.root.geometry()
                    dim, posx, posy = geometry.split("+")
                    width, height = dim.split("x")
                    new_width, new_height = int(int(width) * 1.02), int(int(height) * 1.02)
                    self.root.geometry(f"{new_width}x{new_height}+{posx}+{posy}")
                case "-":
                    # Decrase window size bit by bit
                    geometry = self.root.geometry()
                    dim, posx, posy = geometry.split("+")
                    width, height = dim.split("x")
                    new_width, new_height = int(int(width) * 0.98), int(int(height) * 0.98)
                    self.root.geometry(f"{new_width}x{new_height}+{posx}+{posy}")
                case _:
                    pass
    
    def toggle_buttons_shift(self):
        shift_pressed = (
            self.modifiers_pressed[KeyboardLayout.LSHIT_KEY]  or 
            self.modifiers_pressed[KeyboardLayout.RSHIFT_KEY] or 
            self.modifiers_pressed[KeyboardLayout.CAPS_KEY]
        )
        layout = KeyboardLayout.SHIFT_LAYOUT if shift_pressed else KeyboardLayout.VISUAL_LAYOUT
        for key, button in self.key_buttons.items():
            row, col = KeyboardLayout.index_of(key)
            button_text = layout[row][col]
            button.configure(text=button_text)

    def toggle_buttons_altgr(self):
        layout = KeyboardLayout.ALT_GR_LAYOUT if self.modifiers_pressed[KeyboardLayout.ALT_GR_KEY] else KeyboardLayout.VISUAL_LAYOUT
        for key, button in self.key_buttons.items():
            row, col = KeyboardLayout.index_of(key)
            button_text = layout[row][col]
            button.configure(text=button_text)
    
if __name__ == "__main__":
    app = KeyboardApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()