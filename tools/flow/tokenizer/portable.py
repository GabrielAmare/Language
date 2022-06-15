import typing

from .base import Token, EOT
from .data import FlowData

__all__ = [
    'make_tokenizer_function'
]


def make_tokenizer_function(struct: FlowData) -> typing.Callable[[str], typing.Iterator[Token]]:
    def tokenizer(text: str) -> typing.Iterator[Token]:
        state = 0
        content = ''
        at = 0
        to = 0
        managers, omits = struct
        for char in text + EOT:
            while char:
                handlers, default = managers[state]
                for handler in handlers:
                    if char in handler[0]:
                        action = handler[1]
                        break
                else:
                    if not default:
                        raise NotImplementedError
                    action = default
                add, use, build, state = action
                if add:
                    content += char
                if use:
                    to += 1
                    char = None
                if build:
                    token = Token(type=build, content=content, at=at, to=to)
                    content = ''
                    at = to
                    if token.type not in omits:
                        yield token

    return tokenizer
