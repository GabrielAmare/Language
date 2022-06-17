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
                if action[0]:  # add
                    content += char
                if action[1]:  # use
                    to += 1
                if action[2]:  # clr
                    char = None
                if action[3]:
                    token = Token(type=action[3], content=content, at=at, to=to)
                    yield token
                if action[4]:
                    content = ''
                    at = to
                state = action[5]
    
    return tokenizer
