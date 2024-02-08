import threading
import subprocess
from enum import Enum

# Define the command to run the keyHook.exe
CMD = r".\\keyHook.exe"

class KeyActionType(Enum):
    Press = "Press"
    Release = "Release"

    @staticmethod
    def is_press(string):
        return string == KeyActionType.Press.value

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