import dataclasses

__all__ = [
    'EOT',

    'VALID',
    'ERROR',

    'INCLUDE',
    'EXCLUDE',
    'NOTHING',

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

INCLUDE = NamedConstant('INCLUDE')
EXCLUDE = NamedConstant('EXCLUDE')
NOTHING = NamedConstant('NOTHING')

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
