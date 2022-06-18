from __future__ import annotations

import dataclasses
import functools

from .abstract import AbstractProxy
from .core import *
from .interfaces import ProxyInterface, DefaultProxyInterface

__all__ = [
    'DefaultProxy',
    'Proxy',
]


@dataclasses.dataclass
class DefaultProxy(AbstractProxy, DefaultProxyInterface):
    def _on(self, params: Params, to: int | object) -> Proxy:
        action = self._action(params, to)
        self.manager.default = action
        return Proxy(flow=self.flow, state=action.to, entry=self.entry)
    
    def success(self, /, *, options=EXCLUDE, build='') -> None:
        params = Params(options=options, build=build)
        self._on(params, to=VALID)
    
    def failure(self, /, *, options=EXCLUDE, build='') -> None:
        params = Params(options=options, build=build)
        self._on(params, to=ERROR)
    
    def build(self, build: str, /, *, options=0, to=ENTRY) -> Proxy:
        options |= CLEAR
        params = Params(options=options, build=build)
        return self._on(params, to)
    
    def match(self, /, *, options=INCLUDE, to=NEW) -> Proxy:
        options &= INCLUDE  # we remove the CLEAR option.
        params = Params(options=options, build='')
        return self._on(params, to=to)
    
    def repeat(self, /, *, options=INCLUDE, build='') -> Proxy:
        if build:
            options |= CLEAR
        params = Params(options=options, build=build)
        return self._on(params, to=STAY)

    def goto(self, to: int | object) -> Proxy:
        return self._on(params=Params(options=0, build=''), to=to)


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
    
    def _action(self, params: Params, to: int | object) -> Action:
        self.init()
        to = self._state(to)
        return Action(params=params, to=to)
    
    def _on(self, chars: str, options: int, build: str, to: int | object) -> Proxy:
        params = Params(options=options, build=build)
        action = self._action(params, to)
        self.add_handler(Handler(Condition(chars), action))
        return Proxy(flow=self.flow, state=action.to, entry=self.entry)
    
    def success(self, chars: str, /, *, options=INCLUDE, build='') -> None:
        if build:
            options |= CLEAR
        self._on(chars, options, build, to=VALID)
    
    def failure(self, chars: str, /, *, options=INCLUDE, build='') -> None:
        if build:
            options |= CLEAR
        self._on(chars, options, build, to=ERROR)
    
    def build(self, chars: str, build: str, /, *, options=INCLUDE, to=ENTRY) -> Proxy:
        options |= CLEAR
        return self._on(chars=chars, options=options, build=build, to=to)
    
    def match(self, chars: str, /, *, options=INCLUDE, to=NEW) -> Proxy:
        options &= INCLUDE  # we remove the CLEAR option.
        return self._on(chars=chars, options=options, build='', to=to)
    
    def repeat(self, chars: str, /, *, options=INCLUDE, build='') -> Proxy:
        if build:
            options |= CLEAR
        return self._on(chars=chars, options=options, build=build, to=STAY)
    
    ####################################################################################################################
    # COMPOUNDS
    ####################################################################################################################
    
    def optional(self, chars: str, /, *, build=None, to=NEW):
        if build is None:
            self.match(chars, to=to)
            return self.default.match(options=0, to=to)
        else:
            self.build(chars, build, to=to)
            return self.default.build(build, to=to)
    
    def sequence(self, *seq_chars: str, options=INCLUDE, build='', to=None):
        cur = self
        
        for chars in seq_chars[:-1]:
            cur = cur.match(chars, options=options)
        
        if build is None:
            if to is None:
                to = NEW
            return cur.match(seq_chars[-1], options=options, to=to)
        else:
            if to is None:
                to = ENTRY
            return cur.build(seq_chars[-1], build, options=options, to=to)
    
    def repeat_plus(self, chars: str, /, *, options=INCLUDE, build='') -> Proxy:
        return self.match(chars).repeat(chars, options=options, build=build)
    
    def build_bloc(self, at_chars: str, to_chars: str, build: str, to=ENTRY) -> Proxy:
        return self.match(at_chars).default.repeat().build(to_chars, build, to=to)
