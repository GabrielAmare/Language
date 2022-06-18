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
    def _on(self, options: int, build: str, to: int | object) -> Proxy:
        params = Params(options, build)
        action = self._action(params, to)
        self.manager.default = action
        return Proxy(flow=self.flow, state=action.to, entry=self.entry)
    
    def success(self, /, *, options=EXCLUDE, build='') -> None:
        self._on(options=options, build=build, to=VALID)
    
    def failure(self, /, *, options=EXCLUDE, build='') -> None:
        self._on(options=options, build=build, to=ERROR)
    
    def build(self, build: str, /, *, options=0, to=ENTRY) -> Proxy:
        options |= CLEAR
        return self._on(options=options, build=build, to=to)
    
    def match(self, /, *, options=INCLUDE, to=NEW) -> Proxy:
        options &= INCLUDE  # we remove the CLEAR option.
        return self._on(options=options, build='', to=to)
    
    def repeat(self, /, *, options=INCLUDE, build='') -> Proxy:
        if build:
            options |= CLEAR
        return self._on(options=options, build=build, to=STAY)
    
    def goto(self, to: int | object) -> Proxy:
        return self._on(options=0, build='', to=to)


@dataclasses.dataclass
class Proxy(AbstractProxy, ProxyInterface):
    @property
    def handlers(self) -> list[Handler]:
        return self.flow.managers[self.state].handlers
    
    @functools.cached_property
    def default(self):
        return DefaultProxy(flow=self.flow, state=self.state, entry=self.entry)
    
    def proxy(self, to=NEW, entry=ENTRY) -> Proxy:
        return Proxy(flow=self.flow, state=self._state(to), entry=self._state(entry))
    
    def add_case(self, condition: Condition, params: Params, to: object) -> int:
        self.init()
        to = self._state(to)
        
        add = True
        for handler in self.handlers:
            if not handler.condition.shadows(condition):
                continue
            
            if handler.condition == condition and handler.action.params == params:
                if to == handler.action.to:
                    add = False
                    continue
                
                if to not in self.flow.managers:
                    add = False
                    to = handler.action.to
                    continue
                
                raise ValueError(f"[2] {handler.condition} is shadowing {condition}")
            
            raise ValueError(f"[1] {handler.condition} is shadowing {condition}")
        
        if add:
            action = Action(params=params, to=to)
            handler = Handler(condition=condition, action=action)
            self.flow.managers[self.state].handlers.append(handler)
        
        return to
    
    def new(self) -> int:
        return self.flow.new_state()
    
    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()
    
    def _on(self, chars: str, options: int, build: str, to: int | object) -> Proxy:
        params = Params(options=options, build=build)
        to = self.add_case(Condition(chars), params, to)
        return Proxy(flow=self.flow, state=to, entry=self.entry)
    
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
