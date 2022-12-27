from __future__ import annotations

import dataclasses
import typing

from .cardinality_tracker import Cardinality
from .casters import Caster
from .dependencies.bnf import *

__all__ = [
    'Attribute',
    'Namespace',
]

_DEFAULT = bool | str | int | float | None


@dataclasses.dataclass
class Attribute:
    name: str
    types: set[str]
    optional: bool
    multiple: bool
    default: _DEFAULT = None
    
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
        if self.default != other.default and self.default is not None:
            raise ValueError("Incompatible default values between the two attributes.")
        
        return Attribute(
            name=self.name,
            types=self.types.union(other.types),
            optional=self.optional or other.optional,
            multiple=self.multiple,
            default=self.default if self.default is not None else other.default
        )
    
    def apply_casters(self, casters: dict[str, Caster]) -> Attribute:
        types: set[str] = set()
        default: _DEFAULT = self.default
        
        for name in self.types:
            if name not in casters:
                types.add(name)
                continue
            
            caster = casters[name]
            types.add(caster.name)
            
            if caster.default is None:
                continue
            
            if default is not None:
                raise NotImplementedError("Cannot have multiple default values for an attribute.")
            
            default = caster.default
        
        return dataclasses.replace(self, types=types, default=default)


@dataclasses.dataclass
class ParallelGRToNamespaceFactory(ParallelGRVisitor):
    cardinality: Cardinality = dataclasses.field(default_factory=Cardinality)
    
    def _match(self, obj: Match) -> Namespace:
        return Namespace()
    
    def _store(self, obj: Store) -> Namespace:
        namespace = Namespace()
        namespace.set(
            name=str(obj.key),
            types={str(obj.type)},
            optional=bool(self.cardinality.optional),
            multiple=bool(self.cardinality.multiple),
        )
        return namespace
    
    def _literal_if(self, obj: LiteralIf) -> Namespace:
        with self.cardinality(optional=True):
            assert not self.cardinality.multiple
            namespace = Namespace()
            namespace.set(
                name=str(obj.key),
                types={'bool'},
                optional=bool(self.cardinality.optional),
                multiple=bool(self.cardinality.multiple),
                default=False,
            )
            return namespace
    
    def _literal(self, obj: Literal) -> Namespace:
        return Namespace()
    
    def _canonical(self, obj: Canonical) -> Namespace:
        return Namespace()
    
    def _grouping(self, obj: Grouping) -> Namespace:
        return self(obj.rule)
    
    def _repeat0(self, obj: Repeat0) -> Namespace:
        with self.cardinality(optional=True, multiple=True):
            return self(obj.rule)
    
    def _repeat1(self, obj: Repeat1) -> Namespace:
        with self.cardinality(multiple=True):
            return self(obj.rule)
    
    def _optional(self, obj: Optional) -> Namespace:
        with self.cardinality(optional=True):
            namespace = self(obj.rule)
            return namespace
    
    def _enum0(self, obj: Enum0) -> Namespace:
        assert not self(obj.separator).attrs
        with self.cardinality(multiple=True):
            return self(obj.item)
    
    def _enum1(self, obj: Enum1) -> Namespace:
        assert not self(obj.separator).attrs
        with self.cardinality(multiple=True):
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
    
    def set(self, name: str, types: set[str], optional: bool, multiple: bool, default: _DEFAULT = None) -> None:
        if self.has(name):
            raise KeyError(f"Duplicate of {name!r}.")
        
        attr = Attribute(
            name=name,
            types=types,
            optional=optional,
            multiple=multiple,
            default=default
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
    
    def apply_casters(self, casters: dict[str, Caster]) -> Namespace:
        return dataclasses.replace(self, attrs=[attr.apply_casters(casters) for attr in self.attrs])
