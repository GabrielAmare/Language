from __future__ import annotations

import abc
import dataclasses
import typing

__all__ = [
    'Element',
    'Token',
    'Lemma',
    'LemmaData',
    'LemmaValue',
    'ActionList',
    'Action',
    'SetAs',
    'AddIn',
    'ParsingError',
]


@dataclasses.dataclass
class Element:
    """
        Element class is an abstraction of elements that can be found in/built from a text input.
        :param type: Type of the element.
        :param at: Starting index of the element.
        :param to: Ending index of the element.
    """
    type: str
    at: int
    to: int


@dataclasses.dataclass
class Span:
    """
        :param at: starting index.
        :param to: ending index.
    """
    at: int
    to: int


@dataclasses.dataclass
class Token(Element):
    """Token elements are built directly from a text input."""
    content: str
    at_row: int = -1
    at_col: int = -1


@dataclasses.dataclass
class Action(abc.ABC):
    element: Element

    @abc.abstractmethod
    def apply_on(self, data: LemmaData) -> None:
        """"""


@dataclasses.dataclass
class SetAs(Action):
    key: str

    def apply_on(self, data: LemmaData) -> None:
        assert self.key not in data, f"cannot duplicate key {self.key!r}"
        data[self.key] = self.element


@dataclasses.dataclass
class AddIn(Action):
    key: str

    def apply_on(self, data: LemmaData) -> None:
        if self.key in data:
            assert isinstance(data[self.key], list), f"cannot assign a single element to a list of elements."
            data[self.key].append(self.element)
        else:
            data[self.key] = [self.element]


LemmaValue = typing.Union[Element, list[Element]]
LemmaData = typing.Dict[str, LemmaValue]
ActionList = list[Action]


@dataclasses.dataclass
class Lemma(Element):
    """AST (AbstractSyntaxTree) elements are built from Token elements or others AST elements."""
    data: LemmaData

    def has(self, __key: str) -> bool:
        return __key in self.data

    def get(self, __key: str) -> LemmaValue:
        return self.data.get(__key)

    @classmethod
    def build(cls, __type: str, at: int, to: int, actions: ActionList) -> Lemma:
        data: LemmaData = {}
        for action in actions:
            action.apply_on(data)

        return cls(type=__type, at=at, to=to, data=data)


@dataclasses.dataclass
class ParsingError(Exception):
    """Error returned when a processor was unable to parse the AST correctly."""
    msg: str = ''

    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return self.__class__.__name__
