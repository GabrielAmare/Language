import abc
import dataclasses
import typing

from ._1_elements import Element
from ._2_matches import MatchError, Match, MatchUnit, MatchList

__all__ = [
    'Pattern',
    'PatternSequence',
    'PatternRepeat',
    'PatternOptional',
    'AtomPattern',
]


class Pattern(abc.ABC):
    """This class represent a pattern."""

    @abc.abstractmethod
    def match(self, index: int, elements: list[Element]) -> tuple[int, Match]:
        """"""


@dataclasses.dataclass
class PatternSequence(Pattern):
    """This class represent a sequence of patterns to be matched in order."""
    patterns: list[Pattern]

    def match(self, index: int, elements: list[Element]) -> tuple[int, Match]:
        total = MatchList()

        for pattern in self.patterns:
            index, local = pattern.match(index, elements)
            total.include(local)

        return index, total


@dataclasses.dataclass
class PatternRepeat(Pattern):
    """This class represent a pattern that can be matched any number of types. (0 times allowed)"""
    pattern: Pattern

    def match(self, index: int, elements: list[Element]) -> tuple[int, Match]:
        total = MatchList()
        while True:
            try:
                index, local = self.pattern.match(index, elements)

            except MatchError:
                break

            total.include(local)

        return index, total


@dataclasses.dataclass
class PatternOptional(Pattern):
    """This class represent a pattern that can be matched 1 or 0 times."""
    pattern: Pattern

    def match(self, index: int, elements: list[Element]) -> tuple[int, Match]:
        try:
            return self.pattern.match(index, elements)

        except MatchError:
            return index, MatchList()


@dataclasses.dataclass
class AtomPattern(Pattern):
    """This class represent a pattern that validates one item."""
    function: typing.Callable[[Element], bool]
    action: typing.Callable[[Element], None] | None = None

    def match(self, index: int, elements: list[Element]) -> tuple[int, Match]:
        try:
            element = elements[index]
        except IndexError:
            raise MatchError("no elements left to match.")

        if self.function(element):
            return index + 1, MatchUnit(element, self.action)

        else:
            raise MatchError("element type mismatched expected type.")

