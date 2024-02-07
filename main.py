import tkinter as tk
import subprocess
import threading

# Define the command to run the keyHook.exe
CMD = r".\\keyHook.exe"

# Define the action types for key events received from the keyHook.exe
ACTION_TYPE_PRESS = "Press"
ACTION_TYPE_RELEASE = "Release"

FUNCTIONAL_KEYS =  ["F1", "Esc"]


class KeyHookThread(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.alive = True
        self.callback = callback
        self.proc = None

    def run(self):
        for action in self.iter_stdout():
            action_type, key = action.split("-")
            self.callback(action_type, key)

    def stop(self):
        self.alive = False
        self.proc.kill()

    def iter_stdout(self):   
        self.proc = subprocess.Popen(
                CMD,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        for stdout_line in iter(self.proc.stdout.readline, ""):
            if not self.alive:
                print(stdout_line)
                break
            if stdout_line != b'':
                yield stdout_line.decode("utf-8").strip()


class KeyboardApp:
    def __init__(self, root):
        self.BACKGROUND_COLOR = "dark grey"
        self.HIGHLIGHT_COLOR = "light blue"
        self.root = root
        self.root.geometry("600x300")
        self.root.title("Keyboard Visualizer")
        self.root.attributes("-topmost", True)
        self.key_listner = KeyHookThread(self.on_key_action)
        self.key_listner.start()

        # Make background transparent
        self.root.attributes('-alpha', 0.9)
        self.root.configure(bg=self.BACKGROUND_COLOR)

        # Define the updated keyboard layout
        self.keyboard_layout = [
            ["Tab", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Caps", "Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
            ["Shift", "A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Ctrl", "Y", "X", "C", "V", "Space", "B", "N", "M"]
        ]

        self.keys = [key for row in self.keyboard_layout for key in row]
    
        # Create a canvas to hold the key buttons
        self.button_canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.button_canvas.pack(expand=True, fill='both')

        # Create a dictionary to store the key buttons
        self.key_buttons = {}
        max_buttons = max(len(row) for row in self.keyboard_layout)
    
        # Create and place the key buttons on the canvas with resizable options
        for row_idx, row in enumerate(self.keyboard_layout):
            for col_idx, key in enumerate(row):
                button = tk.Button(self.button_canvas, bg=self.BACKGROUND_COLOR, text=key,
                                   command=lambda k=key: self.highlight_key(k))
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

    def quit(self):
        # Call to close subprocess so the thread running it can join
        self.key_listner.stop()
        self.root.quit()
        exit(0)

    def on_key_action(self, action_type, pressed_key):
        if pressed_key in self.keys:
            self.key_buttons[pressed_key].config(bg=self.HIGHLIGHT_COLOR if action_type == ACTION_TYPE_PRESS else self.BACKGROUND_COLOR)
        elif pressed_key in FUNCTIONAL_KEYS:
            if (action_type == ACTION_TYPE_PRESS):
                match pressed_key:
                    case "F1":
                        self.root.iconify() if self.root.state() == "normal" else self.root.deiconify()
                    case "Esc":
                        self.quit()
                    case unknwon:
                        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardApp(root)
    root.mainloop()

