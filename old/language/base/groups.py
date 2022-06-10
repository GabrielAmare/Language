import dataclasses
import operator
import typing

__all__ = [
    'Charset'
]


@dataclasses.dataclass
class Charset:
    items: frozenset[str] = dataclasses.field(default_factory=frozenset)
    inverted: bool = False

    def __contains__(self, item: str) -> bool:
        return operator.xor(item in self.items, self.inverted)

    def union(self, *others: 'Charset') -> 'Charset':
        """
            Return the union of Charset objects.
            >>> x = Charset(frozenset('xt'))
            >>> y = Charset(frozenset('yt'))
            >>> z = Charset(frozenset('zt'))
            >>> u = Charset.union(x, y, z)
            >>> assert u == Charset(frozenset('xyzt'))
        """
        items, inverted = self.items, self.inverted
        for other in others:
            if other.inverted:
                items = (frozenset.intersection if inverted else frozenset.difference)(other.items, items)
            else:
                items = (frozenset.difference if inverted else frozenset.union)(items, other.items)
            inverted = inverted or other.inverted
        return Charset(items=items, inverted=inverted)

    def intersection(self, *others: 'Charset') -> 'Charset':
        """
            Return the intersection of Charset objects.
            >>> x = Charset(frozenset('xt'))
            >>> y = Charset(frozenset('yt'))
            >>> z = Charset(frozenset('zt'))
            >>> i = Charset.intersection(x, y, z)
            >>> assert i == Charset(frozenset('t'))
        """
        items, inverted = self.items, self.inverted
        for other in others:
            if other.inverted:
                items = (frozenset.union if inverted else frozenset.difference)(other.items, items)
            else:
                items = (frozenset.difference if inverted else frozenset.intersection)(items, other.items)
            inverted = inverted and other.inverted
        return Charset(items=items, inverted=inverted)

    @property
    def complement(self) -> 'Charset':
        """
            Return `self` complement.
            >>> x = Charset(frozenset('x'))
            >>> xb = x.complement
            >>> assert xb == Charset(frozenset('x'), True)
        """
        return dataclasses.replace(self, inverted=not self.inverted)
