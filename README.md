# Keyboard Visualizer

This is a simple keyboard visualizer designed to be easy for newer programmers to understand, ensuring that it contains nothing malicious. 
Unlike other open-source keyboard visualizers that are often complex, this one has fewer than 500 lines of code (loc) and is straightforward.


https://github.com/jaszlo/KeyboardVisualizer/assets/55958177/65cc2fea-1024-4218-820f-e300caa6cbbb


## Is this a keylogger?
No, it is not. 
The potentially concerning aspect is written in C++ and currently only supports Windows. 
You can find the relevant code [here](./c_src/keyHook.cpp). 
Keys are only printed to the stdout. This C++ application is then launched as a subprocess in the main.py script within a new thread.
The actions of this thread can be seen in [KeyHook.py](./py_src/KeyHook.py). 
It simply reads the stdout and visualizes the pressed keys in the frontend. 
Because the frontend is written in Python, extending support for other operating systems should be relatively straightforward.

## Adding a new keyboard and customizations
If you want to modify the color, transparency, or default size of the visualized keyboard, make changes in the [Styles.py](./py_src/Styles.py) file according to your preferences. 
If your keyboard layout differs from mine, you'll need to edit [KeyboardLayout.py](./py_src/KeyboardLayout.py). 
Adjust the `LAYOUT`, `VISUAL_LAYOUT`, `SHIFT_LAYOUT`, and `ALT_GR_LAYOUT` to match your keyboard. 
- `LAYOUT` represents the actual values provided by the keyHook.exe.
- `VISUAL_LAYOUT` represents the default values displayed.
- `SHIFT_LAYOUT` represents the displayed values when the shift key is pressed.
- `ALT_GR_LAYOUT` represents the displayed values when the AltGr key is pressed.

Ensure that the spans of keys are correct if a key spans across multiple columns or rows. Use the variable names from the `LAYOUT` for this purpose. Also, confirm that the following variables still match with the updated `LAYOUT`:
```python
LCTRL_KEY = LAYOUT[5][0]
LSHIT_KEY = LAYOUT[4][0]
CAPS_KEY = LAYOUT[3][0]
ALT_KEY = LAYOUT[5][2]
ALT_GR_KEY = LAYOUT[5][9]
RCTRL_KEY = LAYOUT[5][-1]
RSHIFT_KEY = LAYOUT[4][-1]
MODIFIERS = [LCTRL_KEY, LSHIT_KEY, CAPS_KEY, ALT_KEY, ALT_GR_KEY, RCTRL_KEY, RSHIFT_KEY]
SHIFT_KEYS = [LSHIT_KEY, RSHIFT_KEY]
CTRL_KEYS = [LCTRL_KEY, RCTRL_KEY]
```

###### _Spell checked and revised by ChatGPT._
