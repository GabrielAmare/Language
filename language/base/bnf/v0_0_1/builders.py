from __future__ import annotations

import abc
import typing

from .models import *

__all__ = [
    'AbstractContext',
    'GroupContext',
    'LemmaContext',
    'TokenContext',
]

import dataclasses


@dataclasses.dataclass
class AbstractContext(abc.ABC):
    root: GroupContext | None
    name: str
    
    @abc.abstractmethod
    def definition(self) -> BuildGR:
        pass


@dataclasses.dataclass
class GroupContext(AbstractContext):
    _groups: list[GroupContext] = dataclasses.field(default_factory=list)
    _lemmas: list[LemmaContext] = dataclasses.field(default_factory=list)
    _tokens: list[TokenContext] = dataclasses.field(default_factory=list)
    _references: list[GroupContext] = dataclasses.field(default_factory=list)
    
    def group(self, name: str | GroupContext) -> GroupContext:
        if isinstance(name, str):
            ctx = GroupContext(
                root=self,
                name=name,
            )
            self._groups.append(ctx)
            return ctx
        elif isinstance(name, GroupContext):
            self._references.append(name)
            return name
    
    def lemma(self, name: str, rule: ParallelGR, indented: bool = False) -> GroupContext:
        ctx = LemmaContext(
            root=self,
            name=name,
            rule=rule,
            indented=indented,
        )
        self._lemmas.append(ctx)
        return self
    
    def token(self, name: str, rule: ParallelGR) -> GroupContext:
        ctx = TokenContext(
            root=self,
            name=name,
            rule=rule,
        )
        self._tokens.append(ctx)
        return self
    
    def definition(self) -> BuildGroup:
        return BuildGroup(
            type=Variable(self.name),
            refs=tuple([
                *(group.name for group in self._groups),
                *(lemma.name for lemma in self._lemmas),
                *(token.name for token in self._tokens),
                *(ref.name for ref in self._references),
            ]),
        )
    
    def definitions(self) -> typing.Iterator[BuildGR]:
        yield self.definition()
        for group in self._groups:
            yield from group.definitions()
        for lemma in self._lemmas:
            yield lemma.definition()
        for token in self._tokens:
            yield token.definition()
    
    def engine(self) -> Engine:
        return Engine(
            entry=Variable(self.name),
            rules=tuple(self.definitions()),
        )


@dataclasses.dataclass
class LemmaContext(AbstractContext):
    rule: ParallelGR
    indented: bool
    
    def definition(self) -> BuildLemma:
        return BuildLemma(
            type=Variable(self.name),
            rule=self.rule,
            indented=INDENTED if self.indented else None,
        )


@dataclasses.dataclass
class TokenContext(AbstractContext):
    rule: ParallelGR
    
    def definition(self) -> BuildToken:
        return BuildToken(
            type=Variable(self.name),
            rule=self.rule,
        )
