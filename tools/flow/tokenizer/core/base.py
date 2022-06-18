import dataclasses

__all__ = [
    'EOT',
    
    'VALID',
    'ERROR',
    
    'ADD',
    'INC',
    'CLR',
    'CLEAR',
    
    'NEW',
    'STAY',
    'ENTRY',
    
    'Token',
    'TokenizerError',
    'Context'
]


@dataclasses.dataclass
class NamedConstant:
    name: str
    
    def __str__(self):
        return self.name


EOT = '\0'
VALID = -1
ERROR = -2

ADD = 1  # Add the char to the context content.
INC = 2  # Increment the index.
CLR = 4  # Get rid of the element (this will ask a new element).
CLEAR = 8  # Clear the context content & move the at cursor to the current index.

NEW = NamedConstant('NEW')
STAY = NamedConstant('STAY')
ENTRY = NamedConstant('ENTRY')


@dataclasses.dataclass
class Token:
    type: str
    content: str
    at: int
    to: int


@dataclasses.dataclass
class TokenizerError(ValueError):
    token: Token


@dataclasses.dataclass
class Context:
    at: int = 0
    to: int = 0
    content: str = ''
    tokens: list[Token] = dataclasses.field(default_factory=list)
