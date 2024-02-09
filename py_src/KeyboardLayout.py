LAYOUT = [
        [ "ESC", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"], 
        [ "ZIRKUMFLEX", "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "ß",  "AKUT", "RÜCK"],  
        [ "TABULATOR", "Q",  "W",  "E",  "R",  "T",  "Z",  "U",  "I",  "O",  "P",  "Ü",  "+"],
        [ "FESTSTELL", "A",  "S",  "D",  "F",  "G",  "H",  "J",  "K",  "L",  "Ö",  "Ä",  "#", "EINGABE"],
        [ "UMSCHALT", "<",  "Y",  "X",  "C",  "V",  "B",  "N",  "M",  ",",  ".",  "-",  "UMSCHALT RECHTS"],
        [ "STRG", "LINKE WINDOWS", "ALT", "LEER", "", "", "", "", "", "ALT GR", "ANWENDUNG", "STRG-RECHTS"]
    ]


SPANS = {
    # (COL, ROW)
    "RÜCK": (1, 2),
    "EINGABE": (1, 2),
    "LEER": (6, 1),
}

def span_of(key):
    return SPANS.get(key, (1, 1))


def get_shift_mapping(chr):
    without_shift = "^1234567890ß´qwertzuiopü+asdfghjklöä#<yxcvbnm,.-"
    with_shift = "!\"§$%&/()=QWERTZUIOPÜ*ASDFGHJKLÖÄ'YXCVBNM;:_"
    if chr not in without_shift:
        return chr
    return with_shift[without_shift.index(chr)] if chr in without_shift else chr

def get_alt_gr_mapping(chr):
    without_alt_gr = "237890ßqe<+"
    with_alt_gr = "²³{[]}\\@€|~" 
    if chr not in without_alt_gr:
        return chr
    return with_alt_gr[without_alt_gr.index(chr)] if chr in without_alt_gr else chr

SPECIAL_MAPPINGS = {
    "ESC": "Esc",
    "ZIRKUMFLEX": "^",
    "TABULATOR": "Tab",
    "FESTSTELL": "Caps",
    "UMSCHALT": "Shift",
    "STRG": "Ctrl",
    "LINKE WINDOWS" : "Win",
    "ALT": "Alt",
    "LEER": "Space",
    "ALT GR": "AltGr",
    "ANWENDUNG": "App",
    "STRG-RECHTS": "Ctrl",
    "UMSCHALT RECHTS": "Shift",
    "EINGABE": "Enter",
    "RÜCK": "Back",
    "AKUT": "´"
}
