import dataclasses
import typing

from .base import *

__all__ = [
    'TypeSwitch'
]


@dataclasses.dataclass
class TypeSwitch:
    """
        Data structure used to represent python switches like this :
            if isinstance($arg$, $types[0]$):
                $cases[0]$
            elif isinstance($arg$, $types[1]$):
                $cases[1]$
            ...
            else:
                $default$
    """
    arg: Expression
    types: list[Expression]
    cases: list[Block]
    default: typing.Optional[Block]

    def items(self) -> typing.Iterator[tuple[Expression, Block]]:
        yield from zip(self.types, self.cases)
