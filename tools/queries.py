from __future__ import annotations

import abc
import dataclasses
import typing

E = typing.TypeVar('E')
F = typing.TypeVar('F')

__all__ = [
    'Query',
    'QueryList',
    'QueryFilter',
    'QueryMap',
    'Item'
]


def _isinstance(cls: type):
    return lambda obj: isinstance(obj, cls)


def _getattr(name: str):
    return lambda obj: getattr(obj, name)


def _equals(second: object):
    return lambda first: first == second


@dataclasses.dataclass
class Query(typing.Generic[E], abc.ABC):
    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator[E]:
        """"""

    def filter(self, function: typing.Callable[[E], bool]) -> QueryFilter[E]:
        return QueryFilter(query=self, function=function)

    def map(self, function: typing.Callable[[E], F]) -> QueryMap[E, F]:
        return QueryMap(query=self, function=function)

    def getattr(self, name: str) -> QueryMap:
        return self.map(_getattr(name))

    def instanceof(self, cls: typing.Type[F]) -> QueryFilter[F]:
        return self.filter(_isinstance(cls))

    def as_list(self) -> typing.List[E]:
        return list(self)

    def as_tuple(self) -> typing.Tuple[E, ...]:
        return tuple(self)

    def as_set(self) -> typing.Set[E]:
        return set(self)

    def first(self, safe: bool = True) -> typing.Optional[E]:
        for item in self:
            return item
        else:
            if safe:
                return None
            else:
                raise KeyError()

    def last(self) -> typing.Optional[E]:
        item = None
        for item in self:
            continue
        return item

    def __bool__(self):
        return len(self) > 0


@dataclasses.dataclass
class QueryList(typing.Generic[E], Query[E]):
    items: typing.List[E] = dataclasses.field(default_factory=list)

    def __contains__(self, item: E) -> bool:
        return item in self.items

    def __iter__(self) -> typing.Iterator[E]:
        yield from self.items

    def __len__(self):
        return len(self.items)

    def append(self, item: E) -> None:
        self.items.append(item)

    def extend(self, items: typing.Iterator[E]) -> None:
        self.items.extend(items)

    def remove(self, item: E) -> None:
        self.items.remove(item)

    def insert(self, index: int, item: E) -> None:
        self.items.insert(index, item)

    def pop(self, index: int) -> E:
        return self.items.pop(index)

    def __getitem__(self, index: int) -> E:
        return self.items[index]

    def __setitem__(self, index: int, item: E) -> None:
        self.items[index] = item

    def __delitem__(self, index: int) -> None:
        del self.items[index]


@dataclasses.dataclass
class QueryFilter(typing.Generic[E], Query[E]):
    query: Query[E]
    function: typing.Callable[[E], bool]

    def __iter__(self) -> typing.Iterator[E]:
        yield from filter(self.function, self.query)

    def __len__(self):
        length = 0
        for _ in self:
            length += 1
        return length


@dataclasses.dataclass
class QueryMap(typing.Generic[E, F], Query[F]):
    query: Query[E]
    function: typing.Callable[[E], F]

    def __iter__(self) -> typing.Iterator[F]:
        yield from map(self.function, self.query)

    def __len__(self):
        length = 0
        for _ in self:
            length += 1
        return length


@dataclasses.dataclass
class Item(abc.ABC):
    @classmethod
    def getattr(cls, name) -> Func:
        return Func(function=_getattr(name))

    @classmethod
    def equals(cls, value) -> Func:
        return Func(function=_equals(value))


@dataclasses.dataclass
class _Func(abc.ABC):
    def getattr(self, name) -> Then:
        return Then(first=self, second=Item.getattr(name))

    def equals(self, value) -> Then:
        return Then(first=self, second=Item.equals(value))

    @abc.abstractmethod
    def __call__(self, item):
        """"""


@dataclasses.dataclass
class Then(_Func):
    first: _Func
    second: _Func

    def __call__(self, item):
        return self.second(self.first(item))


@dataclasses.dataclass
class Func(_Func):
    function: callable

    def __call__(self, item):
        return self.function(item)
