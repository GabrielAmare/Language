import abc
import dataclasses
import typing

import language.base.abstract

__all__ = [
    'AbstractGR',
    'BuildGR',
    'BuildGroup',
    'BuildLemma',
    'BuildToken',
    'Canonical',
    'Engine',
    'Enum0',
    'Enum1',
    'Grouping',
    'GroupingGR',
    'Literal',
    'MatchAs',
    'MatchChar',
    'MatchGR',
    'MatchIn',
    'Optional',
    'Parallel',
    'ParallelGR',
    'Repeat0',
    'Repeat1',
    'RepeatGR',
    'Sequence',
    'SequenceGR',
    'INDENTED',
]


@dataclasses.dataclass(frozen=True)
class AbstractGR(language.base.abstract.Writable, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class BuildGR(AbstractGR, abc.ABC):
    type: str


@dataclasses.dataclass(frozen=True)
class ParallelGR(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class SequenceGR(ParallelGR, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class RepeatGR(SequenceGR, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class GroupingGR(RepeatGR, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class MatchGR(GroupingGR, abc.ABC):
    pass


@dataclasses.dataclass(frozen=True)
class Engine(AbstractGR):
    entry: str
    rules: tuple[BuildGR, ...]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield '\n'
            yield from e.__tokens__()
        yield '\n'
        yield 'entry'
        yield ' '
        yield self.entry


@dataclasses.dataclass(frozen=True)
class BuildGroup(BuildGR):
    refs: tuple[str, ...]
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'group'
        yield ' '
        yield self.type
        yield ' '
        yield '='
        yield ' '
        for i, e in enumerate(self.refs):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield e


@dataclasses.dataclass(frozen=True)
class _Indented(AbstractGR):
    def __tokens__(self) -> typing.Iterator[str]:
        yield '@I'


INDENTED: _Indented = _Indented()


@dataclasses.dataclass(frozen=True)
class BuildLemma(BuildGR):
    rule: ParallelGR
    indented: _Indented | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'lemma'
        yield ' '
        yield self.type
        yield ' '
        yield '='
        yield ' '
        yield from self.rule.__tokens__()


@dataclasses.dataclass(frozen=True)
class BuildToken(BuildGR):
    rule: ParallelGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'token'
        yield ' '
        yield self.type
        yield ' '
        yield '='
        yield ' '
        yield from self.rule.__tokens__()


@dataclasses.dataclass(frozen=True)
class Parallel(ParallelGR):
    rules: tuple[SequenceGR, ...]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield from e.__tokens__()


@dataclasses.dataclass(frozen=True)
class Sequence(SequenceGR):
    rules: tuple[RepeatGR, ...]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
            yield from e.__tokens__()


@dataclasses.dataclass(frozen=True)
class Enum0(RepeatGR):
    item: GroupingGR
    separator: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.separator.__tokens__()
        yield '.'
        yield from self.item.__tokens__()


@dataclasses.dataclass(frozen=True)
class Enum1(RepeatGR):
    item: GroupingGR
    separator: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.separator.__tokens__()
        yield '..'
        yield from self.item.__tokens__()


@dataclasses.dataclass(frozen=True)
class Optional(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '?'
        yield from self.rule.__tokens__()


@dataclasses.dataclass(frozen=True)
class Repeat0(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '*'
        yield from self.rule.__tokens__()


@dataclasses.dataclass(frozen=True)
class Repeat1(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '+'
        yield from self.rule.__tokens__()


@dataclasses.dataclass(frozen=True)
class Grouping(GroupingGR):
    rule: ParallelGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '['
        yield from self.rule.__tokens__()
        yield ']'


@dataclasses.dataclass(frozen=True)
class Canonical(MatchGR):
    expr: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '$'
        yield repr(self.expr)


@dataclasses.dataclass(frozen=True)
class Literal(MatchGR):
    expr: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield repr(self.expr)


@dataclasses.dataclass(frozen=True)
class MatchAs(MatchGR):
    key: str
    type: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '<'
        yield self.type
        yield ' '
        yield 'as'
        yield ' '
        yield self.key
        yield '>'


@dataclasses.dataclass(frozen=True)
class MatchChar(MatchGR):
    charset: str
    inverted: bool | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        if self.inverted:
            yield '!'
        yield repr(self.charset)


@dataclasses.dataclass(frozen=True)
class MatchIn(MatchGR):
    key: str
    type: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '<'
        yield self.type
        yield ' '
        yield 'in'
        yield ' '
        yield self.key
        yield '>'
