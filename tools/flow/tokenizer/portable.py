import typing

from .base import Token, EOT
from .data import FlowData

__all__ = [
    'make_tokenizer_function'
]


def make_tokenizer_function(managers: FlowData) -> typing.Callable[[str], typing.Iterator[Token]]:
    def tokenizer(text: str) -> typing.Iterator[Token]:
        state = 0
        content = ''
        at = 0
        to = 0
        for char in text + EOT:
            while char:
                manager = managers[state]
                action = manager[1]
                for handler in manager[0]:
                    if char in handler[0]:
                        action = handler[1]
                        break
                if not action:
                    raise NotImplementedError
                params = action[0]
                if params[0]:  # add
                    content += char
                if params[1]:  # inc
                    to += 1
                if params[2]:  # clr
                    char = None
                if params[3]:  # build
                    token = Token(type=params[3], content=content, at=at, to=to)
                    yield token
                if params[4]:  # clear
                    content = ''
                    at = to
                state = action[1]
    
    return tokenizer
