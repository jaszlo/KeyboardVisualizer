import threading
import subprocess
from enum import Enum

# Define the command to run the keyHook executable

import platform
system = platform.system().lower()
prefix = "Unknown"
if system == "windows":
    prefix = ".\\win"
elif system == "darwin":
    prefix = "./mac"
elif system == "linux":
    prefix = "./lin"
postfix = ".exe" if platform == "win" else ""
CMD = f"{prefix}KeyHook{postfix}"

class KeyActionType(Enum):
    Press = "P"
    Release = "R"

    @staticmethod
    def is_press(string):
        return string == KeyActionType.Press.value


class KeyHookThread(threading.Thread):
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.alive = True
        self.callback = callback
        self.proc = None

    def run(self):
        for action in self.iter_stdout():
            # P-<KEY> for press, R-<KEY> for release
            action_type, key = action[:1], action[2:]
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
        for stdout_line in iter(self.proc.stdout.readline, b""):
            if not self.alive:
                break
            yield stdout_line.decode("utf-8").strip()