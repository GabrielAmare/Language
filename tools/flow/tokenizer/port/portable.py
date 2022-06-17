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
                if options & 4:  # clr
                    char = None
                if build:  # build
                    token = Token(type=build, content=content, at=at, to=to)
                    yield token
                if options & 8:  # clear
                    content = ''
                    at = to
                state = action[1]
    
    return tokenizer
