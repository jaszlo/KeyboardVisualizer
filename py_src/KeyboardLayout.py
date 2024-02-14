# Layout of the keyboard. Values are as given by the keyHook executable
# Modify this to match the layout of your keyboard. Also modify the modifiers and special keys accordingly
import platform
system = platform.system().lower()
if system == "windows":
    LAYOUT = [
            [ "ESC", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "ZIRKUMFLEX", "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "ß",  "AKUT", "RÜCK"],  
            [ "TABULATOR", "Q",  "W",  "E",  "R",  "T",  "Z",  "U",  "I",  "O",  "P",  "Ü",  "+"],
            [ "FESTSTELL", "A",  "S",  "D",  "F",  "G",  "H",  "J",  "K",  "L",  "Ö",  "Ä",  "#", "EINGABE"],
            [ "UMSCHALT", "<",  "Y",  "X",  "C",  "V",  "B",  "N",  "M",  ",",  ".",  "-",  "UMSCHALT RECHTS"],
            [ "STRG", "LINKE WINDOWS", "ALT", "LEER", "", "", "", "", "", "ALT GR", "ANWENDUNG", "STRG-RECHTS"]
        ]

    VISUAL_LAYOUT = [
            [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "^", "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "ß",  "´", "Back"],  
            [ "Tab", "q",  "w",  "e",  "r",  "t",  "z",  "u",  "i",  "o",  "p",  "ü",  "+"],
            [ "Caps", "a",  "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  "ö",  "ä",  "#", "Enter"],
            [ "Shift", "<",  "y",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "-",  "Shift"],
            [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
        ]

    SHIFT_LAYOUT = [
            [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "°", "!",  "\"", "§",  "$",  "%",  "&",  "/",  "(",  ")",  "=",  "`",  "´", "Back"],  
            [ "Tab", "Q",  "W",  "E",  "R",  "T",  "Z",  "U",  "I",  "O",  "P",  "Ü",  "*"],
            [ "Caps", "A",  "S",  "D",  "F",  "G",  "H",  "J",  "K",  "L",  "Ö",  "Ä",  "'", "Enter"],
            [ "Shift", "<",  "Y",  "X",  "C",  "V",  "B",  "N",  "M",  ";",  ":",  "_",  "Shift"],
            [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
        ]

    ALT_GR_LAYOUT = [
        [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
        [ "^", "1",  "²",  "³",  "4",  "5",  "6",  "{",  "[",  "]",  "}",  "\\",  "´", "Back"],  
        [ "Tab", "@",  "w",  "€",  "r",  "t",  "z",  "u",  "i",  "o",  "p",  "ü",  "~"],
        [ "Caps", "a",  "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  "ö",  "ä",  "#", "Enter"],
        [ "Shift", "|",  "y",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "-",  "Shift"],
        [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
    ]

    # CTRL + functional keys results in actions
    # CTRL + ESC = Exit
    # CTRL + F1 = Hide/Show
    #                 First Row      "+"            "-"
    FUNCTIONAL_KEYS = LAYOUT[0] + [LAYOUT[2][-1], LAYOUT[4][-2]]


    # List of all modifiers. Values are as given by the keyHook executable
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

    # Special layout for some keys. Values are as given by the keyHook executable
    SPANS = {
        # (COL, ROW)
        "RÜCK": (1, 2),
        "EINGABE": (1, 2),
        "LEER": (6, 1),
    }

elif "darwin":
    LAYOUT = [
            [ "ESC", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "ZIRKUMFLEX", "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "ß",  "AKUT", "RÜCK"],  
            [ "TABULATOR", "Q",  "W",  "E",  "R",  "T",  "Z",  "U",  "I",  "O",  "P",  "Ü",  "+"],
            [ "FESTSTELL", "A",  "S",  "D",  "F",  "G",  "H",  "J",  "K",  "L",  "Ö",  "Ä",  "#", "EINGABE"],
            [ "UMSCHALT", "<",  "Y",  "X",  "C",  "V",  "B",  "N",  "M",  ",",  ".",  "-",  "UMSCHALT RECHTS"],
            [ "STRG", "LINKE WINDOWS", "ALT", "LEER", "", "", "", "", "", "ALT GR", "ANWENDUNG", "STRG-RECHTS"]
        ]

    VISUAL_LAYOUT = [
            [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "^", "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "ß",  "´", "Back"],  
            [ "Tab", "q",  "w",  "e",  "r",  "t",  "z",  "u",  "i",  "o",  "p",  "ü",  "+"],
            [ "Caps", "a",  "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  "ö",  "ä",  "#", "Enter"],
            [ "Shift", "<",  "y",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "-",  "Shift"],
            [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
        ]

    SHIFT_LAYOUT = [
            [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
            [ "°", "!",  "\"", "§",  "$",  "%",  "&",  "/",  "(",  ")",  "=",  "`",  "´", "Back"],  
            [ "Tab", "Q",  "W",  "E",  "R",  "T",  "Z",  "U",  "I",  "O",  "P",  "Ü",  "*"],
            [ "Caps", "A",  "S",  "D",  "F",  "G",  "H",  "J",  "K",  "L",  "Ö",  "Ä",  "'", "Enter"],
            [ "Shift", "<",  "Y",  "X",  "C",  "V",  "B",  "N",  "M",  ";",  ":",  "_",  "Shift"],
            [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
        ]

    ALT_GR_LAYOUT = [
        [ "Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
        [ "^", "1",  "²",  "³",  "4",  "5",  "6",  "{",  "[",  "]",  "}",  "\\",  "´", "Back"],  
        [ "Tab", "@",  "w",  "€",  "r",  "t",  "z",  "u",  "i",  "o",  "p",  "ü",  "~"],
        [ "Caps", "a",  "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  "ö",  "ä",  "#", "Enter"],
        [ "Shift", "|",  "y",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "-",  "Shift"],
        [ "Ctrl", "Win", "Alt", "Space", "", "", "", "", "", "AltGr", "App", "Ctrl"]
    ]

    # CTRL + functional keys results in actions
    # CTRL + ESC = Exit
    # CTRL + F1 = Hide/Show
    #                 First Row      "+"            "-"
    FUNCTIONAL_KEYS = LAYOUT[0] + [LAYOUT[2][-1], LAYOUT[4][-2]]


    # List of all modifiers. Values are as given by the keyHook executable
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

    # Special layout for some keys. Values are as given by the keyHook executable
    SPANS = {
        # (COL, ROW)
        "RÜCK": (1, 2),
        "EINGABE": (1, 2),
        "LEER": (6, 1),
    }


def index_of(key):
    for row in range(len(LAYOUT)):
        for col in range(len(LAYOUT[row])):
            if LAYOUT[row][col] == key:
                return (row, col)
    return None


def span_of(key):
    return SPANS.get(key, (1, 1))
