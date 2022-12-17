from __future__ import annotations

import dataclasses
import typing

from language.base.bnf.v0_0_1 import *

__all__ = [
    'Attribute',
    'Namespace',
]


@dataclasses.dataclass
class Attribute:
    types: set[str]
    optional: bool
    multiple: bool
    
    def __ior__(self, other: Attribute) -> Attribute:
        if self.multiple != other.multiple:
            raise ValueError("Cannot merge two attributes with a different cardinality in a parallel manner.")
        
        return Attribute(
            types=self.types.union(other.types),
            optional=self.optional or other.optional,
            multiple=self.multiple
        )


@dataclasses.dataclass
class Namespace:
    # attributes: dict[str, Attribute] = dataclasses.field(default_factory=dict)
    names: list[str] = dataclasses.field(default_factory=list)
    attrs: list[Attribute] = dataclasses.field(default_factory=list)
    
    def items(self) -> typing.Iterator[tuple[str, Attribute]]:
        return zip(self.names, self.attrs)
    
    def optional(self) -> Namespace:
        return Namespace(
            names=self.names[:],
            attrs=[dataclasses.replace(attr, optional=True) for attr in self.attrs]
        )
    
    def __iand__(self, other: Namespace) -> Namespace:
        names = self.names[:]
        attrs = self.attrs[:]
        for name, attr in other.items():
            if name in names:
                raise ValueError("Cannot merge two attributes with the same name in a sequential manner.")
            else:
                names.append(name)
                attrs.append(attr)
        return Namespace(names, attrs)
    
    def __ior__(self, other: Namespace) -> Namespace:
        names = self.names[:]
        attrs = self.attrs[:]
        for name, attr in other.items():
            if name in names:
                index = names.index(name)
                attrs[index] |= attr
            else:
                names.append(name)
                attrs.append(attr)
        return Namespace(names, attrs)
    
    class NamespaceBuilderVisitor(ParallelGRVisitor):
        def _match_char(self, obj: MatchChar) -> Namespace:
            return Namespace()
        
        def _match_as(self, obj: MatchAs) -> Namespace:
            return Namespace(names=[str(obj.key)],
                             attrs=[Attribute(types={str(obj.type)}, optional=False, multiple=False)])
        
        def _match_in(self, obj: MatchIn) -> Namespace:
            return Namespace(names=[str(obj.key)],
                             attrs=[Attribute(types={str(obj.type)}, optional=False, multiple=True)])
        
        def _literal(self, obj: Literal) -> Namespace:
            return Namespace()
        
        def _canonical(self, obj: Canonical) -> Namespace:
            return Namespace()
        
        def _grouping(self, obj: Grouping) -> Namespace:
            return self(obj.rule)
        
        def _repeat0(self, obj: Repeat0) -> Namespace:
            namespace = self(obj.rule)
            assert all(attr.multiple for attr in namespace.attrs)
            return namespace.optional()
        
        def _repeat1(self, obj: Repeat1) -> Namespace:
            namespace = self(obj.rule)
            assert all(attr.multiple for attr in namespace.attrs)
            return namespace
        
        def _optional(self, obj: Optional) -> Namespace:
            namespace = self(obj.rule)
            return namespace.optional()
        
        def _enum0(self, obj: Enum0) -> Namespace:
            assert not self(obj.separator).attrs
            namespace = self(obj.item)
            assert all(attr.multiple for attr in namespace.attrs)
            return namespace
        
        def _enum1(self, obj: Enum1) -> Namespace:
            assert not self(obj.separator).attrs
            namespace = self(obj.item)
            assert all(attr.multiple for attr in namespace.attrs)
            return namespace
        
        def _sequence(self, obj: Sequence) -> Namespace:
            namespace = Namespace()
            for rule in obj.rules:
                namespace &= self(rule)
            return namespace
        
        def _parallel(self, obj: Parallel) -> Namespace:
            namespace = Namespace()
            for rule in obj.rules:
                namespace |= self(rule)
            return namespace
    
    from_bnf_rule = staticmethod(NamespaceBuilderVisitor())
    
    def __contains__(self, name: str) -> bool:
        return name in self.names
    
    def __setitem__(self, name: str, attr: Attribute) -> None:
        if name in self.names:
            raise KeyError(f"{name!r} is already defined in the Namespace.")
        
        self.names.append(name)
        self.attrs.append(attr)
    
    def __getitem__(self, name: str) -> Attribute:
        try:
            index = self.names.index(name)
        except IndexError:
            raise KeyError(f"{name!r} is not defined in the Namespace.")
        
        return self.attrs[index]
    
    def intersection(self, other: Namespace) -> Namespace:
        """Return a Namespace with only the common attributes."""
        result: Namespace = Namespace()
        
        for name in self.names:
            if name not in other:
                continue
            
            self_attr = self[name]
            other_attr = other[name]
            
            if self_attr != other_attr:
                continue
            
            result[name] = self_attr
        
        return result
    
    def union(self, other: Namespace) -> Namespace:
        """Return a merged `Namespace` of `self` and `other`."""
        result: Namespace = Namespace()
        
        for name, attr in self.items():
            result[name] = attr
        
        for name, attr in other.items():
            if name in result and result[name] != attr:
                raise ValueError
            
            result[name] = attr
        
        return result
    
    def difference(self, other: Namespace) -> Namespace:
        """Return a copy of `self` without the attributes of `other`."""
        result: Namespace = Namespace()
        
        for name, attr in self.items():
            if name in other:
                continue
            
            result[name] = attr
        
        return result
