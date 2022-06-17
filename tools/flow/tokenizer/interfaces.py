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
    def success(self, chars: str, /, *, add=False, inc=True, clr=True, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def failure(self, chars: str, /, *, add=False, inc=True, clr=True, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def build(self: P, chars: str, build: str, /, *, add=True, inc=True, clr=True, to=ENTRY) -> P:
        """"""
    
    @abc.abstractmethod
    def match(self: P, chars: str, /, *, add=True, inc=True, clr=True, to=NEW) -> P:
        """"""
    
    @abc.abstractmethod
    def repeat(self: P, chars: str, /, *, add=True, inc=True, clr=True, build=None) -> P:
        """"""


@dataclasses.dataclass
class DefaultProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, /, *, add=False, inc=True, clr=True, build='', clear=False) -> None:
        """"""
    
    @abc.abstractmethod
    def failure(self, /, *, add=False, inc=True, clr=True, build='', clear=False) -> None:
        """"""
    
    @abc.abstractmethod
    def build(self: P, build: str, /, *, add=False, inc=False, clr=False, to=ENTRY) -> P:
        """"""
    
    @abc.abstractmethod
    def match(self: P, /, *, add=True, inc=True, clr=True, to=NEW) -> P:
        """"""
    
    @abc.abstractmethod
    def repeat(self: P, /, *, add=True, inc=True, clr=True, build=None) -> P:
        """"""
