from __future__ import annotations

import abc
import dataclasses
import functools
import typing

from base.processing import *
from .base import *

__all__ = [
    'Processor',
    'ProcessorContext'
]


@dataclasses.dataclass(frozen=True, order=True)
class Result:
    at: int
    to: int


@dataclasses.dataclass(frozen=True, order=True)
class Inner(Result):
    actions: ActionList = dataclasses.field(default_factory=list)
    roots: list[Variable] = dataclasses.field(default_factory=list)

    @classmethod
    def cursor(cls, at: int, actions: ActionList = None, roots: list[Variable] = None) -> Inner:
        if actions is None:
            actions = []
        if roots is None:
            roots = []
        return cls(at=at, to=at, actions=actions, roots=roots)

    def end_cursor(self, __type: Variable) -> Inner:
        return Inner.cursor(at=self.to, roots=self.roots + [__type], actions=[])

    def build(self, __type: Variable) -> Outer:
        return Outer(
            at=self.at,
            to=self.to,
            element=Lemma.build(str(__type), at=self.at, to=self.to, actions=self.actions)
        )

    def match(self, outer: Outer) -> Inner:
        assert self.to == outer.at
        return Inner(
            at=self.at,
            to=outer.to,
            actions=self.actions,
            roots=[]
        )

    def match_as(self, outer: Outer, key: Variable) -> Inner:
        assert self.to == outer.at
        return Inner(
            at=self.at,
            to=outer.to,
            actions=self.actions + [outer.set_as(key)],
            roots=[]
        )

    def match_in(self, outer: Outer, key: Variable) -> Inner:
        assert self.to == outer.at
        return Inner(
            at=self.at,
            to=outer.to,
            actions=self.actions + [outer.add_in(key)],
            roots=[]
        )


@dataclasses.dataclass(frozen=True, order=True)
class Outer(Result):
    element: Element

    def set_as(self, __key: Variable) -> SetAs:
        return SetAs(element=self.element, key=str(__key))

    def add_in(self, __key: Variable) -> AddIn:
        return AddIn(element=self.element, key=str(__key))

    @classmethod
    def from_token(cls, at: int, token: Token) -> Outer:
        return cls(at=at, to=at + 1, element=token)


@dataclasses.dataclass
class OuterMemo:
    _data: typing.Dict[int, Outer] = dataclasses.field(default_factory=dict)

    def save(self, result: Outer) -> None:
        self._data[result.at] = result

    def load(self, at: int) -> Outer:
        try:
            return self._data[at]

        except KeyError:
            raise ParsingError(f"No group element stored at {at!r} !")


@dataclasses.dataclass
class ProcessorContext(abc.ABC):
    processor: Processor
    tokens: list[Token]
    memo: OuterMemo = dataclasses.field(default_factory=OuterMemo)

    def get_token(self, at: int) -> Token:
        try:
            return self.tokens[at]

        except IndexError:
            raise ParsingError(msg=f"No token found at {at!r}.")

    def match_token(self, __type: Variable, at: int) -> Outer:
        """Try to match a token from the token list."""
        token = self.get_token(at)

        if token.type != str(__type):
            raise ParsingError(
                msg=f"Expected {str(__type)!r} at {at!r} but got {token.type!r} [{token.at_row}:{token.at_col}].")

        return Outer.from_token(at, token)

    def _read_list(self, rules: list[ParallelGR], inner: Inner) -> Inner:
        for rule in rules:
            inner = self.read(rule, inner)
        return inner

    def _read_repeat(self, inner: Inner, mn: int, mx: int, rules: list[ParallelGR]) -> Inner:
        for cycle in range(self.processor.max_repeat_iterations):
            if cycle == mx - 1:  # when mx == 0, this behaves as mx == infinity
                break

            try:
                inner = self._read_list(rules, inner)

            except ParsingError:
                if mn <= cycle:
                    break

                else:
                    raise ParsingError("Min number of cycles in repeat not reached !")

        else:
            raise RecursionError("Max iterations reached !")

        return inner

    @functools.singledispatchmethod
    def read(self, obj: ParallelGR, inner: Inner) -> Inner:
        """"""

    # # noinspection PyUnusedLocal
    # @read.register
    # def _(self, obj: Canonical, inner: Inner) -> Inner:
    #     """Canonical objects are completely ignored while reading."""
    #     return inner
    #
    # @read.register
    # def _(self, obj: RepeatPlus, inner: Inner) -> Inner:
    #     return self._read_repeat(mn=1, mx=0, rules=[obj.rule], inner=inner)
    #
    # @read.register
    # def _(self, obj: Repeat, inner: Inner) -> Inner:
    #     mn = Integer.to_int(obj.mn)
    #     mx = Integer.to_int(obj.mx)
    #     return self._read_repeat(mn=mn, mx=mx, rules=[obj.rule], inner=inner)
    #
    # @read.register
    # def _(self, obj: Enum0, inner: Inner) -> Inner:
    #     inner = self._read_list([obj.element], inner)
    #     return self._read_repeat(mn=0, mx=0, rules=[obj.separator, obj.element], inner=inner)
    #
    # @read.register
    # def _(self, obj: Enum1, inner: Inner) -> Inner:
    #     inner = self._read_list([obj.element], inner)
    #     return self._read_repeat(mn=1, mx=0, rules=[obj.separator, obj.element], inner=inner)

    @read.register
    def _(self, obj: Match, inner: Inner) -> Inner:
        # # when the match refer to an alias object
        # # the match keeps the same scope (no outer built).
        # if self.processor.parser.has(obj.type):
        #     toplevel = self.processor.parser.get(obj.type)
        #     if isinstance(toplevel, Alias):
        #         return self.read(toplevel.rule, inner)

        outer = self.build(obj.type, inner)
        return inner.match(outer)

    @read.register
    def _(self, obj: MatchAs, inner: Inner) -> Inner:
        outer = self.build(obj.type, inner)
        # match `outer` as value of `obj.key` in `inner`
        return inner.match_as(outer, obj.key)

    @read.register
    def _(self, obj: MatchIn, inner: Inner) -> Inner:
        outer = self.build(obj.type, inner)
        # match `outer` in values of `obj.key` in `inner`
        return inner.match_in(outer, obj.key)

    @read.register
    def _(self, obj: Sequence, inner: Inner) -> Inner:
        return self._read_list(obj.rules, inner)

    @read.register
    def _(self, obj: Parallel, inner: Inner) -> Inner:
        for rule in obj.rules:
            try:
                return self.read(rule, inner)

            except ParsingError:
                continue

        raise ParsingError("No items matched in Parallel rule.")

    @read.register
    def _(self, obj: Optional, inner: Inner) -> Inner:
        try:
            return self.read(obj.rule, inner)
        except ParsingError:
            return inner

    @read.register
    def _(self, obj: Grouping, inner: Inner) -> Inner:
        return self.read(obj.rule, inner)

    @read.register
    def _(self, obj: Negative, inner: Inner) -> Inner:
        try:
            self.read(obj.rule, inner)

        except ParsingError:
            return inner

        raise ParsingError("Negative match !")

    @read.register
    def _(self, obj: RepeatStar, inner: Inner) -> Inner:
        return self._read_repeat(mn=0, mx=0, rules=[obj.rule], inner=inner)

    @functools.singledispatchmethod
    def build_toplevel(self, obj: TopLevel, origin: Inner) -> Outer:
        """"""
        raise NotImplementedError(type(obj))

    @build_toplevel.register
    def _(self, obj: Branch, origin: Inner) -> Outer:
        inner = origin.end_cursor(obj.type)
        inner = self.read(obj.rule, inner)
        return inner.build(obj.type)

    def build_group_once(self, obj: Group, inner: Inner) -> Outer:
        for sub_type in obj.types:
            try:
                return self.build(sub_type, inner)

            except ParsingError:
                continue

        else:
            raise ParsingError(msg=f"Unable to build group {str(obj.type)!r}.")

    def build_group_step(self, obj: Group, inner: Inner, skip: typing.Callable[[Variable], bool]) -> Outer:
        for sub_type in obj.types:
            if skip(sub_type):  # Non Recursive Items will not be triggered if the
                continue

            try:
                return self.build(sub_type, inner)

            except ParsingError:
                continue

        else:
            raise ParsingError(msg=f"Unable to build group {str(obj.type)!r}.")

    def match_group(self, obj: Group, inner: Inner) -> Outer:
        outer = self.memo.load(inner.at)

        if not self.processor.parser.is_element_of(obj.type, outer.element.type):
            raise ParsingError(msg=f"The stored element at {inner.at!r} does not match {obj.type!r}")

        return outer

    def build_group_loop(self, obj: Group, inner: Inner) -> Outer:
        group_recursion = self.processor.parser.get_recursion(obj.type)

        for cycle in range(self.processor.max_repeat_iterations):
            try:
                if cycle:
                    result = self.build_group_step(obj, inner, skip=lambda __type: not group_recursion[__type])
                else:
                    result = self.build_group_once(obj, inner)
            except ParsingError:
                return self.match_group(obj, inner)

            self.memo.save(result)

        raise RecursionError(f"Max recursion reached while trying to build group {obj!r} !")

    @build_toplevel.register
    def _(self, obj: Group, origin: Inner) -> Outer:
        inner = origin.end_cursor(obj.type)

        if obj.type in origin.roots:  # match case
            return self.match_group(obj, inner)

        group_recursion = self.processor.parser.get_recursion(obj.type)
        group_is_left_recursive = any(group_recursion.values())

        if group_is_left_recursive:  # recursive case
            return self.build_group_loop(obj, inner)

        return self.build_group_once(obj, inner)

    def build(self, __type: Variable, inner: Inner) -> Outer:
        if not self.processor.parser.has(__type):
            return self.match_token(__type, inner.to)

        obj = self.processor.parser.get(__type)

        return self.build_toplevel(obj, inner)


@dataclasses.dataclass
class Processor:
    reader: Reader
    max_repeat_iterations: int = 100
    debug: bool = False
    models: object = None
    show_tokens_on_error: int = 3

    @functools.cached_property
    def parser(self) -> Parser:
        return self.reader.parser

    def __call__(self, tokens: list[Token]) -> Element:
        """Process the given tokens"""
        context = ProcessorContext(processor=self, tokens=tokens)
        inner = Inner.cursor(at=0, actions=[], roots=[])
        outer = context.build(self.parser.start, inner)

        if (outer.at, outer.to) == (0, len(tokens)):
            return outer.element

        raise ParsingError(f"\n--> Incomplete parsing stopped at {outer.to!r} on {len(tokens)!r} tokens.\n" +
                           "\n".join(
                               "  |" + " >"[outer.to == index] + " " + repr(token)
                               for index, token in enumerate(tokens)
                               if abs(outer.to - index) <= self.show_tokens_on_error
                           ))

    def build(self, element: Element) -> object:
        if not hasattr(self.models, element.type):
            raise NotImplementedError(f"{element.type} not defined within models !")

        factory = getattr(self.models, element.type)

        if isinstance(element, Token):
            config = {
                'content': element.content
            }

        elif isinstance(element, Lemma):
            config = {
                key: list(map(self.build, value)) if isinstance(value, list) else self.build(value)
                for key, value in element.data.items()
            }

        else:
            raise NotImplementedError(f"undefined element class {element.__class__.__name__} !")

        return factory(**config)
