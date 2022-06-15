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
    def success(self, chars: str, /, *, do=EXCLUDE, build=None) -> None:
        """"""

    @abc.abstractmethod
    def failure(self, chars: str, /, *, do=EXCLUDE, build=None) -> None:
        """"""

    @abc.abstractmethod
    def build(self: _I, chars: str, build: str, /, *, do=INCLUDE, to=ENTRY) -> _I:
        """"""

    @abc.abstractmethod
    def match(self: _I, chars: str, /, *, do=INCLUDE, to=NEW) -> _I:
        """"""

    @abc.abstractmethod
    def repeat(self: _I, chars: str, /, *, do=INCLUDE, build=None) -> _I:
        """"""


@dataclasses.dataclass
class ManagerDefaultProxyInterface(abc.ABC):
    @abc.abstractmethod
    def success(self, /, *, do=EXCLUDE, build=None) -> None:
        """"""

    @abc.abstractmethod
    def failure(self, /, *, do=EXCLUDE, build=None) -> None:
        """"""

    @abc.abstractmethod
    def build(self: _I, build: str, /, *, do=NOTHING, to=ENTRY) -> _I:
        """"""

    @abc.abstractmethod
    def match(self: _I, /, *, do=INCLUDE, to=NEW) -> _I:
        """"""

    @abc.abstractmethod
    def repeat(self: _I, /, *, do=INCLUDE, build=None) -> _I:
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

    def _action(self, do: object, build: str | None, to: int | object) -> Action:
        self.init()
        return Action(do=do, _build=build, to=self._state(to))


@dataclasses.dataclass
class ManagerDefaultProxy(AbstractManagerProxy, ManagerDefaultProxyInterface):
    def _on(self, /, *, do: object, build: str | None, to: int | object) -> ManagerProxy:
        action = self._action(do, build, to)
        self.manager.default = action
        return ManagerProxy(flow=self.flow, state=action.to, entry=self.entry)

    def success(self, /, *, do=EXCLUDE, build=None) -> None:
        pass

    def failure(self, /, *, do=EXCLUDE, build=None) -> None:
        pass

    def build(self: _I, build: str, /, *, do=NOTHING, to=ENTRY) -> ManagerProxy:
        return self._on(do=do, to=to, build=build)

    def match(self: _I, /, *, do=INCLUDE, to=NEW) -> ManagerProxy:
        return self._on(do=do, to=to, build=None)

    def repeat(self: _I, /, *, do=INCLUDE, build=None) -> ManagerProxy:
        return self._on(do=do, build=build, to=STAY)


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

    def _action(self, do: object, build: str | None, to: int | object) -> Action:
        self.init()
        to = self._state(to)
        return Action(do=do, _build=build, to=to)

    def _on(self, chars: str, /, *, do: object, build: str | None, to: int | object) -> ManagerProxy:
        action = self._action(do, build, to)
        self.flow.managers[self.state].handlers.append(Handler(Condition(chars), action))
        return ManagerProxy(flow=self.flow, state=action.to, entry=self.entry)

    def success(self, chars: str, /, *, do=EXCLUDE, build=None) -> None:
        self._on(chars, do=do, build=build, to=VALID)

    def failure(self, chars: str, /, *, do=EXCLUDE, build=None) -> None:
        self._on(chars, do=do, build=build, to=ERROR)

    def build(self, chars: str, build: str, /, *, do=INCLUDE, to=ENTRY) -> ManagerProxy:
        return self._on(chars, do=do, build=build, to=to)

    def match(self, chars: str, /, *, do=INCLUDE, to=NEW) -> ManagerProxy:
        return self._on(chars, do=do, to=to, build=None)

    def repeat(self, chars: str, /, *, do=INCLUDE, build=None) -> ManagerProxy:
        return self._on(chars, do=do, build=build, to=STAY)

    ####################################################################################################################
    # COMPOUNDS
    ####################################################################################################################

    def optional(self, chars: str, /, *, build=None, to=NEW):
        if build is None:
            self.match(chars, do=INCLUDE, to=to)
            return self.default.match(do=NOTHING, to=to)
        else:
            self.build(chars, build, do=INCLUDE, to=to)
            return self.default.build(build, do=NOTHING, to=to)

    def sequence(self, *seq_chars: str, do=INCLUDE, build=None, to=None):
        cur = self

        for chars in seq_chars[:-1]:
            cur = cur.match(chars, do=do)

        if build is None:
            if to is None:
                to = NEW
            return cur.match(seq_chars[-1], do=do, to=to)
        else:
            if to is None:
                to = ENTRY
            return cur.build(seq_chars[-1], build, do=do, to=to)

    def repeat_plus(self, chars: str, /, *, do=INCLUDE, build=None) -> ManagerProxy:
        return self.match(chars).repeat(chars, do=do, build=build)

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
            manager.default = Action(do=INCLUDE, to=err_1.state)

        # if not manager.verify(self.eot()):
        #     condition = Condition(self.eot())
        #     action = Action(do=EXCLUDE, _build=manager.default._build, to=VALID)
        #     handler = Handler(condition, action)
        #     manager.handlers.append(handler)
