import string

from tools import files
from tools.flow.tokenizer import *
from tools.flow.tokenizer.portable import make_tokenizer_function

# create the tokenizer
flow = Flow()

# make a proxy for the tokenizer entry
start = Proxy(flow, 0)

########################################################################################################################
# PATTERN DEFINITIONS
########################################################################################################################

# symbols
start.build('+', 'PLUS')
start.build('-', 'MINUS')
start.build('*', 'STAR')
start.build('/', 'SLASH')

# integer
start.repeat_plus(string.digits).default.build('Integer')

# whitespace
start.repeat_plus(string.whitespace).default.build('')

# once everything is defined, finalize the tokenizer to add default fallback on non-handled cases and error handling.
finalize(flow)

DIRECT_USE = False

if __name__ == '__main__':
    # export the data to json, which can then be re-used using other languages
    files.save_json_file('tokenizer_1.json', flow.data)

    if DIRECT_USE:
        # you can now use the created flow to tokenize some text
        tokenize = flow.__call__

    else:
        # or if you want to use the json file create a tokenizer function from the data
        data = tuple(files.load_json_file('tokenizer_1.json'))
        tokenize = make_tokenizer_function(data)

    src = "1 + 23 * 45 - 67 / 890"

    for token in tokenize(src):
        print(f"{token.type.ljust(8)} -> {token.content!r}")
