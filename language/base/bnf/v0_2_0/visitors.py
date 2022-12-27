from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .models import *

__all__ = [
    'BuildGRVisitor',
    'ParallelGRVisitor',
]
_E = TypeVar('_E')


class ParallelGRVisitor(Generic[_E], ABC):
    def __call__(self, obj: ParallelGR) -> _E:
        if isinstance(obj, Parallel):
            return self._parallel(obj)
        elif isinstance(obj, Sequence):
            return self._sequence(obj)
        elif isinstance(obj, Enum0):
            return self._enum0(obj)
        elif isinstance(obj, Enum1):
            return self._enum1(obj)
        elif isinstance(obj, Optional):
            return self._optional(obj)
        elif isinstance(obj, Repeat0):
            return self._repeat0(obj)
        elif isinstance(obj, Repeat1):
            return self._repeat1(obj)
        elif isinstance(obj, Grouping):
            return self._grouping(obj)
        elif isinstance(obj, Canonical):
            return self._canonical(obj)
        elif isinstance(obj, Literal):
            return self._literal(obj)
        elif isinstance(obj, LiteralIf):
            return self._literal_if(obj)
        elif isinstance(obj, Match):
            return self._match(obj)
        elif isinstance(obj, Store):
            return self._store(obj)
        else:
            raise NotImplementedError
    
    @abstractmethod
    def _parallel(self, obj: Parallel) -> _E:
        pass
    
    @abstractmethod
    def _sequence(self, obj: Sequence) -> _E:
        pass
    
    @abstractmethod
    def _enum0(self, obj: Enum0) -> _E:
        pass
    
    @abstractmethod
    def _enum1(self, obj: Enum1) -> _E:
        pass
    
    @abstractmethod
    def _optional(self, obj: Optional) -> _E:
        pass
    
    @abstractmethod
    def _repeat0(self, obj: Repeat0) -> _E:
        pass
    
    @abstractmethod
    def _repeat1(self, obj: Repeat1) -> _E:
        pass
    
    @abstractmethod
    def _grouping(self, obj: Grouping) -> _E:
        pass
    
    @abstractmethod
    def _canonical(self, obj: Canonical) -> _E:
        pass
    
    @abstractmethod
    def _literal(self, obj: Literal) -> _E:
        pass
    
    @abstractmethod
    def _literal_if(self, obj: LiteralIf) -> _E:
        pass
    
    @abstractmethod
    def _match(self, obj: Match) -> _E:
        pass
    
    @abstractmethod
    def _store(self, obj: Store) -> _E:
        pass


class BuildGRVisitor(Generic[_E], ABC):
    def __call__(self, obj: BuildGR) -> _E:
        if isinstance(obj, BuildGroup):
            return self._build_group(obj)
        elif isinstance(obj, BuildLemma):
            return self._build_lemma(obj)
        elif isinstance(obj, BuildToken):
            return self._build_token(obj)
        else:
            raise NotImplementedError
    
    @abstractmethod
    def _build_group(self, obj: BuildGroup) -> _E:
        pass
    
    @abstractmethod
    def _build_lemma(self, obj: BuildLemma) -> _E:
        pass
    
    @abstractmethod
    def _build_token(self, obj: BuildToken) -> _E:
        pass
