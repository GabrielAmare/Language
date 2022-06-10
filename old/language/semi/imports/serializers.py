import typing

from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__class_method__
def from_str(cls: Variable.__class__, value: str) -> Variable:
    return cls(content=value)


@__class_method__
def from_str(cls: String.__class__, value: str) -> String:
    return cls(content=repr(value))


@__class_method__
def from_int(cls: Integer.__class__, value: int) -> typing.Optional[Integer]:
    if value == 0:
        return None

    return cls(content=repr(value))


@__class_method__
def from_bool(cls: Inverted.__class__, value: bool) -> typing.Optional[Inverted]:
    return cls() if value else None


@__class_method__
def from_frozenset(cls: Group.__class__, items: typing.FrozenSet[str], inverted: bool = False) -> Group:
    return cls(
        items=String.from_str(''.join(sorted(items))),
        inverted=Inverted.from_bool(inverted)
    )


@__method__
def to_str(self: Variable) -> str:
    return self.content


@__method__
def to_str(self: String) -> str:
    return eval(self.content)


@__method__
def to_int(self: Integer) -> int:
    if self is None:
        return 0

    return int(self.content)


@__method__
def to_bool(self: Inverted) -> bool:
    return isinstance(self, Inverted)


@__method__
def to_frozenset(self: Group) -> typing.FrozenSet[str]:
    return frozenset(self.items.to_str())


@__method__
def as_grouping(self: ParallelGR) -> GroupingGR:
    """Transform the given rule to a GroupingGR instance."""
    if isinstance(self, GroupingGR):
        return self

    elif isinstance(self, (Parallel, Sequence, Repeat)):
        return Grouping(self)

    else:
        raise NotImplementedError


@__method__
def as_repeat(self: ParallelGR, mn: typing.Optional[Integer], mx: typing.Optional[Integer]) -> RepeatGR:
    """Transform the given rule to a RepeatGR instance."""
    rule = self.as_grouping()
    v_mn = Integer.to_int(mn)
    v_mx = Integer.to_int(mx)
    if v_mx == 0 or v_mn <= v_mx:
        return Repeat(rule=rule, mn=mn, mx=mx)
    else:
        return Error()
