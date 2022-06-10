import string

__all__ = [
    'SYMBOL_NAMES'
]

# trying to follow the names used in :
# -> https://en.wikipedia.org/wiki/List_of_typographical_symbols_and_punctuation_marks
SYMBOL_NAMES = {
    '!': 'EXC',
    '#': 'SHARP',
    '$': 'DOLLAR',
    '%': 'PERCENT',
    '&': 'AMPERSAND',
    '\'': 'APOSTROPHE',
    '\"': 'DITTO_MARK',
    '`': 'BACKTICK',
    '(': 'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '*': 'ASTERISK',
    '+': 'PLUS',
    ',': 'COMMA',
    '-': 'DASH',
    '.': 'DOT',
    '/': 'SLASH',
    ':': 'COLON',
    ';': 'SEMICOLON',
    '<': 'LV',
    '=': 'EQ',
    '>': 'RV',
    '?': 'INT',
    '@': 'AT',
    '[': 'LB',
    '\\': 'COUNTER_SLASH',
    ']': 'RB',
    '^': 'HAT',
    '_': 'UNDERSCORE',
    '{': 'LS',
    '|': 'VBAR',
    '}': 'RS',
    '~': 'WAVE',
    ' ': 'SPACE',
    '\n': 'NEWLINE'
}

assert all(map(SYMBOL_NAMES.__contains__, string.punctuation + '\n ')), \
    "the symbol map must reference a name for each of the symbol characters."
