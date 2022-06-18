import typing

from tools.flow.tokenizer.core import *

__all__ = [
    'make_tokenizer_function'
]


def make_tokenizer_function(managers: FlowData) -> typing.Callable[[str], typing.Iterator[Token]]:
    def tokenizer(text: str) -> typing.Iterator[Token]:
        handler: HandlerData
        action: ActionData
        default: ActionData | None
        chars: ConditionData
        options: int
        build: str
        
        state: int = 0
        content: str = ''
        at: int = 0
        to: int = 0
        at_row: int = 0
        at_col: int = 0
        to_row: int = 0
        to_col: int = 0
        for char in text + EOT:
            while char:
                handlers, default = managers[state]
                for chars, action in handlers:
                    if char in chars:
                        break
                else:
                    action = default
                if not action:
                    raise NotImplementedError
                options, build = action[0]
                if options & 1:  # add
                    content += char
                if options & 2:  # inc
                    to += 1
                    if char == '\n':
                        at_row += 1
                        at_col = 0
                    else:
                        at_col += 1
                if options & 4:  # clr
                    char = None
                if build:  # build
                    token = Token(type=build, content=content,
                                  at=at, to=to,
                                  at_row=at_row, at_col=at_col,
                                  to_row=to_row, to_col=to_col)
                    yield token
                if options & 8:  # clear
                    content = ''
                    at = to
                    at_row = to_row
                    at_col = to_col
                state = action[1]
    
    return tokenizer
