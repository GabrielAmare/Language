from __future__ import annotations

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
    'INDENTED',
    'INVERTED',
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
    'String',
    'Variable',
]


@dataclasses.dataclass
class AbstractGR(language.base.abstract.Writable, abc.ABC):
    pass


@dataclasses.dataclass
class BuildGR(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class ParallelGR(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class _Indented(AbstractGR):
    def __tokens__(self) -> typing.Iterator[str]:
        yield ':i'


INDENTED: _Indented = _Indented()


@dataclasses.dataclass
class _Inverted(AbstractGR):
    def __tokens__(self) -> typing.Iterator[str]:
        yield '!'


INVERTED: _Inverted = _Inverted()


@dataclasses.dataclass
class String(AbstractGR):
    content: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield str(self.content)


@dataclasses.dataclass
class Variable(AbstractGR):
    content: str
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield str(self.content)


@dataclasses.dataclass
class Engine(AbstractGR):
    entry: Variable
    rules: list[BuildGR]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield '\n'
            yield from language.base.abstract.tok(e)
        yield '\n'
        yield 'entry'
        yield ' '
        yield from language.base.abstract.tok(self.entry)


@dataclasses.dataclass
class SequenceGR(ParallelGR, abc.ABC):
    pass


@dataclasses.dataclass
class Parallel(ParallelGR):
    rules: list[SequenceGR]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield from language.base.abstract.tok(e)


@dataclasses.dataclass
class BuildGroup(BuildGR):
    type: Variable
    refs: list[Variable]
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'group'
        yield ' '
        yield from language.base.abstract.tok(self.type)
        yield ' '
        yield '='
        yield ' '
        for i, e in enumerate(self.refs):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield from language.base.abstract.tok(e)


@dataclasses.dataclass
class BuildLemma(BuildGR):
    type: Variable
    rule: ParallelGR
    indented: _Indented | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'lemma'
        if self.indented:
            yield from language.base.abstract.tok(self.indented)
        yield ' '
        yield from language.base.abstract.tok(self.type)
        yield ' '
        yield '='
        yield ' '
        yield from language.base.abstract.tok(self.rule)


@dataclasses.dataclass
class BuildToken(BuildGR):
    type: Variable
    rule: ParallelGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'token'
        yield ' '
        yield from language.base.abstract.tok(self.type)
        yield ' '
        yield '='
        yield ' '
        yield from language.base.abstract.tok(self.rule)


@dataclasses.dataclass
class RepeatGR(SequenceGR, abc.ABC):
    pass


@dataclasses.dataclass
class Sequence(SequenceGR):
    rules: list[RepeatGR]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
            yield from language.base.abstract.tok(e)


@dataclasses.dataclass
class GroupingGR(RepeatGR, abc.ABC):
    pass


@dataclasses.dataclass
class Enum0(RepeatGR):
    separator: GroupingGR
    item: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from language.base.abstract.tok(self.separator)
        yield '.'
        yield from language.base.abstract.tok(self.item)


@dataclasses.dataclass
class Enum1(RepeatGR):
    separator: GroupingGR
    item: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from language.base.abstract.tok(self.separator)
        yield '..'
        yield from language.base.abstract.tok(self.item)


@dataclasses.dataclass
class Optional(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '?'
        yield from language.base.abstract.tok(self.rule)


@dataclasses.dataclass
class Repeat0(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '*'
        yield from language.base.abstract.tok(self.rule)


@dataclasses.dataclass
class Repeat1(RepeatGR):
    rule: GroupingGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '+'
        yield from language.base.abstract.tok(self.rule)


@dataclasses.dataclass
class MatchGR(GroupingGR, abc.ABC):
    pass


@dataclasses.dataclass
class Grouping(GroupingGR):
    rule: ParallelGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '['
        yield from language.base.abstract.tok(self.rule)
        yield ']'


@dataclasses.dataclass
class Canonical(MatchGR):
    expr: String
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '$'
        yield from language.base.abstract.tok(self.expr)


@dataclasses.dataclass
class Literal(MatchGR):
    expr: String
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from language.base.abstract.tok(self.expr)


@dataclasses.dataclass
class MatchAs(MatchGR):
    type: Variable
    key: Variable
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '<'
        yield from language.base.abstract.tok(self.type)
        yield ' '
        yield 'as'
        yield ' '
        yield from language.base.abstract.tok(self.key)
        yield '>'


@dataclasses.dataclass
class MatchChar(MatchGR):
    charset: String
    inverted: Inverted | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        if self.inverted:
            yield from language.base.abstract.tok(self.inverted)
        yield from language.base.abstract.tok(self.charset)


@dataclasses.dataclass
class MatchIn(MatchGR):
    type: Variable
    key: Variable
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '<'
        yield from language.base.abstract.tok(self.type)
        yield ' '
        yield 'in'
        yield ' '
        yield from language.base.abstract.tok(self.key)
        yield '>'
