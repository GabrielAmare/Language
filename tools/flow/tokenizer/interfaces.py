import abc
import dataclasses
import typing

from .core import *

__all__ = [
    'DefaultProxyInterface',
    'ProxyInterface',
]

P = typing.TypeVar('P')


@dataclasses.dataclass
class ProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, chars: str, /, *, options=INC + CLR, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def failure(self, chars: str, /, *, options=INC + CLR, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def build(self: P, chars: str, build: str, /, *, options=ADD + INC + CLR, to=ENTRY) -> P:
        """"""
    
    @abc.abstractmethod
    def match(self: P, chars: str, /, *, options=ADD + INC + CLR, to=NEW) -> P:
        """"""
    
    @abc.abstractmethod
    def repeat(self: P, chars: str, /, *, options=ADD + INC + CLR, build=None) -> P:
        """"""


@dataclasses.dataclass
class DefaultProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, /, *, options=INC + CLR, build='') -> None:
        """"""
    
    @abc.abstractmethod
    def failure(self, /, *, options=INC + CLR, build='') -> None:
        """"""
    
    @abc.abstractmethod
    def build(self: P, build: str, /, *, options=0, to=ENTRY) -> P:
        """"""
    
    @abc.abstractmethod
    def match(self: P, /, *, options=ADD + INC + CLR, to=NEW) -> P:
        """"""
    
    @abc.abstractmethod
    def repeat(self: P, /, *, options=ADD + INC + CLR, build=None) -> P:
        """"""
