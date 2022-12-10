import abc
import dataclasses
import typing

import language.base.abstract

__all__ = [
    'AbstractGR',
    'Statement',
    'Module',
]


@dataclasses.dataclass
class AbstractGR(language.base.abstract.Writable, abc.ABC):
    pass


@dataclasses.dataclass
class Statement(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class Module(AbstractGR):
    statements: list[Statement]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.statements):
            if i:
                yield '\n'
            yield from e.__tokens__()
