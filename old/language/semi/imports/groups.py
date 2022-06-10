import operator
import typing

from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__method__
def union(self: Group, *others: Group) -> Group:
    """Return the union of `self` and `others`."""
    l_items: frozenset[str] = self.to_frozenset()
    l_inv: bool = Inverted.to_bool(self.inverted)

    for other in others:
        r_items: frozenset[str] = other.to_frozenset()
        r_inv: bool = Inverted.to_bool(other.inverted)

        if r_inv:
            if l_inv:
                l_items = r_items.difference(l_items)
            else:
                l_items = r_items.intersection(l_items)
        else:
            if l_inv:
                l_items = l_items.union(r_items)
            else:
                l_items = l_items.difference(r_items)

        l_inv = l_inv or r_inv

    items: String = String.from_str(''.join(l_items))
    inv: typing.Optional[Inverted] = Inverted.from_bool(l_inv)

    return Group(items=items, inverted=inv)


@__method__
def intersection(self: Group, *others: Group) -> Group:
    """Return the intersection of `self` and `others`."""
    l_items: frozenset[str] = self.to_frozenset()
    l_inv: bool = Inverted.to_bool(self.inverted)

    for other in others:
        r_items: frozenset[str] = other.to_frozenset()
        r_inv: bool = Inverted.to_bool(other.inverted)

        if r_inv:
            if l_inv:
                l_items = r_items.difference(l_items)
            else:
                l_items = r_items.union(l_items)
        else:
            if l_inv:
                l_items = l_items.intersection(r_items)
            else:
                l_items = l_items.difference(r_items)

        l_inv = l_inv and r_inv

    items: String = String.from_str(''.join(l_items))
    inv: typing.Optional[Inverted] = Inverted.from_bool(l_inv)

    return Group(items=items, inverted=inv)


@__property__
def complement(self: Group) -> Group:
    """Return `self` complement."""
    inverted = Inverted.from_bool(not Inverted.to_bool(self.inverted))
    return Group(items=self.items, inverted=inverted)


@__method__
def __contains__(self: Group, item: str) -> bool:
    """Return True when item is in `self`."""
    return operator.xor(item in self.to_frozenset(), Inverted.to_bool(self.inverted))


@__property__
def is_inverted(self: Group) -> bool:
    return Inverted.to_bool(self.inverted)
