from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Iterator

from language.base.abstract import Writable, tok

__all__ = [
    'AbstractGR',
    'AtomGR',
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
    'INDENTED',
    'INVERTED',
    'Literal',
    'Match',
    'Optional',
    'Parallel',
    'ParallelGR',
    'Repeat0',
    'Repeat1',
    'RepeatGR',
    'Sequence',
    'SequenceGR',
    'Store',
    'String',
    'Variable',
]


@dataclass(frozen=True)
class AbstractGR(Writable, ABC):
    pass


@dataclass(frozen=True)
class ParallelGR(AbstractGR, ABC):
    pass


@dataclass(frozen=True)
class _Indented(AbstractGR):
    def __tokens__(self) -> Iterator[str]:
        yield ':i'


INDENTED: _Indented = _Indented()


@dataclass(frozen=True)
class _Inverted(AbstractGR):
    def __tokens__(self) -> Iterator[str]:
        yield '!'


INVERTED: _Inverted = _Inverted()


@dataclass(frozen=True)
class String(AbstractGR):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass(frozen=True)
class Variable(AbstractGR):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass(frozen=True)
class BuildGR(AbstractGR, ABC):
    type: Variable


@dataclass(frozen=True)
class Engine(AbstractGR):
    entry: Variable
    rules: tuple[BuildGR, ...]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield '\n'
            yield from tok(e)
        yield '\n'
        yield 'entry'
        yield ' '
        yield from tok(self.entry)


@dataclass(frozen=True)
class SequenceGR(ParallelGR, ABC):
    pass


@dataclass(frozen=True)
class BuildLemma(BuildGR):
    rule: ParallelGR
    indented: _Indented | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield 'lemma'
        if self.indented:
            yield ':i'
        yield ' '
        yield from tok(self.type)
        yield ' '
        yield '='
        yield ' '
        yield from tok(self.rule)


@dataclass(frozen=True)
class BuildToken(BuildGR):
    rule: ParallelGR
    
    def __tokens__(self) -> Iterator[str]:
        yield 'token'
        yield ' '
        yield from tok(self.type)
        yield ' '
        yield '='
        yield ' '
        yield from tok(self.rule)


@dataclass(frozen=True)
class Parallel(ParallelGR):
    rules: tuple[SequenceGR, ...]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield from tok(e)


@dataclass(frozen=True)
class BuildGroup(BuildGR):
    refs: tuple[Variable, ...]
    
    def __tokens__(self) -> Iterator[str]:
        yield 'group'
        yield ' '
        yield from tok(self.type)
        yield ' '
        yield '='
        yield ' '
        for i, e in enumerate(self.refs):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield from tok(e)


@dataclass(frozen=True)
class RepeatGR(SequenceGR, ABC):
    pass


@dataclass(frozen=True)
class Sequence(SequenceGR):
    rules: tuple[RepeatGR, ...]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
            yield from tok(e)


@dataclass(frozen=True)
class GroupingGR(RepeatGR, ABC):
    pass


@dataclass(frozen=True)
class Enum0(RepeatGR):
    separator: GroupingGR
    item: GroupingGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.separator)
        yield '.'
        yield from tok(self.item)


@dataclass(frozen=True)
class Enum1(RepeatGR):
    separator: GroupingGR
    item: GroupingGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.separator)
        yield '..'
        yield from tok(self.item)


@dataclass(frozen=True)
class Optional(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> Iterator[str]:
        yield '?'
        yield from tok(self.rule)


@dataclass(frozen=True)
class Repeat0(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> Iterator[str]:
        yield '*'
        yield from tok(self.rule)


@dataclass(frozen=True)
class Repeat1(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> Iterator[str]:
        yield '+'
        yield from tok(self.rule)


@dataclass(frozen=True)
class AtomGR(GroupingGR, ABC):
    pass


@dataclass(frozen=True)
class Grouping(GroupingGR):
    rule: ParallelGR
    
    def __tokens__(self) -> Iterator[str]:
        yield '['
        yield from tok(self.rule)
        yield ']'


@dataclass(frozen=True)
class Canonical(AtomGR):
    expr: String
    
    def __tokens__(self) -> Iterator[str]:
        yield '$'
        yield from tok(self.expr)


@dataclass(frozen=True)
class Literal(AtomGR):
    expr: String
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.expr)


@dataclass(frozen=True)
class Match(AtomGR):
    charset: String
    inverted: _Inverted | None = None
    
    def __tokens__(self) -> Iterator[str]:
        if self.inverted:
            yield '!'
        yield from tok(self.charset)


@dataclass(frozen=True)
class Store(AtomGR):
    type: Variable
    key: Variable
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.type)
        yield ' '
        yield '->'
        yield ' '
        yield from tok(self.key)
