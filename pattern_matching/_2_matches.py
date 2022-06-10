import abc
import dataclasses
import typing

from ._1_elements import Element, Context

__all__ = [
    'MatchError',
    'Match',
    'MatchUnit',
    'MatchList',
    'flatten',
]


class MatchError(Exception):
    ...


class Match(abc.ABC):
    """This class represent a pattern match."""

    @abc.abstractmethod
    def apply(self, context: Context) -> None:
        """"""


@dataclasses.dataclass
class MatchUnit(Match):
    element: Element
    action: typing.Callable[[Context, Element], None] | None = None

    def apply(self, context: Context) -> None:
        if self.action:
            self.action(context, self.element)


@dataclasses.dataclass
class MatchList(Match):
    sub_matches: list[Match] = dataclasses.field(default_factory=list)

    def __iter__(self) -> typing.Iterator[Match]:
        return iter(self.sub_matches)

    def include(self, match: Match) -> None:
        self.sub_matches.append(match)

    def apply(self, context: Context) -> None:
        for sub_match in self.sub_matches:
            sub_match.apply(context)


def _flatten(__match: Match) -> typing.Iterator[MatchUnit]:
    if isinstance(__match, MatchList):
        for item in __match.sub_matches:
            yield from _flatten(item)

    elif isinstance(__match, MatchUnit):
        yield __match

    else:
        raise NotImplementedError


def flatten(__match: Match) -> Match:
    matches = list(_flatten(__match))

    if len(matches) == 1:
        return matches[0]

    return MatchList(matches)
