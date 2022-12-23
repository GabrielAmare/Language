from __future__ import annotations

import dataclasses
import typing

from .dependencies.bnf import *

__all__ = [
    'Attribute',
    'Namespace',
]


@dataclasses.dataclass
class Attribute:
    name: str
    types: set[str]
    optional: bool
    multiple: bool
    
    def __ior__(self, other: Attribute) -> Attribute:
        assert self.name == other.name
        if self.multiple != other.multiple:
            raise ValueError("Cannot merge two attributes with a different cardinality in a parallel manner.")
        
        return Attribute(
            name=self.name,
            types=self.types.union(other.types),
            optional=self.optional or other.optional,
            multiple=self.multiple
        )
    
    def __or__(self, other: Attribute) -> Attribute:
        assert self.name == other.name
        if self.multiple != other.multiple:
            raise ValueError("Cannot merge two attributes with a different cardinality in a parallel manner.")
        
        return Attribute(
            name=self.name,
            types=self.types.union(other.types),
            optional=self.optional or other.optional,
            multiple=self.multiple
        )


@dataclasses.dataclass
class CardinalityContext:
    factory: ParallelGRToNamespaceFactory
    optional: bool = False
    multiple: bool = False
    
    def __enter__(self):
        if self.optional:
            self.factory.optional_ctx += 1
        if self.multiple:
            self.factory.multiple_ctx += 1
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.optional:
            self.factory.optional_ctx -= 1
        if self.multiple:
            self.factory.multiple_ctx -= 1


@dataclasses.dataclass
class ParallelGRToNamespaceFactory(ParallelGRVisitor):
    optional_ctx: int = 0
    multiple_ctx: int = 0
    
    def context(self, optional: bool = False, multiple: bool = False) -> CardinalityContext:
        return CardinalityContext(self, optional=optional, multiple=multiple)
    
    def _match_char(self, obj: MatchChar) -> Namespace:
        return Namespace()
    
    def _match_as(self, obj: MatchAs) -> Namespace:
        assert self.multiple_ctx == 0
        namespace = Namespace()
        namespace.set(
            name=str(obj.key),
            types={str(obj.type)},
            optional=bool(self.optional_ctx),
            multiple=bool(self.multiple_ctx),
        )
        return namespace
    
    def _match_in(self, obj: MatchIn) -> Namespace:
        assert self.multiple_ctx > 0
        namespace = Namespace()
        namespace.set(
            name=str(obj.key),
            types={str(obj.type)},
            optional=bool(self.optional_ctx),
            multiple=bool(self.multiple_ctx),
        )
        return namespace
    
    def _literal(self, obj: Literal) -> Namespace:
        return Namespace()
    
    def _canonical(self, obj: Canonical) -> Namespace:
        return Namespace()
    
    def _grouping(self, obj: Grouping) -> Namespace:
        return self(obj.rule)
    
    def _repeat0(self, obj: Repeat0) -> Namespace:
        with self.context(optional=True, multiple=True):
            return self(obj.rule)
    
    def _repeat1(self, obj: Repeat1) -> Namespace:
        with self.context(multiple=True):
            return self(obj.rule)
    
    def _optional(self, obj: Optional) -> Namespace:
        with self.context(optional=True):
            namespace = self(obj.rule)
            return namespace
    
    def _enum0(self, obj: Enum0) -> Namespace:
        assert not self(obj.separator).attrs
        with self.context(multiple=True):
            return self(obj.item)
    
    def _enum1(self, obj: Enum1) -> Namespace:
        assert not self(obj.separator).attrs
        with self.context(multiple=True):
            return self(obj.item)
    
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


@dataclasses.dataclass
class Namespace:
    attrs: list[Attribute] = dataclasses.field(default_factory=list)
    
    def has(self, name: str) -> bool:
        return any(attr.name == name for attr in self.attrs)
    
    def get(self, name: str) -> Attribute:
        for attr in self.attrs:
            if attr.name == name:
                return attr
        else:
            raise KeyError(name)
    
    def set(self, name: str, types: set[str], optional: bool, multiple: bool) -> None:
        if self.has(name):
            raise KeyError(f"Duplicate of {name!r}.")
        
        attr = Attribute(
            name=name,
            types=types,
            optional=optional,
            multiple=multiple
        )
        
        self.attrs.append(attr)
    
    def add(self, attr: Attribute) -> None:
        self.attrs.append(attr)
    
    def __iter__(self) -> typing.Iterator[Attribute]:
        return iter(self.attrs)
    
    def copy(self) -> Namespace:
        return Namespace(
            attrs=[dataclasses.replace(attr) for attr in self.attrs]
        )
    
    def optional(self) -> Namespace:
        return Namespace(
            attrs=[dataclasses.replace(attr, optional=True) for attr in self.attrs]
        )
    
    def __iand__(self, other: Namespace) -> Namespace:
        result = self.copy()
        
        for attr in other:
            if result.has(attr.name):
                raise ValueError("Cannot merge two attributes with the same name in a sequential manner.")
            else:
                result.add(attr)
        return result
    
    def __ior__(self, other: Namespace) -> Namespace:
        result = self.copy()
        
        for attr in other:
            if result.has(attr.name):
                a = result.get(attr.name)
                index = result.attrs.index(a)
                result.attrs[index] = a | attr
            else:
                result.add(attr)
        return result
    
    @classmethod
    def from_bnf_rule(cls, rule: ParallelGR) -> Namespace:
        factory = ParallelGRToNamespaceFactory()
        return factory(rule)
    
    # deprecated
    def __contains__(self, name: str) -> bool:
        return self.has(name)
    
    # deprecated
    def __setitem__(self, name: str, attr: Attribute) -> None:
        if self.has(name):
            raise KeyError(f"{name!r} is already defined in the Namespace.")
        
        self.attrs.append(attr)
    
    # deprecated
    def __getitem__(self, name: str) -> Attribute:
        return self.get(name)
    
    def intersection(self, other: Namespace) -> Namespace:
        """Return a Namespace with only the common attributes."""
        result: Namespace = Namespace()
        
        for self_attr in self.attrs:
            if not other.has(self_attr.name):
                continue
            
            other_attr = other.get(self_attr.name)
            
            if self_attr != other_attr:
                continue
            
            result.attrs.append(self_attr)
        
        return result
    
    def union(self, other: Namespace) -> Namespace:
        """Return a merged `Namespace` of `self` and `other`."""
        result: Namespace = Namespace()
        
        for attr in self:
            result[attr.name] = attr
        
        for attr in other:
            if attr.name in result and result[attr.name] != attr:
                raise ValueError
            
            result[attr.name] = attr
        
        return result
    
    def difference(self, other: Namespace) -> Namespace:
        """Return a copy of `self` without the attributes of `other`."""
        result: Namespace = Namespace()
        
        for attr in self:
            if attr.name in other:
                continue
            
            result[attr.name] = attr
        
        return result
