translator = {
    '. _': 'A',
    '_ . . .': 'B',
    '_ . _ .': 'C',
    '_ . .': 'D',
    '.': 'E',
    '. . _ .': 'F',
    '_ _ .': 'G',
    '. . . .': 'H',
    '. .': 'I',
    '. _ _ _': 'J',
    '_ . _': 'K',
    '. _ . .': 'L',
    '_ _': 'M',
    '_ .': 'N',
    '_ _ _': 'O',
    '. _ _ .': 'P',
    '_ _ . _': 'Q',
    '. _ .': 'R',
    '. . .': 'S',
    '_': 'T',
    '. . _': 'U',
    '. . . _': 'V',
    '. _ _': 'W',
    '_ . . _': 'X',
    '_ . _ _': 'Y',
    '_ _ . .': 'Z',
    '. _ _ _ _': '1',
    '. . _ _ _': '2',
    '. . . _ _': '3',
    '. . . . _': '4',
    '. . . . .': '5',
    '_ . . . .': '6',
    '_ _ . . .': '7',
    '_ _ _ . ': '8',
    '_ _ _ _ .': '9',
    '_ _ _ _ _': '0',
    '_ _ . . _ _': ',',
    '. _ . _ . _': '.',
    '. . _ _ . .': '?',
    '_ . . _ .': '/',
    '_ _ _ . . .': ':',
    '_ . . . . _': '-',
    '. _ _ _ _ .': '\'',
    '. _ . . _ .': '\"',
    '_ . _ . _ .': ';',
    '_ . _ _ ': '(',
    '_ . _ _ . _': ')',
    '_ . . . _': '=',
    '. _ . _ .': '+',
    '_ . . _': 'x',
    '. _ _ . _ .': '@',
    '. . _ _': ' ',
    '. . _ .': 'BACKSPACE',
    '. _ . _': 'AUTOCOMPLETE',

}

phrases = [
    "Yes",
    "No",
    "Thirsty",
    "Medicine",
    "Okay",
    "Good",
    "I am fine",
    "Doctor/Nurse",
    "Help",
    "Washroom",
    "Hungry",
    "Good Morning/Evening/Night/Afternoon",
    "What’s your name?",
    "End of message",
    "What is the time?",
    "How are you?",
    "Did you eat?",
    "Can you switch the TV on?",
    "I want to go out.",
    "I’m in pain.",
    "Hands",
    "Legs",
    "Head",
    "Fingers",
    "Toes",
    "Chest",
    "Stomach",
    "Good boy/good girl(pet)",
    "fan/ac/lights",

]


def interpret(content):
    try:
        return translator[content]
    except:
        return ''


def content_return(content):
    out = []
    for phrase in phrases:
        if phrase.startswith(content):
            out += [phrase]
    return out
