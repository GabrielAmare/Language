from __future__ import annotations

import abc
import dataclasses
import functools
import typing

from .base import *
from .core import *

_I = typing.TypeVar('_I')

__all__ = [
    'ManagerProxyInterface',
    'ManagerDefaultProxyInterface',
    'AbstractManagerProxy',
    'ManagerDefaultProxy',
    'ManagerProxy',
    'finalize',
]


@dataclasses.dataclass
class ManagerProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, chars: str, /, *, add=False, use=True, clr=True, build=None) -> None:
        """"""

    @abc.abstractmethod
    def failure(self, chars: str, /, *, add=False, use=True, clr=True, build=None) -> None:
        """"""

    @abc.abstractmethod
    def build(self: _I, chars: str, build: str, /, *, add=True, use=True, clr=True, to=ENTRY) -> _I:
        """"""

    @abc.abstractmethod
    def match(self: _I, chars: str, /, *, add=True, use=True, clr=True, to=NEW) -> _I:
        """"""

    @abc.abstractmethod
    def repeat(self: _I, chars: str, /, *, add=True, use=True, clr=True, build=None) -> _I:
        """"""


@dataclasses.dataclass
class ManagerDefaultProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, /, *, add=False, use=True, clr=True, build='', clear=False) -> None:
        """"""

    @abc.abstractmethod
    def failure(self, /, *, add=False, use=True, clr=True, build='', clear=False) -> None:
        """"""

    @abc.abstractmethod
    def build(self: _I, build: str, /, *, add=False, use=False, to=ENTRY) -> _I:
        """"""

    @abc.abstractmethod
    def match(self: _I, /, *, add=True, use=True, clr=True, to=NEW) -> _I:
        """"""

    @abc.abstractmethod
    def repeat(self: _I, /, *, add=True, use=True, clr=True, build=None) -> _I:
        """"""


@dataclasses.dataclass
class AbstractManagerProxy:
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
        elif isinstance(state, AbstractManagerProxy):
            return state.state
        else:
            raise ValueError(f"unable to parse {state!r}.")

    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()

    def _action(self, add: bool, use: bool, clr: bool, build: str, clear: bool, to: int | object) -> Action:
        self.init()
        return Action(add=add, use=use, clr=clr, build=build, clear=clear, to=self._state(to))


@dataclasses.dataclass
class ManagerDefaultProxy(AbstractManagerProxy, ManagerDefaultProxyInterface):
    def _on(self, /, *, add: bool, use: bool, clr: bool, build: str, clear: bool, to: int | object) -> ManagerProxy:
        action = self._action(add, use, clr, build, clear, to)
        self.manager.default = action
        return ManagerProxy(flow=self.flow, state=action.to, entry=self.entry)

    def success(self, /, *, add=False, use=True, clr=True, build=None, clear=False) -> None:
        pass

    def failure(self, /, *, add=False, use=True, clr=True, build=None, clear=False) -> None:
        pass

    def build(self: _I, build: str, /, *, add=False, use=False, clr=False, to=ENTRY) -> ManagerProxy:
        return self._on(add=add, use=use, clr=clr, to=to, build=build, clear=bool(build))

    def match(self: _I, /, *, add=True, use=True, clr=True, to=NEW) -> ManagerProxy:
        return self._on(add=add, use=use, clr=clr, to=to, build='', clear=False)

    def repeat(self: _I, /, *, add=True, use=True, clr=True, build=None) -> ManagerProxy:
        return self._on(add=add, use=use, clr=clr, build=build, clear=bool(build), to=STAY)


@dataclasses.dataclass
class ManagerProxy(AbstractManagerProxy, ManagerProxyInterface):
    @functools.cached_property
    def default(self):
        return ManagerDefaultProxy(flow=self.flow, state=self.state, entry=self.entry)

    def proxy(self, to=NEW, entry=ENTRY) -> ManagerProxy:
        return ManagerProxy(flow=self.flow, state=self._state(to), entry=self._state(entry))

    def new(self) -> int:
        return self.flow.new_state()

    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()

    def _action(self, add: bool, use: bool, clr: bool, build: str, clear: bool, to: int | object) -> Action:
        self.init()
        to = self._state(to)
        return Action(add=add, use=use, clr=clr, build=build, clear=clear, to=to)

    def _on(self, chars: str, /, *,
            add: bool, use: bool, clr: bool,
            build: str, clear: bool,
            to: int | object) -> ManagerProxy:
        action = self._action(add, use, clr, build, clear, to)
        self.flow.managers[self.state].handlers.append(Handler(Condition(chars), action))
        return ManagerProxy(flow=self.flow, state=action.to, entry=self.entry)

    def success(self, chars: str, /, *, add=False, use=False, clr=True, build='', clear=False) -> None:
        self._on(chars, add=add, use=use, clr=clr, build=build, clear=clear, to=VALID)

    def failure(self, chars: str, /, *, add=False, use=False, clr=True, build='', clear=False) -> None:
        self._on(chars, add=add, use=use, clr=clr, build=build, clear=clear, to=ERROR)

    def build(self, chars: str, build: str, /, *, add=True, use=True, clr=True, to=ENTRY) -> ManagerProxy:
        return self._on(chars, add=add, use=use, clr=clr, build=build, clear=bool(build), to=to)

    def match(self, chars: str, /, *, add=True, use=True, clr=True, to=NEW) -> ManagerProxy:
        return self._on(chars, add=add, use=use, clr=clr, to=to, build='', clear=False)

    def repeat(self, chars: str, /, *, add=True, use=True, clr=True, build=None) -> ManagerProxy:
        return self._on(chars, add=add, use=use, clr=clr, build=build, clear=bool(build), to=STAY)

    ####################################################################################################################
    # COMPOUNDS
    ####################################################################################################################

    def optional(self, chars: str, /, *, build=None, to=NEW):
        if build is None:
            self.match(chars, add=True, use=True, clr=True, to=to)
            return self.default.match(add=False, use=False, to=to)
        else:
            self.build(chars, build, add=True, use=True, clr=True, to=to)
            return self.default.build(build, add=False, use=False, to=to)

    def sequence(self, *seq_chars: str, add=True, use=True, clr=True, build=None, to=None):
        cur = self

        for chars in seq_chars[:-1]:
            cur = cur.match(chars, add=add, use=use, clr=clr)

        if build is None:
            if to is None:
                to = NEW
            return cur.match(seq_chars[-1], add=add, use=use, clr=clr, to=to)
        else:
            if to is None:
                to = ENTRY
            return cur.build(seq_chars[-1], build, add=add, use=use, clr=clr, to=to)

    def repeat_plus(self, chars: str, /, *, add=True, use=True, clr=True, build=None) -> ManagerProxy:
        return self.match(chars).repeat(chars, add=add, use=use, clr=clr, build=build)

    def build_bloc(self, at_chars: str, to_chars: str, build: str, to=ENTRY) -> ManagerProxy:
        return self.match(at_chars).default.repeat().build(to_chars, build, to=to)


def finalize(flow: Flow) -> None:
    # VALID
    ManagerProxy(flow, 0).success(EOT)

    # ERROR
    err_1 = ManagerProxy(flow, flow.new_state())
    err_1.failure(EOT, build='~ERROR')

    for manager in flow.managers.values():
        if manager.default is None:
            manager.default = Action(add=True, use=True, clr=True, to=err_1.state, build='', clear=False)

        # if not manager.verify(self.eot()):
        #     condition = Condition(self.eot())
        #     action = Action(add=False, use=True, clr=True, _build=manager.default._build, to=VALID)
        #     handler = Handler(condition, action)
        #     manager.handlers.append(handler)
