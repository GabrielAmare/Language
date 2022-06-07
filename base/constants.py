__all__ = [
    'SYMBOL_NAMES'
]

SYMBOL_NAMES = {
    # often used as wrappers
    '\'': 'SQ',  # single-quote
    '\"': 'DQ',  # double-quote
    '`': 'BT',  # back-tick
    '(': 'LP',  # left-parenthesis
    ')': 'RP',  # right-parenthesis
    '<': 'LC',  # left-chevron
    '>': 'RC',  # right-chevron
    '[': 'LB',  # left-bracket
    ']': 'RB',  # right-bracket
    '{': 'LS',  # left-spline
    '}': 'RS',  # right-spline
    # often used as punctuation
    ',': 'CM',  # comma
    ':': 'CL',  # colon
    ';': 'SC',  # semi-colon
    '.': 'DOT',  # dot
    '!': 'EM',  # exclamation-mark
    '?': 'QM',  # question-mark
    # often used as operators
    '+': 'PL',  # plus
    '-': 'DH',  # dash
    '*': 'SR',  # star
    '/': 'SL',  # slash
    '%': 'PC',  # percent
    '&': 'AS',  # ampersand
    '|': 'VB',  # vertical-bar
    '=': 'EQ',  # equal (sign)
    # whitespace
    ' ': 'SP',  # space
    '\t': 'TB',  # tab
    '\n': 'NL',  # new-line
    '\r': 'CR',  # carriage-return
    '\v': 'VT',  # vertical-tab
    '\f': 'FF',  # form-feed
    # unclassified symbols
    '#': 'SH',  # sharp
    '$': 'DL',  # dollar
    '@': 'AT',  # at
    '\\': 'CS',  # counter-slash
    '^': 'HT',  # hat
    '_': 'US',  # underscore
    '~': 'WV',  # wave
}
