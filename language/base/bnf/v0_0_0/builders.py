from __future__ import annotations

import abc
import typing

from .models import *

__all__ = [
    'EngineBuilder',
    'AbstractContext',
    'GroupContext',
    'LemmaContext',
    'TokenContext',
]

import dataclasses


@dataclasses.dataclass
class EngineBuilder:
    entry: str
    _rules: dict[str, BuildGroup] = dataclasses.field(default_factory=dict)
    
    def token(self, __type: str, rule: ParallelGR) -> EngineBuilder:
        assert __type not in self._rules
        self._rules[__type] = BuildToken(type=__type, rule=rule)
        return self
    
    def lemma(self, __type: str, rule: ParallelGR, indented: bool = False) -> EngineBuilder:
        assert __type not in self._rules, f"{__type!r} have been found in {list(self._rules.keys())!r}"
        self._rules[__type] = BuildLemma(type=__type, rule=rule, indented=INDENTED if indented else None)
        return self
    
    def group(self, __type: str, __refs: typing.Iterator[str]) -> EngineBuilder:
        assert __type not in self._rules
        self._rules[__type] = BuildGroup(type=__type, refs=tuple(__refs))
        return self
    
    def build(self) -> Engine:
        assert self.entry
        assert self.entry in self._rules
        
        return Engine(
            rules=tuple(self._rules.values()),
            entry=self.entry
        )


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
            ctx = GroupContext(root=self, name=name)
            self._groups.append(ctx)
            return ctx
        elif isinstance(name, GroupContext):
            self._references.append(name)
            return name
    
    def lemma(self, name: str, rule: ParallelGR, indented: bool = False) -> GroupContext:
        ctx = LemmaContext(root=self, name=name, rule=rule, indented=indented)
        self._lemmas.append(ctx)
        return self
    
    def token(self, name: str, rule: ParallelGR) -> GroupContext:
        ctx = TokenContext(root=self, name=name, rule=rule)
        self._tokens.append(ctx)
        return self
    
    def definition(self) -> BuildGroup:
        return BuildGroup(type=self.name, refs=tuple([
            *(group.name for group in self._groups),
            *(lemma.name for lemma in self._lemmas),
            *(token.name for token in self._tokens),
            *(ref.name for ref in self._references),
        ]))
    
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
            entry=self.name,
            rules=tuple(self.definitions())
        )


@dataclasses.dataclass
class LemmaContext(AbstractContext):
    rule: ParallelGR
    indented: bool
    
    def definition(self) -> BuildLemma:
        return BuildLemma(
            type=self.name,
            rule=self.rule,
            indented=INDENTED if self.indented else None
        )


@dataclasses.dataclass
class TokenContext(AbstractContext):
    rule: ParallelGR
    
    def definition(self) -> BuildToken:
        return BuildToken(
            type=self.name,
            rule=self.rule
        )
