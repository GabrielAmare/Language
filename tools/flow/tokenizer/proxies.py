from __future__ import annotations

import abc
import dataclasses
import functools
import typing

from .base import *
from .core import *

_I = typing.TypeVar('_I')

__all__ = [
    'ProxyInterface',
    'DefaultProxyInterface',
    'AbstractProxy',
    'DefaultProxy',
    'Proxy',
    'finalize',
]


@dataclasses.dataclass
class ProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, chars: str, /, *, add=False, inc=True, clr=True, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def failure(self, chars: str, /, *, add=False, inc=True, clr=True, build=None) -> None:
        """"""
    
    @abc.abstractmethod
    def build(self: _I, chars: str, build: str, /, *, add=True, inc=True, clr=True, to=ENTRY) -> _I:
        """"""
    
    @abc.abstractmethod
    def match(self: _I, chars: str, /, *, add=True, inc=True, clr=True, to=NEW) -> _I:
        """"""
    
    @abc.abstractmethod
    def repeat(self: _I, chars: str, /, *, add=True, inc=True, clr=True, build=None) -> _I:
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
    def build(self: _I, build: str, /, *, add=False, inc=False, clr=False, to=ENTRY) -> _I:
        """"""
    
    @abc.abstractmethod
    def match(self: _I, /, *, add=True, inc=True, clr=True, to=NEW) -> _I:
        """"""
    
    @abc.abstractmethod
    def repeat(self: _I, /, *, add=True, inc=True, clr=True, build=None) -> _I:
        """"""


@dataclasses.dataclass
class AbstractProxy:
    flow: Flow
    state: int
    entry: int = 0
    
    @property
    def manager(self) -> Manager:
        return self.flow.managers[self.state]
    
    def _state(self, state: int | object) -> int:
        if state is STAY:
            return self.state
        elif state is ENTRY:
            return self.entry
        elif state is NEW:
            return self.flow.new_state()
        elif isinstance(state, int):
            return state
        elif isinstance(state, AbstractProxy):
            return state.state
        else:
            raise ValueError(f"unable to parse {state!r}.")
    
    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()
    
    def _action(self, params: ActionParams, to: int | object) -> Action:
        self.init()
        return Action(params=params, to=self._state(to))


@dataclasses.dataclass
class DefaultProxy(AbstractProxy, DefaultProxyInterface):
    def _on(self, params: ActionParams, to: int | object) -> Proxy:
        action = self._action(params, to)
        self.manager.default = action
        return Proxy(flow=self.flow, state=action.to, entry=self.entry)
    
    def success(self, /, *, add=False, inc=False, clr=True, build=None, clear=False) -> None:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=clear)
        self._on(params, to=VALID)
    
    def failure(self, /, *, add=False, inc=False, clr=True, build=None, clear=False) -> None:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=clear)
        self._on(params, to=ERROR)
    
    def build(self: _I, build: str, /, *, add=False, inc=False, clr=False, to=ENTRY) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=True)
        return self._on(params, to)
    
    def match(self: _I, /, *, add=True, inc=True, clr=True, to=NEW) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build='', clear=False)
        return self._on(params, to=to)
    
    def repeat(self: _I, /, *, add=True, inc=True, clr=True, build=None) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=bool(build))
        return self._on(params, to=STAY)


@dataclasses.dataclass
class Proxy(AbstractProxy, ProxyInterface):
    @functools.cached_property
    def default(self):
        return DefaultProxy(flow=self.flow, state=self.state, entry=self.entry)
    
    def proxy(self, to=NEW, entry=ENTRY) -> Proxy:
        return Proxy(flow=self.flow, state=self._state(to), entry=self._state(entry))
    
    def add_handler(self, new_handler: Handler) -> None:
        add = True
        for handler in self.flow.managers[self.state].handlers:
            if handler.shadows(new_handler):
                match new_handler:
                    case Handler(
                        condition=handler.condition,
                        action=Action(
                            params=handler.action.params,
                            to=to
                        )
                    ):
                        if to == handler.action.to:
                            add = False
                            continue
                        
                        if new_handler.action.to not in self.flow.managers:
                            add = False
                            new_handler.action.to = handler.action.to
                            continue
                        
                        raise ValueError(f"[2] {handler} is shadowing {new_handler}")
                    
                    case _:
                        raise ValueError(f"[1] {handler} is shadowing {new_handler}")
        if add:
            self.flow.managers[self.state].handlers.append(new_handler)
    
    def new(self) -> int:
        return self.flow.new_state()
    
    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()
    
    def _action(self, params: ActionParams, to: int | object) -> Action:
        self.init()
        to = self._state(to)
        return Action(params=params, to=to)
    
    def _on(self, chars: str, params: ActionParams, to: int | object) -> Proxy:
        action = self._action(params, to)
        self.add_handler(Handler(Condition(chars), action))
        return Proxy(flow=self.flow, state=action.to, entry=self.entry)
    
    def success(self, chars: str, /, *, add=False, inc=False, clr=True, build='', clear=False) -> None:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=clear)
        self._on(chars, params, to=VALID)
    
    def failure(self, chars: str, /, *, add=False, inc=False, clr=True, build='', clear=False) -> None:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=clear)
        self._on(chars, params, to=ERROR)
    
    def build(self, chars: str, build: str, /, *, add=True, inc=True, clr=True, to=ENTRY) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=True)
        return self._on(chars, params, to=to)
    
    def match(self, chars: str, /, *, add=True, inc=True, clr=True, to=NEW) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build='', clear=False)
        return self._on(chars, params, to=to)
    
    def repeat(self, chars: str, /, *, add=True, inc=True, clr=True, build=None) -> Proxy:
        params = ActionParams(add=add, inc=inc, clr=clr, build=build, clear=bool(build))
        return self._on(chars, params, to=STAY)
    
    ####################################################################################################################
    # COMPOUNDS
    ####################################################################################################################
    
    def optional(self, chars: str, /, *, build=None, to=NEW):
        if build is None:
            self.match(chars, add=True, inc=True, clr=True, to=to)
            return self.default.match(add=False, inc=False, to=to)
        else:
            self.build(chars, build, add=True, inc=True, clr=True, to=to)
            return self.default.build(build, add=False, inc=False, to=to)
    
    def sequence(self, *seq_chars: str, add=True, inc=True, clr=True, build=None, to=None):
        cur = self
        
        for chars in seq_chars[:-1]:
            cur = cur.match(chars, add=add, inc=inc, clr=clr)
        
        if build is None:
            if to is None:
                to = NEW
            return cur.match(seq_chars[-1], add=add, inc=inc, clr=clr, to=to)
        else:
            if to is None:
                to = ENTRY
            return cur.build(seq_chars[-1], build, add=add, inc=inc, clr=clr, to=to)
    
    def repeat_plus(self, chars: str, /, *, add=True, inc=True, clr=True, build=None) -> Proxy:
        return self.match(chars).repeat(chars, add=add, inc=inc, clr=clr, build=build)
    
    def build_bloc(self, at_chars: str, to_chars: str, build: str, to=ENTRY) -> Proxy:
        return self.match(at_chars).default.repeat().build(to_chars, build, to=to)


def finalize(flow: Flow) -> None:
    # VALID
    Proxy(flow, 0).success(EOT)
    
    # ERROR
    err_1 = Proxy(flow, flow.new_state())
    err_1.failure(EOT, build='~ERROR')
    
    for manager in flow.managers.values():
        if manager.default is None:
            manager.default = Action(ActionParams(add=True, inc=True, clr=True, build='', clear=False), to=err_1.state)
        
        if not manager.verify(EOT):
            condition = Condition(EOT)
            if manager.default and manager.default.params.clear:
                params = ActionParams(add=False, inc=False, clr=True, build=manager.default.params.build, clear=False)
                action = Action(params, to=VALID)
            else:
                params = ActionParams(add=False, inc=False, clr=True, build='~ERROR', clear=False)
                action = Action(params, to=ERROR)
            
            handler = Handler(condition, action)
            manager.handlers.append(handler)
